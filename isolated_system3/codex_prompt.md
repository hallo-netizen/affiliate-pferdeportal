# SYSTEM 3 — ISOLATED RULE-BOUND ARTICLE TEST

Goal: produce exactly one German test article for `isolated_system3/live_fixture/wordpress_input.json` under the already authoritative Pferde-Atelier rules, without importing any workflow/runner/gate/state from any other text system.

## Mandatory isolation sequence
1. Before reading any content/workflow file outside `isolated_system3`, bind ONLY these authoritative RULE SOURCES into `isolated_system3/_sealed_rule_live/`:
   - `control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`
   - `control/startmaster0107/runtime_packages/PSERC-FIX.zip`
   - complete tree `PSTE_0.56.25/`
2. Verify the sources BEFORE copying/extracting:
   - PPM SHA256 = `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
   - PSERC SHA256 = `77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314`
   - source Git tree of `PSTE_0.56.25` = `b411a8b12e7c3e8c99645cfc9a762ba30eff0905`
3. PSTE copy verification is path-independent and content-exact:
   - From the verified source tree, create a canonical manifest containing EVERY regular file under `PSTE_0.56.25/` as `(relative_path, sha256(exact bytes))`, sorted bytewise by relative path.
   - Copy those files into `isolated_system3/_sealed_rule_live/PSTE_0.56.25/` preserving the exact relative paths and exact bytes.
   - Recompute the same manifest from the sealed copy. The source and sealed manifests must match exactly: same path set, no extra file, no missing file, same SHA256 for every file.
   - Do NOT compare the Git tree SHA of the relocated copy with the source Git tree SHA; relocation changes the enclosing Git tree identity even when file bytes are identical.
4. Copy the verified PPM and PSERC archives into the sealed directory without byte changes and verify their SHA256 again after copying. If extraction is necessary to read rule content, extract only inside `isolated_system3/_sealed_rule_live/` and never execute code from the archives.
5. These sources are RULE CONTENT only. Do not copy, execute, import or reuse any runner, controller, gate, handoff, state machine, worker instruction, generated article, runtime state or workflow logic from another text system.
6. After the verified seal is complete, do not read or use any file outside `isolated_system3` for article generation or validation.
7. Treat the sealed rule content and its manifest as immutable. Any source hash mismatch, sealed-copy mismatch, missing required input, contradiction or unavailable mandatory rule => FAIL. Never repair, guess, relax, map or reinterpret.

## Article task
- Read the WordPress fixture only after the rule copy is sealed.
- Determine the EXACT canonical article-type/profile identifier and all applicable requirements from the sealed rule content itself. Do not assume or translate article-type names.
- Produce the finished article as WordPress-ready HTML in `isolated_system3/codex_output.md` only if the fixture exactly satisfies the canonical profile input contract.
- Apply every mandatory applicable content, structure, table, internal-link, SEO, language and quality rule contained in the sealed rule content.
- Do not replace canonical rules with the old 250–450-word test rules.
- Do not invent missing facts, links, keywords, products, measurements, sources, article types or metadata. If a canonical mandatory input is absent, STOP with the exact missing input instead of producing an invalid article.
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
