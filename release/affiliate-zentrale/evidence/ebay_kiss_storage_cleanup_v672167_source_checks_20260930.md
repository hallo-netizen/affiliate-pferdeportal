# Affiliate-Zentrale 6.72.167 – eBay KISS + Storage Cleanup targeted evidence

Date: 2026-09-30  
Branch: affiliate-release-current  
Target: protocol/AFFILIATE_RELEASE_EBAY_KISS_STORAGE_CLEANUP_TARGET_20260930.md  
Source manifest SHA-256: `480277aa8850ec5916c62a24548f90155dfa21591228e3c8a41b338ddc46afc4`

## Scope

One bundled eBay cleanup on top of 6.72.166:
- remove obsolete historical eBay recovery/migration runtime paths;
- keep current generic build/checkpoint/fail-closed safety;
- decouple the OAuth connectivity test from provider-channel pause while runtime access remains pause-gated;
- archive/retire terminal runs from historical builds instead of presenting them indefinitely as current operational state;
- compact ended, non-public eBay source payloads after 7 days using the central housekeeping path;
- preserve all current PRIVATE/BUSINESS classification, quality, coverage, output and compliance rules;
- preserve the 6.72.166 performance changes.

## Source delta versus 6.72.166 authority head 40f9575041bc3d9aa7494215cfdccd84eca43667

Current compare at evidence time:
- `trait-ppar-ebay-run.php`: +23 / -894 lines
- `trait-ppar-ebay.php`: +2 / -118 lines
- `trait-ppar-housekeeping.php`: +3 / -2 lines
- `trait-ppar-provider-registry.php`: +1 / -1 line
- `pferdeportal-affiliate-router.php`: +3 / -10 lines
- documentation/governance/manifest changes only outside runtime.

Run trait:
- before: 3015 lines / 103 functions
- after: 2144 lines / 87 functions
- removed old recovery/migration functions: 17
- added current bounded terminal-retirement function: 1

eBay core:
- additional proven-dead compatibility functions removed: 4
- current eBay core after sweep: 10337 lines / 325 functions

## Static source-bound assertions

PASS:
- plugin header + runtime constant are 6.72.167;
- removed historical recovery symbols are absent from current main/run source;
- `maybe_close_incompatible_ebay_run_for_checkpoint_restart()` remains;
- public checkpoint bootstrap/commit remains;
- active-run single-owner / `already_running` behavior remains;
- BUSINESS safe-supply / public invariant gate remains, including `business_gapfill_public_invariant_failed`;
- eBay provider connection test calls `ebay_access_token($settings, true, false)`;
- ordinary runtime calls retain default `$respect_channel_pause = true`;
- central housekeeping targets only exact terminal shape:
  `source_state='ended' AND status='purged_ended' AND listing_post_id=0 AND output_state='inactive'`;
- eBay terminal raw-payload compaction cutoff is 7 days;
- active source rows are not targeted by this cleanup query;
- 6.72.166 bounded BUSINESS source projection remains present;
- current source manifest still contains exactly 27 source files.

## Isolated positive / negative logic simulation

PHP 8.4 local harness: PASS.

Positive:
- provider OAuth test succeeds while provider channel is paused, proving connectivity can be tested independently;
- historical failed terminal run is archived and cleared from current operational state;
- a new manual attempt archives stale terminal state before configuration validation;
- ended + purged_ended + inactive + no listing + older than 7 days is eligible for payload compaction.

Negative / fail-closed:
- normal eBay runtime token request remains blocked when provider channel is paused;
- missing credentials still fail during the connection test;
- current-build failed terminal run remains visible for immediate diagnostics;
- an open/running run is never deleted by terminal-state retirement;
- an active run is never replaced by a new run;
- active source rows are never compacted by the ended-row housekeeping rule;
- listing-linked ended rows are not compacted;
- ended rows younger than 7 days are retained.

Result: `ALL_PASS`.

## Important limitation

This evidence is targeted source + isolated logic evidence. It is **not** the final WordPress/MariaDB/full-release gate and does not authorize a live installer by itself.

## Status

`TARGETED_SOURCE_AND_ISOLATED_LOGIC_PASS_FULL_GATE_OPEN`

Next action:
`RUN_COMBINED_FULL_RELEASE_GATE_FOR_6_72_167`
