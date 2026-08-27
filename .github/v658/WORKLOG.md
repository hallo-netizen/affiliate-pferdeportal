# Arbeitsprotokoll – V6.58 idealo Partner API Metadata Check – 27.08.2026

## Live-Basis
V6.57 isolierte idealo-Prüfstufe ist auf Pferde Atelier live PASS:
- 655 Produkte
- 655 PASS
- 0 WARN
- 515554 Feedzeilen geprüft
- 0 fehlerhafte Zeilen
- keine öffentliche Ausgabe

## Offizielle Dokumentationsbindung
Ingenious dokumentiert `/creatives/productdata/findFeeds` als Partner-API-Endpunkt zur Prüfung von Feed-Aktualität. Request: POST mit `x-api-key`, `adspaceId`, Paging. Relevante Responsefelder: `feedId`, `lastFileHash`, `lastUpdatedAt`, `numberOfProducts`. Die Unified API `https://api.ingenious.cloud` akzeptiert plattformspezifische API-Keys.

## V6.58 Scope
Geändert exakt:
- `includes/trait-ppar-idealo.php`
- `pferdeportal-affiliate-router.php` nur Versionsbindung
- `readme.txt`

Unverändert/hashidentisch zum V6.57-Ausgangsstand:
- eBay-Traits
- Output-Objects
- Frontend CSS/JS
- Designplugin
- Multi-Provider-Matching

## Funktion
- API-Key nur serverseitig im `x-api-key` Header
- Adspace 568313
- Feed 2747
- exakte Feed-ID-Prüfung
- Persistenz von Feed-Hash, letztem Update, Produktzahl, Prüfzeitpunkt
- keine öffentliche idealo-Aktivierung
- manueller CSV/GZ-Import bleibt Fallback

## Lokale Gates
- PHP-Lint PASS
- positiver Partner-API-Harness PASS
- HTTP-401 Negativpfad PASS
- API-Key nicht in URL/Fehlermeldung PASS
- geschützte eBay/Frontend-Parität PASS

## Live offen
Ein echter Klick `Speichern & API prüfen` mit dem bereits gespeicherten iPN API-Key.