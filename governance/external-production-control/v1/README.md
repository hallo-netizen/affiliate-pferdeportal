# External Production Control V1

Purpose: make Chat execution deterministic **outside** the existing editorial/production workflow.

It does not call, modify or replace PSTE, PSERC, PPM, LanguageTool, Redaktionsplan, READY, article content, research, Fact-Packs, quality gates, design or publishing.

## What it fixes

- one authoritative current state instead of memory/history reconstruction
- exact next action; all other actions rejected
- exact next input file + SHA; no filename guessing
- no duplicate active artifact roles / plan slots / canonical article IDs
- no recheck of locked PASS steps without documented delta
- missing future artifacts cannot block the current step
- no local `FINAL`; live evidence is mandatory
- a fresh handoff bundle after every checkpoint
- handoff contains all data needed to resume without memory

## Mandatory startup in every chat

1. Open the current MASTER and the current `CHAT_HANDOFF_CURRENT.zip`.
2. Read `START_HERE.txt` and `CURRENT_STATE.json` only as navigation sources.
3. Run `production_control_guard.py resume`.
4. Run `authorize` before the next production action.
5. After every checkpoint, generate a new state + handoff; never hand over an old bundle.

Historical files remain evidence only.

## Fast-path after STARTMASTER0075

The full MASTER is **not** repacked for every normal production checkpoint. That would add time without adding evidence. The binding MASTER remains fixed while the small external `CURRENT_STATE.json` / `CHAT_HANDOFF_CURRENT.zip` advances.

This does **not** weaken the MASTER: the external state may only describe checkpoint, next action, exact artifacts and evidence; it is forbidden to change workflow rules or content. A new full MASTER is required only for a real MASTER/governance/source delta.

This makes new-chat resume cheap: verify the MASTER SHA, then work from the small current handoff instead of rereading historical MASTER/GitHub material.

Before any chat ends, run `close-chat`; only the files listed in its delivery manifest may be handed to the user.
