# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-10-03
STATUS: PSTE 0.57.26 LIVE / 0.57.28 NACHHALTIGER FAMILIEN-/STRUKTUR-KANDIDAT LOKAL HARD-PASS / 695ER VOLLEXPORT VORLIEGEND / 694 EXAKT EINDEUTIGE TITEL

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


Frische Zielvertrags-Lane-Klassifikation aus genau diesem Replay:
- **A DIREKT PLANBAR: 0**
- **B OHNE NEUE EXTERNE RECHERCHE REPARIERBAR: 0 aktuell bewiesen**
- **C STRUKTUR-/MENSCHENENTSCHEIDUNG: 548**
- **D GEPRÜFT PARKEN / NICHT PRODUZIEREN: 146**

Warum B aktuell 0:
Kein Replay-Fall ist mit der vorhandenen Evidenz bereits als eindeutiger interner Reparaturfall bewiesen. Bei den 364 Familienfehlern lautet die frische Familienauflösung **345 × NO_MATCH / 19 × REVIEW_REQUIRED**; die bevorzugte Familienmitgliedschaft ist **0 × PASS**. Eine automatische B-Hochstufung wäre geraten.


Wichtig für den aktiven Zielvertrag:
Die 694 Titel dürfen **nicht manuell als Ersatz für den bestehenden Normal-Metadata-Pfad** in Beitragsarten/Kategorien durchsortiert werden. Der Zielvertrag verlangt ausdrücklich Nutzung/Reparatur des vorhandenen Pfads. Solange `NORMAL_PASS=0`, gibt es keine belastbare Produktionsverteilung.



## BELASTBARER LOKALER KANDIDAT – PSTE 0.57.28

Kandidat:
`PSTE-0.57.28-SUSTAINABLE-FAMILY-STRUCTURE-ROUTING-CANDIDATE.zip`

SHA-256:
`a8df7248f38eaf2b23ce1fe30020b6c0aa2aef1881be9fe107c12da07ae11c41`

Exakte Basis:
PSTE 0.57.27 Produktwahl-Kandidat / SHA-256 `414b18f99e676516464790c842eedebc71a72a701c32bb95bd2d924d45ae9c79`.

Zielvertragskonformer Zweck:
- **keine Einmalliste für die aktuellen 694 Begriffe**, sondern Reparatur des bestehenden Normalpfads für aktuelle und zukünftige Begriffe;
- konservative deutsche Familien-Morphologie repariert reale Fehlformen wie `Gebiss ↔ Gebisse` und `striegelt ↔ Striegel`;
- neuer read-only `PSTE_Family_Structure_Router` macht einen echten Familien-`NO_MATCH` nach bereits bewiesener Portalrelevanz generisch als `STRUCTURE_GAP` sichtbar, **wenn keine sinnvolle bestehende Nachbarfamilie vorhanden ist**;
- sobald eine bestehende Familie als nah/plausibel erscheint, bleibt der Fall REVIEW statt eine neue Familie zu erfinden;
- keine Familie/Kategorie wird automatisch neu angelegt und keine Produktionsautorität erzeugt;
- danach bleibt eine echte Strukturentscheidung + normaler Reentry verpflichtend;
- Produktwahl aus 0.57.27 bleibt enthalten und wird um einen konservativen grammatischen Superlativ-Fallback ergänzt; direkte A-vs-B-Fälle bleiben Vergleich, reine Informationsflächen bleiben ausgeschlossen;
- solange Produktwahl downstream nicht registriert ist, wird ein Produktwahl-Match im Normalpfad ausdrücklich `RETAINED_NON_PRODUCING` statt falsch als FAQ/Beratung weitergereicht.

Exakter Dateidelta 0.57.27 → 0.57.28:
- geändert: `includes/class-pste-family-identity-v2.php`;
- neu: `includes/class-pste-family-structure-router.php`;
- geändert: `includes/class-pste-normal-metadata-path.php`;
- geändert: `includes/class-pste-product-choice-classifier.php`;
- geändert: `portal-seo-topic-engine.php`;
- alle übrigen Dateien unverändert.

Frische lokale Hard-Evidence:
- ZIP-Integrität: PASS;
- Fresh-Unpack PHP-Lint: **81/81 PASS**;
- realer 694er Read-only-Replay:
  - `STRUCTURE_GAP`: **320**;
  - `SANDBOX_REQUIRED`: **371**;
  - `RETAINED_NON_PRODUCING`: **3**;
  - `NORMAL_PASS`: **0**;
- alle 694 Replay-Fälle: Write-Flags false;
- Familienresolver gegenüber 0.57.27: **0 bestehende MATCH-Regressionen**, genau 3 zusätzliche konservative MATCH-Fälle:
  - `Wie striegelt man Pferde am besten?` → Striegel;
  - `Was ist das sanfteste Gebiss für Pferde?` → Gebisse;
  - `Ist ein Baucher-Gebiss auf einem Turnier erlaubt?` → Gebisse;
- Strukturrouter synthetisch Positiv/Negativ: **6/6 PASS**, inklusive zukünftiger unbekannter Begriffe;
- Produktwahl Positiv/Negativ: **14/14 PASS**;
- realer vorhandener 326er Sandboxbestand: **326/326 NO_MATCH** für Produktwahl, keine künstliche Umklassifizierung;
- Repository/Admin/DataForSEO/Research Archive/Sandbox Store/Storage Maintenance/DB Write Guard/Storage Codec/Title Composer/Title Diversity/Title Pipeline/Intent Profile/Category Gap gegenüber 0.57.27 unverändert.

Grenzen:
- 0.57.28 ist **nicht live installiert/readback-bestätigt**;
- keine neue Provider-/DataForSEO-Recherche;
- keine Gate-Absenkung;
- keine automatische Taxonomieanlage;
- kein Produktions-PASS für Produktwahl.

## HARTE GRENZE PRODUKTWAHL

`Produktwahl` ist aktuell **nur als PSTE-Kandidatenklassifikation** belegt; 0.57.28 hält solche Treffer deshalb ausdrücklich nicht-produzierend fest.

Der vorhandene nachgelagerte Produktionssnapshot registriert weiterhin nur:
`FAQ`, `Beratung`, `Vergleich`, `Pflege`, `Journal`.

Daher:
- keine Übergabe von `Produktwahl` an Textmaschine/PPM/PSERC, solange der Nutzer dort nicht den eigenen Schreibregelsatz festgelegt und der vorhandene Registrierungsweg ihn aufgenommen hat;
- 0.57.28 ist **kein Live-Release und kein Produktions-PASS**.

## ERSTER OFFENER BLOCKER

`PSTE_05728_NEEDS_WORDPRESS_LIVE_READBACK`

Die nachhaltige lokale Reparatur ist als 0.57.28-Kandidat gebaut und hart geprüft. Offen ist jetzt **nicht** mehr eine 364er Einmal-Handsortierung, sondern die reale WordPress-Bestätigung, dass exakt dieser Kandidat geladen ist und der vorhandene Bestands-/Normalpfad dieselben fail-closed Zustände liefert.

## GENAU EINE NEXT ACTION

`INSTALL_05728_THEN_LIVE_READBACK_NO_NEW_RESEARCH`

1. PSTE 0.57.28 in WordPress installieren/aktualisieren.
2. Version/Aktivstatus real zurücklesen.
3. Den **vorhandenen Bestands-/Normalpfad** erneut ausführen und Ergebnis read-only exportieren/prüfen.
4. Erwartung ist **nicht** künstlich mehr READY, sondern saubere Trennung: echte Struktur-Gaps, echte Reviews und nicht-produzierende Produktwahl-Treffer.
5. Erst nach Live-Readback die konkreten `STRUCTURE_GAP`-Entscheidungen treffen und anschließend normalen Reentry verwenden.
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
