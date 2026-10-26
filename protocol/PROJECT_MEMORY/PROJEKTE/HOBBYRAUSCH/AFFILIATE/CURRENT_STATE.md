# HOBBYRAUSCH – AFFILIATE – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: AKTIV / HD-009 GATE 5 WORDPRESS-RUNTIME PASS / INSTALLATIONSKANDIDAT VORHANDEN / KEIN LIVE-PASS

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

5. **GATE 5 – Installationspaket/CURRENT.zip: PASS**
   - GitHub-Actions-Lauf `40337386359`: SUCCESS.
   - Gate-4-Regressionssuite erneut PASS.
   - Fresh-Unpack byte-identisch zur geprüften WORKSOURCE.
   - PHP-Lint 23/23 PASS.
   - frische WordPress-Installation und Plugin-Aktivierung PASS.
   - ohne HD-004-Registry erwartetes fail-closed `hdar_category_registry_unavailable` PASS.
   - mit bereitgestelltem HD-004-Runtimevertrag: 8 Welten / 320 Hobbyseiten / 320 Artikelkategorien PASS.
   - eBay/idealo-Regressionspfade PASS; kein erfundener Amazon-Adapter.
   - isoliertes `CURRENT.zip` + `MANIFEST.md` + Evidence über PR #569 in den Campus übernommen.
   - Kandidat SHA-256: `457628ebe31735928ca73465ea69ac4da5b5a442693ee1a8c652861432d67c81`.

## Erster offener Blocker

Produktiver Hobby-Depot-Live-Readback fehlt. Bestehende Provider-Zugangsdaten sind bewusst nicht im Campus/Quellcode gespeichert und müssen als separater WordPress-Laufzeitschritt übernommen werden.

## NEXT ACTION

Den Gate-5-PASS-Kandidaten in der echten Hobby-Depot-WordPress-Laufzeit installieren, vorhandene Affiliate-Partner-Zugangsdaten über die bestehenden Laufzeit-/Konfigurationsschnittstellen übernehmen, HD-004-Zielquelle sowie eBay/idealo positiv und fail-closed negativ prüfen und anschließend echten Frontend-/Provider-Readback durchführen. Amazon bleibt ohne belegten realen Adapter `prepared`. Erst nach diesem Nachweis Live-PASS setzen.
