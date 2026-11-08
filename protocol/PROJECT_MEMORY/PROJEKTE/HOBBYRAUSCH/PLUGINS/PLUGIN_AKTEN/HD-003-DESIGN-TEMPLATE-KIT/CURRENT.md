# HD003 – Hobbydepot Design – CURRENT

**Stand 08.11.2026: vollständiger Installationskandidat 1.50.807 (Hobbyfinder).**  
**Produktiv zuletzt vom Nutzer gemeldet: 1.50.806; 1.50.807 noch nicht live abgenommen.**

**Voll-ZIP:** `HOBBY_DEPOT_DESIGN_HD003_1.50.807.zip` im isolierten GitHub-Pluginbüro (`ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/`), **65.784.974 Bytes**, SHA256 `494bd514882695f81357f53fe3d9608d3a2d4a4c6fda0a974b8d72a97cf0ce02`.
Direktdownload: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hobby-depot-hd003-1.50.807-hobbyfinder/HOBBY_DEPOT_DESIGN_HD003_1.50.807_HOBBYFINDER.zip

**Nur Hobbyfinder** (`/magazin/hobbyfinder/`): Betreiber hat Lupen-Hero und kurzen Spruch **„Das passende Hobby für dich.“** ausdrücklich freigegeben; damit wird das alte `suchen-finden.webp` auf dieser einen Seite ersetzt. Das bisherige hohe Eigenwerbebanner wird auf Hobbyfinder durch kompakte, flache Darstellung mit kleineren, mobil lesbaren echten Buttons „Werbebedingungen“ und „Preise“ ersetzt; gebuchte externe Anzeigen werden nicht umgeleitet oder ersetzt. Übrige Hero-Bilder, Kategorie- und Beitragsdesign, Anzeigenplätze, HD006 Bildzentrale und HD007 bleiben unverändert.

**Technische Freigabe:** Quelle ist das SHA-geprüfte Original-Vollplugin 1.50.806, die 1288 unveränderten Dateien sind byteidentisch, nur zwei vorhandene PHP-Dateien + zwei neue freigegebene Bilddateien; ZIP komplett, 13/13 PHP-Lint, 78/78 Browserprüfungen auf 1440, 960, 768, 640, 390, 360px PASS. GitHub Action 42506140904; gebautes Vollplugin und Browser-/Buildtests im isolierten HD003-Büro dokumentiert. **WordPress-Live-Sichtprüfung noch offen.**

**Keine weiteren Änderungen an 1.50.806 durchführen; für neue Arbeiten 1.50.807 als Arbeitsgrundlage und die nachfolgende Historie beachten.**

---

## Historischer Stand 1.50.806 (nicht mehr aktuelle Installationsdatei)

# HD003 – Hobbydepot Design – gültige Current-Version

**Version 1.50.806 · 08.11.2026**

- Vollständiges WordPress-Plugin: `HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip`, **65.705.901 Bytes**, SHA-256 `665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358`, Git-Blob `e3496adbc4524da0c6375d198d9010e2cc30d9f4`. `CURRENT.zip` ist byteidentisch. Installierter WordPress-Pluginordner und Einstieg bleiben `affiliate-portal-template-kit/pferde-template-kit.php`; die getrennte **HD006 Bildzentrale** wird ausdrücklich nicht umbenannt oder verändert.
- **Ursache des sichtbaren Fehlers:** Das bestehende Artikel-Hero übernimmt ein Gutenberg-Foto, aber die bisherige ausgegebene Dubletten-Vermeidung richtete sich an ein fremdes Theme-Element `.entry-content`, während Hobbydepot ListingHive `.post__text` verwendet. Daher wurde dasselbe JPG nochmals im Artikel gezeigt. Dazu kam die alte, bildlose automatisch eingefügte HD009-Textbannerkachel `data-ppar-slot="post_inline_banner"` und die in 1.50.805 nachträglich eingeführte zweite Drachenfotografie in der rechten Kategorienkarte.
- **KISS-Ursachenfix 1.50.806:** Beim endgültigen Ausgeben eines normalen WordPress-Beitrags wird nur das tatsächlich im Hero gezeigte JPG aus dem Gutenberg-Fließtext entfernt (per Bild-URL-Abgleich; keine anderen Sachbilder werden gelöscht). Der automatisch eingefügte generische `post_inline_banner` verschwindet ebenfalls aus Artikeln, nicht jedoch aus Kategorie-, Register- oder Startseiten. Eine nachgeladene Post-Inline-Anzeige wird als Sicherung ausgeblendet. Die rechte Hab-inspirierte Spalte zeigt vorhandene echte Kategorie-/Beitragslinks **ohne weiteres Foto**; das falsche, auf Sportdrachen fest verdrahtete Foto wurde entfernt.
- Entfernt aus dem selben bestehenden HD003-PHP auch den alten erfolglosen `wp_footer`-Doppelbild-JavaScript und die auf ein falsches Theme zielenden doppelten CSS-Regeln sowie die jetzt überflüssigen Sidebar-Foto-Stile. Kein neues Plugin, kein zweiter Artikeleinstieg, kein neuer WordPress-Datenbanktisch.
- **Wie Hab & Bewahr:** Nur tatsächliche relevante Inhalte/Verweise in der rechten Spalte; keine bildlosen Amazon-Suchbanner oder Produkt-Dummys im Lesetext. Echte Amazon-Produktkarten bleiben bei HD009/DataForSEO, bis eine freigegebene Quelle und sinnvoller Slot verfügbar sind.
- **Unverändert:** Bereits abgestimmte Leseschrift und der Hab-inspirierte Zweispalten-Modellentwurf aus 1.50.804/1.50.805 bleibt zunächst auf den bestehenden Zweileiner-/Vierleiner-Design-Testartikel begrenzt. Diese Artikeleinteilung wird nicht ohne Sicht-PASS auf alle übrigen Beiträge ausgeweitet. Original-Hero, Claim, „Auf einen Blick“, Textlisten, echte zusätzliche Sachbilder, andere Artikeltexte, Bilder in Archiv-/Kategoriebannern, Homepage, Hobbyregister, HD009 0.1.28 und HD006 Bildzentrale bleiben erhalten.
- **Harte Tests:** Exaktes Ausgangs-ZIP 1.50.805 anhand SHA bestätigt; vollständiges ZIP **1.290/1.290 CRC PASS**, alle **13 PHP-Dateien Syntax PASS**. Der echte neue PHP-Filter wurde ausgeführt: identische Bildkopie entfernt, andere Bilder erhalten, generischer Textbanner weg, unverwandte Banner-/Kategorie-URLs unangetastet, rechte Spalte ohne Foto. Browser-Simulation mit echtem Live-Testartikel bei **1440/960/768/390/360 Pixel PASS**, ein Hero, kein zweites Drachenbild, kein text-only Amazon-Banner und keine überlaufenden Spalten. GitHub Action **42489458324**.
- **Noch offen:** Installation im produktiven WordPress und Live-Sichtabnahme. Die Browserprüfung verwendet die tatsächliche vorhandene Live-HTML-Seite und simuliert die neuen Änderungen; sie ersetzt **keinen** Livebeweis einer Installation. Andere Kategorieseiten mit fehlenden Herofotos gehören fachlich zur getrennten Bildzentrale/Seitendesign-Frage, nicht zum Beitragsdoppelbild.
