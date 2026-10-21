# HOBBYRAUSCH – GLOSSAR – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-21
STATUS: **1.0.6 LIVE ROUTE PASS / PFERDEATELIER-KONZEPT VERBINDLICH ÜBERNOMMEN / DESIGN-UMSETZUNG SPÄTER**

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

## ERSTER OFFENER BLOCKER

Designumsetzung des jetzt verbindlich festgelegten Pferdeatelier-Glossarkonzepts im Hobby-Depot-Stil.

## EXAKT EINE NEXT ACTION

**Noch kein neues Plugin installieren. Als nächstes das Glossar-Design auf Basis dieses festgezogenen Konzepts bauen und erst danach Hauptseite + Einzelseite live abnehmen.**
