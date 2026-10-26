# HOBBYRAUSCH – AFFILIATE – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: AKTIV / HD-009 GATE 4 LOCAL-CI PASS / NOCH NICHT INSTALLIERBAR

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_AFFILIATE`.

## Gebundener Auftrag

Pferdeatelier-Affiliate-Zentrale als technische Basis nach Hobby Depot portieren.

Verbindlich:
- allgemeine Engine, Providerlogik, Kontroll-/Veto-/Output-Logik und Partner-Anbindungen erhalten;
- Pferdeatelier-spezifische Portal-, Produkt-, Banner-, Artikel-, Taxonomie- und Recovery-Bestände vollständig entfernen;
- Zugangsdaten niemals in Campus/Quellcode/Protokoll offen speichern; vorhandene Konfigurationsschnittstellen erhalten;
- eBay- und idealo-Recherche exakt übernehmen und auf Hobby-Depot-Ziele neu anbinden;
- Amazon nicht erfinden: aktuelle Pferdeatelier-Quelle enthält nur einen vorbereiteten Providervertrag, keinen realen Amazon-Adapter;
- vor Installationskandidat vollständige Positiv-/Negativ-/Regressionstests.

## Technische Arbeitsbasis

Arbeitsbranch:
`hobbyrausch/hd009-affiliate-port-20261026`

Plugin-Akte:
`../PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/CURRENT.md`

Ausgangsquelle:
Branch `affiliate-release-current` →
`release/affiliate-zentrale/current/affiliate-portal-router/`

Ausgangsstand:
- 28 autoritative Quelldateien byte-identisch in HD-009 WORKSOURCE kopiert;
- danach ausschließlich in der Hobby-Depot-Arbeitskopie weiterarbeiten;
- Pferdeatelier-Releasebranch bleibt unverändert.

Bereits entfernt:
- `assets/ebay-portal-catalog-v2.json`
- `assets/portal-structure-v279.json`
- `recovery/aff043-historical-product-state-20260915.json`

## Aktueller belastbarer Providerstand

- eBay: echte aktive Implementierung vorhanden.
- idealo: echte aktive Implementierung vorhanden.
- Amazon: nur `prepared`; laut Quellcode fehlt der reale Adapter bis echter Zugang vorhanden ist.

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
   - eBay und idealo verwenden die zentrale Hobby-Depot-Zielquelle.
   - alte gelöschte Pferdeprojekt-Dateiquellen sind aus aktiven Pfaden entfernt.
   - Amazon bleibt vorbereitet; kein Adapter erfunden.

4. **GATE 4 – Positiv/Negativ/Regression: PASS**
   - geprüfter Quellstand: `a1b482e4e1b70163ec48b32dc2bd5780eb5f72ec`;
   - GitHub-Actions-Lauf `40319481655`, Job `121560434781`: SUCCESS;
   - PHP-Lint 23/23 PASS;
   - gültiger HD-004-Snapshot → HD-009 → eBay/idealo PASS;
   - Registry/Snapshot/Weltzahl/<300-Hobbyziele/eBay/idealo fail-closed NEGATIV PASS;
   - Fremdprojektdateien/-marker Regression PASS;
   - Amazon bleibt `prepared` und ohne aktiven Adapter PASS.
   - Evidence: `../PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE_GATE4_20261026.md`.

5. **GATE 5 – Installationspaket/CURRENT.zip:** OFFEN.

## Erster offener Blocker

Ein installierbarer, fresh-unpack-geprüfter HD-009-Kandidat mit realem WordPress-Aktivierungs-/Laufzeitnachweis und anschließendem isoliertem `CURRENT.zip`/Manifest fehlt noch.

## NEXT ACTION

GATE 5 ausführen: aus dem Gate-4-PASS-Quellstand einen einzigen HD-009-Installationskandidaten bauen, Fresh-Unpack/Pluginstruktur/Version/SHA-256 prüfen und in einer frischen WordPress-Laufzeit aktivieren. Dabei HD-004-Verfügbarkeit positiv und fehlend fail-closed sowie eBay/idealo/Amazon-Status regressiv prüfen. Erst nach vollständigem PASS `ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip` + `MANIFEST.md` synchronisieren. Kein Live-PASS behaupten.
