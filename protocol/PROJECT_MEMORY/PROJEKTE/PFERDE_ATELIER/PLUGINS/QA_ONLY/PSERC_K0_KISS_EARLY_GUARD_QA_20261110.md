# PSERC / K0: Früherer Stopp bei verändertem Redaktionsplan – QA, 10.11.2026

**Auftrag:** Bestehende WordPress→PSERC→K0-Dateiausgabe vollständig prüfen und danach ausschließlich nachweislich ungenutzte Altlasten entfernen. **Kein K0-, Live- oder Datenumbau.**

## Neuer tatsächlicher Codebefund
- Zwei vorhandene Bedienoberflächen verwenden **dieselbe**, schon bestehende PSERC-Datenquelle: `PSTE_Admin::exportPlanningTopics` und `PSERC_Admin::exportLivePreview` lesen `PSERC_Plan_Snapshot_Store::getActive()` / `materializeReadyBatch()`. **Keine zusätzliche Ausgabestelle nötig.** Nicht beide Exportfunktionen löschen; Nutzerführungs-Vereinfachung später durch nur eine regulär sichtbare Schaltfläche, den anderen Aufruf als vorhandenen Kompatibilitätspfad bewahren.
- Die von PSERC in `start()` gebundene `PSTE_Context_Refresh`-Abhängigkeit kann den Status `COMPLETE` haben, während die **heutige** `PSTE_Snapshot::editorialPlan()`-Prüfsumme bereits abweicht. Vorher wurde dieser Zustand erst in `tickActivate()` gesperrt; dadurch unnötige komplette Compilerarbeit und Verwirrung. Screenshot: `BLOCKED / ACTIVATE / PSERC_PLAN_LIVE_EDITORIAL_PLAN_CHANGED_BEFORE_ACTIVATE`.
- Schutzsperre gegen tatsächliche Planänderung ist **notwendig**. Es ist **nicht** bewiesen, welche Zeile/Option im echten TEST-WordPress abweicht. Keinen Planwert raten oder überschreiben.
- Tatsächlich bereits in der originalen PSERC-0.28.55-Testfassung lokal durchlaufen: 7 positive/negative K0-Dateiformat-/Quelltests PASS, 5 Datenfelder pro Artikel; **nicht** der echte 1-READY-WordPress-K0-Download.

## Isolierte, kleinste Codeänderung als QA (NICHT installieren)
Original unverändertes Plugin `PSERC-0.28.55-TEST.zip` direkt aus privatem Pluginbüro, nur in `PSERC_Plan_Compile_Job::start()` genau die **vorhandene** `PSERC_Plan_Dependency_Fingerprint::liveEditorialPlanMatches($dep)`-Prüfung **vor** Beginn einer Compiler-Generation zusätzlich aufrufen. Die **bestehende** ACTIVATE-Prüfung bleibt identisch. Kein zusätzlicher Worker/Importer/Algorithmus, keine neue Tabelle/Option/WordPress-Änderung. Ohne aktuelle Plandaten wird früh gestoppt, nicht automatisch freigegeben.

Quelländerung:
```diff
@@ PSERC_Plan_Compile_Job::start()
         if((string)($context['status']??'')!=='COMPLETE')return self::blockedView('PSERC_PLAN_PSTE_CONTEXT_NOT_COMPLETE');
+        // Reuse the EXISTING final plan freshness guard before any compile work.
+        // The same guard remains at ACTIVATE; do not rewrite or bypass either binding.
+        if(!PSERC_Plan_Dependency_Fingerprint::liveEditorialPlanMatches($dep))return self::blockedView('PSERC_PLAN_LIVE_EDITORIAL_PLAN_CHANGED_BEFORE_START');
         $active=PSERC_Plan_Snapshot_Store::getActive();
```

Unverändert: `PSERC_Plan_Compile_Job::tickActivate`, `PSERC_Plan_Dependency_Fingerprint`, bestehende K0-Ausgabe, Redaktionspläne, PSTE, PPM und alle Daten/Produktion. Paketversion `0.28.57-same-guard-early-stop` ausschließlich QA. **Die frühere QA .56 wird nicht vorausgesetzt oder übernommen.**

## Abnahme bisher
- **Alle 63 ZIP-Einträge identisch**, nur Original-Compile-Job, Original-Version und Original-Integritätsmanifest verändert.
- **43/43 PHP-Syntaxchecks PASS**, ZIP CRC PASS.
- Original `PSERC_Package_Integrity::validate()` auf entpackter QA .57: `PSERC_COMPILER_PACKAGE_INTEGRITY_PASS`, **61/61 Dateien gebunden**.
- Echte PHP-Startfunktion mit kontrollierten Quellen-Tests: **STALE** stoppt vor Lesen des aktiven Plans/Schreiboperation; **CURRENT** übernimmt vorhandenen aktiven Plan weiter unverändert; **PENDING** behält bisherigen Stopp. **3/3 PASS.**
- Original-Export/Boundary-Regression .55 **7/7 PASS**; keine Exportcode-Änderung im QA-Paket.
- QA-ZIP dauerhaft **nur in privater Bibliothek**: `/pferdeatelier/PLUGINS/QA/PSERC-0.28.57-KISS-FRUEHER-PLANSTOP-NUR-QA-NICHT-INSTALLIEREN.zip`, SHA256 `c0c5d5dd5ad5aa91bcf0652d85889c1fe711cffc59b1c05ac05a090dc4965edd`.
- **KEIN** realer gemeinsamer WordPress-Test, kein K0-Handoff >=1 READY und deshalb **keine Installations-/Releasefreigabe**.

## Konkrete nächste Prüfung (keine alten Schleifen)
1. Aus **TEST-WordPress** den bereits gespeicherten `PSTE_CONTEXT_JOB.final_plan_sha256` und **nur lesend** den aktuellen `PSTE_Snapshot::editorialPlan().sha256` vergleichen; bei Abweichung die vorhandene Redaktionsplanquelle/deren Status feststellen. Unverändert erhalten, nicht per Änderung überspielen. Ohne diesen echten WP-Beleg keine Ursache behaupten.
2. Danach denselben bereits freigegebenen Kandidaten in PSERC-Reader bis `READY_FOR_METADATA_HANDOFF` kontrollieren, originale V2-Datei mit 5 Feldern herunterladen und gegen K0-Eingangsvertrag testen, **ohne Artikelproduktion**.
3. **Erst danach** Backend-Navigation vereinheitlichen und statisch/dynamisch gegen Hook-, Option-, Cron-, CLI- und gespeicherte Archivverweise beweisbar toten Code entfernen. Keine Funktionen/Daten/Recherchen löschen.
