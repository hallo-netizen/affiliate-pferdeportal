# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-28
STATUS: V1.8.8 PERSISTENT GUIDED FLOW GEBAUT / LIVE-INSTALLATION ALS NÄCHSTES

## Aktueller Stand

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.8.8 Hobby Depot Persistent Flow`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.8_HOBBY_DEPOT_PERSISTENT_FLOW.zip`

Installer SHA-256:
`eae83b6b472de2e78993d271b0da9d57021ba7134d51b7150f0b99c63bd4a85b`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.8.8_HOBBY_DEPOT_PERSISTENT_FLOW.zip`

Source SHA-256:
`4bb9929946941f5be75574ebb869408a3154255f56d2f8e28cc1ecdb5d4b9c62`

## V1.8.8 – Ursache der unnötig komplizierten Bedienung behoben

Bisher:
- derselbe Zwischenstand musste zwischen internen Stufen wiederholt heruntergeladen und erneut hochgeladen werden;
- kostenlose Preflights und Folgeaktionen waren an kurzlebige Transient-Tokens gebunden;
- die DataForSEO-Verbindung erschien als wiederkehrender Bedienpunkt;
- die technische Einzelwerkzeug-Ansicht dominierte den normalen Ablauf.

Jetzt:
- aktueller Workflow-Arbeitsstand wird serverseitig persistent gespeichert;
- intern erzeugte Drafts, Global-Coverage, Research, FINAL und Deployment-Dry-Run werden automatisch weiterverwendet;
- derselbe Zwischenstand muss nicht mehr erneut hochgeladen werden;
- eine Datei wird nur noch einmal ausgewählt, wenn wirklich ein neuer externer Stand hereinkommt, z. B. eine korrigierte Chat/Master-Datei;
- DataForSEO-PASS wird an Credentials + Markt + Sprache gebunden gespeichert und nur bei Änderung ungültig;
- normale Oberfläche zeigt Status + genau die nächste zulässige Aktion;
- bisherige Einzelwerkzeuge bleiben vollständig als technische Notfallansicht erhalten.

## Funktionsschutz

Unverändert aktiv:
- explizite Bestätigung vor Paid-Calls;
- serverseitig signierte Sichtfreigaben;
- Scope-/Research-/Hash-Bindung;
- Global-Coverage- und Detailresearch-Gates;
- Spezialisierungs-Tiefenprüfung;
- read-only Gesamtprüfung;
- FINAL_APPROVED;
- Deployment-Dry-Run;
- explizite Schreibfreigabe;
- Readback;
- Idempotenz;
- Drift-Schutz;
- Rollback.

## Tests

- Source Vollsuite: 229/229 PASS;
- Fresh-Unpack-Installer: 229/229 PASS;
- Source PHP-Lint: 18/18 PASS;
- Installer Runtime PHP-Lint: 17/17 PASS;
- Runtime-Parität Source↔Installer: 22/22 Dateien byteidentisch;
- Produktion-PHP Pferde-Domain-Scan: 0 Treffer.

## Live-Teststand vor Update

- DataForSEO live PASS;
- 4 Paid-Calls;
- Kosten 0.06804 USD;
- bereinigter Initial-Draft live serverseitig signiert;
- signierte Datei:
  `kategorie-research-draft-initial-freigegeben-20260928-104812-utc.json`
- noch kein WordPress-Write.

## NEXT ACTION

V1.8.8 über V1.8.7 installieren. Danach den bereits signierten Initial-Draft genau einmal unter `Arbeitsstand übernehmen` laden. Ab dann verwendet der normale Ablauf diesen Stand serverseitig weiter; nächster sichtbarer Schritt ist direkt `Global-Coverage starten`.
