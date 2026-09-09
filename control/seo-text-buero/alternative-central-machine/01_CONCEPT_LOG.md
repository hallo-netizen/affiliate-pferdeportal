# KONZEPTLOG – Alternative Zentralmaschine

## Ausgangsproblem

Die bisherige Raum-/Raum-Architektur erreicht starke Bindung pro Schritt, erzeugt aber viele technische Übergaben: neuer Raum, neuer Kontext, neue Bindung, neue Handoff-Datei, neue Identitäts-/Hashprüfung. Historisch sind genau an solchen Übergängen wiederholt Fehler entstanden.

## Nicht ausreichende Alternativen

### A. Ein Super-Worker erledigt mehrere Schritte
ABGELEHNT.
Grund: Worker hätte Interpretations- und Ablaufspielraum.

### B. Worker 1 -> KI-Prüfer -> Worker 2
ABGELEHNT als eigenständige Lösung.
Grund: verschiebt den Wächter nur nach außen. Wenn Prüfer intelligent entscheidet oder Übergaben frei formuliert sind, bleibt dieselbe Fehlerklasse.

### C. Räume nur in "Arbeitsstationen" umbenennen
ABGELEHNT.
Grund: keine echte Architekturänderung.

## Aktueller Kandidat: zentrale Zustandsmaschine + dumme Mikroworker

Prinzip:

1. Ein einziger technischer Steuerkern besitzt Auftrag, Zustand und feste Reihenfolge.
2. Er ist kein Chat und keine KI.
3. Er kann nur den im Code/Vertrag fest definierten Folgeschritt aufrufen.
4. Jeder Worker erhält nur die Eingaben seines einen Mikroschritts.
5. Worker kennen keinen Folgeschritt und dürfen keinen auswählen.
6. Worker kommunizieren nie direkt miteinander.
7. Ein Worker schreibt nur in ein festes Ergebnisschema.
8. Der Steuerkern prüft das Ergebnis mechanisch.
9. Nur PASS führt zum exakt festgelegten nächsten Schritt.
10. Jede Abweichung führt zu BLOCKED.
11. Fachkontext bleibt ein einziges kanonisches Job-Objekt und wird nicht an jedem Übergang neu konstruiert.
12. Textmaschine und bestehende Fachregeln bleiben unverändert und werden lediglich an der bereits vorgesehenen Stelle aufgerufen.
13. Am Ende entsteht ein unveränderlich gebundenes Ausgabepaket für die externe Signierung/WordPress-Übergabe.

## Entscheidender Unterschied zum bisherigen Raumprinzip

NICHT weniger Prüfungen.
NICHT größere Worker.
NICHT mehr Vertrauen.

Sondern:
- nur ein Eigentümer des Zustands,
- keine frei formulierten Handoffs,
- kein Worker baut den Auftrag des nächsten Workers,
- kein mehrfaches Rekonstruieren desselben Fachkontexts,
- keine verteilte Workflow-Navigation.

Die Sicherheitsidee "ein Worker = genau ein Schritt" bleibt erhalten.

## Noch nicht bewiesen

Der Kandidat ist erst dann ernsthaft belastbar, wenn positive und negative Prototyptests zeigen:
- Reihenfolge nicht überspringbar,
- falscher Worker nicht aufrufbar,
- Worker kann Folgeschritt nicht beeinflussen,
- zusätzliche Felder/Anweisungen werden abgewiesen,
- Ergebnismanipulation wird erkannt,
- Kontext/IDs bleiben identisch,
- FAIL kann nicht in PASS umgedeutet werden,
- Neustart setzt exakt am gespeicherten Zustand fort,
- Ausgabeänderung nach finaler Bindung wird erkannt,
- spätere WordPress-Übergabe akzeptiert nur exakt signierte/gebundene Bytes.
