# SYSTEM 4A — ISOLIERTER KAPSEL-/AUTORITÄTS-PROTOTYP

STATUS: **TEST ONLY / PRODUKTION BLOCKED / KEIN MERGE / KEIN PUBLISH**

Diese Datei ist die eine aktuelle 4A-Statuswahrheit.

## Zweck

4A ist keine neue Textmaschine. Einziger Unterschied zu System 4 ist die Autoritätsgrenze:

- äußerer Supervisor besitzt Workflow-State, Route, Kontrollbindung und PASS-Verwendung;
- Worker/Codex liefert ausschließlich Fachinhalt;
- System-4-Prüfer, Design-, Qualitäts- und WordPress-Regeln bleiben unverändert;
- FAIL bleibt derselbe Artikel;
- Ausgang bleibt `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` plus Parent-Chat-Readback.

Wenn diese Trennung nur mit neuer Signer-/Token-/Room-/Receipt-/Package-Kaskade möglich wäre, 4A stoppen.

## Letzter vollständig lokal bewiesener Stand vor dem aktuellen Runtime-Rootfix

Historischer sicherer 4A-Stand am Commit `56ace832c78e3683306c44ae187b4c7d0eb46755`:

- Architektur / Eingang / Ausgang / Skalierung: **41/41 PASS**;
- echter lokaler Produktions-Acceptance-Lauf mit LanguageTool 6.8 und PPM 6.7.9: **10/10 PASS**;
- 1 / 3 / 25 / 1000 Artikel, Same-Article-Repair, Cross-UID-Grenze, Parent-Chat-Readback und die damaligen Negativfälle waren lokal grün.

Diese PASS-Zahlen gelten **nicht automatisch** für den danach geänderten Rootfix-Stand. Nach jeder Änderung muss der komplette lokale Workflow neu bewiesen werden.

## Neuer realer Codex-Befund

Ein späterer ausdrücklich freigegebener Ein-Artikel-Codex-Lauf erreichte:

`ROOT_ENTRY_PASS -> PRODUCTION_INGRESS_BOUND -> RESEARCH_REQUEST -> BLOCK`

Blocker:

`WORKER_COMMAND_PATH_NOT_ACCESSIBLE:/root/.pyenv/versions/3.11.12/bin/python3`

Kein LT, kein PPM, kein `ARTICLE_PASS`, kein Batch und keine Enddatei wurden erreicht.

### Rootcause

Das frühere Worker-Staging löste nur den privaten Worker-Dateipfad. `from_python_bundle()` übernahm weiterhin `sys.executable` des Supervisors. Im realen Codex zeigte dieses auf ein privates `/root/.pyenv/.../python3`, das für den Cross-UID-Worker `nobody` nicht ausführbar war.

Zusätzlich erbte der Worker bisher den Supervisor-`PATH`; damit bestand dieselbe versteckte Umweltkopplung auch dort.

Das war eine Testlücke: Der frühere positive lokale Runtime-Test verwendete ebenfalls das lokal zugängliche `sys.executable` und reproduzierte deshalb keinen privaten Interpreter bei gleichzeitig zugänglichem Worker.

## Aktueller KISS-Rootfix

Der Cross-UID-Worker übernimmt jetzt **weder `sys.executable` noch den Supervisor-`PATH`**.

Eine kleine gemeinsame Runtime-Grenze gilt:

1. Supervisor-Werkzeuge werden nur aus einem festen Systempfad aufgelöst;
2. Worker-Python wird nur aus `/usr/local/bin:/usr/bin:/bin` gewählt;
3. der gefundene Interpreter wird vor Verwendung real als Ziel-UID gestartet und auf minimale Python-Lauffähigkeit geprüft;
4. kein zugänglicher System-Interpreter = `WORKER_PYTHON_RUNTIME_UNAVAILABLE` und harter BLOCK;
5. Cross-UID-Worker erhalten einen festen sauberen Worker-`PATH` statt des Supervisor-`PATH`;
6. bestehende Pfad-Preflights, Worker-Staging, Authority-Isolation und `stderr`/Exit-Code-Behandlung bleiben bestehen.

Betroffene Implementierung:

- `isolated_system4a/external_host.py`

Neue/verschärfte Regressionen:

- privater Workerpfad bleibt BLOCK;
- **privater Interpreter + zugänglicher Worker** bleibt BLOCK;
- zugänglicher System-Interpreter + zugänglicher Worker läuft positiv;
- Supervisor-`PATH` mit `/root/.pyenv/...` darf nicht in den Worker gelangen;
- kein zugänglicher System-Interpreter = fail-closed;
- echter Worker-Absturz liefert weiterhin Exit-Code + `stderr`.

## Lokale Beweislage des aktuellen Rootfixes

Im aktuellen lokalen Root-/`runuser`-Testcontainer wurden gezielt ausgeführt:

- System-Python für `nobody` aufgelöst: `/usr/bin/python3.13`;
- Cross-UID-Ausführung mit diesem Interpreter: **PASS**;
- privater Interpreter unter `0700`: **NEGATIV PASS / korrekt geblockt**;
- kein zugänglicher Runtimepfad: **NEGATIV PASS / korrekt geblockt**;
- Supervisor-PATH-Leck: **NEGATIV PASS / kein Leak**;
- privates Supervisor-Python wird durch den Worker-Start nicht übernommen: **PASS**.

### Noch NICHT neu bewiesen

Der komplette geänderte 4A-Stand wurde nach diesem Rootfix **noch nicht** erneut als Gesamtworkflow abgenommen.

Grund im aktuellen lokalen Ausführungscontainer:

- GitHub-Checkout ist wegen DNS-Auflösung nicht möglich;
- die echten LanguageTool-6.8- und PPM-6.7.9-Binärabhängigkeiten sind dort nicht vorhanden.

Daher aktuell ausdrücklich **kein** neues `41/41 PASS` und **kein** neues `10/10 PASS` für den Rootfix-Stand.

## Andere Felder derselben Fehlerklasse

Bei der Prüfung wurde außerdem gefunden:

- `os_boundary_acceptance.py` verwendet im Cross-UID-Test noch das Supervisor-`sys.executable`;
- dies ist Testcode, aber dieselbe Umweltkopplung und muss vor einer neuen Gesamtfreigabe ebenfalls auf die gemeinsame Cross-UID-Runtime-Regel umgestellt und mitgetestet werden.

Same-UID-/Managed-Agent-Wege sowie Fach-, Design-, LT-, PPM-, Batch-, WordPress- und Handoff-Regeln wurden durch den Rootfix nicht fachlich verändert.

## Codex-Regel

**Kein Codex-Lauf ohne ausdrückliche vorherige Freigabe des Users.**

Aktuell:

`REAL_CODEX_4A_RETEST = NOT AUTHORIZED`

## NEXT ACTION

Nur lokal:

1. gleiche Runtime-Regel auch im Cross-UID-Pfad von `os_boundary_acceptance.py` verwenden;
2. aktuellen Branch vollständig lokal verfügbar machen;
3. alle 4A-Tests mit Positiv- und Negativfällen neu ausführen;
4. echten vollständigen LT-/PPM-Produktions-Acceptance-Lauf neu ausführen;
5. gesamte Kette `Fachinput -> Ingress -> Cross-UID Worker -> Research -> Facts -> Context -> Draft -> LT -> Same-Article-Repair -> PPM -> Batch -> V2 -> Parent-Chat` beweisen;
6. erst bei vollständigem PASS den Rootfix als lokal abgenommen markieren.

Bis dahin: **BLOCKED / kein Codex / kein Merge / kein Publish**.

## Abbruchregel

Wenn System 4 State/Route/PASS ebenfalls technisch aus der Worker-Autorität entfernt, verliert 4A seinen einzigen strukturellen Vorteil und wird als eigenes Konzept beendet.
