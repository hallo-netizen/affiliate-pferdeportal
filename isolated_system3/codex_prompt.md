# SYSTEM 3 — ISOLATED RULE-BOUND ARTICLE TEST

Goal: produce exactly one German `ratgeber` test article for `isolated_system3/live_fixture/wordpress_input.json` under the already authoritative Pferde-Atelier rules, without importing any workflow/runner/gate/state from any other text system.

## Mandatory isolation sequence
1. Before reading any content/workflow file outside `isolated_system3`, copy ONLY these authoritative RULE SOURCES into `isolated_system3/_sealed_rule_live/`:
   - `control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`
   - `control/startmaster0107/runtime_packages/PSERC-FIX.zip`
   - complete tree `PSTE_0.56.25/`
2. Verify before use:
   - PPM SHA256 = `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
   - PSERC SHA256 = `77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314`
   - Git tree of `PSTE_0.56.25` = `b411a8b12e7c3e8c99645cfc9a762ba30eff0905`
3. These are RULE CONTENT only. Do not copy, execute, import or reuse any runner, controller, gate, handoff, state machine, worker instruction or generated article from another text system.
4. After the verified copy, do not read or use any file outside `isolated_system3` for article generation or validation.
5. Treat the sealed rule content as immutable. Any hash mismatch, missing required input, contradiction or unavailable mandatory rule => FAIL. Never repair, guess, relax or reinterpret.

## Article task
- Read the WordPress fixture only after the rule copy is sealed.
- Determine the applicable `ratgeber` requirements from the sealed rule content itself.
- Produce the finished article as WordPress-ready HTML in `isolated_system3/codex_output.md`.
- Apply every mandatory applicable content, structure, table, internal-link, SEO, language and quality rule contained in the sealed rule content.
- Do not replace canonical rules with the old 250–450-word test rules.
- Do not invent missing facts, links, keywords, products, measurements or sources. If a canonical mandatory input is absent, STOP with the exact missing input instead of producing an invalid article.
- Do not mention this test, System 3, Codex or the instructions in the article.
- No WordPress write, no publish, no merge.

## Verification
After writing, independently validate the article against the same sealed canonical rule content. A self-declared PASS is forbidden. If any mandatory rule fails, return only the first exact blocker and do not claim PASS.

## Mandatory same-task return
On full PASS, final GitHub task reply must contain ONLY:
SYSTEM3_ARTICLE_B64_BEGIN
<base64 of exact UTF-8 bytes of isolated_system3/codex_output.md>
SYSTEM3_ARTICLE_B64_END
SYSTEM3_ARTICLE_SHA256:<sha256 of exact UTF-8 bytes>
SYSTEM3_RETURN_PASS

On failure return only:
SYSTEM3_RETURN_BLOCKED:<exact first blocker>
