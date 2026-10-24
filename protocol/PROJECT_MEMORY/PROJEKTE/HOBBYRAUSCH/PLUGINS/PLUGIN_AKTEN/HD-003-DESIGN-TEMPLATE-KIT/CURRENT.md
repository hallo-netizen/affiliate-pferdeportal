# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.50.740 / EIGENES SERVICE-TEMPLATE / BODY + TABELLEN VOLLBREITE HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Aktuelles Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.740_SERVICE_TEMPLATE_BODY_TABLES_HARDPASS.zip`

SHA-256:
`133db11baf242e9f9a8d9cc17d8fe482bd13fb50af78c16dec49d67445de4825`

Pluginroot im Bundle:
`affiliate-portal-template-kit/`

## Aktueller Vertrag
- zentrale Hobby-Depot-Body-Achse max. 1200 px;
- Header und Footer behalten unverändert ihre bisherige 1440-px-Achse;
- Hobbymagazin „Wissen & Glossar“ verlinkt kanonisch auf `/magazin/wissen-glossar/`;
- Footer-Glossarlink verwendet ebenfalls die kanonische Route;
- keine sonstige Header-/Footer-Designänderung.

## QA
- Hobbymagazin-Toolkarte aus echtem Plugin gerendert: kanonischer Glossarlink PASS, alte `/glossar/`-Route dort nicht mehr vorhanden;
- 1200-px-Body-Regeln aus 1.50.730 weiterhin vorhanden;
- Header-/Footer-1440-Override weiterhin vorhanden;
- Gesamtbundle Fresh-Unpack und Source↔ZIP bytegleich;
- PHP im Gesamtbundle 22/22 PASS.

## EXAKT EINE NEXT ACTION
**Bundle serverseitig in die drei bestehenden kanonischen Pluginordner überschreiben; keine zusätzlichen Pluginordner anlegen.**


## 1.50.732 – Hobbyfinder + globale Hauptsuche
- Hobbyfinder: „Passende Themen“ war kein Finder-Ergebnis, sondern der allgemeine Magazin-Unterthemenblock.
- Auswahlquelle dieses Blocks: zuerst dem Hobbyfinder im zentralen Registry-Baum untergeordnete `journal_cat`-Knoten; Fallback `alleine`, `gruppe`, `zu-zweit`.
- Hobbyfinder-Reihenfolge jetzt: Hero/Intro → vorhandene `journal_banner`-Fläche → eigentlicher Finder → „Passende Themen“ als „Weiter entdecken“ unten.
- „Zur Startseite“ und „Neu starten“ im Finder unverändert.
- globale Header-Suche erhält eigenen AJAX-Transport ab 2 Zeichen, 180-ms-Debounce und AbortController.
- vier fachlich getrennte Ergebniswelten: HOBBYS | MAGAZIN | GLOSSAR | ANZEIGEN.
- HOBBYS: ausschließlich 862er Hobbyregister (inkl. Alias-Matching).
- MAGAZIN: ausschließlich veröffentlichte Posts mit `journal_cat`.
- GLOSSAR: ausschließlich veröffentlichte `hdg_term`.
- ANZEIGEN: ausschließlich `hp_listing_category` + veröffentlichte `hp_listing`.
- „Alle Suchergebnisse anzeigen“ führt auf eigene gruppierte Ergebnisseite mit denselben vier Bereichen.
- keine beliebigen WordPress-Seiten in der Vorschau.

## QA
- serverseitiger Positiv-/Negativtest aller vier Suchwelten PASS;
- normale beliebige WP-Seite als Negativfall ausgeschlossen PASS;
- Ajax-Client im Chromium mit simuliertem Fetch PASS;
- Responsive Ergebnislayer 1600 / 1024 / 760 / 390 px PASS;
- Hobbyfinder-Quellreihenfolge Banner → Finder → Unterthemen PASS;
- Fresh-Unpack Source↔ZIP bytegleich: 936 Dateien;
- PHP 11/11 PASS; ZIP CRC PASS.


## 1.50.733 – Hauptsuche bleibt vollständig im Browserfenster
- Live-Screenshot zeigte horizontales Abschneiden des vierteiligen Ajax-Ergebnislayers.
- Ursache: der breite Ergebnislayer war fest an der linken Kante des Suchformulars verankert.
- Korrektur: Ergebnislayer wird vor Anzeige und nach jeder Ajax-Antwort anhand des aktuellen Viewports neu positioniert und mit 16 px Sicherheitsrand eingeklemmt.
- Breite bleibt bis 1180 px erhalten; unter 760 px weiterhin 100 % des Suchformulars/einspaltig.
- Vier Suchwelten Hobbys / Magazin / Glossar / Anzeigen und deren Datenquellen unverändert.

## QA
- exakte Screenshot-Geometrie ca. 903 px Viewport / Suchformular links 267 px simuliert: Ergebnis 16–887 px, kein horizontaler Überlauf.
- Geometriesimulation zusätzlich 1648 / 1366 / 1024 / 761 px PASS.
- Positionierung läuft vor Loading-State, nach Ajax-Ergebnis und bei Resize.
- Fresh-Unpack: 936 Dateien Source↔ZIP bytegleich.
- PHP 11/11 PASS; ZIP CRC PASS.


## 1.50.734 – Suchergebnisseite für Enter/Teilbegriffe
- Live-Fehler: AJAX-Flyout fand z. B. für „Holz“ Treffer, Enter zeigte keine nutzbare Ergebnisseite.
- Exakte Ursache: `render_search_results_page_v150732()` liefert HTML als Rückgabewert; das Suchtemplate rief die Methode ohne `echo` auf.
- Korrektur: Suchtemplate gibt den Renderer tatsächlich aus.
- Zusätzlich wird die markierte Hobby-Depot-Hauptsuche anhand `hd_header_search=1` + `s` geroutet und hängt nicht mehr zwingend an WordPress/ListingHive-`is_search()`.
- Renderer liest den Suchbegriff primär direkt aus dem markierten GET-Request; `get_search_query()` bleibt Fallback.
- Dieselben vier Datenhelfer wie im Flyout bleiben maßgeblich: Hobbys | Magazin | Glossar | Anzeigen.
- Teilbegriff-Harness „Holz“ mit absichtlich `is_search()=false`: eigene Ergebnisseite PASS; Holzschnitzen/Holzwerken/Holzbrandmalerei PASS; irrelevantes Metallgießen ausgeschlossen.
- Ohne `hd_header_search` wird keine fremde Suche gekapert.
- Fresh-Unpack: 936 Dateien Source↔ZIP bytegleich.
- PHP 11/11 PASS; ZIP CRC PASS.


## 1.50.735 – Footer-/Service-Seiten
Betroffene Seitentypen:
- Impressum
- Disclaimer
- Datenschutz
- Werbebedingungen / Werb- & Anzeigebedingungen
- Werben / Werbung im Hobby Depot
- Preise
- Kontakt
- FAQ

Änderungen:
- ein einheitlicher Service-Hero für alle Seiten;
- dasselbe bereits vorhandene Asset `hero-masters-v150684/alltagsobjekte.webp` wird wiederverwendet;
- kein grüner Kicker „Hobby Depot“ mehr;
- kein Rahmen um den Seitentitel;
- altes Theme-/Astra-Titelduplikat wird auf diesen Seiten ausgeblendet;
- Preise: Tabellen und ihre Kubio-/Block-Wrapper werden auf volle Inhaltsbreite gesetzt;
- Preise: Tabellenzellen, Tabellenkopf und Abstände vereinheitlicht;
- Preise + Disclaimer: semantische Zwischenüberschriften und alleinstehende Fett-Zeilen erhalten klaren Absatz oberhalb/unterhalb;
- bestehende Inhalte bleiben unangetastet.

QA:
- alle Ziel-Slugs als Service-Seite erkannt;
- vorhandenes Hero-Asset: 1600×587 WebP, ca. 100 KB;
- PHP 11/11 PASS;
- CSS-Klammerprüfung PASS;
- ZIP CRC PASS;
- Fresh-Unpack Source↔ZIP bytegleich, 936 Dateien;
- lokaler Chromium-Harness konnte wegen Umgebungsblockade lokaler URLs nicht ausgeführt werden; deshalb bewusst LOCAL PASS, Live-Sichtprüfung offen.


## 1.50.736 – Service-Seiten Feinkorrektur
- Hero-Bild bleibt bestehen.
- Abstand Hero → erster Seiteninhalt zentral reduziert: 18 px Desktop, 16 px mobil.
- Gilt einheitlich für Impressum, Disclaimer, Datenschutz, Werbebedingungen, Werben, Preise, Kontakt und FAQ.
- Preise: drei Tabellen inklusive kompletter Kubio-Ahnenkette auf volle Inhaltsbreite gesetzt.
- Preise: Tabellen links bündig innerhalb der Inhaltsachse; Preis-Spalte bleibt nicht umbrechend.
- Preise: „Anzeigen in unserem Anzeigenmarkt“, „Redaktionelle Artikel & Advertorials“, „Exklusive Banner“ und alle „Kurzbedingungen“ als echte sichtbare Zwischenüberschriften mit Abstand oben/unten.
- Inline-Fettungen wie „Anzeige“, „Werbung“, „Advertorial“ bleiben unangetastet.
- Disclaimer: importierte `strong + br`-Zwischenüberschriften werden gezielt als Blocküberschriften formatiert; 9/9 erkannt.
- Test mit dem echten übernommenen Footer-/Kubio-Inhalt durchgeführt.
- Chromium-Fixture: Tabellen 3/3 volle Inhaltsbreite; Preis-Zwischenüberschriften 6 erkannt; Disclaimer-Zwischenüberschriften 9 erkannt.
- PHP 11/11 PASS; ZIP CRC PASS; Fresh-Unpack 936 Dateien bytegleich.


## 1.50.737 – Service-Body volle Breite
- Ursache aus Live-Screenshots: gerenderte Kubio-Zwischencontainer blieben schmal, weil 1.50.736 zu stark auf bestimmte Klassen zielte.
- Korrektur ohne Kubio-Klassennamen-Abhängigkeit: jede Containerkette, die echten Text/Überschriften/Listen/Tabellen trägt, wird bis zur `entry-content`-Achse auf 100 % aufgeweitet.
- gesamte Service-Seiten-Textachse entspricht damit exakt der Hero-/Body-Achse.
- Preise: alle drei Tabellen 100 % Inhaltsbreite, gleiche linke Kante wie Hero/Body.
- Zwischenüberschriften werden serverseitig markiert, nicht erst im Browser erraten.
- Preise: 6 relevante Zwischenüberschriften, jeweils 30 px Abstand oben / 18 px unten.
- Disclaimer: 9/9 Fett-Zwischenüberschriften, jeweils 30 px oben / 18 px unten.
- bestehendes Hero-Bild bleibt unverändert.
- sichtbarer Chromium-Test mit echtem importiertem Preise-/Disclaimer-Inhalt und absichtlich künstlich auf 68/76/82 % verschachtelten Containern: alle Wrapper, Tabellen und Überschriften auf volle 1200-px-Achse gezogen, PASS.
- PHP 11/11 PASS; ZIP CRC PASS; Fresh-Unpack 936 Dateien bytegleich.


## 1.50.738 – Ursache 1.50.736/737 korrigiert
- Live-Beobachtung: Breite/Abstände blieben trotz statischer PASS-Tests praktisch unverändert.
- Ursache: Kubio baut bzw. verändert die finalen Inhaltscontainer nach dem ersten Footer-/CSS-Pass; die bisherigen Fixes liefen zu früh.
- 1.50.738 misst deshalb nach dem tatsächlichen Kubio-Render gegen den realen Service-Hero und wiederholt die Normalisierung kurzzeitig nach DOM-Änderungen / Load / Resize.
- keine Kubio-Klassennamen als Voraussetzung.
- Preise: 3/3 Tabellen werden nachträglich auf exakt dieselbe x-/Breitenachse wie der Hero gesetzt.
- Preise: 6/6 definierte Fett-Zwischenüberschriften werden am gerenderten DOM erkannt, Blockdarstellung + 30 px oben / 18 px unten.
- Disclaimer: 9/9 definierte Fett-Zwischenüberschriften analog.
- Nachfolgendes <br> nach diesen Überschriften wird entfernt, damit der Abstand ausschließlich kontrolliert ist.
- Test mit echtem importiertem Preise-/Disclaimer-Inhalt; Inhalt absichtlich erst 420 ms später in 68/76/82-%-schmale verschachtelte Container eingesetzt.
- Ergebnis nach Runtime: Hero, Site, Outer, Mid, Inner und Tabellen jeweils exakt gleiche x-/Breitenwerte.
- Derselbe Test erneut auf Fresh-Unpack des finalen ZIP: PASS.
- PHP 11/11 PASS; ZIP CRC PASS; 936 Dateien Source↔ZIP bytegleich.


## 1.50.739 – Korrektur der falschen Kubio-Runtime-Annahme
- Im Hobby Depot ist Kubio nicht installiert.
- Die Seiten wurden lediglich aus einer früher mit Kubio erstellten Quelle importiert.
- Deshalb wurde die in 1.50.738 eingeführte Runtime-/MutationObserver-Nachbehandlung vollständig entfernt.
- Die importierten Altstrukturen werden jetzt direkt serverseitig im WordPress-Inhaltsrendern normalisiert.
- Kubio-Blockkommentare werden entfernt.
- Disclaimer: 9/9 bekannte Fett-Zwischenüberschriften werden in echte Blocküberschriften überführt.
- Preise: 6/6 relevante Zwischenüberschriften werden statisch markiert; 3/3 Tabellen erhalten eindeutige Klassen.
- Service-Body, Entry-Content und Tabellen werden zentral auf dieselbe 1200-px-Achse wie der Hero gesetzt.
- Kein Runtime-JS für diese Service-Seiten; kein MutationObserver; keine Timer.
- Browser-Simulation mit absichtlich schmalen Theme-Regeln:
  - Hero / Body / Entry jeweils 1200 px und gleiche x-Kante;
  - Preise 3/3 Tabellen 1200 px;
  - 6 Preis-Zwischenüberschriften 30 px oben / 18 px unten;
  - 9 Disclaimer-Zwischenüberschriften 30 px oben / 18 px unten.
- PHP 11/11 PASS; ZIP CRC PASS; Fresh-Unpack 936/936 Dateien bytegleich.


## 1.50.740 – Service-Seiten aus Theme-/Import-Huelle geloest
- Live zeigte nach 1.50.739 weiterhin schmale Text-/Tabellenachsen.
- Ursache: die Server-Normalisierung kam an, aber die Seiten liefen weiterhin durch das normale Theme-Seitentemplate und damit durch dessen schmale Inhaltsachse.
- Korrektur: eigene schlanke Plugin-Vorlage `templates/hobby-depot-service-v150740.php` fuer alle Service-/Footer-Seiten.
- Hero und Service-Body verwenden exakt dieselbe Formel/Aussenachse.
- Zwischenueberschriften werden nicht mehr als h2/h3 erzeugt, sondern als normale Textabsätze mit `strong`: gleiche Schriftgroesse wie Fliesstext, nur fett.
- Preise: 3/3 Tabellen erhalten volle Service-Body-Breite bereits direkt im gerenderten HTML plus CSS.
- Tabellen linksbuendig; keine Theme-/Import-Huelle kann die Breite mehr reduzieren.
- Frisch entpacktes finales ZIP mit echtem importiertem Preise-/Disclaimer-Inhalt geprueft.
- Geometrie Preise bei 1600: Hero/Main/3 Tabellen jeweils x=200, Breite=1200.
- Geometrie bei 1100: jeweils x=36, Breite=1028.
- Geometrie bei 760: jeweils x=12, Breite=736.
- Geometrie bei 390: jeweils x=12, Breite=366.
- Zwischenueberschriften Preise 6/6 und Disclaimer 9/9: 15.5 px = Fliesstext, Gewicht 700, 30 px oben / 18 px unten.
- keine h2/h3-Umwandlung im normalisierten Service-Inhalt.
- PHP 12/12 PASS; ZIP CRC PASS; Fresh-Unpack 937/937 Dateien bytegleich.
