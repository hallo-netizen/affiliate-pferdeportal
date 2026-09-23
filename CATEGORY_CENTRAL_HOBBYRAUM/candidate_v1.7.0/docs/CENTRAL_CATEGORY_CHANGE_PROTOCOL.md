# Zentrales Büro „Kategorien“ – Änderungsablauf V1

## Eine Wahrheit
Der aktive zentrale Kategorienstand im Plugin `Affiliate-Portal Kategorie-Workflow` ist die einzige Sollquelle für Kategorien. Andere Plugins dürfen daraus ableiten, aber keine konkurrierende Kategorien-Wahrheit erzeugen.

## Änderung
1. Aktuellen zentralen Stand und SHA lesen.
2. Neuen vollständigen, `FINAL_APPROVED`-Strukturstand bereitstellen.
3. Read-only Vorschau erzeugen.
4. Neu / entfernt / geändert vollständig prüfen.
5. Löschungen immer ausdrücklich bestätigen.
6. Erst danach zentral übernehmen.
7. Generation steigt exakt um 1; SHA, Grund, Benutzer und Delta werden protokolliert.
8. Vorheriger Stand wird als inaktiver Fallback erhalten.
9. Betroffene Plugins anschließend einzeln aus dem neuen zentralen Stand aktualisieren und separat hart testen.
10. Kein Plugin darf beim normalen Aufruf Kategorien heimlich verändern.

## Rollback
Rollback stellt den letzten gespeicherten Fallback als neuen aktiven Stand wieder her. Die Generation läuft weiter; Historie wird nicht überschrieben.

## Sicherheitsregel
Solange ein Verbraucher nicht erfolgreich aktualisiert und positiv/negativ/regressiv geprüft wurde, bleibt dessen bisheriger produktiver Stand unverändert.
