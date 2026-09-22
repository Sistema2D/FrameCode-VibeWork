"""Math, provenance and failure boundary tests; synthetic evidence is not efficacy."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from loop_contract_fcvw import protocol, strict_json
from loop_metrics_fcvw import digest, evaluate, markdown, write_report


def config():
    task = dict(id='security-audit', split='evaluation', origin='real', execution_kind='agent', domain='security',
                source_revision='revision-a', acceptance_ref='acceptance-v1', labels_ref='labels-v1', labeler='reviewer',
                label_basis='independent', labeled_at='2026-09-20T10:00:00Z', mandatory_paths=['AGENTS.md'],
                useful_chunks=['useful#1'], forbidden_chunks=['secret#1'])
    return dict(schema='fcvw/loop-protocol@1', id='unit-protocol', frozen_at='2026-09-20T11:00:00Z',
                registration='prospective', baseline='baseline', repetitions=1, min_pairs=2,
                limits=dict(max_iterations=10, max_wall_ms=100000, max_tokens=100000),
                margins=dict(validation_defect_rate=.05, human_correction_rate=.05, useful_recall=.05),
                followup_ms=1000, primary_metric='TVC', analysis_ref='analysis-v1',
                strategies=[dict(id=s, mode='delivered', delivered_strategy=s, config_ref=s+'-config') for s in ('baseline', 'budget')],
                tasks=[task, {**task, 'id': 'migration-audit', 'domain': 'migration'}])


def iteration(cfg, task='security-audit', strategy='baseline', index=1, state='validated', validation='pass', tokens=100):
    run_id = task+'-'+strategy
    start = datetime(2026, 9, 21, tzinfo=timezone.utc) + timedelta(seconds=index-1)
    return dict(schema='fcvw/loop-run@1', kind='iteration', event_id=f'iteration-{index}', run_id=run_id,
                protocol_digest=digest(cfg), task_id=task, strategy=strategy, repetition=1, iteration=index,
                source_revision='revision-a', initial_state_ref='same-clean-state', operator='executor', model='test-model',
                tokenizer='test-tokenizer', measurement_note='Synthetic unit fixture; no real provider was called',
                started_at=start.isoformat(), ended_at=(start+timedelta(seconds=1)).isoformat(), validation=validation,
                state=state, stop_reason=None if state=='running' else state, acceptance_satisfied=state=='validated', blockers=0,
                qa=dict(divergences=0, asked=0, pending=0), failure_signature='error-A' if validation=='fail' else None,
                evidence_ref='synthetic-validation', usage_complete=True, context_complete=True, human_corrected=False,
                calls=[dict(call_id=f'{run_id}-call-{index}', input_tokens=tokens, output_tokens=20, token_source='provider', usage_ref='synthetic-usage')],
                contexts=[dict(delivery_id=f'{run_id}-delivery-{index}', mandatory_paths=['AGENTS.md'],
                               chunks=[dict(chunk_id='useful#1',tokens=30),dict(chunk_id='irrelevant#1',tokens=70)],
                               token_source='tokenizer',evidence_ref='synthetic-context')],
                durations_ms=dict(retrieval=10, model=100, tools=100, validation=50, human_wait=0))


def followup(row, defect=False, regression=False):
    return dict(schema='fcvw/loop-run@1',kind='followup',event_id='followup-1',run_id=row['run_id'],
                observed_until=(datetime.fromisoformat(row['ended_at'])+timedelta(seconds=2)).isoformat(),
                defect=defect,regression=regression,evidence_ref='synthetic-followup')


class LoopMetricsTests(unittest.TestCase):
    def setUp(self):
        self.config = config()

    def test_exact_cost_iterations_rework_and_timing(self):
        rows = [iteration(self.config,index=1,state='running',validation='fail'),
                iteration(self.config,index=2,state='running',validation='fail'), iteration(self.config,index=3)]
        report = evaluate(self.config, rows+[followup(rows[-1])])
        result = report['runs'][0]
        self.assertEqual((result['TVC'],result['IVC'],result['TTVS_ms']), (360,3,3000))
        self.assertAlmostEqual(result['RTR'],2/3)
        self.assertEqual(result['RFR'],.5)
        self.assertEqual(result['retrieval']['UCTR'],.3)
        self.assertFalse(result['FPV'])

    def test_missing_and_estimated_usage_is_not_zero_or_measured_tvc(self):
        for source, tokens in (('provider',None),('estimate',50),('unavailable',None)):
            with self.subTest(source=source):
                row=iteration(self.config)
                row['calls'][0].update(token_source=source,input_tokens=tokens,output_tokens=tokens)
                result=evaluate(self.config,[row])['runs'][0]
                self.assertIsNone(result['TVC']); self.assertIsNone(result['RTR'])
                self.assertIn('provider_usage_incomplete_or_estimated',result['evidence_gaps'])

    def test_partial_call_inventory_does_not_claim_full_cost(self):
        row=iteration(self.config); row['usage_complete']=False
        result=evaluate(self.config,[row])['runs'][0]
        self.assertEqual(result['known_provider_tokens_lower_bound'],120)
        self.assertIsNone(result['tokens_accumulated'])

    def test_cost_requires_complete_billing_and_same_currency(self):
        a=iteration(self.config,state='running',validation='fail');b=iteration(self.config,index=2)
        for row in (a,b):row['calls'][0].update(cost=.1,currency='USD',cost_ref='synthetic-bill')
        result=evaluate(self.config,[a,b])['runs'][0]
        self.assertEqual(result['monetary_cost'],dict(amount=.2,currency='USD'))
        b['calls'][0]['currency']='BRL'
        self.assertIsNone(evaluate(self.config,[a,b])['runs'][0]['monetary_cost'])

    def test_missing_context_cannot_claim_complete_observation(self):
        row=iteration(self.config);row['contexts']=[]
        with self.assertRaisesRegex(ValueError,'complete context'):evaluate(self.config,[row])
        row['context_complete']=False
        self.assertIn('actual_context_incompletely_observed',evaluate(self.config,[row])['runs'][0]['evidence_gaps'])

    def test_interrupted_and_not_started_runs_remain_visible(self):
        row=iteration(self.config,state='blocked',validation='not_run')
        result=evaluate(self.config,[row])
        run=result['runs'][0]
        self.assertEqual(run['tokens_accumulated'],120)
        self.assertIsNone(run['TVC']); self.assertIsNone(run['IVC']); self.assertIsNone(run['TTVS_ms'])
        self.assertEqual(len(result['missing_runs']),3)
        self.assertEqual(result['cohorts'][0]['FPVR'],0)
        self.assertEqual(result['readiness'],'inconclusive')

    def test_exact_duplicates_and_reordered_resume_are_idempotent(self):
        a=iteration(self.config,state='running',validation='fail')
        b=iteration(self.config,index=2)
        expected=evaluate(self.config,[a,b])
        resumed=evaluate(self.config,[b,a,deepcopy(a)])
        self.assertEqual(expected['events_digest'],resumed['events_digest'])
        self.assertEqual(expected['runs'],resumed['runs'])
        self.assertEqual(resumed['duplicate_events_ignored'],1)

    def test_conflicting_event_and_reused_call_rejected(self):
        a=iteration(self.config,state='running',validation='fail')
        b=deepcopy(a); b['calls'][0]['input_tokens']=999
        with self.assertRaisesRegex(ValueError,'conflicting'):
            evaluate(self.config,[a,b])
        b=iteration(self.config,index=2); b['calls'][0]['call_id']=a['calls'][0]['call_id']
        with self.assertRaisesRegex(ValueError,'reused'):
            evaluate(self.config,[a,b])

    def test_missing_iterations_and_post_terminal_execution_rejected(self):
        for rows in ([iteration(self.config,index=2)],
                     [iteration(self.config),iteration(self.config,index=2)]):
            with self.assertRaises(ValueError): evaluate(self.config,rows)

    def test_cannot_hide_duplicate_execution_with_new_run_id(self):
        a=iteration(self.config); b=deepcopy(a)
        b['run_id']='another'; b['calls'][0]['call_id']='another-call'; b['contexts'][0]['delivery_id']='another-delivery'
        with self.assertRaisesRegex(ValueError,'duplicate planned'):
            evaluate(self.config,[a,b])

    def test_false_completion_and_pending_qa_decision_rejected(self):
        for changes in (dict(acceptance_satisfied=False),dict(blockers=1),dict(validation='not_run'),
                        dict(qa=dict(divergences=1,asked=1,pending=1)),dict(qa=dict(divergences=1,asked=0,pending=1))):
            row=iteration(self.config);row.update(changes)
            with self.assertRaisesRegex(ValueError,'false validated'):
                evaluate(self.config,[row])

    def test_required_context_and_forbidden_hits_fail_closed(self):
        row=iteration(self.config); row['contexts'][0]['mandatory_paths']=[]
        row['contexts'][0]['chunks'].append(dict(chunk_id='secret#1',tokens=1))
        report=evaluate(self.config,[row])
        self.assertEqual(report['readiness'],'invariant_violation')
        self.assertEqual(set(report['invariant_violations'][0]['findings']),{'mandatory_context_missing','forbidden_context_delivered'})

    def test_shadow_proposal_is_not_actual_execution(self):
        self.config['strategies'][1].update(mode='shadow',delivered_strategy='baseline')
        row=iteration(self.config,strategy='budget')
        row['contexts'][0]['proposed_chunks']=[dict(chunk_id='secret#1',tokens=50)]
        report=evaluate(self.config,[row])
        self.assertEqual(report['runs'][0]['retrieval']['forbidden_hits'],[])
        self.assertEqual(report['runs'][0]['proposal']['forbidden_hits'],['secret#1'])
        self.assertIn('shadow_only_does_not_test_changed_delivery',report['evidence_gaps'])
        self.assertEqual(report['comparisons'][0]['attribution'],'same_delivery_only_overhead_or_noise')

    def test_zero_denominators_and_no_failure(self):
        row=iteration(self.config);row['calls']=[];row['contexts'][0]['chunks']=[]
        result=evaluate(self.config,[row])['runs'][0]
        self.assertEqual(result['TVC'],0);self.assertEqual(result['RTR'],0)
        self.assertIsNone(result['RFR']);self.assertIsNone(result['retrieval']['UCTR'])
        self.assertEqual(result['retrieval']['optional_tokens'],0)

    def test_estimated_context_ratio_is_separate(self):
        row=iteration(self.config);row['contexts'][0]['token_source']='estimate'
        report=evaluate(self.config,[row]); summary=report['cohorts'][0]
        self.assertEqual(summary['UCTR']['n'],0)
        self.assertEqual(summary['UCTR_estimated']['median'],.3)

    def test_protocol_identity_provenance_and_revision_checked(self):
        row=iteration(self.config)
        self.config['limits']['max_tokens']+=1
        with self.assertRaisesRegex(ValueError,'digest'):evaluate(self.config,[row])
        row=iteration(self.config);row['source_revision']='different'
        with self.assertRaisesRegex(ValueError,'revision'):evaluate(self.config,[row])
        row=iteration(self.config);row['operator']='reviewer'
        self.assertIn('independent_review_not_established',evaluate(self.config,[row])['runs'][0]['evidence_gaps'])

    def test_pre_registration_and_real_agent_claims_are_not_inferred(self):
        self.config['registration']='retrospective';self.config['tasks'][0]['execution_kind']='deterministic_audit'
        self.config['frozen_at']='2026-09-22T00:00:00Z'
        report=evaluate(self.config,[iteration(self.config)])
        self.assertIn('retrospective_protocol',report['evidence_gaps'])
        self.assertIn('not_real_agent_execution',report['runs'][0]['evidence_gaps'])
        self.assertIn('protocol_or_labels_not_frozen_before_run',report['runs'][0]['evidence_gaps'])

    def test_followup_quality_never_rewrites_first_completion(self):
        row=iteration(self.config);report=evaluate(self.config,[row,followup(row,True,True)])
        result=report['runs'][0]
        self.assertTrue(result['FPV']);self.assertTrue(result['late_defect']);self.assertTrue(result['late_regression'])
        self.assertEqual(result['TVC'],120)
        bad=followup(row);bad['run_id']='unknown'
        with self.assertRaisesRegex(ValueError,'without run'):evaluate(self.config,[bad])

    def test_complete_pairs_are_ready_for_review_not_promotion(self):
        rows=[]
        for task in self.config['tasks']:
            for strategy in ('baseline','budget'):
                row=iteration(self.config,task=task['id'],strategy=strategy,tokens=100 if strategy=='baseline' else 80)
                rows += [row,followup(row)]
        report=evaluate(self.config,rows)
        self.assertEqual(report['readiness'],'ready_for_independent_review')
        compare=report['comparisons'][0]['metrics']['TVC']
        self.assertEqual(compare['candidate_minus_baseline_mean'],-20)
        self.assertEqual(compare['paired_tasks'],2)
        self.assertEqual(report['dependent_experiments']['issue_57'],'not_authorized_by_tool')

    def test_incompatible_pair_not_counted(self):
        a=iteration(self.config);b=iteration(self.config,strategy='budget');b['initial_state_ref']='different'
        comparison=evaluate(self.config,[a,b])['comparisons'][0]
        self.assertEqual(comparison['paired_runs'],0);self.assertEqual(comparison['incompatible_pairs'],1)

    def test_strict_inputs_reject_raw_payloads_invalid_numbers_and_duplicates(self):
        for raw in ('{"x":1,"x":2}','{"x":NaN}'):
            with self.assertRaises(ValueError):strict_json(raw)
        for field,value in (('prompt','private prompt'),('blockers',True),('started_at','no-timezone')):
            row=iteration(self.config);row[field]=value
            with self.assertRaises(ValueError):evaluate(self.config,[row])
        invalid=config();invalid['strategies'][1]['config_ref']='baseline-config'
        with self.assertRaisesRegex(ValueError,'duplicate strategy'):protocol(invalid)

    def test_limits_overlap_and_missing_measurements(self):
        row=iteration(self.config);row['durations_ms']['tools']=2000
        with self.assertRaisesRegex(ValueError,'phase duration'):evaluate(self.config,[row])
        self.config['limits']['max_tokens']=10
        report=evaluate(self.config,[iteration(self.config)])
        self.assertIn('declared_limit_exceeded',report['invariant_violations'][0]['findings'])

    def test_planned_expansion_bound_and_context_denominators(self):
        oversized = deepcopy(self.config)
        oversized['repetitions'] = 100
        oversized['tasks'] = [{**oversized['tasks'][0], 'id': str(i)} for i in range(251)]
        with self.assertRaisesRegex(ValueError, 'planned executions'):
            protocol(oversized)
        row = iteration(self.config)
        row['contexts'][0]['token_source'] = 'estimate'
        cohort = evaluate(self.config, [row])['cohorts'][0]
        self.assertEqual((cohort['UCTR']['n'], cohort['UCTR']['missing']), (0, 1))
        self.assertEqual((cohort['UCTR_estimated']['n'], cohort['UCTR_estimated']['missing']), (1, 0))

    def test_cli_roundtrip_and_output_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'protocol.json';runs=root/'runs.jsonl'
            p.write_text(json.dumps(self.config),encoding='utf-8');runs.write_text(json.dumps(iteration(self.config))+'\n',encoding='utf-8')
            result=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('loop_metrics_fcvw.py')),
                                   '--protocol',str(p),'--runs',str(runs),'--check'],capture_output=True,text=True)
            self.assertEqual(result.returncode,1)
            report=json.loads(result.stdout);self.assertEqual(report['readiness'],'inconclusive')
            binding=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('loop_metrics_fcvw.py')),
                                    '--protocol',str(p),'--show-protocol-digest'],capture_output=True,text=True)
            self.assertEqual(binding.returncode,0)
            self.assertEqual(binding.stdout.strip(),digest(self.config))
            self.assertIn('TVC median',markdown(report))
            for output in (root/'AGENTS.md',p):
                with self.assertRaises(ValueError):write_report(output,'data',root,[p,runs])
            out=root/'.fcvw-cache/report.json';write_report(out,'data',root,[p,runs])
            self.assertEqual(out.read_text(),'data')


if __name__ == '__main__':
    unittest.main()
