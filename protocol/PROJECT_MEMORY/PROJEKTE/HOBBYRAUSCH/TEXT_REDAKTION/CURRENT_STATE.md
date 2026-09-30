# HOBBYRAUSCH – TEXT_REDAKTION – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: HD-002 V0.1.1 FRESH-INSTALL-MIGRATION-FIX HARD LOCAL PASS / LIVE-RETEST OFFEN

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_TEXT_REDAKTION`.

## Aktueller Stand

Eigenes Hobby-Depot-Plugin:
`Hobby Depot SEO Themenengine 0.1.1`

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.1_FRESH_INSTALL_MIGRATION_FIX_HARD_PASS.zip`

SHA-256:
`6230a7e7db47dc1c337106051cd658e2093e0a3873dbb4d9225749538123577d`

V0.1.0 ist wegen des live reproduzierten Erstinstallationsfehlers `HDTE_SITE_BASELINE_REQUIRED` superseded.

## Fix

Fresh Install ohne eigenen HDTE-Datenbestand darf die Startmigration ohne Baseline abschließen.

Diese Ausnahme gilt nur bei maschinell verifiziert leerem eigenen Datenbestand.

Bestandsmigrationen bleiben baselinepflichtig und fail-closed.

## Prüfung

- alter 0.1.0-Fehler reproduziert;
- kompletter 0.1.1-Fresh-Install-Ablauf COMPLETE;
- Resume des pausierten Fresh-Install-Jobs PASS;
- 3 relevante Negativfälle BLOCKED wie erwartet;
- PHP 80/80;
- Ownership 11/11;
- Frage≠FAQ 12/12;
- Family 8/8;
- HD-001→HD-002 9/9;
- kritische Storage-/Performance-Dateien 4/4 byte-identisch.

## Projektgrenze

Keine Änderung am Pferdeatelier-PSTE.
Keine Runtime-Abhängigkeit.
Eigene `HDTE_`-/`hdte_`-Identitäten bleiben erhalten.

## NEXT ACTION

0.1.1 über die installierte 0.1.0 ersetzen und anschließend in der Themenengine **„Sichere Migration fortsetzen“** ausführen.

Nach READY:
Owner-Handoff importieren → Gesamtbestand erfassen → Buchbinden-E2E.
