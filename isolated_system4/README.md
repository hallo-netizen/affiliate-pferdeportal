# SYSTEM 4 — TRUE SINGLE ROOM

Status: **LOKALER PUNKT-0/SUPERVISOR-KANDIDAT VOLLSTÄNDIG GETESTET — PRODUKTION BLOCKED BIS BYTEGLEICHE REMOTE-ÜBERTRAGUNG + REMOTE-RETEST.**

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand bleibt getrennt und ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Aktueller Remote-Stand

PR #238, Branch `hobbyroom/system4-true-single-room-v1`.

Kein Merge. Kein Publish. `publish_allowed=false`.

Der Remote-Branch enthält weiterhin den zuvor grünen Teststufe-2-Produktionskern. Der am 2026-09-14 lokal vollständig geprüfte neue Punkt-0/Supervisor-Code ist **noch nicht als kompletter Code-Tree remote gebunden**. Die neuen kleinen Kernblobs sowie `root_entry.py` konnten bereits bytegleich als Git-Objekte erzeugt werden; sie wurden bewusst **noch nicht** an den Branch gehängt. Verbleibender Transportblocker ist insbesondere der große geänderte `controller.py`-Blob. Der direkte lokale Git-Weg ist ebenfalls nicht verfügbar (`Could not resolve host: github.com`). Deshalb gibt es keine halbfertige Remote-Codeversion.

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
- SHA256: `a1b13bb804c573be5d5c0bf17c9e320c09c87a264a283b0450d4306ed99f02da`;
- `codex_used=false`.

## Remote-Git-Objekte des lokalen Kandidaten

Bereits bytegleich in GitHub als **unreferenzierte Blobs** vorhanden, aber noch nicht an den Branch gehängt:
- `point0_snapshot.py` -> `4dab3cc58da04cf2d5d53f22bc7e837b3cca7c88`;
- `supervisor.py` -> `0afb25204fe8cac1dc24912f638451842a68399b`;
- `root_supervisor_bridge.py` -> `2c9e0ce6e22efee20ceedfef5e3ba37c044eeb2f`;
- `worker_dispatch.py` -> `608627f4d9d1b09758e42fd7ece4690fe9761575`;
- `codex_entry.py` -> `c74044a85e9da6de3e9af6472555306e8f6fb28c`;
- `root_entry.py` -> `b533e8223351ef291be6b624bb803b9f888d5268`.

## HOBBYRAUM / NEXT ACTION

Status: **BLOCKED FÜR PRODUKTION / LOKALER KANDIDAT PASS**.

NEXT ACTION:
1. verbliebene getestete Codebytes, insbesondere `controller.py`, bytegleich als Git-Blobs übertragen;
2. jeden Remote-Git-Blob gegen lokalen `git hash-object` prüfen;
3. erst wenn **alle** Blobs stimmen, einen einzigen atomaren Code-Tree/Commit auf PR #238 setzen;
4. auf exakt diesem finalen Remote-Code-Head die vollständige Positiv-/Negativstrecke erneut ausführen;
5. `Pferde Atelier Immutable Base Hardlock` muss auf genau diesem finalen Code-Head SUCCESS sein;
6. erst danach neuer realer Codex-Artikelversuch.

Kein Merge. Kein Publish. Kein weiterer Codex-Lauf vor diesem Remote-Nachweis.
