# 19.11.2026 – PAA Timeout in Original-Pferdeatelier und Hobbydepot behoben, 0.4.24.6

## Echter Befund
Nutzerscreenshot und `texterstellung-diagnose-20261119-100006.json`: 3D-Bogenschießen `BLOCKED_PARKED`, Grund `PSTE_PAA_TASK_TIMEOUT`, 5 Rohkeywords, 0 abgeschlossene Kandidaten. Die externe Task-ID ist im unveränderlichen Original-Archiv vorhanden, nicht im Diagnosedownload enthalten. Der DataForSEO-Live-Ready-Status wurde NICHT live eingesehen.

## Originalvergleich und Korrektur
Die drei PSTE-Quelldateien für Job, Research-Driver und DataForSEO-Client sind bytegleich zwischen Pferdeatelier 0.4.23, der vom Pferdeatelier 0.4.31 abgeleiteten Blankokopie 0.4.31.1 und Hobbydepot 0.4.24.5. `PSTE_Research_Job::advanceQuestionsTask()` prüfte nach 1800s die eigene Timeout-Sperre VOR dem Readiness-GET. So wird selbst eine schon verfügbare Task-Rückmeldung nicht gelesen.

Die aktuelle Hobbydepot-Installer-ZIP `Texterstellung_Hobbydepot_0.4.24.6_PAA_ARCHIV_FORTSETZUNG.zip` **ändert nur drei bestehende PHP-Dateien** (84/87 byteidentisch, keine neue Architektur):
1. Original `class-pste-research-job.php`: PAA-Readiness für die **bereits gespeicherte Task-ID** zuerst per GET prüfen; Timeout erst, wenn ausdrücklich noch nicht READY. Archivierter, signierter Originalauftrag kann mit derselben UUID und fertiger GET-Rückmeldung über die **bestehende** `persistQuestionsResponse()`-Funktion bis FINALIZE laufen.
2. Original `class-pste-breadth-research-queue.php`: Nur einen explizit archivierten PAA-Timeout-Einzelauftrag (Queue 1/1, Eigentümer/UUID/Kategorie/Archivhash korrekt) wiederaufnehmen. Kein `task_post`; nur GET `tasks_ready` und `task_get/advanced`. NOT_READY, GET-Fehler, Fremd-/Doppelauftrag, korrupte Signatur: **keine Änderungen**, fail-closed. Archiv bleibt unveränderlich.
3. Bestehendes `texterstellung.php`: Version 0.4.24.6, bei genau diesem geparkten Einzelfehler ein Admin-Button **„Gesperrten Auftrag prüfen und falls fertig fortsetzen“** samt vorhandener Nonce-/Rechteprüfung und anschließendem originalen Driverstart. Andere Recherche und deren Kostenhaken unverändert.

## Prüfbeweis und Grenze
- ZIP CRC 87/87, PHP-Lint 78/78, JSON 8/8.
- **28/28 gezielte lokale Original-PHP-WordPress-Mocktests PASS**, darunter archivierter Job → exakt gleiche UUID → Original-PAA fertig → FINALIZE, 2 GET/0 POST; „nicht ready“/Anbieterfehler 0 Recovery-Writes; falsche UUID, fremde Kategorie, kaputtes Archiv, andere aktive Arbeit, mehrfacher Start werden abgewiesen; Test old PAA >1800s READY→FINALIZE, NOT_READY→Timeout. Originalarchiv bleibt erhalten.
- SHA256 `89fec4d67623116b764a2a9581a1871550b3529ef5f53d556707d12e42708fb8`, Größe 506709 Bytes.
- **Keine echte WordPress-/Provider-Endabnahme**, keine Behauptung über noch vorhandenes Task-Ergebnis, und keine externe Gebührenbestätigung. Keine K0-/K-Multi-/Kategorien-/PSERC-/Publish-Regeländerung. Pferdeatelier-Original unangetastet.

## Büro nachweislich geschrieben
- `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.6_PAA_ARCHIV_FORTSETZUNG.zip`
- `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.24.6_PAA_ARCHIV_FORTSETZUNG.zip`
- Büro `Texterstellung-CURRENT.md` aktualisiert, alter 0.4.24.5-Stand bleibt archiviert.
- MD/JSON-Testbericht und vollständiges 28-Testlog im Fachbüro.

**Einziger nächster Nutzerweg:** Backup → 0.4.24.6 unter WordPress „Installiertes Plugin ersetzen“ einspielen → `Texterstellung → Recherche → Gesperrten Auftrag prüfen und falls fertig fortsetzen` **einmal**. Ist Task nicht fertig, Archiv unverändert, keine Neu-Recherche. Bei Erfolg muss danach die Original-FINALIZE-Anzeige beobachtet werden; nicht als fertig behaupten, bevor echter Live-Status folgt.
