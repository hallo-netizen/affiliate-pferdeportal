# HOBBYRAUSCH – DESIGN CONSISTENCY AUDIT

STAND: 2026-10-15
ROLLE: Konsistenznachweis für den aktuellen Bildquellen-WIP.
KEINE eigene Current-Autorität.

## Geprüfter Stand
Branch:
`hobbyroom/project-memory-campus-v1-20260905`

Geprüfter Head vor diesem Audit:
`88d9cfe8639512ed027664cdd4d22b41a099d661`

## Current-/Plugin-Bindung
PASS:
- 1.50.650 bleibt eingefrorener aktiver Grundstand.
- 1.50.651–1.50.663 bleiben gesperrt.
- kein Plugin-Nachfolger freigegeben.
- Release weiterhin gesperrt.
- kein Mapping-/PHP-/CSS-/Template-/Architekturumbau.

## 30er-Quellenblock
PASS:
- 30 Kategorien insgesamt.
- 7 echte neue Einzelquellen vorhanden.
- 13 neue Richtungen exakt an Nach-1.50.663-Referenzen gebunden.
- 6 Kategorien nur als Bestandteil des vom Nutzer akzeptierten neuen 8er-Blocks belegt; **keine konkrete Motivrichtung erfunden**.
- 4 Kategorien ohne rekonstruierbare neue Bindung.
- damit 7 + 13 + 6 + 4 = 30.

## 7 vorhandene Quellen
PASS:
- 7/7 echte Quellendateien an exakte Datei-IDs gebunden.
- 7/7 Quellen-SHA-256 gegen rematerialisierte Bytes bestätigt.
- 7/7 Hero-Ausschnitte 600×320 visuell PASS.
- 7/7 Preview-Ausschnitte 200×107 visuell PASS.
- 0 Upscaling.
- 0 technische Nah-Dubletten.
- WIP-Archiv SHA-256:
  `bae7d84034b6d011d566927cd4193b4b74f223c6c9b1b87ef5cc6275f0bda9bb`.

## 13 exakt gebundene Richtungen
PASS:
- aktive Datei: `HERO_REFERENCE_CROPS_13_V2_20261015.json`.
- 13/13 eindeutige Kategorien.
- 13/13 eigene V2-Referenzcrop-Dateien.
- 13/13 eindeutige Crop-Datei-IDs.
- 13/13 eindeutige SHA-256.
- Uploadbytes 13/13 erneut materialisiert und hash-verifiziert.
- Keramik & Glas korrekt aus dem echten **4×3**-Raster, R2C1.
- Technik & Medien korrekt aus dem echten **5×2**-Raster, R2C1.
- übrige aktive Referenzen aus 4×2-Rastern.
- alte Crop-Tabelle ist als SUPERSEDED markiert.

## Generierungsqueue
PASS:
- aktive Datei: `HERO_GENERATION_QUEUE_13_WIP_20261015.json`.
- exakt 13 Positionen.
- 13/13 Kategorien eindeutig.
- 13/13 exakte Referenzcrop-Datei-ID.
- 13/13 exakter Referenzcrop-SHA.
- 13/13 deterministischer zukünftiger Quellname.
- 13/13 eindeutiger Hero-Zielpfad.
- 13/13 eindeutiger Preview-Zielpfad.
- alte überbreite 19er-Queue gelöscht.
- keine geratenen Motivrichtungen.
- keine Vorschau-Runde.

## Blocked
Exakt 10 Kategorien bleiben ohne ausführbare Generierung:
- Heimwerken;
- Robotik & Automation;
- Wirbellose;
- Wind & Drachen;
- Klettern & Seil;
- Wasser;
- Alltagsobjekte;
- Naturfunde;
- Spielzeug & Spiele;
- Münzen & Geld.

Grund:
Für diese 10 existiert keine exakte neue Motivbindung. Bei den ersten sechs ist nur die Zugehörigkeit zum akzeptierten neuen 8er-Block belegt. Für die letzten vier ist gar keine neue Bindung rekonstruierbar.

## Maße / Release-Gate
PASS:
- aktueller Hero-Bildersatz: **600×320**.
- Preview: **200×107**.
- alte 600×220-Werte sind als historisch/falsch markiert.
- `RELEASE_GATE_20261013.md` ist auf 600×320 korrigiert.
- das 30er-Quellengate ist ausdrücklich nur Untergate des globalen 65-Hero-/328-Karten-Gates.

## Ergebnis
**KONSISTENZ PASS.**

Es gibt aktuell keine zweite freigegebene Pluginwahrheit und keinen erlaubten Rückgriff auf alte Bildstände.

Offen bleibt ausschließlich:
1. 13 exakt gebundene Richtungen in echte neue Einzelquellen überführen;
2. für 10 BLOCKED-Kategorien erst eine echte neue Motivbindung herstellen;
3. danach 30/30 Motiv-PASS;
4. erst dann einmaliger reiner 60-Dateien-Image-only-Kandidat;
5. danach globales Release-Gate und Live-Readback.


## Vollständiger 30er-Overlay-Volltest
Zusätzlich wurde der komplette 30-Kategorien-/60-Bilddateien-Pfad gegen die echte 1.50.650-Basis mit synthetischen Testbildern durchlaufen.

Erster Lauf:
- exakt ein Zielpfadfehler gefunden: Münzen-&-Geld-Preview;
- Ursache: Hero historisch `munzen-`, Preview-Renderer-Alias `muenzen-`;
- als AF-041 dokumentiert und Manifest korrigiert.

Zweiter Lauf:
- 30/30 Kategorien;
- 60/60 Zielpfade vorhanden;
- exakt 60 Bilddateien geändert;
- 0 Dateien hinzugefügt;
- 0 Dateien entfernt;
- 0 unerwartete Änderungen;
- Mapping byte-identisch;
- ZIP-Roundtrip PASS.

Die synthetische Test-ZIP wurde nach dem technischen Nachweis lokal gelöscht und ist kein auslieferbares Artefakt.

## Bildgenerator-Fehlpfad
Zwei fachfremde Plugin-/Statusgrafiken wurden als AF-040 hart quarantänisiert und zählen als Quelle 0. Sie sind weder im Manifest noch im Buildpfad gebunden.
