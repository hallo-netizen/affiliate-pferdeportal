# V6.58 Livebefund – Pluginidentität und 403-Eingrenzung – 27.08.2026

## Live-Screenshot WordPress Plugins
- Genau eine `Affiliate-Zentrale (Portal-kompatibel)` ist aktiv.
- Angezeigte Version: `6.58.0`.
- Keine zweite/alte Affiliate-Zentrale im Pluginbestand sichtbar.
- `Affiliate Portal Template Kit (Pferde-kompatibel)` ist ein separates Design-/Template-Plugin und kein Duplikat der Affiliate-Zentrale; nicht anfassen.
- `Affiliate-Portal Kategorie-Workflow`, `Pferde Atelier Design Core` und `Universal Portal Design Suite` sind im gezeigten Zustand inaktiv und nicht Ursache des V6.58-API-Tests.

## Konsequenz
Die Hypothese 'WordPress führt eine zweite/alte Affiliate-Zentrale aus' ist widerlegt und darf nicht weiter verfolgt werden.

## Lokale Source-Prüfung V6.57 -> V6.58
Nur drei Dateien unterscheiden sich:
- `includes/trait-ppar-idealo.php`
- `pferdeportal-affiliate-router.php` (Versionsbindung)
- `readme.txt`

Byteidentisch zwischen V6.57 und V6.58 bleiben insbesondere:
- `includes/trait-ppar-ebay.php`
- `includes/trait-ppar-ebay-run.php`
- `includes/trait-ppar-output-objects.php`
- `assets/frontend.css`
- `assets/frontend.js`
- `assets/ebay-portal-catalog-v2.json`

Damit gibt es keinen belegten Rückgriff auf eBay-, Output-, Frontend- oder Kataloglogik.

## Offizielle Ingenious-Unterlagen
- `/creatives/productdata/findFeeds` ist als POST dokumentiert.
- API-Key wird als `x-api-key` gesendet.
- `https://api.ingenious.cloud` ist als unified API für plattformspezifische API-Keys dokumentiert.
- Systemgenerierte API-Keys sind für UI-Exporte und Automatisierung vorgesehen.

## V6.58 Source
V6.58 ruft `https://api.ingenious.cloud/creatives/productdata/findFeeds` mit `wp_remote_post(...)`, `x-api-key`, `Content-Type: text/plain` und `redirection => 2` auf.

## 403-Eingrenzung
Der zuvor beobachtete Live-Fehler endete auf einer account-/plattformbezogenen URL unter `api.partner.net.ingenioustechnologies.com/v1/...` und wurde dort als GET/403 sichtbar. Da V6.58 selbst POST auf `api.ingenious.cloud` ausführt, ist die verbleibende Fehlerklasse auf HTTP-Redirect/API-Basis-Pfad/Methodenerhalt eingegrenzt. Ein Credential-, Doppelplugin-, eBay- oder Frontendumbau ist dafür nicht belegt.

## KISS-/Bündelregel ab jetzt
Kein weiterer Mini-Installer nur für Diagnostik. Nächster Release erst als gebündelter Idealo-Block nach harter lokaler Prüfung gegen Gesamtworkflow:
1. API-Transport/Endpoint ohne Methodendrift robust lösen.
2. Metadatencheck für Feed 2747 / Adspace 568313.
3. Automatische Feed-Aktualisierung mit Hash/ETag/Last-Modified und Rate-Limit-Beachtung.
4. Import weiter isoliert und fail-closed; keine öffentliche Idealo-Ausgabe in diesem Block.
5. eBay-/Output-/Frontend-/Katalogdateien hashidentisch halten.
6. Erst nach Live-PASS dieses Blocks getrennte Idealo-Ausgabe; Multi-Shop-Matching noch später.
