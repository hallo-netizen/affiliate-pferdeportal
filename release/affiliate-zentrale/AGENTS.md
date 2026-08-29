# Affiliate-Zentrale – verbindlicher Release-Hardlock

Für jede Arbeit an der Affiliate-Zentrale gilt zusätzlich zum Root-`AGENTS.md`:

1. **Zuerst** `control/release-governance/CURRENT_RELEASE.json` lesen und anschließend `python3 control/release-governance/release_guard.py start --branch "$(git branch --show-current)"` ausführen. Bei BLOCKED: stoppen, nicht rekonstruieren, nicht ausweichen.
2. Einzige Arbeitsquelle ist `release/affiliate-zentrale/current/CURRENT_WORKING_SOURCE.b64/` (direkte Base64-Abbildung der exakten ZIP-Bytes). Alte Branches, `affiliate-portal-router/`, `CI_V*`, `STAGING_V*`, Chat-Dateien und historische Pluginbäume sind **keine** Releasequelle.
3. Release-Arbeit ausschließlich auf `affiliate-release-current`. Keine Versions-, Staging-, Probe-, Rekonstruktions- oder Nebenbranches.
4. Die beiden historischen Referenzartefakte unter `archive/artifacts/` sind immutable: V6.62.0 = freigegebene Basis; V6.63.4 = gebundener Negativfall. Sie dürfen weder ersetzt noch neu erzeugt werden.
5. `CURRENT_WORKING_SOURCE.b64/` darf nur zusammen mit einem dazu bytegenau passenden `CURRENT_SOURCE_SHA256.txt` geändert werden. Keine Änderung außerhalb des erlaubten Scopes.
6. Keine Nebenrefactorings. Nur der gebundene Auftrag.
7. Keine Release-ZIP erzeugen oder als installierbar bezeichnen, solange `release_allowed=false` oder auch nur ein `required_release_gates`-Eintrag nicht `PASS` ist.
8. Jeder PASS muss mit einer hashgebundenen Evidence-Datei unter `release/affiliate-zentrale/evidence/` belegt sein.
9. Vor einem Release muss `python3 control/release-governance/release_guard.py release-check` PASS liefern. Ein Ergebnis ohne diesen PASS ist nicht freigegeben.
