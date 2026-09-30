# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: HD-001 V1.9.2 LIVE FAIL / ROLLBACK PASS / V1.9.3 DIAGNOSE LOKAL POS+NEG PASS · HD-002 V0.1.1 LIVE-MIGRATION PASS

## HD-001 – Kategorie-Workflow

V1.9.2 ist live erneut mit
`DEPLOY_READBACK_MISMATCH`
fehlgeschlagen.

Automatischer Rollback:
PASS.

Keine Abnahme.

Der zuvor angenommene Parent-Adoption-Fehler war nicht der reale zweite Livepfad:
Der gebundene Live-Inventar-Snapshot enthält keine der sieben Buchbinden-Zielobjekte; der echte Ausgangsplan ist 7 × CREATE.

Exakte lokale Simulation desselben Kandidaten:
- 7 CREATE;
- Deploy + Readback PASS.

Damit besteht eine noch nicht erklärte Differenz zwischen lokalem WordPress-Test und Live-WordPress.

### V1.9.3 Diagnose

Noch kein Produktionsfix.

Positiv:
- exakter Produktionsplan PASS.

Negativ:
- Slug-, Name-, Parent-, concept_id- und logical-parent-Abweichungen werden jeweils feldgenau erkannt;
- automatischer Rollback jeweils PASS.

Regression:
- 251/251 PASS;
- PHP-Lint PASS.

## HD-002 – Themenengine

V0.1.1 Live-Migration COMPLETE.

Weiterhin kein `Gesamtbestand erfassen`, solange der produktive Kategorien-Deploy nicht erfolgreich readback-verifiziert ist.

## NEXT ACTION

Kein erneuter Write.

Zuerst vorhandenes Live-Protokoll exportieren:
`Kategorien → Protokoll → Protokoll als JSON exportieren`

Danach Ursache weiter eingrenzen.
