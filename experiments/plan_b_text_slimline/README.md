# PLAN B – TEXT Slimline Shadow V1

## Rolle

Vollständig getrennte technische Versuchslinie. **Kein Bestandteil des produktiven TEXT-/STARTMASTER-Wegs.**

Basis für die Branch-Abzweigung: `main c8a96e7a2f598de69134d90b143257c3559bc98a`.

## Unverhandelbar

- genau **eine Tür**;
- Wächter bleibt **dumm**: nur exakte Identität, Hash, Status, Vertrag, feste Reihenfolge;
- Chat bleibt in der **Zwangsjacke**: keine Navigation, keine State-Schreibautorität, keine Reparaturautorität, keine Publish-Autorität;
- alle 12 bestehenden Qualitätsstufen bleiben erhalten;
- Fachlogik, Inhalt, SEO, Design, PPM/PSERC/PSTE und Publish-Regeln werden nicht verändert;
- externe PSERC-Finalisierung und GitHub-Endstempel bleiben getrennte Sicherheitsgrenzen;
- PASS -> automatisch exakt nächster festgelegter Zustand; alles andere -> STOP.

## Was Plan B vereinfacht

Nur technische Orchestrierung:

1. eine State-Datei statt mehrerer konkurrierender Navigationszustände;
2. eine Tür für `current` + `submit`;
3. keine alternative Route und keine Fallback-Auswahl;
4. sieben Artikel laufen deterministisch nacheinander;
5. nach Artikel 7 entsteht automatisch genau ein `PREPARED_BATCH.json`;
6. Final Review -> External Finalize -> GitHub Endstamp sind feste Zustände;
7. keine Entscheidung des Chats über den nächsten Schritt.

## Was bewusst NICHT vereinfacht wird

- keine Qualitätsstufe entfernt;
- keine Stage-Proofs entfernt;
- FACHWORKFLOW_PASS bleibt eigenständige Qualitätswahrheit;
- ITEM_RECEIPT bleibt eigenständige technische Abschlusswahrheit;
- PPM-Finalartikel-/Report-Hashbindung bleibt;
- externe Signierung bleibt extern;
- Endstempel bleibt eigene Grenze.

## Aktueller Implementierungsstatus

`slimline_controller.py` ist eine **Shadow-Referenzimplementierung**. Sie führt keine Produktionsaktion aus und ist in keinen bestehenden Workflow eingebunden.

Sie kann:
- einen gebundenen Batch initialisieren;
- exakt ein aktuelles Ticket ausgeben;
- vorhandene 12-Stage-/FACHWORKFLOW-/ITEM-Receipts stumpf prüfen;
- bei PASS automatisch den festen Folgezustand setzen;
- bei Abweichung fail-closed stoppen;
- nach dem letzten Item einen nicht sichtbaren Prepared-Batch erzeugen;
- Final Review, externe PSERC-Finalisierung und GitHub-Endstempel als feste nachgelagerte Grenzen erzwingen.

## Späterer Prüfansatz

Nicht jetzt mit Produktion verbinden.

Nach dem Test des bestehenden Konzepts kann derselbe 7er-Batch in einer isolierten Prüfumgebung gegen Plan B laufen. Vergleichskriterien:
- dieselben sieben Inputs;
- dieselben 12 Qualitäts-PASSes;
- dieselben finalen Artikelbytes/Hashes;
- dieselbe PPM-Bindung;
- dieselbe Publish-Sperre;
- dieselben externen Sicherheitsgrenzen;
- weniger technische Zustände/Übergaben.

Erst bei vollständiger Gleichheit darf Plan B überhaupt als Integrationskandidat diskutiert werden.
