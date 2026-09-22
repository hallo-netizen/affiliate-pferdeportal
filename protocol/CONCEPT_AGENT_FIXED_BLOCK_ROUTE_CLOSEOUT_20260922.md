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
