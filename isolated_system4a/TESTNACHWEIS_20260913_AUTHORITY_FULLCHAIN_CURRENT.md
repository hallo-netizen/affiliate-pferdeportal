# SYSTEM 4A — TESTNACHWEIS 2026-09-13

Belegdatei, keine zweite CURRENT_STATE. **Aktueller Status steht ausschließlich in `README.md`.**

## Letzter vollständiger lokaler Beweis vor dem aktuellen Runtime-Rootfix

Am Stand `56ace832c78e3683306c44ae187b4c7d0eb46755` waren lokal bewiesen:

- Architektur-/Grenztests: **41/41 PASS**;
- echter Produktions-Acceptance-Lauf mit LanguageTool 6.8 und PPM 6.7.9: **10/10 PASS**;
- Same-Article-Repair, 1 / 3 / 25 / 1000 Artikel, Cross-UID-Grenze und Parent-Chat-Readback.

Gebundene reale Abhängigkeiten dieses historischen Volltests:

- LanguageTool 6.8 JAR SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`;
- PPM 6.7.9 Paket SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`;
- `mocks_used=false`.

Historischer positiver Pfad:

`Fachinput -> Supervisor-Ingress -> privates 0700-Worker-Bundle -> Supervisor-Staging -> Cross-UID-Worker -> Research -> Facts -> Context -> Draft -> real LT -> Same-Article-Repair -> real LT PASS -> real PPM PASS -> Batch -> V2 -> Parent-Chat byteidentisch`

Historischer positiver Handoff:

- 66.753 Byte;
- SHA256 `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`;
- Revision 2;
- `publish_allowed=false`.

## Danach gefundener realer Runtime-Fehler

Ein späterer freigegebener Codex-Lauf erreichte:

`ROOT_ENTRY_PASS -> PRODUCTION_INGRESS_BOUND -> RESEARCH_REQUEST -> BLOCK`

Blocker:

`WORKER_COMMAND_PATH_NOT_ACCESSIBLE:/root/.pyenv/versions/3.11.12/bin/python3`

Damit war bewiesen, dass der frühere 41/41-/10/10-Test die reale private Interpretergrenze nicht abdeckte.

Rootcause:

- Worker-Bundle war korrekt gestaged;
- `from_python_bundle()` übernahm aber weiterhin das Supervisor-`sys.executable`;
- im echten Codex lag dieses unter privatem `/root/.pyenv/...`;
- zusätzlich erbte der Worker den Supervisor-`PATH`.

## Aktueller Rootfix

Der aktuelle 4A-Stand trennt nun auch die Runtime-Umwelt:

- kein Supervisor-`sys.executable` für Cross-UID-Worker;
- kein geerbter Supervisor-`PATH` für Cross-UID-Worker;
- Worker-Python nur aus festem Systempfad;
- echter Start-Probeversuch als Ziel-UID vor Verwendung;
- kein brauchbarer System-Interpreter = harter `WORKER_PYTHON_RUNTIME_UNAVAILABLE`-BLOCK;
- `runuser` ebenfalls aus festem Supervisor-Systempfad aufgelöst.

Neue Regressionen decken insbesondere ab:

- privater Interpreter + zugänglicher Worker -> BLOCK;
- zugänglicher System-Interpreter + zugänglicher Worker -> PASS;
- Supervisor-PATH mit `/root/.pyenv` -> kein Worker-PATH-Leak;
- kein zugänglicher System-Python -> BLOCK;
- privater Workerpfad -> weiterhin BLOCK;
- Worker-Crash -> weiterhin Exit-Code + stderr.

## Aktuell lokal tatsächlich ausgeführt

Gezielter Root-/Cross-UID-Harness im aktuellen lokalen Testcontainer:

- System-Python `/usr/bin/python3.13` als `nobody` startfähig -> **PASS**;
- privater Interpreter unter `0700` -> **NEGATIV PASS / geblockt**;
- kein System-Runtimepfad -> **NEGATIV PASS / geblockt**;
- privates Supervisor-Python wird nicht übernommen -> **PASS**;
- Supervisor-PATH wird nicht in den Worker übernommen -> **PASS**.

## Noch nicht neu ausgeführt

Nach dem Rootfix wurden **noch nicht** erneut ausgeführt:

- vollständiger 4A-Sammellauf;
- echter kompletter LanguageTool-/PPM-Produktions-Acceptance-Lauf;
- erneuter Codex-Lauf.

Der aktuelle lokale Ausführungscontainer kann den Branch wegen DNS nicht auschecken und enthält die gebundenen LT-/PPM-Binärabhängigkeiten nicht. Deshalb werden die historischen 41/41 und 10/10 ausdrücklich **nicht** auf den neuen Rootfix-Stand übertragen.

Zusätzlich ist vor einer neuen Gesamtfreigabe dieselbe `sys.executable`-Kopplung in den Cross-UID-Testhilfen (`os_boundary_acceptance.py` sowie der alte Workerpfad-Negativfall im Produktions-Acceptance-Test) zu bereinigen, damit die Tests Ursache und Symptom sauber trennen.

**Aktuell: BLOCKED / kein Merge / kein Publish / kein Codex ohne ausdrückliche User-Freigabe.**
