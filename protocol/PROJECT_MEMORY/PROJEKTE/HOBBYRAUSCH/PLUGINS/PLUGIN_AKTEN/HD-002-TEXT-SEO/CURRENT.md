# HD-002 – HOBBY DEPOT SEO THEMENENGINE – CURRENT

STAND: 2026-09-30
STATUS: V0.1.0 PRODUCTION CANDIDATE / HARD LOCAL PASS / LIVE-INSTALLATION OFFEN

## Identität

Plugin:
`Hobby Depot SEO Themenengine`

Version:
`0.1.0`

Produktionskandidat:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.0_HD002_PRODUCTION_CANDIDATE.zip`

Installer SHA-256:
`2d3a0bd9180b30ff76e7fb0ed84a8e7cf1a4a7c0d2135999329cb5d11371a684`

Source:
`QUELLCODE_HDTE_V0.1.0_PRODUCTION_CANDIDATE.zip`

Source SHA-256:
`5204950ba0b74e58054a5fddddfdb037ef3daf40baa4fd54b47171d149828a45`

## Harte Projekttrennung

- eigener PHP-Präfix: `HDTE_`;
- eigener Option-/Table-/Hook-Präfix: `hdte_`;
- Projekt-ID: `hobby_depot`;
- keine Runtime-Abhängigkeit vom Pferdeatelier-PSTE;
- keine gemeinsamen Tabellen/Optionen;
- Aktivierungs-/Release-Guard blockiert Fremdprojekt-Reste;
- paralleler Boot mit PSTE ohne Klassen-/Speicherkollision geprüft.

## Referenzbasis

Einmalig als technische Vorlage:
`PSTE-0.57.13-DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS.zip`

Referenz-SHA:
`bb5f3cc84dc00fa85e2c0ddf48c8994a4788c2595c6d98f0d440780377060248`

Finaler Referenzdelta-Check:
**kein neuerer PSTE-Storage-/Performance-Stand vorhanden.**

Die übernommene Storage-/Performance-Logik wurde in HD-002 eigenständig mit `hdte_`-Speichern geführt.

## Produktionscheck

Packaging:
- WordPress-Pluginordner normalisiert auf `hobby-depot-seo-topic-engine`;
- gegenüber dem zuvor geprüften HD-002-Code 135/135 interne Dateien byte-identisch;
- keine doppelten ZIP-Einträge;
- keine `.orig/.bak/.tmp/.old/~`.

Fresh-Unpack:
- PHP-Lint 80/80 PASS;
- Project Boundary PASS;
- Foreign-Project-Runtime-Reste: 0.

Direkter HD-001 → HD-002 Vertragstest:
- HD-001 erzeugt `APKW_EDITORIAL_INTENT_OWNERSHIP_HANDOFF_V1`;
- HD-002 übernimmt den Handoff als READY;
- Buchbinden Positiv-/Negativfälle: 9/9 PASS;
- falsche FAQ-Zuordnung BLOCKED;
- semantische Dublette BLOCKED;
- fehlender `semantic_intent_key` BLOCKED;
- neuer eigenständiger Intent mit gültigem Owner PASS.

Zusätzliche lokale Tests bleiben:
- Ownership 11/11 PASS;
- Frage≠FAQ 12/12 PASS;
- Family Identity 8/8 PASS;
- Frontend-Boot ohne zusätzliche DB-Writes;
- Admin-Boot ohne Writes;
- Koexistenz neben PSTE PASS.

## Beleggrenze

Noch keine Live-WordPress-Installation.
Noch keine produktive Datenänderung.

## NEXT ACTION

HD-001 V1.9.1 live sauber abnehmen und erst danach HD-002 V0.1.0 installieren.

Anschließend:
1. V1.9.1-Editorial-Handoff in HD-002 importieren;
2. Buchbinden E2E real ausführen;
3. nur die offenen Research-Räume Fragen/Probleme und FAQ nachrecherchieren.
