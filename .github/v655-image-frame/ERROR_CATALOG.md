# FEHLERKATALOG – Kategorie-/Produktseiten Bildrahmen ONLY

## IMG-655-001 – Produktbilder springen je nach Quellformat

**Symptom:** In Produktvorschlägen auf Leaf-/Produktseiten beginnen Titel und Buttons nicht sauber auf einer Linie, weil Hochformat-, Querformat- und quadratische Produktbilder unterschiedlich große Bildboxen erzeugen.

**Ursache:** Die Slots `product_after_category_tiles` und `category_product_1/2/3` verwenden den generischen `.ppar-banner-image`-Renderer. Vor dem Fix gilt dort keine feste Bildhöhe; die Bildgeometrie folgt dem Quellbild.

**Rootfix:** Ausschließlich CSS, streng auf diese Produkt-Slots begrenzt. Fester 150-px-Medienrahmen und 150×150-px-Bildelement, zentriert, `object-fit: contain`, `object-position: center center`.

**Nicht geändert:** Karten-/Buttondesign, Texte, Produktwahl, Artikelprodukt-Renderer, Banner, HivePress-PRIVATE-Bilder, PHP, Provider, eBay-Lauf, Scheduler und Designplugin.

**Negativschutz:** Der Release-Gate blockiert, wenn außer `affiliate-portal-router/assets/frontend.css` irgendeine Produktionsdatei abweicht oder wenn die neuen Selektoren auf Artikel-, Partner- oder HivePress-Bildklassen ausgreifen.
