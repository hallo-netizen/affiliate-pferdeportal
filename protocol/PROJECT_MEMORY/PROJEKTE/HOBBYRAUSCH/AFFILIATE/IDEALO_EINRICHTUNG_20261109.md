# Hobbydepot / HD009 – Idealo nach Freischaltung (09.11.2026)

## Autorität / bestehender Stand
- Nutzer meldet: Idealo-Zugang wurde freigeschaltet. **Es wurde noch kein produktiver API-Test nachgewiesen; keine Zugangsdaten vorgelegt oder abgerufen.**
- Gültige Affiliate-Zentrale: HD009 `0.1.32` / `CURRENT.zip`, SHA-256 `d433db74b493407a4c26faef591574e644201846078b7aa7aa3541126f9359b8`.
- Im Originalplugin `affiliate-portal-router/includes/trait-ppar-idealo.php`: eigener Idealo-iPN-Adapter vorhanden, keine Neuprogrammierung nötig.
- IDEALO-eigener Adminbereich: WordPress → Affiliate-Zentrale → idealo, Slug `affiliate-portal-provider-idealo`. Quellprüfung: GitHub Action [42611779132](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42611779132) und [42611946920](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42611946920).
- Für API-Prüfung verlangt das vorhandene Formular: iPN API-Key, Adspace-ID, Portal-spezifische Feed-ID und bestätigte Zuordnung zum Hobbydepot; bereits vorhandene API-Tests verwenden `findFeeds` der autorisierten Partner-API (nicht idealo Händler-PWS-API). Feed-Download-URL erst für vollständigen CSV/GZ-Import und automatische Aktualisierung nötig.
- Das Formular bietet `Speichern & API prüfen`; der API-Test ist getrennt von Produktimport und Ausgabe. Ohne gültigen Feedimport und Freigabe der Ausgaberegeln werden keine Idealo-Kampagnen öffentlich aktiviert.
- Ausgangsoptionen sicher lassen: `Portalweite Affiliate-Ausgabe = Nur bestehende eBay-/Bestandslogik`, `Feed automatisch ...` AUS, keine manuelle Feedaktualisierung und keine Produktkampagnenfreigabe vor PASS. Bestehende DataForSEO-Amazon-Kostenfreigabe bleibt AUS und wird nicht angefasst.
- Sicherheitsregel: Nie API-Key oder eine geheime Feed-Download-URL in Chat/GitHub/Protokolle kopieren. Nur über das Backend eingeben. Statusmeldung des Tests bzw. nichtgeheime Screenshots austauschen.
- Achtung: Normaler Idealo-Publisherfreigabe-Status allein beweist nicht iPN-API- oder Feedberechtigung. Nutzer im Idealo-Partnerbereich prüfen lassen, ob API-Key / Adspace-ID / Feed-ID vorhanden sind; ggf. beim Partnerprogramm klären. Keine Händler-API einsetzen.
- Ausgabemodi im HD009: `ebay_only`, `idealo_only`, `separate`, `combined`, `automatic`; Standard-Linkstrategie `hybrid` (Vergleich allein, Einzelangebot als GTIN-Zusatzbutton).
- Aktuelles vorläufiges Ergebnis: **vorbereitet, keine Liveverbindung getestet, kein idealo-Feed synchronisiert, kein Plugin verändert**.

## Konkreter nächster Schritt
1. Im WordPress-Backend die **Affiliate-Zentrale → idealo** öffnen.
2. Prüfen, ob im freigeschalteten iPN-Konto die drei Daten verfügbar sind. iPN API-Key nur ins WP-Formular eingeben, niemals weiterreichen.
3. `idealo-Verbindung verwenden`, Daten + Portalbestätigung, Feed-Auto-Refresh AUS, öffentlicher Ausgabemodus unverändert; dann `Speichern & API prüfen`.
4. Die **Statusmeldung** (ohne Geheimnisse) prüfen, erst dann Portal-Konzeptabgleich, kontrollierter Import und gezielter Kacheltest; danach Werbeausgabe separat aktivieren.

## Schutz
Keine Änderung an HD003 Design 1.50.810, HD007 Register, K0, Hab & Bewahr oder Affiliate HD009 CURRENT.
