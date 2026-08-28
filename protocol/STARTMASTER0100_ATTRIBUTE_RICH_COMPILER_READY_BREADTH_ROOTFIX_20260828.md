# STARTMASTER0100 – Attribute-rich titles + compiler-ready breadth rootfix

## Binding title contract
Presentation qualifiers exist only to make titles human, smooth, attractive and direct. Examples: `passend`, `geeignet`, `richtig`, `optimal`, `ideal`. They have **zero SEO/longtail authority**. SEO authority remains exclusively with the exact bound target keyword / true longtail. Presentation words must not invent product properties, search intent, recommendation claims or content facts, and must not become a new single repeated template family.

Problem surfaces that must no longer reach READY include `So wählst du Bahnplaner für Reithallen`, `So findest du Rampenmatten für Pferdeanhänger` and mechanical `Keyword + prüfen` forms. Verified rootfix examples include `Den richtigen Bahnplaner für Reithallen finden` and `So findest du die passenden Rampenmatten für Pferdeanhänger`.

## Root cause – title quality
PSTE could still fall back to bare `keyword + verb` Beratung surfaces. The natural-language presentation layer was not consistently primary. PSTE 0.56.25 prefers attribute-rich grammatically inflected presentation surfaces while keeping the exact target keyword contiguous and unchanged. `empfehlenswert` was removed because it would imply an editorial recommendation.

## Root cause – quantity / quota
Fresh Research and Retained/Current Backlog did not consistently pass the same pre-title planning-readiness / duplicate / cannibalization gate before satisfying the production-wave quota. Existing duplicate topics could therefore consume the target and only be blocked downstream by PSERC.

PSTE 0.56.25 applies one shared readiness gate to both paths. Duplicate/cannibalization failures remain stored and fail closed but never count as usable quota. Compiler projection/count/title allocation counts only `planning_suitability=YES`, matching PSERC eligibility. Retained backlog is revalidated locally before provider calls. Default production-wave target is **40 true usable topics / max 40 families**.

## Live24 root-cause replay
- initial compiler-eligible shape: 24
- true existing-content duplicates: 14
- true usable after pre-quota gate: 10
- additional distinct topics required for target 40: 30
- final true usable: 40
- blocked topics deleted: false
- blocked topics count toward quota: false

## Per-fix complete-workflow gates
Every individual change was tested immediately against the complete positive/negative workflow.

- Step A title naturalness: PASS
- Step B shared planning readiness / quota: PASS
- Step C broad 40-wave contract: PASS
- Final source workflow: PASS
- Installer re-extract workflow: PASS
- Final MASTER re-extract + embedded-plugin workflow: PASS
- realistic 40: 40 PASS / 0 REVIEW
- scale 500: 500 PASS / 0 REVIEW
- attribute words zero SEO authority: PASS
- same SEO longtail remains duplicate regardless of presentation adjective: PASS
- PSERC duplicate/longtail/cannibalization thresholds unchanged: PASS
- PSERC 0.28.14 generation-retention regression: PASS
- combined PSTE↔PSERC capability: PASS
- PHP lint: PSTE 74/74, PSERC 42/42 PASS
- no content/design/PPM/LanguageTool/production-machine changes: PASS
- article production batch policy unchanged: PASS
- immutable references and production block byte drift: 0

## PSERC storage incident / live recovery
PSERC 0.28.14 retention was executed live before this release. Technical generations were reduced from 37 to 3 protected generations (active + 2 fallbacks). After cleanup and physical table rebuild, `slfo_options` was reduced to **236.0 MiB**. No article, PSTE, PPM, content or design scope was touched. Automatic bounded retention remains active.

## Release artifacts
PSTE 0.56.25 SHA-256: `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`

PSERC 0.28.14 remains unchanged SHA-256: `a5008fc463c78f919a1dc03a510e681c426d97b5f3785de820169805dab3b988`

STARTMASTER0100 SHA-256: `d04fd6076d346575ba1e4e49a5f5a60d92d411358a7a934973ba2bb07bc0be25`

Final MASTER post-ZIP audit: 258/258 files byte-identical after re-extract, manifest 257/257 PASS, embedded full workflow PASS.

## Exact next live step / handoff
1. Install/overwrite **PSTE 0.56.25 only**. Keep PSERC 0.28.14 unchanged.
2. Do not start article production yet.
3. In SEO Themenengine run exactly one production wave with target **40** and max **40 families**.
4. After the wave, run exactly one candidate-only editorial-plan/snapshot refresh.
5. Export metadata-preview JSON and verify live: title naturalness, attribute diversity, READY/REVIEW/BLOCKED counts, duplicate/cannibalization protection.
6. Only after live PASS proceed to broad article production.

STARTMASTER0100 is binding. No plugin release is valid unless each fix and the final package pass the complete local positive/negative workflow.