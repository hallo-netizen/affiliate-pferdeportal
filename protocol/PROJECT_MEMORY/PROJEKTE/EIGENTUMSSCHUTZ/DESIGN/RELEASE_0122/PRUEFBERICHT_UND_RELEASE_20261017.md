# Hab & Bewahr – Design 0.1.22 – Megamenü-Vollständigkeit und Überlauf

**Datum:** 17.10.2026. **Status:** Korrektur des bestehenden Designplugins lokal fertig; nicht live installiert. Keine Änderung am Kategorieplugin, C2.2-Import, DB, WP-IDs, Permalinks oder Artikeln.

## Ausgangslage – tatsächlich beobachtet
Original-Nutzerscreenshot nach den erfolgreichen Kategorieimporten zeigt Wetter-Megamenü mit nur **fünf Bereichsgruppen in einer Reihe**. Daneben ist **„Alle Themen“ unter jeder Gruppe** und in der Kopfleiste sichtbar, auch wenn kein Menü-Überlauf belegt ist.

**Exakte Ursache im realen Originaldesign 0.1.21**, `templates/site.php`:
- `$areas=array_slice($areas,0,5)` kürzt die Welt-Nav auf fünf Bereiche, obwohl laut C2.2-Originalprofil **Wetter sieben Bereiche** hat.
- `echo '<a class="hbdp-mega-more" ...>Alle Themen</a>'` erscheint bei jeder Gruppe unabhängig von der Anzahl gültiger Kindthemen.
- Im Mega-Kopf steht ebenfalls immer ein pauschales `Alle Themen`.
- `assets/style.css` enthielt zusätzlich eine veraltete `--6`-Grid-Variante mit **sechs Desktop-Spalten**.

Die autoritative C2.2-Plugin-Profildatei hat in den sechs Welten **36 Schutzbereiche**: 6/5/7/5/6/7 (Plugin-Profilwelt-Reihenfolge: Einbruch/Feuer/Technik/Vandalismus/Wasser/Wetter), bei Wetter konkret: Blitz & Überspannung, Freizeit & Unwetter, Frost & Schnee, Hitze & Trockenheit, Starkregen & Hochwasser, Sturm & Hagel, Tier- & Schädlingsschäden. Diese 36 Bereiche sind keine neue WordPress-Änderung.

## Zielfix – Fachinhalte bestimmen die Anzahl, nicht das Menü
- Kein PHP-`array_slice` über Welt-Bereiche. **Alle 36 ursprünglichen Bereiche bleiben in den sechs Menüs sichtbar**, bei Wetter **sieben Gruppen in zwei Reihen (5 + 2)**. Maximal fünf **Spalten pro Desktop-Reihe**, nie global fünf Gruppen.
- Jede Bereichsgruppe zeigt maximal **vier** anklickbare konkrete Themenlinks. `Alle Themen` erscheint **nur bei mindestens fünf tatsächlich gültigen direkten Kindlinks**; Ziel ist die vorhandene Bereichs-Hubseite, die alle Kinder anzeigt.
- Im Kopf des Welt-Megamenüs kein pauschales `Alle Themen`, da die Bereiche im Menü vollständig dargestellt werden und deshalb hier keine verdeckten Gruppen verbleiben.
- Unverändert: hubseiten, archive, canonical deduping, WP-IDs, Slugs, 743+472 neue C2.2-Importe; keine neuen Frontend-Datenbankabfragen neben der bereits cached Menügeneration. Neuer Transient-Key `0.1.22` invalidiert den alten gekürzten Menü-Cache ohne DB-Mutation.
- Nur vier der 53 ursprünglichen Design-Dateien sind geändert: `templates/site.php`, `assets/style.css`, Bootstrap-Versions-/Assetnummer und README.

## Lokal ausgeführte Tests
1. Original-`hbdp_main_navigation` aus dem realen PHP-Template (nicht ein selbst neu geschriebener HTML-Renderer) gegen **sechs C2.2-Welten / 36 Schutzbereiche** aus dem echten 1.14.8.30-Kategorieplugin-Profil mit zusätzlichen eigenständigen Alt-Unterthemen als Fixture gerendert.
2. **36/36 Bereichsgruppen**, pro Welt exakt **6/5/7/5/6/7**, Wetter vollständig einschließlich bisher abgeschnittener Hitze/Tier-Schäden.
3. Direkte Unterthemenlinks maximal vier; bei fünf oder mehr gültigen Unterthemen ein `Alle Themen`-Link, bei vier oder weniger **kein Link**; ein ungültiger WordPress-Permalink zählt NICHT als verstecktes erreichbares Thema.
4. Im Testfixture **15/15** korrekt benötigte Bereichs-Übersichtslinks, keine falschen, kein pauschales Welt-Kopf-`Alle Themen`.
5. Tatsächlicher lokaler Chromium/CSS-Browsertest (Original CSS mit Änderung) bei Desktopbreiten 1440, 1280, 1100, 1024 und Mobile 760, 390 CSS-Pixel: sieben Wetter-Gruppen durchgehend vorhanden. Desktop fünf Spalten und **zwei Reihen**; Mobile eine Spalte und sieben untereinander. **Bei keiner Testbreite horizontales Abschneiden**, kein CSS-Overflow im Seitenkörper.
6. Bei 1440 × 900 beträgt die simulierte Menühöhe **590 px**, die zwei Reihen passen vollständig in das 650-px-Maximum. Bei 1280 × 800 ebenso.
7. 53/53 Ursprungsdateien erhalten, genau vier geändert. ZIP CRC bestanden, PHP-Lint der Plugin-PHP-Dateien bestanden.
8. Keine WordPress-Live-Installation/kein 1:1-Live-Chromiumtest durch diese lokale Simulation behauptet.

**Lokaler release-Build:** `HAB_UND_BEWAHR_DESIGN_0.1.22_MEGAMENUE_ZWEI_REIHEN_ALLE_THEMEN.zip`, **1.795.986 Bytes**, SHA-256 `4fd769ff3c4a553060228791e067035a0e4d2a4417d13a6f1f166b4b52c0a00a`.

**Reproduzierbarer Quellpatch in GitHub:** `RELEASE_0122/apply_to_0121.py`.

## NEXT ACTION
**Nur das bestehende Hab-&-Bewahr-DESIGN-Plugin** als normales Update auf 0.1.22 bringen, KEIN Kategorieplugin ersetzen, KEINEN Import auslösen. Danach auf Desktop bei Wetter prüfen: sieben Bereichsgruppen in zwei Reihen (5+2), kein pauschales „Alle Themen“; nur bei wirklich fünf oder mehr sichtbaren/erreichbaren Unterthemen in einer Bereichsgruppe ein Überlauf-Link. In WordPress erfolgte bei der Erstellung dieses Builds keine Änderung.
