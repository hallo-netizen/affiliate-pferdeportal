# HD-009 – HOBBY DEPOT AFFILIATE-ZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: GATE 5 WORDPRESS-RUNTIME PASS / INSTALLATIONSKANDIDAT VORHANDEN / KEIN LIVE-PASS

Plugin-ID: HD-009-AFFILIATE-ZENTRALE
Name: Hobby Depot Affiliate-Zentrale
Art: Portierung der Pferdeatelier Affiliate-Zentrale

Fach-Current:
../../../AFFILIATE/CURRENT_STATE.md

Arbeitsbranch:
`hobbyrausch/hd009-affiliate-port-20261026`

Arbeitsquelle:
`hobbyrausch/hd009-affiliate-port-20261026:protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/WORKSOURCE/affiliate-portal-router/`

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

## Freigegebener technischer Kandidatenstand

- Installationskandidat vorhanden;
- isoliertes `CURRENT.zip` vorhanden;
- `MANIFEST.md` + `EVIDENCE_GATE5_20261026.md` vorhanden;
- GitHub-Actions-Lauf `40337386359`: SUCCESS;
- Kandidat SHA-256: `457628ebe31735928ca73465ea69ac4da5b5a442693ee1a8c652861432d67c81`;
- PR #569 in den Campus gemergt;
- **kein Liveeinsatz / kein Live-PASS**;
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

5. **GATE 5 – Installationspaket/CURRENT.zip: PASS**
   - Fresh-Unpack byte-identisch zur WORKSOURCE;
   - PHP-Lint 23/23 PASS;
   - echte frische WordPress-Installation + Aktivierung PASS;
   - HD-004 fehlt → fail-closed PASS;
   - HD-004-Runtimevertrag vorhanden → 8 Welten / 320 Hobbyseiten / 320 Artikelkategorien PASS;
   - eBay/idealo-Regressionspfade PASS;
   - Amazon weiterhin nur vorbereitet, kein Adapter erfunden;
   - `CURRENT.zip`, `MANIFEST.md`, `EVIDENCE_GATE5_20261026.md` im Campus.

## ERSTER OFFENER BLOCKER

Produktiver Hobby-Depot-Live-Readback fehlt. Provider-Zugangsdaten wurden absichtlich nicht in Quellcode/Campus geschrieben und müssen separat über die vorhandenen WordPress-Laufzeitschnittstellen übernommen werden.

## EXAKT EINE NEXT ACTION

Den Gate-5-PASS-Kandidaten in der echten Hobby-Depot-WordPress-Laufzeit installieren, vorhandene Provider-Zugangsdaten über die bestehenden Konfigurationsschnittstellen übernehmen, HD-004 sowie eBay/idealo positiv und fail-closed negativ prüfen und echten Frontend-/Provider-Readback durchführen. Amazon bleibt bis zu einem belegten realen Adapter `prepared`. Kein Live-PASS ohne diesen Nachweis.
