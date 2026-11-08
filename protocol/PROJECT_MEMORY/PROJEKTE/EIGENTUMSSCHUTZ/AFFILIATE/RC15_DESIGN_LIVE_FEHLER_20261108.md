# HAB-004 RC15 – echte Live-Designfehler beseitigt (08.11.2026)

**EINZIGE NEUE INSTALLATIONS-ZIP IM CHAT:** `Hab-und-Bewahr-Affiliate-RC15-Designkorrektur.zip`, Version `0.1.12-rc15`, 2.094.091 Bytes, SHA256 `63c03d4bc5e4663ac583d9e604ed3019bfcbd4bdc5c2def16ce64d986b6cf737`. Vollständiges ZIP, WordPress-Ordner `affiliate-portal-router/` unverändert. **Nicht behaupten, dass GitHub-CURRENT bereits RC15 ist:** GitHub-CURRENT immer noch RC11, sofern nicht ausdrücklich auf Dateiebene aktualisiert. RC15 wurde noch nicht von Benutzer installiert.

## Echte Ursache (Screenshots Nutzer, 08.11.2026 09:34)

Die WordPress-Live-Screenshots nach RC14 zeigen sechs Bereichsfotos bereits korrekt, aber weiterhin verschachtelte äußere und innere Rahmen sowie GRÜNEN, viel zu großen Amazon-Button. Die PHP-Ausgabe ist somit RC14, aber die CSS-Darstellung des Hab-Affiliate-Plugins blieb unter der alten CSS-URL geladen: `enqueue_frontend_assets()` benutzte die unveränderte Konstante `self::VERSION = '6.72.211'` als Browsercache-Version, obwohl RC12/RC13/RC14 Stylesheet jeweils geändert wurde. **Neue PHP-Bannerversion bei alter CSS-Datei = genau diese visuelle Mischung.** Das echte HAB-001 Design stellt zudem eigenes `section.hbdp-area-demo-ad` mit Rand/Padding/Anzeige bereit, die Basis-Affiliate-Styles stellen einen zweiten Rand bereit. Vorherige Offline-Tests nutzten eigene vereinfachte Wrapper und übersahen somit die echte Kombination. **Das ist die Ursache der Live-Diskrepanz.**

## Maßnahme: nur das Original repariert, keine neue Architektur

Aus der vollständigen RC14 ZIP genau **drei bestehende Dateien geändert, alle anderen 32 unverändert**:
1. `affiliate-portal-router.php`: Pluginkopf `0.1.12-rc15`, **ausschließlich** beim existierenden `wp_enqueue_style('ppar-frontend',...)` neue cache-eindeutige Versionskennung `self::VERSION . '-hb-rc15-20261108'`. Interne Legacy-Konstante und Produkt-/Importlogik unverändert.
2. `assets/frontend.css`: die **bestehende** Hausbanner-Klasse `.ppar-hb-amazon-house` gegen die **echten** HAB-001 Designwrapper und die bisherige Affiliate-Slot-Basis gestylt. Keine zusätzliche Ausgabe/Funktion. Außen-/Innenränder für diesen Banner komplett entfernt; ein bestehendes sichtbares Anzeige-Label am Designwrapper; Original Hobbydepot `erhältlich bei amazon` einmal im kleinen orangefarbenen Button mit Pfeil, keine zusätzliche Textzeile oder Hab-Logo; breiter Banner 6:1, Mobile 4,2:1, Glossar/Artikel-Quadrat 1:1, sanfter vertikaler Verlauf. CSS gezielt, gebuchte/andere Banner bleiben unangetastet.
3. `readme.txt`: Versionsangabe aktualisiert.

## Harte Abnahme vor Weitergabe

- Codevergleich RC14→RC15: **exakt drei bestehende Dateien geändert**, 35/35 ZIP-Einträge identisch in Verzeichnisstruktur, 35/35 CRC PASS, 25/25 PHP Syntax PASS, Original-Logik für sechs Welten, Artikel, Glossar und eBay/Idealo unverändert.
- Vorhandene originale 63 PHP-Tests auf Welt-/Kategorievererbung, Amazon-Tracking, Artikel-/Glossar-Slots und Abschalter **PASS**.
- Neuer Chromium-Test benutzt **wirkliche unveränderte `area-prototype.css` und `glossary.css` des HAB-001 Designplugins**, nach den neuen Affiliate-Styles geladen (schärfer als alte Mock-Vorschau), die tatsächlichen `section.hbdp-area-demo-ad`/Artikel-HTML-Wrapper und originale Hab WebP- und Amazon-Button-Assets. 1250px, 900px, 390px: keine Rahmen auf Werbeplatz/Plugin-Banner; genau ein sichtbares Anzeige-Label, Button `rgb(255,156,22)`, Bilddateien laden, kein horizontaler Überlauf. Quadrat bei allen Bildschirmgrößen exakt 300×300px; voller breiter Banner 6:1 (Mobil 4,2:1). Bei erster CSS-Probe deckte der Test zu kleine Quadrat-Höhe auf und wurde **vor RC15 ZIP** behoben.
- **Noch KEIN echter WordPress-Live-Test nach Installation.** Nicht als live erledigt deklarieren. Der Benutzer installiert RC15 als Update von RC14 und testet dieselben `Wassermelder`/ `Wertsachen & Tresore`-Kategorieseiten und ein Glossar-Quadrat; es kann ein echter Server-Seiten-/CDN-Cache verbleiben, CSS-Version-Wechsel löst aber zumindest Browser-Asset-URL aus. Keine Aufforderung zum kostenpflichtigen DataForSEO-Lauf.

Originale: Aktuelles Hobbydepot HD009 0.1.25 (Original-Amazon-Badge `hdar-amazon-available-at-amazon-de-official.png`), HAB-001-Design-Original, HAB-004 RC14 (ZIP im vorherigen Chat). Weder Pferdeatelier, Hobbydepot noch HAB-001 geändert.
