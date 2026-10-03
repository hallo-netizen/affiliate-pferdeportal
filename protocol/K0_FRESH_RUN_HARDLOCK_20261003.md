# K0 fresh-run hardlock

New upload + `K0:start` must always produce a fresh K0 production run.

Forbidden for a new request:
- reuse of an existing `WORDPRESS_SINGLE.json` or `WORDPRESS_BATCH.json` as the final result;
- treating an identical batch hash as execution proof;
- reusing previous writer, LanguageTool 6.8, PPM 6.7.9 or export PASS as proof of the new request.

Required before visible output: new run identity and fresh gate chain for this request.

Scope: K0 only.
