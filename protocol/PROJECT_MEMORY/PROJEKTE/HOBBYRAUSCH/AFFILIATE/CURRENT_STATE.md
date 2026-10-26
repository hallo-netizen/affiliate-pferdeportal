# HOBBYRAUSCH – AFFILIATE – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: AKTIV / HD-009 PORTIERUNG IN ARBEIT / NICHT INSTALLIERBAR

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

## Erster offener Blocker

Verbleibende Pferdeatelier-spezifische Abhängigkeiten im PHP-/JS-/CSS-Code und die fehlende Hobby-Depot-Zielstruktur sind noch nicht bereinigt.

## NEXT ACTION

Verbleibende Pferde-/Pferdeatelier-Abhängigkeiten dateiweise inventarisieren und aus HD-009 entfernen bzw. durch Hobby-Depot-Zielverträge ersetzen, ohne Provider-/Engine-Logik zu beschädigen.
