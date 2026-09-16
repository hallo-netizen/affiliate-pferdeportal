# SYSTEM 4A — HARTER STATUS TESTSTRECKE

Stand: 16.09.2026
Ablage: Texterstellungsbüro / Konzept 4A (`isolated_system4a/`)
Statusart: belegter Status-Snapshot; keine neue CURRENT_STATE und keine Produktionsfreigabe.

## 1. Sind alle Regeln positiv und negativ getestet?

**NEIN — 557/557 ist derzeit nicht hart belegt.**

Belegt ist:
- PPM 6.7.9 besitzt ein Register mit 557 aktiven Regeln.
- Es existieren umfangreiche Positiv-/Negativ- und Mutationstests sowie reale LT-/PPM-Acceptance-Läufe.
- Der aktuelle System-4A-Repair-Owner-Workflow ist auf Head `531a40bedf6f4bd9c709d1ad36d4c46db966c166` erfolgreich gelaufen.
- Ein vollständiger 1-Artikel-Regeltest ist mit echtem PPM 6.7.9 und LT 6.8 PASS und enthält gezielte Negativmutationen, beweist aber nicht automatisch 557/557 Einzelregeln.

Nicht belegt ist derzeit eine maschinenfeste Liste `557 Regeln -> je Regel positiver Nachweis + gezielter negativer Nachweis + exakter Fehler/Prüfer` auf demselben aktuellen Head.

Daher darf aktuell **kein 557/557-PASS behauptet werden**.

## 2. Geht die Maschine bei reparierbaren Fehlern zurück statt komplett zu blockieren?

**JA — für reparierbare Fehler ist der Rückgabe-/Repair-Weg gebaut und getestet.**

Belegter Ablauf:
`echter Prüfer -> Fehlerklasse -> Repair-Owner -> Rückgabe an Erzeugerstufe -> Reparatur desselben Artikels/Artefakts -> derselbe Prüfer erneut -> bei PASS weiter`.

Der Workflow `System 4A Repair Owner Contract`, Run `35105842615`, Head `531a40bedf6f4bd9c709d1ad36d4c46db966c166`, ist SUCCESS. Er führt die Repair-Owner-Vertragstests aus, darunter Routing, Fail-closed-Grenzen, Parent-Titel, Parent-Metadaten, Stage-Owner-Return, Source-Acquisition und Machine-Route-Lock.

Der Same-Article-Repair ist zusätzlich konkret getestet: ein reparierbarer LanguageTool-Befund führt zu `REPAIR_REQUIRED`, Owner `DRAFT_WORKER`, danach Reparatur desselben Drafts und erneuter Lauf desselben Prüfers bis `OUTPUT_GATE_REQUIRED`.

## 3. Was wird absichtlich NICHT repariert?

Nicht jeder Fehler darf zurückgeschickt und automatisch repariert werden.

**HARD BLOCK / fail-closed ist korrekt** bei Integritäts-, Sicherheits-, Manipulations-, Hash-/Manifest-, ungebundenen Daten-, echten Tool-/Validator-Ausführungsfehlern und nicht sicher klassifizierbaren Fehlern.

Beispiel: `LANGUAGETOOL_REAL_EXECUTION_FAILED` bleibt harter Block und darf nicht als Textreparatur umgedeutet werden.

## 4. Harte aktuelle Aussage

- Artikelproduktion, Same-Article-Repair und Repair-Owner-Rückgabe sind real getestet.
- Reparierbare Fehler sollen nicht den gesamten Lauf endgültig töten, sondern an den zuständigen Owner zurücklaufen und erneut geprüft werden.
- Sicherheits-/Integritätsfehler blockieren absichtlich.
- **Offen bleibt der vollständige Einzelregelbeweis für alle 557 Regeln.**

## Belege / Verweise

- System-4A-Head der belegten Repair-/Acceptance-Strecke: `531a40bedf6f4bd9c709d1ad36d4c46db966c166`
- Repair Owner Contract Run: `35105842615` — SUCCESS
- Workflow: `.github/workflows/system4a-repair-owner-contract.yml`
- Repair-Tests:
  - `isolated_system4/test_repair_owner_routing_contract.py`
  - `isolated_system4/test_repair_owner_failclosed_contract.py`
  - `isolated_system4/test_parent_title_repair_contract.py`
  - `isolated_system4/test_parent_metadata_owner_authority_contract.py`
  - `isolated_system4/test_stage_owner_return_contract.py`
  - `isolated_system4/test_source_acquisition_owner_contract.py`
  - `isolated_system4/test_machine_route_lock_contract.py`
  - `isolated_system4/test_repair_continuity.py`
- Einzelartikel-Regelbeweis: `isolated_system4/FIRST_FULL_RULE_TEST_ARTICLE_PROOF.json`
- Teststreckenvertrag: `isolated_system4/PROTOKOLL_TESTSTRECKE_V2_20260914.md`

## NEXT ACTION

Nicht neue Architektur bauen. Als nächstes ausschließlich den fehlenden Beweis schließen:

`557 registrierte Regeln -> pro Regel vorhandenen echten Positiv-/Negativnachweis zuordnen -> nur tatsächlich fehlende Mutationen ergänzen -> 557/557 erst nach realem maschinenfestem Nachweis melden.`
