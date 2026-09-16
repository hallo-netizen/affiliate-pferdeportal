# PROTOKOLL-NACHHOLUNG — SYSTEM 4A ACCEPTANCE — 2026-09-16

Status dieses Dokuments: **historische Ausführungs- und Entscheidungs-Evidence**.

Dieses Dokument ist **keine CURRENT_STATE**, kein Zielvertrag, keine Bürotür und keine eigene dynamische NEXT-ACTION-Wahrheit. Der aktuelle operative Stand ist immer frisch aus dem tatsächlich aktuellen Branch/Head, den dazugehörigen echten Workflow-Läufen und — sobald autorisiert synchronisiert — der zuständigen Campus-CURRENT_STATE zu bestimmen.

## Arbeitsbindung

- Repository: `hallo-netizen/affiliate-pferdeportal`
- Arbeitsbranch: `hobbyroom/system4a-startgate-test-20260914`
- Ausgangshead der Nachholarbeit: `bffc891870a81bc872d21bc198944969a79eb812`
- Ausgangslage: Exact Head Bundle und Repair Owner Contract grün; Real LT68 PPM679 Acceptance rot.
- Zielvertrag unverändert: `isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`
- Textmaschine, PPM 6.7.9, Designvertrag und fachliche Prüfschwellen wurden in dieser Nachholarbeit **nicht gelockert**.

## Tatsächlich ausgeführte Reparaturen und Befunde

### 1. Repair-Continuity — veralteter Import

Der reale Diagnoseweg zeigte zuerst:

`ModuleNotFoundError: No module named 'live_parity'`

Ursache: `test_repair_continuity.py` importierte eine nicht vorhandene alte Schnittstelle, während der aktuelle gebundene Testweg `live_parity_v2.py` ist.

Änderung: Testimport auf `live_parity_v2 as live_parity` gebunden.

WARUM: Nur die aktuelle reale Parity-Schnittstelle darf Testautorität sein; kein Alias auf eine nicht existente alte Teststrecke.

### 2. Authoring Contract — Heading-Distance 27:28

Nach dem Import-Fix erreichte der Repair-Test den Authoring Contract und blockierte mit:

`ARTICLE_AUTHORING_CONTRACT_FAIL:PREWRITE_HEADING_DISTANCE:27:28`

Die Mindestschwelle 28 war korrekt. Die zuvor erfolgte LT-saubere Kürzung der deterministischen Testworker-Tails hatte einzelne Abstände um etwa ein Wort verkürzt.

Änderung: Die deterministischen LT-sauberen Tails wurden wieder ausreichend lang formuliert.

WARUM: Der bestehende 28-Wort-Vertrag bleibt unverändert; die Testausgabe muss den Vertrag erfüllen, nicht der Vertrag an die Testausgabe angepasst werden.

### 3. Repair-Continuity — veraltete Testannahmen

Nach Erreichen des eigentlichen Repair-Pfads waren drei Annahmen veraltet:

- Positivtests suchten frühere Tail-Sätze.
- Der Design-Negativtest veränderte nur eine HTML-Klasse; die Same-Article-Continuity prüft zunächst den sichtbaren Text und erkannte deshalb noch keine fachliche Reparatur.

Änderung:

- `_minor_repair` auf die aktuellen deterministischen Sätze gebunden.
- Design-Negativtest ergänzt zusätzlich eine kleine sichtbare Same-Article-Reparatur, damit anschließend tatsächlich der Design-Guard geprüft wird.

WARUM: Der Negativtest muss die beabsichtigte Schranke erreichen und darf nicht vorher an einer anderen korrekten Schranke hängen bleiben.

Ergebnis auf späterem Acceptance-Lauf: Repair-Schritte 23–28 PASS.

### 4. Batch-Handoff 1..N — Test-Fixture-Schuld nach Authoring-Contract-Hardening

Der nächste reale Fehler lag in `Textmaschine matrix — batch handoff one-to-N`.

Exakte Ursache: Der historische Commit `e342a9a1df6889b9db349c3b302cf6174066869e` hatte im Batch-Gate die verpflichtende Revalidierung durch `authoring_contract.validate_bound(...)` ergänzt. Die alten Batch-Test-Fixtures enthielten jedoch keinen gebundenen Authoring Contract und starben deshalb vor ihren eigentlichen Positiv-/Negativprüfungen.

Änderung:

- `test_batch_gate.py` und `test_universal_batch_gate.py` erzeugen den Authoring Contract jetzt mit dem echten `authoring_contract.build()`.
- Die Fixtures lesen die echten statischen PPM-6.7.9-Regeln.
- Das Batch-Gate selbst wurde **nicht** gelockert oder umgangen.
- Ein Negativtest für fehlenden Authoring Contract wurde ergänzt.

WARUM: Die neue Sicherheitsprüfung gehört zum realen Gate und muss in den Tests erhalten bleiben. Testdaten müssen dem aktuellen realen Vertragsstand folgen.

Ergebnis:

- Diagnose-Run `35080032743`: PASS.
- Kanonischer Real-Acceptance-Lauf `35080032773`: Schritt 29 `Textmaschine matrix — batch handoff one-to-N` PASS.

### 5. Aktueller erster realer Acceptance-Blocker — 1-Artikel-Live-Parity

Im kanonischen Run `35080032773` auf Head `493d1395cbffc2616df2f5fac206419c621d4677` waren die Schritte 1–30 erfolgreich. Der erste rote Schritt war:

`31 — Run complete one article route`

Zur Ursachenfeststellung wurde ein temporärer Diagnoseworkflow auf Head `61927bb6f49d3a03bd07c3b4098b10d0f57d31fe` exakt an denselben 1-Artikel-Weg, denselben Fresh-Run-Token-Mechanismus und dieselben LT-6.8-Hashes gebunden.

Diagnose-Run: `35080766923`.

Exakter Befund:

- LanguageTool 6.8 meldet im frischen Testartikel dreimal `GERMAN_SPELLER_RULE` für die Formulierung `Gummidichtungen`.
- Repair-Owner ist korrekt `DRAFT_WORKER`.
- Der deterministische Testworker erzeugt im `repair`-Aufruf für diesen LT-Befund jedoch denselben Draft erneut.
- Der Controller blockiert deshalb korrekt mit:

`REPAIR_DRAFT_UNCHANGED`

WARUM dieses Verhalten aktuell BLOCKED bleibt: Die Same-Article-/Unchanged-Schranke ist korrekt und darf nicht gelockert werden. Zu reparieren ist ausschließlich die deterministische Testworker-/Fixture-Seite für den konkret gebundenen LT-Befund; bis ein neuer echter Run die Änderung beweist, bleibt Real Acceptance rot.

### 6. Zielvertrags-Wegweiser korrigiert

`CODEX_LIVE_TASK.md` ist ausdrücklich historisch. Seine Liste „Aktuell verbindlich“ zeigte trotzdem noch auf den älteren Zielvertrag vom 13.09.

Änderung: Wegweiser auf den ausdrücklich aktuellen Zielvertrag `ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md` korrigiert.

WARUM: Keine widersprüchliche Pflichtlektüre; der historische Wegweiser darf keinen abgelösten Zielvertrag als aktuell ausgeben.

## Campus-/CURRENT_STATE-Befund

Die offizielle Bürotür auf `main` führt eindeutig:

`control/CURRENT_STARTMASTER.json`
→ `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
→ `control/startmaster0107/CURRENT_STATE.json`

Die dortige CURRENT_STATE bildet den aktiven System-4A-Branch/Head/Teststand nicht ab und enthält weiterhin den älteren 107007-/PPM679-Stand sowie einen anderen Hobbyraum.

Die CURRENT_STATE legt `state_write_authority = ENTRANCE_GATE_ONLY` fest. Der autoritative Gate-Code `control/deterministic-entrance-gate/door.py` erlaubt State-Fortschreibung ausschließlich nach einem PASS-Receipt entlang einer bereits vorgebundenen monotonen `next_binding`. Worker-Receipts dürfen weder Navigation entscheiden noch State-Schreiben anfordern.

Entscheidung: **Keine direkte Chat-/Branch-Umschreibung der Campus-CURRENT_STATE und keine zweite CURRENT_STATE anlegen.** Die Campus-Synchronisation bleibt BLOCKED, bis ein autorisierter Entrance-Gate-/State-Owner-Weg den System-4A-Stand bindet.

## Nicht verändert

- kein Plugin entwickelt oder aktualisiert;
- keine Plugin-Ausgabekopie erzeugt;
- keine Textmaschinenregel gelockert;
- keine PPM-6.7.9-Regel geändert;
- kein Designvertrag geändert;
- kein zweiter Zielvertrag angelegt;
- keine zweite CURRENT_STATE angelegt;
- keine Bürotür mit dynamischer Branch-/Head-/Run-Wahrheit angereichert;
- kein Publish und kein Merge freigegeben.

## Prüfstatus dieser Nachholung

- Dokumentation der tatsächlich ausgeführten Reparaturen/Befunde: nachgeholt.
- WAS/WARUM für dauerhafte Änderungen: nachgeholt.
- Aktueller System-4A-Gesamt-PASS: **nicht erteilt**.
- Real Acceptance: **BLOCKED** am exakt diagnostizierten 1-Artikel-Repair-Fall `REPAIR_DRAFT_UNCHANGED` nach realem LT-Finding.
- Campus-CURRENT_STATE-Synchronisation: **BLOCKED** durch fehlende vorgebundene State-Owner-/Entrance-Gate-Bindung für diesen System-4A-Arbeitsstand.
- Parent-Chat-Endnachweis: nicht erreicht; gemäß `PROTOKOLL_TESTSTRECKE_V2_20260914.md` entsteht kein Gesamt-PASS allein aus einem Remote-Run.
