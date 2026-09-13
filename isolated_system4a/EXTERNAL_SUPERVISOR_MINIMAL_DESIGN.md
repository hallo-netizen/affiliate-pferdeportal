# SYSTEM 4A — MINIMALER EXTERNER SUPERVISOR

## Zweck

Ein einziger äußerer Supervisor ist die einzige Laufzeitautorität. Der Worker besitzt weder State noch Route noch PASS.

## Eine Tür

Der produktive Einstieg darf **nicht** `FullChainSupervisor.run_full(..., worker_callable, ...)` sein.

Dieser direkte Callable-Weg ist im Produktionsmodus fail-closed mit:

`PRODUCTION_REQUIRES_EXTERNAL_SUPERVISOR_HOST`

Der bewiesene Produktionsweg ist:

`gebundener Rohinput -> realcase_production_entry.py -> ExternalSupervisorHost(mode='production') -> Cross-UID Worker -> vorhandene System-4-Prüfer -> exakter V2-Handoff -> Parent-Chat-Readback`

Kein produktiver Aufrufer und kein Worker darf einzelne Phasen setzen oder finalisieren.

## Interner Ablauf

`Snapshot prüfen -> Ingress binden -> Research -> Research-Guard -> Facts -> Facts-Guard -> Production Context -> Supervisor-Bindung -> Draft -> Content/Design -> echter FULL-Check -> Same-Article-Repair falls erforderlich -> erneuter FULL-Check -> Batch/Querschnitt -> exakter V2-Handoff -> Parent-Chat-Roundtrip -> Readback/Hash`

## Autoritäten

Supervisor besitzt exklusiv:
- State;
- Phase;
- Route;
- Resume;
- Authority-Key;
- PASS-Verwendung;
- finalen Ausgang.

Worker darf ausschließlich den Inhalt des gerade erlaubten Arbeitsauftrags liefern.

Prüfer bleiben die bestehenden System-4-Prüfer read-only.

## Technische Trennung

Produktiv läuft der Worker außerhalb der Supervisor-Autorität:
- Cross-UID-Prozess;
- Supervisor-State und Authority-Key für Worker nicht schreibbar;
- Worker kann keine Phase/PASS/Publish-Autorität zurückgeben;
- Workerraum enthält keinen schreibbaren Supervisor-State und keine zweite Route;
- Protokoll akzeptiert ausschließlich den erwarteten Arbeitsinhalt.

## Produktionsmodus

Produktionsmodus akzeptiert ausschließlich den realen `System4ReadOnlyChecks`-Backendweg. Kein Fake-Backend, kein synthetischer FULL-PASS, kein `mock.patch` auf:
- `production_checks.run_all`;
- LanguageTool 6.8;
- PPM 6.7.9.

Fehlt eine exakte gebundene Abhängigkeit oder weicht ihr Hash ab: fail-closed BLOCKED.

Der externe Host ist im aktuellen No-Codex-Produktionsvertrag vollständig gebunden und zweimal Null-bis-Ende reproduziert worden. Beide Läufe erzeugen dieselbe finale Datei bytegleich und feldgleich; Parent-Chat-Rekonstruktion ist jeweils bytegleich zur Enddatei.

## Testmodus

Ein expliziter Testmodus darf kontrollierte Worker/Checker verwenden, aber sein Ergebnis heißt ausschließlich **ARCHITECTURE E2E**, nie Produktions-E2E.

## Ausgang

Kein neuer WordPress-Vertrag.

Final ausschließlich:
`SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`

Der bestehende `handoff_transport` validiert und kanonisiert die Datei. Danach müssen Parent-Chat-Transport, Rekonstruktion, erneute Validierung und Byte-/SHA256-Readback dieselbe Datei bestätigen.

## Gültigkeitsregel

Der aktuelle PASS gilt nur für exakt gebundene Vertrags- und Produktionsbytes. Jede Änderung erzwingt erneut den kompletten Fehlerhistorien-Regressionslauf, positiven und negativen Null-bis-Ende-Lauf sowie den Byte-/Feldgleichheitsbeweis.

Kein Merge. Kein Publish. Kein Codex-Lauf ohne ausdrückliche User-Freigabe mit `Starte Codex`.
