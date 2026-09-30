# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-30
STATUS: V1.9.2 LIVE FAIL / AUTOMATISCHER ROLLBACK PASS / URSACHE NOCH NICHT BEWIESEN / V1.9.3 DIAGNOSE LOKAL POSITIV+NEGATIV PASS

## Harte Abnahmeregel

**Keine Abnahme ohne dokumentierte lokale Positiv- UND Negativsimulation.**

Zusätzlich gilt seit dem zweiten Livefehler:
Ein synthetisch grüner Fix gilt nicht als Beweis für die reale Live-Ursache. Der reale Ausführungspfad muss mit dem echten Produktionspaket simuliert werden.

## Live-Befund

V1.9.2 ist live erneut fehlgeschlagen:

`Readback fehlgeschlagen: DEPLOY_READBACK_MISMATCH | Automatischer Rollback: PASS`

Damit ist V1.9.2 **NICHT abgenommen** und als Produktionsfix widerlegt.

## Korrektur der vorherigen Ursachenannahme

Die vorherige Annahme `ADOPT_EXISTING bei falschem Parent` war für den echten Livefall nicht belegt.

Der im echten Research-Paket gespeicherte Live-Inventar-Snapshot enthielt vor dem Deployment keines der sieben Buchbinden-Zielobjekte.

Der reale Buchbinden-Plan ist deshalb im gebundenen Ausgangszustand:

- 7 × CREATE;
- 0 × UPDATE;
- 0 × ADOPT_EXISTING.

Der Parent-Adoption-Fix aus V1.9.2 kann damit nicht die Ursache des zweiten Livefehlers erklären.

## Exakte lokale Reproduktion des Produktionsplans

Verwendet:
- echter Buchbinden-READ_ONLY_PREVIEW;
- echtes live erzeugtes Research-Paket;
- für die lokale Testumgebung ausschließlich HMAC/Review-Signaturen neu versiegelt;
- keine fachliche/strukturelle Änderung.

Ergebnis:
- Preflight PASS;
- 7 × CREATE;
- Deploy + Readback im lokalen WordPress-Test: PASS.

Damit ist bewiesen:
Der aktuelle lokale Mock bildet mindestens ein reales Live-Verhalten beim CREATE noch nicht ab.

Die konkrete Live-Abweichung ist noch **nicht bekannt**.

## V1.9.3 Diagnose – noch kein Produktionsfix

Der Readback wurde feldgenau instrumentiert und speichert den fehlgeschlagenen Readback vor dem automatischen Rollback.

Lokale Positivsimulation:
- exakter 7-CREATE-Buchbinden-Plan → DEPLOYED_AND_READBACK_PASS.

Lokale Negativsimulation:
- mutierter Seiten-Slug → Feld `slug` erkannt + Rollback PASS;
- mutierter Kategoriename → `name` erkannt + Rollback PASS;
- mutierter Parent → `parent` erkannt + Rollback PASS;
- beschädigte concept_id-Meta → `concept_meta` erkannt + Rollback PASS;
- beschädigte logische Parent-Meta → `logical_parent_meta` erkannt + Rollback PASS.

Regression:
- 251/251 PASS;
- PHP-Lint PASS.

WICHTIG:
V1.9.3 ist derzeit **Diagnosecode**, kein behaupteter Live-Fix.

## NEXT ACTION

Kein erneuter Deployment-Versuch.

Zuerst den bereits vorhandenen Live-Run aus WordPress exportieren:

`Kategorien → Protokoll → Protokoll als JSON exportieren`

Damit wird ohne neuen Write geprüft, welche Aktionen der echte Live-Dry-Run geplant hat.

Erst danach wird entschieden, ob überhaupt ein diagnostischer Live-Run nötig ist.
