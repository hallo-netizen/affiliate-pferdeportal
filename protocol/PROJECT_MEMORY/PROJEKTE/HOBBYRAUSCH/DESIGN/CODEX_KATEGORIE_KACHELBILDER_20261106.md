# Hobby Depot: Codex-Kategorie- und Kachelbilder – geprüfter Arbeitsauftrag

**Gültigkeit:** ausschließlich Hobby Depot, ausschließlich Kachel- und Kategoriebilder (Designplugin HD-003). Keine Arbeit an der eigenständigen Bildzentrale HD-006 (Beitragsbilder), keine Arbeit an Pferdeatelier/K0 oder Hab & Bewahr.

## Nachgewiesene Ausgangslage, 06.11.2026
- HD-003 Original **1.50.798**, vollständig vorhanden: `PLUGINS/ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip`.
- ZIP: 65.702.034 Byte, 1.290 Einträge, SHA-256 `05ea37f040c1189ea9fda29c2dd795740351d83fe8022f8d966a453679fec7a8`.
- Der Stand enthält 805 Bilddateien insgesamt, darunter 289 Unterkategorie-Dateien einschließlich historischer Versionen, 69 Hero-Master, 105 Hobby-Master. **Dateizahl ist nicht die Zahl fertiger aktueller Themen.**
- Die Bildauflösung für echte WP-Kategorieseiten/Kacheln läuft über `category_image_v150774` in `includes/class-hobby-depot-profile-v150709.php`; eine Bilddatei wird nur dann verwendet, wenn sie zum exakten Slug und richtigen Bereich passt.
- Hub2-Fotos werden aus `assets/hobby-depot-v150617/subcategories/<welt>/<slug>-v150634.webp` (Kachel), beziehungsweise `assets/hobby-depot-v150617/hero-masters-v150684/<slug>.webp` (Hero) und vorhandenen zugelassenen Varianten abgerufen.
- Das Hobbyregister HD-007 hat eine **eigene** Masterbild-Logik. Dessen Produktionsliste nicht mit der Liste für Kategorie-/Kachelbilder vermischen.
- Einlesen der bestehenden WordPress-Mediathek/WordPress-Livedaten wurde noch nicht authentifiziert. Ein lückenloser aktueller Fertig-/Fehlbestand lässt sich daher nicht allein aus ZIP-Dateinamen ableiten.

## Strenge Bildregeln
1. Vor dem Erzeugen **exakten Seite-/Kachel-Slug und bisherige Zuordnung** aus WordPress bzw. aktuell freigegebener Bildliste prüfen. Fertiges nicht erneut erzeugen.
2. **Genau eine finale Quelle pro fehlendem Thema**, keine Bildserie, keine Variantenansammlung. Hauptmotiv muss das konkrete Hobby verständlich darstellen.
3. **Eine reale durchgehende Szene.** Keine Collage, keine Bild-in-Bild-Darstellung, keine Raster, keine Split-Bilder, keine Schrift, keine Logos und keine Motivvermischung.
4. Vor endgültiger Freigabe **zweite Bildprüfung**: ein Motiv, korrekte Zuordnung/Anatomie, kein Duplikat und erkennbar im kleinen Kachelzuschnitt. Fehlerhaftes Bild nicht zuordnen, sondern als FAILED protokollieren.
5. Aus einer einzigen freigegebenen Quelle beide vorhandenen Formate bilden: **600×320 Hero und 200×107 Kachelvorschau**, ohne sichtbares Hochskalieren. Die bestehende Hobbyregister-Regel **1500×1000** gilt nur für HD-007.
6. Nur ein vollständig geprüftes Bild an **exakt die passende** Quelle im HD-003-Plugin binden. Keine Oberkategorie- oder Fremdbild-Fallbacks.
7. Bestehende Bilder niemals unbemerkt überschreiben. Keine PHP-/CSS-/SEO-/Navigations-/Bildzentrale-Änderungen durch den Bildauftrag.

## Integration und Abnahme (ohne manuelle Einzelbildarbeit des Betreibers)
1. Codex produziert ausschließlich fehlende Motive lokal, in einer isolierten Arbeitskopie und mit standardisiertem Manifest `slug → Bildquelle → Zuschnitte → Zielpfade → QA`.
2. Integrationsprogramm setzt Hero- und Kachelbilder in die **bestehenden** HD-003-Assetpfade. Keine neuen WordPress-Plugins.
3. Rebuild des **vollständigen** bestehenden HD-003-Installationspakets aus dem bitgenau geprüften Original; nur erwartete Bilddateien dürfen sich ändern/ergänzen.
4. Automatischer Lokaltest: ZIP/CRC, exakte Slug-/Weltbindung, Formate, genau ein Master pro Thema, keine gleiche Datei für verschiedene Themen, fehlende/falsche Ziele = FAIL. PHP-Code-Dateien bytegleich. Danach unabhängige visuelle Prüfung durch Codex.
5. Vor Liveschaltung in einem separaten GitHub-Prüfzweig archivieren. Nur ein getestetes Gesamtupdate, keine Einzel-Uploads. **Echte Installation auf WordPress und spätere Bildausgabe müssen separat live bestätigt sein.**
6. Authentifizierte WordPress-Verwaltung und ggf. Codex-Desktop-Zugang setzen eine tatsächlich vorhandene Verbindung voraus. Die Verbindung ist in diesem Chat **nicht** nachgewiesen. Keine Behauptung einer vollständigen unattended Live-Implementierung ohne diesen Nachweis.

## Technischer Prüfstand
- Statische Original-ZIP- und Quellcodeprüfung: GitHub Actions 42192547563 und 42192975148.
- Keine Bildgenerierung und kein WordPress-Liveimport durch diese Bestandsprüfung.
- Beschaffung/Prüfung des aktuellen Fertig-/Fehlbestandes (WP & Design-Assets) ist der erste Produktionsschritt.
