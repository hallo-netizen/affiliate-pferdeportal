# HD003 – Design Template Kit Hobby Depot – gültige Current-Version

**HD003 1.50.803 · 08.11.2026**

- Installationsdatei: `HOBBY_DEPOT_DESIGN_HD003_1.50.803.zip`, vollständig und byteidentisch zu `CURRENT.zip`.
- 65.702.560 Bytes, SHA-256 `06e412f04fd3768477c6e825b39708baed0927be68260fce55fd316dff14d95f`, Git-Blob `47f3cf9973196ae373eb56705607b0144e2a9546`. Plugin-Ordner und Einstieg `affiliate-portal-template-kit/pferde-template-kit.php` unverändert.
- **Passende Beiträge:** Die drei vorhandenen Beitragsvorschau-Darstellungen nutzen weiter das echte Beitragsbild, falls vorhanden. Nur bei fehlendem Beitragsbild verwenden sie ein genehmigtes, fachlich passendes Hobbyfoto aus dem bereits vorhandenen HD003-Fotobestand, anhand der vorhandenen zentralen Leaf-Kategoriezuordnung. Wenn keine exakte Hobbyfotografie vorhanden ist, wird das passende Weltfoto verwendet. Keine erfundenen Bilder/Produkte.
- Beispiel: `[DESIGNTEST] Zweileiner oder Vierleiner` hat tatsächlich `featured_media=0`; Vorschau verwendet deshalb das vorhandene `hobby-masters/sportdrachen.webp` mit einem Delta-Lenkdrachen, nicht das separate Wind-&-Drachen-Bannerfoto.
- **Unverändert:** gesamte Kategorie-/Seitenhierarchie, Menü, Startseite, Filter, Hero, Affiliateplätze, Produktlogik, Kacheltexte, alle Assets. Nur zwei PHP-Dateien geändert (Version und eine gemeinsame Bildrückfallregel), keine neue Pluginarchitektur.
- **Geprüft:** Original 1.50.798 SHA-verifiziert; alle ZIP-Einträge unverändert erhalten, CRC PASS, PHP 13/13 PASS. PHP-Test: tatsächliche vorhandene Methoden für Bild ohne Featured Image und Vorrang eines vorhandenen Fotos PASS; Browser-Simulation der Kachel auf realer Sportdrachen-Kategorieseite bei 1440/900/390/360 PASS. Actions 42463656841/42463793782.
- **Echte Installation und anschließende WordPress-Abnahme offen.** Die alte Plugin-Akte 1.50.798 ist in Git-Historie erhalten.
