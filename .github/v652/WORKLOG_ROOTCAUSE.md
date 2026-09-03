# V6.52 Root-Cause Worklog — autonomous background execution

Binding basis: V6.51 MASTER contracts. No content/design/fach change. `main` remains unchanged; all work stays on `v652-core-cron-selfpump-rootfix-20260822` / PR #9 draft.

## Live defect carried forward from V6.51

On the real Pferde-Atelier server a newly restarted canonical eBay run persisted as `running` in phase `reconcile_local` but remained at package/tick 0 for hours after the browser was no longer used. This violates the binding no-browser-dependency contract.

## Hard release rule

No PASS, installer or MASTER release may be emitted unless the automated release pipeline itself produces the complete final gate. Every production change invalidates all prior release evidence and forces the complete gate from zero, including historical contracts, supported/core-current WordPress real gates, PHP 8.4/MariaDB 11.4, autonomous no-browser background execution, failure/restart/concurrency/checkpoint cases, adversarial Cron-lock liveness, and Fresh-Unpack parity.

## Root-cause evidence

- Full release run `32584518233`: BLOCKED in the real WordPress/MariaDB workflow after the first V6.52 background-dispatch production step. Final release artifact correctly skipped.
- Full release run `32586758988`: BLOCKED at the same real autonomous background gate after replacing CLI-only seeding with one real HTTP seed request. Final release artifact correctly skipped.
- Direct WordPress nonblocking HTTP diagnostic `32587605700`: PASS; three nonblocking `wp_remote_post()` calls reached a local HTTP target.
- Corrected isolated transport diagnostic `32590451309`: PASS. With WP-CLI cron spawning disabled during setup, no pre-server lock, automatic `_wp_cron` interference removed, and four PHP workers, `spawn_cron()` produced a real `POST /wp-cron.php` both during a normal request and at shutdown. Both scheduled probes executed exactly once.
- Full release run `32591220406`: reached the final source gate and then correctly BLOCKED on a V6.51 metadata RED expectation that had become three exact legacy failures rather than two. The V6.51 assertions remain preserved as RED; the successor expectation now records all three exact metadata deltas.
- Adversarial orphan-lock diagnostic run `32592062938`: exact pre-fix V6.52 patch01 counterproof. A fresh `doing_cron` lock produced `COUNT=0` and `CRON_HITS=0` on both WordPress 6.8.3 and 7.0.1. Thus patch01 could still leave an active run indefinitely at tick 0 while incorrectly treating lock presence as successful dispatch.

## Proven test-harness defect in earlier no-browser gate

The earlier autonomous self-pump harness bootstrapped WordPress repeatedly through WP-CLI before its local HTTP server existed. Those WP-CLI requests could create a fresh `doing_cron` lock while their nonblocking loopback target was unreachable. The resulting orphan lock contaminated the supposed clean no-browser proof. The corrected harness disables WP-Cron during CLI setup, clears setup state under that guard, removes the guard without another WordPress bootstrap, and then starts a four-worker HTTP server.

This harness correction does not erase the live defect and is not itself release evidence.

## Production root cause and V6.52 correction

Two technical liveness gaps are handled without changing any provider/content/design/fach rule:

1. The canonical worker event is scheduled as due and handed to WordPress Core Cron at request shutdown so pre-6.9 and current WordPress do not require another browser/page request to start or continue the durable run.
2. A fresh/orphan `doing_cron` lock is no longer accepted as proof that a due worker event has been dispatched. The dispatcher waits only a bounded interval for the existing Cron owner to consume/reschedule the event or release/change the lock. If the due event remains unresolved, the run fails cleanly with `background_transport_lock_timeout`, the stale worker event is cleared, the safe public checkpoint is preserved, and clean restart remains available. Missing worker event/transport and failed handoff likewise fail closed instead of leaving a running zombie.

Production deltas remain restricted to the existing V6.52 technical transport files; no second fach worker and no direct plugin REST/AJAX worker endpoint are introduced.

## Mandatory final gate now wired

Wrapper v20 applies both V6.52 production rootfixes and requires:

- complete V6.51/V6.50.1/historical source contract matrix;
- V6.52 source contract including bounded Cron-lock resolver and fail-closed transport;
- autonomous browser-closed three-tick Core-Cron chain on WordPress 6.8.3 and 7.0.1;
- adversarial fresh/orphan Cron-lock case on WordPress 6.8.3 and 7.0.1 ending terminal `failed`, restart available, safe checkpoint byte-identical, stale worker event cleared and no unrelated request;
- existing real WordPress/MariaDB gates, checkpoint/restart/concurrency/no-progress/failure contracts;
- release metadata followed by the complete matrix again;
- installer and Fresh-Unpack followed by the same complete source and real gates;
- exact source/installer/MASTER parity and release evidence.

Any production change after this point invalidates the run and requires the complete gate from zero again. No installer is released before that final artifact exists.
