# STARTMASTER0107 – Networkless Agent Runtime Invariant

Scope: ausschließlich technische Codex-Cloud-Laufzeit. Keine Fach-, Inhalts-, Qualitäts-, SEO-, Design-, LanguageTool-, PPM-, PSERC-, PSTE-, Dubletten-/Kannibalisierungs- oder Publish-Autorität.

## Forensischer Befund

Der Fehler `GIT_CHECK_FAILED:ls-remote origin refs/heads/main` entspricht exakt dem historischen `worker_freshness_guard.py` aus Commit `a52dc0df70d3c9f33cf61f337b2aafec9a44afaf`. Der aktuelle Guard auf main enthält diesen Remote-Aufruf nicht mehr. Damit ist ein veralteter Laufzeitstand im Codex-Container nachgewiesen; es handelt sich nicht um eine Fach-/Artikelentscheidung.

## Dauerhafte Invariante

1. Netz-/GitHub-Remote-Prüfungen erfolgen ausschließlich in Codex Setup/Maintenance vor der Agent-Phase.
2. Wenn der Codex-Task auf `main` gestartet wird, synchronisiert Setup/Maintenance den kompletten Worktree hart auf den zu diesem Zeitpunkt aktuellen GitHub-main-SHA.
3. Dabei wird die vollständige Repository-URL benutzt; ein vorhandenes `origin`-Remote ist keine Voraussetzung.
4. Erst nach erfolgreichem Hard-Sync wird `refs/remotes/origin/main` als lokaler, bereits verifizierter Marker für die Offline-Agent-Phase gesetzt.
5. `worker_freshness_guard.py`, `runtime_entry_gate.py` und der 107007→107008-Abschluss benötigen in der Agent-Phase kein Netzwerk.
6. Nicht-main-Branches werden vom Produktions-Hard-Sync nicht verändert.
7. Wächter bleiben fachblind und entscheidungsfrei. Sie prüfen nur technische Identitäten, Hashes, Statuswerte und gebundene Pfade.
8. `publish_allowed=false` und Release-Receipt-only bleiben unverändert.

## Ziel

Ein gecachter oder veralteter `main`-Checkout darf nicht mehr bis in die Artikelproduktion oder den 107007-Abschluss gelangen. Er wird vor Agent-Start auf den aktuellen GitHub-main-Stand synchronisiert. Dadurch kann ein historischer Guard mit `ls-remote origin` nicht mehr aus einem stale cached main ausgeführt werden.
