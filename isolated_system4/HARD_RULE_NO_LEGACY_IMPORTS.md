# SYSTEM 4 — HARD RULE: NO LEGACY IMPORTS

System 4 may reuse only authoritative domain content, rule texts, immutable tool/runtime inputs, and externally defined mandatory checks.

Forbidden to import or copy from any prior attempt or architecture:
- STARTMASTER workflow logic
- H7/H8/Single-Door room logic
- ACM orchestration logic
- System 3 orchestration logic
- legacy handoff formats
- legacy runtime bridges
- legacy gates/controllers/repair routes
- legacy state machines/checkpoints
- legacy proof/receipt chains
- legacy package construction/signing flow
- legacy workaround code or compatibility adapters

Allowed as authoritative inputs only:
- the isolated Textmaschine and its current binding/rule content
- current authoritative SEO/content/domain rules
- current mandatory LanguageTool check specification/tool
- current PPM/PSERC/PSTE domain validation rules, only as rule/tool inputs and not their old orchestration
- external rule: no external links in article output
- external table rule(s), as current rule text/specification only
- WordPress metadata input contract and WordPress draft output requirements

System 4 must implement its own minimal one-state controller around these inputs. No old workflow code may become an execution dependency.

Every integration test must fail if System 4 imports, executes, shells into, calls, or depends on legacy workflow/orchestration paths outside the explicitly allowlisted authoritative rule/tool inputs.
