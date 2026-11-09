# Idealo Hobbydepot – Historienprüfung und Feed-Blockade (09.11.2026)

## Verbindlicher Befund
- Nutzer: Die Idealo-Freischaltung ist jetzt erfolgt; zuvor konnte im Idealo-Portal der Feed nicht eingerichtet werden. **Die exakte frühere iPN-Meldung/Ansicht konnte aus den verfügbaren historischen Dateien und Gesprächen nicht wiederhergestellt werden.** Daher keine behauptete Diagnose „Freischaltung war definitiv einzige Ursache“.
- Aufgefundene eigene Akte vom 07.11.2026: `AFFILIATE/START_AMAZON_IDEALO_20261107.md` und `PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0.1.12_AMAZON_IDEALO_20261107.md`: Hobbydepot im Idealo-Partnernetz als Website registriert und bestätigt; keine live verifizierte API-/Feed-Freigabe; Altwerte `adspace_id=568313` und `feed_id=2901` ohne Eigentumsnachweis wurden aus HD009 entfernt. Nicht wiederverwenden.
- Live plugin CURRENT HD009 0.1.32: Bestehender `trait-ppar-idealo.php` erwartet API-Key, Hobbydepot-Adspace-ID, Idealo-Advertiser-Feed-ID und explicit `hobby_feed_verified`; `Speichern & API prüfen` ruft `/creatives/productdata/findFeeds`; für echten Import wird die von iPN bereitgestellte Feed-Download-URL benötigt. Standard-Ausgabe `ebay_only`, automatische Feedaktualisierung AUS. **Kein Pluginwechsel erforderlich, bevor Feed-Vorlage vorhanden ist.**
- Unbedingt **Idealo iPN Publisher** (der Kunde vermittelt fremde Produkte), **nicht** Idealo Business Händler-Feed (eigene Produkte an Idealo liefern). Idealo bestätigt separate Affiliate Publisher API: https://partner.idealo.com/de/affiliate-marketing-programm . Ingenious dokumentiert: **Advertiser/Programm stellt Produktdatenfeed bereit**, Publisher nutzt ihn, erstellt nicht selbst die Original-Warenliste; https://ingenioustechnologies.atlassian.net/wiki/spaces/KB/pages/1443561477/How+do+I+manage+a+product+data+feed und https://ingenioustechnologies.atlassian.net/wiki/spaces/KB/pages/1437401137/Managing+the+modules+your+partners+can+use .
- Neu freigeschalteter **Partnerstatus ist nicht automatisch Nachweis**, dass das Produktdatenmodul aktiv/Idealo-Feed freigegeben ist. Der wirkliche Hebel ist die iPN Publisher-Oberfläche; nur sie kann belegen, ob ein Idealo-Feed samt Feed-ID verfügbar ist.

## Nächste Schritte – richtige Reihenfolge
1. **ZUERST iPN-Portal**, nicht WordPress: als Publisher im Hobbydepot-Konto einloggen; Partnerschaften/Programme: `idealo DE` wirklich freigegeben? Hobbydepot-Adspace korrekt? Danach im Creative-/Produktdaten-/Feed-Bereich nach einem **bereits vom Programm angebotenen Idealo-Produktdatenfeed** und dessen Download/Export suchen. **Nicht** als Händler einen eigenen Idealo-Angebotsfeed anlegen.
2. Ist dort ein idealo-Produktfeed auswählbar, Adspace-Zuordnung, Feed-ID und sichere Download-Option/URL im privaten Portal notieren; API-Key über `Access → Credentials` (Ingenious dokumentiertes Menü, tatsächliche iPN-Ansicht prüfen) finden. **Keine Schlüssel/URL in Chat, GitHub oder Screenshot teilen.**
3. Ist nach Idealo-Freigabe der Produktdaten-Bereich leer, Feed gesperrt oder nicht auswählbar, liegt das Problem **vor WordPress**; nicht pseudo-einen WordPress-Feed erstellen. Screenshot der leeren/gesperrten Seite ohne sensible Angaben. Für Berechtigung **idealo Affiliate-Team** `affiliate@idealo.de` kontaktieren mit präziser Bitte: Für den freigegebenen Hobbydepot-Adspace den Idealo-Produktdatenfeed/Feed-Export im iPN aktivieren bzw. Zugriff, Advertiser-Feed-ID und iPN-API-Rechte bestätigen; explizite Ablehnung/Fehlermeldung und keine sensiblen Werte versenden.
4. **Erst nach Idealo-Feed-Nachweis** in WordPress: `Affiliate-Zentrale → idealo`, gültigen API-Key, Hobbydepot-Adspace- und Feed-ID und bestätigte Zuordnung hinterlegen, Ausgabe vorerst `Nur bestehende eBay-/Bestandslogik`, Auto-Refresh AUS; `Speichern & API prüfen`. API-GATE muss konkreten korrekten Feed für Adspace finden. Danach autorisierte Download-URL hinterlegen, Testimport ohne Veröffentlichung, Zuordnung und Bild/Tracking prüfen, Freigabe/Ausgabemodus erst nach PASS.

## Ausdrückliche Ausschlüsse
Keine Vermischung mit `idealo Business` Händler PWS-API oder Händler-CSV-Feed. Keine historischen IDs `568313/2901`, keine Fremdportal-Feeds, kein erfundener Produktdatenfeed. Bestehendes HD009 0.1.32 und alle anderen Plugins unverändert; keine Liveprüfung/Produktimport behauptet.

---

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
