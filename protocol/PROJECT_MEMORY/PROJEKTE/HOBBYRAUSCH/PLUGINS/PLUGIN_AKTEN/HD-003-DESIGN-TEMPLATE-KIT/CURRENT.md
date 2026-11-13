# HD003 CURRENT 1.50.811 – ein Anzeige-Hinweis / Produktkarten 3-2-1

Vollständiges ZIP SHA256: 3cc8118ed5d9d22acadfd2e9aa9184068f71cbe9ccb2574bcffacdd16d8ac6df. Sicherung 1.50.810 erhalten. Beweis: DESIGN/HD003_PRODUKTKARTEN_ANZEIGE_EINMAL_1.50.811_20261113.md.

---

# HD003 – Hobbydepot Design – CURRENT 1.50.810 (09.11.2026)

**Aktuelle geprüfte Vollversion 1.50.810:** Mobile Weiter-Navigation im Hobbyfinder wird jetzt nach jedem Schritt sichtbar an die neue Frage und die erste Auswahlmöglichkeit gescrollt; nach Schritt 8 zur Ergebnisüberschrift. Gilt ausschließlich für Bildschirmbreiten bis 720 px. Desktop, Hobbyregister-Kern HD007, Foto-/Affiliate-Funktionen und die 14-px-Kategorie-Korrektur aus 1.50.809 unverändert.

**Geprüft:** Original-1.50.809-SHA als Ausgangspunkt, 13/13 PHP syntax, ZIP-CRC 1291/1291, nur 2 veränderte PHP-Dateien (Versionskopf + Hobbyfinder-Weiter). Aus dem neuen Plugin extrahiertes echtes Hobbyfinder-JavaScript: acht Weiter-Schritte einschließlich Ergebnisübergang in Browser-Simulation mit 360, 390 und 700 px PASS; Desktop 1024 px ohne automatische Positionsänderung PASS. GitHub Test-Workflow [42592986004](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42592986004).

**Installationsdatei:** https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hobby-depot-hd003-1.50.810-mobile-weiter-scroll/HOBBY_DEPOT_DESIGN_HD003_1.50.810_MOBILE_WEITER_SCROLL.zip
Vollversion im isolierten Pluginbüro: `HOBBY_DEPOT_DESIGN_HD003_1.50.810.zip` und identische `CURRENT.zip`. 65.763.742 Byte, SHA-256 `d63c2c7413f1f3d8ac635abffd3ec7ea69ea0fddff5b4fc6dd4e676ac9c7b1c6`. Vorversion 1.50.809 unverändert im Archiv. **WordPress-Liveinstallation und Liveabnahme offen.**

---

# HD003 – Hobbydepot Design – CURRENT 1.50.809 (09.11.2026)

**Aktuelle geprüfte Vollversion: 1.50.809.** Original 1.50.808 bytegenau als Ausgangspunkt geprüft; nur die vorhandenen Design-PHP-Dateien gezielt verändert (Versionswechsel und mobile Kategorietexte).

- **Mobil bis 760 px:** sichtbarer und ausgeklappter Kategorietext einheitlich **14 px**, einschließlich mittlerer Ebene und Sonderfall **Schuhmacherei/Kettenhemd-FAQ**. Überschriften, Desktop, Layout und Fremdplugins unverändert.
- **Hobbyfinder Ergebnisfotos:** die Originalfunktion gibt Bilder nur bei vorhandener, genau zugeordneter Bild-URL aus; das mobile Raster blendet Fotos nicht aus. Mobile Rendering-Test 360/390/620/760 px mit vorhandenem Testbild erfolgreich. **Kein Live-PASS** für echte Hobbyfinder-Ergebnisbilder, da `/magazin/hobbyfinder/` und `/hobbyfinder/` bei der aktuellen Liveprüfung 404 lieferten; keine Bildzuordnungen geändert.
- **Prüfung:** ZIP 1291/1291, PHP 13/13, Quellvergleich genau 2 betroffene PHP-Dateien, Browser-Regressionen 360/390/620/760/1024 px bestanden; GitHub Action [42586622583](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42586622583).
- **Volles Installations-ZIP:** https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hobby-depot-hd003-1.50.809-mobile-14px/HOBBY_DEPOT_DESIGN_HD003_1.50.809_MOBILE_14PX.zip
- Archivierte Vollversion `HOBBY_DEPOT_DESIGN_HD003_1.50.809.zip` und gleiches `CURRENT.zip` im isolierten HD003-Pluginbüro. 65.763.496 Bytes, SHA-256 `3814889dd2178d1af3674a119284cab8d7317c7a70679ed835fb616fe0bbe79b`.
- **WordPress-Installation/Sichtkontrolle noch offen.** Alte 1.50.808 bleibt unverändert als Rückfallversion, Pferdeatelier/K0, Affiliate HD009, Bildzentrale und Hobbyregister unangetastet.

---

# HD003 – Hobbydepot Design – CURRENT

**Aktuelle vollständige lokale Installationsfassung: 1.50.808 (08.11.2026).** Letzter vom Nutzer im Screenshot bestätigter Live-Stand: 1.50.807; 1.50.808-Live-Sichtprüfung offen.

**Warum 1.50.808?** Der Nutzer hat die zu flache, verzerrt wirkende Eigenwerbung in 1.50.807 verworfen und ausdrücklich die Rückkehr zum **alten Originalbanner aus 1.50.806** verlangt. Deshalb wurde das echte Originalbild samt Original-Höhenverhältnis, Original-Overlay und beiden vorhandenen Werbebedingungen-/Preise-Klickflächen **bytegenau aus 1.50.806 übernommen**. Keine künstliche Skalierung, kein abgeschnittener Flachbanner. Lupen-Hero und kurzer Untertitel **„Das passende Hobby für dich.“** bleiben von 1.50.807 erhalten.

**Voll-ZIP:** `HOBBY_DEPOT_DESIGN_HD003_1.50.808.zip` **und byteidentische `CURRENT.zip`** im isolierten HD003-GitHub-Pluginbüro auf Branch `hobbyroom/hd003-150807-hobbyfinder-20261108` (Git-Blob `3403ec7ad32a2fcec5a5bff0f21186d86d0d1909`). 65.763.366 Byte, SHA-256 `cbf03e54dd7bf4ae44ea6beac66f1ee53d188732d6da4b6c1c92df1b9b5b8f15`. GitHub-PR [#724](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/724) noch offen, Campus-Hauptbranch nicht überschrieben. Direkter Download: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hobby-depot-hd003-1.50.808-original-banner/HOBBY_DEPOT_DESIGN_HD003_1.50.808_HOBBYFINDER_BANNER_ORIGINAL.zip

**Prüfung:** 1.50.806-Ursprungs-ZIP exakt per SHA256 geprüft. Vollständiges 1.50.808-Plugin enthält 1291 Dateien: **1288 Originaldateien byteidentisch**, 2 PHP-Dateien gezielt geändert (Hobbyfinder-Bild-/Text-Zuordnung und Versionskopf), genau 1 neues Lupen-Bild. 13/13 PHP-Dateien Syntax PASS; ZIP CRC 1291/1291 PASS; Originalbanner-Bild/Styles/Klickflächen unverändert; zwei korrekte Zielpfade aus Original unverändert. GitHub Actions `42506740141` erfolgreich. Keine zusätzliche WordPress-Liveabnahme oder neue Seitenmodellierung behauptet.

**Unverändert:** alle anderen Magazine, Kategorien, Beitragsdesign, Anzeigenplätze, HD006 Bildzentrale, HD007, Affiliate, Pferdeatelier/K0. **Alte Eigenwerbe-Banner-Version unverändert**, nicht eine erneute Komprimierung des Bannerbilds.

**Bürovertrag:** [EVIDENCE_1.50.808.md](./EVIDENCE_1.50.808.md). Nur 1.50.808 als aktuelles Download-Plugin weitergeben; 1.50.807 archiviert.

---

## Historischer Zwischenstand 1.50.807 (durch Banner-Rücknahme abgelöst)

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
