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
   - GitHub-Actions-Lauf `40372683116`: SUCCESS.
   - Gate-4-Regressionssuite erneut PASS.
   - Fresh-Unpack byte-identisch zur geprüften WORKSOURCE.
   - PHP-Lint 23/23 PASS.
   - frische WordPress-Installation und Plugin-Aktivierung PASS.
   - ohne HD-004-Registry erwartetes fail-closed `hdar_category_registry_unavailable` PASS.
   - mit bereitgestelltem HD-004-Runtimevertrag: 8 Welten / 320 Hobbyseiten / 320 Artikelkategorien PASS.
   - eBay/idealo-Regressionspfade PASS; Amazon-ASIN-Brücke aus dem idealo-Feed PASS; keine erfundene Amazon-Creators-API.
   - isoliertes `CURRENT.zip` + `MANIFEST.md` + Evidence über PR #578 in den Campus übernommen.
   - Kandidat: `0.1.2-dev`.
   - Kandidat SHA-256: `a4f21c7f2a8d89b35e085f2ddf0f06f6940c8b6af34734322fcbd7d8b7e37b36`.
   - Verbindungsdaten-Preflight vorhanden: Awin, ADCELL, eBay, idealo und Digistore24 werden auf vollständige Pflichtzugänge geprüft; bei fehlenden Pflichtwerten bleibt LIVE-PASS gesperrt.

## Amazon-ASIN-Brücke

- Quelle: vorhandener idealo-iPN-Feed, Feld `asins_product`.
- Nur Produkte mit exakt einer gültigen ASIN werden verwendet.
- Direkter Amazon.de-Produktlink mit Partner-/Tracking-ID.
- Keine eigene Amazon-Produktsuche und keine erfundene Creators-API.
- In einer Kategorie-Dreierreihe wird höchstens ein geeigneter idealo-Kandidat auf Amazon umgelegt; nicht mehr starr nur auf Platz 3.

## Erster offener Blocker

Produktiver Hobby-Depot-Live-Readback fehlt. Bestehende Provider-Zugangsdaten sind bewusst nicht im Campus/Quellcode gespeichert und müssen nach der manuellen Installation in der echten WordPress-Laufzeit vorhanden sein. Der neue Preflight blockiert LIVE-PASS, solange Pflichtfelder fehlen.

## NEXT ACTION

Den Gate-5-PASS-Kandidaten `0.1.2-dev` manuell in der echten Hobby-Depot-WordPress-Laufzeit installieren. Danach den Verbindungsdaten-Preflight öffnen und sicherstellen, dass alle Pflichtzugänge vollständig sind: Awin Publisher-ID + API-Zugriffstoken; ADCELL API-Benutzername + API-Passwort; eBay Client-ID + Client-Secret + 10-stellige EPN-Campaign-ID; idealo iPN API-Key + Adspace-ID + Feed-ID; Digistore24 Read-only API-Schlüssel. Anschließend Verbindungstests, HD-004-Zielquelle, eBay/idealo und Frontend-/Provider-Readback prüfen. Amazon nutzt ausschließlich eindeutige ASINs aus dem idealo-Feed; Partner-/Tracking-ID bleibt Laufzeitkonfiguration. Erst nach vollständigem Preflight und Live-Nachweis Live-PASS setzen.
