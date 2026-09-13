# SYSTEM 4A — AKTUELLER LOKALER TESTNACHWEIS 2026-09-13

Belegdatei, keine zweite CURRENT_STATE.

## Vergleichsbasis

System 4 PR #238 Head: `89b2e8eeb928f744e8814b2c79966672db2e308a`.

Seit dem vorherigen Prüferstand `edfe6049768db68f85bf3babedce3199538217ef` wurden in System 4 nur zusätzliche Transportdateien ergänzt; der im Realtest ausgeführte Fach-/Design-/LT-/PPM-Prüfercode blieb unverändert.

4A verändert ausschließlich `isolated_system4a/**`.

## Lokale Architektur-/Grenztests

Frischer Sammellauf mit Warnings als Fehler:

**41/41 PASS**.

Abgedeckt sind u. a.:

- kompletter Einstieg bis Parent-Chat-Datei;
- Same-Article-Repair;
- 1 / 3 / 25 / 1000 Artikel;
- neue/gemischte Beitragsarten;
- Managed-Session- und Cross-UID-Grenze;
- Worker-State-/PASS-/Manifest-/Publish-Injektion BLOCK;
- Research/Facts/Context/Design/Checker/Repair/Batch BLOCK;
- JSON-/Inline-Tamper BLOCK;
- privates `0700 root`-Worker-Quellverzeichnis;
- Supervisor-Staging dieses privaten Bundles;
- Authority-Dateien/Symlinks im Worker-Bundle BLOCK;
- echter Worker-Crash liefert Exit-Code + stderr.

## Echter lokaler Produktions-Acceptance-Lauf

Gebundene reale Abhängigkeiten:

- LanguageTool 6.8 JAR SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`;
- PPM 6.7.9 Paket SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`;
- `mocks_used=false`.

Produktionslauf nach Worker-Staging-Härtung:

**10/10 PASS**.

Positiv:

`Fachinput -> Supervisor-Ingress -> privates 0700-Worker-Bundle -> Supervisor-Staging -> Cross-UID-Worker -> Research -> Facts -> Context -> Draft -> real LT -> Same-Article-Repair -> real LT PASS -> real PPM PASS -> Batch -> V2 -> Parent-Chat byteidentisch`

Negativ korrekt geblockt:

1. Same-UID-Produktion;
2. externes Kontrollmanifest;
3. direkter ungestagter Cross-UID-Worker unter privatem Pfad;
4. PASS-/Phase-Injektion;
5. Fake-`state.json`;
6. Research-Fail;
7. Facts-Fail;
8. Design-Fail;
9. Parent-Chat-Payload-Tamper.

Finaler positiver Handoff:

- **66.753 Byte**;
- SHA256 `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`;
- Revision **2**;
- `publish_allowed=false`.

## Freigegebener Codex-Probelauf und lokale Root-Cause

Einmaliger freigegebener Codex-Probelauf:

- Titel: `Pferdeanhänger im Herbst sicher vorbereiten`;
- Root Entry: PASS;
- Production Ingress: PASS;
- Blocker bei erstem Research-Request: `WORKER_EXITED_WITHOUT_RESPONSE`;
- kein Handoff, kein Publish, kein zweiter Versuch.

Lokale Reproduktion:

- Ursache: Worker-Skript lag unter einem `0700 root`-Tempverzeichnis und war für `nobody` nicht zugänglich;
- zusätzlich wurde Worker-stderr vom damaligen Host verworfen.

Lokale Korrektur:

- Cross-UID-Pfadprüfung vor Workerstart;
- Exit-Code + stderr bei Workerabbruch;
- Supervisor-eigenes Staging eines privaten Worker-Bundles in einen kontrollierten read-only Bereich;
- `state.json`, `authority.key`, `AGENTS.md`, `.git` und Symlinks im Bundle verboten;
- Cleanup des Supervisor-Stagingbereichs nach Lauf.

Diese Korrektur ist im vollständigen 41/41- und 10/10-Lauf enthalten.

## Beweisgrenze

Lokal real bewiesen:

- Workflow-/State-Autorität außerhalb des Cross-UID-Workers;
- echte System-4-Prüfer unverändert über 4A;
- echter LT-/PPM-Weg inklusive Same-Article-Repair;
- V2-/Parent-Chat-Ausgang byteidentisch;
- realistisches privates Worker-Staging funktioniert positiv und negativ.

Noch offen:

- erneuter operativer Codex-/Managed-Agent-Probelauf auf der korrigierten Grenze.

Dieser Lauf ist **nicht autorisiert**, solange der User ihn nicht ausdrücklich freigibt.

Kein Merge, kein Publish.
