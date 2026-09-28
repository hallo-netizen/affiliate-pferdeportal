# K8 Verbot Live-Start Evidence — 2026-09-28

Zweck: ausschließlich Trigger/Evidence für den bestehenden Deterministic Entrance Gate.

- bestehender text-start Workflow unverändert
- bestehender Produktions-/Artikelworkflow unverändert
- LT 6.8 unverändert
- PPM 6.7.9 unverändert
- PSERC unverändert
- ENDSTEMPEL unverändert
- Recovery unverändert
- publish_allowed=false unverändert
- K8 ändert ausschließlich die Live-Handoff-Bindung hinter dem bestehenden intake_bridge auf die bereits getestete Single-Gate-Verbotslogik
- falscher, fehlender oder stale Befehl: keine Zustandsänderung
- richtiger aktueller Befehl: vorhandener progress_guard-Weg
- keine Current-/NEXT-ACTION-Autorität
