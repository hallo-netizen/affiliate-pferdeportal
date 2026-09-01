# STARTMASTER0107 – Networkless Runtime Rootfix Test Evidence

Scope ausschließlich technische Codex-Cloud-Laufzeit; keine Fach-/Inhalts-/Qualitätsautorität.

## Lokaler deterministischer Harness

Das kanonische Setup-/Maintenance-Skript wurde mit einem kontrollierten Fake-Git/Fake-Python-Harness positiv und negativ geprüft.

Ergebnisse:

- `MAIN_STALE_TO_CURRENT_POSITIVE_PASS`
  - Ausgang: Branch `main`, lokaler HEAD absichtlich veraltet.
  - Erwartung/Pass: GitHub-main-SHA wird über vollständige Repository-URL ermittelt; exakt dieser Commit wird gefetcht; `git reset --hard <MAIN_SHA>` setzt den Worktree auf den aktuellen main; lokaler Marker `refs/remotes/origin/main` wird erst danach gesetzt; `MAIN_SYNC.json` wird erzeugt; Produktions-Preflight wird danach aufgerufen.

- `NON_MAIN_NOT_REWRITTEN_NEGATIVE_PASS`
  - Ausgang: beliebiger Nicht-main-Branch.
  - Erwartung/Pass: kein `ls-remote`, kein `fetch`, kein `reset`, kein Produktions-Preflight. Der Branch-/HEAD-Stand bleibt unverändert.

- `ORIGIN_REMOTE_DEPENDENCY_NEGATIVE_PASS`
  - Erwartung/Pass: die historische fehlerhafte Form `git ls-remote origin refs/heads/main` ist im neuen Setup-/Maintenance-Skript nicht vorhanden.

- `SHELL_SYNTAX_PASS`
  - `bash -n` auf dem kanonischen Skript: PASS.

## Forensische Zuordnung des gemeldeten Fehlers

Der String `GIT_CHECK_FAILED:ls-remote origin refs/heads/main` stammt exakt aus dem historischen `control/output-quarantine/worker_freshness_guard.py` des Commits `a52dc0df70d3c9f33cf61f337b2aafec9a44afaf`. Der aktuelle Guard auf main enthält diesen Remote-Aufruf nicht.

## Unverändert

Recherche, Fact Packs, Textregeln, Qualität, LanguageTool, PPM, PSERC, PSTE, Titel, Keywords, SEO, Design, Dubletten-/Kannibalisierungslogik, Parallelisierung, H8-Signatur, Quarantäne, Release Receipt und Publish-Regeln wurden nicht verändert.
