# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-10-03
STATUS: PSTE 0.57.26 LIVE / 0.57.27 PRODUKTWAHL-KANDIDAT LOKAL GEPRÜFT / 695ER VOLLEXPORT VORLIEGEND / EXAKTE TITELDEDUP 694

## EINE ZUSTÄNDIGE CURRENT-BINDUNG

- **PSTE-Themen-/SEO-Bestand:** diese Datei.
- **Artikelproduktion K9:** ausschließlich `konzept9/greenfield-20260929:CURRENT_STATE.json`.
- **Plugin-Inventar/Updatechronik:** `../PLUGINS/CURRENT_STATE.md`; keine zweite Fachwahrheit.
- **Aktiver Themenverwertungs-Zielvertrag:** `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/ZV-PSTE-THEMENVERWERTUNG-001.md`.

## AKTUELLER BELASTBARER LIVE-STAND

Realer WordPress-Readback vom 02.10.2026:
- Portal SEO Themenengine **0.57.26 aktiv**.
- Speicherpflege **COMPLETE**; sichtbarer Einsparwert **646,3 MB**.
- Bestandsaufbereitung/Titelbildung **COMPLETE**.
- **695 neue Titelkandidaten** aus gespeichertem Material.
- **8 zusätzlich PSERC-prüfbar**.
- **36 vollständig aufbereitet**.
- Provider-Abfragen: **0**.
- Completion: `EXISTING_TITLE_CANDIDATES_GENERATED_NO_PROVIDER_CALL`.

Der vollständige Live-Export liegt jetzt vor: `pste-global-seo-topic-map-20261003-194321-utc.json` aus PSTE 0.57.26. Exakt über `title_candidate_evidence.contract = PSTE_STORED_SOURCE_TITLE_CANDIDATE_V1` wurden **695 Titelkandidaten** extrahiert. Alle 695 besitzen einen nichtleeren `editorial_title`. Exakte Titel-Deduplizierung ergibt **694 eindeutige Titel**; genau eine zusätzliche Dublettenzeile wurde zusammengeführt. Keine semantische Dublettenentscheidung wurde dabei erfunden.



## BELASTBARER LOKALER DELTA-STAND – PSTE 0.57.27

Lokaler Kandidat:
`PSTE-0.57.27-PRODUCTWAHL-CLASSIFICATION-CANDIDATE.zip`

SHA-256:
`414b18f99e676516464790c842eedebc71a72a701c32bb95bd2d924d45ae9c79`

Basis:
PSTE 0.57.26 / SHA-256 `d7d00c1b13144fc584a593993714721ec9a8679e7d65f017e1bc2ed10c1306d6`.

Delta ausschließlich:
- neue Beitragsart-Erkennung **Produktwahl** für konkrete Produktfragen mit prüfbarem Auswahlkriterium;
- direkte A-vs-B-Fälle bleiben aus Produktwahl ausgeschlossen und im vorhandenen Vergleichsweg;
- getrennte Kandidatenexporte `EDITORIAL` / `PRODUCTWAHL`;
- manuelle Beitragsart-Korrektur in der Übersicht als Review-Override ohne Produktionsautorität;
- keine zweite Themen-Datenbank und keine Änderung des vorhandenen Normal-Metadata-/Titel-/Storage-Kerns.

Frisch lokal geprüft am 03.10.2026:
- ZIP-Integrität: PASS.
- PHP-Lint: **80/80 PASS**.
- Produktwahl Positiv/Negativ + Manual-Override: **13/13 PASS**.
- realer vorhandener 326er Sandboxbestand: **0 Produktwahl-MATCH / 0 REVIEW / 326 NO_MATCH**; damit keine künstliche Umklassifizierung dieses Samples.
- geschützte Storage-/Normalpfad-Dateien gegenüber 0.57.26 hashidentisch: PASS.
- manueller Override kopiert kein `payload_json`; er schreibt nur die vorhandenen Review-Felder plus einen History-Eintrag.
- Export bleibt read-only, `production_authority=false`, keine Provider-Abfrage, kein Artikel-/Kategorie-Write.

## HARTE GRENZE PRODUKTWAHL

`Produktwahl` ist aktuell **nur als PSTE-Kandidatenklassifikation** belegt.

Der vorhandene nachgelagerte Produktionssnapshot registriert weiterhin nur:
`FAQ`, `Beratung`, `Vergleich`, `Pflege`, `Journal`.

Daher:
- keine Übergabe von `Produktwahl` an Textmaschine/PPM/PSERC, solange der Nutzer dort nicht den eigenen Schreibregelsatz festgelegt und der vorhandene Registrierungsweg ihn aufgenommen hat;
- 0.57.27 ist **kein Live-Release und kein Produktions-PASS**.

## ERSTER OFFENER BLOCKER

`PSTE_694_TITLE_CANDIDATES_NEED_SEMANTIC_DEDUP_AND_ARTICLE_TYPE_DISTRIBUTION`

Der 695er Export ist nicht mehr der Blocker. Offen ist jetzt die belastbare **semantische Deduplizierung und Beitragsart-Verteilung** der 694 exakt eindeutigen Titel. Produktwahl darf nur nach der lokal geprüften 0.57.27-Regel zugeordnet werden; unklare Fälle bleiben Review statt geraten.

## GENAU EINE NEXT ACTION

`SEMANTIC_DEDUP_AND_ARTICLE_TYPE_DISTRIBUTION_OF_694`

1. Mit den 694 exakt eindeutigen Titeln weiterarbeiten.
2. Semantische Dubletten/Kannibalisierung konservativ prüfen.
3. Beitragsarten FAQ / Beratung / Vergleich / Pflege / Journal / Produktwahl nur bei belastbarer Evidenz zuordnen.
4. Produktwahl ausschließlich nach der geprüften 0.57.27-Regel; A-vs-B bleibt Vergleich, allgemeine Kaufkriterien bleiben Beratung.
5. Unklare Fälle als REVIEW belassen; keine Zuordnung erfinden.
6. Danach neue belastbare Artikelkandidaten mit Titel + Zielkeyword + Artikeltyp + Zielkategorie/Strukturlücke ausgeben.
7. **Keine neue DataForSEO-/Provider-Recherche vorher.**

## NICHT ANFASSEN

- keine neue Themen-Datenbank;
- kein neuer Runner/Gate/Controller;
- keine neue Provider-Recherche, solange vorhandener Bestand nicht ausgewertet ist;
- keine Gate-Absenkung;
- keine automatische Produktionsfreigabe aus `Produktwahl`;
- kein Publish;
- LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL unverändert.

Arbeits-/Fehlernachweis:
`protocol/PSTE_EXISTING_POTENTIAL_CONVERSION_GAP_20261001.md`.
