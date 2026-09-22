# Affiliate-Zentrale 6.72.149 candidate binding

- Candidate: AFFILIATE_ZENTRALE_V6.72.149_RANKING_CONTEXT_NORMALIZATION_HARDTEST.zip
- SHA-256: 683e562fa1e7fb618015504ae6a9571d6c9967bbd43429e4d54b24aef7414abd
- Baseline: 6.72.148
- Changed production files only:
  - affiliate-portal-router/pferdeportal-affiliate-router.php
  - affiliate-portal-router/includes/trait-ppar-automation-suite.php
- PHP lint: 21/21 PASS
- Fresh unpack: 27/27 files byte-identical
- Semantic gate: GitHub Actions run 35706830893 SUCCESS
- A/B ranking decisions: 15000
- Old/new result SHA-256: 425003acdcf1b9edb7a37897a369da11d0536b41e689565860fc0fa291966106
- sanitize_key in tested hot path: 161250 -> 27
- Rollback: reinstall 6.72.148; no migration/options/data cleanup required.
