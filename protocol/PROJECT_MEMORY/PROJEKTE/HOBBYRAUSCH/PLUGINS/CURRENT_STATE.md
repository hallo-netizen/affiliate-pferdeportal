# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-01
STATUS: HD-001 V1.9.4 LIVE DEPLOY+READBACK PASS · HD-002 V0.1.2 AUTO-OWNER-HANDOFF HARD PASS / LIVE-INSTALLATION NÄCHSTES

## HD-001 – Kategorie-Workflow

`Affiliate-Portal Kategorie-Workflow V1.9.4`

Live:
- produktiver Buchbinden-Pilot deployed;
- Schreiben und Readback erfolgreich;
- Bestand bleibt stehen;
- nicht zurückrollen.

Owner-Handoff:
- 7 Owner;
- 11 ARTICLE_ONLY;
- 11/11 gebunden;
- READY_FOR_DOWNSTREAM_EDITORIAL_PLANNING.

## HD-002 – Themenengine

Live aktuell:
`0.1.1` / Migration COMPLETE / READY.

Neuer Kandidat:
`0.1.2 AUTO OWNER HANDOFF HARD PASS`

Installer SHA:
`330028c8cd38f7f27664c804dfafa7649bea70e1f3647bc18229b52f2ba06003`

0.1.2 übernimmt beim bestehenden Button
`Gesamtbestand erfassen`
den deployed HD-001 Owner-Handoff automatisch read-only.

Positiv:
- echter Buchbinden-Stand;
- 7 Owner / 11 Assignments;
- Baseline CURRENT;
- 4 produktive Content-Leaf-Kategorien;
- 1 Themenfamilie;
- HD-001 unverändert.

Negativ:
not deployed / Final fehlt / nicht FINAL_APPROVED / Live-Kategorie fehlt / Handoff manipuliert → jeweils BLOCKED.

Paket:
- Source PHP 80/80;
- Fresh Installer PHP 80/80;
- 135/135 Datei-Parität;
- nur 3 Dateien gegenüber 0.1.1 geändert.

## NEXT ACTION

HDTE 0.1.2 installieren → `Hobby Depot Themenengine → Übersicht → Gesamtbestand erfassen`.

Kein manueller Handoff-Import.
