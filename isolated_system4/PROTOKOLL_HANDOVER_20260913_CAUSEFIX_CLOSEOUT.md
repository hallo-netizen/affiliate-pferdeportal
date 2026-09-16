# PROTOKOLL / ÜBERGABE — SYSTEM 4 CAUSE-FIX CLOSEOUT — 2026-09-13

Status dieses Dokuments: **AKTUELLES ABSCHLUSS-/NACHHOLPROTOKOLL DES SYSTEM-4-ARBEITSSTRANGS.** Es ist kein zweiter CURRENT_STATE. Die eine aktuelle System-4-Statuswahrheit liegt in `isolated_system4/README.md`. Der offizielle Campus-/Projektstand bleibt ausschließlich `control/startmaster0107/CURRENT_STATE.json`.

## 1. Frisch gelesene autoritative Quellen
- PR #238 `hallo-netizen/affiliate-pferdeportal`
- Branch `hobbyroom/system4-true-single-room-v1`
- `isolated_system4/README.md`
- `isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`
- `isolated_system4/AGENTS.md`
- `isolated_system4/FULL_RULE_BATCH_TASK.md`
- `isolated_system4/LIVE_BOUND_INPUT_ONE_ARTICLE.json`
- `control/CURRENT_STARTMASTER.json`
- `control/startmaster0107/CURRENT_STATE.json`
- aktueller Immutable-Base-Hardlock-Run des PR-Heads

## 2. Offizieller Campus-/Fachstand bleibt unverändert
`control/CURRENT_STARTMASTER.json` bindet weiterhin `STARTMASTER0107` und `control/startmaster0107/CURRENT_STATE.json`.

Der offizielle Produktionsstand ist weiterhin `BLOCKED` im Schritt `RUN_NEW_ARTICLE_BATCH_NO_STOP` / Sequenz `107007` mit `PPM679_REAL_EXECUTION_BLOCKED`; `hobbyroom_status=FREI`; `publish_allowed=false`.

System 4 bleibt ein **isolierter PR-Prototyp**. Dieser Chat hat den offiziellen STARTMASTER-/Campus-CURRENT_STATE nicht verändert.

## 3. Reale System-4-Läufe dieses Chats
### 3.1 Manifest-Binding-Blocker
Ein realer Ein-Artikel-Codex-Lauf erreichte die System-4-Root-Tür und stoppte fail-closed an `ROOT_ENTRY_MANIFEST_BINDING_MISSING`, weil der Live-Auftrag das bereits verpflichtende Feld `system4_root_manifest_sha256` nicht enthielt.

Dieser Fehler war kein unbekannter Runtimefehler; der vorhandene Negativtest kannte den fehlenden Manifestfall bereits. Der eigentliche Testfehler lag darin, dass vor dem Codex-Lauf nicht **die exakt später gesendeten Live-Bytes** getestet wurden.

Daraus wurde die dauerhafte Regel abgeleitet: Ein realer Codex-Auftrag darf nur aus einem vorher eingefrorenen, gehashten Live-Input bestehen; exakt dieselben Bytes müssen vorher positiv und in manipulierten Kopien negativ durch den Root-Einstieg gelaufen sein.

### 3.2 Realer Artikel-Lauf bis PPM / Repair-Kollision
Der nächste ausdrücklich freigegebene reale Ein-Artikel-Lauf verwendete den eingefrorenen Artikel:
- Titel `Putzbox für Pferde richtig auswählen`
- Typ `Beratung`
- Kategorie `putzbox-beratung`
- Keyword `Putzbox für Pferde`
- Plan-Slot `88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5`
- `publish_allowed=false`

Der Lauf erreichte real:
`Root -> Research -> Facts -> Context -> Draft -> FULL PPM`

PPM 6.7.9 meldete:
- `FULL:ppm679:BLOCKED_CONTENT_WORD_FLOOR`
- Ist: `448` Wörter
- Soll: mindestens `750` Wörter

Die notwendige Same-Article-Verlängerung wurde danach vom Repair-Kontinuitätsguard blockiert:
`REPAIR_SCOPE_FAIL:REPAIR_SCOPE_TOO_LARGE:LENGTH:0.7680`

Damit war erstmals real bewiesen: Eine **vor dem Schreiben bereits bekannte fachliche Pflicht** wurde nicht vor dem Schreiben hart genug in den Autorweg gebunden und tauchte erst nach dem Draft beim Prüfer auf. Das ist eine Ursachen-/Reihenfolgefrage und kein Anlass, Textmaschine oder PPM zu verändern.

## 4. Ursachenentscheidung — nicht Symptom behandeln
Der kurzzeitig entwickelte Sonderweg „bei `BLOCKED_CONTENT_WORD_FLOOR` darf die Reparatur >30 % wachsen“ wurde als **Symptombehandlung verworfen**.

Dauerhafte Zielentscheidung:
1. Nach `facts` darf noch nicht geschrieben werden.
2. Erst muss der gebundene Production-Context vollständig vorliegen.
3. Daraus wird maschinell ein hashgebundener **Authoring Contract** ausschließlich aus den bestehenden READ-ONLY-Autoritäten abgeleitet.
4. Kein Chat, kein Codex und kein externer Input darf neue Regeln ergänzen, Regeln lockern oder Regeln überschreiben.
5. Erst danach öffnet `DRAFT_REQUIRED`.
6. Ein neuer Draft und eine Reparatur müssen vor Annahme gegen die bereits bekannten unveränderten PPM-/Design-/Context-Pflichten geprüft werden.
7. Dynamische Befunde, die erst am fertigen Text entstehen können, dürfen weiterhin im normalen FULL-Check/Repair-Weg auftauchen.
8. Meldet ein späterer Prüfer einen Fehler, der bereits vor Draft bekannt und bindbar war, ist das eine Invarianzverletzung des Vorab-Gates und darf nicht als normaler neuer Repair-Fall schöngerechnet werden.

**Unverändert / READ-ONLY:** Textmaschine, PPM 6.7.9, PSERC/PSTE, LanguageTool 6.8, Design, WordPress-Plugin, Theme/CSS.

## 5. Positiv-/Negativregel gegen den Gesamtworkflow
Die frühere Prüfmethode mit isolierten Einzeltests war unzureichend. Zwei jeweils grüne Einzelregeln konnten im Gesamtweg kollidieren.

Dauerhafte Testregel:
**Jeder bekannte Workflow-Schritt muss mindestens einmal positiv und einmal negativ im vollständigen Gesamtweg geprüft werden.** Ein Einzeltest allein darf nicht mehr als „Gesamtworkflow getestet“ oder „komplett positiv/negativ getestet“ bezeichnet werden.

Dafür wurde auf den lokal getesteten Cause-Fix-Bytes eine vollständige Fault-Matrix gebaut:
- 15/15 erforderliche Workflow-Stationen positiv und negativ;
- 39 Szenarien;
- Root bis finale WordPress-Datei;
- `mocks_used=false` für den Produktionsbeweis;
- reales LanguageTool 6.8;
- reales PPM 6.7.9.

Zusätzlich liefen auf exakt denselben lokalen Cause-Fix-Bytes:
- kompletter `isolated_system4`-Unittestbestand: **121/121 PASS**;
- Gesamtworkflow-Matrix: **PASS, 15/15, 39 Szenarien**;
- kompletter Root->Datei-Acceptance-Lauf: **10/10 PASS**;
- finale Testdatei: **66753 Bytes**;
- finale Testdatei SHA256: `f6b08cdede6dedef329ca20dde3b648f77cd6f8b6342ee2407cc3441953a7c75`;
- LT-6.8-SHA256: `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`;
- PPM-6.7.9-SHA256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`.

Diese PASS-Belege gelten **nur für die getesteten lokalen Cause-Fix-Bytes**, nicht für den aktuellen Remote-PR-Head.

## 6. Exakt getesteter Cause-Fix-Stand — noch NICHT auf PR #238
Für den getesteten Cause-Fix wurden folgende Zielblobs gebunden:

- `isolated_system4/LIVE_BOUND_INPUT_ONE_ARTICLE.json` -> `145d5489367488f2d71ec062369e5f7cc1b6401c`
- `isolated_system4/authoring_contract.py` -> `902c1bbdd55b6e859debe279b1a541b08038e5d6`
- `isolated_system4/codex_entry.py` -> `70da91296087c8e0abb12ea202b76deb43cc098f`
- `isolated_system4/content_guard.py` -> `70e9a60f9167c4b4b93a706332a001484d26e2d1`
- `isolated_system4/controller.py` -> `e7cf054e3b4ff92a2ce8a0adeb59d2e558aa04ce`
- `isolated_system4/full_workflow_fault_matrix.py` -> `626723a7694184b041145c8dbdf7e6a13b895446`
- `isolated_system4/production_checks.py` -> `3266c1ba5b33e4cc6b7c488bf54c390eeb1ccc66`
- `isolated_system4/root_entry.py` -> `947699b5f79c198ecae949af3be224a3f767172c`
- `isolated_system4/test_authoring_contract.py` -> `d159f94c736f29dbfcf139bcdf987314d1a95c75`
- `isolated_system4/test_content_guard.py` -> `f8fe4936d5497f7731104a53137b620a7dcf1a4d`
- `isolated_system4/test_live_bound_input_exact.py` -> `e97f5b028989b8e23ea1c1314d6c93259e8ae16e`
- `isolated_system4/test_local_end_to_end_chat_handoff.py` -> `562200126a0ac287f1ab5727b298382368fb4290`
- `isolated_system4/test_repair_continuity.py` -> `a61e1893ba0fa909dfc131cbb4c5c458311dfd16`

Gebundener Cause-Fix-Manifestwert:
`8789f0af37183e9988e0b90f9bb5ea2d3e0537c4b43e849d4e34a37fb1a904ff`

Gebundener Cause-Fix-Live-Input:
- 643 Bytes
- SHA256 `9d843b3f77d4c7b4e1c85b59125cbdab5e5ae9277a941516ac2c54368d5f1b15`

## 7. Tatsächlicher aktueller Remote-Stand
Frisch geprüft nach Cleanup:
- PR #238: **open, draft, unmerged**;
- Branch: `hobbyroom/system4-true-single-room-v1`;
- aktueller Head: `c75742bcc9780a6806890ae2f690ed2a0ed8b11f`;
- der Tree dieses Heads ist bytegleich zu `edfe6049768db68f85bf3babedce3199538217ef`;
- seit `edfe6049...` existieren netto keine Dateiveränderungen mehr; die fünf temporären Transportdateien wurden wieder entfernt;
- Immutable Base Hardlock auf exakt `c75742bc...`: **SUCCESS**, Run `34763480816`.

Wichtig: Der in Abschnitt 6 getestete Cause-Fix ist **nicht** auf diesem Remote-Head.

Der aktuelle Remote-Live-Input ist weiterhin die ältere 643-Byte-Datei mit:
- Git blob `212d062eef9895cf67299f7ae6fcceee760cc2ed`
- `system4_root_manifest_sha256 = 3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

`authoring_contract.py` und `full_workflow_fault_matrix.py` gehören zum getesteten Cause-Fix, sind aber im aktuellen Remote-PR-Stand noch nicht gebunden.

Deshalb ist der Remote-PR **NICHT** als 121/121-/15/15-/10/10-Cause-Fix-PASS freigegeben.

## 8. Codex-Nutzung — Fehler dieses Chats und verbindliche Regel
`isolated_system4/AGENTS.md` schreibt bereits eindeutig vor:
- Codex ist knappe Produktionsressource;
- kein Codex für Diagnose, Architektur, Preflight, Handoff-Experimente oder WordPress-Arbeit;
- Codex nur für einen **real gebundenen Artikel-Produktionslauf** nach expliziter Nutzerfreigabe.

Diese Regel wurde in diesem Chat von Chat selbst verletzt: Codex wurde für einen mechanischen Patch-/Push-Auftrag eingesetzt. Der Task konnte lokal testen/committen, aber nicht pushen, weil der Codex-Checkout kein `origin` hatte.

Dauerhafte Konsequenz: **Codex ab jetzt ausschließlich für konkrete Artikeltests/-produktion.** Codeübertragung, GitHub-Commit/Push, Preflight, Diagnose und Dokumentation erfolgen ohne Codex.

## 9. Parallelbranch / Worker
Durch einen Toolfehler wurde der unnötige Branch `tmp-should-not-use` erzeugt.

Aktuell wurde er fast-forward exakt auf `c75742bcc9780a6806890ae2f690ed2a0ed8b11f` gesetzt. Er enthält damit keine abweichende aktuelle System-4-Wahrheit und keine verbliebenen Transportdateien.

Mit den in diesem Chat verfügbaren GitHub-Aktionen kann die Branch-Referenz nicht gelöscht werden. **Cleanup bleibt offen:** Branch `tmp-should-not-use` löschen, sobald ein branch-delete-fähiger Weg zur Verfügung steht. Er darf niemals als Arbeits-, CURRENT- oder Produktionsbranch verwendet werden.

Kein anderer Parallelworker ist als aktuelle System-4-Wahrheit gebunden.

## 10. Eine Wahrheit
- offizieller Campus-/Projekt-CURRENT: ausschließlich `control/startmaster0107/CURRENT_STATE.json`;
- System-4-CURRENT: ausschließlich `isolated_system4/README.md`;
- System-4-Ziel: ausschließlich `isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`;
- aktuelles Abschluss-/Übergabeprotokoll: diese Datei;
- PR-Text: nur Wegweiser;
- ältere Closeouts/Realrun-Protokolle: historische Belege, keine CURRENT-Quelle.

## 11. Plugins
**NICHT BETROFFEN.**

In diesem Chat wurde kein WordPress-Plugin entwickelt, kein Eigen-/Drittanbieter-Plugin technisch geändert und kein Plugin tatsächlich auf eine neue Version aktualisiert. Deshalb keine Änderung im PLUGINS-Büro, keine `CURRENT.zip`, kein PU-Vorgang.

## 12. Campus-/Architekturfolgen
Die neue Ursache-Regel — bekannte spätere Prüferpflichten müssen vor dem Schreiben aus denselben unveränderten Autoritäten gebunden sein und jeder bekannte Fehler muss positiv/negativ gegen den Gesamtworkflow geprüft werden — ist grundsätzlich allgemeingültig.

Sie wird **noch nicht** in globale Campus-/Neubauvorlagen übertragen, weil der Cause-Fix noch nicht auf dem aktuellen System-4-PR-Head gebunden und dort erneut komplett bewiesen ist. Eine globale Übernahme vor diesem Remote-Beweis würde einen noch nicht final gebundenen Prototyp vervielfältigen.

## 13. NEXT ACTION — verbindlich
Status: **BLOCKED**.

Ohne Codex:
1. Exakt die 13 in Abschnitt 6 gebundenen Cause-Fix-Dateibytes auf `hobbyroom/system4-true-single-room-v1` übertragen; keine Neuinterpretation und keine zusätzliche Codeänderung.
2. Remote alle 13 Git-Blobs exakt gegen Abschnitt 6 prüfen.
3. Cause-Fix-Manifest muss exakt `8789f0af37183e9988e0b90f9bb5ea2d3e0537c4b43e849d4e34a37fb1a904ff` ergeben.
4. Auf dem **danach aktuellen Remote-Head** ohne Codex terminal ausführen: 121/121 Unittests, 15/15 Workflow-Matrix mit 39 Szenarien, 10/10 Acceptance mit realem LT 6.8 + PPM 6.7.9.
5. Immutable Base Hardlock auf exakt diesem Head prüfen.
6. Erst danach und nur nach ausdrücklicher Nutzerfreigabe: **genau ein konkreter realer Artikeltest mit Codex**. Kein Codex für Code-/Git-/Testvorbereitung.
7. `tmp-should-not-use` löschen, sobald Branch-Delete technisch verfügbar ist.

Kein Merge. Kein Publish.
