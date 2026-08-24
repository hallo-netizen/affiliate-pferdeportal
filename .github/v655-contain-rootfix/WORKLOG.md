# Arbeitsprotokoll – V6.55 Category Product CONTAIN Rootfix – 24.08.2026

## Bindender Ausgangspunkt
- Gepinntes finales V6.55-Release-Artefakt, nicht ein Zwischenstand.
- Keine Änderung an Designplugin, eBay-Runtime, Scheduler, Provider, Auswahl, Artikelprodukten, Texten, Karten oder Buttons.

## Live belegte Fehler
1. Produktfoto 1 konnte sichtbar stärker gezoomt/abgeschnitten erscheinen; der vorherige `cover`-Ansatz ist verworfen.
2. WordPress-Pluginheader meldete 6.54.0, obwohl `const VERSION` und der aktuelle Stable tag 6.55.0 waren.
3. readme enthielt zusätzlich einen zweiten historischen `Stable tag: 6.48.0`, der nicht als aktuelle Metadatenzeile stehen darf.

## Rootfix
- Nur product-Creatives in `category_product_1`, `_2`, `_3` bekommen im tatsächlichen `render_banner()`-Pfad einen festen 150x150-Medienrahmen.
- Bild selbst: 150x150 Element, `object-fit: contain`, `object-position: center center`; vollständiges Quellbild bleibt sichtbar, kein Crop.
- WordPress-Pluginheader auf 6.55.0 korrigiert.
- Historischen 6.48-Stable-Tag als historischen Text gekennzeichnet, sodass exakt ein kanonischer `Stable tag:` verbleibt.

## Harte Prüfungen
- Negativbeweis reproduziert Metadatenfehler des gepinnten V6.55-Installers.
- Exakter Produktionsscope: nur Haupt-PHP + readme; `frontend.css` byte-identisch.
- PHP-Lint vollständig.
- bestehender V6.55-Architekturvertrag 23/23.
- Fresh-Unpack-Prüfung.
- WordPress 7.0.1 und 6.8.3 mit realem `render_banner()`-Aufruf.
- Artikelprodukt- und Heartbeat-Realtests unverändert grün.
- Browser-Gegenbeweis aus echtem WordPress-Renderoutput: absichtlich kollidierende First-Slot-CSS-Regel + Querformat/Hochformat/Quadrat.
- Pixelprüfung fordert sichtbare Außenkanten aller drei Quellen und die bei `contain` zwingenden Weißräume; `cover` würde diesen Test brechen.
- Source ↔ Installer ↔ MASTER Parität.

## Live-Abnahme
Technischer PASS allein ist kein Live-PASS. Die echte Pferde-Atelier-Seite entscheidet nach Installation per sichtbarem Screenshot.
