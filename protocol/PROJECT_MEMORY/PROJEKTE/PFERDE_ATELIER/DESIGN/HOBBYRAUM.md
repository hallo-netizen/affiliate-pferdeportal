# DESIGN – HOBBYRAUM

STAND: 2026-09-07
STATUS: AKTIV / KANDIDAT BEREIT

## KLARSTELLUNG

Die vorherigen Kandidaten V1.50.473, V1.50.474 und V1.50.475 sind **REJECTED**.

Der gewünschte Eingriff ist ausschließlich:

**Beitragsvorschau / pa297-popular ↔ Affiliate-Partnerbanner / pa266-network**

Keine andere Seitenstruktur darf verändert werden.

## AKTUELLER KANDIDAT

V1.50.476 wurde frisch aus dem exakten bestätigten V1.50.472-Vorgänger gebaut.

Unverändert:
- H1/Artikelblock;
- Unterkategorie-/Beitragsart-Verweise;
- CSS;
- Texte;
- Karten/Links;
- Beitragsauswahl;
- Affiliate-Auswahl;
- Produktlogik;
- V104.

Nur:
- bestehender pa266-network-Block hinter bestehenden pa297-popular-Block verschoben.

## HARD LOCAL QA

- exakter V1.50.472 ZIP/PHP-Hash: PASS
- 498 Dateien geprüft: PASS
- nur pferde-template-kit.php verändert: PASS
- Artikel-/Verweisblöcke unverändert: PASS
- Bannerblock byte-identisch: PASS
- Beitragsvorschau-Block byte-identisch: PASS
- Kategorie-CSS byte-identisch: PASS
- V104 byte-identisch: PASS
- PHP-Lint: PASS
- ZIP-Readback 498/498: PASS
- Rekonstruktion zu byte-identischem V1.50.472: PASS

NEGATIV:
- Banner wieder vor Vorschau -> BLOCKED / PASS
- Banner dupliziert -> BLOCKED / PASS
- Artikel verändert -> BLOCKED / PASS
- Bannerinhalt verändert -> BLOCKED / PASS

## KANDIDAT

Branch:
`fix/category-banner-popular-swap-v150476-20260907`

Beleg:
`design-baseline/2026-09-07/v150476-banner-popular-swap/`

Installer:
`PFERDE_ATELIER_DESIGN_V1.50.476_CONTRACT_V104_NUR_AFFILIATE_BEITRAGSVORSCHAU_TAUSCH_INSTALLIEREN.zip`

ZIP SHA-256:
`90fd3d607696150564ad08ad071a4047b10aec8c1cd09d84468b09d0659b6207`

## NEXT ACTION

Nur V1.50.476 installieren und dieselbe Seite prüfen.
Bis dahin: kein LIVE-PASS, kein Merge, keine weitere Änderung.
