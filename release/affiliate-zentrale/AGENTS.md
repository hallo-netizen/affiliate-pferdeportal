# Affiliate-Zentrale – externe Release-Kontrollinstanz

Für **jede** Arbeit an der Affiliate-Zentrale gilt zusätzlich zum Root-`AGENTS.md`:

1. **Zuerst** `control/release-governance/CURRENT_RELEASE.json` lesen. Diese Datei ist die einzige maschinenlesbare Entscheidungsinstanz für Ziel, aktuellen Zustand, autorisierten nächsten Schritt, Arbeitsbranch, Scope und Release-Gates.
2. Vor Arbeit: `python3 control/release-governance/release_guard.py governance-check`. Auf `affiliate-release-current` zusätzlich: `python3 control/release-governance/release_guard.py start --branch "$(git branch --show-current)"`.
3. Einzige aktuelle Releasequelle ist der **direkt committed** Quellbaum `release/affiliate-zentrale/current/affiliate-portal-router/` plus das hashgebundene `CURRENT_SOURCE_SHA256.txt`. Der Guard darf diese Quelle ausschließlich **prüfen**, niemals erzeugen, rekonstruieren oder reparieren.
4. Für die aktuelle Quelle sind **Base64-, GZIP-, Chunk-, Patch-, ZIP- oder Historien-Rekonstruktionen verboten**. Alte Branches, Root-`affiliate-portal-router/`, `CI_V*`, `STAGING_V*`, Chat-Anhänge und historische Pluginbäume besitzen keine Releaseautorität.
5. Release-Arbeit ausschließlich auf `affiliate-release-current`. Keine Versions-, Staging-, Probe-, Rekonstruktions- oder Nebenbranches.
6. Das Feld `objective_control` hält das Gesamtziel fest. Maximal **ein** Arbeitsstrang. Kein Microfix, keine Zusatzanalyse und keine neue Version, außer der aktuell gebundene fehlgeschlagene Gate-Schritt erfordert genau diese Änderung.
7. Das Feld `execution_state.authorized_next_action` ist der **einzige** nächste Arbeitsschritt. Keine Alternativroute, keine freiwillige Zusatzprüfung, keine neue Architektur. Änderungen sind zusätzlich auf `authorized_change_prefixes` begrenzt.
8. Bereits bestandene Gates werden **nicht erneut ausgeführt**, solange ihr Evidence-Hash an denselben `current_source_manifest_sha256` gebunden ist. Ändert sich der Quellmanifest-Hash, ist nur die davon betroffene/stale Evidence neu zu erzeugen.
9. Historische V6.62.0-/V6.63.4-Daten sind immutable **Evidenz**, keine Arbeitsquelle. Sie dürfen nicht neu erzeugt werden.
10. Keine Release-ZIP erzeugen oder als installierbar bezeichnen, solange `release_allowed=false`, der Status nicht `RELEASED` ist oder auch nur ein Pflichtgate nicht hashgebunden `PASS` ist.
11. Jeder PASS benötigt Evidence unter `release/affiliate-zentrale/evidence/` mit Evidence-SHA **und** Bindung an den aktuellen Source-Manifest-SHA.
12. Vor Freigabe muss `python3 control/release-governance/release_guard.py release-check` PASS liefern. Ohne diesen PASS gibt es keine Installation und keine Releasebehauptung.

## Fail-closed-Regel

Wenn die kanonischen Source-Bytes fehlen oder ein Guard blockiert, darf **keine eigene Ersatzlösung** entwickelt werden. Ausgeführt wird ausschließlich `authorized_next_action` aus `CURRENT_RELEASE.json`. Der Blocker darf nicht durch Rekonstruktion, neue Branches, neue Versionen oder zusätzliche Prüfpfade umgangen werden.
