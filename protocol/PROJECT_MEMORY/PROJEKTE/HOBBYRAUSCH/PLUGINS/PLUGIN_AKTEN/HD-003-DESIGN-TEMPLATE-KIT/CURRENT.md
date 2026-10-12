# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.637 LOCAL HARD PASS / LIVE-PASS HUB2 OFFEN**

Version:
**1.50.637**

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.637_HOBBY_DEPOT_HUB2_CLAIM_EXPAND_TEST_POST_FIX_LOCALPASS.zip`

SHA-256:
`84bcfad3f867356b34f19a2f61b790300f1496869b3e92a3597481e332116e65`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.637_HOBBY_DEPOT_HUB2_CLAIM_EXPAND_TEST_POST_FIX_LOCALPASS.zip`

## Scope
Nur Hub2:
- individueller Claim statt `Themenbereich`;
- längerer Text, Lead sichtbar + Vertiefung aufklappbar;
- kein Hero;
- 4 private [TEST]-Beiträge mit Beitragsbild;
- gezielter eingeloggter Demo-Fallback bei fehlender gleichnamiger Beitragskategorie.

## Regression
- 847/847 Assets byteidentisch zu 1.50.636;
- Header/Nav/Hero/Ebene1 unverändert;
- Unterkategorie-Icons unverändert;
- Affiliate-Slotlogik unverändert;
- keine Taxonomie-/Architekturänderung.

## Lokal
- PHP 25/25 PASS;
- ZIP PASS;
- Simulation 1440/1024/760: Overflow 0, 4 Beitragskarten, 0 Hero-Bilder, 1 Details-Bereich;
- 4/4 Beitragsbilder geladen;
- PHP-Harness: fehlende gleichnamige Beitragskategorie → 4 Demo-Karten PASS.

## EXAKT EINE NEXT ACTION
**1.50.637 installieren und live dieselbe Hub2-Seite prüfen.**
