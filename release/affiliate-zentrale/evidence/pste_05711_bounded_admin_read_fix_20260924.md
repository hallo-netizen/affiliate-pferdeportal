# PSTE 0.57.11 bounded admin read fix – 2026-09-24

Status: **REAL WORDPRESS E2E PASS / LIVE APPLY + READBACK OPEN**

## Live failure

After installing PSTE 0.57.10, clicking **Themenkarte** produced the WordPress critical-error page.

## Root cause

Analytics-heavy PSTE admin views could materialize a large topic pool and related data in one request. On a sufficiently large live dataset this can exhaust PHP memory before the admin fail-safe can render a normal error message.

The same risk class was therefore checked across the complete PSTE admin surface rather than patching only Themenkarte.

## Fix scope

0.57.11 adds bounded/fail-safe reads for the analytics-heavy admin paths. It does **not** change category matching, category concept, provider logic, ranking, research-source logic or content-production rules.

The 0.57.10 internal-clarification retention fix remains included:
- unresolved but relevant raw terms are retained;
- original query is preserved;
- no direct 1:1 production handoff;
- actual duplicates remain already covered.

## Hard Real WordPress proof

Technical head:
`93321123bbb07c902a3bcda2d96ab3c4d3cf6426`

Workflow:
`PSTE Real WordPress HTTP E2E`

Run:
`35998243177`

Result:
**SUCCESS**

The dedicated admin probe inserted **4200 additional topic-pool rows** and then opened every tested PSTE backend page through real authenticated WordPress HTTP.

PASS pages:
- Übersicht
- Themenkarte
- Keywords & Longtails
- Themenprüfung
- Abdeckung
- Prioritäten
- Konflikte
- Semantic Sandbox
- Datenquellen
- Einstellungen

The same run also passed:
- internal clarification retention
- real duplicate regression
- family park policy
- queue/child lock exclusivity
- strict serial driver
- real site setup/context
- bounded Semantic Sandbox export
- stale browser status protection
- safe cancel during PREPARE
- cancelled-wave continuation
- PREPARE stress
- production wave 40

Artifact:
- ID: `10808195166`
- digest: `sha256:f8659106061f5ef51ac0abfd874622ff39222e19b9b9aa85a6f776f1d1627815`

Exact tested candidate:
`PSTE-0.57.11-HOBBYROOM.zip`

SHA256:
`d89e61555dafdc1de4d2e4840730da1a34b3805b1b8be6b06ab7a9f6d9b92b31`

## Next live step

Install only the exact tested 0.57.11 candidate over live 0.57.10.

Do not:
- delete data,
- rebuild the retained pool,
- restart research,
- change categories.

After activation, read back:
1. **Themenkarte** opens without critical error.
2. **Themenprüfung** opens without critical error.
3. `pferde putztasche` remains retained for internal clarification and is not lost.
