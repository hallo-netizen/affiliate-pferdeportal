# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.50.650 GRUNDBASIS / 1.50.664–1.50.667 VERWORFEN / 1.50.668 REGISTRY + MEGA-MENÜ + HUB2-TEXT + HERO→PREVIEW LOCAL HARD PASS / LIVE READBACK OFFEN**

## Belastbarer Grundstand

Affiliate Portal Template Kit **1.50.650** bleibt die saubere Ausgangsbasis inklusive HRD-SCOPE13-Bildreparaturen.

Nicht verwenden:
- 1.50.664;
- 1.50.665;
- 1.50.666;
- 1.50.667.

## Gefundene Systemursache

Der alte Designstand las Struktur teilweise über rohe WordPress-`get_pages()`-Kinder.
Dadurch:
- konnten Altseiten wie Trainspotting an falschen Stellen erscheinen;
- blieb die echte terminale `category`-Ebene unsichtbar;
- wurde die zentrale HD-001/HD-004-Struktur umgangen.

Zusätzlich existierte ein thematisch unsicherer Weltbild-Fallback.

Die Reparatur folgt dem bewährten Hab-&-Bewahr-0.1.20-Prinzip:
**zentrale Struktur ist einzige Wahrheit; bei vorhandener Revision kein stiller WordPress-/Bundled-Fallback; keine Geschwister als Ersatz-Kinder.**

## Kandidat 1.50.668 – LOCAL HARD PASS

Artefakt:
`/hobby rausch/releases/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.668_HOBBY_DEPOT_REGISTRY_NAV_TEXT_HEROPREVIEW_HARDPASS.zip`

SHA-256:
`ee521c5f8b360c16d641e77507b94b64b93432da701e4760e7c4daa67d9440b6`

QA:
- `/hobby rausch/releases/HOBBY_DEPOT_1.50.668_BROWSER_ACCEPTANCE.json`
- `/hobby rausch/releases/HOBBY_DEPOT_1.50.668_FINAL_DIFF.json`

## Struktur-/Renderer-Reparatur

- HD-004 Registry = einzige CORE-Strukturquelle;
- zentrale Revision vorhanden + Registry nicht bereit → fail closed;
- keine rohen `get_pages()`-Kinder als Strukturwahrheit;
- keine Geschwister-Ersatzlogik;
- Page- und `category`-Kinder getrennt korrekt;
- Ameisenhaltung zeigt exakt 7 terminale Inhaltskategorien;
- absichtlich falsch physisch einsortiertes Trainspotting wird unter Messen & Analysieren ausgeschlossen;
- V3-Spotting-Hub rendert Plane/Train/Ship/Car Spotting korrekt;
- Weltbild-Zufallsfallback aus aktivem Renderer entfernt.

Vollsimulation:
- aktuelle 330er Live-Baseline: 0 Strukturabweichungen;
- V3 mit 370 terminalen Hobbyseiten / 2160 Leafs: 0 Strukturabweichungen.

## Mega-Menü

- alle 8 Welten aus Registry;
- >=761 px alle 8 Hauptwelten in einer Zeile;
- zunächst grafisch gleichmäßig bis zu 5 direkte Gruppen;
- genau eine zusätzliche Orientierungsebene;
- max. 4 Links je sichtbarer Gruppe + `Alle Themen` falls nötig;
- `Mehr Kategorien` klappt restliche Gruppen im selben Flyout auf;
- kein Vollbaum / keine zusätzliche Verschachtelung;
- Mobil eigenes sauberes Verhalten.

## Hub2-Kategorietext

Vertrag umgesetzt:
- Hero: Schreibschrift-Claim + H1 + kurzer Einstieg;
- längerer Text **unter** dem Hero;
- sichtbarer Lead;
- mittig `Mehr zu <Kategorie> erfahren`;
- Rest im Aufklapper;
- Öffnen verändert Hero-Höhe um 0 px;
- >1100 px Text/Bild nebeneinander;
- <=1100 px Text → Bild → langer Text darunter.

## Hero → Kategorievorschau

- 65/65 bestehende direkte Hub2-Previews aus dem jeweils aktuellen Hero neu abgeleitet;
- Preview exakt 200×107;
- 65 gemappte Hero-Dateien byte-identisch zum eingefrorenen Ausgangsstand;
- keine unabhängige zweite Bildquelle.

## Browser-Abnahme lokal

Echter Headless-Browser mit realem Plugin-HTML/CSS:
- 1920 / 1440 / 1101 / 1100 / 1024 / 768 / 761 / 760 / 390 geprüft;
- alle 8 Mega-Menüs geprüft;
- `Mehr Kategorien` positiv/negativ geprüft;
- kein horizontaler Overflow;
- 1101 = Desktop-Hero, 1100 = gestapelt;
- 761 = Desktopnavigation mit 8 Welten, 760 = Mobilmenü;
- Text-Aufklapper verändert Hero-Höhe um 0 px.

Technik:
- PHP 58/58 PASS;
- ZIP PASS;
- ZIP-Roundtrip 984/984;
- 0 Dateien entfernt;
- 0 Hero-Dateien verändert.

## V3-Hinweis

Der V3-Strukturkandidat ist **noch nicht live**.
Er fügt fünf neue direkte Hub2-Bereiche hinzu:
- Spotting & Verkehr;
- Citizen Science;
- Natur bestimmen;
- Suchen & Finden;
- Modellbau.

Bevor diese fünf neuen Hub2 live freigegeben werden, brauchen sie gemäß Bildvertrag jeweils eigenes geprüftes Hero + daraus abgeleitete Preview. Kein generisches Weltbild als stiller Fallback.

## PASS-GRENZE

**Kein Live-PASS ohne echten WordPress-Readback.**

## EXAKT EINE NEXT ACTION

**Zuerst HD-004 als Runtime-Registry live bereitstellen und danach 1.50.668 gegen die bestehende 330er Live-Baseline prüfen. V3-Struktur erst nach eigenem Dry-Run und nach Bildern für die fünf neuen Hub2 synchronisieren.**
