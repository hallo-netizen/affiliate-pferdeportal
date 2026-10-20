# HOBBYRAUSCH – GLOSSAR – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **CORE 1.0.4 ROUTENFIX LOCAL PASS / KANONISCHE URL FEST / LIVE OFFEN**ntscheidung

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

## Glossar-Hauptseite – Designvertrag aus Bürogebäude Sicherheit

Die bewährte Glossar-Darstellung aus **Sicherheit** wird für Hobby Depot übernommen und nur farblich/typografisch an Hobby Depot angepasst:

- zentrale Seite `/glossar/`;
- Suchfeld;
- A–Z-Navigation;
- Filter nach den acht Hobbywelten;
- kompakte Karten mit Icon, Begriff, Hobbywelt und kurzer Vorschau;
- Desktop 3 Karten pro Zeile, Tablet 2, Mobil 1;
- maximal 9 Karten je Ergebnisseite;
- Filter, Suche und Pagination erzeugen keine eigenen SEO-Zielseiten;
- keine Quellenzeilen oder langen Erklärblöcke auf den Karten;
- keine erfundenen Ziele;
- echte Glossar-Einzelseite nur wenn der SEO-Owner geklärt und der Begriff fachlich freigegeben ist.

Noch nicht freigegebene Kurzansichten dürfen keine indexierbare dünne Ersatzseite werden.

## Einzelseite – Inhaltsvertrag

Nur für echte Glossar-Owner:

- 150–200 Wörter;
- kurze Definition;
- fachliche Einordnung und klare Abgrenzung;
- genau eine Hobbywelt;
- verwandte Begriffe;
- Quellen;
- individueller SEO-Titel und Meta-Description;
- Prüfdatum und Prüfintervall 6/12/24 Monate;
- keine künstliche Artikellinkliste;
- optional genau ein starkes vorhandenes Hauptziel;
- kein Auto-Publish.

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

## ROUTENFIX 1.0.4

Kanonische Glossar-Hauptseite:
`/magazin/wissen-glossar/`

Die fehlerhafte 1.0.3-Logik mit eigener Root-Seite `/glossar/` ist entfernt. 1.0.4 bindet ausschließlich die bestehende Magazinstruktur. Fehlt die Unterseite, wird nur `wissen-glossar` als Kind der vorhandenen `magazin`-Seite angelegt. Keine zweite Glossar-Haupt-URL.

Begriff-URLs:
`/magazin/wissen-glossar/begriff/<slug>/`

Artefakt:
`HOBBY_DEPOT_GLOSSAR_CORE_1.0.4_KANONISCHE_URL_INSTALLIEREN.zip`

SHA-256:
`587b7be7813a2c136c2b32bc20699519bad9f01d41faf0b5ff064e4d03ea8c52`

PHP-Lint 7/7 PASS; ZIP-Integrität PASS.

## ERSTER OFFENER BLOCKER

Echter WordPress-Live-Readback der kanonischen URL nach Installation von 1.0.4.

## EXAKT EINE NEXT ACTION

**1.0.4 über die vorhandene Glossar-Version installieren und ausschließlich https://hobby-depot.de/magazin/wissen-glossar/ prüfen.**

Finales Hobby-Depot-Glossar-Design noch nicht auf Basis des bestätigten Sicherheit-Glossars umgesetzt.

## EXAKT EINE NEXT ACTION

**Glossar-Frontend von Hobby Depot auf das bewährte Sicherheit-Design angleichen, ohne Begriffe massenhaft zu produzieren; danach mit 1–2 echten Testbegriffen SEO-Owner-Regel, Textvertrag und Darstellung gemeinsam abnehmen.**
