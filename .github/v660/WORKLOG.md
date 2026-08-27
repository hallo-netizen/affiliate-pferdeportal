# V6.60 final worklog – 27.08.2026

Authority: Multi-Provider Target Contract V1.0 > current source > proven GitHub history > assumptions.

1. V6.58 installer was re-extracted and bound as exact baseline.
2. Real idealo feed 2747 was audited: 515,554 rows, 0 malformed, 655 selected rows.
3. Exact public target scope was restricted to existing canonical targets: Reithelme, Reitstiefel, Gerten. Reitbekleidung remains staged-only.
4. idealo adapter completed as an independent provider with neutral normalized product data, explicit opt-in, stale-data guard and Last-Good behavior.
5. V6.58 API redirect 403 root cause handled by host-bound manual redirects that preserve POST and x-api-key.
6. Full-feed staging was snapshot-bound so removed products cannot be rematerialized from stale rows.
7. Output modes added without changing upgrade default: ebay_only, idealo_only, separate, combined, automatic.
8. Cross-provider identity hardlocked to exact normalized GTIN only. No fuzzy/title/image/AI match.
9. Multi-button cards render only real available provider URLs. Single-provider markup stays unchanged.
10. Article-plan dedupe is provider-separated in separate mode and exact-GTIN identity based in combined/automatic.
11. eBay mode guards were kept narrow; canonical eBay run/heartbeat/safe-gap files remained byte-identical.
12. Scoped CSS added only for multi-provider action groups; designplugin untouched.
13. Hard local gates run: real-feed contract, idealo positive/negative, eBay randomized parity, article modes, markup byte parity, static whole-workflow, PHP lint, fresh-unpack/hash/ZIP structure.
14. Final installer created as one V6.60 package; no intermediate plugin releases are part of the final handoff.

External configuration only: the actual iPN-generated full-feed download URL is still needed for autonomous feed downloading and is deliberately not guessed.