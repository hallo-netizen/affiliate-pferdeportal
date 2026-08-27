# Affiliate-Zentrale V6.61.4 – Product Card Triple/Image Rootfix

## Anlass
V6.61.3 ist nach realer Sichtprüfung verworfen. Sichtbare Fehler waren fehlende eBay-Bilder, ein defektes idealo-Bild und dadurch leere bzw. unvollständige Produktpositionen sowie nicht belastbar gleiche Karten.

## Ursachenkorrektur
- **eBay:** Die öffentliche Produktkarte hängt nicht mehr an einer alten in der Kampagne gespeicherten CDN-URL bzw. einem historischen Bildhash. Maßgeblich ist der **aktuelle aktive eBay-BUSINESS-Quelldatensatz**. Dessen aktuelles Remote-Bild wird begrenzt geladen, als echtes Bild dekodiert und lokal unter WordPress-Uploads gecacht. Ein unbrauchbarer Kandidat fällt aus der finalen Rangliste; der nächste gültige Kandidat rückt nach.
- **V6.18-Vertrag bleibt erhalten:** `dimension_state=pending` darf intern weiterhin materialisiert sein. V6.61.4 führt den früheren Blocker nicht wieder ein; die öffentliche Bildprüfung ist davon getrennt.
- **idealo:** `image_url` aus iPN ist ein Tracking-Wrapper. V6.61.4 löst ausschließlich erlaubte HTTPS-Ziele auf `cdn.idealo.com` auf (direkt oder über `gfx.productsup.io/src/cdn.idealo.com/...`) und cached das reale Bild lokal. Zeilen ohne reales Bildziel werden verworfen.
- **Drei Produktpositionen:** `category_product_1`, `_2`, `_3` bleiben drei eigenständige Positionen. Nach finalem Provider-/GTIN-Ranking werden nur bildfähige Kandidaten verwendet; die Positionen 1/2/3 greifen auf Kandidat 1/2/3 zu. Es wird kein defekter Kandidat als leere Karte stehen gelassen.
- **Gleiche Geometrie:** Alle drei Kategorie-Produktkarten besitzen denselben 360-px-Kartenkörper, 150×150-px-Bildfläche und `object-fit: contain`. Wrapper, Disclosure-Reserve, Label und Inhalt sind identisch dimensioniert. Responsive Disclosure-Breiten wurden für 3/2/1 Spalten getrennt abgesichert, damit kein horizontaler Überlauf entsteht.
- **Kein Designplugin-Eingriff.** Der Fix liegt ausschließlich in der Affiliate-Zentrale.

## Geschützter Workflow
Gegen V6.61.3 sind exakt vier Plugin-Dateien geändert:
1. `pferdeportal-affiliate-router.php`
2. `includes/trait-ppar-idealo.php`
3. `assets/frontend.css`
4. `readme.txt`

Die übrigen 15/19 Dateien bleiben byteidentisch, darunter eBay-Providertrait, eBay-Run/Safe-Gap/Heartbeat, Network-Sync, Output-Objects, Article-Plans, Control-Contract, Creative-Library, Kataloge und `frontend.js`.

## Aussagegrenze
Der Release ist **LOCAL/FRESH-UNPACK PASS**. Die reale WordPress-Sichtprüfung nach Installation bleibt das letzte externe Gate. Es wird nicht behauptet, dass ein Provider drei Produkte liefern kann, wenn tatsächlich weniger als drei gültige Kandidaten existieren; bei mindestens drei gültigen Kandidaten werden die drei Positionen 1/2/3 vollständig befüllt.
