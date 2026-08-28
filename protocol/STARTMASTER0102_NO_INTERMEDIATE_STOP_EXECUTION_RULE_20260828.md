# STARTMASTER0102 – No-Intermediate-Stop Execution Rule

## Status
ACTIVE USER-MANDATED EXECUTION RULE for current six-article production test and next MASTER handoff.

## Scope
Interaction/orchestration only. No Fachworkflow, content, quality, safety, PPM 6.7.9, LanguageTool, PSTE, PSERC, duplicate/cannibalization, design or publish rule is weakened or changed.

## Binding rule
After the user has explicitly authorized a production block and all required user inputs are present, execution continues automatically through every non-interactive allowed gate until the block is complete or a genuine hard stop occurs.

Do not interrupt with progress messages, intermediate PASS reports, reassurance, summaries or confirmation questions between ordinary gates. Record progress, timings, PASS reuse, local failures and optimization observations in protocol artifacts instead.

A user-facing stop is allowed only when:
1. a mandatory user input is missing;
2. an irreversible live action requires user control;
3. a credential or external manual action is required; or
4. a hard gate fails and cannot be resolved locally without changing a binding rule.

Recoverable local failures are fixed or isolated locally and execution resumes without restarting the whole workflow.

## Current production assignment
- Process all 6 current READY items as one real article test block.
- Measure optimization potential during actual production; do not change fachliche rules during the test.
- Keep `Wissenswertes über Weidetore für Pferde` unchanged as an observation case for Beratung-title semantics.
- Only after the article test: handle the 40/40 live wave failure and then the Sandbox -> stored backlog -> provider-research ordering as separate root fixes.
- No auto-publish.

## Prompt amendment for next MASTER
The next binding start prompt must include a dedicated `KEINE UNNÖTIGEN ZWISCHENSTOPPS – ZWINGEND` section with the rules above.
