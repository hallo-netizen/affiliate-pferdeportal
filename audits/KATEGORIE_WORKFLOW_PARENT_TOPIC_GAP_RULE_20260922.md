# Kategorie-Workflow – Pflichtprüfung auf Parent-Topic-Gaps

Stand: 2026-09-22  
Bezug: Affiliate-Portal Kategorie-Workflow V1.8.0 / MASTER016-R10

## Erkannte Grundlücke

Ein sichtbarer Hub kann selbst ein konkretes, kaufnahes und portalspezifisches Suchthema sein, während seine vorhandenen Kinder nur Teilprodukte, Zubehör, Varianten oder Spezialfälle abdecken. Dann fehlt eine eigene aufnahmefähige Themen-/Produktfamilie für das Hauptthema.

Beispiel Pferde Atelier: `Sattel` enthält Satteldecken, Sattelgurte, Satteltransport usw., aber bisher keine eigene Produkt-/Artikelfamilie für Pferdesättel selbst.

## Neue Pflichtprüfung für künftige Portale

Jeder sichtbare Hub/Parent wird vor FINAL einzeln geprüft:

1. Ist der Parent selbst ein konkretes, eigenständiges und kaufnahes Thema des Portals?
2. Gibt es dafür genügend eigene Suchintentionen, Keywords und Themen?
3. Decken die vorhandenen Kinder nur Teilaspekte, Zubehör, Varianten oder Spezialfälle ab?
4. Fehlt dadurch eine direkte Produkt-/Themenfamilie für den Parent-Head-Intent?

Wenn 1–4 = JA: `PARENT_TOPIC_GAP` und vor FINAL strukturell lösen.

Keine automatische Ergänzung bei zu breiten Sammelbegriffen, biologischen/Wissensthemen oder bereits sauber durch Produkttypen abgedeckten Parents.

## Negativbeispiele Pferde Atelier

- Decken: bestehende Unterstruktur bildet relevante Produkttypen bereits sauber ab.
- Hufe: überwiegend biologisch/fachlich, kein kaufnaher Parent-Produktknoten nach dieser Regel.
- Boxen & Türen: für diese Regel nicht pferdespezifisch genug.
- Halfter & Stricke: als Sammelbegriff kein eigener zusätzlicher Parent-Produktknoten.

## Aktuell bestätigte fünf Fälle Pferde Atelier

1. Sattel
2. Trensen & Gebisse
3. Offenstall
4. Paddock
5. Reitplatz

## KISS-Umsetzungsprinzip

Kein Sonderpfad und kein Architekturumbau. Bestehenden Hub bei Bedarf breiter benennen; darunter genau einen konkreten neuen Produkt-/Themenknoten ergänzen. Bestehende Kinder bleiben erhalten.

Nach jeder solchen Strukturänderung zwingend:

`Kategorie-Workflow Delta/Regression -> WordPress Readback -> frischer Portal-/PSTE-Struktursnapshot -> Sandbox/Research-Neuzuordnung -> PSERC/Redaktionsplan-Neugenerierung -> Positiv-/Negativtest`.

Alte Struktur-Snapshots oder alte Redaktionsplan-Bindungen dürfen nicht still weiterverwendet werden.
