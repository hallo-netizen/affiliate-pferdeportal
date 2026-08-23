# ARBEITSPROTOKOLL – sichtbare Produktbildgröße ONLY

Stand: 23.08.2026

## Auftrag
Ausschließlich den sichtbaren Fehler korrigieren, dass Produktfotos in den drei Produktvorschlägen auf Produkt-/Kategorieseiten je nach Quellformat unterschiedlich groß wirken. Keine weitere Design-, Inhalts-, Auswahl-, Provider-, eBay-, Scheduler- oder Workflow-Funktion ändern.

## Verbindlicher Ausgangspunkt
Final automatisch freigegebenes V6.55-Actions-Artefakt `V655_FINAL_VERIFIED_RELEASE`, Artifact-ID `9492650547`, SHA-256 `5446bd14f3e0d035e8ed74da1cd86393574f890fce5d81eb77d2aea0b611a955`.

## Korrektur der ersten Fehlannahme
Der erste Ansatz mit einem festen 150×150-Rahmen plus `object-fit: contain` war visuell unzureichend. Er vereinheitlichte zwar den CSS-Rahmen, nicht aber die tatsächlich sichtbare Foto-Fläche. Besonders Quellen mit farbigem Hintergrund oder starkem Hoch-/Querformat zeigten weiterhin sichtbare Letterbox-Flächen und wirkten kleiner bzw. versetzt. Der reale Screenshot widerlegte deshalb den ersten PASS.

Die Beobachtung „wenn falsch, dann häufig das erste Bild“ wird ausdrücklich nicht als Slot-Ursache angenommen: `category_product_1`, `_2` und `_3` werden jetzt identisch behandelt; der Test verbietet eine Sonderregel nur für Position 1.

## Rootcause
Für eine zwingend gleiche sichtbare Foto-Fläche reicht `contain` prinzipbedingt nicht aus: das komplette Quellbild wird innerhalb des Quadrats erhalten und kann dabei freie Randflächen erzeugen. Nur eine feste 150×150-Bildfläche mit `object-fit: cover` füllt den sichtbaren Rahmen unabhängig von Portrait-, Quadrat- oder Landscape-Quelle vollständig.

## Korrektur
Nur `affiliate-portal-router/assets/frontend.css` erhält einen streng auf `category_product_1/2/3` begrenzten Override:
- sichtbarer Bildrahmen exakt 150 × 150 px,
- Bildelement exakt 150 × 150 px und nicht schrumpfbar,
- `object-fit: cover`, damit die sichtbare Foto-Fläche immer vollständig 150 × 150 px füllt,
- `object-position: center center`,
- alle drei Positionen exakt dieselbe Regel,
- `product_after_category_tiles` ist ein Banner-Slot und bleibt ausdrücklich unberührt.

Nicht betroffen: Einzelbeitragskarten `.ppar-article-product-*`, Partner-/Affiliate-Banner, Startseitenbanner, HivePress-PRIVATE-Bilder, PHP, eBay-Runtime, Scheduler, Produktwahl, Texte, Karten und Buttons.

## Prüfvertrag
1. Pinned V6.55-Endartefakt und Hashes prüfen.
2. Negativbeweis: sichtbare Größenfixierung fehlt im Ausgangsstand.
3. Patch nur auf exakten bekannten CSS-SHA anwenden.
4. Produktionsdiff muss exakt eine Datei ergeben: `assets/frontend.css`.
5. CSS-Scope-/Geometrie-/Negativassertions: `cover`, kein `contain`, kein Banner-Slot, keine Position-1-Sonderregel, Portrait/Quadrat/Landscape füllen 150×150.
6. Alle Nicht-CSS-Dateien byteidentisch mit final V6.55.
7. PHP-Lint + JSON vollständig PASS.
8. V6.55-Heartbeat-/Kernarchitektur 23/23 PASS.
9. Installer bauen, Fresh-Unpack byteidentisch und Tests erneut PASS.
10. Real WordPress 7.0.1: Artikelprodukt-Regression + Heartbeat PASS.
11. Real WordPress 6.8.3: dieselben Realtests PASS.
12. MASTER-Manifest + Source↔Installer↔MASTER-Parität PASS.
13. Finaler Counterproof; erst dann `FINAL_RELEASE_GATE=PASS`.

`main` wird durch diese Arbeit nicht verändert.
