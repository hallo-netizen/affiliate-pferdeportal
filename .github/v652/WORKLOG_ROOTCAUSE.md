# V6.52 Root-Cause Worklog — autonomous background execution

Binding basis: V6.51 MASTER contracts. No content/design/fach change. `main` remains unchanged; all work stays on `v652-core-cron-selfpump-rootfix-20260822` / PR #9 draft.

## Live defect carried forward from V6.51

On the real Pferde-Atelier server a newly restarted canonical eBay run persisted as `running` in phase `reconcile_local` but remained at package/tick 0 for hours after the browser was no longer used. This violates the binding no-browser-dependency contract.

## Hard release rule

No PASS, installer or MASTER release may be emitted unless the automated release pipeline itself produces the complete final gate. Every production change invalidates all prior release evidence and forces the complete gate from zero, including historical contracts, real WordPress 7.0.1/PHP 8.4/MariaDB 11.4, autonomous no-browser background execution, failure/restart/concurrency/checkpoint cases, and Fresh-Unpack parity.

## Current V6.52 evidence

- Full release run `32584518233`: BLOCKED in the real WordPress/MariaDB workflow after the V6.52 background-dispatch production step. Final release artifact correctly skipped; only blocked evidence emitted.
- Full release run `32586758988`: BLOCKED at the same real autonomous background gate after replacing CLI-only seeding with one real HTTP seed request. Final release artifact correctly skipped.
- Direct WordPress nonblocking HTTP diagnostic `32587605700`: PASS, proving `wp_remote_post(..., blocking=false)` can reach a local HTTP target in the isolated CI environment.
- Core-Cron multiworker diagnostic `32587822739`: FAIL with `COUNT=0`; no `POST /wp-cron.php` reached the server after the single seed request. This proves the remaining defect is transport/dispatch, not canonical fach-worker logic.
- Earlier lock/dual-server diagnostics also remained RED and were not treated as release evidence.

## Current root-cause step

Commit `67ce4434bb461ee4d05afed98d38bc5da64254c3` adds an isolated diagnostic that compares `spawn_cron()` when invoked during a normal request versus at request shutdown, with automatic core `_wp_cron` removed, a clean cron lock, a local multiworker HTTP server, and no browser/app request after the seed. Its purpose is to prove the exact dispatch boundary before any further production change.

No production change follows until this diagnostic has identified the transport failure. After any production correction the complete release workflow must restart from zero.
