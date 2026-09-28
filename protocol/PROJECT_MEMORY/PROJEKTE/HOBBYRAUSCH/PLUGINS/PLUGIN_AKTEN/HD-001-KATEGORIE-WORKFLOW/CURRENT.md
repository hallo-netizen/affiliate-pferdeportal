# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-28
STATUS: V1.8.9 GUIDED RESUME LOKAL POSITIV/NEGATIV PASS / LIVE-ABNAHME NOCH OFFEN

## Aktueller Stand

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.8.9 Hobby Depot Guided Resume`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.9_HOBBY_DEPOT_GUIDED_RESUME.zip`

Installer SHA-256:
`c415df2c63cf3640f723a763ebe6bf527540d377e104d8ce48e7d427246d2c07`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.8.9_HOBBY_DEPOT_GUIDED_RESUME.zip`

Source SHA-256:
`ceea10f2e9b50f6349e5ea83d48cfed3fc78b360e0eeccff4292d38cbb11ad5a`

## Vereinfachung V1.8.9

- Bei leerem Arbeitsstand ist die einmalig nötige Fortsetzungsdatei direkt sichtbar.
- Kein versteckter Aufklapper mehr als erster Bedienweg.
- Danach bleibt genau eine NEXT ACTION sichtbar.
- Interne Zwischenpakete werden nicht erneut hochgeladen.
- DataForSEO-PASS bleibt bei unveränderten Credentials/Markt/Sprache gespeichert.
- Externe Datei wird nur benötigt, wenn wirklich ein neuer/korrigierter Stand von außen kommt.

## Zusätzlicher Fail-Closed-Schutz

- Eine Datei mit vorhandener, aber ungültiger Initialfreigabe wird nicht still als unsignierter Draft übernommen, sondern abgewiesen.
- Ein global freigegebener Draft ohne zugehörige gespeicherte Global-Coverage wird abgewiesen.
- Eine ungültige Global-Review-Bindung wird abgewiesen.

## Lokale Positiv-/Negativprüfung vor Live-Abnahme

Source Vollsuite: 235/235 PASS.
Fresh-Unpack-Installer: 235/235 PASS.
Source PHP-Lint: 18/18 PASS.
Installer Runtime PHP-Lint: 17/17 PASS.
Runtime-Parität Source↔Installer: 22/22 PASS.

Gezielte Positivtests:
- signierter Initial-Draft → persistenter Workspace → Stage initial_approved;
- derselbe gespeicherte Draft → Global-Coverage ohne erneuten Upload;
- Draft + Global-Paket bleiben parallel persistent;
- DataForSEO-PASS bleibt bei unveränderten Einstellungen gültig.

Gezielte Negativtests:
- manipulierte signierte Struktur → Review ungültig;
- beschädigter Workspace-Payload → BLOCKED;
- Paid Global ohne ausdrückliche Bestätigung → BLOCKED;
- geänderte Verbindungseinstellungen → gespeicherter PASS ungültig.

Exakter aktueller Hobby-Depot-Teststand:
`kategorie-research-draft-initial-freigegeben-20260928-104812-utc.json`
- JSON PASS;
- mode RESEARCH_DRAFT;
- project_id hobby-depot-testlabor-20260928;
- lokal neu berechneter Review-Scope entspricht exakt dem gespeicherten Scope:
`998699f3c2508427608f303c2c8008ea3c68a9e76497bfdccfc23fbb81813c74`;
- serverseitige HMAC-Signatur vorhanden; kryptographische Verifikation erfolgt absichtlich nur auf derselben WordPress-Installation mit deren geheimem WordPress-Salt.

## Live-Teststand

V1.8.8 ist aktuell live sichtbar:
- DataForSEO verbunden;
- noch kein persistenter Arbeitsstand übernommen;
- noch kein neuer WordPress-Write.

V1.8.9 ist lokal geprüft, aber noch NICHT live abgenommen.

## NEXT ACTION

V1.8.9 über V1.8.8 installieren. Danach die bereits serverseitig signierte Datei genau einmal direkt im sichtbaren Fortsetzungsfeld laden. Erwartung: sofort Stage `initial_approved` und als einzige NEXT ACTION `Global-Coverage starten`. Erst nach diesem Live-PASS ist V1.8.9 abgenommen.
