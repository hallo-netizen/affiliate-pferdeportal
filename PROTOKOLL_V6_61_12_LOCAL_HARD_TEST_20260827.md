# V6.61.12 – lokale Hard-Prüfung

Status: **LOCAL_HARD_PASS_AWAITING_LIVE**

## Ausgangslage
V6.61.11 bleibt im Live-Screenshot FAIL: Der große V6.61.10-Leerraum ist beseitigt, aber die sichtbaren Produktkarten/CTAs stehen weiterhin auf unterschiedlichen Höhen.

## Quellpfad
Der reale Kategorieprodukt-Wrapper wird vom Designplugin als `is-real`-Grid-Item mit `data-pa266-slot="category_product_N"` erzeugt; Hub-2 nutzt analog `data-pa255-slot`. Der Affiliate-Shortcode liefert den direkten `.ppar-affiliate-slot`-Kindknoten. Automatische eBay-BUSINESS-Produkte laufen als `image_link` über denselben Affiliate-Renderer wie andere Produktprovider. `ebay_remote_listing_image_html()` gehört dagegen zum HivePress-INDIVIDUAL-Listing-Pfad und ist nicht der Kategorieprodukt-Renderer.

## V6.61.12
- alten V6.61.3–V6.61.11-Kategorieprodukt-CSS-Override-Stapel entfernt und durch einen konsolidierten Block ersetzt;
- direkter Zielpunkt: reale `is-real`-Wrapper + Slot-Datenattribute;
- Slot-Tracks: `56px + minmax(360px,1fr)`;
- sichtbare Karte: `150px + minmax(210px,1fr)`;
- kein `:has()` im neuen Block;
- kein `grid-auto-rows:1fr`;
- keine verschachtelte `height:100%`-Kette;
- Bilder 150×150 `contain`;
- Single-/Multi-CTA gleiche 42px-Box;
- Provider-/Feed-/eBay-/idealo-/Output-/Registry-/JavaScript-Dateien unverändert.

## Lokaler Browser-Hardtest
Echtes Chromium mit realer Renderer-DOM-Struktur und relevanten Design-CSS-Regeln:
- 4 Designfamilien: pa272, pa273, pa266, pa255
- 2 Provider-Reihenfolgen
- 2 CSS-Ladereihenfolgen
- 10 Viewports: 1440, 1280, 1024, 900, 768, 700, 620, 480, 390, 360
- **160 Browserfälle PASS**
- Desktop Außenkartenhöhe Delta: 0px
- Desktop sichtbare Kartenhöhe Delta: 0px
- Desktop CTA-Unterkante Delta: 0px
- Bildboxen: 150×150px
- oberer Produktabstand <=24px
- horizontaler Overflow: 0
- lange Titel nicht abgeschnitten

## Scope
Gegenüber V6.61.11 exakt 3 Plugin-Dateien geändert:
1. `assets/frontend.css`
2. `pferdeportal-affiliate-router.php`
3. `readme.txt`

PHP-Lint: 14/14 PASS. Fresh-Unpack byteidentisch: PASS.

Installer SHA-256: `130faee246ca8f82c0176d231f6fc2512c83d1b7f661137adb4538506dd5e457`

Kein LIVE PASS behauptet. Nächster Gate ist ausschließlich der echte Frontend-Sichttest nach Installation.