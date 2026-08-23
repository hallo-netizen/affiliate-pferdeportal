# Critical review and implementation – external production control

## Binding premise
The existing editorial/production workflow remains the sole authority. This control plane is **outside** it. It neither supplies editorial decisions nor replaces a gate.

## What the original concept got right
- one machine-readable current state
- `CURRENT_CHECKPOINT`, `NEXT_ALLOWED_STEP`, `DELTA_TRIGGER`
- reject actions that are not the next action
- atomic checkpoint progression
- history is evidence, not navigation
- small additive implementation outside Fachlogik

## Gaps exposed by the Boxenmatten incident
A state pointer alone was not enough. The failures showed additional control-plane requirements:

1. **Exact artifact identity:** a chat could still hand over the wrong JSON even when the next step was known.
2. **Handoff completeness:** there was no mechanical proof that every chat ended with the current MASTER, current state and exact next input.
3. **False FINAL:** a local/mock PASS could be mislabeled as full workflow PASS.
4. **Duplicate/stale current objects:** old pointers and old packages could coexist and be mistaken for current.
5. **False blockers:** missing evidence for a later step could cause work to stop too early.
6. **Memory fallback:** if a file was missing, a chat could still reconstruct from recollection/history.
7. **No mandatory checkpoint handoff:** an intermediate state could be left without a deterministic resume packet.
8. **No package/live-result binding:** a live result needed to be tied to the exact package ID/source before promotion.
9. **No final delivery gate:** there was no last machine check that the files given to the user were the files referenced by the current state.

## Implemented V1 controls
- unversioned authoritative `CURRENT_STATE.json`
- state hash (`state_id`) and parent state chain
- exact action authorization
- exact SHA-bound `next_step_input`
- duplicate active role / plan-slot / canonical-ID rejection
- current-step-only blocker scope
- future missing artifacts do not block the present step
- locked PASS list + no memory/history navigation
- `PRELIVE_PASS` / live / final separation
- exact live-result conditions including package ID/source and publish=false
- deterministic `CHAT_HANDOFF_CURRENT.zip`
- automatic handoff generation when a machine-result checkpoint is advanced
- `close-chat` final delivery verification
- negative tests for wrong action, wrong file, tamper, duplicates, local FINAL, wrong live package and stale/missing conditions

## Deliberate non-goals
The control plane does not decide titles, topics, article types, research, facts, wording, structure, links, quality, PPM behavior, publishing or workflow order. Those remain entirely in the existing MASTER/workflow.

## Guarantee boundary
Within the governed execution path, wrong action/file/state/final-promotion is fail-closed. No external file can literally prevent a future model from ignoring all instructions and bypassing the guard; therefore every MASTER/handoff now requires running the guard first and `close-chat` last. This is the strongest enforcement possible without modifying the production plugins/workflow itself—which is explicitly forbidden.
