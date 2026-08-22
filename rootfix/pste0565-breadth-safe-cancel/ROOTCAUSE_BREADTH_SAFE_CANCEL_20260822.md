# PSTE 0.56.5 – Breitenlauf-Abbruch – Root Cause und Hard Scope

Stand: 2026-08-22

## Belegter Fehler

PSTE 0.56.4 registriert für den Breitenlauf nur `pste_breadth_research_start` und `pste_breadth_research_advance`. Ein regulärer Cancel-Endpunkt fehlt. Die persistente Queue kennt nur `RUNNING`, `PAUSED_ERROR`, `OUTCOME_UNKNOWN`, `COMPLETE`. Beim Öffnen der Einstellungsseite wird ein `RUNNING`-Breitenlauf automatisch wieder durch `breadthLoop()` fortgesetzt.

Damit kann der Benutzer den kostenpflichtigen Breitenlauf nicht dauerhaft beenden. Das Verlassen der Seite stoppt nur weitere Browser-Ticks; ein erneutes Öffnen setzt den persistenten Lauf wieder fort.

## Hard Scope

Erlaubt ist ausschließlich ein sicherer, dauerhafter Abbruchpfad für den Breitenlauf.

Nicht erlaubt und nicht Teil dieses Blocks:

- keine Änderung an Rechercheauswahl, Longtail-/Keywordlogik oder DataForSEO-Queries
- keine Änderung an Sandbox, Familienzuordnung, Kategorien oder Artikeltypen
- keine Änderung an Titel-, SEO-, Qualitäts-, Textmaschinen-, PPM-, Design- oder WordPress-Schreiblogik
- kein Publish
- keine Änderung an PSERC, PPM oder Link Policy

## Sicherheitsanforderung

Ein Abbruch darf keine neue Provideranfrage auslösen und darf einen bereits extern gesendeten Request nicht blind löschen. Ist ein Providerrequest gerade in-flight, darf höchstens dessen vorhandener/cachebarer Readback lokal abgeschlossen werden. Bei unbekanntem Provider-Ausgang bleibt der bestehende Fail-closed-Schutz erhalten.

Nach erfolgreichem Abbruch müssen Queue und aktiver Kindlauf terminal beendet sein, Budgetreservierung freigegeben sein und ein erneutes Öffnen der Einstellungsseite darf den abgebrochenen Breitenlauf nicht wieder starten.
