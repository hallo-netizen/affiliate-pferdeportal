# Arbeitsprotokoll – V6.55 Category Product Inline Geometry Rootfix

## Anlass

Die Live-Screenshots vom 23./24.08.2026 haben die vorherigen CSS-only-Bildkorrekturen widerlegt: insbesondere das erste Produktbild einer Reihe konnte weiterhin sichtbar anders groß bzw. verschoben erscheinen. PR #16 wurde deshalb geschlossen und darf nicht verwendet werden.

Zusätzlich wurde am tatsächlich ausgelieferten V6.55-Basisinstaller eine Metadateninkonsistenz reproduziert: WordPress-Pluginheader `Version: 6.54.0`, interne `const VERSION = '6.55.0'`, oberer `Stable tag: 6.55.0`. Dadurch konnte WordPress bei der Installation die falsche Versionsnummer anzeigen.

## Rootfix

Ausgangspunkt bleibt ausschließlich das gepinnte final verifizierte V6.55-Artefakt. Geändert wird exakt eine Produktionsdatei: `affiliate-portal-router/pferdeportal-affiliate-router.php`.

1. Der WordPress-Pluginheader wird von `6.54.0` auf `6.55.0` korrigiert. Interne Pluginversion und eBay-Runtime-Build bleiben unverändert.
2. Die Bildgeometrie wird nicht mehr ausschließlich über eine cachebare CSS-Datei erzwungen, sondern direkt im tatsächlichen `render_banner()`-HTML-Pfad.
3. Nur Produkt-Creatives in `category_product_1`, `category_product_2` und `category_product_3` erhalten den neuen Bildrahmen.
4. Wrapper und Bild erhalten inline `!important` exakt 150×150 px; das Bild nutzt `object-fit: cover` und `object-position: center center`.
5. Banner-Slots, Artikelprodukte, Journal-Slots und Nicht-Produkt-Creatives bleiben unverändert.

## Gegenprüfung

Der Browser-Gegenbeweis enthält absichtlich eine feindliche `:first-child`-Regel, die vor dem Rootfix das erste Bild auf 61×137 px und die übrigen auf 92×110 px zwingt. Mit dem Rootfix müssen alle drei Wrapper und Bilder im realen Browserlayout exakt 150×150 px ergeben.

Zusätzlich sind Pflicht: vollständiger PHP-Lint, bestehender V6.55-Architekturgate, reale WordPress-Installationen 7.0.1 und 6.8.3, realer `render_banner()`-Aufruf, Metadaten-Readback über `get_plugin_data()`, bestehender Artikelprodukt-Test, Public-Heartbeat-Test, Fresh-Unpack- und MASTER-Parität.

## Scope-Hardlock

Produktionsänderungen: exakt 1 Datei.

Nicht geändert: `assets/frontend.css`, Designplugin, eBay-Runtime-Build, Scheduler, Providerlogik, Produktauswahl, Texte, Karten-/Buttondesign, Bannerlogik, Artikelproduktlogik, HivePress-PRIVATE-Bilder.

## Freigabestatus

Lokale technische Gegenprüfungen sind positiv. Eine Releasefreigabe darf ausschließlich durch den vollständigen GitHub-Workflow erfolgen. Der reale sichtbare Live-Nachweis auf Pferde Atelier bleibt danach weiterhin offen und darf erst nach Installation des finalen Artefakts anhand des echten Frontends bestätigt werden.
