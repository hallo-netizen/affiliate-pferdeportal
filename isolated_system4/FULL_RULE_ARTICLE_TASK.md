# SYSTEM 4 — FIRST FULL-RULE ARTICLE TEST

TEST ONLY. No merge. No publish. No production release.

## Hard isolation
- System 4 implementation and every modification must stay under `isolated_system4/**`.
- Do not import/copy/wrap/call/exec or depend on STARTMASTER, H7/H8/Single-Door, ACM, System 3 orchestration, legacy handoffs, runtime bridges, gates, state machines, receipt/proof/package chains, repair routes, signers or workaround code.
- Old attempts may be read only as negative/design evidence.
- Do not reuse old articles, fact packs, research, stage proofs, recovery or production artifacts.

## Read-only authority discovery
Codex MAY read repository files outside `isolated_system4/**` solely to identify the CURRENT AUTHORITATIVE rule texts/specifications and pure checker/tool inputs for:
- isolated Textmaschine/content rules;
- SEO/content/domain rules;
- LanguageTool requirement/tool specification;
- PPM/PSERC/PSTE domain validation requirements, only as rule/tool inputs;
- internal-link rule binding;
- current mandatory table rule;
- current prohibition of external links;
- WordPress metadata input and draft-output contract.

Reading does not authorize executing or importing old orchestration. No file outside `isolated_system4/**` may be modified.

## Required System 4 implementation
Build new minimal System-4-native adapters/checkers only under `isolated_system4/**` against the single persistent canonical article state.
- Writer may change only draft/work content.
- Checkers may not change article content; only PASS/FAIL + code/evidence.
- Controller transitions are fixed.
- FAIL keeps the same article identity and same state; repair only the reported defect, then rerun the same checker.
- No internal article/package handoffs.
- WordPress metadata is the outer input; current authoritative WordPress draft package is the outer output.
- `publish_allowed=false` is mandatory.

## Mandatory NO-LEGACY proof
Add a machine test that fails if System 4 Python code imports/executes/calls or runtime-depends on forbidden old workflow/control paths. Explicitly allowlisted read-only rule/specification files or pure tools must not become orchestration dependencies.

## Mandatory positive/negative proof
At minimum prove:
- valid article -> all attached real rule checkers PASS;
- required table removed -> BLOCKED when the authoritative contract requires it;
- external link inserted -> BLOCKED;
- required internal-link binding missing/wrong -> BLOCKED when required;
- mandatory LanguageTool/domain checker unavailable -> fail closed;
- title/keyword/plan_slot/immutable metadata tamper -> BLOCKED;
- forbidden legacy import/call -> BLOCKED;
- `publish_allowed=true` -> BLOCKED.

## First fresh article
Preferred input is the first item of `isolated_system4/live_fixture/wordpress_snapshot.json`.

If and only if that bound article type is currently blocked by an authoritative rule such as `production_allowed=false`, DO NOT weaken or bypass the rule. Instead continue automatically:
1. Read the SAME current authoritative article-type contract and determine an article type explicitly marked/certified for production (`production_allowed=true` or the exact equivalent current contract state).
2. Prefer an already existing CURRENT WordPress/PSERC editorial-plan metadata item of that certified type, with its real title/keyword/category/plan_slot, found read-only from current authoritative metadata.
3. If no current bound metadata item of any certified type exists, create a clearly synthetic TEST-ONLY metadata fixture under `isolated_system4/**` for a certified type and an invented harmless horse-related topic. This synthetic fallback may prove System-4 rules/architecture but must NOT be misrepresented as a real production/WordPress-plan binding.
4. If the current WordPress output contract requires a real canonical plan binding and no certified current plan item exists, still generate and fully rule-check the synthetic test article, but terminal status must explicitly distinguish `FULL_RULE_ARTICLE_PASS_OUTPUT_BINDING_BLOCKED` rather than claim full production-output PASS.

For whichever eligible test input is selected:
- Fresh research/facts/draft only in a temporary workspace.
- No old article body as source.
- Run through every now-bound real production rule/checker.
- On repairable FAIL, change only the same draft for the exact reported defect and rerun the same checker.
- Continue to PASS or the first genuine non-repairable hard blocker.

## Output
Determine the CURRENT authoritative WordPress draft-output contract freshly. Do not use WXR merely because the earlier architecture test used it if the actual current production handoff requires another contract. Produce only a draft/non-publish output. Never fabricate a real plan binding for a synthetic fixture.

## Terminal return
Return only one of:

`SYSTEM4_FIRST_FULL_RULE_ARTICLE_PASS`
with title, article type, authoritative sources/tools actually bound, checker sequence, repair sequence if any, final article verbatim, output contract/file, SHA256, `publish_allowed=false`, and NO-LEGACY PASS;

or `SYSTEM4_FULL_RULE_ARTICLE_PASS_OUTPUT_BINDING_BLOCKED`
when the fresh synthetic article fully passes every real article rule/checker but a real WordPress/PSERC plan-bound output cannot truthfully be created because no certified current plan item exists; include the exact output-binding blocker;

or the first genuine non-repairable blocker with exact status/error and authoritative source causing it.

Never claim production-quality/output PASS while any required real rule/tool or real required output binding is missing.
