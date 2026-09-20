# PSTE 0.56.44 independent Codex review

READ ONLY. NO REPAIR. NO COMMIT BEYOND THIS REVIEW BRANCH. NO MERGE. NO PUBLISH.

The file `PSTE_05641_TO_05644_FULL.diff.gz.b64` is the exact gzip+base64 encoding of the complete unified diff from the bound 0.56.41 plugin to candidate 0.56.44.

Decode with:
```
base64 -d PSTE_05641_TO_05644_FULL.diff.gz.b64 | gzip -dc > /tmp/pste.diff
```

Expected raw diff SHA-256:
`043bbedac467a2c20f8cf2b50aa2ec0a0a264485dc6eab0d074fd599ff8ce742`

Review the complete diff against the repository's historical PSTE_0.56.25 post-PR38 behavior and PR #38.

Required checks:
1. Root cause: execution must not stop merely because the response sees its own still-held lock as ARBEITET.
2. Historical RUNNING auto-driver semantics restored for single and breadth.
3. Status is observability only; successful advance continues. Busy/foreign lock is read-only-polled. Unknown transport outcome is not resent.
4. Existing safe cancellation remains valid and cancel is available immediately for fresh single/breadth runs.
5. PR #38 distinct-family / queuedFamilyCount fix remains unchanged.
6. PAA uses async task_post -> tasks_ready -> task_get/advanced, depth 4, with no duplicate post.
7. Coverage only after true exhaustion, through the existing planning/compiler path, and does not assign plan_slot or canonical_article_id.
8. No new article/publish write authority.
9. Retained-backlog reuse is fail-closed and cannot skip a changed retained payload/baseline/inventory/structure/editorial plan/check logic.
10. Identify any regression or missing end-to-end negative case.

Return:
- CODEX_05644_REVIEW: PASS or FAIL
- exact concrete issue(s), if any
- files/functions involved
- no speculative style comments.