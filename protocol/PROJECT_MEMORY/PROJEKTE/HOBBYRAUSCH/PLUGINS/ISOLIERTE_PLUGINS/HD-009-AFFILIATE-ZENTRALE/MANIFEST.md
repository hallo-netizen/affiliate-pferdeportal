# HD-009 – Hobby Depot Affiliate-Zentrale

Status: INSTALLATIONSKANDIDAT / WORDPRESS-RUNTIME-PASS / KEIN LIVE-PASS
Version: 0.1.1-dev
Datei: CURRENT.zip
SHA-256: 663ff5a77932704ef1e354e37c7591f99046e54f90beb67c03cb63837a155511
Source-Branch: hobbyrausch/hd009-affiliate-port-20261026
Gate-4-Referenz: a1b482e4e1b70163ec48b32dc2bd5780eb5f72ec
Gate-5-Run: 40344179549

Prüfungen:
- Gate-4-Regressionssuite erneut PASS
- Fresh-Unpack byte-identisch zur WORKSOURCE
- PHP-Lint 23/23 PASS
- frische WordPress-Installation PASS
- Plugin-Aktivierung PASS
- HD-004 fehlt → fail-closed PASS
- HD-004-Vertrag vorhanden → 8 Welten / 320 Hobbyziele PASS
- eBay/idealo geladen, Amazon bleibt ohne erfundenen Adapter PASS
- Verbindungsdaten-Preflight vorhanden; frische Installation blockiert korrekt bei fehlenden Pflichtzugängen

Grenze: kein produktiver Live-Readback, keine Zugangsdaten im Artefakt.
