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

## Historischer Arbeitsstand beim Start der Route

Dieser Abschnitt ist historische Ausgangslage und keine aktuelle Arbeitswahrheit.

Zum Start waren Produktions-PASS und echte Textmaschinen-/PPM-Anbindung noch nicht bewiesen.
Der damalige nächste Schritt war P0.
Der aktuelle Stand steht ausschließlich unten unter **AKTUELLER ROUTENSTAND P46**.


## HARD RULE – PROTOTYP-ENTWICKLUNG VON GROSS NACH KLEIN

Diese Regel ist für die gesamte Alternativroute bindend.

1. PROTOTYP ZUERST, KEINE DETAILORGIE
- zuerst nur beweisen, ob das Grundkonzept trägt
- keine vollständige Produktionsarchitektur bauen, bevor der kleine Prototyp eindeutig PASS ist
- keine Nebenbaustellen und keine vorsorglichen Zusatzmodule

2. VON GROSS NACH KLEIN
- zuerst Architekturprinzip und zentrale Zustandsführung
- danach wenige Mikroworker
- danach genau eine reale Problemregelklasse
- erst danach echte Textmaschine und weitere Fachkomponenten
- Details nur dann bauen, wenn die vorherige Ebene ihren Nutzen bewiesen hat

3. ZWINGENDE GEGENPRÜFUNG NACH JEDEM SCHRITT
Jeder Schritt muss gegen alle folgenden Kriterien geprüft werden:
- 0,0 Entscheidungsfreiheit für Chat/KI
- 0,0 freie Workflow-/Folgeschritt-/Reparaturwahl für Worker
- kein von außen austauschbarer oder abschaltbarer Prüfer
- keine freie Einflussnahme von außen auf Zustand, Reihenfolge, Regeln oder Ergebnis
- fail-closed bei Abweichung
- nachhaltig und wartbar
- themenunabhängig
- vollautomatisierbar
- theoretisch auf beliebig viele Artikel/Items wiederholbar
- keine neue versteckte Handoff-/Kontextkomplexität
- nachweislich einfacher oder mindestens nicht komplexer als der bisherige Weg
- nachweislich weniger oder mindestens nicht stärker fehleranfällig

4. SACKGASSEN-SCHUTZ
Wenn ein Prototypschritt:
- mehr Sonderfälle als Nutzen erzeugt,
- neue freie Entscheidungsstellen benötigt,
- zusätzliche Handoff-Schichten braucht,
- alte Fehlerklassen nur verschiebt statt beseitigt,
- oder die Architektur sichtbar komplizierter macht,

dann gilt sofort:
STOP -> Ursache dokumentieren -> Konzept verwerfen oder auf vorherige Ebene zurückgehen.
Kein Weiterbauen eines unbewiesenen Weges.

5. BEWEISPFLICHT
Ein subjektives „sieht gut aus“ ist kein PASS.
Jeder Prototypschritt braucht:
- mindestens einen positiven Test,
- gezielte negative Manipulations-/Umgehungstests,
- dokumentierte GO/STOP-Entscheidung,
- Vergleich gegen die oben genannten Kriterien.

6. ISOLATION
Alle Arbeiten und Erkenntnisse dieser Route bleiben ausschließlich im separaten Alternativbranch und Aktenschrank.
Keine Vermischung mit dem parallelen Reparaturchat oder dessen produktivem Arbeitsweg.


## HARD RULE – KISS

Für die gesamte Alternativroute gilt zusätzlich:

- immer die kleinstmögliche technische Lösung wählen, die alle Sicherheitsregeln erfüllt
- keine neue Schicht, kein neuer Gate-Typ, kein neuer Signer, kein neuer Runner und kein neuer Controller, wenn eine bestehende einfache Funktion dieselbe Aufgabe sicher erledigt
- neue Erkenntnis zuerst in bestehende Struktur einordnen; nicht automatisch neue Architektur bauen
- wenige feste Zustände statt vieler Zwischenzustände
- wenige feste Datenobjekte statt vieler Handoff-Dateien
- eine Regel an genau einer autoritativen Stelle
- Erweiterbarkeit über feste, klar begrenzte Schnittstellen; keine Sonderwege
- Komplexität ist ein FAIL-Kriterium, wenn sie keinen nachweisbaren Sicherheits- oder Funktionsgewinn bringt

KISS steht nicht über Sicherheit. Wenn Einfachheit und 0,0-Freiheit kollidieren, gewinnt die Sicherheitsregel. Innerhalb derselben Sicherheit gewinnt immer die einfachere Lösung.


## HARD RULE – BESTEHENDE CHAT/CODEX- UND DATEIÜBERGABE-INFRASTRUKTUR NICHT NEU ERFINDEN

Für alle weiteren Prüfungen der Alternativroute gelten zwei bereits implementierte Systemfähigkeiten als bestehende Infrastruktur:

1. CODEX-START AUS JEDEM CHAT
- Codex kann bereits aus jedem Chat gestartet werden.
- Das gilt ausdrücklich auch innerhalb der Artikelerstellung.
- Die Alternativarchitektur baut dafür KEINEN neuen Entry-, Runner-, Dispatcher- oder Startweg.
- Geprüft wird nur, ob die Zentralmaschine diesen bestehenden Einstieg sicher nutzen kann.

2. KORREKTE DATEIÜBERGABE IST BEREITS IMPLEMENTIERT
- Die bestehende korrekte Dateiübergabe im Workflow gilt als vorhandene Infrastruktur.
- Kein neuer Datei-Handoff, kein neues Übergabeformat und keine zweite Transferarchitektur werden erfunden.
- In der Alternativroute wird ausschließlich geprüft, wie der bereits vorhandene Übergabeweg an den einen kanonischen Jobzustand bzw. die signierte Releasegrenze angebunden wird.

KISS-Folge:
Bestehende Start- und Transferfähigkeit wiederverwenden; keine Parallelarchitektur bauen.

Sicherheitsfolge:
Diese Fähigkeiten dürfen keine neue Workflowfreiheit erzeugen. Chat/Codex starten nur den fest gebundenen Prozess; die Dateiübergabe transportiert nur das fest gebundene Objekt.


## FINALER PROTOTYPSTATUS P34

Status: GO.

Autoritative Abschlussakte dieser Prototypphase:
`36_P34_FINAL_PROTOTYPE_GO.md`

Eingefrorenes KISS-Ziel:
bestehender Chat/Codex-Start -> EINE Zentralmaschine -> bestehende Fachbausteine -> prepare ohne Write -> EINE externe Signatur -> verifizierter Draft-Write -> Readback/DOM -> STOP ohne Publish.

P0–P34 sind ausschließlich Labor-/Beweisakten und dürfen nicht als Produktionsstufen interpretiert oder implementiert werden.

Nächste zulässige Entwicklungsphase:
Minimaler Realintegrations-Prototyp mit genau einem gebundenen Item.

HARD RULE:
Bei jeder Unstimmigkeit zuerst vorhandenen Baustein prüfen.
Keine neue Architektur als Reflex.


## AKTUELLER ROUTENSTAND P46

Stand: 2026-09-09
Status: AKTIV – REALINTEGRATIONS-PROTOTYP, NOCH KEINE PRODUKTIONSFREIGABE

Aktueller Alternativbranch:
`alternative/seo-text-central-machine-20260908`

Aktueller Beweisstand:
- P0–P46 im gemeinsamen isolierten Laborlauf PASS
- historischer 7/7-Goldbatch vollständig hashgeprüft
- 7 × derselbe reale Ein-Item-Pfad PASS
- vorhandene `FACHWORKFLOW_HANDOFF_REQUEST.json` bleibt einzige Produktions-Eingangswahrheit
- kein neues Jobmanifest im Zielbetrieb
- dünner Handoff-Controller ohne frei wählbare Route/Worker/Validator/Engine
- plan_slot / canonical_article_id / plan_item_key vollständig getrennt und fail-closed gebunden
- bestehender PPM-`prepare()`-Punkt als schreibfreie Vor-Signatur-Grenze bewiesen
- externe Signatur vor Draft-Write bewiesen
- bestehende öffentliche PPM-Prewrite-Bausteine vorhanden
- exakte Prewrite-Reihenfolge aus bestehendem `execute_plan` gelesen
- private Helper wurden nur inventarisiert; keine Reflection-/Umgehungslösung
- publish_allowed=false

### AKTUELLE EINZIGE NEXT ACTION

P47 – kleinster Realintegrationsschritt:

Aus exakt der bestehenden `FACHWORKFLOW_HANDOFF_REQUEST.json` im bereits vorhandenen dünnen Controller ausschließlich die in P44/P45 belegten **öffentlichen bestehenden PPM-Bausteine** in der belegten Reihenfolge bis zum schreibfreien `prepare()` ausführen.

Danach ausschließlich:
`prepare -> externe Signatur -> verifizierter Prepared-Payload -> bestehendes create_draft -> Readback/DOM -> STOP ohne Publish`.

Harte STOP-Regel:
Wenn dafür private PPM-Helper kopiert, per Reflection aufgerufen, neue PPM-APIs, ein zweites Handoff, ein neues Jobmanifest oder ein weiterer Controller nötig wären:
STOP. Erst vorhandenen Baustein erneut prüfen.

### PARALLELWEG-GRENZE

Der produktive STARTMASTER-/Reparaturweg bleibt vollständig getrennt.
Dessen CURRENT_STATE, Fehlerstatus, Hobbyraum und aktive Reparaturbranches werden von dieser Route nicht überschrieben.

### CAMPUS-STANDARD

Die erkannte allgemeine KISS-Architektur ist noch **nicht** in den Campus-Neubaustandard übernommen.
Grund: Diese Route ist ausdrücklich isolierter Prototyp und noch nicht als allgemeiner Campus-Standard freigegeben.

Status:
`CAMPUS_PROPAGATION_BLOCKED_UNTIL_ALTERNATIVE_ARCHITECTURE_APPROVED`

Bis zur Freigabe keine Vermischung mit dem Campus-/Produktionsstandard.
