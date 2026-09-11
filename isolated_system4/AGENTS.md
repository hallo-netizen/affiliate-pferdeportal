# SYSTEM 4 ISOLATION — TEST ONLY

Scope: only `isolated_system4/**`.

- Do not modify anything outside `isolated_system4/`.
- Do not import/copy/wrap runtime, workers, gates, handoffs, signers, contracts or state machines from concepts 1–3.
- Historical systems may be read only as inspiration/negative evidence.
- No merge, no production, no publish.
- For the first live test execute exactly:
  `python3 isolated_system4/live_test.py isolated_system4/live_fixture/wordpress_snapshot.json`
- Report the complete stdout and final PASS/FAIL. Do not repair architecture during this test run.
