# Concept Agent – Pflichtcheck-Trigger für autoritativen Main-Eingang

Stand: 22.09.2026

Zweck dieser Datei ist ausschließlich, den bereits vorgeschriebenen GitHub-Pflichtcheck `hardlock` für PR #365 auf demselben Head wie `hardlock-base` auszulösen.

Geänderte Nutzlogik in PR #365:
- `concept_agent/CONTROL_ENTRY_POINTER.json`
- `concept_agent/START_HERE.md`

Scope:
- nur Navigation/Eingang für neue Chats und Fortsetzungen;
- keine Änderung des bestehenden Fachworkflows;
- keine Änderung an Recherche, Texterstellung, LanguageTool 6.8, PPM 6.7.9, PSERC oder ENDSTEMPEL;
- keine Plugin-Änderung;
- kein Publish.

Akzeptanz: Merge nur, wenn `hardlock` und `hardlock-base` auf exakt demselben PR-Head PASS sind.
