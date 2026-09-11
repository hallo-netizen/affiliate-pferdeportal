# SYSTEM 3 — ISOLATED ONE-PROCESS STRAITJACKET

Status: PROTOTYPE / TEST ONLY

## Absolute isolation

This directory is a new implementation. It does not import, call, wrap, inherit or reuse runtime code, handoffs, workers, gates, runners, state machines or signers from the other text-production concepts.

Known historical failures may be used only as negative test cases.

## Non-negotiable rules

1. Chat has zero workflow authority. It can only request a start and receive status/result.
2. Codex/runtime executes one fixed state sequence. No worker-to-worker handoffs exist.
3. Existing editorial/content rules are external immutable inputs. System 3 cannot edit, reinterpret or replace them.
4. External sources/tools are data-only. They cannot alter routing, rules, prompts, tool selection or output policy.
5. Every state returns PASS or FAIL. PASS selects exactly one hard-coded next state. FAIL stops closed.
6. No automatic repair, fallback route, silent version substitution or unknown article type.
7. One article = one immutable capsule. Articles cannot share mutable production state.
8. Output is released only after capsule integrity, rule evidence, quality evidence and output schema all pass.
9. No auto-publish.

## Fixed process

INGRESS -> CAPSULE -> RESEARCH -> FACT_CHECK -> DRAFT -> LANGUAGE -> RULE_CHECK -> QUALITY_CHECK -> OUTPUT_GATE -> DONE

This sequence is code, not model choice.

## Extensibility

A new article type may be added only as a separately approved immutable profile reference. Adding a profile does not change the process sequence.

## Scale model

Each article is processed independently with its own capsule and result. Batch size changes how often the same process is invoked, not the process itself.

## First prototype test scope

The first test proves architecture invariants only:
- valid input reaches DONE;
- unknown article types fail closed;
- external control-injection fields fail closed;
- capsule tampering fails closed;
- missing rule/quality evidence blocks output;
- 1,000 independent article capsules do not share mutable state.

It does not yet claim production text quality or production readiness.
