# P2 – FESTE TEXTMASCHINEN-SCHNITTSTELLE

Datum: 2026-09-08
Status: GO ALS SCHNITTSTELLEN-PROTOTYP, KEIN ECHTER TEXTMASCHINEN-PRODUKTIONS-PASS

## Ziel

Prüfen, ob die bestehende Textmaschine später über genau EINE feste, nicht frei steuerbare Schnittstelle an die Zentralmaschine angebunden werden kann, ohne die Textmaschine selbst zu verändern.

## Vorprüfung gegen den realen Bestand

Der aktuelle reale Fachworkflow zeigt bereits einen festen Produktionspfad:
`PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan`.

Dabei sind im bestehenden Code bereits fest gebunden:
- PPM 6.7.9
- PPM-Paket-SHA-256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
- Text-/Artikeltyp-Regelsatz-SHA-256 `dc79a6d7d30fba2f7f13c80d35bf4d137669f2b3469d7bc28a5d0873858f192f`
- Fact-Pack
- production_plan_item
- production_plan_header
- finaler Artikelhash
- fail-closed PPM-Ergebnis

Der reale 6-Artikeltest vom 28.08.2026 hat diesen bestehenden Fach-/Produktionsverbund bereits erfolgreich ausgeführt, ohne Textmaschine/PPM/LanguageTool/Fachregeln zu verändern.

Folgerung:
Es ist grundsätzlich plausibel, den unveränderten bestehenden Produktionskern hinter EINER festen Maschinen-Schnittstelle aufzurufen.

## Wichtige P0-Korrektur vor P2

Die Gegenprüfung fand noch eine unzulässige P0-Freiheit:
Der Dummy-Finalcheck konnte selbst `all_required_checks_passed=true` melden.

Das war ein Selbstattest und damit kein echter harter Prüfer.

KISS-Korrektur:
- generisches `submit(...)` entfernt
- kein frei übergebbarer Validator
- kein `submit_final_check`
- Zentralmaschine besitzt nur noch drei explizite Aktionen:
  1. `submit_research`
  2. `run_textmachine`
  3. `run_final_check`
- Finalcheck berechnet sein Prototyp-PASS selbst

Damit wurde P0 vor P2 strenger UND einfacher.

## P2-Prototyp

Die echte Textmaschine wurde NICHT angefasst und NICHT kopiert.

Stattdessen wurde für den isolierten Architekturtest ein kleiner eingefrorener Stub verwendet, der die spätere feste Paketgrenze simuliert.

Eigenschaften:
- fester Dateipfad
- fester SHA-256
- fester Contract
- kein Runtime-Parameter für Engine/Pfad
- relevante Environment-Overrides werden nicht als Steuerweg akzeptiert
- Zentralmaschine ruft Worker 2 selbst auf
- Worker 1 kann keinen Draft einschleusen
- Worker 2 kann nur exakt gebundenen Item-/Fact-Kontext zurückgeben
- Kontextdrift = BLOCKED
- Maschinen-Dateidrift = BLOCKED
- Worker 3 / Finalcheck ist nicht extern selbstattestierend

## Lokaler Positiv-/Negativtest

12/12 PASS.

Positiv:
- feste 3-Stufen-Reihenfolge
- unveränderlicher Maschinenaufruf
- vier völlig verschiedene Themen PASS
- 25 vollständige subprocess-basierte Artikelinstanzen PASS

Negativ:
- Textmaschine vor Recherche aufrufen -> BLOCKED
- Engine im Konstruktor wählen -> technisch nicht möglich
- Engine per Environment überschreiben -> wirkungslos
- Textmaschinen-Datei verändern -> HASH-BLOCKED
- Research-Worker versucht Draft einzuschleusen -> BLOCKED
- externer Validator-/next-step-API existiert nicht
- Final-PASS kann nicht extern behauptet werden
- P1-Regelverletzung aus Maschinenoutput -> BLOCKED
- Finalcheck vor Textmaschine -> BLOCKED

Hinweis Lasttest:
Ein erster 200-Subprocess-Test überschritt lediglich die lokale Testlaufzeit; es trat bis zum Timeout kein fachlicher Testfehler auf.
Für den P2-Schnittstellenbeweis wurde der Test auf 25 echte Prozessaufrufe begrenzt.
P0 hatte bereits 1.000 unabhängige In-Process-Artikelinstanzen PASS.
Dies ist kein behaupteter Performance-Benchmark.

## Zwingende Gegenprüfung

### 0,0 Workflowfreiheit
PASS im P2-Prototyp.
Kein Worker kann Schritt, Folgeschritt, Validator oder Engine wählen.

### Einfluss von außen
PASS für die getestete Schnittstelle.
Pfad-/Engine-/Environment-/Output-Manipulationen werden ignoriert oder BLOCKED.

Noch nicht behauptet:
Schutz gegen feindlichen Code mit direktem Schreibzugriff auf den Zentralmaschinen-Quellcode selbst. Das ist später Aufgabe der äußeren Repository-/Release-Sicherung, nicht eines zusätzlichen internen Controllers.

### KISS
PASS.
Kein neuer Controller-Zoo.
Ein Kern, drei explizite Aktionen, ein eingefrorener Maschinenstub nur für den Test.
Die P0-API wurde sogar verkleinert.

### Nachhaltigkeit
PASS als Architekturprinzip.
Die spätere echte Textmaschine kann als eingefrorene Komponente hinter derselben festen Grenze liegen, statt ihre internen Schritte in der Zentralmaschine nachzubauen.

### Textmaschine unverändert
PASS.
Keine Datei der echten Textmaschine/PPM wurde geändert.

### Themenunabhängigkeit
PASS im Prototyp.
Pferdedecke, Kaffeemühle, Photovoltaik und Steuerrecht liefen über dieselbe Architektur.

### Automatisierung
PASS.
Nach Research-PASS sind Maschinenaufruf und Finalcheck fest vorgegeben; kein Chat entscheidet den Folgeschritt.

### Skalierung
PASS als Architekturprinzip.
Kein festes Batchlimit im Modell. Artikel sind unabhängige Zustandsinstanzen.
Reale Parallelität/Leistung hängt selbstverständlich von vorhandenen Rechenressourcen ab.

### Weniger fehleranfällig als bisher
VORLÄUFIG PASS.
Für Worker 2 gibt es:
- keinen neuen Raum
- kein frei formuliertes Handoff
- keinen Neuaufbau der Workflowentscheidung
- keinen wählbaren Enginepfad
- genau einen Zustandseigentümer

## GO/STOP

GO.

P2 zeigt keine Sackgasse und keine Notwendigkeit für zusätzliche Kontrollschichten.

ABER:
Noch kein echter PPM/Textmaschinen-Lauf innerhalb der Alternativmaschine.
Der nächste spätere Beweis müsste den Stub 1:1 durch den bereits vorhandenen, hashgebundenen realen PPM/PSERC-Einstieg ersetzen, ohne Textmaschine oder deren Regeln zu ändern.

Wenn dafür mehrere neue Handoffs, Runtime-Entscheidungen oder zusätzliche Controller nötig würden:
STOP.
