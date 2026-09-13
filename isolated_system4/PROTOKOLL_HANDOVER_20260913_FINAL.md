# PROTOKOLL / ÜBERGABE — SYSTEM 4 — FINAL CLOSEOUT 2026-09-13

Dieses Dokument ist das **aktuelle Abschluss-/Übergabeprotokoll**. Es ist kein CURRENT_STATE. Aktuelle System-4-Statuswahrheit bleibt ausschließlich `isolated_system4/README.md`; offizieller Campus-/Projekt-CURRENT bleibt ausschließlich `control/startmaster0107/CURRENT_STATE.json`.

## AKTUELLER STAND
- PR #238 bleibt isolierter Draft-PR, unmerged, unpublished.
- Der ausführbare Remote-System-4-Codebaum ist nach dem Transport-Cleanup weiterhin bytegleich zu `edfe6049768db68f85bf3babedce3199538217ef`; danach erfolgten ausschließlich Dokumentations-/Wegweiseränderungen.
- Der lokal vollständig getestete Cause-Fix ist **noch nicht auf dem Remote-PR gebunden**.
- Aktueller Remote-Live-Input bleibt die ältere 643-Byte-Datei mit Manifest `3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c` und Git-Blob `212d062eef9895cf67299f7ae6fcceee760cc2ed`.
- `authoring_contract.py` und `full_workflow_fault_matrix.py` gehören zum getesteten Cause-Fix, sind aber im Remote-Code noch nicht gebunden.

## LETZTER SICHERER REALBEFUND
Der reale Ein-Artikel-Codex-Lauf für `Putzbox für Pferde richtig auswählen` erreichte:
`Root -> Research -> Facts -> Context -> Draft -> real PPM 6.7.9`.

PPM blockierte mit `FULL:ppm679:BLOCKED_CONTENT_WORD_FLOOR` bei 448 statt mindestens 750 Wörtern. Die notwendige starke Verlängerung wurde anschließend durch `REPAIR_SCOPE_FAIL:REPAIR_SCOPE_TOO_LARGE:LENGTH:0.7680` blockiert.

Ursache: Eine bereits vor dem Schreiben bekannte Pflicht war nicht früh genug maschinell an den Autorweg gebunden.

## VERBINDLICHE URSACHENLÖSUNG
Nicht die Repair-Grenze für Wortzahl aufweichen.

Zielweg:
`Research -> Facts -> CONTEXT_REQUIRED -> gebundener Production-Context -> hashgebundener Authoring Contract aus denselben unveränderten Autoritäten -> DRAFT_REQUIRED -> Draft -> unveränderte echte Prüfer`.

Kein Chat, Codex, Nutzertext oder anderer externer Input darf Regeln ergänzen, lockern oder überschreiben.

Textmaschine, PPM 6.7.9, PSERC/PSTE, LanguageTool 6.8, Design, WordPress-Plugin und Theme/CSS bleiben READ-ONLY.

## TESTREGEL
Jeder bekannte Workflow-Schritt muss positiv und negativ gegen den vollständigen Gesamtworkflow geprüft werden. Isolierte Einzeltests zählen nicht als Gesamtworkflow-Beweis.

Auf den lokal exakt gebundenen Cause-Fix-Bytes tatsächlich terminal ausgeführt:
- 121/121 Unittests PASS;
- 15/15 Workflow-Stationen positiv und negativ;
- 39 Gesamtworkflow-Szenarien PASS;
- 10/10 Root->Datei-Acceptance PASS;
- reales LT 6.8;
- reales PPM 6.7.9;
- finale Testdatei 66753 Bytes;
- SHA256 `f6b08cdede6dedef329ca20dde3b648f77cd6f8b6342ee2407cc3441953a7c75`.

Diese Belege gelten ausdrücklich nur für die getesteten Cause-Fix-Bytes, **nicht** für den aktuellen Remote-PR-Head.

## OFFENE FEHLER / BLOCKER
1. `S4-BLOCK-CAUSEFIX-NOT-REMOTE`: Die 13 getesteten Cause-Fix-Dateibytes sind noch nicht vollständig auf PR #238 gebunden.
2. `S4-BLOCK-REMOTE-REPROOF`: Nach Übertragung müssen 121/121, Matrix 15/15 + 39 und Acceptance 10/10 auf exakt dem dann aktuellen Remote-Head ohne Codex erneut terminal laufen; danach Hardlock auf exakt diesem Head.
3. `S4-CLEANUP-TMP-BRANCH`: `tmp-should-not-use` wurde versehentlich angelegt. Er wird bis zur möglichen Löschung stets auf denselben Stand wie der Arbeitsbranch gehalten und darf niemals als Arbeits-/CURRENT-/Produktionsbranch verwendet werden.

## CODEX
Verbindlich: Codex **nur** für konkrete real gebundene Artikel-/Batch-Produktion und nur nach ausdrücklicher Nutzerfreigabe.

Kein Codex für Diagnose, Architektur, Code/Patch, Commit/Push, Preflight, Regressionstests, Dokumentation oder WordPress-/Handoff-Experimente.

Die Nutzung von Codex für einen Patch-/Push-Auftrag in diesem Chat war ein Regelverstoß; sie aktualisierte den Remote-PR nicht.

## NEXT ACTION
Ohne Codex:
1. exakt die 13 im Detailprotokoll `PROTOKOLL_HANDOVER_20260913_CAUSEFIX_CLOSEOUT.md` gebundenen Cause-Fix-Dateibytes auf `hobbyroom/system4-true-single-room-v1` übertragen;
2. alle 13 Remote-Blobs exakt prüfen;
3. Manifest `8789f0af37183e9988e0b90f9bb5ea2d3e0537c4b43e849d4e34a37fb1a904ff` nachweisen;
4. 121/121 + Matrix 15/15/39 + Acceptance 10/10 mit realem LT/PPM auf exakt dem aktuellen Head terminal ausführen;
5. Immutable Base Hardlock prüfen;
6. erst danach und nur nach ausdrücklicher Freigabe genau einen konkreten Codex-Artikeltest.

## NICHT ANFASSEN
- Textmaschine / Fachregeln
- PPM 6.7.9
- PSERC/PSTE
- LanguageTool-Version/Regeln
- Design / Theme / CSS
- WordPress-Plugin
- offizieller STARTMASTER0107/CURRENT_STATE
- kein Merge / kein Publish

## CAMPUS-/ARCHITEKTURFOLGE
Die Prinzipien „bekannte Prüferpflichten vor dem Schreiben aus denselben Autoritäten binden“ und „jeden bekannten Fehler positiv/negativ im Gesamtworkflow prüfen“ sind grundsätzlich allgemein sinnvoll. Sie werden noch **nicht** in globale Campus-/Neubauvorlagen übernommen, solange der Cause-Fix nicht auf dem Remote-System-4-Head gebunden und dort vollständig reproduziert ist.

## PLUGINS
**NICHT BETROFFEN.** In diesem Chat wurde kein Plugin entwickelt, technisch verändert oder auf eine neue Version aktualisiert. Keine Änderung im PLUGINS-Büro, keine CURRENT.zip, kein PU-Vorgang.

## EINE WAHRHEIT
- Campus CURRENT: `control/startmaster0107/CURRENT_STATE.json`
- System-4 CURRENT: `isolated_system4/README.md`
- System-4 Ziel: `isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`
- aktuelles Übergabeprotokoll: diese Datei
- PR-Text: ausschließlich Wegweiser
- ältere Protokolle: Historie/Beleg, keine CURRENT-Wahrheit
