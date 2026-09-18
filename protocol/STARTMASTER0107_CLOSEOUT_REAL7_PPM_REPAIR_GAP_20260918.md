# STARTMASTER0107 — Abschluss-/Nachholprüfung 2026-09-18 — REAL7 PPM-/Repair-Lücke

Dieses Dokument ist **Historie/Nachweis**, keine CURRENT- oder NEXT-ACTION-Wahrheit.

## 1. Frisch geprüfte Autoritäten

- Einstieg: `control/CURRENT_STARTMASTER.json`
- Bürotür/Navigation: `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
- einzige operative Current-Autorität: `control/startmaster0107/CURRENT_STATE.json`
- aktueller Main vor dieser Nachholung: `226a31f88a4f418f0b33f85800e634af1148d48d`
- Dispatcher PR #107 / `codex-chat-launcher`: `226a31f88a4f418f0b33f85800e634af1148d48d`
- Zielvertrag: `isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`
- Zielvertrag bleibt unverändert.
- Kein Codex gestartet, kein Publish, keine Fach-/Qualitäts-/Designregel geändert.

## 2. Aktueller beobachteter Realfehler

Der Nutzer stellte aus dem aktuellen Codex-Shell-Lauf für Artikel 0 folgenden PPM-6.7.9-Befund bereit. Der Lauf wurde danach gestoppt; 0/7 Artikel sind abgeschlossen.

Vier sichtbare PPM-Befunde, alle mit `repair_owner=DRAFT_WORKER`:

1. `BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO`
   - Ist: `0.2909090909090909`
   - Soll: höchstens `0.02`
   - Feld: `content.duplicate_sentence_ratio`
   - Aussage: 29,09 % statt maximal 2 % vollständige Satzwiederholung.
2. `BLOCKED_KNOWN_SHORT_CONCLUSION`
   - Ist: `0.09494949494949495`
   - Soll: mindestens `0.1`
   - Feld: `content.conclusion_ratio`
3. `BLOCKED_WAVE2_CONCLUSION_BALANCE`
   - Ist: 94 Wörter / 3 Absätze / Ratio `0.09494949494949495`
   - Soll: mindestens 2 Absätze und Ratio `0.1`
4. `BLOCKED_WAVE2_TABLE_VALUE`
   - Tabelle: 1 Tabelle, 4 Body-Zeilen, 3 Spalten
   - Ist `unique_token_ratio=0.09230769230769231`
   - Soll `unique_token_ratio=0.18`
   - Überschrift: „Hindernisstangen für Pferde: Auswahlkriterien direkt vergleichen“

Wichtig: Diese exakte Vierergruppe ist im aktuell abrufbaren PR-107-Terminalverlauf noch **nicht** als eigener Bot-Terminalkommentar dauerhaft gebunden. Deshalb wird kein Task-/Kommentar-ID-Zusammenhang erfunden. Der Befund wird hier exakt als vom Nutzer aus dem realen Codex-Shell-Lauf bereitgestellte Evidence protokolliert.

## 3. Was NICHT die Ursache ist

Nicht belegt und deshalb ausdrücklich **nicht** als Ursache behaupten:
- „Codex kann keine guten Artikel schreiben.“
- „PPM 6.7.9 ist falsch.“
- „Die Textregeln sind falsch.“
- „Konzept 4A funktioniert grundsätzlich nicht.“

Bereits vorhandene Historie belegt, dass Codex/4A echte Artikelstrecken erfolgreich durchlaufen können. Der Zielvertrag hält die bestehende Textmaschine und die fachlichen Regeln ausdrücklich unverändert.

## 4. Tatsächlich gefundene Testlücke

Die bisher als „Repair vollständig bewiesen“ behandelten Tests beweisen vor allem **Routing und Recheck**, nicht die reale Erzeugung einer erfolgreichen Reparatur durch Codex.

### `test_textmachine_repair_roundtrip_matrix.py`
- erzeugt `RepairRequired` per Mock;
- prüft, ob der richtige Owner gewählt und derselbe Artikel gebunden bleibt;
- der anschließende PASS wird ebenfalls mit gemocktem `production_checks.run_all(... PASS ...)` geprüft;
- damit ist der Rückweg bewiesen, nicht die reale Textreparatur durch Codex.

### `real_known_regression_acceptance_v3.py`
- läuft durch echte Validatoren;
- der fehlerhafte Text ist aber eine vorbereitete Fixture;
- die „Reparatur“ erfolgt durch Übergabe der bereits vorbereiteten Datei `files['final']` an `controller.py repair`;
- Codex erzeugt diese Reparatur nicht.

### `full_local_acceptance.py`
- derselbe Grundsatz: vorbereiteter fehlerhafter Text -> vorbereitete `final`-Fixture -> echter Recheck;
- der Report setzt ausdrücklich `codex_used=false`.

Daraus folgt präzise:
**Bewiesen war: Prüfer erkennt Fehler -> System routet zum richtigen Owner -> eine bereits korrekt reparierte Datei kann übernommen und erneut real geprüft werden.**
Nicht bewiesen war:
**Codex erhält einen realen komplexen PPM-Befund mit mehreren gleichzeitigen DRAFT_WORKER-Fehlern und erzeugt daraus selbst zuverlässig eine Reparatur, die den erneuten Fullcheck besteht.**

Das ist das Versäumnis in der bisherigen Abnahmebewertung.

## 5. Repair-Guard als zusätzlicher Risikopunkt

`content_guard.validate_repair_continuity()` begrenzt einen normalen Repair auf:
- maximale Längenänderung 30 %;
- Mindestähnlichkeit 72 %.

Das ist ein echter vorhandener Schutz gegen breite Neuschreibung.

Bei einem Text mit 29,09 % doppelten Sätzen kann eine ausreichend starke Bereinigung möglicherweise eine größere Umarbeitung verlangen. **Nicht bewiesen** ist jedoch, dass genau dieser Guard im aktuellen Lauf ausgelöst hat. Ohne den exakten Vorher-/Nachher-Artikel darf das nicht als Root Cause behauptet werden.

## 6. Was für die exakte Root-Cause noch fehlt

Für eine lückenlose Ursachenbestimmung fehlen dauerhaft gebundene Bytes/States dieses konkreten Artikels:
- Draft **vor** dem ersten Repair;
- PPM-Findings dazu;
- Draft **nach** jedem Repair;
- zugehöriger State/Revision/SHA;
- terminaler PPM-/LT-Befund je Revision.

Ohne diese Daten kann nicht belastbar entschieden werden, ob:
1. die 29,09 % Satzwiederholung bereits im ersten Codex-Draft enthalten war;
2. sie durch eine Reparatur entstanden/verstärkt wurde;
3. der Repair-Guard eine nötige Korrektur verhindert hat;
4. der Worker die Findings unvollständig/falsch umgesetzt hat.

Jede dieser vier Ursachenbehauptungen ohne diese Bytes wäre Raten.

## 7. Zielvertrag

Ziel unverändert:
`Chat -> gebundene Inputs/Point-0 -> Codex Research/Facts/Context/Draft -> echtes LT 6.8 -> echter PPM 6.7.9 -> Same-Article-Repair -> 1..N Batch -> 107008 -> ENDSTEMPEL -> WordPress-Importformat -> bytegleiche finale Datei im Parent-Chat`.

Unverändert:
- Textmaschine/PPM/LT/Design nicht lockern;
- kein Worker/Chat darf PASS selbst behaupten;
- kein Publish;
- keine Wiederverwendung historischer Artikel;
- jeder zukünftige Artikel muss real PASSen.

## 8. Was erledigt ist

- Startweg/Point-0/Root/Worker-Dispatch technisch bewiesen.
- Hash-/Source-/NEW-Bindungen vorhanden.
- echte LT-/PPM-Prüfer eingebunden.
- Repair-Owner-Klassifikation und Routing vorhanden.
- 1..N/Batch/Handoff/ENDSTEMPEL-/WordPress-Strecke technisch getestet.
- der aktuelle PPM-Fehler ist fail-closed erkannt; Artikel 1 wurde nicht freigegeben.
- der falsche Schluss „grüne Repair-Tests = reale Codex-Repairfähigkeit bewiesen“ ist hier korrigiert.

## 9. Was noch erledigt werden muss

**Genau eine fachliche Lücke vor jedem neuen Produktionsbatch: reale Codex-Repair-Parität beweisen.**

Dazu:
1. keinen neuen 7er-Lauf starten;
2. vor jeder Änderung zuerst exakten fehlerhaften Artikelzustand + Revisionen sichern;
3. beweisen, ob Fehler schon im Erst-Draft oder erst nach Repair entsteht;
4. Test-/Proof-Layer so korrigieren, dass ein vorbereiteter `final`-Fixture nicht mehr als Beweis einer realen Codex-Reparatur gilt;
5. Produktionstechnik, PPM/LT, Qualitätsgrenzen und Design dabei nicht verändern;
6. erst danach mit **neuer ausdrücklicher Nutzerfreigabe** genau einen realen Codex-Artikel als Repair-Abnahme laufen lassen;
7. erst nach echtem Artikel-PASS wieder Mehrfachbatch erwägen.

## 10. Optimierung / Wiederholschutz

Vor einem künftigen Codex-Mehrfachlauf muss ein maschinenlesbarer Preflight unterscheiden:
- `REPAIR_ROUTING_PROVEN`
- `REAL_CODEX_REPAIR_PROVEN`

Ein grüner Routing-/Fixture-Test darf nie wieder automatisch als `REAL_CODEX_REPAIR_PROVEN` gewertet werden.

Zusätzlich muss jeder echte Repairlauf Vorher-/Nachher-SHA, Findings, Revision und finalen Checkerstatus dauerhaft erfassbar machen, damit ein temporärer Workspace-Verlust die Ursachenanalyse nicht erneut zerstört.

## 11. Exakter Einstieg nächster Chat

`control/CURRENT_STARTMASTER.json`
-> `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
-> `control/startmaster0107/CURRENT_STATE.json`
-> Frischecheck gegen aktuellen Main und PR #107.

Dann ausschließlich die dortige `next_action`.

**Kein Codex ohne neue ausdrückliche Nutzerfreigabe. Kein 7er-Restart. Keine Änderung von PPM/LT/Textqualität/Design, bevor die Repair-Ursache bewiesen ist.**
