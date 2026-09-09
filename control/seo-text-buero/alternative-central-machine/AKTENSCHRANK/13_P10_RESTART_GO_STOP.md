# P10 – RESTART OHNE VERTRAUENSWÜRDIGEN ZWISCHEN-CHECKPOINT

Datum: 2026-09-08
Status: GO

## Idee

Keinen komplexen internen PREPARED-/Checkpoint-Zustand dauerhaft vertrauen.

Stattdessen:
- extern signierter Jobauftrag am Eingang
- extern signierte fertige Artikel am Ausgang
- unfertiger Artikel wird nach Crash vollständig neu gestartet
- nur gültig signierte fertige Artikel werden übersprungen

Damit keine interne Signaturkaskade und kein manipulierbarer Zwischencheckpoint.

## Laborlauf

9/9 PASS.

Positiv:
- gültig signierter fertiger Artikel wird übersprungen
- nächster unfertiger Artikel wird gewählt
- Restart beginnt exakt bei RESEARCH / Schritt 1
- wenn alle Artikel gültig abgeschlossen sind -> Batch fertig
- 100 Items im signierten Jobauftrag ohne künstliches Batchlimit

Negativ:
- manipulierter signierter Jobauftrag -> BLOCKED
- doppelte Item-ID, selbst korrekt signiert -> BLOCKED
- unvollständiges Finalpaket (Datei ohne Signatur) -> BLOCKED
- manipuliertes bereits fertiges Release -> BLOCKED
- korrekt signiertes Release für falsche Job-ID -> BLOCKED

## Gegenprüfung

### 0,0 Freiheit
PASS.
Resume entscheidet nicht heuristisch.
Es gibt nur:
- gültig signiert fertig -> überspringen
- noch nichts final vorhanden -> exakt dieses Item bei Schritt 1 starten
- inkonsistenter Zustand -> BLOCKED

### KISS
PASS.
Kein Zwischencheckpoint-Format.
Keine interne Signierung.
Keine PREPARED-/Restore-Kaskade.
Keine Handoff-Datei pro Mikroschritt.

### Sicherheit
PASS als Prinzip.
Nur extern signierte Jobdefinition und extern signierte Finalergebnisse gelten als dauerhaft vertrauenswürdig.

### Automatisierung
PASS.
Nach Crash kann der Prozess ohne Chatentscheidung den ersten nicht final abgeschlossenen Artikel bestimmen.

### Skalierung
PASS als Architekturprinzip.
Keine feste Artikelzahl; 100-Item-Job im Test.
Reale Ressourcen bleiben endlich.

### Nachhaltigkeit
PASS.
Crash-/Restart-Logik hängt nicht von einem konkreten Fachthema oder Raum ab.

## Historische Relevanz

M03 PREPARED Persist/Restore:
Die konkrete alte Fehlerklasse kann bei diesem Konzept strukturell entfallen.

M01 State-/Bundle-Kette:
Für laufende Mikroschritte ist kein dauerhaftes verteiltes State-Bundle nötig.
Dauerhafte Vertrauensanker sind nur signierter Job + signierte fertige Releases.

M29/M30 Batch-/Finalkontext:
Job-ID und Item-ID werden gegen signierte Finalreleases geprüft.

## Grenze

Der reale spätere Jobauftrag muss von einer autorisierten externen Stelle signiert sein.
Der Trust-Anker des öffentlichen Schlüssels muss im realen Deployment fest gebunden werden.

## GO/STOP

GO.

Nächste sinnvolle Prüfstufe:
P11 = vollständiges Mapping der bestehenden unveränderten Fachgates auf feste Mikroschritte der Zentralmaschine.

Noch keine Umsetzung aller Fachgates.
Zuerst nur beweisen, dass jedes bestehende Gate genau einen festen Platz hat und keines zusammengelegt, weggelassen oder frei gewählt wird.
