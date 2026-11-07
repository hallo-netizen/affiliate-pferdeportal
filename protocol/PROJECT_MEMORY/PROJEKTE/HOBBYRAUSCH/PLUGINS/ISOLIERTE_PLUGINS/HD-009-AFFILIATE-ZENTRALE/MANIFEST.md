# Hobby Depot HD-009 – Einzige aktuelle Affiliate-Plugin-ZIP

Stand: 07.11.2026
Plugin: Hobby Depot – Affiliate-Zentrale
Version: **0.1.12-dev**
Datei: **CURRENT.zip**
ZIP-Größe: **707639 Bytes**
ZIP-SHA-256: `7ebbea15bb9f1692a949c41cc982489f5be2a2d12695e9342cac7dc8ce1550ae`
GitHub-Binär-Blob: `ba3b84f2c891ea8bb4ac8a459438e1b46882f5f6`
Pluginordner: `affiliate-portal-router/`
Plugin-Hauptdatei: `affiliate-portal-router/hobby-depot-affiliate-router.php`

## Verifiziert

- Vollständige 0.1.12-dev-Test-ZIP wurde aus dem echten Hobby-Plugin 0.1.10-dev gebaut; Originaleinstellungen/Pluginordner bleiben erhalten.
- **GitHub-Binärdatei wirklich gespeichert:** Nach dem Schreiben ist sie im offiziellen HD009-Verzeichnis mit 707639 Bytes und dem erwarteten Git-Blob SHA erneut nachgelesen worden.
- ZIP-CRC PASS; 30 reguläre Dateien; 24 PHP-Dateien mit Syntaxprüfung PASS.
- Lokale isolierte Tests PASS: getrennte Amazon+idealo-Startausgabe, ASIN-Anzeigen mit exakter Hobby-Zielzuordnung, zweierlei Bannerformat, leere fremde Ziele, gesperrte fremde/alte idealo-Feed-IDs.
- Altes 0.1.10-eBay-Ursachenfixpaket, HD003/HD004-Hobbyzielbindung und eigene Amazon-ASIN-Brücke bleiben Teil derselben Pluginlinie.

## Geändert in 0.1.12-dev

- Neue sichtbare Unterseite `Affiliate-Zentrale → Amazon + idealo` für selbständige Amazon-DataForSEO-Suche (Admin-Klick; API kostenpflichtig), bewusste Freigabe und Eigenbanner.
- idealo arbeitet parallel mit seinem bestehenden iPN-Feedimport; **keine** feste Adspace-ID 568313 oder Feed-ID 2901 mehr.
- Der Hobby-Depot-Feed muss im Backend ausdrücklich bestätigt und über die Partner-API getestet sein. Erst der anschließend neu importierte zugehörige Feed kann öffentliche idealo-Karten liefern.
- Exakte Hobbyseiten- und Produktkennungen; keine pauschale Synchronisierung zwischen Amazon und idealo; übrige Partner werden im Startmodus nicht sichtbar, ihre Daten bleiben erhalten.
- Zwei selbst entwickelte Modellbau-Motive: Querbanner 1440×240 und Quadrat 700×700; typografischer Fallback bei anderen Hobbys.
- Amazon-Produktkarten ohne unfreigegebene Amazon-Bilder oder Preise.

## Noch nicht geprüft

Keine tatsächliche WordPress-Installation oder produktive Verbindung zu Amazon PartnerNet, idealo iPN oder DataForSEO durch diesen Build. **Ein technisch getesteter Upgrade-Installer, noch kein Live-PASS.**

## Einziger verbindlicher Standort

Fachliches Affiliate-Büro: `../../../AFFILIATE/` und dessen `CURRENT_STATE.md`.
Technische einzige Plugin-ZIP: **diese `CURRENT.zip`**.
Keine zweite Affiliate-Pluginlinie, keine neue Bürostruktur. Ältere HD009-Originale dienen nur als Archiv-/Testquellen.

Einrichtungs- und Prüfbeleg: `../../PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0.1.12_AMAZON_IDEALO_20261107.md`.
