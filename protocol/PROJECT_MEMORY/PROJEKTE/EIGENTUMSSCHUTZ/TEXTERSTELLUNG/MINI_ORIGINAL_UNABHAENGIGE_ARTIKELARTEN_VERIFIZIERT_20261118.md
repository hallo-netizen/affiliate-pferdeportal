# Hab / Universal 0.4.31.1 – Original-MINI bereits artikelartunabhängig (18.11.2026)

**Keine Plugin-Änderung. Keine neue Architektur, keine neuen Funktionen, keine Fixes. Keine Installationsfreigabe.**

## Neuer beweisbarer Befund – korrigiert bisherigen Blocker
- `TXE_Workshop::miniWorkerCheckpoint()` der originalen **0.4.31** wählt bereits in genau EINEM CATEGORY-Schritt `route`, echten WordPress-`category_slug` und **unabhängigen** K0-`article_type` aus der bestehenden `TXE_K0_Article_Types`-Liste. Keine Artikelart aus dem Kategorievariantennamen abgeleitet; Originalcheck `checkedMiniCategory` prüft nur exakt eingefrorene WP-Kategorie.
- Isolierte Original-PHP-Ausführung mit historisch echtem Hab-Term `Türen & Fenster` (Slug `einbruch-und-haus-und-wohnung-turen-und-fenster-1`) und synthetischem WP-Leseobjekt: **Beratung/FAQ/Pflege/Vergleich/Anleitung** je PASS. Unbekannter Kategorie-Slug und Nutzung des Kategorienetiketts `Sicherheit` als K0-Art blockiert. Kein inhaltlicher Typ für den echten Term festgelegt.
- **Original 0.4.31: 7/7 PASS; Hab Minimal 0.4.31.1: 7/7 PASS; Universal Minimal 0.4.31.1: 7/7 PASS.** 21/21 lokale Tests mit denselben bestehenden Originalmethoden, **0 Programmänderungen**.
- Die vorherige pauschale Aussage, eine feste K0-Artikelart pro Hab-Kategorie sei für MINI zwingend und der Grund für sämtliche Sperren, ist **falsch**. Der Original-MINI-Worker ist hier bereits richtig und darf nicht umgebaut werden.

## Tatsächlicher verbliebener technische Blocker
- `TXE_Workshop::seoExport()` ruft **vor** dem MINI-Kategorie-Worker `PSTE_Snapshot::structure()` auf. Diese benötigt `PSTE_Portal_Category_Map::load()`; die originale Karte verlangt pro Produktionskategorie ein festes `article_type`-Feld. Die bereinigten Kopien haben absichtlich `entries=[]` und blockieren deshalb mit `PSTE_PORTAL_CATEGORY_MAP_COUNT_INVALID`. Dieselbe PSTE-Struktur speist den ursprünglichen DataForSEO-/Keyword-Rechercheweg.
- Das ist **ein anderer** Artikeltypbegriff der ursprünglichen PSTE-Themenstruktur als die bereits unabhängig festgelegte K0-Schreibartikelart im MINI. Eine Zuordnung zu erfinden oder den Kategorienleser neu zu bauen, verstößt gegen Nutzeranweisung.
- In der vorhandenen Hab-Tarifcheck-Bestandsprüfung vom 14.11.2026 `hab-tarifcheck-bestandspruefung-20261114-130255.json` sind 160 aus WP gespeicherte Kategorien-/Seitenknoten bei einer begrenzten Prüfung, unter anderem R3 `Mechanik & Zugang` ID 157 und Kindterm `Türen & Fenster` ID 183, belegt. Diese Datei ist KEIN vollständiger WP-Readback; `article_type` ist darin nicht enthalten. **Kein neuer Kategorieexport nötig**, Nutzer hat unveränderten Bestand bestätigt.
- Weiterer technischer Rest: Das alte PSTE-Journal-Routing ist in den bereinigten Kopien ohne Pferde-Signatur bewusst deaktiviert. Original-K0-Registrierung für Hab bleibt zu bestätigen.

## Quell- und Prüfintegrität
- Original-ZIP SHA256 `07b99fa549e87d28db53f0fac0b107c92a9f0de4a3de80ad5f31fb3b7b399f7d`, ZIP-CRC PASS.
- Hab-Minimal ZIP SHA256 `3f74e5c47f79ed36571dfc9a2adb63f639bdb9aafa294c19722ad2394fbe48d4`, ZIP-CRC PASS.
- Universal-Minimal ZIP SHA256 `cbbca4c2a2f1122198cb3cda927ab739ad94e9df87bf9ace28c9201a4f16dc4d`, ZIP-CRC PASS.
- In beiden **bestehenden** Library-Büros erfolgreich gespeichert: `MINIMAL_ORIGINAL_0431/PRUEFUNG_MINI_ORIGINAL_20261118/PRUEFPROTOKOLL.md`, `TESTERGEBNISSE.json` und ausgeführtes `test_mini_original_article_type.php`.

## Nächste zulässige Tätigkeit
Nur den vorhandenen alten PSTE-Recherche-Kategorienvertrag anhand der bereits vorhandenen Konfigurationsdaten prüfen; **MINI/K0 nicht ändern**. Ohne belegte passende PSTE-Kategorievariante bleibt die ursprüngliche DataForSEO-Recherche bei reinem Auskommentieren nicht betriebsfähig. Keine erfundenen Typen, keine Live-WP-Schreibaktion, keine Installation freigeben. **Nur freigegebene Plugin-ZIPs zum Download bereitstellen.**