# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-30
STATUS: V1.9.2 LIVE FAIL / ROLLBACK PASS / V1.9.3 LIVE-READBACK-DIAGNOSE POSITIV+NEGATIV HARD PASS / DIAGNOSE-LIVERUN NÄCHSTES

## Harte Abnahmeregel

**Keine Abnahme ohne dokumentierte lokale Positiv- UND Negativsimulation.**

Ein synthetischer Einzeltest gilt nicht als Beweis für die reale Live-Ursache. Der echte Produktionspfad muss mit dem echten Produktionspaket simuliert sein.

## Live-Befund

V1.9.2 ist live zweimal mit dem echten Buchbinden-Kandidaten am Readback gescheitert:

`DEPLOY_READBACK_MISMATCH | Automatischer Rollback: PASS`

Das exportierte Live-Protokoll bestätigt für beide Buchbinden-Läufe:
- CREATE 7;
- ADOPT_EXISTING 0;
- UPDATE 0;
- UNCHANGED 0.

Damit ist die frühere Parent-/ADOPT_EXISTING-Ursachenannahme für diesen Livefall widerlegt.

## V1.9.3 – Diagnose, kein Produktionsfix

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.9.3`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.3_LIVE_READBACK_DIAGNOSTIC_POSNEG_PASS.zip`

Installer SHA-256:
`6bd488625e545a1921d88423c1658792d8747aa81b035140c93bcc1174a4fda3`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.3_LIVE_READBACK_DIAGNOSTIC_POSNEG_PASS.zip`

Source SHA-256:
`d4258a5c7d873ff024d3027ba2fe3e774c9d3575930f972c238cde8ada43fc62`

Änderung:
- keine Strukturentscheidung geändert;
- keine Research-/Ownership-Regel geändert;
- keine automatische Fehlerreparatur;
- fehlgeschlagener Readback wird vor Rollback gespeichert;
- Fehlermeldung nennt Knoten, Adapter/Taxonomie, abweichende Felder sowie Soll-/Istwerte.

## Lokale Positiv-/Negativsimulation

Exakter Produktionspfad:
- echter Buchbinden-READ_ONLY_PREVIEW;
- echtes Research-Paket;
- 7 CREATE;
- Positiv: Deploy + Readback PASS.

Negativ:
- Seiten-Slug mutiert → `slug` erkannt + Rollback PASS;
- Kategoriename mutiert → `name` erkannt + Rollback PASS;
- Parent mutiert → `parent` erkannt + Rollback PASS;
- concept_id-Meta mutiert → `concept_meta` erkannt + Rollback PASS;
- logical-parent-Meta mutiert → `logical_parent_meta` erkannt + Rollback PASS.

Regression:
- 251/251 PASS;
- Fresh-Unpack PHP-Lint PASS;
- Source↔Installer Runtime-Parität 22/22 byteidentisch.

## Beleggrenze

Die konkrete Live-Abweichung ist noch nicht bekannt.
V1.9.3 ist deshalb ausdrücklich **keine Produktionsabnahme** und **kein behaupteter Fix**.

## NEXT ACTION

V1.9.3 über V1.9.2 installieren.

Der fehlgeschlagene Apply hat die Workspace-Stufe nicht weitergeschaltet; der bestehende serverseitige Dry-Run bleibt auf `dryrun_ready`.

Dann:
`Kategorien → Geprüften Plan anwenden`

Bei erneutem Mismatch liefert die Meldung jetzt:
`node + fields + expected + actual`
und führt weiterhin den automatischen Rollback aus.

Diese exakte Meldung ist die nächste Autorität für den Ursachenfix.
