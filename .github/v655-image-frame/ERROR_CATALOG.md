# FEHLERKATALOG – sichtbare Produktbildgröße ONLY

## IMG-655-001 – Produktfotos wirken je nach Quellformat unterschiedlich groß

**Symptom:** In den drei Produktvorschlägen auf Produkt-/Kategorieseiten wirken einzelne Fotos kleiner oder versetzt, obwohl der umgebende Kartenbereich gleich ist. In den beobachteten Beispielen fiel das teils am ersten Produkt besonders auf.

**Erste Fehlannahme:** Ein fester 150×150-Rahmen mit `object-fit: contain` wurde zunächst als ausreichend bewertet. Der reale Screenshot widerlegte das: `contain` erhält das gesamte Quellbild und erzeugt je nach Seitenverhältnis freie Randflächen. Die sichtbare Foto-Fläche bleibt dadurch unterschiedlich groß.

**Verifizierte Ursache:** Die drei Produkt-Slots `category_product_1/2/3` verwenden Quellbilder mit unterschiedlichen Seitenverhältnissen und Hintergründen. Soll die **sichtbare** Foto-Fläche zwingend gleich groß sein, muss das Bild selbst eine feste 150×150-Fläche vollständig füllen. Eine Position-1-Sonderlogik ist im Fix ausdrücklich verboten; alle drei Slots erhalten dieselbe Regel.

**Rootfix:** Ausschließlich CSS, streng auf `category_product_1/2/3` begrenzt. Fester 150×150-px-Rahmen und 150×150-px-Bildelement, zentriert, `object-fit: cover`, `object-position: center center`. Der Banner-Slot `product_after_category_tiles` bleibt unberührt.

**Nicht geändert:** Karten-/Buttondesign, Texte, Produktwahl, Artikelprodukt-Renderer, Banner, HivePress-PRIVATE-Bilder, PHP, Provider, eBay-Lauf, Scheduler und Designplugin.

**Negativschutz:** Der Release-Gate blockiert, wenn außer `affiliate-portal-router/assets/frontend.css` irgendeine Produktionsdatei abweicht, wenn `contain` im neuen Fixblock verbleibt, wenn der Banner-Slot erfasst wird oder wenn Position 1 eine Sonderregel gegenüber Position 2/3 erhält.
