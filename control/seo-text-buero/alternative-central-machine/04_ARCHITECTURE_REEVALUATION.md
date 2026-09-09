# ARCHITEKTUR-NEUBEWERTUNG – GO/STOP

Datum: 2026-09-08
Status: KONZEPTENTSCHEIDUNG FÜR PROTOTYP, KEIN PRODUKTIONS-PASS

## Unverhandelbare Prüfkriterien

- Chat/KI: 0,0 Workflow-Entscheidungsfreiheit
- Worker: exakt ein gebundener Mikroschritt
- Prüfer: keine freie Bewertung des Workflowfortschritts
- Textmaschine unverändert
- alle bestehenden Fach-/SEO-/Qualitäts-/Tabellen-/Link-/LanguageTool-/PPM-/PSERC-/PSTE-/Dubletten-/Kannibalisierungs-/Publish-Regeln bleiben erhalten
- themenunabhängig
- vollautomatisierbar
- fail-closed
- kein Auto-Publish
- externe Endsignatur / unveränderte WordPress-Übergabe
- keine interne Signierung als neue Pflicht
- geringere Übergabe-/Kontextfehleranfälligkeit als Raum-/Raum-System

## Kandidat A – Super-Worker / ein Worker führt mehrere Schritte aus

STOP.

Grund:
- erzeugt Interpretations- und Ablaufspielraum im Worker
- verletzt 0,0-Freiheit
- Fehler in einem großen Worker sind schwerer zu isolieren
- ein Prompt/Rezept allein ist keine technische Zwangsgrenze

## Kandidat B – Worker -> unabhängiger TÜV -> Worker

STOP als Hauptarchitektur.

Grund:
- verschiebt den bisherigen Wächter nur nach außen
- bleibt bei frei anbindbarem Prüfer manipulierbar
- erzeugt weiterhin viele echte Handoffs
- kann bei semantischem KI-Prüfer neue Bewertungsfreiheit schaffen

Zulässig nur als zusätzliche finale Außenprüfung.

## Kandidat C – Goldmaster-Replay

NICHT als Hauptarchitektur.

Stärke:
- reale erfolgreiche Produktionsstände sind wertvolle Referenz
- spätere Änderungen können einzeln positiv/negativ gegen bewährten Stand geprüft werden

Schwäche:
- löst die strukturellen Handoff-/Kontextprobleme nicht automatisch
- reproduziert bei 1:1-Übernahme auch alte Architekturgrenzen

Verwendung:
- als Referenz-, Migrations- und Regressionstestverfahren für Kandidat D

## Kandidat D – zentrale Zustandsmaschine + dumme Mikroworker

GO für Prototyp.

Harte Form:
1. genau ein nicht-intelligenter Steuerkern besitzt Auftrag, Reihenfolge und Zustand
2. jeder Worker erhält nur genau seinen einen Mikroschritt
3. kein Worker kennt oder wählt den Folgeschritt
4. keine Worker-zu-Worker-Kommunikation
5. ein einziges kanonisches Jobobjekt bleibt Eigentum des Steuerkerns
6. kein Neuaufbau des Fachkontexts an jedem Übergang
7. Validatoren sind fest im unveränderlichen Ablauf registriert
8. der Aufrufer/Chat darf keinen Validator, Folgeschritt oder Reparaturweg mitgeben
9. Validatorresultat nur PASS oder BLOCKED mit festem Fehlercode
10. BLOCKED hat keine improvisierte Ersatzroute
11. bestehende Textmaschine wird nur über ihre vorhandene Schnittstelle aufgerufen und nicht verändert
12. externe Endsignatur bindet das fertige Ausgabepaket bis zur WordPress-Eingangsprüfung

## Wichtiger Befund aus POC 001

Der erste POC enthielt bereits eine echte Sicherheitslücke:
CentralMachine.submit(...) nahm den Validator als Callable vom Aufrufer entgegen.

Damit hätte ein freier Aufrufer theoretisch einen Validator übergeben können, der immer True liefert.

Folgerung:
- POC 001 beweist nur Grundmechanik
- vor POC 002 muss diese Freiheit vollständig entfernt werden
- Validatoren müssen Bestandteil der fest versionierten Maschine/Schrittdefinition sein und dürfen nicht zur Laufzeit vom Chat/Worker geliefert werden

Dieser Befund ist ein positives Zeichen für das Prototypverfahren: die Lücke wurde vor Anbindung der echten Textmaschine entdeckt.

## Vergleich mit realer Historie

Der reale 6-Artikeltest vom 28.08.2026 beweist, dass Textmaschine, PPM, PSERC, PSTE, LanguageTool und Fach-/Qualitätsregeln zusammen erfolgreich produzieren konnten.

Die spätere Fehlerhistorie M26-M33 konzentriert sich stark auf:
- fehlenden/falschen Fachkontext
- Handoff-Materialisierung
- Batch-/Release-Identität
- zusätzliche Executor-Abhängigkeiten
- Runtime-Paketpfade
- Endstempel-/GitHub-Übergaben

Der Kandidat D zielt genau darauf:
Sicherheitsprüfungen behalten, aber verteilte Zustands- und Handoff-Neukonstruktion reduzieren.

## Empfohlene Entwicklungsstrategie

Nicht sofort Gesamtworkflow bauen.

P0:
- zentrale Zustandsmaschine härten
- externe Validator-Injektion entfernen
- 3 Dummy-Mikroworker
- harte Positiv-/Negativ-Angriffe
- GO/STOP

P1:
- eine reale problematische Regelklasse als unveränderlichen Validator anbinden (Tabelle oder Link)
- ausdrücklich testen, dass sie nicht nachträglich frei an-/abgeschaltet werden kann
- GO/STOP

P2:
- bestehende Textmaschine unverändert nur an einer Schnittstelle anbinden
- keine restlichen Fachmodule gleichzeitig hinzufügen
- GO/STOP

Erst bei PASS von P0-P2:
Detailentwicklung des vollständigen automatischen Workflows.

## Entscheidung

Zu starten ist ausschließlich Kandidat D:
ZENTRALE ZUSTANDSMASCHINE + DUMME MIKROWORKER + FEST EINGEBAUTE VALIDATOREN.

Goldmaster-Replay dient als Referenz/Regression.
Ein unabhängiger TÜV kann später zusätzlich am Ausgang stehen.
Super-Worker und reine Zickzack-TÜV-Architektur werden nicht weiterverfolgt.
