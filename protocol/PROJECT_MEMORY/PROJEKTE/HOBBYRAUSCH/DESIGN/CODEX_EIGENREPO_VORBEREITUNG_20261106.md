# Hobby Depot – Codex-Startweg, Stand 06.11.2026

## Harte Prüfung
- PR #632 hat Codex Cloud erfolgreich erreicht, aber Root-AGENTS und Cloud-Gate binden diesen gemeinsamen Repositorystart ausschließlich an Pferdeatelier/K0; Hobby-Bildtest wurde BLOCKED / 0 von 20.
- Eine experimentelle Hobby-Ausnahme auf nur einem Zweig hat die bestehende unveränderbare Root-/Sicherheitsdatei berührt und wurde deshalb vollständig zurückgenommen.
- Nach der Rücknahme ist `AGENTS.md` im Hobby-Prüfzweig wieder bytegenau identisch zur offiziellen Campus-Basis (`ff579ce4f22994fb741ea6c65ad6be8cf07cc269`). Im PR-Diff gibt es keine geänderten K0-, Cloud-Gate- oder Root-Dateien. Die ursprüngliche K0-Steuerung wurde weder gepatcht noch umgangen.
- Ein K0-GitHub-Hardlock-Lauf hat nach Wiederherstellung den PATH_GUARD_PASS gezeigt; der Workflow scheitert separat an einem fehlenden `control/paul-scope-gate/paul_scope_gate.py` im Runner – dieser fremde Fehler ist **kein** Beweis fuer eine gelungene K0-Sicherheitspruefung und wird durch diesen Hobby-Auftrag nicht repariert.

## Saubere Lösung
**Eigenes Repository `hallo-netizen/hobby-depot-codex`** ohne die repo-weite K0-`AGENTS.md` und ohne `control/cloud-entry-gate/`. Dies wird ausdrücklich neu angelegt; kein Umgehen bestehender Sicherheit auf dem K0-Repository.

- ChatGPT-Codex verbindet sich mit dem eigenständigen Repo und führt den 20er-Test als voneinander getrennte Einzelbildaufträge aus (keine Bildraster/Collagen). Keine OpenAI-API.
- Das in diesem Chat erstellte, lokal getestete Starterpaket `HOBBY_DEPOT_CODEX_EIGENREPO_STARTPAKET.zip` enthält eigene `AGENTS.md`, 20 vorgesehene offene Kandidaten aus dem Hobbyregister HD007 1.2.19, vollständiges Statusregister mit 862 Hobbys, Produktionsauftrag, technisch unabhängige Fail-Closed-Bildprüfung und verlustfreien Staging-ZIP-Bau. 
- Beleg: `tests/test_fail_closed.py` PASS; 20 fehlende Bilder ergeben ausdrücklich BLOCKED und die Integration erstellt ohne tatsächlich bestandene Bildprüfung keine ZIP. Dies ist **keine** echte Codex-Bilderzeugung.
- HD003 nutzt bereits die Slug-bezogene HD007-Masterablage; kein Umbau der Beitragsbildzentrale HD006 vorgesehen. Original-Plugin und WordPress bleiben unverändert.
- Der GitHub-Connector dieser Sitzung kann Repos lesen und darin schreiben, bietet aber **keine Repository-Erstellung**. Für die vollständige Aktivierung ist einmalig das leere Repository `hobby-depot-codex` im Account `hallo-netizen` anzulegen, anschließend können die Dateien per verbundenem GitHub hinzugefügt und ein @codex-Test-PR eröffnet werden.

## Status
**Vorbereitung und Sicherheitstrennung: PASS.** 
**Eigenständiges GitHub-Repo: NICHT ANGELEGT.**
**Echter Codex-20er-Bildlauf: NOCH NICHT AUSGEFÜHRT.**
**K0 unverändert.**
