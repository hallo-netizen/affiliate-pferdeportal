# HD009 0.1.33 – direkter idealo-Feedimport
Datum: 12.11.2026. Ziel ausschließlich Hobby Depot, HD009.

## Beweis – Warum?
Die bereits aktivierte iPN-API Hobby Depot 568912 / Feed 2747 meldet PASS und Produkte, aber
der vorhandene HD009-Import, der Button und die 12h-Automatik verlangten zusätzlich eine
manuelle Download-URL. Staged 0, Materialisiert 0. Screenshot im Auftrag 12.11.2026.

## Was wurde geändert?
Exakt 2 Dateien des aus dem vollständigen unveränderten HD009 CURRENT 0.1.32 geprüften ZIP:
- includes/trait-ppar-idealo.php: Wenn bestehende API-Verbindung für die eigene Hobby-Adspace
  geprüft, Export aus bestehenden Zugangsdaten serverseitig über
  api.ingenious.cloud/creatives/productdata/export mit CSV+GZIP; bisherige manuelle URL
  bleibt optional; bestehender Download-Worker, Parser, Staging, Zielzuordnung,
  GTIN, Materialisierung, Berechtigungs- und Veröffentlichungsprüfung bleiben identisch.
- hobby-depot-affiliate-router.php: Header/Versionsstand 0.1.33.

Keine zweite Affiliate-Zentrale, kein Core, keine zusätzlichen Tabellen, kein Frontend-HTTP,
keine Fremdportal-Version übernommen. Weder eBay noch Amazon/DataForSEO verändert.
Kein öffentliches Idealo vor Abschluss des tatsächlichen Imports und bewusster Freigabe.

## Prüfvertrag
Quellbasis SHA-256: d433db74b493407a4c26faef591574e644201846078b7aa7aa3541126f9359b8
Neues ZIP SHA-256: b6482b5d880e941c97ac726dffa85fbc46ba8514587e23700951d176ebcb63db
41 Originaldateien, 41 Dateien vollständig CRC-PASS, alle PHP-Dateien Syntax-PASS.
Original Importer, Materialisierung, GTIN-Sperren, Provider-Prüfung und
Hintergrundworker-Methode unverändert (method-by-method geprüft).
Echte PHP-Funktionstests gegen Originalmethoden mit synthetischem Test-API-Key:
own adspace/Feed, falscher Adspace, nicht geprüft, deaktiviert, fehlender Key,
GZIP-Download, JSON-Status, HTTP 429, Doppelstart-Sperre, optionale alte URL.
Runner: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43275891846

## Live-Status und Next Step
Kein echter privater WordPress-/iPN-Feed-Import in GitHub durchführbar.
Nach Installation: Affiliate-Zentrale → Anbieter & APIs → idealo:
Feed jetzt aktualisieren, nach Abschluss Staged/PASS/Materialisiert/Ziele kontrollieren.
Erst dann Ausgabe von bisher ebay_only auf freigegebenen Modus einstellen,
Frontend auf richtige Produkte, Bilder, Zuordnung, Tracking überprüfen.
Release: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hobby-hd009-0.1.33-idealo-direct-20261112
