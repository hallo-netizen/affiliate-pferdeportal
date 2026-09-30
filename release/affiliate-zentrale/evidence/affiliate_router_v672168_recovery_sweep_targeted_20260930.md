# Affiliate-Zentrale 6.72.168 – Recovery Sweep targeted evidence

Date: 2026-09-30
Base release: 6.72.167 @ 430531bf1834de59984d21d1f60e828c13721256
Target: protocol/AFFILIATE_RELEASE_RECOVERY_SWEEP_MANUAL_HOUSEKEEPING_TARGET_20260930.md
Current source manifest SHA-256: `c38f7eb13702f944fabdec2c8d5de85a7786e037d94201a1e12d2ed5ac128cd4`

## Targeted source result

PASS:
- plugin version bound to 6.72.168;
- 39 AFF039/AFF043/AFF044 write-recovery/admin/runtime functions removed;
- AFF039/AFF043 recovery cron/runtime hooks removed;
- AFF043 automatic init restore removed;
- AFF039/AFF043/AFF044 admin-post handlers and control-center panels removed;
- current eBay core trait is byte-identical to released 6.72.167;
- current eBay run trait is byte-identical to released 6.72.167;
- retained read-only incident helpers are byte-identical to released 6.72.167:
  - aff039_incident_evidence
  - aff039_incident_proven
  - aff043_snapshot
  - category_product_incident_historical_active_lookup
  - category_product_incident_inactive_auto_allowed
- central housekeeping busy gate is byte-identical to released 6.72.167;
- 6.72.167 ended-eBay 7-day compaction contract remains present;
- KISS System exposes `Speicherpflege jetzt starten` and delegates to the existing `run_housekeeping()`;
- central housekeeping retires only obsolete AFF039/AFF043/AFF044 recovery state/options/locks/schedules.

Main plugin reduction:
- 6.72.167: 11167 lines
- 6.72.168 targeted source: 10633 lines
- net main-file reduction: 534 lines

## Safety boundary

The historical hash-bound 2026-09-15 snapshot and minimal read-only category-product fallback remain in this version. They are intentionally not removed until live data proves no current delivery depends on them.

## Status

`TARGETED_SOURCE_PASS_WORDPRESS_MARIADB_FULL_GATE_REQUIRED`

Next action:
`RUN_BOUND_RELEASE_GATES`
