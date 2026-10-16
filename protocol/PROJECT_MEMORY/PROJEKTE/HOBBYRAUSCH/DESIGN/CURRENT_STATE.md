# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-16
STATUS: **1.50.650 GRUNDBASIS / 1.50.664–1.50.667 LIVE VERWORFEN / 1.50.668 REGISTRY-FUNDAMENT LOCAL HARD PASS / STRUKTUR-LIVEPASS ZUERST**

## Belastbarer Grundstand

Affiliate Portal Template Kit **1.50.650** bleibt die saubere technische Ausgangsbasis inklusive der bestätigten Bildreparaturen.

Die Zwischenstände **1.50.664, 1.50.665, 1.50.666 und 1.50.667 sind nicht freigegeben**:
- Mega-Menü live falsch;
- Kategorietext live nicht korrekt;
- Strukturquelle im Design grundlegend falsch;
- deshalb nicht weiterverwenden.

## Gefundene Systemursache

1.50.650 las Hobby-Unterseiten mit rohem WordPress-`get_pages()`.
Folgen:
- alte/fremde WordPress-Seiten konnten in Karten/Navigation erscheinen;
- echte `category`-Kinder terminaler Hobbyseiten waren unsichtbar;
- die zentrale HD-001/HD-004-Struktur wurde umgangen.

Zusätzlich existierte ein Weltbild-Fallback, der bei fehlendem exaktem Kartenbild ein thematisch fremdes Bild liefern konnte.

## Registry-Fundament 1.50.668 – LOCAL HARD PASS

Artefakt:
`/hobby rausch/releases/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.668_HOBBY_DEPOT_REGISTRY_FOUNDATION_LOCALPASS.zip`

SHA-256:
`0fb575aeddd19aac285188507d0753eaa554b558183d6686c2a900322c865a5a`

QA:
`/hobby rausch/releases/HOBBY_DEPOT_REGISTRY_FOUNDATION_150668_QA_20261016.json`

Exaktes Delta zu 1.50.650:
- 981 → 984 Dateien;
- 3 neue versionsgebundene PHP-Dateien;
- Hauptplugin geändert;
- 0 Dateien entfernt;
- 0 Bilddateien verändert;
- PHP 58/58 PASS;
- ZIP-Roundtrip 984/984 byte-identisch.

Technik:
- HD-004 Registry ist einzige CORE-Strukturquelle;
- keine rohen `get_pages()`-Kinder mehr für Hobby-Navigation/Karten;
- Page- und Category-Kinder getrennt korrekt;
- letzte Ebene unter terminalen Hobbyseiten wird sichtbar;
- tiefe Hub2-Ebene = Icon/Text statt Fotoflut;
- Weltbild-Zufallsfallback entfernt;
- auch Term-Kinder lesen Registry;
- fehlt Registry: fail-closed, **kein stiller Rückfall auf 1.50.650**.

## Positiv-/Negativsimulation

Synthetischer WordPress-Bestand enthält absichtlich falsches Trainspotting unter Messen & Analysieren.

PASS:
- rohes WordPress sieht Trainspotting;
- Registry-Renderer blendet es dort aus;
- Messen & Analysieren = Bodenanalyse / Elektrochemie als Hobby / Spektroskopie / Wasseranalyse;
- Ameisenhaltung = 7 echte Inhaltskategorien;
- Spotting & Verkehr = Car / Plane / Ship / Trainspotting;
- 0 Fotokarten auf der tiefen Ebene;
- fehlende Registry → 0 erratene Kinder.

Browser mit echtem Plugin-CSS:
1440 / 1024 / 768 / 390 px PASS, 0 horizontaler Overflow.

## Wichtig

1.50.668 repariert bewusst **noch nicht** das gescheiterte Mega-Menü oder den Kategorietext. Erst Struktur-Livepass, dann Design Ebene für Ebene.

## EXAKT EINE NEXT ACTION

**Zuerst V3-Struktur über HD-001 echten WordPress-Dry-Run und anschließend kontrollierten Sync/Readback freigeben. Danach HD-004 + 1.50.668 live als Fundament prüfen. Erst danach Mega-Menü und Kategorietext neu aufbauen.**
