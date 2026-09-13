# SYSTEM 4A — MINIMALER EXTERNER SUPERVISOR

## Zweck

Ein einziger äußerer Supervisor ist die einzige Laufzeitautorität. Codex/Worker besitzt weder State noch Route noch PASS.

## Eine Tür

Der produktive Einstieg darf **nicht** `FullChainSupervisor.run_full(..., worker_callable, ...)` sein.

Dieser direkte Callable-Weg ist seit 2026-09-13 im Produktionsmodus fail-closed mit:

`PRODUCTION_REQUIRES_EXTERNAL_SUPERVISOR_HOST`

Zulässiges Ziel ist ausschließlich:

`EXTERNAL HOST -> narrow worker transport -> isolated worker -> existing read-only checkers -> exact V2 handoff`

Kein produktiver Aufrufer und kein Worker darf einzelne Phasen setzen oder finalisieren.

## Interner Ablauf

`Snapshot prüfen -> Kapseln erzeugen -> Research -> Research-Guard -> Facts -> Facts-Guard -> Production Context -> Context-Bindung -> Draft -> Content/Design -> echter FULL-Check -> ggf. Same-Article-Repair -> FULL-Check -> Batch/Querschnitt -> exakter V2-Handoff -> Parent-Chat-Roundtrip -> Readback/Hash`

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

Produktiv muss der Worker außerhalb der Supervisor-Autorität laufen. Mindestgrenze:
- getrennte OS-/Service-Autorität oder gleichwertig harte externe Session-Grenze;
- Supervisor-State und Authority-Key für Worker nicht lesbar und nicht schreibbar;
- Worker kann Supervisorprozess/-service nicht ersetzen;
- Workerraum enthält keinen schreibbaren Supervisor-State und keine zweite Route;
- Protokoll akzeptiert ausschließlich den erwarteten Arbeitsinhalt; Phase/PASS/Publish-Injektion wird blockiert.

`os_boundary_acceptance.py` prüft diese Eigenschaft lokal als separaten Autoritätsbeweis. Er ersetzt nicht den vollständigen Produktions-E2E.

## Produktionsmodus

Produktionsmodus akzeptiert ausschließlich den realen `System4ReadOnlyChecks`-Backendweg. Kein Fake-Backend, kein synthetischer FULL-PASS, kein `mock.patch` auf:
- `production_checks.run_all`;
- LanguageTool 6.8;
- PPM 6.7.9.

Fehlt die exakte LT-/PPM-Abhängigkeit: fail-closed BLOCKED, niemals PASS.

Bis der externe Host tatsächlich gebunden und vollständig geprüft ist, gibt es **keinen zulässigen produktiven 4A-Startweg**.

## Testmodus

Ein expliziter Testmodus darf kontrollierte Worker/Checker verwenden, aber sein Ergebnis heißt ausschließlich **ARCHITECTURE E2E**, nie Produktions-E2E.

## Ausgang

Kein neuer WordPress-Vertrag.

Final ausschließlich:
`SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`

Der bestehende `handoff_transport` validiert und kanonisiert die Datei. Danach müssen Parent-Chat-Transport, Rekonstruktion, erneute Validierung und Byte-/SHA256-Readback dieselbe Datei bestätigen.

## Abbruchregel

Wenn diese Form nicht mit genau einem äußeren Supervisor realisierbar ist oder neue Signer-/Token-/Room-/Receipt-/Package-Kaskaden braucht: 4A stoppen.
