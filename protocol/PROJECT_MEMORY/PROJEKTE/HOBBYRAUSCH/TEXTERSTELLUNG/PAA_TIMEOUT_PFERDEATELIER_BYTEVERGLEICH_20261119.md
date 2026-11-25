# 19.11.2026 – Originalvergleich PSTE_PAA_TASK_TIMEOUT (Hobby 0.4.24.5 vs. Pferdeatelier 0.4.23 und 0.4.31)

## Echtdiagnose / Screenshot
Original `texterstellung-diagnose-20261119-100006.json`: www.hobby-depot.de, Plugin 0.4.24.5; Original-Batch `COMPLETE` nur als **Queue-Endstatus**, `blocked_count=1`, Kind `3D-Bogenschießen` `BLOCKED_PARKED`, Fehler `PSTE_PAA_TASK_TIMEOUT`; **5 Rohkeywords, 0 redaktionell verwendbare Kandidaten**. Archivphase `QUESTIONS`/`TASK_PENDING`; `archived_paid_task_id_present=true`, `archived_provider_call_in_flight=false`. Start 09:26:51 UTC (19.11), Diagnose 10:00:06 UTC. DataForSEO-Zugangsdaten laut Diagnose vorhanden. Provider-Task-Fertigstatus und echter Gebührenbetrag NICHT in der Diagnose enthalten.

## Forensischer Bytevergleich direkt aus ZIPs
`Texterstellung_KISS_0.4.23_TEST_MINI_Anleitung_K0_KISS.zip` (archiviertes Pferdeatelier-Original), `Texterstellung_BLANKO_0.4.31.1_MINIMAL_NICHT_FREIGEGEBEN.zip` (laut Projektarchiv aus Original-Pferdeatelier 0.4.31 als minimal bereinigte Vorlage) und `Texterstellung_Hobbydepot_0.4.24.5_SANDBOX_LEERBESTAND_FIX.zip` wurden tatsächlich geöffnet. **Original-PHP Dateien in ALLEN DREI ZIPs byteidentisch**:
- `original/pste/includes/class-pste-research-job.php` SHA256 beginnend `d4b56c7047a4e9d222`
- `original/pste/includes/class-pste-research-driver.php` SHA256 beginnend `98bf53606b387065de`
- `original/pste/includes/class-pste-dataforseo-client.php` SHA256 beginnend `ffc0c299c443e8761b`.
Damit ist die gleiche TIMEOUT-Bedingung im Pferdeatelier-Original belegt, **nicht**, dass auf der echten Pferdeatelier-Live-Seite derselbe Abbruch beobachtet wurde.

## Exakte unveränderte Code-Reihenfolge
`PSTE_Research_Job::advanceQuestionsTask()` in allen drei Paketen:
1. `paa_task_id` vorhanden; wenn nicht, PAA-Auftrag mit `postPeopleAlsoAskTask()` anlegen und ID/Uhrzeit speichern.
2. **VOR** einer tatsächlichen Readiness-Prüfung folgt `time()-strtotime(paa_task_posted_at_utc)>1800`: setzt `PAUSED_ERROR` und `PSTE_PAA_TASK_TIMEOUT`.
3. Erst **danach** wird `PSTE_DataForSEO_Client::peopleAlsoAskTaskReady(taskId)` per read-only `GET /v3/serp/google/organic/tasks_ready` gerufen; nach READY `GET .../task_get/advanced/{taskId}`.
Zwingende Schlussfolgerung: nach 30 Minuten ab gespeicherter Auftragszeit kann auch ein bereits bereites Ergebnis nicht mehr abgerufen werden, weil die lokale Timeout-Prüfung zuerst stoppt. Der Fehlercode ist ein **lokaler Plugin-Zeitgrenzen-Code**; kein Nachweis eines DataForSEO-Fehlers. Ob der konkrete Task tatsächlich bereit war, bleibt ohne Providerstatus unbekannt.

**Immutabler Archivschutz:** `PSTE_Research_Archive::store` konserviert zuerst den Originalauftrag inklusive Task-ID, verifiziert dessen Integrität, parkt anschließend. **Nicht erneut starten** und keine zweite möglicherweise gebührenpflichtige Taskpost erzeugen, bevor derselbe persistierte Task rein lesend abgefragt werden kann. Für diesen bereits geparkten Auftrag fehlt bislang ein geprüfter Live-Wiederaufnahmeweg.

## Zusätzlich konkret falsche frühere Testanweisung
Im tatsächlich ausgelieferten `texterstellung.php` ist beim Start `txe_research_next` **`cost_ack` vorgeschrieben**, ansonsten `DATAFORSEO_KOSTEN_NICHT_BESTAETIGT`. Der Haken im Formular ist `required`. Eine „kostenlose Rechercheprobe mit Haken aus“ war deshalb **unmöglich**; frühere Empfehlung falsch. Ein auf dem Screenshot NACH dem Start ausgeschalteter Haken beweist nicht, welcher Wert beim Start verwendet wurde. Ein tatsächlicher Betrag ist nicht belegt.

## Freigabestatus
**Kein neuer Plugin-Build, keine Änderungen an K0/Multi, Kategorie/PSERC, keine Providerabfrage**. Das vorhandene Hobbydepot-Plugin `0.4.24.5` bleibt der unveränderte aktuelle Bürostand, nicht als Rechercheproduktionsfehler-frei deklarieren.
Sichere fachliche nächste Handlung: Einmalig anhand der **gespeicherten Task-ID** den Providerstatus nur lesend ermitteln, **ohne POST oder Neu-Recherche**. Danach in bestehender Original-PAA-Stelle das Verhältnis Readiness/Timeout korrigieren und den Original-Archivfall sicher rückführbar machen; vollständige Positiv-/Negativtests. **Keine neue ZIP**, bevor diese Einzelfehler tatsächlich nachgewiesen behoben sind.
Bericht im echten Pluginbüro und Fachbüro: `Texterstellung_0.4.24.5_PAA_TIMEOUT_ORIGINALVERGLEICH_20261119.md`.
