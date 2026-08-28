# Deterministic Entrance Gate V1

Diese Schicht ist absichtlich fachblind. Sie kennt keine Beitragsart, keine Titel-, Keyword-, Recherche-, Qualitäts-, Design-, PSTE-, PSERC-, PPM- oder LanguageTool-Regel.

Sie tut ausschließlich vier technische Dinge:
1. ROOT/CURRENT_STATE/Step-Bundle hashgebunden validieren.
2. Genau einen aktuellen Schritt als isolierte Execution Capsule ausgeben.
3. Einen Worker-Receipt nur für exakt dieses Ticket akzeptieren.
4. Jede Navigation, State-Schreibanforderung oder Workflowänderung des Workers verwerfen.

Fachlogik bleibt vollständig hinter der Tür. Neue Beitragsarten oder spätere Regeländerungen erfordern keine Änderung am Gate, solange der bestehende Workflow einen neuen Step/Bundle bindet.

`worker_harness.py` besitzt einen Codex-CLI-Modus ohne OpenAI-API-Key. Er ist als harter Ausführungsweg gedacht, sobald Codex lokal mit dem vorhandenen ChatGPT-Konto angemeldet ist. Der MASTER selbst benötigt dafür keinen API-Key und keine neue WordPress-Komponente.
