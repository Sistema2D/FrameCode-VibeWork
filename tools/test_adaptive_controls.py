"""Synthetic boundary proofs, never empirical evidence of adaptive benefit."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from adaptive_control_fcvw import assess, control, activation, runtime, seal, validate_runtime
from adaptive_learning_fcvw import replay, validate_state, select
from build_context_index import build_index
from check_fcvw import snapshot
from loop_metrics_fcvw import digest
from test_adaptive_routing import graph
from test_loop_metrics import config as loop_config, iteration, followup

NOW = datetime(2026, 9, 23, 12, tzinfo=timezone.utc)


def fixture():
    protocol = loop_config()
    protocol['tasks'].append({**protocol['tasks'][0], 'id':'training', 'split':'adjustment'})
    events = []
    for task in protocol['tasks']:
        for strategy in ('baseline','budget'):
            row = iteration(protocol, task=task['id'], strategy=strategy)
            events.extend((row, followup(row)))
    return dict(schema='fcvw/adaptive-control@1', id='synthetic-control', enabled=True, phase='limited',
                issued_at='2026-09-22T00:00:00Z', expires_at='2099-01-01T00:00:00Z', authorized_by='fixture-reviewer',
                authorization_ref='synthetic-authorization', review_decision='approve_limited', review_ref='synthetic-review',
                source_digest='revision-a', index_digest='index-a', scope=['live-task'], mandatory_paths=['AGENTS.md'],
                eligible_chunks={'useful#1':dict(path='a.md',chunk_hash='hash-a'), 'irrelevant#1':dict(path='b.md',chunk_hash='hash-b')},
                limits=dict(optional_tokens=2000,max_iterations=20,max_wall_ms=100000,max_tokens=10000,repeat_failure_limit=3),
                learning=dict(step=.1,bound=.2,decay=.9,max_feedback=20), feedback_authorities=['human-reviewer'],
                rollback=dict(window=2,tvc_ratio=1.2,rtr_delta=.1,rfr_delta=.1,defect_delta=.05),
                protocol=protocol, events=events, evaluation_strategy='budget')


def feedback():
    return dict(schema='fcvw/adaptive-feedback@1',id='f1',recorded_at='2026-09-23T10:00:00Z',source='human',
                author='human-reviewer',review_ref='synthetic-human-review',authorization_ref='synthetic-authorization',
                task_id='training',run_id='training-baseline',chunk_id='useful#1',verdict='useful',evidence_ref='synthetic-check')


def observed():
    return dict(run_id='live-1',task_id='live-task',observed_at=NOW.isoformat(),iterations=0,elapsed_ms=0,
                tokens=0,token_source='provider',usage_complete=True,qa_pending=0,safety_block=False,checkpoints=[],quality_windows=[])


def candidates():
    return [dict(path=path,chunk_id=chunk,chunk_hash=hashed,score=1,excerpt='public text '+path,excerpt_complete=True)
            for path,chunk,hashed in (('a.md','useful#1','hash-a'),('b.md','irrelevant#1','hash-b'))]


class AdaptiveControlTests(unittest.TestCase):
    def setUp(self):
        self.cfg=fixture()

    def choose(self, cfg=None, obs=None, **kwargs):
        cfg=cfg or self.cfg
        with patch('adaptive_learning_fcvw.structural_graph', return_value=graph()):
            return select(cfg,runtime(cfg,obs or observed()),candidates(),['AGENTS.md'],root=Path('.'),
                          source_digest='revision-a',index_digest='index-a',now=NOW,**kwargs)

    def test_assessment_recomputes_evidence_without_authorizing_promotion(self):
        result=assess(self.cfg['protocol'],self.cfg['events'],'budget')
        self.assertEqual(result['decision'],'eligible_for_review')
        self.assertEqual(result['loop_report']['dependent_experiments']['issue_57'],'not_authorized_by_tool')
        self.cfg['events'][0]['usage_complete']=False
        self.assertEqual(assess(self.cfg['protocol'],self.cfg['events'],'budget')['decision'],'inconclusive')

    def test_negative_and_late_quality_prevent_promotion(self):
        for late in ('defect','regression'):
            cfg=fixture()
            for row in cfg['events']:
                if row['kind']=='followup' and 'budget' in row['run_id']: row[late]=True
            result=assess(cfg['protocol'],cfg['events'],'budget')
            self.assertEqual(result['decision'],'inconclusive')
            self.assertIn('late_'+late+'_noninferiority_not_established',result['reasons'])
        self.cfg['events'][0]['contexts'][0]['mandatory_paths']=[]
        self.assertEqual(assess(self.cfg['protocol'],self.cfg['events'],'budget')['decision'],'reject')

    def test_labels_or_shadow_cannot_substitute_active_evidence(self):
        for task in self.cfg['protocol']['tasks']: task['label_basis']='author'
        for row in self.cfg['events']:
            if row['kind']=='iteration':row['protocol_digest']=digest(self.cfg['protocol'])
        self.assertEqual(assess(self.cfg['protocol'],self.cfg['events'],'budget')['decision'],'inconclusive')
        cfg=fixture();cfg['protocol']['strategies'][1].update(mode='shadow',delivered_strategy='baseline')
        for row in cfg['events']:
            if row['kind']=='iteration':row['protocol_digest']=digest(cfg['protocol'])
        self.assertIn('shadow_is_not_active_evidence',assess(cfg['protocol'],cfg['events'],'budget')['reasons'])

    def test_feedback_replay_is_deduplicated_ordered_and_bounded(self):
        a=feedback();b={**a,'id':'f2','chunk_id':'irrelevant#1','verdict':'harmful'}
        first=replay(self.cfg,[a,b,a]);second=replay(self.cfg,[b,a])
        self.assertEqual(first,second)
        self.assertEqual(first['weights'],{'useful#1':.09,'irrelevant#1':-.1})
        self.cfg['learning']['bound']=.05
        self.assertTrue(all(abs(v)<=.05 for v in replay(self.cfg,[a,b])['weights'].values()))

    def test_conflicting_or_renamed_feedback_cannot_reward_twice(self):
        a=feedback()
        for b in ({**a,'evidence_ref':'conflict'}, {**a,'id':'renamed'}):
            with self.assertRaises(ValueError):replay(self.cfg,[a,b])

    def test_holdout_unknown_unvalidated_and_unmeasured_cannot_train(self):
        a=feedback()
        for task,run in (('security-audit','security-audit-baseline'),('unknown','training-baseline')):
            with self.assertRaises(ValueError):replay(self.cfg,[{**a,'task_id':task,'run_id':run}])
        self.cfg['events'][-4]['usage_complete']=False
        with self.assertRaisesRegex(ValueError,'complete validated'):replay(self.cfg,[a])

    def test_feedback_poisoning_authority_and_raw_payload_denied(self):
        for key,value in (('source','click'),('author','attacker'),('authorization_ref','forged'),
                          ('verdict','no_correction'),('prompt','private'),('chunk_id','AGENTS.md#document'),
                          ('recorded_at','2100-01-01T00:00:00Z')):
            with self.subTest(key=key),self.assertRaises(ValueError):replay(self.cfg,[{**feedback(),key:value}])

    def test_state_reset_export_rollback_and_forgery(self):
        old=replay(self.cfg,[]);new=replay(self.cfg,[feedback()])
        self.assertEqual(validate_state(deepcopy(new),self.cfg),new)
        self.assertEqual(validate_state(old,self.cfg)['weights'],{})
        new['weights']['useful#1']=.2
        with self.assertRaises(ValueError):validate_state(new,self.cfg)
        new=seal({k:v for k,v in new.items() if k!='checksum'})
        with self.assertRaisesRegex(ValueError,'replay'):validate_state(new,self.cfg)

    def test_controls_are_bounded_explicit_and_expire(self):
        for key,value in (('enabled',False),('review_decision','reject'),('phase','operational'),('expires_at','2026-09-22T01:00:00Z')):
            cfg=deepcopy(self.cfg);cfg[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):activation(cfg,NOW)
        self.cfg['learning']['step']=float('nan')
        with self.assertRaises(ValueError):control(self.cfg)

    def test_active_selection_preserves_mandatory_and_budget(self):
        decision=self.choose(state=replay(self.cfg,[feedback()]),top_k=1)
        self.assertEqual(decision['status'],'active')
        self.assertEqual(decision['results'][0]['chunk_id'],'useful#1')
        self.assertNotIn('AGENTS.md',[r['path'] for r in decision['results']])
        self.assertLessEqual(decision['selection']['estimated_optional_tokens'],2000)
        self.assertEqual(self.choose(budget=0)['results'],[])

    def test_shadow_and_disable_never_change_actual_delivery(self):
        for mode in ('shadow','disabled'):
            decision=self.choose(mode=mode)
            self.assertTrue(decision['baseline_preserved']);self.assertIsNone(decision['results'])

    def test_corrupt_state_falls_back_but_invalid_control_blocks(self):
        decision=self.choose(state={'checksum':'bad'})
        self.assertEqual(decision['status'],'fallback');self.assertFalse(decision['execution_blocked'])
        self.cfg['index_digest']='other-index'
        self.assertTrue(self.choose()['execution_blocked'])

    def test_unknown_candidates_and_changed_hash_do_not_enter_selection(self):
        self.cfg['eligible_chunks'].pop('irrelevant#1')
        self.assertEqual(len(self.choose()['results']),1)
        self.cfg['eligible_chunks']['useful#1']['chunk_hash']='stale'
        self.assertEqual(self.choose()['status'],'fallback')

    def test_qa_safety_and_unknown_tokens_block_even_after_rollback(self):
        for key,value in (('qa_pending',1),('safety_block',True),('tokens',None)):
            obs=observed();obs[key]=value
            self.assertTrue(self.choose(obs=obs,mode='disabled')['execution_blocked'])
            previous=runtime(self.cfg,obs)
            current=runtime(self.cfg,observed(),previous)
            self.assertTrue(current['blocked'])

    def test_stagnation_not_run_and_cosmetic_actions_do_not_reset_streak(self):
        obs=observed();obs['checkpoints']=[dict(validation='fail',signature='same'),dict(validation='not_run',signature=None),
                                         dict(validation='fail',signature='same'),dict(validation='fail',signature='same')]
        obs['iterations']=4
        self.assertEqual(runtime(self.cfg,obs)['reason'],'stagnation_review_required')
        obs['checkpoints'][1]={'validation':'pass','signature':None}
        self.assertFalse(runtime(self.cfg,obs)['blocked'])

    def test_stop_latch_and_append_only_runtime(self):
        obs=observed();obs['qa_pending']=1;old=runtime(self.cfg,obs)
        continued=runtime(self.cfg,observed(),old)
        self.assertTrue(continued['blocked'])
        bad=deepcopy(continued);bad['blocked']=False;bad['reason']=None
        bad=seal({k:v for k,v in bad.items() if k!='checksum'})
        # A recomputed checksum is not authentication; append must preserve prior latch.
        self.assertTrue(runtime(self.cfg,bad['observation'],continued)['blocked'])
        obs=observed();obs['checkpoints']=[dict(validation='fail',signature='x')];obs['iterations']=1
        old=runtime(self.cfg,obs)
        obs['checkpoints'][0]['signature']='changed'
        with self.assertRaisesRegex(ValueError,'history rewritten'):runtime(self.cfg,obs,old)

    def test_budgets_drift_and_persistent_quality_trigger_stop(self):
        for key,value in (('tokens',10000),('elapsed_ms',100000),('iterations',20)):
            obs=observed();obs[key]=value
            if key=='iterations':obs['checkpoints']=[dict(validation='pass',signature=None)]*20
            self.assertTrue(runtime(self.cfg,obs)['blocked'])
        obs=observed();point=dict(tvc_ratio=1.3,rtr_delta=0,rfr_delta=0,defect_delta=0)
        obs['quality_windows']=[point]
        self.assertFalse(runtime(self.cfg,obs)['blocked'])
        obs['quality_windows'].append(point)
        self.assertEqual(runtime(self.cfg,obs)['reason'],'persistent_quality_degradation')

    def test_runtime_binding_and_stale_wall_time(self):
        current=runtime(self.cfg,observed());self.cfg['id']='new-control'
        with self.assertRaises(ValueError):validate_runtime(current,self.cfg)
        obs=observed();obs['observed_at']='2026-09-22T12:00:00Z'
        self.assertTrue(self.choose(obs=obs)['execution_blocked'])

    def test_estimated_or_partial_runtime_usage_cannot_evade_budget(self):
        for changes in ({'token_source':'estimate'}, {'token_source':'tokenizer'}, {'usage_complete':False},
                        {'tokens':None,'token_source':'unavailable'}):
            obs={**observed(),**changes}
            self.assertEqual(runtime(self.cfg,obs)['reason'],'usage_unknown_or_estimated')
            self.assertTrue(self.choose(obs=obs)['execution_blocked'])
        obs={**observed(),'token_source':'unavailable'}
        with self.assertRaises(ValueError):runtime(self.cfg,obs)

    def test_cli_default_parity_and_missing_control_safe_failure(self):
        root=Path(__file__).resolve().parents[1]
        if root.name=='FCVW':root=root.parent
        tool=Path(__file__).with_name('retrieve_context.py')
        with tempfile.TemporaryDirectory() as tmp:
            index=Path(tmp)/'index.jsonl'
            index.write_text(''.join(json.dumps(r)+'\n' for r in build_index(root)),encoding='utf-8')
            cmd=[sys.executable,'-X','utf8','-B',str(tool),'--root',str(root),'--index',str(index),'--query','security','--session','security']
            baseline=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
            denied=subprocess.run(cmd+['--adaptive-mode','assist'],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual((baseline.returncode,denied.returncode),(0,1))
            a,b=json.loads(baseline.stdout),json.loads(denied.stdout)
            self.assertEqual(a['mandatory_paths'],b['mandatory_paths'])
            self.assertEqual(a['complementary_results'],b['complementary_results'])
            self.assertTrue(b['adaptive_experiment']['execution_blocked'])

    def test_cli_state_lifecycle_and_output_boundary(self):
        tool=Path(__file__).with_name('adaptive_learning_fcvw.py')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);cfg=folder/'control.json';fb=folder/'feedback.json'
            cfg.write_text(json.dumps(self.cfg),encoding='utf-8');fb.write_text(json.dumps([feedback()]),encoding='utf-8')
            def run(command,target,*args):
                return subprocess.run([sys.executable,'-B',str(tool),command,'--control',str(cfg),'--output',str(folder/target),*args],capture_output=True,text=True)
            self.assertEqual(run('replay','state.json','--feedback',str(fb)).returncode,0)
            self.assertEqual(run('export','export.json','--state',str(folder/'state.json')).returncode,0)
            self.assertEqual((folder/'state.json').read_bytes(),(folder/'export.json').read_bytes())
            self.assertEqual(run('reset','reset.json').returncode,0)
            self.assertEqual(run('rollback','restored.json','--state',str(folder/'export.json')).returncode,0)
            self.assertEqual((folder/'restored.json').read_bytes(),(folder/'export.json').read_bytes())
            self.assertEqual(run('reset','control.json').returncode,2)

    def test_cli_active_shadow_corrupt_state_and_blocked_rollback(self):
        root=Path(__file__).resolve().parents[1]
        if root.name=='FCVW':root=root.parent
        tool=Path(__file__).with_name('retrieve_context.py')
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);records=build_index(root);index=folder/'index.jsonl'
            index.write_text(''.join(json.dumps(r)+'\n' for r in records),encoding='utf-8')
            cfg=fixture();revision=snapshot(root)['tree_sha256']
            cfg['source_digest']=revision;cfg['index_digest']=hashlib.sha256(index.read_bytes()).hexdigest()
            for task in cfg['protocol']['tasks']:task['source_revision']=revision
            for row in cfg['events']:
                if row['kind']=='iteration':row.update(source_revision=revision,protocol_digest=digest(cfg['protocol']))
            cfg['eligible_chunks']={r['chunk_id']:dict(path=r['path'],chunk_hash=r['chunk_hash']) for r in records
                                     if r['path'] not in ('AGENTS.md','FCVW/CONTEXT_MAP.md') and r['retrieval_scope']=='routed'}
            cfgpath=folder/'control.json';cfgpath.write_text(json.dumps(cfg),encoding='utf-8')
            obs=observed();obs['observed_at']=datetime.now(timezone.utc).isoformat()
            rt=folder/'runtime.json';rt.write_text(json.dumps(runtime(cfg,obs)),encoding='utf-8')
            cmd=[sys.executable,'-X','utf8','-B',str(tool),'--root',str(root),'--index',str(index),'--query','security']
            baseline=json.loads(subprocess.check_output(cmd,encoding='utf-8'))
            args=['--adaptive-control',str(cfgpath),'--adaptive-runtime',str(rt)]
            active=subprocess.run(cmd+args+['--adaptive-mode','assist'],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(active.returncode,0,active.stderr+active.stdout)
            data=json.loads(active.stdout)
            self.assertEqual(data['adaptive_experiment']['status'],'active')
            self.assertTrue(all(r['excerpt_complete'] for r in data['complementary_results']))
            self.assertEqual(data['mandatory_paths'],baseline['mandatory_paths'])
            bad=folder/'bad.json';bad.write_text('not-json',encoding='utf-8')
            result=json.loads(subprocess.check_output(cmd+args+['--adaptive-mode','assist','--adaptive-state',str(bad)],encoding='utf-8'))
            self.assertEqual(result['complementary_results'],baseline['complementary_results'])
            self.assertEqual(result['adaptive_experiment']['status'],'fallback')
            shadow=json.loads(subprocess.check_output(cmd+args+['--adaptive-mode','shadow'],encoding='utf-8'))
            self.assertEqual(shadow['complementary_results'],baseline['complementary_results'])
            obs['qa_pending']=1;rt.write_text(json.dumps(runtime(cfg,obs)),encoding='utf-8')
            denied=subprocess.run(cmd+args+['--adaptive-mode','disabled'],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(denied.returncode,1)
            self.assertEqual(json.loads(denied.stdout)['adaptive_experiment']['reason'],'qa_user_decision_required')


if __name__=='__main__':
    unittest.main()
