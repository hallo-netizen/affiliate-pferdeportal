# Affiliate Router 6.72.175 – automatic banner full gate

Date: 2026-10-02
Branch: affiliate-release-current
Workflow run: 36993641563
Targeted WordPress/MariaDB simulation run: 36993180309
Source manifest SHA-256: 8a432f663fa9033abb5757b159d2efbd95ecdca0714ca223cdea5a2292196564
Final installer SHA-256: 9a251ce26a607b68b2b790804c335676b239de5ba147172be6da6fa787284101

## Result

- Exact delta versus released 6.72.174: PASS; only classifier/slot selector, full-pool upgrade scheduler, version metadata and readme changed.
- Targeted real WordPress/MariaDB chain: Schabrackendesigner -> Schabracken -> hub2 -> hub_after_cards -> active campaign: PASS.
- Multi-target target choice with FAQ/advice/generic alternatives: PASS.
- Ambiguous target evidence remains fail-closed: PASS.
- Previous-version full-pool cursor reset/replan: PASS.
- Legacy removed-from-automation migration uses valid central control table: PASS.
- Inactive / bad-format / veto negative tests: PASS.
- All non-rootfix plugin files byte-identical to released 6.72.174: PASS.
- PHP lint 21/21: PASS.
- Existing provider/banner regressions: PASS.
- Existing frontend regression versus 6.72.174: PASS.
- 6.72.170 exact-GTIN regression: PASS.
- Recovery/housekeeping regression: PASS.
- Product deals/partner analytics: PASS.
- Manual single-upload importer: PASS.
- Fresh unpack/source ZIP byte identity 27/27: PASS.
- Current frontend smoke: PASS.
- Existing performance hardlocks preserved: PASS.

FULL_BOUND_GATE_672175_AUTOMATIC_BANNER_PASS
