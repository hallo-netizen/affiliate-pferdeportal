# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.703 SERVICE-TITEL + NATIVE-FOOTER-FIX LOKAL PASS / LIVE-ABNAHME OFFEN**

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

### Korrektur 1.50.703 – Serviceseitentitel und ListingHive-Footer

1.50.702 beseitigte die Zusatz-Intros, entfernte dabei aber zugleich den einzigen sichtbaren Seitentitel der importierten Serviceseiten. Außerdem griff die bisherige Theme-Footer-Ausblendung im realen ListingHive-Frontend nicht zuverlässig.

Exakt korrigiert:
- 11 importierte Serviceseiten erhalten genau einen sichtbaren Titel plus Breadcrumb;
- kein generischer Introtext und kein „Mehr erfahren“ auf diesen Seiten;
- importierter Seiteninhalt selbst bleibt unverändert und wird nur einmal ausgegeben;
- ListingHive-Themefooter `.site-footer` wird im Hobby-Depot-Profil hart ausgeblendet;
- eigener Hobby-Depot-Footer bleibt sichtbar;
- Reihenfolge bleibt Rechtliches → Informationen → Anzeigenmarkt;
- Magazin wird dedupliziert;
- Anbieter wird aus Informationen herausgefiltert;
- Hobbyfinder bleibt vorerst separat.

Lokale QA 1.50.703:
- PHP-Lint: **135/135 PASS**;
- 11/11 Serviceseiten: genau 1 H1, Breadcrumb vorhanden, kein „Mehr erfahren“, kein Zusatz-Intro: **PASS**;
- Footer-Runtime: genau 1 eigener Footer, Reihenfolge PASS, Magazin 1×, Anbieter 0×, Hobbyfinder 1×: **PASS**;
- ListingHive-Struktur gegen echten Theme-Code geprüft: Themefooter ist `<footer class="site-footer">`; neue Ausblendung zielt exakt darauf;
- CSS-Selektormatch gegen ListingHive-Footerstruktur: native Footerbestandteile getroffen, eigener `.hd-footer-v150616` nicht getroffen;
- geänderte Dateien gegenüber 1.50.702: genau 3 (Hauptdatei Versionswert, aktuelle Hobby-Depot-Klasse, Evidence-Datei);
- ZIP-Integrität: **PASS**.

ARTEFAKT:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.703_SERVICE_TITLE_NATIVE_FOOTER_FIX_LOCALPASS.zip

SHA-256:
74cb488a891dab9bfff237c3820c05a2cf3dd3651f52a5335e2af671b33ce228

GRÖSSE:
58,673,853 Bytes.
## ERSTER OFFENER BLOCKER

Echter WordPress-/Frontend-Readback des 1.50.703-Stands. Kein Live-PASS aus lokaler QA ableiten.

## EXAKT EINE NEXT ACTION

**Nur 1.50.703 über 1.50.702 installieren und Frontend neu laden. Keinen erneuten Footer-Import starten. Prüfen: Seitentitel auf Impressum/Preise/AGB usw. wieder sichtbar; kein „Mehr erfahren“/Doppelinhalt; nur ein Footer; Reihenfolge Rechtliches → Informationen → Anzeigenmarkt; Magazin einmal; Anbieter weg; Hobbyfinder separat.**

## ARBEITSBINDUNG

- 1.50.694 = redaktionelle Detailtext-Benchmark.
- 1.50.696 = bestätigte Hub2-Grafikbenchmark.
- 1.50.698 = bestätigter lokaler Hub2-Textstand, in 1.50.699 unverändert.
- 1.50.699 = letzte funktionierende Basis vor Footer-Arbeit.
- 1.50.700 = **verworfen** wegen Runtime-Klassen-/Template-Mismatch.
- 1.50.701 = Runtime-Hotfix, ersetzt durch 1.50.702.
- 1.50.702 = ersetzt; entfernte Zusatz-Intros, aber auch Serviceseitentitel.
- 1.50.703 = aktueller Designstand; Serviceseitentitel zurück, kein Zusatz-Intro, ListingHive-Footer hart ausgeblendet.
- Keine neue Architektur.
- Keine Änderungen an Kategoriebaum, Affiliate-Slotarchitektur, Meta-/SEO-Titeln oder Bildern.
- Header-/Responsive-Navigation und Pferdeatelier-Footer sind separate nächste Designblöcke nach der Startseiten-Sichtprüfung.
