# Universal Product Comparison 0.7.1 – Hard Local Release Receipt

Stand: 2026-09-09
Status: LOCAL + FRESH-ZIP PASS / WORDPRESS-LIVE-RETEST OFFEN

Behobener Realfehler:
`PV-LIVE-001`

Release artifact:
`universal-product-comparison-0.7.1-prototype.zip`

SHA-256:
`5d5bcdc191d64524145486064f6830b6843032402dbae4095bb734939b8fe0fd`

KISS-Fix:
- finaler Status `NO_ELIGIBLE_COMPARISONS` bei 0 gültigen Dossiers + 0 SEO-PASS;
- NO_ELIGIBLE niemals Success-Notice;
- Run-Notice zeigt finalen SEO-PASS-/Blockiert-Stand;
- Kostenlabel eindeutig als Schätzung eines jetzt neu gestarteten Laufs;
- keine Architekturänderung.

Exakter Live-Regressionsfall maschinell:
8 waiting → 16 Provider-Aufrufe → $0.1920 → 8 SEO_BLOCKED → 0 Dossiers → `NO_ELIGIBLE_COMPARISONS`.

PASS:
- PHP-Lint 34/34;
- bestehende 0.6-/0.7-Regressionssuite;
- exakter PV-LIVE-001-Fall;
- Admin NO_ELIGIBLE warning + echter PASS success;
- direkte A-gegen-B-/B-gegen-A-Keyword-Evidenz positiv;
- generische/single-product/zero-volume Evidenz negativ;
- Same-Brand/0g-50g/Profil-Drift/Provider-PARTIAL/Dossier-Drift negativ;
- autoritativer PSTE-0.56.25-Kostencheck: 8 Kandidaten max $0.2496;
- echte PSTE-Themenmap False-Pair-Guard;
- Fresh-ZIP-Wurzel PASS;
- Source↔Fresh-ZIP 44/44 byte-identisch;
- komplette Suite erneut aus frisch entpackter ZIP PASS;
- Mutation-Selbsttest: alter False-PASS, falsche Success-Notice und altes Kostenlabel werden von den neuen Regressionen sicher verworfen.

Autoritative Abhängigkeiten:
- Product Knowledge 0.5.0 SHA-256 `80218ec721631353d62a7e3058e76d9c4a4829802c4d5c6bd6f1f2014b6879e3`;
- PSTE 0.56.25 SHA-256 `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`.

Grenze:
Noch kein WordPress-Live-PASS für 0.7.1. Writer/Draft/Publish bleiben außerhalb dieser Prüfstufe.
