# Pferdeatelier – IST-Simulation mit realen Methoden, 11.11.2026

## Scope
**Getestet wurden tatsächlich ausgeführte PHP-Funktionen** aus PSTE **0.57.144.40** / PSERC **0.28.67** auf der lokalen Testumgebung. Die WordPress-/DB-/Provider-Anbindungen wurden als **in-memory-Attrappen** ersetzt. **Kein** echter WordPress-End-to-End-Lauf, keine Artikelproduktion, keine Datenbankänderung, keine Provider-Aufrufe. Keine Pluginänderung.

### Echter Admin-Endpunkt `PSTE_Admin::productionAutoStepAjax()`
- Fehlender gültiger Bestands-Audit → **ERROR 400 `PSTE_AUTOMATIK_NO_FULL_BACKLOG_REPLAY_USE_SHORTPATH`**. 0 alte Queue-Starts, 0 neues Keyword, 0 Plan-Starts, 0 Provider-Anfragen.
- Alte `existing_only`-Queue RUNNING → **ERROR 400 `PSTE_AUTOMATIK_NO_FULL_BACKLOG_REPLAY_USE_SHORTPATH`**, 0 Queue-Fortsetzung. Schutz vor neuem 5.000er-Lauf **PASS**, Automatiknutzbarkeit **FAIL**.
- Gültiger Audit, 0 Freigaben → simulierter Compiler lehnt ab mit `PSERC_PLAN_NO_SOURCE_TOPICS_PRESERVE_PRIOR_SNAPSHOT`. Automatiknutzbarkeit **FAIL**. Hier wurde der PSERC-Compiler als Dummy-Antwort modelliert; Ergebnis kein echter Compiler-End-to-End-Test.
- Gültiger Audit, simulierte Compilerannahme → Admin ruft vorhandenen Plan-Start auf, meldet SUCCESS. **Nur Verbindungstest**, nicht nachgewiesene READY-Ausgabe.

### Getrennter echter Keyword-Start-Endpunkt `PSTE_Admin::researchStartAjax()`
Mit Kategorie 123, Keyword `Regendecken Pferde Passform`, ausdrücklich simuliertem `confirm_cost=1`: echte Handler-Funktion ruft `PSTE_Research_Job::start` genau 1x und `PSTE_Research_Driver::kick` genau 1x auf. Diese beiden Worker wurden **gemockt**; keine echte Recherche, keine Kosten, kein gespeicherter WordPress-Job. **Startverdrahtung PASS**, tatsächliche Keyword→Titel-Qualität **UNGETESTET**.

### Tatsächliche Worker-Methode `PSTE_Research_Driver::executeOneStep()`
- `child.status=BLOCKED_PENDING_PARK` → `[true,0,"CHILD_PARKED_CONTINUE|CHILD_X"]`; `parkBlockedCurrentAndContinue` 1x aufgerufen. **Fehlerisolierung an diesem Übergang PASS**. Keine Behauptung, dass jeder Fehlerzustand im System isoliert ist.
- `PSTE_Research_Job` RUNNING, simuliertes COMPLETE → `[false,0,"SINGLE_COMPLETE"]`; advance 1x. **Worker-Abschlussverdrahtung PASS**.

### Bereits vorhandene echte Tests nochmals ausgeführt
- `test_no_5k_autoresume.php`: PASS – gespeicherter `existing_only`-Job nicht neu gestartet/fortgesetzt.
- `test_empty_never_activated.php`: PASS – 0 READY aktiviert keinen neuen aktiven PSERC-Plan.
- `test_three_original.php`: PASS – 3 gesicherte frühere signierte fünfteilige Metadaten/READY-IDs nachweisbar, kein aktueller WP-READY-Status.

## Ergebnis / Fehlerabgrenzung
**Bereits richtig**: Einzelkind-Fehler parken und weiter, keine automatische Wiederholung des alten 5.000er-Audits, kein leeres Plan-Activate. Diese Punkte **nicht erneut umbauen**.

**Nicht funktionsfähig belegt**: Der Knopf `Automatik` in `.40` stoppt bei fehlendem alten Audit explizit mit `USE_SHORTPATH`; er startet **selbst kein neues Keyword**. Der separate echte `researchStartAjax` unterstützt einen Keyword-Start, aber die Verbindung von diesem Job zur PSERC-Planfreigabe/Metadatenexport/K0 wurde nicht end-to-end ausgeführt. Ein Erfolg des getrennten Keyword-Start-Handlers beweist **keinen** erfolgreichen Gesamtworkflow.

**Sparsame nächste Maßnahme**: Vor jeder produktiven Version den bereits vorhandenen Keyword-Rechercheweg samt anschließender PSERC-Übergabe in einer **isolierten WordPress-Testinstallation** als eine komplette Probe ausführen; Audit-Neustart ausdrücklich verboten. Kein neuer Worker, keine neue DB-Regel, kein 5.013er-Durchlauf, keine weiteren abstrakten Doppelprüfungen. Wenn die bestehende Automatik statt neuem Keyword nur bestätigte Bestandsquellen verarbeiten darf, muss diese Funktion klar benannt sein, statt irreführend „Keyword bis Export“ zu versprechen.

**Diese Simulation hat den vollständigen Produktionszielvertrag ausdrücklich NICHT bestanden.** Ein neues Plugin wird deshalb nicht freigegeben.
