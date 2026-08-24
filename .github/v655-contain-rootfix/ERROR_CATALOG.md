# Fehlerkatalog – V6.55 Category Product CONTAIN Rootfix

## E1 – CSS-Box mit `contain` ohne echten Renderpfad als PASS gewertet
Status: geschlossen. Ein CSS-Deklarationstest ist kein visueller Nachweis.

## E2 – `cover` als Gleichgrößenlösung eingesetzt
Status: verworfen. `cover` schneidet Quer-/Hochformatquellen ab und erzeugte den live sichtbaren Zoom/Crop.

## E3 – WordPress-Pluginheader 6.54.0 bei interner Version 6.55.0
Status: Rootfix. Header wird auf 6.55.0 gesetzt und in echten WordPress-Installationen über `get_plugin_data()` geprüft.

## E4 – zweiter historischer `Stable tag: 6.48.0`
Status: Rootfix. Nur der aktuelle `Stable tag: 6.55.0` bleibt kanonische Metadatenzeile; der alte Eintrag wird als historisch gekennzeichnet.

## E5 – möglicher Sonderkonflikt beim ersten Produkt
Status: hart gegengeprüft. Browserfixture enthält absichtlich eine stärkere First-Slot-Regel mit falscher Größe/`cover`. Der echte Inline-Renderpfad muss trotzdem für alle drei Slots identische 150x150-Elemente und `contain` liefern.

## E6 – Vollständigkeit des Bildes nicht geprüft
Status: hart gegengeprüft. Querformat, Hochformat und Quadrat besitzen farbige Außenkanten. Pixelprüfung fordert alle vier Außenkanten plus die bei `contain` erwarteten Letterbox-Flächen. Crop/Zoom kann damit nicht als PASS durchlaufen.
