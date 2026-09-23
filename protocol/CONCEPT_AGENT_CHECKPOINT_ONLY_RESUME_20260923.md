# Concept Agent — Checkpoint-only Resume 2026-09-23

Ziel: Unterbrechung und Wiedereinstieg dürfen keinen freien Produktionsweg öffnen.

Umgesetzt:
- Nach MACHINE_READY desselben Batches kein zweiter text-start.
- Fortsetzung nur mit exakt gültigem Produktionscheckpoint.
- Checkpoint bindet genau eine allowed_action.
- Fehlt Checkpoint oder stimmen Batch, Binding, Hash oder allowed_action nicht exakt: STOP.
- Bereits vorhandene Artikel dürfen nicht als kompletter Batch nachträglich angehängt werden.
- Nur genau der vom Checkpoint freigegebene Artikel darf in die Produktion eintreten.
- LT 6.8 bleibt vor PPM 6.7.9.
- Reparatur bleibt beim selben Artikel und beginnt danach wieder bei LT 6.8.
- Nach vollständigem LT/PPM-PASS ist die nächste gebundene Aktion PSERC.
- Kein Publish.
- isolated_system4, Workflows, Qualitätsregeln, LT, PPM, PSERC und ENDSTEMPEL bleiben unverändert.
