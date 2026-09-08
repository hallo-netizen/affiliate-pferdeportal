# P35 – FESTER 7/7-GOLDSTANDARD + NEUTRALER REALINTEGRATIONSTEST

Datum: 2026-09-08
Status: TESTPLAN EINGEFROREN

## Historischer 7/7-Goldstandard

Autoritative Quelle:
`control/startmaster0107/recovery_sources/7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a/MANIFEST.json`

Batch:
`7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`

Source Commit:
`f4df3847ab4d807a71e82104fd5e1151eff98f2e`

Item Count:
7

Die sieben historischen Artikel bleiben unverändert als Goldstandard für:
- Batch-Identität
- Dateiintegrität
- SHA-Bindung
- 7er-Kardinalität
- deterministische Reihenfolge

Sie werden NICHT umgeschrieben.

## Integrationsstrategie

KISS:

1. zuerst EIN neutrales Testitem
2. vollständiger Zielweg
3. positiver + negativer Test
4. nur bei PASS derselbe Weg mit sieben Items
5. erst danach historische 7/7-Dateien als reale Inhaltsreferenz anbinden, wenn deren heutige Plan-/Fact-Pack-Kontexte noch sauber auflösbar sind

Damit blockiert ein historischer Plan-Slot nicht die Architekturprüfung.

## Erlaubtes neutrales Thema

Für den isolierten Integrationsprototyp darf ein künstliches, fachneutrales Thema verwendet werden.

Beispiel:
`Regenwasserspeicher für einen kleinen Garten auswählen`

Kein Produktionsinhalt.
Kein Publish.
Keine Änderung am Pferde-Portal.

## STOP-Regel

Wenn ein künstliches Thema nur durch Umgehung echter PPM-Verträge möglich wäre:
STOP.

Dann wird stattdessen ein vorhandener echter Fixture-/Planfall verwendet.

Keine Sonderlogik nur für den Test.
