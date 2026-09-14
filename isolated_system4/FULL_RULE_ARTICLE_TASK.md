# SYSTEM 4 — FIRST FULL-RULE ARTICLE TEST

TEST ONLY. No merge. No publish. No production release.

## Hard isolation
- System 4 implementation and every modification must stay under `isolated_system4/**`.
- Do not import/copy/wrap/call/exec or depend on STARTMASTER, H7/H8/Single-Door, ACM, System 3 orchestration, legacy handoffs, runtime bridges, gates, state machines, receipt/proof/package chains, repair routes, signers or workaround code.
- Old attempts may be read only as negative/design evidence.
- Do not reuse old articles, fact packs, research, stage proofs, recovery or production artifacts.

## Textmaschine + design are immutable
- The current Textmaschine/content rules are READ-ONLY. Do not edit, relax, extend, reinterpret, normalize, replace or shadow them.
- PPM 6.7.9, current article-type/content rules, table contract, WordPress plugin, theme/CSS and design selectors are READ-ONLY.
- System 4 may validate a candidate against those existing contracts but may not repair or restyle the contract itself.
- Existing production HTML/design must remain unchanged: current production root/type classes and attributes, current table selector classes and current Beratung H2 section-heading level.
- `design_guard.py` is PASS/BLOCK only and performs zero content/design mutation.
- If the test would require a Textmaschine-rule or design change, stop with `BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE`.

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
- existing production/design class drift -> BLOCKED with zero mutation;
- external link inserted -> BLOCKED;
- required internal-link binding missing/wrong -> BLOCKED when required;
- mandatory LanguageTool/domain checker unavailable -> fail closed;
- title/keyword/plan_slot/immutable metadata tamper -> BLOCKED;
- forbidden legacy import/call -> BLOCKED;
- `publish_allowed=true` -> BLOCKED.

## First fresh article — fixed real binding
Use the FIRST item of `isolated_system4/live_fixture/wordpress_snapshot.json` exactly as bound. It is the real 7/7 `Beratung` item.

Hard correction after fresh evidence:
- The current PSERC metadata batch marks all seven `Beratung` items `READY_FOR_TEXTMACHINE_METADATA_INTAKE`.
- The bound runtime batch for the same batch SHA is `EXECUTION_READY`.
- The current PSERC-approved production package contains a signed workflow release with `status=PASS` for the same seven plan slots.
- Therefore an isolated article-type field such as `production_allowed=false` / `WAVE2_QUARANTINE_PENDING_RECERTIFICATION` found inside a PPM package MUST NOT by itself be interpreted as a current production blocker.
- Do not switch article type and do not create a synthetic fallback because of that field.
- Only a CURRENT actually executed authoritative domain checker against the bound article may block the article. If such a checker genuinely returns a non-repairable article-type prohibition during execution, report that exact runtime result and source.

For the bound first item:
- Fresh research/facts/draft only in a temporary workspace.
- No old article body as source.
- Run through every now-bound real production rule/checker.
- Preserve the existing Textmaschine rules and design contract byte-for-byte at their authority sources; do not modify them to obtain PASS.
- On repairable FAIL, change only the same draft for the exact reported defect and rerun the same checker.
- Continue to PASS or the first genuine non-repairable hard blocker.

## Output
Determine the CURRENT authoritative WordPress draft-output contract freshly. Do not use WXR merely because the earlier architecture test used it if the actual current production handoff requires another contract. Produce only a draft/non-publish output. No design transformation may occur after the checked body.

## Terminal return
Return only one of:

`SYSTEM4_FIRST_FULL_RULE_ARTICLE_PASS`
with title, article type, authoritative sources/tools actually bound, checker sequence, repair sequence if any, final article verbatim, output contract/file, SHA256, `publish_allowed=false`, unchanged-design PASS, and NO-LEGACY PASS;

or the first genuine non-repairable blocker with exact status/error and authoritative source causing it.

Never claim production-quality/output PASS while any required real rule/tool or real required output binding is missing.
