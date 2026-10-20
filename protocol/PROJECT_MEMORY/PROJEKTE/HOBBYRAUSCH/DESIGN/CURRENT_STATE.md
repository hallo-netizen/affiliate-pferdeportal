# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.702 FOOTER-/SERVICESEITEN-FIX LOKAL PASS / LIVE-ABNAHME OFFEN**

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

### Korrektur 1.50.702 – Footer und importierte Serviceseiten

1.50.701 beseitigte den Runtime-Fatal, ließ aber zwei Darstellungsfehler offen:
- der eigene Hobby-Depot-Footer und der Theme-Footer wurden gleichzeitig sichtbar;
- normale importierte Seiten wie Impressum/Datenschutz/AGB liefen zusätzlich durch den generischen Hobby-Depot-Seitenintro-Renderer und erhielten dadurch einen zweiten Intro-/„Mehr erfahren“-Block vor dem echten Seiteninhalt.

1.50.702 korrigiert ausschließlich diese Ursachen und die gewünschte Footer-Reihenfolge:
- eigener Hobby-Depot-Footer bleibt der sichtbare Footer;
- nativer Theme-Footer `footer#colophon.site-footer` wird im Hobby-Depot-Profil ausgeblendet;
- Reihenfolge: **Rechtliches → Informationen → Anzeigenmarkt**;
- Informationen werden nur aus dem importierten Menü gelesen; kein Merge mit alten festen Portal-Links;
- Magazin dadurch exakt einmal;
- alter Anbieter-Link entfernt;
- Hobbyfinder vorerst separat als einzelner Link im Brandblock;
- 11 importierte Footer-/Serviceseiten werden vom generischen Intro-/„Mehr erfahren“-Renderer ausgenommen und zeigen ihren WordPress-Seiteninhalt damit nur einmal.

Lokale QA 1.50.702:
- PHP-Lint: **135/135 PASS**;
- Footer-Harness: genau ein eigener Footer: **PASS**;
- Reihenfolge Rechtliches / Informationen / Anzeigenmarkt: **PASS**;
- Magazin exakt einmal: **PASS**;
- Anbieter nicht vorhanden: **PASS**;
- Hobbyfinder exakt einmal separat: **PASS**;
- 11/11 importierte Seitenslugs ohne zusätzlichen generischen Introblock: **PASS**;
- Theme-Footer-Hide-Regel: **PASS**;
- importierte DB-Seiteninhalte selbst nicht verändert.

ARTEFAKT:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.702_FOOTER_SERVICEPAGE_FIX_LOCALPASS.zip

SHA-256:
e9670785905041bd4d24cfe5a62138e2d8b9b37572115f6f7d5076481ab15859

GRÖSSE:
58,673,102 Bytes.
## ERSTER OFFENER BLOCKER

Echter WordPress-/Frontend-Readback des 1.50.702-Stands. Kein Live-PASS aus lokaler QA ableiten.

## EXAKT EINE NEXT ACTION

**Nur 1.50.702 über 1.50.701 installieren und Frontend neu laden. Keinen erneuten Footer-Import starten. Prüfen: nur ein Footer; Reihenfolge Rechtliches → Informationen → Anzeigenmarkt; Magazin einmal; Anbieter weg; Hobbyfinder separat; Impressum/AGB/Datenschutz usw. ohne zusätzlichen „Mehr erfahren“-Block und ohne doppelten Inhalt.**

## ARBEITSBINDUNG

- 1.50.694 = redaktionelle Detailtext-Benchmark.
- 1.50.696 = bestätigte Hub2-Grafikbenchmark.
- 1.50.698 = bestätigter lokaler Hub2-Textstand, in 1.50.699 unverändert.
- 1.50.699 = letzte funktionierende Basis vor Footer-Arbeit.
- 1.50.700 = **verworfen** wegen Runtime-Klassen-/Template-Mismatch.
- 1.50.701 = Runtime-Hotfix, ersetzt durch 1.50.702.
- 1.50.702 = aktueller Designstand; Footer nur einmal, gewünschte Menüordnung, keine Zusatz-Intros auf importierten Serviceseiten.
- Keine neue Architektur.
- Keine Änderungen an Kategoriebaum, Affiliate-Slotarchitektur, Meta-/SEO-Titeln oder Bildern.
- Header-/Responsive-Navigation und Pferdeatelier-Footer sind separate nächste Designblöcke nach der Startseiten-Sichtprüfung.
