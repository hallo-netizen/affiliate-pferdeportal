# HD-009 – Hobby Depot Affiliate-Zentrale

Status: INSTALLATIONSKANDIDAT / WORDPRESS-RUNTIME-PASS / KEIN LIVE-PASS
Version: 0.1.2-dev
Datei: CURRENT.zip
SHA-256: a4f21c7f2a8d89b35e085f2ddf0f06f6940c8b6af34734322fcbd7d8b7e37b36
Source-Branch: hobbyrausch/hd009-affiliate-port-20261026
Gate-4-Referenz: c1d6fc04ffb50f0f820555954454d07530a2abb2
Gate-5-Run: 40372683116

Prüfungen:
- Gate-4-Regressionssuite erneut PASS
- Fresh-Unpack byte-identisch zur WORKSOURCE
- PHP-Lint 23/23 PASS
- frische WordPress-Installation PASS
- Plugin-Aktivierung PASS
- HD-004 fehlt → fail-closed PASS
- HD-004-Vertrag vorhanden → 8 Welten / 320 Hobbyziele PASS
- eBay/idealo geladen; Amazon-ASIN-Brücke aus idealo-Feed PASS; keine erfundene Creators-API
- Verbindungsdaten-Preflight vorhanden; frische Installation blockiert korrekt bei fehlenden Pflichtzugängen

Grenze: kein produktiver Live-Readback, keine Zugangsdaten im Artefakt.
