# Affiliate Router 6.72.171 – final combined release evidence

Date: 2026-10-01
Branch: affiliate-release-current
Workflow run: 36842612555
Tested head before release-binding-only commit: 5a1ba68eb5c84378b2bb201628b6b6985564098a
Source manifest SHA-256: 5094f6df73c172b01819294d3dd455002fa244aa9676da0ebbbb4b058530dda4
Final installer SHA-256: dbe630c72f5273abb5c3b48223bbed00498be0a0578f18eca3f001e92bb03fba
Final installer: release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.171.zip

## Current combined gate

- Exact source binding: PASS
- Exact delta versus released 6.72.170: PASS; only main router, automation target-rank cache and eBay request-local cache changed.
- PHP lint: 21/21 PASS
- Existing provider / Awin / OTTO / banner regressions: PASS
- WordPress 7.1.2 + MariaDB activation/regressions: PASS
- 6.72.170 -> 6.72.171 existing frontend query equivalence: PASS
- 6.72.170 exact-GTIN positive/negative rootfix regression: PASS
- Recovery sweep + housekeeping regression: PASS
- Product deals + partner analytics gate: PASS
- Universal manual import positive/negative gate: PASS
- Frontend smoke: PASS
- Exact local A-B run 36839006440: PASS; functional 1:1; 393.694 ms -> 365.895 ms (7.06 %).
- 2012-row snapshot exact A-B run 36839006513: PASS; functional 1:1; total 1248.595 ms -> 249.597 ms (80.01 %), hub 71.20 %, leaf 89.87 % faster.
- Deterministic installer file count: 27 PASS
- Source -> ZIP byte identity: 27/27 PASS
- Fresh-unpack PHP lint: 21/21 PASS

## Result

FULL_COMBINED_RELEASE_GATE=PASS
REAL_SERVER_READBACK_REQUIRED_AFTER_RELEASE=YES
