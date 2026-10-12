# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.637 LOCAL HARD PASS / WORDPRESS-LIVE HUB2 OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.637_HOBBY_DEPOT_HUB2_CLAIM_EXPAND_TEST_POST_FIX_LOCALPASS.zip`

SHA-256:
`84bcfad3f867356b34f19a2f61b790300f1496869b3e92a3597481e332116e65`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.637_HOBBY_DEPOT_HUB2_CLAIM_EXPAND_TEST_POST_FIX_LOCALPASS.zip`

## Live-Befund 1.50.636
- Beitragsvorschau zeigte keine Testbeiträge;
- Ursache: Hub2 verlangte weiterhin eine gleichnamige WordPress-Beitragskategorie, bevor überhaupt Beiträge abgefragt wurden;
- oberer Text noch zu kurz;
- generisches `Themenbereich` über der H1 soll durch kurzen individuellen Claim ersetzt werden.

## Delta 1.50.637 – nur Hub2
- individueller kurzer Claim pro Kategorie statt `Themenbereich`;
- oberer Text auf ca. 170 Wörter erweitert;
- sichtbarer Lead oben, weitere Vertiefung direkt dort per `Mehr zu <Kategorie> erfahren` aufklappbar;
- kein Hero-Foto;
- 4 Testbeiträge werden beim ersten eingeloggten Admin-/Frontend-Aufruf robust angelegt bzw. vorhandene Testposts wiederverwendet;
- Testposts sind privat und klar mit `[TEST]` markiert;
- jeder Testpost hat Beitragsbild;
- alle vorhandenen Beitragskategorien werden zugeordnet; zusätzlich `journal_cat`, falls Posts unterstützt werden;
- wenn Hub2 keine gleichnamige Beitragskategorie besitzt, zeigt die eingeloggte Hub2-Vorschau gezielt diese 4 privaten Demo-Beiträge statt des leeren Hinweises.

## Freeze / unverändert
- 847/847 Assets byteidentisch zu 1.50.636;
- Hero-Assets byteidentisch;
- Header/Nav unverändert;
- Ebene 1 unverändert;
- Unterkategorie-Iconlogik aus 1.50.636 unverändert;
- Affiliate-Slotlogik unverändert;
- keine Taxonomie-/Architekturänderung.

## Lokal geprüft / simuliert
- PHP **25/25 PASS**;
- ZIP PASS;
- 847/847 Assets byteidentisch;
- Hub2-Simulation 1440 / 1024 / 760:
  - 0 horizontaler Overflow;
  - 4 Beitragskarten;
  - 0 Hero-Bilder;
  - 1 aufklappbarer Intro-Bereich;
  - individueller Claim sichtbar;
  - kein generisches `Themenbereich`;
- Beitragsfallback zusätzlich als PHP-Unit-Harness geprüft: **4 Demo-Karten PASS**;
- 4/4 Beitragsbilder 600×320 im Simulationslauf geladen.

## EXAKT EINE NEXT ACTION
**1.50.637 installieren und live dieselbe Hub2-Seite prüfen: Claim, aufklappbarer Einstieg und 4 Testbeiträge.**
