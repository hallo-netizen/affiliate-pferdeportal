# Affiliate-Zentrale V6.61.14 – Inline Postload Rootfix

Stand: 27.08.2026
Status: LOCAL_HARD_PASS_AWAITING_LIVE

## Live-Befund
V6.61.13 blieb live FAIL. Sichtbares Verhalten: Die drei category_product-Karten sind beim ersten Paint für Millisekunden gleich groß und springen danach wieder auseinander.

V6.61.13 änderte für die eigentliche Nachlade-Korrektur ausschließlich die externe Datei `assets/frontend.js`; PHP änderte nur Version/Metadaten. Der unveränderte Live-Endzustand belegt, dass dieser externe Guard die finale Live-Geometrie nicht bestimmt hat. Ohne direkten Live-DOM-/Netzwerkzugriff wird nicht behauptet, ob Cache/Optimizer, Asset-Ausführung oder ein anderer später Runtime-Effekt die Ursache dafür ist.

## V6.61.14
Der category_product-Gleichhöhen-Guard wird nicht mehr aus der externen `frontend.js` bezogen, sondern direkt vom aktuell geladenen Plugin-PHP als Inline-Footer-Script ausgegeben. Dadurch hängt die Korrektur nicht vom externen JS-Asset-Pfad ab.

DOM-Erkennung ist zudem robuster: direkte reale Grid-Kinder werden über ihren direkten `.ppar-affiliate-slot[data-ppar-slot^="category_product_"]` erkannt; ein bestimmtes `data-pa266-slot`-Attribut am äußeren Design-Wrapper ist nicht mehr Voraussetzung.

Der Guard verriegelt Karte, Slot, Content, Kartenlink, Textbereich und CTA nach Bild-, Font-, Resize- und DOM-Nachläufen zeilenweise auf die tatsächlich notwendige gemeinsame Höhe.

Keine Provider-, Feed-, Ranking-, Tracking-, URL-, Campaign- oder Designplugin-Logik geändert.

## Lokale Browserprüfung
Negative Kontrolle: externer Layout-Guard fehlt + kontrollierter später Reflow => ungleiche Karten reproduziert.

Positive Kontrolle V6.61.14: 40/40 Chromium-Fälle PASS = 10 Breiten x 2 Provider-/Markup-Reihenfolgen x 2 CSS-Zeitfolgen. Für jede Mehrkarten-Zeile: Außenhöhe Delta <=1 px, Kartenlink-Höhe Delta <=1 px, CTA-Unterkante Delta <=1 px. Desktop-Bildrahmen 150x150. Horizontaler Overflow 0. Runtime-Marker `data-ppar-layout-runtime="6.61.14"` in allen positiven Fällen vorhanden.

PHP-Lint PASS, JS-Syntax PASS, Fresh-Unpack byteidentisch PASS.

## Änderungsumfang gegenüber V6.61.13
Exakt drei Plugin-Dateien geändert:
- `assets/frontend.js` – externer V6.61.13-Layout-Guard entfernt, ursprüngliche Bildformat-Klassifizierung beibehalten.
- `pferdeportal-affiliate-router.php` – Version 6.61.14 + Inline-Footer-Guard.
- `readme.txt` – Release-Dokumentation.

Installer: `affiliate-zentrale_v6.61.14_INLINE_POSTLOAD_ROOTFIX_HARD_VERIFIED.zip`
SHA-256: `42bbf502efabc19d6272020c256ddc2c53ee2fd96ada041164c359a1c2bf00b0`

MASTER: `MASTER_AFFILIATE_ZENTRALE_V6_61_14_INLINE_POSTLOAD_ROOTFIX_20260827.zip`
SHA-256: `285f0936bddd2db45de3cb18ede98a3cde75d052ab3cecc188f490360c177b37`
