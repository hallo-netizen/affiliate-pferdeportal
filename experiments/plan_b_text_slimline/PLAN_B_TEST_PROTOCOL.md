# PLAN B – späteres Prüfprotokoll

## A. Isolation

Plan B bleibt bis zur ausdrücklichen Testfreigabe vollständig unverdrahtet:
- kein Import aus produktivem Controller;
- kein Workflow-Trigger;
- kein `main`-Merge;
- kein WordPress-Zugriff;
- kein Publish.

## B. Vergleich gegen bestehenden funktionierenden Stand

1. denselben Generation-1-7er-Batch verwenden;
2. existierenden Qualitätsprozess unverändert ausführen;
3. bestehende 12 Stage-Proofs + FACHWORKFLOW_PASS + ITEM_RECEIPT als Input an Plan-B-Tür geben;
4. Artikelbytes und alle relevanten Hashes vergleichen;
5. Final Review auf exakt demselben Prepared-Inhalt;
6. externe PSERC-Finalisierung unverändert;
7. GitHub-Endstempel unverändert.

## C. PASS nur wenn

- 12/12 Qualitätsstufen unverändert PASS;
- PPM content_hash == final article SHA;
- kein alternativer Pfad;
- Chat kann keinen Schritt wählen;
- Wächter hat keine Fach-/Qualitäts-/Designlogik;
- jede Abweichung führt STOP;
- `publish_allowed=false` bis zur bestehenden Publish-Grenze;
- finale Artikelbytes gegenüber Referenz identisch;
- keine Sicherheitsgrenze entfallen ist.

## D. Abbruch

Ein einziger Unterschied bei Qualität, Inhalt, Design, Hashbindung, Signierung, Endstempel oder Publish-Sperre -> Plan B FAIL, keine Integration.


## E. Aktuell erkannte Testlücke – LanguageTool

Live-Befund Plan A vom 07.09.2026:
`BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING`.

Harte Gegenprüfung Plan B:
Der aktuelle Shadow-Controller prüft bei Nicht-PPM-Stufen nur Stage-Proof, Status, Identität, Evidence und Artefakt-Hashes. Er führt LanguageTool selbst nicht aus und bindet keinen vorhandenen LanguageTool-Ausführungsbefehl.

Damit ist der bisherige Plan-B-Positivtest für `languagetool` **kein Beweis realer LanguageTool-Ausführung**.

Folge:
- Plan B nicht als Vergleichs-Live-Test starten, solange der bestehende reale LanguageTool-Ausführungsweg nicht historisch/technisch identifiziert ist.
- keine Qualitätsregel ändern;
- keine neue LanguageTool-Architektur erfinden;
- später muss Plan B denselben belegten bestehenden LanguageTool-Weg verwenden wie Plan A.
