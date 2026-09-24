# PSTE internal clarification retention fix – 2026-09-24

Status: **TECHNICAL PASS / LIVE APPLY + READBACK OPEN**

## User requirement

Portal-relevant research terms must not be lost. If the raw search phrase is not directly suitable as an editorial title or cannot yet be assigned safely, PSTE must retain it internally, keep the original query unchanged, and only later pass it through the normal editorial reformulation/assignment path. It must not be copied 1:1 into production merely because it was discovered.

Observed live example on PSTE 0.57.9:

- query: `pferde putztasche`
- Fundstellen: 55
- reason codes:
  - `PSTE_PORTAL_RELEVANCE_PROVEN_FAMILY_ASSIGNMENT_NOT_PROVEN`
  - `PSTE_SANDBOX_INTERNAL_CLARIFICATION_REQUIRED`
  - `PSTE_FAMILY_V2_SUBJECT_HEAD_MISSING`
  - `PSTE_CONTEXT_QUERY_MISSING`
- Kontext: `PENDING`

The existing persistence path was already lossless: the normal metadata path preserves the raw keyword and the Semantic Sandbox retains internal-clarification candidates for later re-entry. No direct production handoff is performed.

## Root cause

The defect was semantic classification/display, not category resolution and not data loss.

`PSTE_Topic_Policy::classifyRole()` returned `ROLE_ALREADY_COVERED` immediately for failed planning-readiness / pre-title gates before separating actual duplicate/coverage reasons from internal clarification. Therefore retained candidates such as `pferde putztasche` could be shown as **Bereits abgedeckt** despite not being covered.

Actual duplicate/coverage signals remain distinct, including `EXACT_NORMALIZED_QUERY_DUPLICATE`, `CROSS_TYPE_ANSWER_EQUIVALENCE`, `ANSWER_EQUIVALENT_EXISTING`, `ANSWER_EQUIVALENT_PLANNED` and canonical-slot ownership.

## Minimal fix

Technical branch: `pste-05700-server-step-driver-proof`

Patch:
`proof/pste-wordpress-real-e2e/pste05710-internal-clarification-retention-role.patch`

Product scope is limited to:

1. `includes/class-pste-topic-policy.php`
   - explicit coverage/duplicate reasons still produce `ROLE_ALREADY_COVERED`
   - internal clarification / structure-gap retention produces `ROLE_RESEARCH_KEYWORD`
   - generic unrelated fail-closed behavior remains unchanged

2. `includes/class-pste-admin.php`
   - overloaded filter label becomes **Zwischengespeichert, blockiert oder bereits abgedeckt**
   - internal-clarification reason is described as pending internal assignment/editorial reformulation instead of falsely saying the topic is already covered

No category matcher/resolver, provider, research source, ranking, content-production or data-deletion logic is changed.

## Lossless-retention proof

Existing protected behavior remains:

- raw keyword is preserved through `raw_keyword_preserved`
- Semantic Sandbox records internal clarification with `PSTE_SANDBOX_EDITORIAL_CLARIFICATION_RETAINED`
- no direct production handoff
- later re-entry uses the normal metadata/editorialization path

Targeted role proof:

- internal clarification example (`pferde putztasche` pattern) -> `RESEARCH_KEYWORD`
- real duplicate example -> `ALREADY_COVERED`

## Full Real WordPress E2E

Proof commit:
`cd1d65ad0f41e409d03686210f32fae1f0358b8a`

Workflow:
`PSTE Real WordPress HTTP E2E`

Run:
`35991171575`

Result:
**SUCCESS**

Dedicated step:
`Prove internal clarification is retained and not marked covered` -> **SUCCESS**

All existing Real WordPress E2E stages also passed, including serial driver, Sandbox export, stale-status protection, safe cancel, continuation, PREPARE stress and production wave 40.

Artifact:
- ID: `10804353613`
- digest: `sha256:48dbb18e97b232e9c67832c3321cab7b8b495b9abacb7a3fca5bd1d3b97b2ecf`

Exact tested candidate:
`PSTE-0.57.10-HOBBYROOM.zip`

SHA256:
`f55d01f10205daaf86d579f986c0be000d2ec2f44ccb281decc3b939e205e65f`

## Category closeout context

The category concept is already FINAL/FROZEN. The 1149-category resolver baseline passed all 25 new categories plus known old positives. On 2026-09-24 the user additionally verified in the live PSTE manual research-family selector that all five new families are present:

- Pferdesättel
- Trensen
- Offenstallbau
- Paddockbau
- Reitplatzbau

Therefore the present 0.57.10 change is **not a category fix**. It only corrects the retained-candidate role/UI semantics.

## Next live step

Live screenshot showed PSTE **0.57.9**.

Before further category closeout work:
1. install only the exact tested 0.57.10 candidate above;
2. do not delete/rebuild retained data and do not blindly restart research;
3. read back `pferde putztasche` in **Themenprüfung**;
4. expected role: **Recherchekeyword**, not **Bereits abgedeckt**;
5. verify the original query is still retained in **Semantic Sandbox** for later normal editorial reformulation.

Only after that live readback PASS continue with PSERC 1149 refresh, link-target refresh, total category E2E and final read-only WordPress preflight.
