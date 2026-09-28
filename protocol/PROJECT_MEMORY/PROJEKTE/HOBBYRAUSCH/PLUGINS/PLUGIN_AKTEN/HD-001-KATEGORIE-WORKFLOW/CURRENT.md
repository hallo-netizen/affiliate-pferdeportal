# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-28
STATUS: V1.8.7 SIMPLE REVIEW GEBAUT / INITIAL-REVIEW LIVE BEREITS SIGNIERT

## Aktueller Stand

Neue Bedienversion:
`Affiliate-Portal Kategorie-Workflow V1.8.7 Hobby Depot Simple Review`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.7_HOBBY_DEPOT_SIMPLE_REVIEW.zip`

Installer SHA-256:
`b11313949ef46bf690e48b103cf930c9dad2dd761144d5e9f04a5e41b4bfabe4`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.8.7_HOBBY_DEPOT_SIMPLE_REVIEW.zip`

Source SHA-256:
`97f2ec77bd17f26b0b62d85e67746824bd1435563a9514e238c443dac1a90f70`

## V1.8.7 Reduktion

Entfernt wurden ausschließlich manuelle technische Eingaben bei allen sichtbaren Review-Gates:
- kein manuelles Kopieren des Review-Scope SHA-256;
- keine manuelle Freigabe-Zusammenfassung.

Erhalten bleiben:
- Datei-/Paketbindung;
- sichtbares ausdrückliches Bestätigungs-Häkchen;
- Adminrecht und Nonce;
- serverseitige Berechnung des Review-Scope;
- serverseitig signierte Review-Quittung;
- Hash-/Signaturprüfung der Folgegates.

Der Server erzeugt Hash und Protokolltext automatisch.

Tests:
- Source Vollsuite 227/227 PASS;
- Fresh-Unpack-Installer 227/227 PASS;
- Source PHP-Lint 17/17 PASS;
- Installer Runtime PHP-Lint 16/16 PASS;
- Runtime-Parität Source↔Installer 21/21 byteidentisch.

## Live-Test / bereits erledigte Erstfreigabe

V1.8.6 DataForSEO-Testlabor:
- 4 Paid-Calls;
- 0.06804 USD;
- Research-Draft erzeugt;
- kein WordPress-Write.

Bereinigter Draft wurde live serverseitig als Initial-Review signiert.

Signierte Datei:
`kategorie-research-draft-initial-freigegeben-20260928-104812-utc.json`

SHA-256:
`6f072094c2d0c8255aaada41c43f9ede9e23e1bea7485cadb0f688f37d45c67c`

Review-Scope:
`998699f3c2508427608f303c2c8008ea3c68a9e76497bfdccfc23fbb81813c74`

## NEXT ACTION

V1.8.7 über V1.8.6 installieren. Danach mit der bereits signierten Initial-Datei den kostenfreien Global-Coverage-Prüfplan erzeugen. Keine manuelle Hash- oder Zusammenfassungseingabe mehr.
