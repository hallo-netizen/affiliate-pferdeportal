# Hab & Bewahr – Affiliate-Übergangsbanner RC13 – 07.11.2026

## Wo stehen wir?
**Vollständige WordPress-Test-ZIP im aktuellen Chat bereitgestellt:** `Hab-und-Bewahr-Affiliate-RC13-Banner-Test.zip` (627700 Bytes, SHA256 `4179371267f4d983b095ab846166c9d9dd44eb010c54e18ca3d808585c617f1e`, Version `0.1.10-rc13`). Enthält die zuvor **nicht installierte** RC12 komplett; kein separates Plugin. Nutzer hat RC12 ausdrücklich noch nicht installiert. GitHub-`HAB-004/CURRENT.zip` ist **weiter RC11**, also nicht die RC13-Datei und **nicht** die Testversion. Das ZIP aus dem Chat ist ein **offline bestandener Kandidat, nicht live installiert oder abgenommen**. ZIP-Quelle ist diese Konversation; nicht behaupten, sie liege bereits im GitHub-Pluginbüro.

## HARTE Quellprüfung, BEVOR geändert
**Vier Originale überprüft:** HAB-004 RC11 und RC12, HAB-001 Design inklusive Glossar-Template und Original-Themenbilder, Hobbydepot-HD009 0.1.20/Stand 0.1.22 und originales Pferdeatelier-Affiliate-Plugin. Beide Bannerformate waren im RC12-Amazon-House-Fallback **schon angelegt**; in RC13 wurde nur das vorhandene Markup/CSS wirklich quadratisch bzw. vollbreit und die **fehlende Anbindung an den echten HAB-001-Glossar-Sidebar-Filter** hergestellt. Keine neue Werbe-Engine, keine neue Datenbank, kein neuer Cron, keine zusätzlichen kostenpflichtigen Provider-Abfragen, keine Änderungen an anderen Portalen.

## Was funktioniert im RC13-Kandidaten? (OFFLINE)
- **Querformat** im bestehenden breiten Bannerplatz: dasselbe geprüfte Hab-Themenbild wie in der bestehenden Bildzentrale, sanfter Verlauf von links, ruhiger kleiner Amazon-Button, responsive Seitenbreite (Desktop 4.2:1, Mobile >=3.15:1 und Mindesthöhe).
- **Quadrat** in der vorhandenen **Glossar-Einzelseiten-Seitenleiste**: originales `hbdp_glossary_ad_markup` (HAB-001 `includes/glossary.php`) anstelle der bei Hab wirkungslosen Pferdeatelier-`the_content`-Insertion; 1:1-Quadrat, sanfter Verlauf von oben, kleines Amazon-CTA.
- Bereits bestehende Schaltung und Kampagnenauswahl **vor** Amazon-House-Fallback; bestehende Fremdwerbung/gebuchte Anzeige hat Vorrang. Fallback nur mit exakt freigegebenem, nachgewiesenem Themenbild, nur mit Aktivierung und gültiger Hab-Amazon-Tracking-ID `habundbewahr-21`. Link `https://www.amazon.de/s?k=<passendes_Kategorie-Thema>&tag=habundbewahr-21`; nie pauschale `XY Hobbyzubehör`-Links oder erfundene Einzelprodukte.
- Glossar: **veröffentlicht und fachlich passender, eindeutig belegter Kategorie-/Seitenbezug** aus `_hbdp_primary_target`. Wenn dieser fehlt, ausschließlich eindeutige EXAKTE Kategorie-Titelübereinstimmung. Bei fehlendem Bezug, fehlendem freigegebenem Foto oder fehlender Amazon-Aktivierung **kein** Falschbanner. Nicht versprechen, dass auf allen Glossarseiten eine Anzeige erscheint.
- Echte Hab-Designbilder geprüft: `topic-62-wassermelder.webp` (1672×941 px) für Wassermelder, `new-boiler.webp` (1619×971 px) für Leckwarnung & Absperrung; in Original-HAB-001-ZIP vorhanden, kein neues Bild importiert. Sind als **Themenfotos** gekennzeichnet, **nicht** als Produktfoto einer spezifischen ASIN.
- RC13 berührt nur fünf Dateien von 28 (23 byteidentisch gegenüber RC12): Hauptdatei (nur bestehender Glossar-Renderer-Aufruf + Version), `class-ppar-hab-bewahr-bridge.php` (bestehender Glossar-Filter), `trait-ppar-hb-amazon.php` (Banner-Text), `assets/frontend.css` (nur RC12-House-Banner-CSS gegen zwei korrekte Formate), `readme.txt` (Version). Mehranbieter-Buttons, DataForSEO, Produktimport, Amazon-Einzelkarten, eBay/Idealo-System unverändert.
- 20 PHP-Funktionstests PASS: native Filter, echtes Kategorienbild, Quadrat, Suchlink/Tracking, Disclosure, manuelle/Buchungspriorität, kein extra Anbieter, kein Produktfoto-Missbrauch, Amazon AUS, global AUS, fehlendes Foto, unveröffentlichtes Glossar, unbekanntes Glossar, doppeldeutige/ungültige Zielzuordnung, außerhalb des Glossars, breites Banner.
- 25/25 PHP-Syntaxprüfungen, 28/28 ZIP-CRC PASS.
- Browser-Screenshots mit **echtem Original-Themenbild**, mit Glossar-CSS + Original-Affiliate-CSS: 1200px, 1024px und 390px, Querformat, Quadrat, klickbarer Button innerhalb des Formats, kein horizontaler Überlauf; **nur Browser-/Mock-Layout, keine echte Live-WordPress-Abnahme**.

## Nicht Teil dieser Bannerphase
- **Einzelprodukte** bleiben vorerst als kompakte Amazon-ASIN-/Titel-Links ohne Einzelproduktfotos; eBay-/Idealo-Fotos und weitere Anbieter werden später eingerichtet. Nicht behaupten, RC13 hätte echte Amazon-ASIN-Produktbilder implementiert.
- Amazon-Bilder nie als Produktfoto ohne geprüfte Nutzungsrechte; selbst gestaltete Banner bestehen aus eigenen Hab-Themenbildern.
- Live-Installation muss danach bestätigt werden; insbesondere Glossar-Einzelseite mit **tatsächlich freigegebenem passenden Target**, Kategorie Wassermelder und R3-Produktseiten sowie Format Desktop/Mobil prüfen.
- Kein RC12-Installations-Zwischenschritt; die vollständige RC13-ZIP ersetzt direkt das bisherige HAB-004 WordPress-Plugin.

## Projektstatus
**BANNERSLOT IMPLEMENTIERT UND OFFLINE-GEPRÜFT; LIVE NOCH OFFEN.**
**PLUGIN-EINZELPRODUKTBILDER WEITERHIN NICHT GELÖST, NICHT VERDECKEN.** 
Die endgültige `CURRENT.zip` auf GitHub ist nicht automatisch die im Chat erzeugte RC13-Datei. Spätere Chats müssen ZIP und SHA vor Änderungen unterscheiden und ohne Vermutung prüfen.
