# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.701 FOOTER-RUNTIME-HOTFIX LOKAL PASS / LIVE-ABNAHME OFFEN**

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

### Korrektur 1.50.701 – Footer-Runtime

1.50.700 war fehlerhaft und ist verworfen. Exakte Ursache: Die Hauptdatei lud die neu benannte Klasse `Hobby_Depot_Profile_V150700`, während die weiterhin gerouteten Templates `hobby-depot-front-v150699.php` und `hobby-depot-content-v150699.php` weiterhin `Hobby_Depot_Profile_V150699` aufriefen. Ergebnis im Frontend: Fatal Error / „Class Hobby_Depot_Profile_V150699 not found“.

1.50.701 basiert deshalb wieder direkt auf dem funktionierenden 1.50.699-Runtimevertrag. Klassenname, Klassendatei und beide gerouteten Templates bleiben unverändert auf V150699 gebunden. Nur die Pluginversionsnummer ist 1.50.701.

Footerlogik 1.50.701:
- vorhandener Hobby-Depot-Brandblock bleibt;
- vorhandene Hobby-Depot-Einstiege Hobbyfinder / Magazin / Anbieter bleiben erhalten;
- importierte WordPress-Menüs `Informationen`, `Rechtliches` und `footer-anzeigen` werden direkt aus WordPress gelesen und im Designfooter ausgegeben;
- Magazin wird dedupliziert;
- kein erneuter Footer-Import für die Anzeige erforderlich, sofern Seiten/Menüs bereits importiert sind;
- 1.50.700 wurde aus der Library entfernt.

Lokale QA 1.50.701:
- PHP-Lint: **135/135 PASS**;
- Runtime-Klassenbindung Hauptdatei → Klasse → Fronttemplate → Contenttemplate: **PASS**;
- reproduzierter 1.50.700-Fatal: **in 1.50.701 ausgeschlossen**;
- Footer-Runtime-Harness mit importierten Menüs: Brand / Hobbyfinder / Magazin / Anbieter / Werben / Rechtliches / Anzeigenmarkt: **8/8 PASS**;
- geänderte Dateien gegenüber 1.50.699: Hauptdatei (nur Versionsnummer), aktuelle Hobby-Depot-Klasse (nur Footer-Datenquelle/-Darstellung), Evidence-Datei;
- ZIP-Integrität: **PASS**.

ARTEFAKT:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.701_FOOTER_RUNTIME_HOTFIX_LOCALPASS.zip

SHA-256:
7b1793f661452f05de29fd1dddc0389b8874924ee1eb4b676404590dbd8b6d3a

GRÖSSE:
58,671,462 Bytes.
## ERSTER OFFENER BLOCKER

Echter WordPress-/Frontend-Readback des 1.50.701-Stands. Kein Live-PASS aus lokaler QA ableiten.

## EXAKT EINE NEXT ACTION

**1.50.701 installieren und Frontend neu laden. Prüfen, dass der Fatal verschwunden ist und der Designfooter die bereits importierten Menüs Informationen, Rechtliches und Anzeigenmarkt zusätzlich zu Hobbyfinder / Magazin / Anbieter ausgibt. Keinen erneuten Import starten.**

## ARBEITSBINDUNG

- 1.50.694 = redaktionelle Detailtext-Benchmark.
- 1.50.696 = bestätigte Hub2-Grafikbenchmark.
- 1.50.698 = bestätigter lokaler Hub2-Textstand, in 1.50.699 unverändert.
- 1.50.699 = letzte funktionierende Basis vor Footer-Arbeit.
- 1.50.700 = **verworfen** wegen Runtime-Klassen-/Template-Mismatch.
- 1.50.701 = aktueller Designstand; 1.50.699-Runtimebindung bleibt erhalten, Footer liest zusätzlich die bereits importierten Menüs.
- Keine neue Architektur.
- Keine Änderungen an Kategoriebaum, Affiliate-Slotarchitektur, Meta-/SEO-Titeln oder Bildern.
- Header-/Responsive-Navigation und Pferdeatelier-Footer sind separate nächste Designblöcke nach der Startseiten-Sichtprüfung.
