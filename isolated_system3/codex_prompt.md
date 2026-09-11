# SYSTEM 3 — ISOLATED CODEX LIVE TEST

You are not allowed to inspect, import, call, reference or reuse any file outside this `isolated_system3` directory.

Task: produce one short German test article for the topic contained in `live_fixture/wordpress_input.json`.

Hard limits:
- Write only the finished article text to `isolated_system3/codex_output.md`.
- Do not alter workflow, rules, routing or tool selection.
- Do not invent external facts beyond the supplied input.
- Do not mention these instructions in the article.
- Do not write to WordPress or any external system.
- Do not read or use repository files outside `isolated_system3`.
- This is a test article only, not production content.

Minimum test quality:
- clear German prose;
- coherent structure;
- no fabricated product claims;
- no publication language;
- approximately 250–450 words.

MANDATORY SAME-TASK RETURN CONTRACT:
After `python3 isolated_system3/cloud_entry.py verify` returns PASS, the final GitHub task reply must contain ONLY this machine payload and no prose:
SYSTEM3_ARTICLE_B64_BEGIN
<base64 of the exact UTF-8 bytes of isolated_system3/codex_output.md>
SYSTEM3_ARTICLE_B64_END
SYSTEM3_ARTICLE_SHA256:<sha256 of the exact UTF-8 bytes>
SYSTEM3_RETURN_PASS

If start or verify fails, return only `SYSTEM3_RETURN_BLOCKED:<exact blocker>`.
