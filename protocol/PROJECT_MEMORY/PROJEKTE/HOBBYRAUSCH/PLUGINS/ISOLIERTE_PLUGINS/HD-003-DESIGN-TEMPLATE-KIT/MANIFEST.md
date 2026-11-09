# HD003 Pluginbüro – Stand 09.11.2026

**CURRENT: 1.50.809** – vollständiger getesteter Installer und `CURRENT.zip` byteidentisch (65.763.496 Bytes, SHA-256 `3814889dd2178d1af3674a119284cab8d7317c7a70679ed835fb616fe0bbe79b`).

Änderung nur im mobilen Kategorietext: sichtbarer und ausgeklappter Teil exakt 14 px (bis 760 px), Sonderregeln einbezogen. Hobbyfinder-Code/Fotos und Banner aus 1.50.808 unverändert. Browser-Mobiltest mit gültigem Testbild PASS; Live-Hobbyfinder unter bekannten Adressen aktuell 404 und daher nicht live geprüft. Vollversion im [GitHub Release](https://github.com/hallo-netizen/affiliate-pferdeportal/releases/tag/hobby-depot-hd003-1.50.809-mobile-14px), Prüfworkflow [42586622583](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/42586622583). Live-Installation noch offen. 1.50.808 archiviert.

---

# HD003 DESIGN-PLUGIN – PLUGINBÜRO / CURRENT

**Stand 08.11.2026: 1.50.808 ist der aktuell archivierte Installationskandidat.**  
**Büro-Voll-ZIP und `CURRENT.zip` sind auf diesem GitHub-Branch identisch**, beide verweisen auf Blob `3403ec7ad32a2fcec5a5bff0f21186d86d0d1909` (65.763.366 Byte, SHA256 `cbf03e54dd7bf4ae44ea6beac66f1ee53d188732d6da4b6c1c92df1b9b5b8f15`).

**Änderung gegenüber 1.50.806:** Nur der Hobbyfinder erhält das freigegebene Lupen-Hero und den Untertitel **„Das passende Hobby für dich.“**. Nach Ablehnung der zu flachen 1.50.807-Werbung gilt wieder das **unveränderte Originalwerbebanner aus 1.50.806**, inklusive Bildgröße, beider Buttons und Klickbereiche. Andere Seiten, Beiträge und Plugins unverändert.

**Nachweise:** [Design-Pluginakte CURRENT](../../PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md), [EVIDENCE_1.50.808](../../PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/EVIDENCE_1.50.808.md), GitHub Actions `42506740141`: 13/13 PHP-Syntax, 1291/1291 ZIP-CRC, 1288 unveränderte Originaldateien, Werbe- und Linkregressionen PASS. **Livetest 1.50.808 noch nicht belegt.**

**GitHub-Änderung:** [PR #724](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/724) → Projekt-Campus-Hauptbranch; noch nicht als übernommen behaupten.

**Original-Vollversion im Release:** https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hobby-depot-hd003-1.50.808-original-banner/HOBBY_DEPOT_DESIGN_HD003_1.50.808_HOBBYFINDER_BANNER_ORIGINAL.zip

---

## Historische Manifest-Angaben – 1.50.806 (nicht mehr Current)

# HD003 – Hobbydepot Design – gültige Current-Version

**Sichtabnahme des Nutzers, 08.11.2026:** HD003 **1.50.806** für das Hobbydepot-Beitragsdesign **„erst einmal okay, bis auf Kleinigkeiten“**. Dies ist eine **vorläufige Freigabe des erreichten Testartikel-Designs**, keine Detail-Vollabnahme und insbesondere **keine Freigabe einer produktiven Amazon-Artikelbox**. Gesicherter aktueller Vollinstaller `HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip` plus byteidentisches `CURRENT.zip` (Git-Blob `e3496adbc4524da0c6375d198d9010e2cc30d9f4`, SHA-256 `665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358`). Nichts am Plugin geändert, **keine Versionsänderung**. Ein Hero, kein wiederholtes Hero-Foto, kein bildloser Amazon-Suchbanner im Artikel, keine zweite Bildkachel rechts. Hab-&-Bewahr-inspirierter Lesestil bleibt zunächst **nur auf dem markierten Testartikel**; Detailkleinigkeiten bleiben offen, aber keine neue Designrunde ohne Anlass. **Nächster Arbeitsbereich ist die echte Amazon-Produktbox auf Artikelebene in der HD009 Affiliate-Zentrale**, einschließlich DataForSEO-Recherche, Freigabe, korrekter Zuordnung und erlaubtem Produktbild. HD003, HD006 (Bildzentrale), HD007 und die bestehende HD009 0.1.28 bleiben durch diese Dokumentation unangetastet.



**Version 1.50.806 · 08.11.2026**

- Vollständiges WordPress-Plugin: `HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip`, **65.705.901 Bytes**, SHA-256 `665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358`, Git-Blob `e3496adbc4524da0c6375d198d9010e2cc30d9f4`. `CURRENT.zip` ist byteidentisch. Installierter WordPress-Pluginordner und Einstieg bleiben `affiliate-portal-template-kit/pferde-template-kit.php`; die getrennte **HD006 Bildzentrale** wird ausdrücklich nicht umbenannt oder verändert.
- **Ursache des sichtbaren Fehlers:** Das bestehende Artikel-Hero übernimmt ein Gutenberg-Foto, aber die bisherige ausgegebene Dubletten-Vermeidung richtete sich an ein fremdes Theme-Element `.entry-content`, während Hobbydepot ListingHive `.post__text` verwendet. Daher wurde dasselbe JPG nochmals im Artikel gezeigt. Dazu kam die alte, bildlose automatisch eingefügte HD009-Textbannerkachel `data-ppar-slot="post_inline_banner"` und die in 1.50.805 nachträglich eingeführte zweite Drachenfotografie in der rechten Kategorienkarte.
- **KISS-Ursachenfix 1.50.806:** Beim endgültigen Ausgeben eines normalen WordPress-Beitrags wird nur das tatsächlich im Hero gezeigte JPG aus dem Gutenberg-Fließtext entfernt (per Bild-URL-Abgleich; keine anderen Sachbilder werden gelöscht). Der automatisch eingefügte generische `post_inline_banner` verschwindet ebenfalls aus Artikeln, nicht jedoch aus Kategorie-, Register- oder Startseiten. Eine nachgeladene Post-Inline-Anzeige wird als Sicherung ausgeblendet. Die rechte Hab-inspirierte Spalte zeigt vorhandene echte Kategorie-/Beitragslinks **ohne weiteres Foto**; das falsche, auf Sportdrachen fest verdrahtete Foto wurde entfernt.
- Entfernt aus dem selben bestehenden HD003-PHP auch den alten erfolglosen `wp_footer`-Doppelbild-JavaScript und die auf ein falsches Theme zielenden doppelten CSS-Regeln sowie die jetzt überflüssigen Sidebar-Foto-Stile. Kein neues Plugin, kein zweiter Artikeleinstieg, kein neuer WordPress-Datenbanktisch.
- **Wie Hab & Bewahr:** Nur tatsächliche relevante Inhalte/Verweise in der rechten Spalte; keine bildlosen Amazon-Suchbanner oder Produkt-Dummys im Lesetext. Echte Amazon-Produktkarten bleiben bei HD009/DataForSEO, bis eine freigegebene Quelle und sinnvoller Slot verfügbar sind.
- **Unverändert:** Bereits abgestimmte Leseschrift und der Hab-inspirierte Zweispalten-Modellentwurf aus 1.50.804/1.50.805 bleibt zunächst auf den bestehenden Zweileiner-/Vierleiner-Design-Testartikel begrenzt. Diese Artikeleinteilung wird nicht ohne Sicht-PASS auf alle übrigen Beiträge ausgeweitet. Original-Hero, Claim, „Auf einen Blick“, Textlisten, echte zusätzliche Sachbilder, andere Artikeltexte, Bilder in Archiv-/Kategoriebannern, Homepage, Hobbyregister, HD009 0.1.28 und HD006 Bildzentrale bleiben erhalten.
- **Harte Tests:** Exaktes Ausgangs-ZIP 1.50.805 anhand SHA bestätigt; vollständiges ZIP **1.290/1.290 CRC PASS**, alle **13 PHP-Dateien Syntax PASS**. Der echte neue PHP-Filter wurde ausgeführt: identische Bildkopie entfernt, andere Bilder erhalten, generischer Textbanner weg, unverwandte Banner-/Kategorie-URLs unangetastet, rechte Spalte ohne Foto. Browser-Simulation mit echtem Live-Testartikel bei **1440/960/768/390/360 Pixel PASS**, ein Hero, kein zweites Drachenbild, kein text-only Amazon-Banner und keine überlaufenden Spalten. GitHub Action **42489458324**.
- **Noch offen:** Installation im produktiven WordPress und Live-Sichtabnahme. Die Browserprüfung verwendet die tatsächliche vorhandene Live-HTML-Seite und simuliert die neuen Änderungen; sie ersetzt **keinen** Livebeweis einer Installation. Andere Kategorieseiten mit fehlenden Herofotos gehören fachlich zur getrennten Bildzentrale/Seitendesign-Frage, nicht zum Beitragsdoppelbild.
