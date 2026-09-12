# SYSTEM 4 — FIRST CODEX LIVE TEST

Run only the isolated System 4 test. No file changes unless required to make the command executable; if any change would be needed, STOP and report the first blocker instead.

Command:
`python3 isolated_system4/live_test.py isolated_system4/live_fixture/wordpress_snapshot.json`

Required positive proof:
- Codex entry PASS
- bad draft is blocked with `TITLE_BINDING_FAIL`
- phase becomes `REPAIR_REQUIRED`
- corrected draft passes
- release produces WordPress WXR draft + release JSON
- `publish_allowed=false`
- immutable metadata tampering blocks release
- terminal `SYSTEM4_FIRST_CODEX_BOUNDARY_LIVE_TEST_PASS`

This is architecture/boundary proof only, not production text-quality approval.
