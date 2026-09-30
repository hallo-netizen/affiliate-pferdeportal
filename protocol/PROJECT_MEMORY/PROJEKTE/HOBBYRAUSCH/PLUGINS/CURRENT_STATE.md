# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: HD-001 V1.9.1 + HD-002 V0.1.0 LOKAL HARD PASS / LIVE-ABNAHME OFFEN

## Aktueller belastbarer Stand

Hobby Depot besitzt zwei klar getrennte Pluginstränge:

### HD-001 – Kategorie-Workflow
Aktuell:
`Affiliate-Portal Kategorie-Workflow V1.9.1`

Status:
- Stage-Hardlock;
- Editorial-Ownership-Handoff;
- 248/248 PASS;
- Fresh-Unpack PASS;
- noch nicht live abgenommen.

### HD-002 – Text-/SEO-Plugin
Aktuell:
`Hobby Depot SEO Themenengine V0.1.0`

Status:
- eigener Hobby-Depot-Codepräfix `HDTE_`;
- eigene Speicher-/Option-/Tabellen-/Hook-Präfixe `hdte_`;
- keine Runtime-Abhängigkeit vom Pferdeatelier-PSTE;
- maschinelle Projektgrenze PASS;
- Ownership 11/11 PASS;
- Frage≠FAQ 12/12 PASS;
- Family Identity 8/8 PASS;
- PHP 80/80 PASS;
- Koexistenz mit PSTE ohne Klassen-/Speicherkollision PASS;
- noch nicht live installiert.

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.0_HD002_HARD_LOCAL_PASS.zip`

SHA-256:
`c6b24fdff3499c1e9a1039fae722d6ad8418df215e55a07e394408bbcac9f2a5`

## Harte Projektgrenze

Pferdeatelier-Plugins dürfen aus Hobby Depot nur gelesen bzw. einmalig als Referenzbasis kopiert werden.

Ab der Kopie:
- ausschließlich eigener Hobby-Depot-Strang;
- keine gemeinsamen Optionen/Tabellen;
- keine Bearbeitung des Pferdeatelier-Plugins;
- keine Runtime-Abhängigkeit;
- Fremdprojekt-Reste werden maschinell BLOCKED.

## NEXT ACTION

Vor Liveinstallation von HD-002 einmal Delta prüfen, ob seit dem gebundenen PSTE-Referenzstand ein neuerer Storage-/Performance-Stand vorliegt.

Wenn kein neuer Delta existiert:
1. HD-001 V1.9.1 live sauber abnehmen;
2. HD-002 V0.1.0 installieren;
3. V1.9.1-Handoff in HD-002 importieren;
4. Buchbinden E2E real ausführen.
