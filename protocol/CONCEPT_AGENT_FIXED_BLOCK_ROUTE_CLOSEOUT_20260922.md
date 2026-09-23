# Concept Agent – Fixed Block Route Closeout – 2026-09-22

Status: Historie/Nachweis, keine CURRENT-Autorität.

## WAS

Die bestehende Concept-Agent-Steuerung wurde nur an einem Punkt geschlossen:
- fehlender exakter Cross-Chat-Transport -> fest gebundene Aktion `RESTART_BATCH_FROM_INTAKE`;
- Transport-Hash-/Binding-Abweichung -> `TERMINAL_SECURITY_BLOCK`;
- der Chat darf keine Folgeaktion wählen;
- keine Rekonstruktion des fehlenden Transports.

Keine Änderung an Fachworkflow, LanguageTool 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL, Plugins oder Qualitätsregeln.

## WARUM

Der vorherige Zustand konnte nach einem korrekten Hardlock-BLOCK wieder Entscheidungsfreiheit an den Chat zurückgeben. Das widersprach dem Ziel, dass der Chat nur den Eingang auslöst und GitHub die einzige zulässige Folgeaktion vorgibt.

## NACHWEIS

- GitHub Actions Run 35770259944: PASS.
- 1 Artikel: vorhandener Transport -> Produktion bis genau eine Finaldatei PASS.
- 3 Artikel: vorhandener Transport -> Produktion bis genau eine Finaldatei PASS; Reparaturschleife 1/2/1 bewiesen.
- 1 Artikel: fehlender Transport -> fester Neustart ab INTAKE -> genau eine Finaldatei PASS.
- 3 Artikel: fehlender Transport -> fester Neustart ab INTAKE -> genau eine Finaldatei PASS.
- Negativ 1 und 3 Artikel: manipulierte Transportdatei -> TERMINAL_SECURITY_BLOCK.
- Proof SHA-256: `36318454d7ff5d01908a3c9727cc8ef6bdf09dc6ce5f7940dea614d1c90cce2f`.
- Aktueller realer 16er-Einstieg Run 35770433508: Eingang bis ARTICLE_PRODUCTION validiert; fehlender exakter Transport erkannt; feste Aktion `RESTART_BATCH_FROM_INTAKE`; keine Chat-Entscheidung.

Die aktuelle Wahrheit für Eingang/Re-Entry/Folgeaktion bleibt ausschließlich:
`concept-agent/production-control:concept_agent/CONTROL_STATE.json`.

## OFFENER PUNKT AUS ABSCHLUSSPRÜFUNG

Der echte GitHub-Workflow führt die fest gewählte Aktion `RESTART_BATCH_FROM_INTAKE` derzeit noch **nicht selbst aus**. Er erzeugt `CONCEPT_AGENT_RESTART_REQUIRED_V1.json` und beendet den Lauf mit Exit 20. Damit ist die Entscheidungsfreiheit des Chats beseitigt, aber der automatische Neustart im produktiven Workflow noch nicht vollständig verdrahtet.

Erster offener Blocker: `FIXED_RESTART_ACTION_NOT_EXECUTED`.

Exakt nächste Arbeit: Die bereits gewählte Restart-Aktion im bestehenden GitHub-Workflow ausführbar verdrahten und danach denselben 1-/Mehrartikel-Positiv-/Negativtest sowie den realen 16er-Einstieg erneut fahren.


## NACHHOLPRÜFUNG / DELTA 2026-09-23

Status dieses Abschnitts: Historie/Nachweis, keine CURRENT-Autorität.

### WAS TATSÄCHLICH GEÄNDERT WURDE

- Die vom Chat bereitgestellte autoritative PSERC-Metadaten-Datei wurde bytegenau als `concept_agent/current/PSERC_METADATA_SNAPSHOT.json` auf `concept-agent/production-control` gebunden.
- Exakte Dateigröße: 44.209 Bytes.
- Exakte SHA-256: `3ac8a725f3e7ebb8a6e332b07e88b989e508e05fe9aa29260aaca6f9bedfc761`.
- Batch: `df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0`, 16 Artikel.
- Snapshot-Bindungscommit: `5c7182a63705e5955cd6b7b4d44e992cc55ef318`.
- Danach wurde ausschließlich über den autoritativen Concept-Agent-Eingang ein neuer `run-current` ausgelöst: Request-Commit `c1eadf85edb361ac54c704d55aa2f24b6be8df99`.
- Autoritativer Control-Run `35824073396`: SUCCESS.

### WAS DER AKTUELLE REALE LAUF BEWIESEN HAT

Der Lauf `35824073396` prüfte wieder ab Stage 0 und bestätigte:
- INTAKE: PASS;
- RESEARCH: PASS;
- RESEARCH_BOUND: PASS;
- AUTHORING_BOUND: PASS;
- nächste fachlich gebundene Stufe: ARTICLE_PRODUCTION, Artikelindex 0;
- fehlender historischer Cross-Chat-Transport -> fest gebundene Aktion `RESTART_BATCH_FROM_INTAKE`;
- Restart-Intake mit dem bytegenau gebundenen aktuellen Snapshot -> `CONCEPT_AGENT_INTAKE_READY`, 16/16 PASS;
- danach stoppt die produktive Control-YAML weiterhin bei `PREPARE_INTAKE_ONLY`.

### FEHLERPROTOKOLL

1. `AUTHORITATIVE_PSERC_EXACT_FIVE_INTAKE_SOURCE_NOT_DURABLY_BOUND`
   - Status: RESOLVED.
   - Behebung: bytegenaue dauerhafte Snapshot-Bindung, Commit `5c7182a63705e5955cd6b7b4d44e992cc55ef318`.
   - Beweis: Control-Run `35824073396` akzeptiert denselben 16er-Batch im Restart-Intake.

2. `FIXED_RESTART_ACTION_NOT_EXECUTED`
   - Status: SUPERSEDED / TEILWEISE BEHOBEN.
   - Der Restart wird inzwischen tatsächlich ausgeführt und erreicht `CONCEPT_AGENT_INTAKE_READY`.
   - Der frühere Protokolltext „RESTART_REQUIRED schreiben und Exit 20“ ist daher nicht mehr der aktuelle Fehler.

3. `PRODUCTIVE_FRESH_BATCH_EXECUTOR_FROM_INTAKE_NOT_PRESENT`
   - Status: OPEN / FIRST BLOCKER.
   - Konkreter Ist-Fehler: Nach erfolgreichem Restart-Intake endet `.github/workflows/concept-agent-production.yml` bei `PREPARE_INTAKE_ONLY`.
   - Es ist dort keine produktive Fortsetzung durch den bestehenden Research-/Authoring-Weg in den bestehenden Concept-Agent-Runner gebunden.

4. Falscher historischer System4/Parent-Startversuch
   - Status: ROLLED BACK / NICHT CURRENT.
   - Der Versuch lief in einen alten Pre-Codex-Hardlock und wurde zurückgenommen.
   - Keine aktuelle NEXT ACTION und keine autoritative Produktionsroute.

### TESTNACHWEISE DIE NICHT ALS CURRENT DIENEN

- Isolierter Blackbox-/Re-Entry-Nachweis: 1 Artikel und 3 Artikel, Positiv/Negativ und Chatwechsel/Abbruch wurden geprüft.
- Realer Produktionskern mit LanguageTool 6.8 und PPM 6.7.9: Acceptance-Run `35791815469` PASS.
- Diese Evidence belegt Teilstrecken und Fehlergrenzen, ersetzt aber nicht den noch ausstehenden EINEN realen durchgehenden Control-Lauf vom Chat-Snapshot bis zur finalen Datei.

### CURRENT / NEXT ACTION

Keine Statuswahrheit in diesem Protokoll ableiten.

Einzige Current-Autorität:
`concept-agent/production-control:concept_agent/CONTROL_STATE.json`.

Dortiger nachgeholter Stand:
- Current-Update-Commit: `bf528a17a1227e8c04ade631f85cdc39fe58c363`;
- erster offener Blocker: `PRODUCTIVE_FRESH_BATCH_EXECUTOR_FROM_INTAKE_NOT_PRESENT`;
- genau eine NEXT ACTION: ausschließlich den `PREPARE_INTAKE_ONLY`-STOP nach erfolgreichem Restart-Intake an die produktive bestehende Fortsetzung anbinden; danach denselben unveränderten echten End-to-End-Test von Chat-Datei bis genau einer finalen Datei erneut ausführen.
