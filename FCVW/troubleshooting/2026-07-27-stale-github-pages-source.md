---
schema: "fcvw/troubleshooting@1"
id: "TRB-20260727-pages-source-7151"
artifact_role: "record"
owner: "framework-maintainers"
upgrade_strategy: "preserve"
record_scope: "framework"
retrieval_scope: "search_only"
title: "Stale GitHub Pages source after clean-template migration"
type: "failure"
status: "validated"
confidence: "high"
detected_at: "2026-07-27"
last_reviewed: "2026-07-27"
related_version: "V0.14.0"
related_plan: "P2-R5-2026-07-27-open-issues-42-48-and-document-graph"
sources:
  - "FCVW/Plans/completed/P2-R5-2026-07-27-open-issues-42-48-and-document-graph.md"
  - "FCVW/FILESYSTEM.md"
  - "FCVW/AUDIT.md"
  - "FCVW/framework-releases/V0.14.0.md"
tags:
  - "#failure-log"
  - "#github-pages"
  - "#release"
---

# Troubleshooting: Stale GitHub Pages source after clean-template migration

## 1. Identification

- **Date detected:** 2026-07-27
- **Detected by:** post-release automated-run inspection
- **Affected version:** `V0.14.0`
- **Affected surface:** external GitHub Pages repository setting `main:/docs`
- **Related plan:** [Open issues 42-48 and document graph](../Plans/completed/P2-R5-2026-07-27-open-issues-42-48-and-document-graph.md)
- **Governing contracts:** [filesystem](../FILESYSTEM.md), [audit](../AUDIT.md), and [release](../RELEASE.md)

## 2. Symptom Description

```text
No such file or directory @ dir_chdir0 - /github/workspace/docs
```

The Pages build attached to ready revision `7151c30f67e875ecbcd05624c1562d2787d603f9` failed while the release assets and all repository validators passed.

## 3. Hypotheses

| # | Hypothesis | Validated | Result |
|---|---|---|---|
| H1 | The Pages source still targets removed root `docs/`. | `yes` | Pages API returned legacy source `main:/docs`; the directory is intentionally absent. |
| H2 | Changing the Pages source to repository root is compatible. | `no` | Jekyll rejected intentional template date placeholder `"YYYY-MM-DD"`. |
| H3 | The GitHub Release assets are corrupt. | `no` | All five downloaded assets matched local SHA-256 values byte-for-byte. |

## 4. Root Cause

The repository retained a legacy GitHub Pages configuration after the clean-template contract stopped distributing a root `docs/` site. Both Pages-supported legacy sources conflict with current governance: `/docs` is absent by design, while `/` contains reusable templates whose placeholders are valid FCVW content but invalid Jekyll dates.

## 5. Solution Applied

- [x] Confirm the repeated Pages failure and exact configured source.
- [x] Test the only non-`docs` legacy source and capture its incompatibility.
- [x] Disable the errored Pages site while preserving historical workflow runs.
- [x] Clear the repository Website field that still referenced a legacy Pages URL.

**Files modified:** none for the operational correction; the GitHub repository Pages setting was removed. This record and its relationships preserve the evidence.

## 6. Validation

| Check | Result | Evidence |
|---|---|---|
| Pages configuration removal | `pass` | `GET /repos/Sistema2D/FrameCode-VibeWork/pages` returns HTTP `404` after deletion. |
| Repository Website cleanup | `pass` | Repository metadata reports an empty `homepage` value after the legacy Pages URL was cleared. |
| Release download integrity | `pass` | Four ZIPs and `SHA256SUMS.txt` downloaded from v0.14.0 matched local SHA-256 values. |
| Framework regression suites | `pass` | 16/16 validator tests and 62/62 feature/adversarial tests. |
| Governance and graph | `pass` | Clean-template validation 0/0 and document graph 192/3/0 after this record was linked. |

## 7. Prevention

When a framework migration removes an in-repository documentation-site source, the release audit must inspect the GitHub Pages setting. Keep Pages disabled unless a compatible external pipeline or dedicated site source is explicitly governed; do not recreate forbidden clean-template paths to satisfy stale infrastructure.

## 8. Wiki Promotion

- [ ] Failure is worth promoting to `wiki/failures/`.
- Decision: retain this scoped troubleshooting record; no broader wiki page is needed unless the configuration recurs.
- Tags: `#failure-log`, `#github-pages`, `#release`

## 9. Status

`resolved`

**Resolution date:** 2026-07-27
