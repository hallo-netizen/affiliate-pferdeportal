# Pferdeatelier – Vollplan an den einen vorhandenen Prüf-Owner binden (02.11.2026)

**QA ONLY. Kein installierbares Plugin, kein WordPress/K0-E2E und keine LIVE-Änderung.**

## Tatsächlich verfügbare Quelle
- Ausgang: vollständige bereits getestete Portal SEO Themenengine **0.57.143.2**, aus der bestehenden Pferdeatelier-Library ausgelesen.
- Original-ZIP `/Pferdeatelier/TempVerify/PFERDEATELIER_PSTE_0.57.143.2_SUCHERGEBNISSE_NUR_TESTUMGEBUNG.zip`
- Original-SHA256 `d75922e84ca0ab8c68937bdef061510abd9f206beb40dbb5d3682b44d99008ea`; 116 Plugin-Dateien, 78 PHP.
- **Nur lokale isolierte QA-Änderung** an bestehenden `class-pste-planning-readiness-gate.php`, `class-pste-repository.php`, `class-pste-runner.php`. Keine neue Regel, Klasse, Worker, Tabelle, kein Originalplugin überschrieben.
- **Vollständiger 3-Dateien-Patch** bereits im bestehenden physischen Plugin-Archiv `/Pferdeatelier/TempVerify/PFERDEATELIER_PSTE_1432_ZENTRALER_PLANBESTAND_NUR_QA_20261102.patch`, SHA256 `e9c66d3d76a4afd0bebf6c3cfba7cbb14291eff37be2cc0e3753343bb9b04577`. Eigenständiger Original-ZIP-Entpackungslauf: GNU patch `--dry-run --fuzz=0 -p1` 3/3 PASS; angewandte Quelle bytegleich mit den lokalen geänderten drei PHP-Dateien.

## Nachgewiesener Fehler und konkrete Korrektur
Beim Wiederaufnehmen älterer Themen bekam `PSTE_Planning_Readiness_Gate` bisher nur WordPress-Inventar, **nicht** die redaktionell geplanten Artikel. `PSTE_Context_Evaluator` prüfte geplante Doppelthemen dagegen eigenständig, konnte veraltete Sperrgründe behalten und entgegen neuer zentraler Prüfung `PASS` zu `NO` machen.

Der wiederverwendete **eine zentrale** Planungsowner bekommt beim Retained-Backlog-Durchlauf **einmal pro bestehendem begrenztem 40er-Paket** den aktuellen *vollständigen* redaktionellen Plan mittels `PSTE_Snapshot::editorialPlan()`. Dessen SHA muss zur bestehenden Kontextbindung passen, sonst fail-closed ohne Freigabe. Alle Familien und auch ungeklärte Kategorien bleiben enthalten. Die bisherige Plan-zu-Inventar-Projektion ist unverändert vom Runner in den schon bestehenden zentralen Gate verlagert; Runner delegiert. Die beiden älteren Kontext-Äquivalenzmarkierungen werden **nur im Moment einer tatsächlichen aktuellen zentralen Neuentscheidung** aus diesem Kandidaten entfernt; unabhängig entstandene Gründe bleiben erhalten. Keine Zusatzabfrage *je Thema*, sondern genau ein vorhandener Plan-Optionsleser pro 40er-Paket.

## Tests
- 21 zusätzliche Positiv-/Negativ-Prüfungen mit realen PHP-Klassen PASS: geplante und publizierte Artikel, zusätzlich anderer Kategorie-Zweig, alter Kontextmarker und aktuelle Freigabe, unabhängiger SOURCE_PROVENANCE-Sperrgrund bleibt, 5.014 synthetische IDs ohne Verlust.
- Sechs bestehende echte PHP-Testprogramme weiterhin PASS: `qa_143_workflow.php`, `test_reentry_proof.php`, `test_sql_prefilter.php`, `test_search_admin.php`, `test_pserc_143.php`, `test_one_workflow.php`. Externe Titel-JSON im letzten Programm wirklich geschrieben, geändert, eingelesen, mit synthetischen WordPress-Zeilen.
- 78/78 PHP-Dateien Syntaxprüfung PASS.
- Patch aus unveränderter 143.2 erneut unabhängig exakt angewendet: 3/3, byteidentisch.

## Ausdrückliche Sicherheitsgrenze – verwerfener Löschversuch
Eine **separate, verworfene Risikokopie** hat probeweise die älteren Kontext-Äquivalenzmarker komplett entfernt. Eine neue Negativprobe hat nachgewiesen: bei zuvor gespeichertem Gate-PASS und **zwischenzeitlich neuem Planartikel** würde die Kandidatenrolle ohne weitere aktuelle Gate-Bindung `YES` liefern, während die aktuelle zentrale Prüfung das Doppelthema korrekt blockiert. **Diese gefährliche Löschung wurde NICHT in den obigen Patch übernommen und wird NICHT ausgeliefert.** Die Context-Zwischenphase muss noch sicher an den einen Owner gebunden werden.

Der optionale upstream-Artikel-Eigentümerpfad mit Legacy-Äquivalenz bleibt separat auf Doppelentscheidung zu prüfen. Daher **kein behaupteter Gesamt-Einmalprüf-PASS und kein neues Plugin**. Der volle Bericht steht unter `/Pferdeatelier/TempVerify/PFERDEATELIER_PSTE_1432_PLANBESTAND_KONSOLIDIERUNG_QA_20261102.md`. LIVE `pferde-atelier.de` auf 0.57.120 bleibt unangetastet.

**Nächste Arbeit, keine Zwischeninstallation:** die noch offene Context-/Upstream-Prüfung so in die einzige zentrale Planentscheidung führen, dass auch bei Planänderung während der Kontextaktualisierung nie ein altes PASS freigibt; dann alle Tests und echten WP-/K0-Grenzen prüfen und erst EIN kumuliertes Testpaket bauen.