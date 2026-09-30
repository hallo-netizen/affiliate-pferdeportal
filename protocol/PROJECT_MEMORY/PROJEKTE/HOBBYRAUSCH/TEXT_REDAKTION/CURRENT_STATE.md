# HOBBYRAUSCH – TEXT_REDAKTION – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: HD-002 V0.1.1 LIVE-MIGRATION PASS / PRODUKTIVER KATEGORIE-OWNER-STAND FEHLT / GESAMTBESTAND NOCH NICHT ERFASSEN

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_TEXT_REDAKTION`.

## Live-Stand

Installiert:
`Hobby Depot SEO Themenengine 0.1.1`

Die sichere Migration ist live vollständig abgeschlossen.
Backend ist erreichbar und READY.

V0.1.0 bleibt superseded.

## Aktueller sichtbarer Zustand

Übersicht zeigt:
- Beiträge: 0;
- Themenfamilien: 0;
- nutzbare Kategorien: 0;
- Website-Gesamtbild: NOT CAPTURED;
- DataForSEO: NICHT EINGERICHTET;
- Portalabgleich: NOT STARTED.

## Wichtige Sperre vor „Gesamtbestand erfassen“

Der bisherige HD-001-Lauf war ein Testlauf und wurde vollständig zurückgerollt.

Die dafür verwendete Testdatei:
`kategorie-read-only-preview-hobby-depot-testlabor-20260928.json`

enthält:
- 20 Strukturknoten;
- 27 `ARTICLE_ONLY`-Entscheidungen;
- davon 27 ohne `owner_concept_id`.

Damit ist deren Editorial-Ownership-Handoff nicht produktionsbereit.

Außerdem sind die Testkategorien nach Rollback nicht live vorhanden.

Deshalb jetzt NICHT:
`Gesamtbestand erfassen`.

## Technischer Folgepunkt

HD-002 besitzt bereits den technischen Handoff-Importer, aber der produktive Owner-Handoff muss aus einem echten, nicht zurückgerollten Hobby-Depot-Kategorienstand stammen.

Ein lokaler Folgefix wird vorbereitet, damit HD-002 einen gültigen installierten HD-001-Handoff später automatisch read-only übernehmen kann. Das ersetzt aber nicht den fehlenden produktiven Kategorienstand.

## NEXT ACTION

Zuerst echten Hobby-Depot-Kategorienstand für den Buchbinden-Pilot erzeugen und live bereitstellen.

Pilotpfad:
`Fertigen → Buch & Papier → Buchbinden`

Aktuell datenbelegt:
- Einstieg;
- Ausrüstung;
- Material;
- Techniken/Praxis.

Noch nicht datenbelegt:
- Fragen/Probleme;
- FAQ.

Erst nach live vorhandenem, gültigem Owner-Handoff:
Gesamtbestand erfassen → DataForSEO anbinden → Buchbinden-Recherche.
