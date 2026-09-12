# KATEGORIENMODELL – CURRENT STATE

STAND: 2026-09-05

## Status

MODULKLASSE:
**ALLGEMEINGÜLTIG**

Aktueller belegter Master:
**MASTER 016 – R10/R9 Runtime Deployment**

Aktueller belegter Pluginstand:
**V1.8.0**

## Technischer Zweck

WordPress-Plugin:
`Affiliate-Portal Kategorie-Workflow`

Beschreibung aus Pluginheader:
allgemeingültiger SEO-/Affiliate-Kategorie-Workflow für:
- Content
- HivePress/Marketplace
- Journal auf explizit gebundener realer Taxonomie

## Harte Architektur

- 14-stufiger Kategorien-/Research-Kern bleibt read-only;
- `APKW_CONTENT_WRITE_CAPABILITY=false`;
- Post-FINAL-Writer ist intern getrennte Transaktionsschicht derselben Pluginlinie;
- Content → `category`;
- Marketplace → `hp_listing_category`;
- Journal nur auf explizit registrierte/bound Taxonomie;
- keine automatische Taxonomieerzeugung;
- keine stillen Remaps;
- kein Auto-Delete;
- keine autonome Masteränderung.

## R9/R10-Regeln

- SEO-Nachfrage vor Struktur;
- Affiliate-Fit vor Publish;
- keine Bauchgefühl-Kategorie;
- kein starres Mindest-Suchvolumen;
- manuelle Ideen bleiben RESEARCH_CANDIDATE bis Evidenz vorliegt;
- READY/FINAL nur bei 0 unassigned, 0 silent drops, 0 parent-cascade drops;
- Baseline + concept_id-basierte Deltas;
- neue Paid-Research-Aufrufe nur bei echter neuer Research-Identität;
- fachliche Entscheidungen werden nie zwischen Projekten vererbt.

## Prüfstand

Belegt:
- Vollsuite 216/216 PASS
- Fresh Source 216/216 PASS
- Fresh Installer 216/216 PASS
- adversarial Fresh-Unpack PASS
- Source ↔ Installer ↔ MASTER: 0 Diff
- MASTER aktive Vertragsdateien 18/18
- MASTER aktive Regeln 180/180
- Workflow 14/14
- MASTER-Manifest 808/808 PASS
- realer Gaumen-Lauf: SEO 151/151 PASS
- Affiliate-Fit 151/151 PASS
- Lossless Coverage 8.127/8.127
- unassigned=0
- silent_drop=0
- parent_cascade_drop=0
- Mock-Erstimport DEPLOYED_AND_READBACK_PASS
- Zweitlauf 0 Writes / 151 unverändert
- neue unbelegte Kategorie vor Write BLOCKED

## Beleggrenze

**LIVE WORDPRESS DEPLOYMENT ist NICHT als PASS belegt.**

Der Abschlussstatus sagt ausdrücklich:
Installation → serverseitige Stage-13/FINAL-Bindung → Deployment-Dry-Run → Apply → Readback/Baseline wurde auf einer echten Zielinstallation noch nicht als vollständiger Live-PASS ausgeführt.

Kein Chat darf daraus LIVE/PASS erfinden.

## Release-Identitäten

Installer:
`4c98847e96b091955436230b721a39b5049132037546367a810d4ed642f40845`

Source:
`1d17566f309f460e48255b78357912cf5e18b1eba2eed7654516e79c8f9fa7fd`

MASTER:
`2e6990847c5bc32176f87c6f4b006ccdd0f3f57891c176ed5a6874edfdff942c`

Externer Source-ZIP und im MASTER eingebetteter Source-ZIP sind byte-identisch.

## Known Limitations V1.8.0

- 14-Stufen-Kern schreibt absichtlich nichts;
- Post-FINAL-Writer erstellt keine WordPress-Menüs;
- Journal-Taxonomie wird niemals geraten;
- Live-Write bleibt bis serverseitiger FINAL-/Dry-Run-Prüfung fail-closed;
- keine autonomen Paid-Research-Hintergrundcalls.
