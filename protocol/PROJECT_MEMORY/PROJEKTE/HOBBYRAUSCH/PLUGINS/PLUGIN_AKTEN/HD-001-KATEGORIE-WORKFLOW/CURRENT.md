# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-28
STATUS: V1.9.0 STAGE HARDLOCK LOKAL POSITIV/NEGATIV PASS / LIVE-ROLLBACK + RETEST OFFEN

## Live-Befund V1.8.9

Nach Übernahme des vorbereiteten READ_ONLY_PREVIEW zeigte WordPress unerwartet:
- Stage: `Deployment abgeschlossen`;
- `Schreiben und Readback erfolgreich`;
- URL-Meldung `apkw_msg=deployed`.

Dieser Zustand darf aus einem READ_ONLY_PREVIEW-Import allein nicht erreichbar sein.

## Code-Ursache

Zwei reale Lücken im Guided Flow:
1. `workspace_next` prüfte serverseitig nicht bei jedem POST, ob der angeforderte Schritt exakt zur aktuellen Stage gehört. Ein veralteter/staler späterer POST konnte daher bei noch vorhandenen Downstream-Artefakten prinzipiell weiterlaufen.
2. Beim Ersetzen eines früheren Arbeitsstands wurden abhängige spätere Pakete (`final`, `deploy_plan` usw.) nicht konsequent invalidiert.

Damit war der UI-Ablauf zwar geführt, aber der Serverpfad noch nicht hart genug an die aktuelle Stage gebunden.

## Fix V1.9.0

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.9.0 Hobby Depot Stage Hardlock`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.0_HOBBY_DEPOT_STAGE_HARDLOCK.zip`

Installer SHA-256:
`79d914e6896c36c0022dbae25c7c3ec24923dc453eadc499ef6cd1b88fcd83a1`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.0_HOBBY_DEPOT_STAGE_HARDLOCK.zip`

Source SHA-256:
`b63fbedaf4a474923ce6946cafec45faa5ebcea4de36cd534dd9c546d089c3c9`

Neu:
- jeder Guided-POST hat serverseitigen exakten Stage-Guard;
- stale/alter POST für einen späteren Schritt wird BLOCKED;
- neuer/korrigierter Upstream-Stand invalidiert alle davon abhängigen Downstream-Pakete und alte Deployment-Metadaten;
- READ_ONLY_PREVIEW-Import entfernt stale `FINAL_APPROVED` und `deploy_plan`;
- während eines aktiven Deployment-Runs ist ein neuer Upstream-Import BLOCKED, bis Rollback erfolgt;
- persistente DataForSEO-Verbindung und der vereinfachte Guided Flow bleiben unverändert.

## Lokale harte Prüfung vor Live-Abnahme

- Source Vollsuite: 241/241 PASS;
- Fresh-Unpack-Installer: 241/241 PASS;
- Source PHP-Lint: 18/18 PASS;
- Installer Runtime PHP-Lint: 17/17 PASS;
- Runtime-Parität Source↔Installer: 22/22 byteidentisch.

Gezielte Positiv-/Negativtests:
- exakt aktuelle Stage → nächster Schritt erlaubt;
- stale Deployment-Aktion bei `structure_ready` → BLOCKED;
- neuer READ_ONLY_PREVIEW bei stale Final-/Deployment-Plan → Downstream entfernt, Stage bleibt `structure_ready`;
- aktiver Deployment-Run + neuer/korrigierter Upstream-Import → BLOCKED bis Rollback;
- bestehende Persistenz-/Verbindungs-/Review-Negativtests weiterhin PASS.

## Live-Status

V1.8.9 ist aktuell live und zeigt einen bereits ausgeführten Test-Deployment-Run.
Dieser Testbestand muss über den vorhandenen Rollback sauber zurückgesetzt werden.

V1.9.0 ist lokal geprüft, aber noch NICHT live abgenommen.

## NEXT ACTION

V1.9.0 über V1.8.9 installieren. Der persistente Live-Stand muss danach weiterhin `deployed` anzeigen. Dann den aktuell angezeigten Testlauf ausdrücklich vollständig zurückrollen. Erst danach READ_ONLY_PREVIEW erneut übernehmen und beweisen, dass exakt `structure_ready` / finale Prüfung erscheint und kein automatischer oder staler Deployment-Sprung mehr möglich ist.
