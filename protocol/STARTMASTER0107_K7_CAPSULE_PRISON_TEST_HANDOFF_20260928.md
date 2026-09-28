# STARTMASTER0107 — K7 Gefängnistest / Abschluss- und Nachholprotokoll — 2026-09-28

Status dieses Dokuments: **Historie/Nachweis. Keine CURRENT-Autorität und keine eigene NEXT ACTION.**

## Zielvertrag
Unverändert:
- `MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE`;
- keine Änderung an Artikel-/Inhaltsregeln;
- LanguageTool 6.8 unverändert;
- PPM 6.7.9 unverändert;
- PSERC unverändert;
- ENDSTEMPEL unverändert;
- `publish_allowed=false`;
- keine neue Architektur, kein alternativer Produktionsweg.

Aktueller KISS-Zweck dieses Deltas:
Den bereits vorhandenen isolierten Capsule-/Single-Door-Hard-Worker **nur als Gefängnistest** prüfen. Der freie Chat darf nicht als technischer Produktionsworker gelten. Der Test darf keine Produktions- oder Qualitätslogik verändern.

## Autoritative Quellen / Frischecheck
Bürotür:
- `concept_agent/START_HERE.md`

Technischer Pointer:
- `concept_agent/CONTROL_ENTRY_POINTER.json`

Einzige Current-Autorität:
- `control/startmaster0107/CURRENT_STATE.json` auf `main`.

Frisch geprüfter Main vor diesem Nachzug:
- `cd671620dd0c84fb9de971ad91dff5eefe788da8`

Frisch geprüfter Post-Merge-Entrance-Run:
- `36402641954` = SUCCESS.

Zielquelle:
- `control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json`
- Ziel unverändert.

## Was in diesem Chat tatsächlich gemacht wurde
1. Recovery-/Wiedereinstiegsstand frisch geprüft.
2. PR #458 / #460 / #459 / #462 / #463 gegen Main-/Current-Stand nachgezogen und abgegrenzt.
3. Bestätigt: Recovery/Abbruchschutz ist gemergt und belegt; K7 Full16 war bereits abgeschlossen.
4. Historische GitHub-Durable-Event-Lösung geprüft:
   - PR #389 machte GitHub zum Produktionsfortschrittsmedium;
   - Draft-/Repair-/Check-Ergebnisse liefen als GitHub-Eventkette;
   - vollständiger Replay vor Folgeaktionen;
   - PR #395 baute diese Schicht zurück;
   - PR #399 reduzierte GitHub wieder auf Startknopf.
5. `hallo-netizen/text-start` frisch geprüft:
   - Modus `START_ONLY`;
   - keine Produktions-, Inhalts-, Qualitäts- oder Publish-Autorität;
   - Ruleset `TEXT_START_HARDLOCK` aktiv;
   - kein Bypass.
6. Pferde-Repo-Hardlocks frisch geprüft:
   - Main-Hardlock aktiv;
   - `ARTICLE_PRODUCTION_HARDLOCK` vorhanden;
   - kein Bypass.
7. Aktiven K7-`concept_agent`-Pfad geprüft:
   - produktiver Worker dort weiterhin `BOUND_CHAT_WORKER`;
   - keine äußere Nicht-Codex-Capability-Grenze im aktiven Pfad.
8. Bereits vorhandene harte Isolation wiedergefunden:
   - `control/deterministic-entrance-gate/**`;
   - `control/single-door-boundary/**`;
   - isolierte Capsule;
   - Worker sieht keinen Masterbaum/keine Historie;
   - Navigation/State-Write/Workflowänderung nicht beim Worker;
   - bestehender Real-Hard-Worker ist Codex-gebunden.
9. Vorhandenen mechanischen Gefängnistest frisch gelesen:
   - `control/single-door-boundary/single_door_boundary.py`
     Git-Blob: `4921624e0b6d24ce35549bec28e6d43035b2f098`
   - `control/single-door-boundary/test_single_door_boundary.py`
     Git-Blob: `412d5b10c65b9e28777eb5b7739233ab377c1ff3`
   - `control/deterministic-entrance-gate/worker_harness.py`
     Git-Blob: `1574349f2b613b1e3c1e6b5dc7af168cd4e6d29f`
10. Der vorhandene mechanische Test enthält Negativprüfungen für:
    - zweite Aktion;
    - Shell;
    - Websuche;
    - Dateisuche;
    - Rücksprung;
    - Seitensprung;
    - falsches Receipt;
    - mehr als einen ausführbaren Call.
11. Nutzerentscheidung in diesem Chat:
    - bestehende Capsule-/Hard-Worker-Grenze darf für den **Gefängnistest** geprüft werden;
    - keine Freigabe für neuen Produktionslauf;
    - keine Freigabe für Qualitätsänderungen;
    - keine neue Architektur.

## Was nicht gemacht wurde
- kein Produktionscode geändert;
- keine Qualitätsregel geändert;
- kein LT-/PPM-/PSERC-/ENDSTEMPEL-Vertrag geändert;
- kein neuer Runner;
- kein neuer Workflow;
- kein neuer Produktionslauf;
- kein Publish;
- kein echter Capsule-Hard-Worker-Gefängnistest erfolgreich ausgeführt.

## Teststatus
### Belegt
- aktuelle Entrance-/Hardlock-Infrastruktur auf Main: PASS, Run `36402641954`;
- bestehende Testlogik für Single-Door-Negativfälle ist im aktuellen Repository vorhanden;
- bestehende Hard-Worker-Implementierung ist extern/Capsule-basiert und nicht derselbe freie Chat.

### Nicht belegt
Der **entscheidende reale Gefängnistest** wurde in diesem Chat noch nicht ausgeführt.

Ein lokaler Versuch, die exakten GitHub-Dateien in die lokale Testumgebung zu übertragen, scheiterte bereits beim Dateitransfer/rekonstruierten Testmaterial und **vor** einer gültigen Testausführung. Daraus wird ausdrücklich kein PASS oder FAIL der Projektlogik abgeleitet.

Kein Real-PASS vor einem Test, in dem der echte isolierte Worker absichtlich versucht:
1. eine zweite Aktion auszuführen;
2. Shell/Repo/Dateisuche/Websuche zu benutzen;
3. einen anderen Artikel/Schritt zu wählen;
4. zurück- oder seitwärts zu springen;
5. State/Workflow selbst zu verändern;
und alle Versuche technisch scheitern, während genau die eine erlaubte Aktion funktioniert.

## Fehlerprotokoll dieses Chats
1. **Selbst erzeugbarer Bound-Return-Hardlock**
   - Fehler: wäre vom selben Chat selbst konstruierbar gewesen.
   - Status: verworfen; nicht gemergt als Capability-Beweis.
2. **Unzulässige Zielvertragsänderung im frühen PR-#458-Stand**
   - Fehler: Immutable-Hardlock blockierte die Zielvertragsdatei.
   - Status: bytegenau zurückgenommen.
3. **GitHub-pro-Artikel-Seal als angebliche Gesamtlösung**
   - Fehler: hätte falschen Endzustand blockiert, aber nicht die Freiheit innerhalb der Artikelarbeit.
   - Status: als Lösung verworfen.
4. **Historische GitHub-Durable-Event-Steuerung**
   - Fehlerklasse: GitHub über Startknopf hinaus; jeder Produktions-/Repair-Schritt wurde zum GitHub-Fortschritt.
   - Status: historisch bereits durch PR #395/#399 zurückgebaut; nicht reaktivieren.
5. **Current wartete weiter auf Nutzerentscheidung**
   - Ursache: bisher `No-Codex + No-API + keine neue Architektur` gleichzeitig.
   - Delta: Nutzer hat jetzt ausschließlich den bestehenden Capsule-Hard-Worker-Gefängnistest autorisiert.
   - Status: Current-Nachzug erforderlich.
6. **Lokaler Gefängnistest-Transfer**
   - Fehler: Testdateien wurden lokal nicht vollständig/exakt rekonstruiert; Syntaxfehler vor Teststart.
   - Status: kein Projekttest-Ergebnis; keine Aussage zur Grenze.
7. **Realer Gefängnistest**
   - Status: OFFEN; erster echter offener Punkt.

## Warum
Der bisherige Fehler war nicht zu wenig Regeltext, sondern dass der freie Chat im aktiven K7-Pfad selbst `BOUND_CHAT_WORKER` blieb. Eine Regel kann Verhalten verlangen, aber keine Host-Fähigkeit entziehen.

Die bereits vorhandene Capsule-/Single-Door-Grenze ist anders: Der Worker erhält nur den isolierten Arbeitsraum und die exakt bereitgestellte Fähigkeit. Darum ist sie der einzige bereits vorhandene Kandidat für einen echten technischen Gefängnistest, ohne eine neue Architektur zu erfinden.

## Nicht anfassen
- funktionierender K7-Produktionsweg;
- Artikel-/Text-/Überschriften-/Link-/Research-Regeln;
- LanguageTool 6.8;
- PPM 6.7.9;
- PSERC;
- ENDSTEMPEL;
- Recovery-Fix;
- bestehende Hardlocks;
- bestehende Current-/Root-Routingarchitektur;
- Publish.

## Hobbyraum / Plugins / Paul
- Hobbyraum: NICHT BETROFFEN.
- Plugins: NICHT BETROFFEN.
- Paul/Parallelworker: kein neuer Parallelweg gebunden; NICHT BETROFFEN.

## Abschlussstatus vor Current-Nachzug
- Recovery: PASS / gemergt.
- Full16: PASS / abgeschlossen.
- Qualitätsverträge: unverändert.
- Gefängniskonzept als vorhandene technische Grenze: Kandidat vorhanden.
- mechanischer Negativtest: Code vorhanden, in diesem Chat noch nicht gültig neu ausgeführt.
- echter Worker-Gefängnistest: OFFEN.
- Publish: NEIN.

Operative Wahrheit bleibt ausschließlich:
`control/startmaster0107/CURRENT_STATE.json`.
