# Affiliate-Zentrale V6.61.15 – Saved-Live-HTML Root Cause

Stand: 27.08.2026
Status: LOCAL_HARD_PASS_AWAITING_LIVE

## Beweis aus dem tatsächlich gespeicherten Live-HTML
Der gespeicherte Reitstiefel-Live-DOM enthält zunächst die erwarteten drei `category_product_*`-Slots der Affiliate-Zentrale. Danach läuft im Portal-Design das Script `pftk-real-affiliate-products-v150414-js` auf `.pa255-product.is-real,.pa266-product.is-real`.

Dieses Script:
1. verschiebt alle ursprünglichen Kinder der Produktkarte in einen neuen Container `data-pftk-affiliate-source-v150414="1"`;
2. versteckt diesen Source-Container per CSS;
3. erzeugt stattdessen eine neue sichtbare `data-pftk-affiliate-clean-shell-v150414="1"` mit neuem Link/Bild/Titel/Preis;
4. hängt einen separaten sichtbaren CTA `data-pftk-affiliate-cta-v150414="1"` direkt an die äußere Produktkarte.

Damit war erklärt, warum V6.61.14 trotz lokalem Test live scheiterte: Der Guard maß und verriegelte die ursprüngliche `.ppar-*`-Struktur, die nach DOMContentLoaded bereits unsichtbar war. Die sichtbare Endkarte wurde vom Design-Runtime neu erzeugt und blieb außerhalb dieses Guards.

## Exakte lokale Reproduktion mit dem gespeicherten Live-HTML
Mit dem unveränderten gespeicherten Live-HTML, dem echten inline enthaltenen Design-Runtime und den echten Affiliate-Zentrale-Assets wurde V6.61.14 in Chromium reproduziert.

NEGATIV V6.61.14 @ 1440px nach Design-Transformation:
- sichtbare Shell-Höhen: 231.172 / 288.094 / 264.922 px
- CTA-Unterkanten-Differenz: 56.922 px
- sichtbare transformierte Bildflächen: 338x185 / 338x185 / 338x185
- Produktgrid-Overflow: 0

## Rootfix V6.61.15
- wirkungslosen V6.61.14-Footer-Guard entfernt;
- ausschließlich Affiliate-Zentrale geändert, Designplugin unangetastet;
- providerneutrale CSS-Regeln greifen auf die bewiesene sichtbare transformierte Struktur;
- äußere Grid-Zeile bleibt zuständig für gleiche Kartenhöhe;
- sichtbare Clean-Shell streckt sich bis zur gemeinsamen Unterkante;
- CTA sitzt bei allen Karten auf derselben Unterkante;
- sichtbare Produktbildfläche exakt 150x150, `object-fit: contain`;
- Selektoren sind spezifischer als die später geladenen Design-Runtime-Regeln und funktionieren deshalb unabhängig von der CSS-Ladereihenfolge.

POSITIV V6.61.15 @ 1440px:
- äußere Karten: 302.094 / 302.094 / 302.094 px
- sichtbare Shells: 253.094 / 253.094 / 253.094 px
- CTA-Unterkanten-Differenz: 0 px
- sichtbare Bildflächen: 150x150 / 150x150 / 150x150
- Produktgrid-Overflow: 0

Zusätzlich PASS bei 1280, 1200, 1101, 1024, 900, 768, 700, 620, 480, 390 und 360 px mit demselben gespeicherten Live-HTML und der echten darin enthaltenen Design-Transformation.

## Scope
Gegen V6.61.14 exakt drei Plugin-Dateien geändert:
- `assets/frontend.css`
- `pferdeportal-affiliate-router.php`
- `readme.txt`

16/19 Dateien byteidentisch.
PHP-Lint 14/14 PASS.
JS-Syntax PASS.
Fresh-Unpack 19/19 PASS.

Installer: `affiliate-zentrale_v6.61.15_SAVED_LIVE_HTML_ROOTFIX_HARD_VERIFIED.zip`
SHA-256: `172823561ebea8ff6db880f31eb2e6011e535a2ef00ebc3baa80d95097525191`

MASTER: `MASTER_AFFILIATE_ZENTRALE_V6_61_15_SAVED_LIVE_HTML_ROOTFIX_20260827.zip`
SHA-256: `69e81ffc9a0f66f3f52f8657198ac5c65d229a09669e8d94dad6762d0305e39a`
