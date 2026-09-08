# P7 – MINIMALER ÄUSSERER HOCHSICHERHEITSTRAKT

Datum: 2026-09-08
Status: GO

## Ziel

Nach der fertigen Dateiausgabe darf weder Chat, Worker noch irgendeine nachträgliche Änderung unbemerkt bis WordPress gelangen.

KISS-Ziel:
- ein kanonisches Ausgabepaket
- externe Signatur
- ein Importprüfer mit öffentlichem Schlüssel
- keine interne Signatur
- kein Auto-Publish

## Prototyp

Die Produktionsseite kann nur:
- ein kanonisches Release-Paket bauen
- dieses Paket ausgeben

Sie besitzt KEINE Signierfunktion und KEINEN privaten Schlüssel.

Der Importprüfer:
- akzeptiert nur das exakte Release-Schema
- verlangt publish_allowed=false
- prüft den Content-Hash
- verlangt kanonische Bytes
- prüft die externe Ed25519-Signatur mit dem öffentlichen Schlüssel
- liefert nur IMPORT_VERIFIED_NO_PUBLISH oder BLOCKED

## Isolierter Laborlauf

9/9 PASS.

Positiv:
- unverändertes extern signiertes Paket -> IMPORT_VERIFIED_NO_PUBLISH

Negativ:
- fehlende Signatur -> BLOCKED
- falscher öffentlicher Schlüssel -> BLOCKED
- Payload nach Signatur verändert -> BLOCKED
- Payload verändert UND Hash passend neu berechnet -> Signatur trotzdem BLOCKED
- publish_allowed=true, sogar korrekt neu signiert -> BLOCKED
- zusätzliches Feld/Anweisung, sogar korrekt neu signiert -> BLOCKED
- semantisch gleiche, aber anders formatierte JSON-Datei, sogar neu signiert -> BLOCKED, weil nicht kanonisch
- Produktionsmodul enthält keine private-key-/Signierfähigkeit

## Gegenprüfung

### 0,0 Freiheit
PASS.
Der Importprüfer entscheidet nicht frei.
Exaktes Schema + Hash + Signatur + no-publish -> PASS.
Sonst BLOCKED.

### Einfluss nach Dateiausgabe
PASS für Manipulation der ausgegebenen Bytes.
Nachträgliche Änderung kann auch durch Neuberechnung des normalen Hashes nicht versteckt werden, weil die externe Signatur bricht.

### KISS
PASS.
Eine Release-Datei, eine Signatur, ein öffentlicher Prüfschlüssel.
Keine Signierkette und keine interne Signatur.

### Worker angekettet
PASS für die Produktionsschnittstelle.
Der Produktionscode kann nicht selbst signieren.

Noch separat hart zu beweisen:
Der spätere reale Signer muss auch auf Prozess-/Credential-Ebene außerhalb des Produktionsworkers liegen.
P7 beweist bereits die API-/Code-Trennung, aber noch nicht die reale Credential-Isolation.

### WordPress
Noch kein realer WordPress-Import.
Bewiesen ist nur die vorgesehene fail-closed Eingangsprüfung.
Kein WordPress-Schreiben und kein Publish im Test.

## GO/STOP

GO.

Nächster sinnvoller Makrotest:
P8 = ausschließlich die Credential-/Prozess-Trennung des externen Signers beweisen.
Producer darf den privaten Schlüssel technisch nie besitzen.
Signer erhält nur das fertige Release.
Importer erhält nur Release + Signatur + öffentlichen Schlüssel.

Wenn dafür im Produktionskonzept mehr als genau diese eine externe Signierstufe nötig wäre:
STOP.
