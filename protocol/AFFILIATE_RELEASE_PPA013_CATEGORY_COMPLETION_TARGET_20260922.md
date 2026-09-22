# PPA-013 Kategorieabschluss – Zielvertrag 2026-09-22

Rolle: autoritative Zielquelle für den ausdrücklich beauftragten Kategorie-/Darstellungsabschluss am Pferde Atelier.
Diese Datei ist KEINE Status-/CURRENT-/NEXT-ACTION-Quelle. Dynamischer Stand ausschließlich in `control/release-governance/CURRENT_RELEASE.json`.

## Zielstruktur

Die bestehenden Oberkategorien bleiben erhalten. Neue Themenknoten werden als direkte Unterseiten geführt:

- `Sattel & Zubehör` (Seite 108) bleibt Oberkategorie; `Pferdesättel` (972134) ist direkte Unterseite und steht an Position 1.
- `Trensen & Gebisse` (109) bleibt Oberkategorie; `Trensen` (972141) ist direkte Unterseite und steht an Position 1.
- `Offenstall` (110) bleibt Oberkategorie; `Offenstallbau` (972148) ist direkte Unterseite und steht an Position 1.
- `Paddock` (119) bleibt Oberkategorie; `Paddockbau` (972155) ist direkte Unterseite und steht an Position 1.
- `Reitplatz` (120) bleibt Oberkategorie; `Reitplatzbau` (972162) ist direkte Unterseite und steht an Position 1.

Vorhandene Unterkategorien und vorhandene Beitrags-/Artikelzweige unter Offenstall und Reitplatz bleiben erhalten und werden nicht umgehängt oder umbenannt.

## Ausrüstung – sichtbare Reihenfolge

Unter `Ausrüstung` (95) gilt die Reihenfolge:
1. Sattel & Zubehör (108)
2. Trensen & Gebisse (109)
3. Decken (103)
4. Reiterbedarf (107)
5. Halfter & Stricke (105)
6. Deckenzubehör (104)
7. Pflegezubehör (106)

Zweck: Bei der bestehenden Flyout-Grenze von fünf Einträgen müssen Sattel & Zubehör und Trensen & Gebisse sichtbar sein. Keine globale Aufhebung der 5er-Grenze.

## Kachel-Icons

PPA-013 `Pferde Template Kit` ist zuständig.
Hub-2-Kacheln müssen ihr Icon aus dem jeweiligen Kachelthema ableiten, nicht pauschal das Eltern-/Hero-Icon verwenden.
Für die fünf neuen Themen dürfen vorhandene passende Iconfamilien wiederverwendet werden:
- Pferdesättel -> Sattel
- Trensen -> Trensen & Gebisse
- Offenstallbau -> Offenstall
- Paddockbau -> Paddock
- Reitplatzbau -> Reitplatz

Bestehende Kachel-/Iconlogik außerhalb dieses Scopes bleibt unverändert.

## Sieben Unterkategorien

Bei exakt sieben Hub-2-Unterkategorien gilt auf Desktop:
- erste Reihe: 3 Kacheln
- zweite Reihe: 4 Kacheln

Tablet bleibt 2-spaltig, Mobil 1-spaltig. Andere Kachelanzahlen bleiben unverändert.

## Kategorietexte

Nur die fünf neu angelegten Kategorien werden neu geschrieben:
- Pferdesättel
- Trensen
- Offenstallbau
- Paddockbau
- Reitplatzbau

Verbindliche Qualitätsregeln:
- 150–200 Wörter;
- natürliches Deutsch;
- themenspezifische Substanz;
- keine Generator-/Schablonensprache;
- keine Padding-Sätze;
- keine generischen Schlussformeln;
- bestehende gute Texte bleiben vollständig unberührt.

Die Texte müssen inhaltlich zur tatsächlichen Position im Seitenbaum und zu vorhandenen Unterkategorien/Beitragszweigen passen.

## Nicht verändern

- PPA-001 Affiliate-Zentrale;
- `pa-affiliate-design-performance` und dessen Performanceverhalten;
- Kubio;
- Astra/Theme;
- Banner-/Affiliate-Semantik und Daten;
- bestehende Offenstall-/Reitplatz-Unterseiten und deren Beitragszuordnungen;
- gute bestehende Kategorietexte.

## Abnahme

- Struktur-/Menüreihenfolge read-back bestätigt;
- PPA-013-Änderung fail-closed gegen den bestätigten Live-Stand;
- Performance-Helfer SHA-identisch;
- PHP-/Paket-/Fresh-Unpack-Prüfung des verwendeten Hilfsartefakts;
- Desktop 7er-Raster 3/4, Tablet 2, Mobil 1;
- neue Kacheln zeigen passende Icons;
- fünf neue Kategorietexte jeweils 150–200 Wörter und Regelcheck PASS;
- erst danach temporäre Hilfsplugins entfernen.
