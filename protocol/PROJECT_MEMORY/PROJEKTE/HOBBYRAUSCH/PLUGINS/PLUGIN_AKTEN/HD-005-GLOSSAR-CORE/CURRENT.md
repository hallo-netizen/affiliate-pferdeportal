# HD-005 – HOBBY DEPOT GLOSSAR CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.0.25 LAUT WORDPRESS-LISTE AKTIV / LOKALE QA PASS / LIVE-FUNKTIONSPRÜFUNG OFFEN**

Plugin-ID:
`HD-005-GLOSSAR-CORE`

Aktuelles Bundle:
`HOBBY_DEPOT_DESIGN_SEARCH_BUNDLE_20261024_HD003_1.50.731_HD007_1.2.15_HDG_1.0.25_HARDPASS.zip`

SHA-256:
`581736924531499b589a8349fba3b8bf42ef3ffb3755c0043be35a568d1ef4c8`

Pluginroot:
`hobby-depot-glossar/`

Fach-Current:
`../../../GLOSSAR/CURRENT_STATE.md`

## Produktionsstand
- 308 Glossarbegriffe;
- 13 Batches;
- 308 eindeutige external_id;
- 308 eindeutige Slugs;
- Daten/Inhalte gegenüber 1.0.24 unverändert;
- kein Auto-Publish;
- bestehende AJAX-/REST-Sperre des gebündelten Imports bleibt erhalten.

## 1.0.25
- Glossarsuche bleibt normal absendbar als Fallback;
- zusätzlich AJAX-Vorschau ab 2 Zeichen, max. 8 Treffer;
- Suchscope ausschließlich `post_type=hdg_term` und `post_status=publish`;
- normale WordPress-Posts, Seiten und Entwürfe werden nicht in den Vorschlägen ausgegeben;
- globale Hobby-Depot-Hauptsuche bleibt getrennt.

## QA
- echte private `HDG_Manager::validate_batch()` gegen 13/13 Batches: PASS;
- 308/308 Datenbestand und Eindeutigkeit: PASS;
- serverseitiger Scope-Test mit absichtlich eingeschleustem normalen Post + Draft: beide verworfen, PASS;
- Client-Suchskript mit simuliertem Fetch: PASS;
- Fresh-Unpack bytegleich;
- Gesamtbundle PHP 22/22 PASS.

## WordPress-Inventarabgleich 01.11.2026

Die vom Betreiber gelieferte vollständige WordPress-Pluginliste zeigt **Version 1.0.25 als aktiv**. Der zuvor dokumentierte Entwicklungs-/Teststand 1.0.25 ist versionsgleich, aber nicht dadurch funktional live-geprüft. Ein unabhängiger Server-Quellcode-/ZIP-Readback und ein Live-Funktionstest wurden in diesem Abgleich nicht ausgeführt. Keine Plugininstallation oder Campus-CURRENT.zip-Synchronisierung. Beleg: `../../EVIDENCE_WP_PLUGINLISTE_20261101.md`; operative WordPress-Current: `../../../WORDPRESS_TECHNIK/CURRENT_STATE.md`.

## EXAKT EINE NEXT ACTION

**Die laut WordPress-Liste aktive 1.0.25 zunächst im Live-Frontend read-only prüfen und die ZIP-Ablage nachholen; nicht blind durch einen älteren Bundle-Ordner überschreiben.**
