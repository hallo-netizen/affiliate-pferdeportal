# P36 – EIN DÜNNER KISS-REALCONTROLLER

Datum: 2026-09-08
Status: GO

## Ziel

Keine weitere Architektur.

Genau eine Controller-Datei:
`prototype/p36_kiss_real_controller.py`

## Controller kann nur

1. signiertes Jobmanifest verifizieren
2. Items exakt in Manifest-Reihenfolge abarbeiten
3. für jedes Item exakt den festen bereits geprüften Ein-Item-Adapter aufrufen
4. PASS-Receipt sammeln
5. bei erstem Fehler sofort stoppen
6. nie publishen

## Nicht vorhanden

- set_next_step
- choose_worker
- set_validator
- set_route
- set_engine
- alternative_route

Keine frei wählbare Route.
Kein frei wählbarer Worker.
Kein frei wählbarer Validator.
Kein frei wählbarer Reparaturpfad.

## Tests

5/5 PASS.

Positiv:
- 7 Items -> exakt 7 Aufrufe in Manifestreihenfolge
- completed_count = 7
- publish_allowed=false

Negativ:
- manipuliertes signiertes Jobmanifest -> BLOCKED bevor Itemadapter läuft
- doppelte Item-ID -> BLOCKED bevor Itemadapter läuft
- Itemadapter-Fehler bei Item 2 -> sofortiger STOP; Item 3/4 werden nicht gestartet
- statisch keine Runtime-Auswahl-API

## Gesamtregression

P0 bis P36 gemeinsam PASS.

## Wichtige offene Integrationsfrage

P36 beweist bereits:
Job-Identität, Reihenfolge und Workerpfad.

Noch separat hart zu beweisen:
Ein konkretes Job-Item muss an exakt den konkreten PPM-prepared Content gebunden sein.

Kein Item-A/Item-B-Tausch darf vor oder nach der Signatur möglich sein.

Das ist P37.

Keine neue Architektur.
Nur bestehende Item-ID + bestehender Prepared-Payload + bestehende externe Signatur miteinander binden.
