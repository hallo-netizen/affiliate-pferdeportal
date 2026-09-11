# SYSTEM 4 — TRUE SINGLE ROOM

Status: isolated prototype / test only.

No code, runtime, handoff, gate, state machine, signer or worker contract is imported from concepts 1–3. They are historical inspiration only.

## Whole path
WordPress JSON snapshot -> isolated ingress -> ONE persistent canonical article state -> research -> fact check -> draft -> fixed checks -> repair of the SAME draft field if FAIL -> output gate -> deterministic WordPress WXR draft + release manifest.

## Authority
- Chat: start/status only.
- Codex writer: may write research/facts/draft files only when the fixed phase allows it.
- Controller: only routing authority; route is hard-coded.
- Checkers: read-only against article; they only return PASS/FAIL + error code.
- External data/tools: data only; no route/rule/publish authority.
- Output: always WordPress `draft`; auto-publish impossible in this prototype.

## Single-room invariant
The article identity and immutable WordPress metadata exist once in `state.json`. Internal stages do not create new article packages, IDs, rooms, receipts or contract copies. Repair edits only `draft_markdown`; immutable metadata hash must remain unchanged.

## Prototype caveat
The first live test proves workflow/boundary mechanics, repair blocking, immutable-state protection and WordPress-draft output. Its built-in checks are intentionally minimal and are NOT the production editorial/SEO/PPM rule set.
