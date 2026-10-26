# HD-009 – HOBBY DEPOT AFFILIATE-ZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: GATE 4 LOCAL-CI PASS / GATE 5 OFFEN / KEIN RELEASE

Plugin-ID: HD-009-AFFILIATE-ZENTRALE
Name: Hobby Depot Affiliate-Zentrale
Art: Portierung der Pferdeatelier Affiliate-Zentrale

Fach-Current:
../../../AFFILIATE/CURRENT_STATE.md

Arbeitsbranch:
`hobbyrausch/hd009-affiliate-port-20261026`

Arbeitsquelle:
`WORKSOURCE/affiliate-portal-router/`

## Exakte Ausgangsbasis

Quelle:
`affiliate-release-current:release/affiliate-zentrale/current/affiliate-portal-router/`

Pferdeatelier-Branch-Head bei Übernahme:
`7375bc46a57ac4c2ff2a74a6dd4919113defd009`

Formaler Pferdeatelier-Kandidat:
6.72.211 / RELEASE BLOCKED durch AFF-ERR-065.

Wichtig:
Die Hobby-Depot-Portierung übernimmt die technische Quelle als Ausgangsbasis, nicht den Pferdeatelier-Release-/Live-PASS-Status.

28/28 Quelldateien wurden zunächst byte-identisch kopiert.
Danach entfernt:
- Pferdeatelier eBay-Zielkatalog;
- Pferdeatelier Portalstruktur;
- historischer Pferdeatelier-Recovery-Produktbestand.

## Provider-Wahrheit

- eBay: aktiv implementiert.
- idealo: aktiv implementiert.
- Amazon: nur vorbereitet; kein realer Adapter vorhanden.
- Awin/ADCELL/Digistore24/Direktpartner-Engine bleibt zunächst Bestandteil der technischen Basis und wird nur fachlich bereinigt, nicht blind entfernt.

## Credentials

Keine Zugangsdaten werden in diese Akte oder Quellkopie hineindokumentiert.
Die vorhandenen Options-/Konstanten-/Secret-Schnittstellen bleiben als Mechanismus erhalten.
Ein späterer Live-Transfer bestehender Zugangsdaten ist ein separater Laufzeit-/WordPress-Schritt.

## Noch nicht freigegeben

- keine Installations-ZIP;
- kein CURRENT.zip;
- kein Liveeinsatz;
- keine Hobby-Depot-Produktdaten;
- keine Amazon-Produktrecherche behaupten;
- keine Pferdeatelier-Zielbestände wiederverwenden.

## Zwischen-Gates – Stand 2026-10-26

1. **GATE 1 – Pferdeatelier-Bereinigung: PASS**
   - Pferdeatelier-eBay-Zielkatalog entfernt.
   - Pferdeatelier-Portalstruktur entfernt.
   - historischer Pferdeatelier-Recovery-Produktbestand entfernt.
   - verbleibende PHP/JS/CSS-Dateien vollständig auf Pferd/Pferdeatelier/Horse/Equine/Pony/Fohlen/Hengst/Stute/Wallach/Rasse/Breed/Sattel/Schabracke/Huf/Trense/Zaum/Halfter gescannt.
   - aktive Pferde-Fachlogik: 0 Treffer; letzte reine Rassen-/Breed-Altkommentare entfernt.

2. **GATE 2 – Hobby-Depot-Zielquelle: PASS (Vertrag), LIVE noch nicht geprüft**
   - `class-hdar-hobby-depot-source.php` nutzt ausschließlich die read-only HD-004-Kategorie-Registry.
   - verwendete API `hd_category_registry_ready()`, `hd_category_registry_revision()`, `hd_category_registry_snapshot()` stimmt exakt mit `KATEGORIE_ZENTRALE/RUNTIME_API.md` überein.
   - fail-closed bei fehlender Registry, ungültigem Snapshot, != 8 CORE-Welten oder < 300 strukturell belegten Hobbyseiten.
   - keine zweite Kategorie-/Produkt-Masterdatenhaltung im Affiliate-Plugin.

3. **GATE 3 – Provider-Recherchepfade: STATIC PASS**
   - eBay und idealo lesen beide `HDAR_Hobby_Depot_Source`.
   - gelöschte Altquellen `AFF043`, `portal-structure-v279.json` und `ebay-portal-catalog-v2.json` sind aus den aktiven Pfaden entfernt.
   - Kategorie→Hobby-Zuordnung läuft über `article_targets` aus HD-004.
   - eBay-`catalog_version` wird aus der HD-004-Registry-Revision gebildet.
   - Amazon bleibt vorbereitet; kein Adapter erfunden.
   - Runtime-/WordPress-Beweis folgt erst in Gate 4.

4. **GATE 4 – Positiv/Negativ/Regression: PASS**
   - geprüfter Quellstand: `a1b482e4e1b70163ec48b32dc2bd5780eb5f72ec`;
   - GitHub-Actions-Lauf `40319481655`, Job `121560434781`: SUCCESS;
   - PHP 23/23 PASS;
   - Positiv HD-004 → HD-009 → eBay/idealo PASS;
   - Negativ-/fail-closed-Szenarien PASS;
   - Fremdprojekt-Regression PASS;
   - Amazon prepared/inaktiv PASS;
   - Nachweis: `EVIDENCE_GATE4_20261026.md`.

5. **GATE 5 – Installationspaket/CURRENT.zip:** OFFEN.

## ERSTER OFFENER BLOCKER

Es fehlt ein installierbarer, fresh-unpack-geprüfter HD-009-Kandidat mit realem WordPress-Aktivierungs-/Laufzeitnachweis. Gate 4 ist PASS, aber ausdrücklich noch kein Installations- oder Live-PASS.

## EXAKT EINE NEXT ACTION

GATE 5 ausführen: aus dem Gate-4-PASS-Quellstand genau einen Installationskandidaten bauen; Fresh-Unpack, Pluginstruktur, Version und SHA-256 prüfen; in frischer WordPress-Laufzeit Aktivierung sowie HD-004 positiv/fail-closed negativ und Providerregression testen. Erst danach isoliertes `CURRENT.zip` + `MANIFEST.md` synchronisieren. Kein Live-PASS ohne echten Live-Readback.
