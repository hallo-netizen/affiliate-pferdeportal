# HD-002 – HOBBY DEPOT SEO THEMENENGINE – CURRENT

STAND: 2026-09-30
STATUS: V0.1.1 FRESH-INSTALL-MIGRATION-FIX HARD LOCAL PASS / LIVE-RETEST OFFEN

## Aktueller Kandidat

Plugin:
`Hobby Depot SEO Themenengine`

Version:
`0.1.1`

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.1_FRESH_INSTALL_MIGRATION_FIX_HARD_PASS.zip`

SHA-256:
`6230a7e7db47dc1c337106051cd658e2093e0a3873dbb4d9225749538123577d`

## Live gefundener Fehler in 0.1.0

Fehlercode:
`HDTE_SITE_BASELINE_REQUIRED`

Ursache:
Die sichere Startmigration verlangte bei einer vollständig neuen Hobby-Depot-Installation bereits in `EDITORIAL_INIT` einen Website-Baseline-Snapshot.

Dieser Snapshot kann im Backend aber erst nach erfolgreichem READY-Start und Import des Kategorie-/Owner-Handoffs erzeugt werden.

Damit entstand auf einer Neuinstallation ein echter Start-Deadlock.

V0.1.0:
**SUPERSEDED / NICHT WEITER VERWENDEN.**

## Fix 0.1.1

Eine fehlende Baseline ist ausschließlich dann zulässig, wenn der eigene HDTE-Datenbestand maschinell als vollständig leer bewiesen ist:

- Identity-Modus = `EMPTY_NEW_INSTALL`;
- Topic Pool = 0;
- Candidates = 0;
- Occurrences = 0;
- Assignments = 0;
- History = 0;
- Payload-Integrity-Total = 0;
- Abschlussprüfung bestätigt weiterhin leeren Bestand.

Nur dann wird die baselineabhängige Altbestandsmigration übersprungen und der sichere Erststart abgeschlossen.

Sobald eigener Bestand existiert, bleibt die Baseline zwingend und fail-closed.

## Harte lokale Prüfung

Alter Fehler reproduziert:
- 0.1.0 → `HDTE_SITE_BASELINE_REQUIRED` bei `EDITORIAL_INIT`: PASS.

0.1.1 Positiv:
- kompletter öffentlicher Fresh-Install-Ablauf: Start → 14 request-bounded Schritte → COMPLETE: PASS;
- Fortsetzen eines bereits bei `EDITORIAL_INIT` pausierten Fresh-Install-Jobs: PASS.

0.1.1 Negativ:
- bestehender Bestand ohne Baseline: BLOCKED `HDTE_SITE_BASELINE_REQUIRED`;
- Daten erscheinen während Fresh Install: BLOCKED `HDTE_EMPTY_INSTALL_UNEXPECTED_CANDIDATES`;
- Payload-Bestand > 0 ohne Baseline: BLOCKED `HDTE_SITE_BASELINE_REQUIRED`;
- bestehender Bestand mit gültiger Baseline nutzt unverändert den normalen Editorial-Migrationsweg.

Regression:
- PHP-Lint 80/80 PASS;
- Project Boundary PASS;
- Ownership 11/11 PASS;
- Frage≠FAQ 12/12 PASS;
- Family Identity 8/8 PASS;
- HD-001 → HD-002 Buchbinden E2E 9/9 PASS;
- Worktree ↔ Fresh-Unpack 135/135 byte-identisch.

Performance-/Storage-Schutz:
Diese vier kritischen Dateien sind gegenüber 0.1.0 byte-identisch:
- `class-hdte-repository.php`;
- `class-hdte-research-archive.php`;
- `class-hdte-sandbox-record-store.php`;
- `class-hdte-storage-maintenance.php`.

Änderungsfläche 0.1.0 → 0.1.1:
exakt 2 Dateien:
- Pluginversion;
- Safe-Migration-Job.

## Beleggrenze

Noch kein Live-Retest mit 0.1.1.

## NEXT ACTION

V0.1.1 über die installierte V0.1.0 ersetzen.

Danach im Backend:
**Hobby Depot Themenengine → Sichere Migration fortsetzen**

Erwartung:
der bereits pausierte Fresh-Install-Job läuft bis COMPLETE und die Themenengine wird READY.

Danach erst:
Owner-Handoff importieren → Gesamtbestand erfassen → Buchbinden-E2E.
