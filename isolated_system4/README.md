# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED — CAUSE-FIX LOKAL VOLLSTÄNDIG BEWIESEN, ABER NOCH NICHT AUF DEM AKTUELLEN PR-HEAD GEBUNDEN.** Isolierter Prototyp / Test only. Kein Merge, kein Publish.

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand bleibt getrennt und ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Aktueller Remote-Stand

PR #238: `System 4 — true single-room article production`

Branch: `hobbyroom/system4-true-single-room-v1`

Der aktuelle Remote-Head nach Abschluss-/Cleanup-Dokumentation ist ein reiner Dokumentations-/Cleanup-Fortschritt auf dem unveränderten System-4-Codebaum; der getestete Cause-Fix ist **noch nicht** auf dem PR gebunden.

Der zuletzt frisch geprüfte Codebaum vor der aktuellen Dokumentationsnachholung ist bytegleich zu:

`edfe6049768db68f85bf3babedce3199538217ef`

Der aktuelle Remote-Live-Input ist weiterhin die ältere 643-Byte-Datei mit:

`system4_root_manifest_sha256 = 3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

Git blob:

`212d062eef9895cf67299f7ae6fcceee760cc2ed`

Die später lokal bewiesenen Cause-Fix-Dateien `authoring_contract.py` und `full_workflow_fault_matrix.py` sind im aktuellen Remote-Code noch nicht gebunden.

## Offizieller Campusstand — getrennt

`control/CURRENT_STARTMASTER.json` bindet weiterhin `STARTMASTER0107`.

Der offizielle Projektstand bleibt `BLOCKED` bei `RUN_NEW_ARTICLE_BATCH_NO_STOP` / Sequenz `107007` mit `PPM679_REAL_EXECUTION_BLOCKED`; `hobbyroom_status=FREI`; `publish_allowed=false`.

System 4 überschreibt diesen Campusstand nicht.

## Letzter reale Artikeltest

Gebundener Artikel:

- Typ `Beratung`
- Kategorie `putzbox-beratung`
- Titel `Putzbox für Pferde richtig auswählen`
- Keyword `Putzbox für Pferde`
- Plan-Slot `88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5`
- `publish_allowed=false`

Der reale Codex-Lauf erreichte:

`Root -> Research -> Facts -> Context -> Draft -> FULL PPM`

PPM 6.7.9 blockierte den Draft mit:

`FULL:ppm679:BLOCKED_CONTENT_WORD_FLOOR`

- Ist: 448 Wörter
- Soll: mindestens 750 Wörter

Die notwendige Verlängerung wurde danach durch den Same-Article-Repair-Guard blockiert:

`REPAIR_SCOPE_FAIL:REPAIR_SCOPE_TOO_LARGE:LENGTH:0.7680`

Damit ist die Ursache klar: **Eine bereits vor dem Schreiben bekannte Pflicht wurde nicht früh genug maschinell an den Autorweg gebunden.**

## Verbindliche Ursachenlösung

Nicht die 30-%-Repair-Grenze wird für Wortzahl aufgeweicht.

Zielweg:

`Ingress -> Research -> Facts -> CONTEXT_REQUIRED -> gebundener Authoring Contract aus unveränderten autoritativen Quellen -> DRAFT_REQUIRED -> Draft -> unveränderte echte Prüfer -> nur echte dynamische Same-Article-Reparatur -> Batch -> Handoff`

Dabei gilt zwingend:

- Textmaschine READ-ONLY;
- PPM 6.7.9 READ-ONLY;
- PSERC/PSTE READ-ONLY;
- LanguageTool 6.8 unverändert;
- Design, Theme/CSS und WordPress-Plugin READ-ONLY;
- kein Chat/Codex/externer Input darf Schreibregeln ergänzen, lockern oder überschreiben;
- bekannte bindbare Prüferpflichten müssen vor Draft-Annahme aus denselben unveränderten Autoritäten gebunden sein;
- neue Drafts und Reparaturen müssen vor Annahme gegen diese bereits bekannten Pflichten laufen;
- ein später auftauchender Fehler, der schon vor Draft bekannt/bindbar war, ist ein Vorab-Gate-/Invarianzfehler und kein normaler Repair-Erfolg.

## Testregel

**Kein Einzeltest zählt als Gesamtworkflow-Beweis.**

Jeder bekannte Workflow-Schritt muss positiv und negativ gegen den vollständigen Root->Datei-Weg geprüft werden.

Auf den lokal getesteten Cause-Fix-Bytes wurde tatsächlich terminal ausgeführt:

- `121/121` Unittests PASS;
- Gesamtworkflow-Matrix `15/15` Stationen positiv und negativ;
- `39` Szenarien;
- kompletter Root->Datei-Acceptance-Lauf `10/10` PASS;
- echtes LanguageTool 6.8;
- echtes PPM 6.7.9;
- `mocks_used=false` für den Produktionsbeweis;
- finale Testdatei: 66753 Bytes;
- SHA256 `f6b08cdede6dedef329ca20dde3b648f77cd6f8b6342ee2407cc3441953a7c75`.

**Beweisgrenze:** Diese PASS-Werte gelten für die getesteten lokalen Cause-Fix-Bytes. Sie sind ausdrücklich **kein PASS des aktuellen Remote-PR-Heads**, solange exakt diese Bytes dort nicht gebunden und erneut auf genau diesem Head geprüft wurden.

## Getesteter Cause-Fix

Gebundener Cause-Fix-Manifestwert:

`8789f0af37183e9988e0b90f9bb5ea2d3e0537c4b43e849d4e34a37fb1a904ff`

Gebundener Cause-Fix-Live-Input:

- 643 Bytes
- SHA256 `9d843b3f77d4c7b4e1c85b59125cbdab5e5ae9277a941516ac2c54368d5f1b15`

Die exakten 13 Ziel-Blob-Hashes und die vollständigen Testbelege stehen im aktuellen Protokoll:

`PROTOKOLL_HANDOVER_20260913_CAUSEFIX_CLOSEOUT.md`

## Codex-Regel

Codex wird **ausschließlich für einen konkreten real gebundenen Artikeltest/-produktionslauf** verwendet und nur nach ausdrücklicher Nutzerfreigabe.

Kein Codex für:

- Diagnose;
- Architektur-/Codearbeit;
- Patch/Commit/Push;
- Preflight;
- lokale Tests;
- Dokumentation;
- Handoff-/WordPress-Experimente.

Ein Codex-Patch-/Push-Auftrag in diesem Chat war ein Regelverstoß und ist als Fehler protokolliert. Er hat den Remote-PR nicht aktualisiert.

## HOBBYRAUM / NEXT ACTION

Status: **BLOCKED**.

Ohne Codex:

1. Exakt die 13 im aktuellen Protokoll gebundenen Cause-Fix-Dateibytes auf `hobbyroom/system4-true-single-room-v1` übertragen.
2. Alle 13 Remote-Git-Blobs exakt gegen die protokollierten Zielhashes prüfen.
3. Cause-Fix-Manifest muss exakt `8789f0af37183e9988e0b90f9bb5ea2d3e0537c4b43e849d4e34a37fb1a904ff` ergeben.
4. Auf dem danach aktuellen Remote-Head ohne Codex terminal ausführen: `121/121`, Matrix `15/15 + 39`, Acceptance `10/10` mit echtem LT 6.8 + PPM 6.7.9.
5. Immutable Base Hardlock auf exakt diesem Head prüfen.
6. Erst danach und nur nach ausdrücklicher Nutzerfreigabe: **genau ein konkreter realer Artikeltest mit Codex**.

Zusätzlicher Cleanup: Der versehentlich erzeugte Branch `tmp-should-not-use` ist auf denselben Stand wie der Arbeitsbranch fast-forward gesetzt und enthält keine abweichende aktuelle Wahrheit. Er muss gelöscht werden, sobald ein Branch-Delete-fähiger Weg verfügbar ist, und darf niemals als Arbeits-/CURRENT-/Produktionsbranch verwendet werden.

Kein Merge. Kein Publish.
