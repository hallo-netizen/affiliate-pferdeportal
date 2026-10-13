# AFF-ERR-065 – Original Live/Test diagnostics and eBay heartbeat (READ ONLY)

Evidence read 2026-10-13, no WordPress, provider or plugin changes.

## Original WordPress read-only diagnostic, article #972638
Title: Warum sagt man eigentlich „alte Schabracke“?
Both diagnostic exports from 2026-10-12 report Affiliate 6.72.224 and Template Kit 1.50.612. Both article plans report current=false; the cause of staleness is not recorded.

Test environment (2026-10-12T11:04:46Z, 195602-byte JSON): campaign_total=3211; banner all=358, active=161; mandatory_eligible=43; ranked banner candidates=34; plan.status=ready, banner=973719, banner_2=973715, products=none; ranked products=0; idealo import age=499.2h.
Live environment (2026-10-12T11:05:47Z, 48434-byte JSON): campaign_total=2349; banner all=235, active=43; mandatory_eligible=13; ranked banner candidates=0; selected_mandatory_fallback_banner_id=972835; plan.status=no_output, banner=none, banner_2=none, products=none; ranked products=0; idealo import age=499.2h.

FIRST REPRODUCIBLE LIVE-REPORTED CONTRADICTION: live diagnosis finds a nonzero, technically eligible mandatory standby banner (972835) while the saved plan has no output. This narrows the investigation to live 6.72.224 saved-plan selection/fallback/freshness/render boundary, not proven source-absent inventory.
Exact original 6.72.224 PHP/6.72.226 test-ZIP source bytes are not available to the runtime: indexed Project Library lists the original ZIPs, but raw-file materialization was denied. No claim of having compared their original PHP bytes. The canonical GitHub 6.72.211 (now unreleased AFF065 source changes) is not automatically identical to live 6.72.224.

## Current live server signal through existing GitHub eBay heartbeat
Existing untouched workflow: .github/workflows/pferde-atelier-ebay-heartbeat.yml, REST route https://pferde-atelier.de/wp-json/affiliate-zentrale/v1/ebay/tick (POST). No new POST was initiated for this check; only existing completed GitHub Actions logs were read.
All five sampled actual server responses reported status=disabled with contract=external_tick_v2:
2026-10-12T02:23:27Z run 38195587118
2026-10-12T09:33:38Z run 38230669018
2026-10-12T19:19:42Z run 38296901283
2026-10-13T01:31:44Z run 38332552834
2026-10-13T08:27:01Z run 38369322449
In current GitHub source trait-ppar-ebay-run.php::handle_ebay_external_tick, status=disabled is returned when ebay_settings()['enabled'] is empty. Strong direct indication that the public eBay fetch/sync is disabled; not evidence that already materialized products have failed public source checks.
Unchanged public eBay card source gate trait-ppar-ebay.php::ebay_business_campaign_source_allows_delivery_base requires real business-auto marker, strict_v1/concept_v3 contract, source_state=available, nonblocked policy/content, unexpired item and ready/review_last_good route; ebay_public_checkpoint_allows_business_campaign adds a separate checkpoint gate. Do not replace these with enabled=true or bypass them.

## Current decision
Local bounded PHP/WordPress/MariaDB red-green cases remain PASS (38382020308 and 38382652674); they do not prove the 6.72.224 live saved-plan bug fixed.
First remaining evidence barrier: bind the running live/test original PHP source and current live provider/source rows + saved plans, then reproduce the exact no_output/must-fallback contradiction before changing implementation.
No remote toggle, no new plugin, no rebuild, no release.
