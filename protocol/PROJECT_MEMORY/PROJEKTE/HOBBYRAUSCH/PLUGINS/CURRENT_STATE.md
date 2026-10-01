# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-01
STATUS: HD-001 V1.9.4 LIVE PASS · HDTE LIVE PLAN_HASH_MISSING BLOCKED · HDTE V0.1.4 SERVER-SIDE RESUME COMPLETE-WORKFLOW POS+NEG HARD PASS / LIVE-UPGRADE NÄCHSTES

## HD-001

`Affiliate-Portal Kategorie-Workflow V1.9.4`

Live produktiv:
Deployment + Readback PASS.
Nicht zurückrollen.

## HD-002

Owner-Handoff und Gesamtbestand:
PASS.

Live Portalabgleich:
`BLOCKED · HDTE_CONTEXT_STAGE_PLAN_HASH_MISSING`.

0.1.3 nicht live abgenommen, weil der Admin-Reentry noch vom Browser-JavaScript-Autostart abhing.

## V0.1.4

Installer SHA:
`02d52e326cce990833fb6661885d3ba5e30ab6461af76e8b0a2ebdcc3b78c12d`

Fix:
exakt bekannter BLOCKED-Zustand wird beim Öffnen der Übersicht serverseitig validiert und wieder auf RUNNING gesetzt.

Kompletter lokaler Workflow:
- exakter 0-Themen-Livezustand;
- Admin server-side resume;
- jeder Folgeschritt eigener Request;
- COMPLETE.

Weitere Positivfälle:
missing legacy plan field / fresh workflow / 4 Themen / vorhandener Plan → COMPLETE.

Negativ:
malformed absent plan / actual plan present / structure mismatch / wrong error / wrong phase / missing hash / tampered stage / final structure drift / upstream not deployed → fail-closed.

Fresh Installer:
- 80/80 PHP PASS;
- 135/135 source-installer parity;
- kompletter Pos/Neg-Test wiederholt PASS.

## NEXT ACTION

HDTE 0.1.4 installieren → Themenengine-Übersicht öffnen.

Kein neuer Gesamtbestand.
