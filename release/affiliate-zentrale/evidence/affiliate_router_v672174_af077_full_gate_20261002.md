# Affiliate Router 6.72.174 – AF-077 full gate

Date: 2026-10-02
Branch: affiliate-release-current
Workflow run: 36989328161
Source manifest SHA-256: 8229a121f38b28cc8145789d16642b80769dff1898e4ef5332399164f11b8b04
Final installer SHA-256: e96cc4242e13ad7834405b6e035e3297930aed272de5e43e46bfa7a7173f09b3

## Result

- Exact delta versus released 6.72.173: PASS; only classifier, version metadata and readme changed.
- All non-AF077 plugin files byte-identical to released 6.72.173: PASS.
- PHP lint 21/21: PASS.
- Existing provider/banner regressions: PASS.
- AF-077 Schabrackendesigner -> Schabracken real WordPress/MariaDB positive: PASS.
- Negative creative signal remains blocked: PASS.
- Ambiguous real-target match remains fail-closed: PASS.
- Target veto remains absolute: PASS.
- Existing frontend query behavior versus 6.72.173: byte-identical PASS.
- 6.72.170 exact-GTIN regression: PASS.
- Recovery/housekeeping regression: PASS.
- Product deals/partner analytics: PASS.
- Manual single-upload importer: PASS.
- Fresh unpack/source ZIP byte identity 27/27: PASS.
- Current frontend smoke: PASS.

FULL_BOUND_GATE_672174_AF077_PASS
