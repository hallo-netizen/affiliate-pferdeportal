# Workflow-Hard-Audit V1.6.1

## Kritische Befunde aus Master 015 / Plugin 1.5.0
1. Kostenpflichtige Global-Coverage war technisch vor der vereinbarten Erst-Sichtprüfung möglich.
2. Nach Global-Coverage konnten Chat/Master Hauptthemen korrigieren und direkt Detailresearch starten, ohne dass der korrigierte Baum sichtbar freigegeben war.
3. `DEFERRED` wurde als "entschieden" behandelt und konnte dadurch Detail-/Finalgates schließen.
4. Masterdokumente enthielten unterschiedliche Reihenfolgen für die Erst-Sichtprüfung.
5. Der Nutzer konnte daher formal nicht sicher sein, dass genau der sichtbare Entwurf die kostenpflichtige Recherche auslöste.

## Rootfix
- Erst-Sichtprüfung ist jetzt hashgebundenes technisches Gate vor jedem Paid Global-Call.
- Zweite sichtbare Global-Gap-Freigabe ist hashgebundenes technisches Gate vor jedem Paid Detailresearch.
- Finale Sichtprüfung bleibt drittes hashgebundenes Gate vor FINAL.
- `DEFERRED` bleibt als Arbeitsstatus zulässig, blockiert aber Detailresearch bzw. READY/FINAL.
- Jede Änderung nach einem Review ändert den Scope-Hash und erzwingt den jeweiligen Review erneut.
- Keine neuen Content-Write-Pfade.

## HARDLOCK-Befunde 2026-08-20

- `project.target_market` und `project.language_code` sind Pflichtfelder des PROJECT CONTRACT und Bestandteil sämtlicher Review- und Research-Scope-Hashes. Abweichende Laufzeitparameter blockieren vor dem ersten externen Request.
- Keyword-/Core-Ähnlichkeit ist nur ein automatischer Zuordnungshinweis. Jeder relevante Global-Coverage-Fund benötigt eine explizite Entscheidung (`MAIN_TOPIC`, `SUBTOPIC`, `ARTICLE_ONLY` oder `OUT_OF_SCOPE`); ohne Entscheidung bleibt das Gate `BLOCKED`, `DEFERRED` bleibt ebenfalls blockierend.
