# AKTENSCHRANK – MASTER-KONZEPTLOG ALTERNATIVE SEO/TEXT-ARCHITEKTUR

Status: AKTIV
Branch: `alternative/seo-text-central-machine-20260908`
Zweck: vollständig getrennte Dokumentation dieser Alternativroute
Datum: 2026-09-08

## Dokumentationsregel

Alles Relevante aus dieser Parallelentwicklung wird ausschließlich hier bzw. im zugehörigen Alternativordner dauerhaft abgelegt:

- Konzeptideen
- verworfene Alternativen
- Architekturentscheidungen
- Sicherheitsanforderungen
- positive/negative Testergebnisse
- erkannte Freiheitslücken
- GO/STOP-Entscheidungen
- Gründe für Fortsetzung oder Abbruch
- spätere Prototypstände

Keine dieser Überlegungen darf als stilles Chatwissen verloren gehen.

## Harte Isolation

Diese Route ist KEIN Teil des laufenden STARTMASTER-/Reparaturpfads.

Verboten:
- keine Änderung an main
- kein Merge ohne ausdrückliche spätere Entscheidung
- keine Änderung an aktiver Textmaschine
- keine Änderung an PPM/PSERC/PSTE/LanguageTool
- keine Änderung an CURRENT_STATE oder aktiven Produktionsschritten
- keine WordPress-Schreibaktion
- kein Auto-Publish
- keine Nutzung als Ersatzroute für einen BLOCKED-Zustand des anderen Systems

## Zielbild

Gesucht wird eine allgemein nutzbare, vollautomatisierbare Produktionsarchitektur mit:

- 0,0 Workflow-Entscheidungsfreiheit für Chat/KI
- 0,0 Folgeschritt-/Reparaturfreiheit für Worker
- exakt einem gebundenen Mikroschritt pro Worker
- keiner Worker-zu-Worker-Kommunikation
- einem einzigen nicht-intelligenten Eigentümer von Reihenfolge und Zustand
- fest registrierten, nicht extern injizierbaren Prüfern
- PASS oder BLOCKED, keine freie Weiterentscheidung
- unveränderter bestehender Textmaschine
- unveränderten bestehenden Fach-/SEO-/Qualitäts-/Tabellen-/Link-/LanguageTool-/PPM-/PSERC-/PSTE-/Dubletten-/Kannibalisierungs-/Publish-Regeln
- themenunabhängiger Nutzbarkeit
- theoretisch beliebig großer Batchfähigkeit durch wiederholbare Artikel-/Item-Zustände
- externer Endsignatur bzw. manipulationssicherer Bindung bis zur WordPress-Eingangsprüfung
- keiner neuen internen Signaturpflicht

## Bisher geprüfte Konzepte

### 1. Super-Worker / Rezept an einen Worker
STOP.
Grund: zu viel Interpretations- und Ablaufspielraum.

### 2. Worker -> Prüfer -> Worker als Hauptarchitektur
STOP.
Grund: verschiebt den Wächter nur; Handoff- und Bewertungsfreiheit bleiben möglich.

### 3. Goldmaster-Replay
Nicht Hauptarchitektur.
Verwendung: Referenz, Regression, Migrationsprüfung.

### 4. Zentrale Zustandsmaschine + dumme Mikroworker
GO für Prototyp.
Grund:
- Sicherheitsidee 'ein Worker = ein Schritt' bleibt erhalten
- Zustandsbesitz wird zentralisiert
- keine Worker-zu-Worker-Handoffs
- kein mehrfaches Rekonstruieren des Fachkontexts
- Folgeschritt wird ausschließlich technisch fest bestimmt

## Zentrale Sicherheitsregel

Die Steuerung ist kein Chat und keine KI.
Sie darf nur den fest versionierten Folgeschritt ausführen.

Der Worker:
- sieht nur seinen Mikroschritt
- darf keinen nächsten Schritt nennen
- darf keinen Validator auswählen
- darf keinen Reparaturweg wählen
- darf keinen Status selbst fortschreiben

Der Prüfer:
- ist fest registriert
- nicht vom Aufrufer austauschbar
- liefert nur PASS oder BLOCKED mit festem Fehlercode
- darf keinen neuen Workflowweg erfinden

## Bereits gefundene Freiheitslücke im ersten POC

Der erste POC erlaubte dem Aufrufer, bei `submit(...)` einen Validator als Callable mitzugeben.

Das ist unzulässig:
Ein Aufrufer könnte theoretisch einen Validator einsetzen, der immer PASS liefert.

Folge:
- diese Stelle wird vor dem nächsten POC entfernt
- Validatoren müssen fester Bestandteil der versionierten Maschine/Schrittdefinition sein
- keine Validator-Injektion zur Laufzeit

## Entwicklungsregel gegen Sackgassen

Keine Komplettentwicklung auf Verdacht.

Stufen:
P0 – 3 Dummy-Mikroworker + feste Prüfer + harte Angriffe
P1 – genau eine reale Problemregelklasse (Tabelle oder Link)
P2 – bestehende Textmaschine unverändert über feste Schnittstelle
Erst danach weitere Fachkomponenten.

Nach jeder Stufe zwingend GO/STOP gegen:
1. 0,0 Freiheit
2. Einfluss von außen blockiert
3. einfacher als bisher
4. weniger fehleranfällig als bisher
5. nachhaltig
6. themenunabhängig
7. automatisierbar
8. Batch-Skalierung grundsätzlich möglich
9. keine neue versteckte Übergabe-/Kontextkomplexität

Wenn eine Stufe diese Kriterien nicht erfüllt:
STOP. Nicht weiterbauen.

## Historische Problemklassen, die von Anfang an als Angriffe berücksichtigt werden

- Kontextverlust / falscher Fachkontext
- falsche Batch-/Release-Identität
- Handoff-Materialisierung
- zusätzlicher Executor / Capability-Abhängigkeit
- Runtime-Paketpfade
- Endstempel-/GitHub-/WordPress-Übergabe
- nachträglich angetackerte Tabellenregel
- nachträglich angetackerte Linkregel
- Prüfschritt überspringen
- PASS vortäuschen
- Ergebnis nach PASS verändern
- Regel zur Laufzeit deaktivieren
- freien Folgeschritt einschleusen

## Aktueller Arbeitsstand

Noch KEIN Produktions-PASS.
Noch KEINE Anbindung der echten Textmaschine.

Nächster zulässiger Prototypschritt:
P0 so härten, dass Validatoren, Reihenfolge und Zustandsübergänge vollständig nicht-injizierbar und nicht frei steuerbar sind; dann 3-Worker-Positiv/Negativtest und GO/STOP.
