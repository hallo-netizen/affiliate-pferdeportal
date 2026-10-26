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
- Amazon: ASIN-Brücke aktiv; ASIN kommt ausschließlich aus dem vorhandenen idealo-iPN-Feed. Keine eigene Amazon-Produktsuche.
- Awin/ADCELL/Digistore24/Direktpartner-Engine bleibt zunächst Bestandteil der technischen Basis und wird nur fachlich bereinigt, nicht blind entfernt.

## Credentials

Keine Zugangsdaten werden in diese Akte oder Quellkopie hineindokumentiert.
Die vorhandenen Options-/Konstanten-/Secret-Schnittstellen bleiben als Mechanismus erhalten.
Ein späterer Live-Transfer bestehender Zugangsdaten ist ein separater Laufzeit-/WordPress-Schritt.

## Freigegebener technischer Kandidatenstand

- Installationskandidat vorhanden;
- isoliertes `CURRENT.zip` vorhanden;
- `MANIFEST.md` + `EVIDENCE_GATE5_20261026.md` vorhanden;
- GitHub-Actions-Lauf `40372683116`: SUCCESS;
- Kandidat: `0.1.2-dev`;
- Kandidat SHA-256: `a4f21c7f2a8d89b35e085f2ddf0f06f6940c8b6af34734322fcbd7d8b7e37b36`;
- PR #579 in den Campus gemergt;
- Verbindungsdaten-Preflight aktiv: fehlende Pflichtzugänge werden namentlich angezeigt und blockieren LIVE-PASS;
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
   - Amazon-ASIN-Brücke aus idealo-Feed in frischem WordPress PASS; keine Creators-API erfunden;
   - `CURRENT.zip`, `MANIFEST.md`, `EVIDENCE_GATE5_20261026.md` im Campus.

## Amazon-ASIN-Brücke

- idealo liefert GTIN + `asins_product`; HD-009 speichert beides.
- Bei exakt einer gültigen ASIN kann daraus ein direkter Amazon.de-Produktlink erzeugt werden.
- Partner-/Tracking-ID wird im Backend eingetragen und vom Preflight geprüft.
- Keine eigene Amazon-Suche; keine Amazon-Creators-API erfunden.
- Pro Kategorie-Dreierreihe maximal ein Amazon-Produkt, ohne feste Bindung an Platz 3.

## ERSTER OFFENER BLOCKER

Produktiver Hobby-Depot-Live-Readback fehlt. Provider-Zugangsdaten wurden absichtlich nicht in Quellcode/Campus geschrieben. Nach manueller Installation müssen sie in der WordPress-Laufzeit vollständig vorhanden sein; der neue Preflight sperrt LIVE-PASS bei fehlenden Pflichtwerten.

## EXAKT EINE NEXT ACTION

Den Gate-5-PASS-Kandidaten `0.1.2-dev` manuell installieren und danach den Verbindungsdaten-Preflight abarbeiten. Pflichtwerte: Awin Publisher-ID + API-Zugriffstoken; ADCELL API-Benutzername + API-Passwort; eBay Client-ID + Client-Secret + 10-stellige EPN-Campaign-ID; idealo iPN API-Key + Adspace-ID + Feed-ID; Digistore24 Read-only API-Schlüssel. Danach Verbindungstests, HD-004, eBay/idealo und echten Frontend-/Provider-Readback durchführen. Amazon bleibt bis zu einem belegten realen Adapter `prepared`. Kein Live-PASS ohne vollständigen Preflight und Live-Nachweis.
