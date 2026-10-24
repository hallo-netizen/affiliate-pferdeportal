# HOBBYRAUSCH – GLOSSAR – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.0.23 / GLOSSAR-STARTLINK HOVER HARD PASS / 308 BEGRIFFE / LIVE OFFEN**

Das Hobby-Depot-Glossar wird als echtes Fachwörterbuch geführt und darf keine Hobby-, Kategorie- oder Ratgeberintents duplizieren.

Der bestehende Editorial-Einstieg **„Wissen & Glossar“** bleibt die zentrale Glossar-Hauptseite.

## SEO-Owner-Regel – verbindlich

Grundsatz aus dem geprüften Pferde-Atelier-Modell:

**Pro primärem Suchintent genau ein SEO-Owner.**

Vor einer Glossar-Einzelseite wird deshalb immer entschieden:

1. **Begriffserklärung ist die eigentliche Suchabsicht**  
   → Glossar darf SEO-Owner sein und eine eigene Glossarseite erhalten.

2. **Der Begriff ist eigentlich ein Hobby, größeres Thema, Ratgeber, How-to, Kauf-/Vergleichsthema oder Kategorie**  
   → Hobby-Porträt, Beitrag oder Kategorie ist SEO-Owner.  
   → Keine zweite indexierbare Glossarseite.

3. **Noch unklar**  
   → Kandidat bleibt zurückgestellt; keine indexierbare Einzelseite bis zur Klärung.

Synonyme und Schreibvarianten bleiben Aliase und erzeugen niemals zweite Seiten.

## Zusammenspiel mit DataForSEO und späterer SEO-Maschine

DataForSEO ist **Prüfhilfe, nicht Strukturautorität**.

Es wird bei unklaren Begriffen genutzt, um die Suchabsicht zu unterscheiden:
- überwiegend Definition / „was ist …“ → Glossar-Kandidat;
- überwiegend Anleitung, Einstieg, Vergleich, Kauf, Nutzung oder eigenständiges Hobby → Beitrag/Hobby/Kategorie;
- gemischte oder unklare Absicht → zurückstellen statt doppeln.

Ein bereits vergebener SEO-Owner muss später von der SEO-/Textmaschine respektiert werden:
- Glossar-Owner blockiert einen zweiten Grundartikel zum identischen Intent;
- Artikel-/Hobby-/Kategorie-Owner blockiert eine zweite indexierbare Glossarseite;
- eigenständige Longtails mit anderer Suchabsicht bleiben erlaubt.

Es wird **keine zweite Datenbank** gebaut. Diese Owner-Entscheidung gehört in den bestehenden zentralen Begriffs-/Intentbestand.

## Glossar-Hauptseite – verbindliches Pferdeatelier-Konzept

Die Struktur wird funktional **eins zu eins vom Pferdeatelier** übernommen; nur Farben, Begriffe und Hobbywelten werden später an Hobby Depot angepasst.

Reihenfolge:
1. Breadcrumb mit **Startseite → Magazin → Wissen & Glossar**;
2. Hero mit Glossar-H1, kurzer Unterzeile und thematischem Bild;
3. **eigene Glossar-Suche**, die ausschließlich Glossarbegriffe durchsucht;
4. A–Z-Leiste;
5. Themenfilter über die acht Hobbywelten **Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln**;
6. breite **Banner-/Anzeigenfläche**;
7. Überschrift **Alle Glossarbegriffe**;
8. Begriffskarten;
9. Pagination oben und unten am Begriffsblock.

Pferdeatelier-Referenz frisch geprüft:
- 16 Begriffe je Seite;
- Desktop 4 Spalten × 4 Reihen;
- jede Karte: Begriff + Kurzdefinition + „Zum Begriff“;
- Pagination statt endloser langer Seite.

Für Hobby Depot gilt deshalb ebenfalls verbindlich: **16 Begriffe pro Seite**.

Suche, Buchstabenfilter, Themenfilter und Pagination erzeugen keine eigenen konkurrierenden SEO-Owner.

## Einzelseite – verbindliches Pferdeatelier-Konzept

Reihenfolge / Aufbau:

- Breadcrumb beginnt immer mit **Startseite** und führt über Magazin/Glossar/Hobbywelt zum Begriff;
- kleine Rubrik **WISSEN**;
- H1 = Begriff;
- direkt darunter farblich abgesetzter **„Kurz erklärt“**-Kasten mit einer knappen Definition;
- darunter der eigentliche Fachtext mit 150–200 Wörtern;
- **Übergangsregel:** Der erste Satz des Fachtexts darf die Kurzdefinition weder wörtlich noch sinngleich wiederholen. Er muss stattdessen fließend weiterführen, z. B. mit Anwendung, Kontext, typischer Situation oder Abgrenzung;
- **0 Links im Fließtext**.

Rechte Spalte, feste Reihenfolge:
1. **Hobbywelt** – verlinkt zur passenden Hobbywelt/Hauptkategorie;
2. **Verwandte Begriffe** – nur echte vorhandene Glossarbegriffe verlinken;
3. **Anzeige** – reservierte Banner-/Werbefläche;
4. **Mehr zum Thema** – Link auf eine passende starke Hauptkategorie/Hauptseite.

Hobby-Depot-Zusatzentscheidung:
- **„Mehr zum Thema“ ist Pflicht.**
- Ein Glossarbegriff darf deshalb erst live gehen, wenn eine echte passende Hauptkategorie/Hauptseite zugeordnet ist.
- keine erfundenen oder schwachen Ersatzlinks.

Nicht öffentlich:
- Quellen;
- Synonyme/Aliase;
- interne Prüfmetadaten.

Quellen bleiben intern am Datensatz gebunden.

## Produktionsweg

`Begriffspool → Intent-/Dublettenprüfung → bei Bedarf DataForSEO → SEO-Owner festlegen → Recherche + Text → Validator → WordPress-Draft → Readback → Freigabe`

Batch:
maximal 25 Begriffe.

## Installationskandidat

Technische Basis:
**Hobby Depot Glossar Core 1.0.1**

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.1_INSTALLIEREN.zip`

SHA-256:
`b686655bc2571548248fe278c4a74e7db927503f92900c9a661d173b6d04329a`

Persistente Arbeitskopie:
`/Hobby Depot/Glossar/HOBBY_DEPOT_GLOSSAR_CORE_1.0.1_INSTALLIEREN.zip`

1.0.1 ist technisch lokal geprüft, enthält aber noch nicht den heute festgelegten finalen Hobby-Depot-Designvertrag aus Sicherheit.

## Lokale QA 1.0.2

- PHP-Lint: **7/7 PASS**;\n- Design-Prinzip Sicherheit → Hobby Depot: **umgesetzt**;\n- 9 Karten je Seite + 3/2/1-Spalten: **umgesetzt**;
- ZIP-Integrität: **PASS**;
- WordPress-Paketstruktur: **PASS**;
- WordPress-Scheduler/Cron-Produktion: **0**;
- Filtervarianten noindex + Canonical zur Hauptseite;
- Taxonomie nicht öffentlich/indexierbar;
- Draft-Batchvertrag vorhanden.

## ROUTENFIX 1.0.6 – REPRODUZIERT + HARD PASS

Kanonische URL:
`/magazin/wissen-glossar/`

Der echte Konflikt mit dem aktuellen Hobby-Depot-Design 1.50.705 wurde lokal reproduziert:
- Glossar 1.0.5 wählte zuerst das Glossar-Template;
- das Designplugin übernahm danach mit `template_include` Priorität 99999;
- Ergebnis: `hobby-depot-front-v150699.php` = Startseite.

1.0.6 bedient deshalb ausschließlich die exakte Glossar-Route bereits in `template_redirect`, also vor dem Design-Template-Router.

Lokale HTTP-Integrationssimulation mit den echten beiden Plugin-Codebasen:
- `/magazin/wissen-glossar/` → 200, Glossar JA, Startseite NEIN: PASS
- ohne Schluss-Slash → Glossar JA: PASS
- mit Such-Query → Glossar JA: PASS
- doppelter Pfad → Glossar NEIN: PASS
- alte `/glossar/`-Route → Glossar NEIN: PASS
- Startseite `/` → Startseite JA, Glossar NEIN: PASS
- PHP 8/8 Syntax PASS
- ZIP-Integrität PASS

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.6_ROUTE_CONFLICT_HARDPASS_INSTALLIEREN.zip`

SHA-256:
`be9f98f4dabd2728985f7252a77c5e617038cf3905914df597742eeb80e60e3f`

Wichtig: Das ist ein lokaler Integrations-Hard-Pass, noch kein Live-Pass.


## 20.10.2026 – Pferdeatelier-Glossarlogik verbindlich übernommen

Frisch geprüft gegen Pferde-Atelier Glossar-Current/Struktur/Manager:
- Fachtext: **0 Bodylinks**;
- rechte Spalte: **Hobbywelt → Verwandte Begriffe → optional Mehr zum Thema**;
- Mehr zum Thema zeigt genau ein starkes vorhandenes Hauptziel (Seite/Kategorie), sonst nichts;
- Quellen bleiben als Recherche-/Prüfmetadaten gespeichert, werden **nicht öffentlich gerendert**;
- Synonyme bleiben Metadaten/Aliase und werden **nicht als eigener Frontendblock** ausgegeben;
- keine erfundenen Related-/Ziel-URLs.

Lokaler Kandidat 1.0.7 baut ausschließlich auf dem live gerouteten 1.0.6 auf und ändert diese Inhalts-/Linklogik, **kein Design**.

Artefakt: `HOBBY_DEPOT_GLOSSAR_CORE_1.0.7_PFERDEATELIER_LOGIK_LOCALPASS.zip`
SHA-256: `f900ded62a5ea7b6a77a2e8814fc791a34eab0598f8c1c66c4bae1f48a9f30a9`

Lokale Prüfung:
- PHP 8/8 Syntax PASS;
- ZIP-Integrität PASS;
- gerenderte Test-Einzelseite: Hobbywelt PASS;
- zwei reale Related-Linkplätze PASS;
- optionaler Hauptziel-Link PASS;
- Quellen im Frontend 0 PASS;
- Synonymblock im Frontend 0 PASS;
- Bodylink im Fachtext 0 PASS.

**Keine Installation jetzt erforderlich.** 1.0.7 bleibt vorbereiteter Kandidat und soll mit der späteren Designänderung gebündelt werden.

## 21.10.2026 – Glossar-Design 1.0.8

Pferdeatelier-Konzept und -Darstellung wurden funktional übernommen; angepasst wurden ausschließlich Hobby-Depot-Farben, Hobbywelt-Icons und Hobby-Inhalte.

Hauptseite:
- Breadcrumb Startseite → Magazin → Wissen & Glossar;
- Hero;
- reine Glossar-Suche;
- A–Z;
- 8 Hobbywelt-Filter;
- Bannerfläche;
- 16 Begriffe je Seite = 4 × 4 Desktop;
- Pagination;
- Begriffskarte: Titel, Kurzdefinition, „Zum Begriff“.

Einzelseite:
- Breadcrumb Startseite → Magazin → Wissen & Glossar → Hobbywelt → Begriff;
- WISSEN-Kicker + H1;
- „Kurz erklärt“-Kasten;
- 150–200 Wörter Fachtext;
- 0 Bodylinks;
- rechts: Hobbywelt → Verwandte Begriffe → Anzeige → Mehr zum Thema;
- Quellen/Synonyme nicht öffentlich.

Zusätzlich:
- Hauptziel ist im Batch nun Pflicht;
- bestehender, live bestätigter 1.0.6-Routenfix unverändert übernommen.

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.8_PFERDEATELIER_DESIGN_LOCALPASS.zip`

SHA-256:
`ec8b590e00c4d05f5189908cdd8316f22115ecca652026349edbe7e661b1ccd2`

Lokale QA:
- PHP 8/8 PASS;
- ZIP-Integrität PASS;
- 16 Karten/Pagination PASS;
- 8 Hobbywelt-Filter PASS;
- Hero/Suche/A–Z/Banner PASS;
- Breadcrumb Hauptseite PASS;
- Breadcrumb Einzelseite PASS;
- Kurzdefinition PASS;
- Hobbywelt/Related/Anzeige/Mehr zum Thema PASS;
- Bodylinks entfernt PASS;
- Quellen/Synonyme Frontend 0 PASS;
- Core-Routendatei byteidentisch zu 1.0.7;
- serve_index_route / 404-Handler / Template-Router unverändert zu 1.0.7.

## 21.10.2026 – 1.0.9 Pferdeatelier-Designkorrektur

Nutzer-Livevergleich gegen Pferdeatelier zeigte Abweichungen in 1.0.8. Korrigiert:

- CSS-Variablen gelten jetzt auch auf der Begriffseite; dadurch sind „Kurz erklärt“ und rechte Infokarten tatsächlich farbig hinterlegt;
- H1 auf Begriffsebene deutlich größer wie in der Pferdeatelier-Referenz;
- Breadcrumbs größer und wie in der Referenz eingerückt;
- Hobbywelt im Breadcrumb und in der rechten Spalte führt jetzt **zur Glossar-Filterung derselben Hobbywelt**, nicht aus dem Glossar in die Hauptkategorie;
- „Mehr zum Thema“ nutzt weiterhin den expliziten Primärlink; fehlt er, wird nur eine tatsächlich vorhandene Hauptseite/Kategorie derselben Hobbywelt als Fallback verwendet;
- Suche-Button wird hart in Hobby-Depot-Grün/Dunkelgrün gerendert; kein gelber Theme-Override mehr;
- Begriffseite erhält unten Vorheriger-/Nächster-Begriff-Navigation;
- neues Glossar-Hero-Bild eingebaut;
- 16 Begriffe pro Seite unverändert;
- bestehende Route/Core-Datei byteidentisch zu 1.0.8.

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.9_PFERDEATELIER_1ZU1_DESIGN_HARDPASS.zip`

SHA-256:
`73684a4de1de84ca5a09e75bde84ac760abe02c669502fffd027128583d83840`

Lokale Prüfung:
- PHP komplett PASS;
- ZIP-Integrität PASS;
- Index: Hero/Suche/8 Welten/Banner/16 Karten/Pagination PASS;
- Single: Breadcrumb/Kurzdefinition/Hobbywelt/Related/Anzeige/Mehr zum Thema PASS;
- Breadcrumb-Hobbywelt bleibt innerhalb des Glossars PASS;
- Fallback „Mehr zum Thema“ auf echte Hauptwelt-Seite/Kategorie PASS;
- Bodylinks 0 PASS;
- Quellen/Synonyme Frontend 0 PASS;
- Vorheriger/Nächster Begriff PASS;
- Single-CSS-Variablen vorhanden PASS;
- Suchbutton nicht gelb PASS;
- Hero 1432×526 PASS.

## 21.10.2026 – 1.0.10 Korrektur nach Livevergleich

1.0.9 war gestalterisch noch zu stark am Pferdeatelier und die Breadcrumb-Positionen waren falsch.

Korrigiert:
- Breadcrumbs Hauptseite und Begriffseite separat auf Pferdeatelier-Positionierung kalibriert;
- Breadcrumb-Schrift größer;
- komplette Pferdeatelier-Oliv-/Gold-Farbwelt entfernt;
- komplette Glossar-Typografie auf Hobby-Depot-Inter/Sans umgestellt;
- Hobby-Depot-Palette: Dunkelpetrol #17313c, Petrol #0f8f95, Tiefpetrol #0a777c, helle Mintflächen #eef8f7;
- „Kurz erklärt“ und rechte Infokarten mint/grün hinterlegt mit Petrol-Linie;
- Suchbutton Petrol statt Pferdeatelier-Farbe;
- aktive Pagination Petrol statt Gold;
- Begriffsnavigation unten neu: bei nur einem Nachbarn volle Breite ohne leere zweite Karte;
- verwandte Draft-Begriffe werden für angemeldete Redakteure als Preview-Links sichtbar;
- bestehender 1.0.6-Routen-Core unverändert.

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.10_HOBBYDEPOT_FARBEN_BREADCRUMBS_HARDPASS.zip`

SHA-256:
`930ad0e38094b3c4c88f70856a96be31accbecf798551df0701306e8453e2de4`

Lokale Hard-QA:
- kompletter PHP-Lint PASS;
- ZIP CRC PASS;
- 27 Render-/Strukturprüfungen PASS;
- Pferdeatelier-Olive/Gold/Georgia im Plugin: 0 Treffer;
- Breadcrumb Hauptseite 78px Innenversatz, 13px;
- Breadcrumb Begriffseite 60px Innenversatz, 13px;
- H1 Inter 50px / Hobby-Depot-Dunkelpetrol;
- Kurz-erklärt Hintergrund #eef8f7, Linie #0f8f95;
- rechte Karten Hintergrund #eef8f7;
- Suche-Button #0f8f95;
- Einzel-Nachbar-Navigation volle Breite;
- Playwright-DOM/Computed-Style-Readback PASS;
- Core-Datei SHA identisch zu 1.0.9.

## 21.10.2026 – 1.0.11 Breadcrumb/Nav/Related-Korrektur

Nach Nutzer-Livevergleich wurden ausschließlich drei Punkte korrigiert:

1. **Breadcrumbs**
- nicht mehr nach Pferdeatelier gestaltet;
- exakt die native Hobby-Depot-Struktur und -Klassen `.hd-breadcrumb-wrap` / `.hd-breadcrumb`;
- CSS-Regeln für Breite, Top-Abstand, Schriftgröße, Gap, Farben und Current-State textidentisch zum aktuellen Hobby-Depot-Designquellstand;
- Hauptseite und Begriffseite außerhalb des Glossar-Inhaltscontainers gerendert, dadurch dieselbe Portalachse wie normale Hobby-Depot-Seiten.

2. **Weiterwissen im Glossar**
- keine Karten mehr;
- nach Pferdeatelier-Konzept: „Weiterwissen im Glossar“ + „Zur Glossar-Startseite“;
- darunter Zurück links / Weiter rechts;
- über die volle Artikelbreite **unterhalb von Text und Sidebar**, nicht nur in der linken Textspalte.

3. **Verwandte Begriffe**
- vorhandene Begriffe werden verlinkt;
- noch nicht vorhandene verwandte Begriffe bleiben sichtbar, aber unverlinkt;
- für zukünftige Batches können zusätzlich exakte `related_terms`-Anzeigenamen gespeichert werden;
- Test: Kallus → „Veredelung“ sichtbar unverlinkt PASS.

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.11_BREADCRUMB_NAV_RELATED_HARDPASS.zip`

SHA-256:
`701741c8ee2c542c806b897836c84fb3590d5f0ff473c614330c730999b76e1e`

Hard-QA:
- 26 Render-/Strukturchecks PASS;
- kompletter PHP-Lint PASS;
- ZIP-Integrität PASS;
- Breadcrumb-Regeln textidentisch zum Hobby-Depot-Design PASS;
- Browser/DOM 1440 px: Breadcrumb x=130 Breite=1180; Glossar-Hauptachse x=130 Breite=1180 PASS;
- „Verwandte Begriffe / Veredelung“ sichtbar PASS;
- untere Glossarnavigation x=130 Breite=1180 PASS;
- `class-hdg-core.php` SHA identisch zu 1.0.10, Route unverändert PASS.

## 21.10.2026 – 1.0.12 echte native Hobby-Depot-Breadcrumbs

Ursache der vorherigen Fehlversuche:
Die Glossar-Versionen kopierten zwar Breadcrumb-CSS, liefen aber weiterhin in einem **anderen Seitenshell/Theme-Wrapper** als normale Hobby-Depot-Seiten. Dadurch konnte die Position trotz gleicher CSS-Werte sichtbar abweichen.

1.0.12 ändert deshalb die Architektur an dieser Stelle minimal und eindeutig:
- Glossar nutzt jetzt denselben aktiven Hobby-Depot-Header-Renderer wie normale Hobby-Depot-Seiten;
- denselben Footer-Renderer;
- denselben äußeren Content-Wrapper `.hd-content-v150616`;
- Breadcrumb ist wie bei nativen Hobby-Depot-Seiten **das erste Element in diesem Wrapper**;
- das Glossar-Plugin enthält **0 eigene CSS-Regeln für `.hd-breadcrumb` / `.hd-breadcrumb-wrap`**;
- Position, Breite, Schrift, Abstand und Farben kommen damit ausschließlich aus dem aktuellen Hobby-Depot-Designplugin;
- Index und Begriffseite verwenden denselben nativen Shellweg;
- Routen-Core bleibt byteidentisch zu 1.0.11;
- Related-Begriffe und untere Glossarnavigation bleiben erhalten.

Beweis gegen aktuellen Designstand 1.50.705 / Profil V150699:
- natives Design verwendet `.hd-content-v150616` und rendert dort als erstes `render_breadcrumb()`;
- 1.0.12 verwendet exakt denselben Wrapper und rendert dort als erstes die Glossar-Breadcrumb;
- natives Breadcrumb-CSS gefunden: Breite `min(calc(100% - 72px), var(--hd-content))`, Margin `18px auto 0`, Schrift `12px`;
- Plugin-eigene Breadcrumb-CSS-Treffer: **0**;
- aktiver Design-Header/Footer werden direkt wiederverwendet;
- PHP-Lint aller 8 PHP-Dateien PASS;
- ZIP-Integrität PASS;
- Core-Routendatei byteidentisch zu 1.0.11 PASS;
- Related sichtbar/unverlinkt falls Ziel noch fehlt PASS;
- untere Glossarnavigation vorhanden PASS.

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.12_NATIVE_BREADCRUMB_HARDPASS.zip`

SHA-256:
`3e464dbd858cb723a85d9ffa9b4c1e8f92abaaa0a3f4423dd36a72526653d536`

## 21.10.2026 – 1.0.13 Layout-/Typokorrektur

Kritische Prüfung gegen den echten Hobby-Depot-Designstand 1.50.705:

- native Hobby-Depot-Inhaltsbreite ist bis **1440 px** (`--hd-content:1440px`);
- Glossar 1.0.12 war auf **1180 px** begrenzt und deshalb sichtbar schmaler als normale Kategorie-/Hubseiten;
- Glossar-Hauptseite nutzt ab 1.0.13 exakt die native Inhaltsbreite `min(calc(100% - 72px), var(--hd-content))`;
- Begriffseite wird bewusst nicht auf volle 1440 px gezogen: Desktop-Lesebreite max. **1240 px**, bei 1024 px Viewport aber exakt dieselbe 952-px-Achse wie die native Seite. Damit keine überlangen Textzeilen auf großen Monitoren;
- Abstand Breadcrumb → Glossar-Inhalt: Übersicht **14 px**, Begriffseite **16 px**;
- „Kurz erklärt“-Kasten: zusätzlich **3 px linke Petrol-Linie**;
- Kurzdefinition **16 px**, Bodytext **16 px**, Sidebar-Links **12.5 px**; Inter bleibt einheitliche Schriftfamilie;
- mobile Inhaltsbreite an native 24-px-Ränder angepasst;
- Breadcrumb-Code/Route/Related/Nav unverändert.

Browser-Computed-Style-Hardpass:
- 1600 px Viewport: Glossar-Übersicht 1440 px breit; Begriffseite 1240 px;
- 1024 px Viewport: Übersicht 952 px, Begriffseite 952 px;
- Begriffseite Breadcrumb-Abstand 16 px;
- linke Kurz-erklärt-Linie 3 px, rgb(15,143,149);
- Kurzdefinition 16 px; Body 16 px; Sidebarlink 12.5 px.

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.13_LAYOUT_TYPO_HARDPASS.zip`

SHA-256:
`fbc4607cd2e7d1bdf0fd4c63619db3cf51366ed27b239685e4411cf8aea53221`

PHP-Lint PASS; Render-/Strukturtests PASS; ZIP-Integrität PASS.

## 23.10.2026 – 1.0.14 Produktionsbestand 100 Begriffe

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.14_100_BEGRIFFE_PRODUKTION_HARDPASS.zip`

SHA-256:
`4b998db76541e4654c0ec227b9efb9a28acfb231c8fe769cf4518f94a48eba39`

Inhalt:
- 100 geprüfte Glossarbegriffe in 4 Batches à 25;
- alle Fachtexte 150–173 Wörter;
- 0 Bodylinks;
- eindeutige term-IDs und Slugs;
- Quellen, SEO-Daten, Hobbywelt, Related-Begriffe und echte Hauptziele vorhanden;
- die sechs Pilotbegriffe wurden inhaltlich korrigiert;
- neue Validatorregel blockiert zu starke Wiederholung von Kurzdefinition im ersten Fließtextsatz;
- Produktionsbestand wird beim ersten Admin-Aufruf nach Update einmalig und idempotent als Entwürfe angelegt/aktualisiert;
- kein Auto-Publish;
- Layout, Frontend, Templates, Route und Hero gegenüber 1.0.13 unverändert.

Lokale QA:
- PHP-Lint 8/8 PASS;
- 100/100 Inhaltsvalidator PASS;
- Wortbereich 150–173 PASS;
- Übergangsregel 100/100 PASS;
- alter Problemsatz-Test blockiert 5/6 alte Wiederholungen wie erwartet;
- ZIP-Integrität PASS;
- exakt ein Plugin-Root `hobby-depot-glossar/`.

## 23.10.2026 – 1.0.15 Importfix

1.0.14 hatte einen realen Fehler im automatischen Produktionsimport: Ein einzelner vorhandener/abweichender Pilotbegriff beziehungsweise Slug-Konflikt konnte die gesamte 100er-Übernahme lautlos abbrechen.

1.0.15:
- vorhandene passende Pilotbegriffe werden über term-ID oder Slug übernommen und aktualisiert;
- der eingebaute Import prüft danach explizit 100/100 Begriffe;
- Teilstände werden beim nächsten Admin-Aufruf erneut versucht;
- Erfolg oder konkreter Importfehler wird im Backend angezeigt;
- Produktionsdaten, Layout, Route, Templates und Frontend bleiben gegenüber 1.0.14 unverändert.

Test:
- Simulationsfall 6 vorhandene Pilotbegriffe + Produktionsbestand: 6 adoptiert + 94 neu = 100/100 PASS;
- PHP-Lint komplett PASS;
- ZIP-Integrität PASS.

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.18_AJAX_FIX_200_BEGRIFFE_HARDPASS.zip`

SHA-256:
`1cd4a40ca9ed0783e5b90d29ea43d3d448577972fb74f4325d9f5927cd8f4fd4`

## ERSTER OFFENER BLOCKER

Echter WordPress-Readback nach Installation von 1.0.15: Backend muss 100 Glossarbegriffe als Entwürfe zeigen; angemeldete Redakteure sehen die Entwürfe auch auf der Glossarübersicht.

## EXAKT EINE NEXT ACTION

**1.0.15 über den bestehenden Ordner `hobby-depot-glossar` überschreiben und WordPress-Admin einmal neu laden.**


## 24.10.2026 – 1.0.16 Import-/Daten-Hardpass
- Ursache der 1.0.15-Liveblockade: lokale Vorprüfung hatte nicht exakt dieselbe Wortzählung wie HDG_Manager::validate_batch().
- 8 Fachtexte mit 148/149 Wörtern korrigiert: Serife, Schrötling, Trittfrequenz, Debouncing, Hot-Swap, Rektaszension, Münzzeichen, Fehlprägung.
- Direkter Aufruf der echten Plugin-Prüfroutine gegen alle vier eingebauten 25er-Batches: 4/4 PASS, 100/100 PASS.
- Finaler Wortbereich: 150–172 Wörter.
- Übergangsregel Kurzdefinition → erster Fließtextsatz: PASS; maximale Überschneidung 0,3333 unter Blockiergrenze 0,35.
- PHP-Lint komplett PASS; ZIP-Integrität PASS; exakt ein Root hobby-depot-glossar/.


## 24.10.2026 – 1.0.17 Produktionsbestand 150 Begriffe
- 50 neue Glossarbegriffe (101–150) in zwei weiteren 25er-Batches.
- Themen: Fotografie, Keramik, Holz, Pflanzen, Imkerei, Numismatik, Mikroskopie, Astronomie, Typografie, Elektronik.
- echte HDG_Manager::validate_batch()-Routine: 6/6 Batches PASS, 150/150 Begriffe PASS.
- globale Dublettenprüfung: 150 eindeutige external_id, 150 eindeutige Slugs.
- Fachtexte 150–172 Wörter; 0 Bodylinks; Quellen und Hauptziele vollständig.
- Update-Simulation mit bereits vorhandenen 100 Begriffen: 100 übernommen/aktualisiert + 50 ergänzt = 150/150 PASS.
- Layout, Route, Hero und Frontenddarstellung gegenüber 1.0.16 nicht umgebaut.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.18_AJAX_FIX_200_BEGRIFFE_HARDPASS.zip`
- SHA-256: `1cd4a40ca9ed0783e5b90d29ea43d3d448577972fb74f4325d9f5927cd8f4fd4`


## 24.10.2026 – 1.0.18 AJAX-Fix + 200 Begriffe
- Produktionsbestand auf 200 Begriffe erweitert, 8 Batches à 25.
- Ursache des WordPress-Fehlerwegs abgesichert: admin_init läuft auch bei admin-ajax.php; der gebündelte Import kehrt bei AJAX/Heartbeat und REST jetzt sofort zurück.
- Pro normalem Admin-Aufruf wird maximal ein 25er-Batch importiert.
- Simulation mit vorhandenem 150er-Stand: AJAX 150→150 PASS; normale Admin-Aufrufe 150→175→200 PASS.
- echte HDG_Manager::validate_batch()-Routine: 8/8 Batches PASS, 200/200 PASS.
- globale Dublettenprüfung: 200 eindeutige external_id, 200 eindeutige Slugs.
- Wortbereich 151–178 Wörter.
- PHP-Lint 8/8 PASS; ZIP-Integrität PASS; exakt ein Root `hobby-depot-glossar/`.
- Cyberduck-Vertrag: Ordner `hobby-depot-glossar` direkt über den bestehenden Pluginordner kopieren/ersetzen.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.18_AJAX_FIX_200_BEGRIFFE_HARDPASS.zip`
- SHA-256: `1cd4a40ca9ed0783e5b90d29ea43d3d448577972fb74f4325d9f5927cd8f4fd4`


## 24.10.2026 – 1.0.19
- 300 Glossarbegriffe, 12 Batches à 25.
- A–Z vollständig.
- Hobbywelten: Gestalten 47, Fertigen 45, Technik 38, Forschen 40, Pflanzen 35, Tiere 31, Bewegen 32, Sammeln 32.
- 12/12 Batches mit der echten HDG-Validierung PASS; 300 eindeutige IDs und Slugs.
- Fachtexte 150–177 Wörter.
- Update-Simulation 200→225→250→275→300 PASS; AJAX bleibt bei 200.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


## 24.10.2026 – 1.0.20 finaler Lückenschluss
- Endbestand: 308 Glossarbegriffe.
- Mindestabdeckung A–Z: mindestens 5 Begriffe je Buchstabe.
- Mindestabdeckung Hobbywelten: mindestens 30 Begriffe je Welt; kleinste Welt Tiere = 31.
- Ergänzt ausschließlich 8 Lückenbegriffe: Jute, Quadrant, Xenolith, Xylem, Yagi-Antenne, Yaw, Yarn Over, Yarn Weight.
- echte HDG_Manager::validate_batch()-Routine: 13/13 Batches PASS, 308/308 eindeutige IDs und Slugs.
- Fachtexte 151–178 Wörter.
- AJAX-Sperre bleibt aktiv; Update-Simulation 300→308 in einem normalen Admin-Aufruf PASS.
- PHP-Lint komplett PASS; ZIP-Integrität PASS; exakt ein Root `hobby-depot-glossar/`.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


## 24.10.2026 – 1.0.21 Glossar-Übersicht Design/Navigation
- Kachel-Kurzdefinition von 10.5 px auf 11.5 px erhöht.
- Link „Zum Begriff“ von 9.5 px auf 10.5 px erhöht.
- Begriffsanzahl auf der öffentlichen Glossarübersicht vollständig entfernt.
- Überschrift abhängig vom aktiven Zustand:
  - Start: „Alle Glossarbegriffe“
  - Hobbywelt: „Begriffe: <Hobbywelt>“
  - Buchstabe: „Begriffe mit <Buchstabe>“
  - Suche: „Suchergebnisse“
- Link „Zur Glossar-Startseite“ rechts in der Kopfzeile über den Kacheln.
- zweiter Link „Zur Glossar-Startseite“ im unteren Navigationsbereich neben/unter der Pagination.
- 308 Begriffe und Produktionsdaten unverändert; keine Inhaltsänderung.
- PHP-Lint 8/8 PASS; ZIP-Integrität PASS.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


## 24.10.2026 – 1.0.22 Design-Render-Hardpass
- 1.0.21 war nur auf Quellcode-Ebene geprüft; 1.0.22 wird zusätzlich als tatsächlich gerenderte Ausgabe geprüft.
- Vorschautext Kachel: 12.5 px, mit stärkerem Selektor/important gegen Theme-Überschreibung.
- Link „Zum Begriff“: 11.5 px, ebenfalls gehärtet.
- Start: „Alle Glossarbegriffe“.
- Themenfilter: „Begriffe zum Thema <Hobbywelt>“.
- Buchstabenfilter: „Begriffe mit <Buchstabe>“.
- Suche: „Suchergebnisse“.
- öffentliche Begriffsanzahl entfernt.
- „Zur Glossar-Startseite“ oben und unten.
- Glossarroute setzt DONOTCACHEPAGE + nocache_headers und trägt HDG_VERSION im HTML zur eindeutigen Deploy-Prüfung.
- Cyberduck-Paket: alle Dateien frisch datiert.
- Finales ZIP erneut entpackt und daraus gerendert: Start, Fertigen, J, Suche PASS.
- Datenbestand unverändert: 13 Batches, 308 Begriffe, 308 eindeutige IDs/Slugs.
- PHP-Lint 8/8 PASS; ZIP-Integrität PASS; Source/ZIP-Tree bytegleich.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`


## 24.10.2026 – 1.0.23 Hover Glossar-Startseite
- Alle Links „Zur Glossar-Startseite“ erhalten einen sichtbaren Hover-/Focus-Effekt.
- Effekt: Petrol-Farbwechsel, Unterstreichung nimmt Akzentfarbe an, leichte 2px-Bewegung nach rechts.
- Keine sonstige Layout- oder Inhaltsänderung.
- Gerenderte Ausgabe geprüft: oberer und unterer Startseiten-Link vorhanden; Hover-/Focus-Regeln greifen.
- PHP-Lint PASS; finales ZIP erneut entpackt und bytegleich gegen Quelldatei geprüft.
- Artefakt: `HOBBY_DEPOT_GLOSSAR_CYBERDUCK_1.0.23_HOVER_HARDPASS.zip`
- SHA-256: `ba95a5a2919ae4fce30a209c99dac0c3acda19128bd9fd5caf2ab46024931991`
