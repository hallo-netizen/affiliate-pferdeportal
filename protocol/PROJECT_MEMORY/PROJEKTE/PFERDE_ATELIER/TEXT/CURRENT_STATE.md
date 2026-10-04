# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-10-04
STATUS: PSTE 0.57.28 LIVE / AKTIVER EINZELLAUF PAUSED_ERROR / 0.57.31 REPLAY-SAFE LOCAL-FINALIZE-RECOVERY LOKAL HARD-PASS

## EINE ZUSTÄNDIGE CURRENT-BINDUNG

- **PSTE-Themen-/SEO-Bestand:** diese Datei.
- **Artikelproduktion K9:** ausschließlich `konzept9/greenfield-20260929:CURRENT_STATE.json`.
- **Plugin-Inventar/Updatechronik:** `../PLUGINS/CURRENT_STATE.md`; keine zweite Fachwahrheit.
- **Aktiver Themenverwertungs-Zielvertrag:** `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/ZV-PSTE-THEMENVERWERTUNG-001.md`.

## LIVE-READBACK 2026-10-04

Nutzer-Screenshot belegt im gespeicherten Einzellauf:
- Server-Driver: **BLOCKED · `PSTE_DRIVER_REPEATED_SYSTEM_FAILURE`**;
- gespeicherter Einzellauf: **PAUSED_ERROR**;
- Datenquellen 3 von 3;
- Fragen COMPLETE;
- Abschluss **SANDBOX_BATCH 0/15**;
- exakter Fehler: **`PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`**;
- Systemstatus: **HÄNGT-BLOCKED · `PSTE_DRIVER_REPEATED_SYSTEM_FAILURE:PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`**.

Frisch gegen den 0.57.29-Code reproduziert:
- `PSTE_Sandbox_Record_Contract::fromNormalPath()` berechnet bei V2 die Hashes der echten Portal-/Nearest-/Exclusion-Komponenten;
- `applyToRecord()` übernahm diese Komponenten aber **nur für den Legacy-Vertrag**;
- neue V2-Records behielten dadurch leere Top-Level-Komponenten, während `sandbox_dataflow` die Hashes der echten Komponenten trug;
- der persistenznahe Self-Check blockiert danach korrekt mit exakt `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`.
Damit ist die Ursache **reproduziert und nicht geraten**.

Lokaler Rootfix-Kandidat:
`PSTE-0.57.30-SANDBOX-DATAFLOW-ROOTFIX-CANDIDATE.zip`
SHA-256:
`c2f0e9e05f2ffddeea2c7ee022dd18ad04f9f5820ebbab4eabfab1253c235aa4`.

Fix:
- V2-Komponenten werden nur transient vom Producer an `applyToRecord()` mitgegeben;
- dort vor Persistenz gegen die bereits berechneten Hashes validiert;
- exakt einmal als Record-Komponenten gespeichert;
- aus `sandbox_dataflow` vor Speicherung wieder entfernt;
- alle bestehenden Drift-/Hash-Gates bleiben fail-closed.

Frische Tests:
- 0.57.29 Vorher-Negativtest reproduziert exakt `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`;
- 0.57.30 Positivtest Record-Bindung PASS;
- Negativtest nach absichtlicher Portal-Komponentenmutation blockiert weiterhin exakt mit `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`;
- kein transienter Komponenten-Leak in `sandbox_dataflow`;
- UI-Guard Regression **5/5 PASS**;
- Fresh-Unpack PHP-Lint **81/81 PASS**;
- ZIP-Integrität PASS;
- 0 Stray-Backup-Dateien;
- Delta 0.57.29 → 0.57.30 exakt **2 Dateien**:
  - `includes/class-pste-sandbox-record-contract.php`;
  - `portal-seo-topic-engine.php`;
- Familien-/Struktur-/Normalpfad-/Produktwahl-/Admin-/Repository-/Driver-/Storage-/Titel-/Intent-Dateien gegenüber 0.57.29 hashidentisch.

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

## LOKALER NACHPRÜFBEFUND 0.57.30 → 0.57.31

Die lokale Vollsimulation des **tatsächlichen Resume-Wegs** hat einen weiteren Fehler in 0.57.30 aufgedeckt:

- Originalbutton im UI: **„Gespeicherten Block erneut prüfen“**.
- 0.57.30-Handler ruft nur den Server-Driver.
- Der 0.57.30-Driver behandelt einen `PAUSED_ERROR`-Einzellauf sofort als `SINGLE_PARKED`.
- Damit würde der aktuelle lokale Finalize-Fehler **nicht** erneut geprüft, sondern der gespeicherte Lauf archiviert/entfernt.
- 0.57.30 ist deshalb **supersediert und darf nicht installiert werden**.

Neuer Kandidat:
`PSTE-0.57.31-REPLAY-SAFE-LOCAL-FINALIZE-RECOVERY-CANDIDATE.zip`

SHA-256:
`35f670fc8a44310b1cb858764e506b0af950ac3941790bb1f5ee93e4a4270430`

Delta 0.57.30 → 0.57.31:
- `includes/class-pste-research-job.php`: exakt `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT` als replay-sicherer lokaler FINALIZE-Fehler gebunden;
- `includes/class-pste-research-driver.php`: vor dem Parken eines `PAUSED_ERROR`-Jobs wird der vorhandene sichere Recovery-Pfad `PSTE_Research_Job::current()` ausgeführt; nur wenn der Job danach weiterhin PAUSED/UNKNOWN ist, bleibt das bisherige Parken aktiv;
- `portal-seo-topic-engine.php`: Version 0.57.31.

Frische lokale Simulation:
- 0.57.30 bei exakt sicherem PAUSED_ERROR: `SINGLE_PARKED`, 0 Advance, 1 Park → **FAIL**;
- 0.57.31 bei exakt `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`: 1 Recovery + 1 Advance + 0 Park → **PASS**;
- 0.57.31 bei absichtlich unsicherem `PSTE_UNSAFE_PROVIDER_FAILURE`: 0 Advance + 1 Park → **FAIL-CLOSED PASS**;
- 0.57.31 Sandbox-Dataflow-Rootfix positiv: PASS;
- nach absichtlicher Portal-Komponentenmutation blockiert weiterhin exakt `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`;
- Replay-Safe-Klassifikation: Portal-Component-Drift = SAFE; erfundener Providerfehler = NOT_SAFE;
- Fresh-Unpack PHP-Lint **81/81 PASS**;
- Originalbezeichnungen im 0.57.31-Code unverändert belegt:
  - **„Server-Driver:“**
  - **„Gespeicherter Einzellauf:“**
  - **„Gespeicherten Block erneut prüfen“**.

## ERSTER OFFENER BLOCKER

`PSTE_05731_NEEDS_LIVE_INSTALL_AND_EXACT_RESUME_READBACK`

Der Live-Lauf steht weiterhin bei `PAUSED_ERROR` mit `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`. 0.57.31 ist lokal bis zum echten Resume-/Parkpfad positiv und negativ simuliert; offen ist nur der reale WordPress-Readback.

## GENAU EINE NEXT ACTION

`INSTALL_05731_AND_OBSERVE_EXISTING_SAVED_SINGLE_RUN`

1. **Nicht 0.57.30 installieren.**
2. PSTE **0.57.31** installieren.
3. `SEO Themenengine → Einstellungen` öffnen.
4. Im vorhandenen Abschnitt **„Longtails recherchieren, Titel bilden und Kategorien zuordnen“** den Block **„Gespeicherter Einzellauf:“** beobachten.
5. Durch den Versionswechsel darf der sichere lokale Recovery-Pfad den gespeicherten `PAUSED_ERROR` selbst wieder aufnehmen. Falls der Block noch `PAUSED_ERROR` zeigt, exakt den vorhandenen Button **„Gespeicherten Block erneut prüfen“** einmal anklicken.
6. Erfolgsnachweis: `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT` verschwindet und **„Abschluss SANDBOX_BATCH 0/15“** geht über 0/15 hinaus oder ein neuer anderer fail-closed Fehlercode erscheint.
7. Bei neuem Fehler nicht mehrfach klicken; exakten sichtbaren Code übernehmen.
8. Keine neue Produktionswelle und keine neue DataForSEO-/Provider-Recherche.

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
