# TEMPORÄRE SYSTEM-3-CODEX-WERKBANK

Diese Regeln gelten ausschließlich auf dem Testbranch `hobbyroom/system3-codex-proven-path-v1`.

1. Keine bestehende Produktions-, STARTMASTER-, ACM-, Zickzack-, PPM-, PSERC-, PSTE-, WordPress- oder andere Projektlogik ausführen oder verändern.
2. Ausschließlich `isolated_system3/**` bearbeiten.
3. Erster Befehl zwingend: `python3 isolated_system3/cloud_entry.py start`.
4. Nur wenn dieser Befehl `SYSTEM3_CLOUD_ENTRY_PASS` meldet: `isolated_system3/codex_prompt.md` und `isolated_system3/live_fixture/wordpress_input.json` lesen und den Artikel als `isolated_system3/codex_output.md` erzeugen.
5. Keine andere Datei verändern.
6. Danach zwingend: `python3 isolated_system3/cloud_entry.py verify`.
7. Bei jedem FAIL sofort stoppen. Kein Fallback, keine Reparaturroute, keine freie Workflow-Navigation, kein Publish.
