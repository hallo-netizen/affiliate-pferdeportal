# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.700 NATIVER FOOTER-HANDOFF LOKAL PASS / LIVE-ABNAHME OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## AKTUELLER BELASTBARER STAND

### Textbestand unverändert übernommen
- Detail-Hobby-Benchmark bleibt **1.50.694**, insbesondere die acht vom Nutzer ausdrücklich freigegebenen Pflanzen-Texte.
- **1.50.696 Schrift & Lettering** bleibt bestätigte grafische Hub2-Benchmark.
- Die mit **1.50.698** korrigierten **69/69 Hub2-Einstiege** bleiben unverändert.
- vollständiger 395er Detail-Hub-Textbestand unverändert.
- Aufklapptexte und Informations-Erhaltung aus 1.50.698 unverändert.
- Bilder, Kategoriebaum, Affiliate-Slotarchitektur und Meta-/SEO-Titel unverändert.

### Startseite 1.50.699
Der Nutzer hat die Startseitenführung vereinfacht. Freies Stöbern erfolgt direkt über die unmittelbar unter dem Hero sichtbaren Hobbywelten; dafür wird kein zusätzlicher Hero-Pfad benötigt.

Umgesetzt:
- redundanter Hero-Button **„Hobbys entdecken“** entfernt;
- Hero führt nur noch zum **Hobbyfinder**;
- kurze Finder-Anmoderation: **„Noch unsicher, was zu dir passt?“**;
- CTA: **„Hobbyfinder starten →“**;
- **„Unsere Hobbywelten“ → „Deine Hobbywelten“**;
- Unterzeile gekürzt auf **„Klick dich rein und finde Hobbys, die zu dir passen.“**;
- **„Entdecke unsere Themenbereiche.“** entfernt;
- Textlink **„Alle Hobbywelten entdecken →“** entfernt;
- **„Zeit, Budget & Platz“** nur aus den Startseiten-Themen entfernt, nicht aus Editorial-/SEO-Bestand;
- Anbieter bleibt separate DIRECTORY-/HivePress-Säule und Footer-Weg.

Konzeptbindung:
- Hobbyfinder = geführter Auswahlweg auf demselben zentralen Hobbybestand;
- Kriterien wie drinnen/draußen, alleine/zu zweit/Gruppe, ruhig/aktiv, Zeit, Platz, Kosten/Budget, Saison und Ausrüstungsbedarf sind Finder-/Filtermerkmale und werden nicht automatisch eigene Hauptnavigation;
- kein zweiter Hobbybestand, keine neue Architektur.

### Lokale QA 1.50.699
- fokussierte Startseitenprüfung: **8/8 PASS**;
- PHP-Lint: **135/135 PASS**;
- Fresh-Unpack-PHP: **135/135 PASS**;
- ZIP-Integrität: **PASS**;
- aktive Version: **1.50.699**;
- aktive Klasse: Hobby_Depot_Profile_V150699;
- Vergleich gegen 1.50.698: **0 unerwartete Änderungen an vorhandenen Dateien**;
- bestehende 1.50.698-Fach-/Text-/Bildbasis nicht umgebaut.

### Footer-Handoff 1.50.700
Der Screenshot-/Codeabgleich vom 20.10.2026 hat belegt, dass 1.50.699 zusätzlich zum nativen Theme-/Astra-Footer einen eigenen dunklen Hobby-Depot-Footer über `wp_footer -> render_footer` ausgab. Dadurch existierten zwei Footer-Eigentümer gleichzeitig.

1.50.700 entfernt ausschließlich diesen einen aktiven Hook. Der restliche Hobby-Depot-Designstand bleibt unverändert. Der native WordPress-/Astra-Footer ist damit wieder alleiniger Footer-Eigentümer und kann durch die Footer-Umzugshilfe mit Menüs/Seiten/Widgets bestückt werden.

Lokale QA:
- PHP-Lint: **136/136 PASS**;
- Hook-Differenz 1.50.699 → 1.50.700: **exakt 1 entfernt** (`wp_footer -> render_footer`, Priorität 5);
- zusätzliche/geänderte Hooks: **0**;
- Footer-Umzug 1.1.1 bindet die exportierten Footer-Widgets an `footer-widget-*`: **PASS**;
- Footer-Umzug 1.1.1 schreibt keine Astra-Settings: **PASS**;
- ZIP-Integrität: **PASS**.

ARTEFAKT:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.700_NATIVE_FOOTER_HANDOFF_LOCALPASS.zip

SHA-256:
6a3e936db91f3a6ab7aba6af66bc6a86b308ca1cbf7c6478b3be7224d44e02c3

GRÖSSE:
58,801,072 Bytes.

## ERSTER OFFENER BLOCKER

Echter WordPress-/Frontend-Readback des 1.50.700-Stands nach einmaligem Footer-Import. Kein Live-PASS aus lokaler QA ableiten.

## EXAKT EINE NEXT ACTION

**1.50.700 installieren, danach Footer-Umzug 1.1.1 einmal mit der bereinigten Hobby-Depot-JSON ausführen und im Frontend prüfen, dass nur noch der native Footer erscheint und die vier importierten Footer-Bereiche sichtbar sind. Danach Footer-Umzug wieder entfernen.**

## ARBEITSBINDUNG

- 1.50.694 = redaktionelle Detailtext-Benchmark.
- 1.50.696 = bestätigte Hub2-Grafikbenchmark.
- 1.50.698 = bestätigter lokaler Hub2-Textstand, in 1.50.699 unverändert.
- 1.50.699 = Startseitenfassung vor Footer-Handoff.
- 1.50.700 = aktueller Designstand; identisch zu 1.50.699 außer Entfernung des zusätzlichen eigenen Footer-Render-Hooks.
- Keine neue Architektur.
- Keine Änderungen an Kategoriebaum, Affiliate-Slotarchitektur, Meta-/SEO-Titeln oder Bildern.
- Header-/Responsive-Navigation und Pferdeatelier-Footer sind separate nächste Designblöcke nach der Startseiten-Sichtprüfung.
