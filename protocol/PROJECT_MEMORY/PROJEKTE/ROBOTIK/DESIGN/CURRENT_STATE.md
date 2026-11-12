# ROBOTIK – DESIGN – CURRENT

## NEUESTER STAND 12.11.2026 – V0.2.2 ROOT-FIX (lokal PASS, live OFFEN)
- Voriges 0.2.1 trotz Installation laut Nutzer im echten Screenshot ohne Wirkung; die aktive Serverversion ist unabhängig nicht bestätigt. Nicht behaupten, dass ein Browsermock ein WordPress-Live-PASS ist.
- Bewährte Hobbydepot-/Hab-&-Bewahr-Kopf-/Fußstruktur geprüft. **Einziges Robotik-Designplugin** `robotik-strukturdesign` v0.2.2: exakte Site-Root über WordPress `template_redirect` vollständig als schlichte Testansicht ausgeben; keine Theme-Blogansicht oder Seitenleiste; auf Unterseiten Theme unverändert.
- Lokaler Route-Test, 7 reale WP-Hauptbereiche, Footer, Industrie, Browser 1440/1024/390 und ZIP-/PHP-Tests PASS. Sichtbarer Live-Erkennungsmarker „Strukturansicht 0.2.2“ im Footer. Wenn der fehlt: installierte Version/Cache prüfen, nicht neues Plugin raten.
- **Installer:** Library `/robotik/Designbüro/ROBOTIK_STRUKTURDESIGN_0.2.2_ROOT_FIX.zip` (aktuell für Test, 0.2.1 abgelöst), Bericht `TESTDESIGN_022_20261112.md` und Library `ROBOTIK_DESIGN_022_ABNAHME_2026-11-12.md`. Kein WordPress-Live-PASS.
- Kategorie-Workflow/DataForSEO 0.4.2 unverändert; keine neue Synchronisierung.


## AKTUELL 12.11.2026 – TESTDESIGN 0.2.1 nach WordPress-Screenshot
- **Einziger aktuelle Testinstaller:** Library `/robotik/Designbüro/ROBOTIK_STRUKTURDESIGN_0.2.1_GEPRUEFT.zip` (Update derselben Pluginidentität, 0.2.0 ist abgelöst; die ältere GitHub-Binärablage bitte nicht als aktuellen Installer ausgeben).
- Ursache nach Screenshot: Die WordPress-Blog-Startseite mitsamt Sidebar wurde vom bisherigen Designplugin nicht ersetzt. Die Kategorieübersicht war an das alte Theme angehängt. **0.2.1** gibt nur für die Startseite eine eigene minimale WordPress-konforme Darstellung aus: oben 7 Hauptkategorien / aufklappbares Mega-Menü, unten klarer Footer. Andere WP-Seiten bleiben im Theme.
- Lokal PHP-/JS-/ZIP-Prüfungen PASS; Browser 1440 / 1024 / 390 PASS; eingebetteter Importplan 104 Seiten, 7 Hauptbereiche und Industrie unter Gewerbe PASS. Echte WordPress-Live-Prüfung bleibt offen.
- Kategorie-Workflow/DataForSEO **0.4.2 unverändert**. Kein neuer Kategorieimport.
- Vollständiger Beleg: `TESTDESIGN_021_20261112.md`. Nächster Schritt nur Designplugin 0.2.1 als Update installieren, Frontend prüfen.


## NEUESTER STAND 12.11.2026 – Mini-Design 0.2.0 TEST, noch nicht Live
- Korrigierte monochrome Darstellung mit einem gemeinsamen Header, sieben Hauptmenüs, Industrie unter Gewerbe und sichtbarem Footer, rein aus echten Robotik-Seiten.
- Alte 0.1.0-Versteckung des Theme-Footers konnte den eigenen Footer verdecken; neues JS versetzt beide Blöcke nach `body`, erst danach wird der Theme-Rahmen ausgeblendet.
- Lokale Chromium-Proben Desktop/Mobil inkl. fehlendem `wp_body_open` PASS; echter WordPress-Theme-Test noch ausstehend.
- **Installer:** `/robotik/Designbüro/ROBOTIK_STRUKTURDESIGN_0.2.0_TEST.zip`. DataForSEO-Plugin 0.4.2 separat im Kategorie-Konzeptbüro. Details: `TESTDESIGN_020_20261112.md`.


## NEUESTER STAND 11.11.2026 – einfaches Testdesign lokal fertig, NOCH NICHT LIVE
- **Designplugin `Robotik Strukturdesign 0.1.0 (Test)` erstellt:** monochrom, keine Bilder/Farben, Mega-Menü aus den tatsächlich importierten 7 CORE-Wurzelseiten, Industrie als abgesetzter Teil von Gewerbe, Footer mit denselben 7 Bereichen und echten Unterseiten; responsive mobile Navigation.
- Keine erfundenen Seiten/Links; noch nicht angelegte Magazin-/Finder-/Anzeigenmarktseiten nur als nicht anklickbare Beschriftung.
- ZIP-Test, PHP-Lint, JavaScript-Syntax und lokaler Render-Test BESTANDEN. Kein WordPress-Live-/Mobil-PASS behauptet.
- **Installierbares ZIP:** Library `/robotik/Designbüro/ROBOTIK_STRUKTURDESIGN_0.1.0_TEST.zip`. Design ist ein **eigenes Plugin**, Kategorie-Import bleibt getrennt.
- **Bericht:** `TESTDESIGN_MEGA_FOOTER_20261111.md`; ältere V4-/V5-Hauptnavigationseinträge nachfolgend sind historisch, die aktuell geplante Navigation ist Haushalt · Garten · Freizeit · Sport · Bildung · Pflege · Gewerbe.

Stand: 10.11.2026

**Farbentscheidung getroffen:** Silber + Technikblau + Kupfer. KISS, hochwertig, hell, industriell-präzise, warm akzentuiert.
**Erledigt:** eigenständiges Designbüro und erste verbindliche Farb-/Typografie-/Bildregel.
**Noch offen:** Logo/Signet, Voransicht von Start-/Kategorieseite, responsive Abnahme und Übernahme in ein eigenes WordPress-Designplugin. Keine bestehende Portalvorlage wird ohne Prüfung kopiert.
**Nächster Schritt:** nach dem Kategoriekonzept Startseite, Kategorie-Landingpage und Produktseite als gemeinsame Designs definieren.

## Schnittstelle Kategorie-Design – 10.11.2026 (KEINE Design-Implementierung)
Der aktuelle Fachentwurf liefert **acht** kurze CORE-Hauptnavigationstitel und durchgehend **1–2-Wort-Labels** für Seiten und produktbezogene Inhaltskategorien aus `../KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json` **Revision 10**, Feld `navigation_v1`. Der vollständige H1-/Seiten-/Meta-Text darf wesentlich länger sein; **KEINE** Übernahme künstlich verlängerter Suchphrasen in Menüs. Bisherige zehn Welten nur als historische IDs; spätere Sichtprüfung am echten Robotik-Theme auf Desktop/Mobil, Überlauf und alle gültigen Unterknoten. Keine Pluginänderung und kein WordPress-Live-Nachweis durch diese Dokumentation. [Konzept und Quellen](../KATEGORIE/RECHERCHE/KURZNAMEN_HAUPTNAVIGATION_V4_20261110.md).

## Zielgruppenorientierte Navigation – V5 (10.11.2026, Konzept)
Der zuvor als **acht gleichrangige Fachwelten** dokumentierte V4-Navigationsentwurf wurde konzeptionell ersetzt: Startseite und sieben vorläufige Käufer-Menüpunkte für Privatkunden/kleinere Betriebe, zusätzlich **Industrie** als einzelner sichtbar, nicht dominierender Hauptmenüpunkt mit eigener Übersicht und drei Unter-Landingpages. Magazin, Glossar, Register, Finder und Anzeigenmarkt sind **für alle gemeinsam**, nur fachliche Rubriken/Filter innen. **Keine zweite WordPress-Produktstruktur und keine zweite Produktseite**. Stand nur Designvorgabe, kein Live-Menü. Aktueller Master Revision 11 `../KATEGORIE/RECHERCHE/PRODUKTE_V2_20261108.json` → `audience_navigation_v2`, [Details](../KATEGORIE/RECHERCHE/ZIELGRUPPEN_NAVIGATION_V5_20261110.md). Farben/Designplugin unangetastet.
