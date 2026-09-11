# TEMPORÄRE PR237-HOBBYRAUM-WERKBANK

Diese Datei gilt ausschließlich auf `hobbyroom/107007-restore-fach-plan-header-kiss-20260911` und wird vor dem Merge bytegenau auf Main-Stand zurückgesetzt.

1. Dies ist ausschließlich ein isolierter Code-Reparaturjob. KEIN Produktionslauf.
2. NICHT `control/cloud-entry-gate/cloud_entry.py start`, NICHT `runtime_entry_gate.py`, KEIN Receipt, KEIN 107007-Lauf.
3. Erlaubter Arbeitsumfang ausschließlich:
   - `control/single-door-boundary/codex_current_action.py`
   - `control/startmaster0107/fachworkflow_proof_handoff.py`
   - `control/startmaster0107/test_fachworkflow_proof_handoff.py`
   - `control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py` nur notwendige Regressionassertion
   - mechanische Hashkette `STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json`, `CURRENT_STATE.json`, `PFERDE_ATELIER_START_HERE.json`
   - Löschen aller `control/startmaster0107/.tmp_pr237_anchor*`
4. H8, Textmaschine, Fachregeln, PPM, PSERC, PSTE, LanguageTool-Regeln, SEO, Links, Tabellen, Design, Publish-Sicherheit, Cloud Entry, Runner/Gates/Contracts/Executor NICHT ändern.
5. `production_plan_header` muss aktueller Fachworkflow-Rohkontext sein; exakt `production_plan_v4`, dict/nichtleer, ohne `items`. Kein Ersatzwert, kein `production_plan_v5`, kein hardcodiertes `required_plugin_version`.
6. Worker-PASS-Autorität bleibt NONE; `stage_proofs=[]` bleibt zwingend.
7. Danach nur bestehende Code-/Repo-Tests ausführen, committen und auf diesen Branch pushen. NICHT mergen, KEIN Livetest.
