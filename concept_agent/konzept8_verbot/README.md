# K8 Verbot

Eigenständige Arbeitskopie des letzten K7-Working-Copy-Standes vor dem GitHub-Regisseur.

- Quelle: `konzept7/working-copy-20260927`
- K7-GitHub-Freeze: `archive/k7-github-frozen-20260928`
- K8-Baseline: `konzept8-verbot/baseline-20260928`
- K8-Arbeit: `konzept8-verbot/working-copy-20260928`

## Einzige neue Idee

Vor die bestehende K7-Fortsetzung kommt genau eine Schleuse.

- exakt der aktuelle checkpointgebundene Befehl: darf passieren;
- jeder andere, fehlende, alte oder erweiterte Befehl: keine Zustandsänderung;
- derselbe Checkpoint und dieselbe NEXT ACTION bleiben gültig;
- beschädigter Current/Checkpoint: harter STOP statt Raten;
- der bestehende K7-Workflow und seine Qualitätsprüfungen bleiben unverändert.

Die Schleuse selbst erzeugt keinen neuen Fachschritt und entscheidet keine Inhalte oder Qualität.
