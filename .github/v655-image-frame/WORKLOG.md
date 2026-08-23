# ARBEITSPROTOKOLL – Kategorie-/Produktseiten Bildrahmen ONLY

Stand: 23.08.2026

## Auftrag
Ausschließlich den sichtbaren Fehler korrigieren, dass Produktbilder in den Produktvorschlägen auf Produkt-/Kategorieseiten je nach Quellformat unterschiedlich groß bzw. vertikal versetzt erscheinen. Keine weitere Design-, Inhalts-, Auswahl-, Provider-, eBay-, Scheduler- oder Workflow-Funktion ändern.

## Verbindlicher Ausgangspunkt
Final automatisch freigegebenes V6.55-Actions-Artefakt `V655_FINAL_VERIFIED_RELEASE`, Artifact-ID `9492650547`, SHA-256 `5446bd14f3e0d035e8ed74da1cd86393574f890fce5d81eb77d2aea0b611a955`.

## Rootcause
Die Leaf-Seiten-Slots `product_after_category_tiles` und `category_product_1/2/3` verwenden den generischen Affiliate-Bildrenderer `.ppar-banner-image-wrap` / `.ppar-banner-image`. Dessen Grund-CSS lässt Breite/Höhe vom jeweiligen Quellbild bestimmen (`max-width:100%`, `height:auto`). Dadurch erzeugen Hochformat, Querformat und quadratische eBay-Bilder unterschiedliche Bildboxen und verschieben die nachfolgenden Karteninhalte.

## Korrektur
Nur `affiliate-portal-router/assets/frontend.css` erhält am Dateiende einen streng auf diese vier Produkt-Slots begrenzten Override:
- Bildrahmen immer 150 px hoch,
- Bildelement 150 × 150 px,
- horizontal und vertikal zentriert,
- `object-fit: contain`, also kein Abschneiden,
- `object-position: center center`.

Nicht betroffen: Einzelbeitragskarten `.ppar-article-product-*`, Partnerbanner, Startseitenbanner, HivePress-PRIVATE-Bilder, PHP, eBay-Runtime, Scheduler, Produktwahl und Texte.

## Prüfvertrag
1. Pinned V6.55-Endartefakt und Hashes prüfen.
2. Negativbeweis: Fix fehlt im Ausgangsstand.
3. Patch nur auf exakten bekannten CSS-SHA anwenden.
4. Produktionsdiff muss exakt eine Datei ergeben: `assets/frontend.css`.
5. 22 CSS-Scope-/Geometrie-/Negativassertions PASS.
6. Alle Nicht-CSS-Dateien byteidentisch mit final V6.55.
7. PHP-Lint + JSON vollständig PASS.
8. V6.55-Heartbeat-/Kernarchitektur 23/23 PASS.
9. Installer bauen, Fresh-Unpack byteidentisch und Tests erneut PASS.
10. Real WordPress 7.0.1: Artikelprodukt-Regression + Heartbeat PASS.
11. Real WordPress 6.8.3: dieselben Realtests PASS.
12. MASTER-Manifest + Source↔Installer↔MASTER-Parität PASS.
13. Finaler Counterproof; erst dann `FINAL_RELEASE_GATE=PASS`.

`main` wird durch diese Arbeit nicht verändert.
