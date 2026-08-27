# Affiliate-Zentrale V6.61.13 – Postload Layout Lock

Stand: 27.08.2026
Status: LOCAL_HARD_PASS_AWAITING_LIVE

## Anlass
Live-Symptom unter V6.61.12: Die drei category_product-Karten erscheinen beim ersten Paint kurz gleich groß und laufen danach wieder auseinander. Damit ist belegt, dass eine rein statische CSS-Prüfung diesen Fehler nicht ausreichend abdeckt; es existiert ein später Layout-/Reflow-Effekt.

## Korrektur
V6.61.13 ergänzt ausschließlich im Affiliate-Plugin einen post-load Layout-Lock auf der real gerenderten category_product-DOM-Kette. Er reagiert auf ResizeObserver-Änderungen, Bild-Ladevorgänge, Fonts, DOM-/Klassenänderungen, Window-Load/Resize sowie mehrere frühe Nachladezeitpunkte. Innerhalb jeder realen Kartenzeile werden sichtbare Kartenlinkhöhe, Slot/Content-Höhe und äußerer Designkartenrahmen auf den größten tatsächlich benötigten Wert verriegelt. Bei Breakpoint-/Breitenänderung wird neu gemessen.

Keine Provider-, Feed-, Ranking-, Tracking-, Campaign-, URL- oder Designplugin-Logik geändert.

## Lokale Browserprüfung
Normalbetrieb: 40/40 PASS über 1440, 1280, 1024, 900, 768, 700, 620, 480, 390, 360 px; zwei CSS-Ladereihenfolgen; zwei Provider-/Markup-Reihenfolgen; kein horizontaler Overflow; Produktgrid-Top-Shift 0 px; Desktop-Bilder 150x150; Karten-/Linkhöhe und CTA-Unterkante zeilenweise Delta <= 1 px.

Kontrollierter Postload-Reflow: Zunächst korrekter Paint; danach werden die drei Karten bewusst auf 430/360/395 px auseinandergezogen. V6.61.12 bleibt in 20/20 Fällen FAIL. V6.61.13 stellt in 20/20 Fällen wieder gleiche Zeilenhöhe und CTA-Unterkante her. 1440-px-Referenz V6.61.13 final: Link 430/430/430 px, Außenhöhe 488/488/488 px, CTA-Unterkante 485/485/485 px.

Wichtig: Der konkrete fremde Live-Auslöser außerhalb des Affiliate-Plugins wird nicht behauptet. Geprüft ist exakt die beobachtete Fehlerklasse: erster Paint korrekt, spätere Layoutänderung macht die Karten ungleich.

## Code-Scope
Gegen V6.61.12 exakt drei Plugin-Dateien geändert:
- assets/frontend.js
- pferdeportal-affiliate-router.php
- readme.txt

Alle übrigen 16 Plugin-Dateien byteidentisch.

PHP-Lint 14/14 PASS. JS-Syntax PASS. Fresh-Unpack 19 Dateien PASS.

Installer: affiliate-zentrale_v6.61.13_POSTLOAD_LAYOUT_LOCK_HARD_VERIFIED.zip
SHA-256: d5b04b4dbdef8afaf39173be7f7073edc708611b3e431ae63c289c436893c33b

MASTER: MASTER_AFFILIATE_ZENTRALE_V6_61_13_POSTLOAD_LAYOUT_LOCK_20260827.zip
SHA-256: 99fd8f733e9adac048b3a51fb6c5276a4cbef4511bffc9d2e3ee6dfaf162fc9b
