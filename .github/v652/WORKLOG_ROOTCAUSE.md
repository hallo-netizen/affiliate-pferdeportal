# V6.52 Root-Cause Worklog — autonomous background execution

Binding basis: V6.51 MASTER contracts. No content/design/fach change. `main` remains unchanged; all work stays on `v652-core-cron-selfpump-rootfix-20260822` / PR #9 draft.

## Live defect carried forward from V6.51

On the real Pferde-Atelier server a newly restarted canonical eBay run persisted as `running` in phase `reconcile_local` but remained at package/tick 0 for hours after the browser was no longer used. This violates the binding no-browser-dependency contract.

## Hard release rule

No PASS, installer or MASTER release may be emitted unless the automated release pipeline itself produces the complete final gate. Every production change invalidates all prior release evidence and forces the complete gate from zero, including historical contracts, real WordPress 7.0.1/PHP 8.4/MariaDB 11.4, autonomous no-browser background execution, failure/restart/concurrency/checkpoint cases, and Fresh-Unpack parity.

## Current V6.52 evidence

- Full release run `32584518233`: BLOCKED in the real WordPress/MariaDB workflow after the V6.52 background-dispatch production step. Final release artifact correctly skipped; only blocked evidence emitted.
- Full release run `32586758988`: BLOCKED at the same real autonomous background gate after replacing CLI-only seeding with one real HTTP seed request. Final release artifact correctly skipped.
- Direct WordPress nonblocking HTTP diagnostic `32587605700`: PASS; three nonblocking `wp_remote_post()` calls reached a local HTTP target.
- Earlier lock/dual-server/multiworker diagnostics were RED. They were not release evidence.
- Corrected isolated transport diagnostic `32590451309`: PASS. With WP-CLI cron spawning disabled during setup, no pre-server lock, automatic `_wp_cron` interference removed, and four PHP workers, `spawn_cron()` produced a real `POST /wp-cron.php` both during a normal request and at shutdown. Both scheduled probes executed exactly once.

## Proven harness root cause for the previous V6.52 real-gate RED

The earlier autonomous self-pump harness bootstrapped WordPress repeatedly through WP-CLI before its local HTTP server existed. Those WP-CLI requests could create a fresh `doing_cron` lock while their nonblocking loopback target was unreachable. The resulting fresh orphan lock made the later seed request look like a concurrent Cron owner and suppressed the first autonomous dispatch. That contaminated the supposed clean no-browser proof.

This is a test-harness defect, not evidence that clean WordPress `spawn_cron()` itself is broken. It does **not** erase the live V6.51 defect and it does **not** prove V6.52 releasable.

## Current complete-gate step

Commits `9eaf22a2d2295424e2f3b947945fc52521ef7ec8`, `bdae9e23a7fd1c279625e9230bdcd5e7de74ff86`, and `1b532588a07c9d4bce9bdc09e3edd4e45a3699e0` harden only the V6.52 real-gate harness: WP-Cron is disabled while WP-CLI prepares the site, `doing_cron` is cleared under that guard, the guard is removed without bootstrapping WordPress, and the actual browser-closed proof runs against a four-worker HTTP server. Production code is unchanged by this harness correction.

The complete V6.52 release pipeline is restarted from zero via wrapper v17. Even if the clean chain succeeds, a fresh/orphan Cron-lock collision remains a mandatory negative liveness case before final release because a single failed handoff must never leave a run indefinitely at tick 0.
