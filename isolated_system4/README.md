# SYSTEM 4 — TRUE SINGLE ROOM

Status: **LOKALER PUNKT-0/SUPERVISOR-KANDIDAT VOLLSTÄNDIG GETESTET — PRODUKTION BLOCKED BIS BYTEGLEICHE REMOTE-ÜBERTRAGUNG + HARDLOCK.**

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand bleibt getrennt und ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Aktueller Remote-Stand

PR #238, Branch `hobbyroom/system4-true-single-room-v1`.

Kein Merge. Kein Publish. `publish_allowed=false`.

Der Remote-Branch enthält weiterhin den zuvor grünen Teststufe-2-Produktionskern. Der am 2026-09-14 lokal vollständig geprüfte neue Punkt-0/Supervisor-Code ist **noch nicht bytegleich remote gebunden**. Ein Versuch, den großen `root_entry.py`-Blob zu transportieren, ergab einen anderen Git-Blob als lokal; deshalb wurde der Branch bewusst nicht auf einen halbfertigen Code-Tree gesetzt.

## Neuer realer Fehler und Architekturfolge

Der ausdrücklich freigegebene reale Ein-Artikel-Codex-Lauf blockierte bereits in `ARTICLE_RESEARCH` mit:

`SYSTEM4_HARD_BLOCKER:REAL_WEB_RESEARCH_RUNTIME_UNAVAILABLE`

Ursache: `HTTP 401 Unauthorized` aus der Codex-Web-Research-Runtime. LT, PPM, Batch und Handoff wurden in diesem Lauf korrekt nicht erreicht.

Daraus folgt die neue verbindliche Zielarchitektur:

`Maschine erzeugt Punkt-0 -> Maschine beschafft/verifiziert Quellen -> Root bindet -> Supervisor besitzt den Lauf -> Worker-Dispatch -> Facts -> Context -> Codex schreibt/repariert -> LT -> PPM -> Batch -> Handoff`

Codex darf keine freie Websuche mehr besitzen. `controller research` akzeptiert ausschließlich Evidence aus dem hashgebundenen Punkt-0-Research-Pool.

Verbindlicher Zielvertrag:
`ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`

## Lokaler exakt getesteter Kandidat

- lokaler Git-Head: `cd6c134a3ee27f4535ea91bfe6cc223a34c9eb25`
- Root-Manifest: `98b4c1f3bad0334b8a89d5594a8282734c4b01fb907e92e239ee036601c8e457`
- PPM 6.7.9 SHA256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
- LanguageTool 6.8 SHA256: `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`

### Neue/historische Negativmatrix

Auf genau diesem lokalen Kandidaten tatsächlich ausgeführt:
- Punkt-0 / Root / Supervisor / Dispatch: **19/19 PASS**;
- historische Context-/Draft-Fehlerklassen: **16/16 PASS**;
- Route / Batch / Handoff: **5/5 PASS**;
- Gesamt gezielte Matrix: **40/40 PASS**.

Unter anderem fail-closed bewiesen: HTTP 401, falscher Source-Hash, leerer Source-Pool, Point-0-/Receipt-/Snapshot-/Research-Pool-Tamper, Head-/Manifest-Mismatch, Reaktivierung freier Websuche, ungebundene Research-Evidence, unbekannte Fact-ID, Runtime-/Link-/Snapshot-Mismatch, unbekannte Validation-Version, fehlende V5-Requirements, fehlende Fact-Refs/Source-Traces, Batch-State-Tamper, `STATE_ORDER_MISMATCH:0` und Handoff-Manipulation.

### Integrierter Null-bis-Datei-Lauf

Auf demselben Kandidaten:

`Punkt-0 -> Root -> Supervisor -> Worker -> reale gebundene Putzbox-Quellen -> Research -> Facts -> Context -> Draft -> Same-Article-Repair -> echtes LT 6.8 -> echter PPM 6.7.9 -> Batch -> V2-Handoff -> Inline-Unpack`

Ergebnis: **PASS**.

Im produktionsnahen Lauf wurden zwei normale Repair-Befunde korrekt am selben Artikel behoben: LanguageTool-Finding `Hardcase-Putzbox`, danach PPM-Fazitanteil `9,476 % < 10 %`; Revision 3 anschließend FULL PASS.

### Frischer kompletter Artikel OHNE CODEX

Zusätzlich auf frischem Workspace vollständig ausgeführt:
- Artikel: `Putzbox für Pferde richtig auswählen`;
- neuer Punkt-0 aus gebundenem Live-Input + 6 realen Research-Snapshots;
- Root/Supervisor/Worker-Start PASS;
- Research/Facts/Context/Draft PASS;
- LT 6.8 PASS;
- PPM 6.7.9 PASS;
- Batch 1/1 PASS;
- V2-Handoff / Inline-Unpack bytegleich PASS;
- Handoff: `49.294` Bytes;
- SHA256: `a1b13bb804c573be5d5c0bf17c9e320c09c87a264a283b0450d4306ed99f02`;
- `codex_used=false`.

## HOBBYRAUM / NEXT ACTION

Status: **BLOCKED FÜR PRODUKTION / LOKALER KANDIDAT PASS**.

NEXT ACTION:
1. exakt getestete Punkt-0/Supervisor-Codebytes bytegleich auf PR #238 übertragen;
2. jeden Remote-Git-Blob gegen lokalen `git hash-object` prüfen;
3. keine Teilübertragung akzeptieren;
4. auf dem finalen Remote-Head die vollständige Positiv-/Negativstrecke erneut ausführen;
5. `Pferde Atelier Immutable Base Hardlock` muss auf genau diesem finalen Head SUCCESS sein;
6. erst danach neuer realer Codex-Artikelversuch.

Kein Merge. Kein Publish. Kein weiterer Codex-Lauf vor diesem Remote-Nachweis.
