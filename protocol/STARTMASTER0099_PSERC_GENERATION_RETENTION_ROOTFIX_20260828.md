# STARTMASTER0099 – PSERC Generation Retention Rootfix

## Root cause
PSERC 0.26.0 introduced the bounded/resumable compile with record-local technical generations and atomic snapshots. Generation-scoped `pserc_plan_<20hex>_*` records were retained without a generation lifecycle GC. Large `bootstrap_000000` records therefore accumulated in WordPress `options`.

## Live evidence 2026-08-28
- current read-only DB observation: 37 bootstrap generations / 361.46 MB, about 9.77 MB each
- earlier user-observed peak: 131 / 1278.96 MB
- current newest generation `35b66dfe0227bdae253d`: ACTIVE + JOB referenced
- no live lease row at evidence time

## Fix PSERC 0.28.14
- lifecycle cleanup operates on complete exact generations, never blanket `pserc_plan_%`
- fail-closed protection: active snapshot, active topic projection/nullpoint source, compile/resume job, job topic source, lease generation, plus 2 newest fallback generations
- automatic bounded GC only after successful snapshot activation, persisted COMPLETE job, and lease release; max one obsolete generation per successful compile
- admin `PSERC Speicherwartung`: mandatory Dry-Run followed by state-hash-bound generation-by-generation legacy cleanup
- deletion scope only exact `pserc_plan_<20hex>_*` option rows plus same-generation PSERC ready/candidate index rows
- uncertainty, running job, live lease, invalid active snapshot, state drift, or DB delete failure => no cleanup / fail closed

## Full local positive/negative release gate
PASS on source, installer re-extract, and final MASTER embedded installer: generation retention, 37-generation model, READY/Handoff hash invariance, resume/job/topic-source/lease protection, forced DB-delete failure fail-closed, title/longtail/duplicate/cannibalization regression, Exact-Five content/design negatives, PSTE 0.56.24 40/40 + 500/500 regression, combined capability, package integrity, PHP lint, protected content/production/design byte audit, final MASTER re-extract and manifest.

Final installer SHA-256: `a5008fc463c78f919a1dc03a510e681c426d97b5f3785de820169805dab3b988`

Final MASTER0099 SHA-256: `e4969a9825011ccf8dd65d61dc41880343bf1948af6c9702e6eea93be0a971f3`

No changes to PSTE, PPM, LanguageTool, article content, design, affiliate, publish logic, duplicate thresholds, or target-keyword authority.