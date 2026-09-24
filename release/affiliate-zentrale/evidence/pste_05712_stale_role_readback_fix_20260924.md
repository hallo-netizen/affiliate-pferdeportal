# PSTE 0.57.12 stale-role readback fix – 2026-09-24

Status: **REAL WORDPRESS E2E PASS / LIVE APPLY + READBACK OPEN**

## Live defect

On live PSTE 0.57.11, the retained candidate `pferde putztasche` still displayed the role **Bereits abgedeckt**, although the review reason was already correct:

- portal relevant
- internal assignment/editorial reformulation still pending
- internal clarification required
- context pending

## Proven root cause

The read model loaded the persisted database column `topic_role` directly for old automatic rows:

`$candidate['topic_role'] = $row['topic_role']`

That bypassed the newer role policy for existing rows. Therefore an old persisted `ALREADY_COVERED` value survived display even though the current policy classifies the same candidate as a retained research keyword.

## Fix

PSTE 0.57.12 re-evaluates automatic role/planning fields on read for rows without manual review status.

Properties:
- read-only projection
- no data deletion
- no research restart
- no category change
- no database rewrite of the stored role
- original raw query remains unchanged
- actual duplicate reasons still classify as `ALREADY_COVERED`

## New regression proof

The Real WordPress E2E now seeds two legacy rows with deliberately stale persisted roles:

1. internal-clarification row persisted incorrectly as `ALREADY_COVERED`
2. true duplicate row persisted incorrectly as `RESEARCH_KEYWORD`

The readback proof verifies:

- internal clarification -> `RESEARCH_KEYWORD`
- true duplicate -> `ALREADY_COVERED`
- original query unchanged
- planning remains blocked
- persisted database role columns remain unchanged

Dedicated step:
`Prove stale persisted automatic roles are reclassified read-only` -> **SUCCESS**

## Full Real WordPress E2E

Technical commit:
`9288584486857a91425b6b9d15c71680b2dbc691`

Workflow run:
`36000709696`

Result:
**SUCCESS**

The full run also passed:
- internal clarification policy
- family park policy
- queue/child locking
- strict serial driver
- real portal setup
- bounded Sandbox export
- real admin login
- stale-browser protection
- safe cancel
- cancelled-wave continuation
- PREPARE stress
- production wave 40
- bounded-read admin-page test

Artifact:
- ID: `10808671661`
- digest: `sha256:c16839c7a73edc5ee72ac62065982625f21c8585ad73442269f0fb3fa140bdc3`

Exact tested candidate:
`PSTE-0.57.12-HOBBYROOM.zip`

SHA256:
`0cf9c4004f9c237ac60a70a324c431193f8ddcce640ce1a2d08ddbdf901fdc9b`

## Next live step

Install only the exact tested 0.57.12 candidate over live 0.57.11.

Do not:
- delete data
- rebuild the retained pool
- restart research

Then read back in **Themenprüfung**:
`pferde putztasche`

Expected:
- no role **Bereits abgedeckt**
- original query remains present
- internal clarification reason codes remain present
