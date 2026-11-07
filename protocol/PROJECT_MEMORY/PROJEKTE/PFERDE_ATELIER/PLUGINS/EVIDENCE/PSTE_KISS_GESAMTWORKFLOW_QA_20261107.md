# Pferdeatelier / PSTE – KISS-Workflowprüfung 07.11.2026

**Status: TECHNISCHE QA ERFOLGREICH, LIVE-1:1-TEST NICHT ERFOLGT – KEINE INSTALLER-ZIP FREIGEGEBEN.**

## 1. Gesicherter Ausgangspunkt

- Ursprüngliches Installer-Testpaket: PSTE **0.57.144.18**; ausschließlich dessen PHP-Code ist Ausgangspunkt.
- Der letzte hochgeladene **echte** WordPress-Stapelbericht von 0.57.144.18 war noch **RUNNING 40/87**. Darin wurden **3 Relevanzsperren tatsächlich erneut erzeugt**. Die restlichen 47 Fälle waren PENDING.
- Alle 100 ursprünglichen MINI-Entscheidungen und Titel wurden aus den beiden vom Nutzer bereitgestellten Textteilen vollständig wiederhergestellt. Die 87 JA-Themen wurden per exakter Originaltitel-Zuordnung mit den 87 Themen-IDs des echten WordPress-Berichts verbunden (87/87 Treffer).
- Mitgelieferte Kategorieliste: **1.165 Einträge**. Numerische WordPress-Kategorie-IDs sind in der Testumgebung künstlich; kein Abbild der Live-Datenbank.

## 2. Aus dem echten PHP-Code belegte Doppelbewertung

Der Stapelpfad war `PSTE_Mini_Workflow::forwardToPlan` → `PSTE_Admin::processOneTitleDeskReentry` → `PSTE_Repository::reanalyzeRetainedBacklogBatch` → `refreshPortalContextForKeysUsingBinding` → `refreshPortalContextBatch` → `refreshPortalContextForRow`.

Im Original wurde **zuerst** die Relevanz samt JA-Originalbeleg und die zentrale Planungs-/Dublettenprüfung durchgeführt. **Danach** setzte `refreshPortalContextForRow` mit `prepareEditorialPayload` die semantische Prüfung ein zweites Mal in Gang – ohne MINI-JA – und rief bei NORMAL_PASS die Planungsprüfung ein zweites Mal auf.

**Ursache:** Derselbe Kontext-Aktualisierer wird sowohl für die direkt vorher geprüften 87 Themen als auch für unabhängige vollständige Bestandsaktualisierungen genutzt. Eine pauschale Löschung wäre gefährlich: Echte spätere Kategorie-/Bestandsänderungen müssten weiterhin erkannt werden.

## 3. Bereinigte QA-Arbeitskopie – nur EINE vorhandene PHP-Datei geändert

Datei: `includes/class-pste-repository.php`.

- Der zielgenaue Wiederanlauf markiert den **gerade geprüften Zustand** ausdrücklich. Bei der anschließenden Kontext-Aktualisierung wird die eben getroffene Relevanz-, Titel- und Planungsentscheidung nur noch **verwendet**, nicht erneut gefällt.
- Der Wiederanlauf akzeptiert diesen Zustand nur, wenn er **PENDING**, mit genau der erwarteten Portalstruktur und gültigem normalen Pfad gespeichert ist. Fehlt bei einem NORMAL_PASS der gültige Planungsnachweis, wird ohne Schreiben abgebrochen.
- Der **eigenständige** vollständige Kontext-Neuaufbau bewertet erforderlichenfalls neu, liest aber dieselbe bereits vorhandene MINI-JA-Quelle. Bei geänderten Kategorien oder Beiträgen bleibt die Prüfung verbindlich.
- Drei ältere getrennte Wartungswege, die `prepareEditorialPayload` verwenden, bekommen beim erneuten Berechnen ebenfalls das unveränderte ursprüngliche MINI-JA passend zur Themen-ID; keine neue Belegtabelle, keine zusätzliche Regel.
- Keine PSERC-, K0-, WordPress-Kern-, Datenbanktabellen- oder Produktionsdatei geändert.

## 4. Reproduzierbare lokale Tests – echte PHP-Funktionen, WordPress-Speicherung ersetzt

Der Test lud 81 vorhandene PHP-Klassendateien und rief den unveränderten `PSTE_Normal_Metadata_Path`, den echten `PSTE_Planning_Readiness_Gate`, den echten `PSTE_Context_Evaluator` sowie die **geänderte echte** `PSTE_Repository::refreshPortalContextForRow`-Methode auf. WordPress-Optionen und Datenbankzugriffe wurden durch ein nur im Test vorhandenes In-Memory-Objekt ersetzt. Die 1.165 Kategoriebeschreibungen stammen aus der vorhandenen historischen Fixture.

| Kontrollfall | Messung | Ergebnis |
|---|---:|---|
| Normalpfad / JA mit Originaltiteln | 87/87 | Relevanz PROVEN, Titel erhalten |
| Gezielte Kontext-Aktualisierung nach einmaliger Prüfung | 87/87 | Relevanz PROVEN, Titel erhalten |
| **Zweiter kompletter Bestandsabruf im gezielten 87er-Weg** | **0** | Überflüssigen Abruf entfernt |
| Unabhängige vollständige Kontext-Aktualisierung | 87/87 | Relevanz PROVEN, Titel erhalten |
| Notwendige erneute zentrale Planung bei unabhängiger Aktualisierung | 24 | Erfolgreich ausgeführt |
| Eingesetzte SEO-Keyword-Dubletten | 24/24 | Vorher UND nachher korrekt blockiert |
| Ungültiger Zwischenstand | 1/1 | Ohne Datenänderung blockiert |
| Fehlende Planungsbestätigung | 1/1 | Ohne Datenänderung blockiert |
| Gefälschter MINI-Rohbezug | 1/1 | Ohne Datenänderung blockiert |
| Kategorie aus Portalstruktur entfernt | 1/1 | Alter Kategorienbezug verworfen (nicht weiter verwendet) |
| PHP-Syntax aller Dateien | 83/83 | PASS |
| Ausgangs-ZIP-Integrität | 121 ZIP-Einträge | PASS |

**Beobachtung:** Unter den Kategorietestdaten wurden im ersten semantischen Durchgang 24 NORMAL_PASS und 63 STRUCTURE_GAP festgestellt. **Diese Verteilung ist ausdrücklich keine Aussage über deine echten WordPress-Kategorien oder Freigabezahlen.**

## 5. Grenzen des Beweises (wichtig)

**Das ist kein 1:1-Test der echten WordPress-Installation.** Kein aktueller Datenbankklon; kein echter WordPress-Cron, keine echten Kategorien-IDs oder realen Beiträge aus dem produktiven Portal; keine vollständigen Speichertransaktionen des `reanalyzeRetainedBacklogBatch`-Workers. Nur der relevante zweite Abschnitt bis zur Datenbankschreibgrenze wurde aufgerufen, mit In-Memory-Ersatzdatenbank.

**Belegbar:** Beide doppelten Fachprüfungen sind im konkret untersuchten 87er-Wiederanlauf entfernt; die nötigen Einzelprüfungen bei einem **anderen** vollständigen Neuaufbau bleiben bestehen. **Nicht belegbar:** Dass es unter sämtlichen Plugin-Betriebsarten keine anderen Wiederholungen gibt oder dass alle Live-Themen korrekt im Redaktionsplan landen.

## 6. Revisionsstand / Freigabe

- Ausgangsdatei SHA256: `15344794337def5392b7dd06c1516a6680f0ba2f32ce19477b20076069eb0554`.
- QA-Quelldatei SHA256: `76707c0f7a378284dcdea638e72db664a11cc5eac8289f33100bc7f310d6f985`.
- Nur **eine** PHP-Datei weicht von Version 0.57.144.18 ab. Änderungen in der Datei `PSTE_KISS_GESAMTWORKFLOW_QA_20261107.diff` dokumentiert.
- **Keine neue ZIP und keine Installation empfohlen.** Nächste echte Freigabeschranke: isolierter WordPress-Klon mit dem aktuellen Themen-, Kategorie-, Beitrags- und MINI-Datenbestand, vollständiger 87er-Replay und Readback aller 87 Datensätze.