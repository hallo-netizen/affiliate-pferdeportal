# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: V1.9.4 LIVE PASS / V1.9.5 LOKAL HARD PASS / LIVE-UPDATE OFFEN

## Live-Basis

Aktuell installiert:
`Affiliate-Portal Kategorie-Workflow V1.9.4`

Live:
- Buchbinden Deployment PASS;
- Readback PASS;
- DataForSEO live angebunden;
- Bestand nicht zurückrollen.

V1.9.4 Installer SHA-256:
`85990b87f0ef35530b616df7716547cb20974d1c77ca21aa7b3e0edec723f249`

V1.9.4 Source SHA-256:
`12dcce406d842bd7b8a6cde5af6a54dff2a4bbff3e27528c04231898a8f02e01`

Die exakten V1.9.4-Bytes wurden im Library-Campus-Archiv wiedergefunden und verifiziert.

## V1.9.5 Kandidat

Keine neue Pluginlinie.
Keine neue Architektur.
Exakte V1.9.4-Weiterentwicklung.

Änderungen:
- WordPress-Seiten direkt `publish`;
- Publish-Status in Preflight/Fingerprint/Readback;
- V1.9.4 Draft→Publish einmalig migrierbar;
- danach Statusdrift fail-closed;
- Readback-Statusfehler → automatischer Rollback;
- Normalroute: Review-Receipts automatisch nach Hard-PASS;
- kein Review-Haken und keine zusätzliche Deploy-Freigabe im Normalweg;
- für bestehenden `deployed`-Stand direkter Publish-Migrationsschritt mit denselben Final-/Research-Paketen.

Tests:
- Baseline 251/251 PASS;
- V1.9.5 256/256 PASS;
- Fresh Source 256/256 PASS;
- Runtime-Parität 22/22 PASS;
- Source PHP 17/17 PASS;
- Installer PHP PASS.

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.5_DIRECT_PUBLISH_AUTO_GATES_HARD_PASS.zip`

Installer SHA-256:
`9108b69487ec50fa36def974bfe0c12b5edfc8d099b3eda2c71e4fe0035f470c`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.5_DIRECT_PUBLISH_AUTO_GATES_HARD_PASS.zip`

Source SHA-256:
`70846ca354165e7ca8a85f59b870ca3aa3707c7f2645810842f440433404dd85`

## Beleggrenze

V1.9.5 ist **noch nicht live installiert**.
Kein Live-PASS behaupten, bevor WordPress-Write + Publish + Readback real gelaufen sind.

## NEXT ACTION

V1.9.5 installieren → `Kategorien` öffnen → **„Bestehenden Stand direkt veröffentlichen“** → realen Readback prüfen.

Keine neue Research-Runde.
Keine Baum-Neuerzeugung vor diesem Publish-PASS.
