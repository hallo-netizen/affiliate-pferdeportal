# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-10-03
STATUS: PSTE 0.57.26 LIVE / 0.57.27 PRODUKTWAHL-KANDIDAT LOKAL GEPRÜFT / 695ER VOLLEXPORT VORLIEGEND / 694 EXAKT EINDEUTIGE TITEL / FRISCHER NORMALPFAD 0 VON 694 PASS

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


Frischer Zielvertrags-/Normalpfad-Readback am 03.10.2026:
- exakt die vorhandene 0.57.26-Implementierung `PSTE_Normal_Metadata_Path::applyToPayload()` lokal read-only gegen den realen Export + dessen `site_baseline` erneut ausgeführt;
- **694/694** exakt eindeutige Titel erneut geprüft;
- Provider-Aufrufe **0**; Writes **0**;
- `NORMAL_PASS`: **0/694**;
- `SANDBOX_REQUIRED`: **694/694**;
- frische Hauptverluste:
  - Portalrelevanz nicht bewiesen: **146**;
  - Portalrelevanz bewiesen, Familienzuordnung nicht bewiesen: **364**;
  - redaktionelle Themen-Normalisierung nicht PASS: **172**;
  - Typ-/Intent-/Dual-Strand-Block: **11**.
- zusätzlich **6** Kollisionsgruppen über den bereits vorhandenen `semantic_fingerprint`; sie wurden **nicht automatisch zusammengeführt**, weil der Dubletten-/Kannibalisierungsweg nicht umgangen werden darf.

Wichtig für den aktiven Zielvertrag:
Die 694 Titel dürfen **nicht manuell als Ersatz für den bestehenden Normal-Metadata-Pfad** in Beitragsarten/Kategorien durchsortiert werden. Der Zielvertrag verlangt ausdrücklich Nutzung/Reparatur des vorhandenen Pfads. Solange `NORMAL_PASS=0`, gibt es keine belastbare Produktionsverteilung.



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

`PSTE_694_FRESH_NORMAL_PATH_ZERO_PASS`

Der frühere Export-Blocker ist erledigt. Der frische Replay beweist jetzt den eigentlichen Engpass: **kein einziger der 694 exakt eindeutigen Titel erreicht im bestehenden Normal-Metadata-Pfad NORMAL_PASS**. Eine manuelle Beitragsart-Verteilung wäre ein Zielvertrags-Bypass.

Größter frischer interner Block:
**364 × `PSTE_PORTAL_RELEVANCE_PROVEN_FAMILY_ASSIGNMENT_NOT_PROVEN`**.

## GENAU EINE NEXT ACTION

`SPLIT_364_FAMILY_ASSIGNMENT_MISSES_BY_EXISTING_EVIDENCE_ONLY`

1. Die **364 frischen Familienzuordnungsfehler** ausschließlich mit den bereits vorhandenen `family_resolution`-/`family_membership`-/Portal-Baseline-Daten aufteilen:
   - echte interne Resolver-/Reentry-Fälle → Lane B;
   - echte Struktur-/Zuordnungsentscheidungen → Lane C.
2. Keine neue Familienlogik, keinen neuen Klassifikator und keine neue Recherche erfinden.
3. Erst nach dieser Trennung den **bestehenden** Family-/Normal-Metadata-Pfad ursächlich reparieren, falls ein belegter Resolverfehler vorliegt.
4. Beitragsart, Zielkeyword, Kategorie und Plan-Slot erst aus einem echten `NORMAL_PASS` übernehmen.
5. Die 6 `semantic_fingerprint`-Kollisionsgruppen nur als Dubletten-/Kannibalisierungs-Review führen, nicht automatisch mergen.
6. **Keine neue DataForSEO-/Provider-Recherche vorher.**

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
