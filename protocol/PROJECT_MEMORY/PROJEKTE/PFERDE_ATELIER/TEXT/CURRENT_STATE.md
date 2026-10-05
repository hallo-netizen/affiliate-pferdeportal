# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-10-05
STATUS: 0.57.38 PSERC-PLANABDECKUNG LOKAL HARD-PASS / NEUER JOURNAL-INVENTAR-MAPPING-FEHLER EXAKT BELEGT / 0.57.38 NICHT FINAL

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

## LIVE-READBACK 2026-10-04 – REVALIDIERUNGSPERSISTENZ

Nutzer-Screenshot belegt nach dem Bestandslauf:
- `Bestandsaufbereitung COMPLETE`;
- `0 neue Titelkandidaten`;
- **`695 vorhandene Titelkandidaten neu geprüft`**;
- **`320 Strukturentscheidung nötig`**;
- **`372 Review nötig`**;
- **`3 nicht produzierend`**;
- `0 zusätzlich für PSERC prüfbar`;
- `vollständig aufbereitet 37`;
- `Provider-Abfragen: ausgeschlossen`;
- Completion: `EXISTING_POTENTIAL_EXHAUSTED_NO_PROVIDER_CALL`.

Einordnung:
`0 neue Titelkandidaten` ist in diesem Lauf korrekt, weil keine neuen Titel erzeugt werden sollten. Der belegte Erfolg des 0.57.32-Revalidierungspfads ist die sichtbare Persistenz der **695 bereits vorhandenen** Titelkandidaten in die drei fail-closed Folgeklassen.

Die Verteilung ist mit der vorherigen 694er Deduplikationssimulation konsistent:
- 695 Live-Zeilen = 320 Struktur + 372 Review + 3 nicht produzierend;
- nach Zusammenführung der einen bekannten exakten Titel-Dublette ergibt sich erwartbar 694 = 320 Struktur + 371 Review + 3 nicht produzierend.

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

## REALER EXPORTVERGLEICH 0.57.26 → 0.57.31

Verglichen:
- `pste-global-seo-topic-map-20261003-194321-utc.json` / PSTE 0.57.26;
- `pste-global-seo-topic-map-20261004-074909-utc.json` / PSTE 0.57.31.

Ergebnis:
- beide Exporte enthalten 4472 Kandidaten;
- exakt dieselben **695** gespeicherten Titelkandidaten sind vorhanden;
- **695/695 sind als vollständige Kandidatenobjekte byte-/wertgleich**;
- damit hat 0.57.31 für diesen 695er Bestand **keine persistierte fachliche Verbesserung** erzeugt;
- im Gesamtpool änderten sich 52 Kandidaten, aber nicht die 695 Zielkandidaten.

Rootcause im Code:
`PSTE_Repository::reanalyzeRetainedBacklogBatch()` berechnet den aktuellen Normalpfad zwar neu. Bei einem erneuten Nicht-PASS wird das frische Ergebnis für einen bereits vorhandenen Titelkandidaten aber verworfen. Persistiert werden dort bisher nur:
- ein **neu** erzeugter Titelkandidat, wenn vorher kein Titel existierte;
- NORMAL_PASS-Promotionen;
- bestimmte Demotionen bereits planbarer Zeilen.

Dadurch blieb die gesamte 695er Zielmenge trotz neuer Familien-/Strukturlogik unverändert.

## LOKALER KANDIDAT PSTE 0.57.32

`PSTE-0.57.32-TITLE-CANDIDATE-REVALIDATION-PERSISTENCE-CANDIDATE.zip`

SHA-256:
`c021ed852d89b6ae87fb4b6e347f49e6a0906b512671951044ea9a55ee06f772`

Fix:
- bereits vorhandene `PSTE_STORED_SOURCE_TITLE_CANDIDATE_V1`-Titel werden beim Bestandslauf **nicht neu erzeugt**;
- stattdessen wird ihr frisch berechneter fail-closed Revalidierungszustand persistiert;
- Original-`editorial_title` und `title_candidate_evidence` bleiben unverändert;
- `production_title` bleibt leer;
- Compilerstatus bleibt `BLOCKED_BEFORE_COMPILER`;
- NORMAL_PASS darf diesen speziellen Persistenzpfad nicht benutzen;
- Raw-Query-Felder dürfen sich nicht ändern;
- UI zählt künftig zusätzlich: vorhandene Titelkandidaten neu geprüft / Strukturentscheidung nötig / Review nötig / nicht produzierend.

Hardtests:
- Fresh PHP-Lint **81/81 PASS**;
- ZIP-Integrität PASS;
- Positiv: Titel/Evidenz bleiben erhalten, STRUCTURE_GAP-Diagnostik bleibt erhalten, Produktionsautorität bleibt aus;
- Negativ: NORMAL_PASS-Misrouting BLOCK;
- Negativ: Raw-Source-Mutation BLOCK;
- Negativ: falscher Titelkandidatenvertrag BLOCK;
- Normal-Metadata-Pfad 0.57.28 → 0.57.32 hashidentisch; deshalb bleibt die bereits hart simulierte 694er Verteilung fachlich: **320 STRUCTURE_GAP / 371 SANDBOX_REQUIRED / 3 RETAINED_NON_PRODUCING**.

## REALER EXPORT-READBACK PSTE 0.57.32 – PASS

Export:
`pste-global-seo-topic-map-20261004-082759-utc.json`

Belegt im Export:
- `source_plugin.version = 0.57.32`;
- Gesamtbestand: **4472 Kandidaten**;
- gespeicherte Titelkandidaten mit `PSTE_STORED_SOURCE_TITLE_CANDIDATE_V1`: **695**;
- exakt dieselben **695 candidate_id** wie im 0.57.31-Export;
- **695/695 Zielzeilen wurden verändert/persistiert**;
- `editorial_title`: **0 Änderungen**;
- `production_title`: **0 Änderungen**;
- `target_keyword`: **0 Änderungen**;
- `title_candidate_evidence`: **0 Änderungen**;
- Normalpfad-Transitionen:
  - **320** `SANDBOX_REQUIRED → STRUCTURE_GAP`;
  - **372** `SANDBOX_REQUIRED → SANDBOX_REQUIRED`;
  - **3** `SANDBOX_REQUIRED → RETAINED_NON_PRODUCING`.
- exakte Titel-Deduplizierung: **694 eindeutige Titel**;
- genau eine Dublettengruppe:
  - `Schritt für Schritt Pferdebürsten waschen`;
  - 2 Kandidatenzeilen / 1 zusätzliche Dublette.

Damit ist der 0.57.32-Persistenzfix **live exportseitig bestätigt**.

Belastbare Arbeitsaufteilung der 372 Review-Fälle, exklusiv nach erstem offenen Gate:
- **172** redaktionelle Themen-Normalisierung REVIEW;
- **146** Portalrelevanz / externe Evidenz REVIEW;
- **42** Familienzuordnung REVIEW;
- **8** Semantik-/Intent-Konsens REVIEW;
- **4** Artikeltyp noch nicht bewiesen.

Belastbare Struktur-Gap-Aufteilung:
- **320** `STRUCTURE_GAP`;
- davon **51** mit bestehendem strukturellem Seitenhinweis:
  - Reitplatz 21;
  - Longieren 13;
  - Verladen 7;
  - Paddock 5;
  - Putzplatz 2;
  - Hufe 2;
  - Offenstall 1;
- **269** ohne solchen Seitenhinweis.

Nicht produzierend:
- **3 Produktwahl-Fälle**, weiterhin absichtlich ohne Produktionsautorität.

## FACHLICHE BESTANDSKLASSIFIZIERUNG 2026-10-04

Quelle:
- realer 0.57.32-Export `pste-global-seo-topic-map-20261004-082759-utc.json`;
- 695 persistierte Titelkandidaten / 694 exakt eindeutige Titel;
- ausschließlich vorhandene Portal-/Export-Evidenz; keine Provider-/DataForSEO-Neurecherche.

Zielvertrags-Lanes für die 694 eindeutigen Titel:
- **A direkt planbar: 0**;
- **B ohne neue externe Recherche reparierbar: 110**;
- **C Struktur-/Menschenentscheidung: 389**;
- **D geprüft parken / nicht produzieren: 195**.

Lane B – 110:
- 92 bestehende Familienbindung vorhanden; redaktionelle Relation kann aus Titel + vorhandener Familie bestätigt und danach normal reentered werden;
- 9 Fälle lassen sich aus aktuellem Portalbestand sicher an eine bereits vorhandene Familie binden;
- 9 Fälle besitzen eine konkrete manuelle Artikeltypentscheidung mit bereits vorhandener Zielkategorie.

Lane C – 389:
- 269 STRUCTURE_GAP ohne sicheren bestehenden Strukturhinweis;
- 51 STRUCTURE_GAP mit vorhandenem `structural_context_hint`;
- 33 Familienfälle ohne sichere bestehende Familienbindung;
- 34 redaktionelle Relationsfälle, die nicht sicher automatisch bestätigt wurden;
- 2 Pferdehaftpflicht-Fälle mit klarer Kosten-/Vergleichsintention, aber fehlender entsprechender Familienkategorie.

Lane D – 195:
- 145 eindeutige Titel bleiben gemäß Zielvertragsregel 5 bei fehlender realer externer Relevanzevidenz geparkt;
- 46 klare Head-/Keyword-/Transaktionsvarianten werden nicht künstlich zu Artikeln gemacht;
- 1 off-topic/nicht-redaktioneller Fall;
- 3 Produktwahl-Fälle bleiben `RETAINED_NON_PRODUCING`.
Zusätzlich existiert genau 1 physische Dublettenzeile zum logischen Titel `Schritt für Schritt Pferdebürsten waschen`; keine automatische DB-Löschung.

Persistierte Arbeitsartefakte in der persönlichen Projektbibliothek:
- `/Pferdeatelier/PSTE-05732-EXISTING-EVIDENCE-DECISIONS-2026-10-04.json`
  - Library-ID: `libfile_b0d70c5f78748191b045730eac16e5f1`
- `/Pferdeatelier/PSTE-05732-LANE-B-110-DECISIONS.json`
  - Library-ID: `libfile_a0aa30a875188191b361446d51ebcf5c`


## KORREKTUR 2026-10-04 – CHAT-SEITIGE 110ER ENTSCHEIDUNG NICHT AUTORITATIV

Frische Prüfung des realen PSTE-0.57.32-Codes und einzelner 110er Chat-Auswertungen zeigt: Die im Chat erzeugte Datei `PSTE-05732-LANE-B-110-DECISIONS.json` darf **nicht** als WordPress-Entscheidungsquelle angewendet werden.

Konkreter Gegenbeleg:
- Titel: `Wie heißt die Decke unterm Sattel beim Pferd?`;
- der aktuelle Family-V2-Pfad hatte `Unterdecken` als Match, während die redaktionelle Normalisierung korrekt `REVIEW_REQUIRED` / `EDITORIAL_TOPIC_FAMILY_NOT_SEMANTICALLY_PRESENT` hält;
- eine pauschale Chat-Regel „bestehendes Family-Match bestätigen“ würde damit einen fachlich falschen Match automatisieren.

Folge:
- die 110er Chat-Klassifikation ist **nur Audit/Arbeitsanalyse**, keine Freigabe und kein Apply-Paket;
- keine der 110 Entscheidungen wird außerhalb von WordPress in den Bestand geschrieben;
- die vorhandene WordPress-Oberfläche `SEO Themenengine → Themenprüfung` ist der autoritative manuelle Review-/Korrekturweg;
- dort existieren bereits die Originalaktionen `Beitragsart korrigieren` und `Entscheidung speichern` inklusive normaler Gate-/Historienlogik;
- kein Bulk-Bypass, kein Import einer Chat-Entscheidungsdatei.

## LOKALER KANDIDAT PSTE 0.57.33 – WORDPRESS-SAFE EXISTING-TOPIC REENTRY

Kandidat:
`PSTE-0.57.33-WORDPRESS-SAFE-EXISTING-TOPIC-REENTRY-CANDIDATE.zip`

SHA-256:
`57803212686b7256cf26994bbb25be913c39c757753b9dab92c5e37c34ae1e1b`

Zweck:
Nur generische, positiv/negativ validierte Regeln im bestehenden PSTE-Normalpfad automatisieren. WordPress/PSTE bleibt alleinige operative Autorität; kein Import der Chat-110er-Datei, kein neuer Runner, kein Bulk-Bypass.

Realer 695er Zielkohorten-Replay:
- 0.57.32: 320 STRUCTURE_GAP / 372 SANDBOX_REQUIRED / 3 RETAINED_NON_PRODUCING / 0 NORMAL_PASS.
- 0.57.33 lokal: 320 STRUCTURE_GAP / 354 SANDBOX_REQUIRED / 19 RETAINED_NON_PRODUCING / 2 NORMAL_PASS.
- 16 bisherige Reviews werden korrekt als nicht-produzierende Familienkopf-/Keywordvarianten geparkt.
- 2 werden über den bestehenden Normalpfad NORMAL_PASS:
  - `Wie striegelt man Pferde am besten?` → Striegel / FAQ / Kategorie 67.
  - `Muss man unter ein Reitpad eine Schabracke tragen?` → Schabracken / FAQ / Kategorie 84.
- alle 320 Strukturfälle bleiben Strukturfälle; die 3 bisherigen Produktwahl-Holds bleiben nicht-produzierend.

Negativbelege:
- `Wie heißt die Decke unterm Sattel beim Pferd?` bleibt REVIEW und wird nicht Unterdecken zugeordnet.
- `Schabracken pferd dressur` bleibt REVIEW.
- `Welche balance pads für pferde?` bleibt wegen Titel-/Grammatikqualität blockiert.
- `Müssen stützräder in der luft hängen?` bleibt wegen Titelqualität blockiert.
- `Pferde Schabracken waschen` bleibt REVIEW.
- falscher Titel-Evidenzvertrag oder bereits gesetzte Produktions-/Familienautorität benutzt den Stored-Title-Revalidation-Pfad nicht.
- `Beste Regendecken` bleibt als nicht belegter Superlativ blockiert.

Tests:
- PHP-Lint 81/81 PASS.
- Fresh-Unpack PHP-Lint 81/81 PASS.
- ZIP PASS.
- 695er Zielkohorte vollständig replayed.
- kein 4472er Vollpool-PASS behauptet; Vollpoolvergleich lief lokal in ein Tool-Timeout.

## LIVE-READBACK 0.57.33 – BESTANDSLAUF FÄLSCHLICH WIEDERVERWENDET ALTEN AUDIT

Nutzer-Screenshot belegt:
- Plugin `Portal SEO Themenengine 0.57.33` aktiv;
- Startmeldung `Bestandsaufbereitung gestartet: ausschließlich vorhandene Daten, keine Provider-Abfrage.`;
- Abschluss sofort `Bestandsaufbereitung COMPLETE`;
- Zähler vollständig 0: 0 neue Titelkandidaten / 0 vorhandene Titelkandidaten neu geprüft / 0 Strukturentscheidung / 0 Review / 0 nicht produzierend / 0 zusätzlich PSERC-prüfbar;
- Completion `EXISTING_POTENTIAL_EXHAUSTED_NO_PROVIDER_CALL`.

Frisch am 0.57.33-Quellcode reproduzierte Rootcause:
`startQueue()` setzte `local_backlog_complete=true`, sobald `canReuseBacklogAudit()` den vorhandenen abgeschlossenen Audit-Receipt als gültig ansah. Diese Audit-Semantik hashte jedoch nicht die in 0.57.33 geänderten Normalpfad-Abhängigkeiten. Dadurch wurde beim ausdrücklich gestarteten Existing-Only-Lauf der lokale 695er Bestand vollständig übersprungen.

Wichtig:
Der 0.57.33-Normalpfad selbst ist damit nicht live widerlegt; der Live-Lauf hat ihn gar nicht ausgeführt.

## LOKALER KANDIDAT PSTE 0.57.34 – EXISTING-ONLY FORCE REAUDIT

Kandidat:
`PSTE-0.57.34-EXISTING-ONLY-FORCE-REAUDIT-CANDIDATE.zip`

SHA-256:
`6e12c2a5f63f353ca93374252bdb0ea6e5dadd0a3e1f1bf9df305077a771568e`

KISS-Fix:
- bestehender Audit-Receipt darf weiterhin bei normalen providerfähigen Produktionswellen wiederverwendet werden;
- der ausdrücklich manuell gestartete Existing-Only-Lauf (`provider_fallback_allowed=false`) erzwingt dagegen immer den lokalen Bestands-Rescan;
- keine neue Architektur, keine neue DB, kein Provideraufruf, keine Gate-Absenkung;
- Normal-Metadata-/Familien-/Titel-/Repository-Logik gegenüber 0.57.33 byteidentisch.

Tests:
- PHP-Lint 81/81 PASS;
- ZIP-Integrität PASS;
- exakt 2 Dateien geändert: Breadth-Queue + Pluginversion;
- Branchmatrix PASS:
  - Existing-only + gültiger alter Audit → **kein Reuse**, lokaler Rescan;
  - Provider-Welle + gültiger Audit → Reuse weiterhin erlaubt;
  - Provider-Welle + ungültiger Audit → kein Reuse;
  - validierte Cancel-Continuation → vorhandene Fortsetzung bleibt erlaubt;
- lokaler Scan-Pfad bei `local_backlog_complete=false` weiterhin gebunden;
- alle fachlichen 0.57.33 Normalpfad-Dateien hashidentisch.

## FAMILIEN-DISAMBIGUIERUNG 2026-10-04 – 11 DOPPELTE FAMILIENNAMEN GEPRÜFT

Quelle:
- realer PSTE-0.57.32-Export mit 256 Topic-Familien;
- exakt 11 doppelte normalisierte Familiennamen / 22 physische Familienzeilen.

Entscheidung:
10 Gruppen werden **nur intern** semantisch getrennt; sichtbare WordPress-Namen müssen dafür nicht geändert werden:
- Bremsenfallen: Fell-&-Haut-Zweig → `Schutz vor Bremsenstichen`; Insekten-&-Schutz-Zweig → `Bremsenfallen`.
- Dualgassen: Bodenarbeit → `Dualgassen`; Bodenhindernisse → `Dualgassen-Training`.
- Ekzemerdecken: Fell-&-Haut-Zweig → `Sommerekzem & Hautschutz`; Insekten-&-Schutz-Zweig → `Ekzemerdecken`.
- Fliegenmasken: Fell-&-Haut-Zweig → `Augen- & Gesichtsschutz`; Insekten-&-Schutz-Zweig → `Fliegenmasken`.
- Fliegensprays: Fell-&-Haut-Zweig → `Insektenschutz für Haut & Fell`; Insekten-&-Schutz-Zweig → `Fliegensprays`.
- Fohlenhalfter: Ausrüstung → `Fohlenhalfter`; Training → `Fohlen-Halftertraining`.
- Kühlgamaschen: Erste Hilfe → `Akute Kühlung`; Regeneration → `Kühlgamaschen`.
- Schermaschinen: Ausrüstung → `Schermaschinen`; Gesundheit/Fell → `Pferdeschur & Fellgesundheit`.
- Seniorenfutter: Fütterung → `Seniorenfutter`; Gesundheit/Senioren → `Fütterung im Alter`.
- Sicherheitshalfter: Ausrüstung → `Sicherheitshalfter`; Training → `Sicheres Halftertraining`.

Eine Gruppe ist **keine semantische Doppelbelegung, sondern echte Struktur-Dublette**:
- `Weidezaungeräte`, product_page_id 282 und 283;
- gleicher sichtbarer Portalpfad `Weide > Zauntechnik > Weidezaungeräte`;
- identische Artikeltypen FAQ/Beratung/Vergleich/Installation/Kosten;
- deshalb nicht künstlich umbenennen, sondern vor Live-Änderung einen kanonischen Besitzer bestimmen und die andere Struktur sauber konsolidieren.

Validierung:
- keiner der 10 neuen internen Familienbegriffe kollidiert mit einer bestehenden anderen Topic-Family;
- nach den 10 internen Trennungen bleiben 255 eindeutige interne Familiennamen bei weiterhin 256 physischen Familienzeilen;
- nach späterer Konsolidierung der echten Weidezaungeräte-Dublette wären 255 physische Familien / 255 eindeutige interne Familien vorhanden.

Autoritative Mapping-Datei:
`protocol/PSTE_TOPIC_FAMILY_DISAMBIGUATION_20261004.json`.

Wichtig:
- noch keine WordPress-Kategorie gelöscht;
- keine sichtbaren Namen geändert;
- Redaktionsplan noch nicht umgehängt;
- Live-PSTE noch nicht verändert.

## FINALER LOKALER KANDIDAT PSTE 0.57.35 – KONSOLIDIERT / FULL WORKFLOW HARD PASS

Kandidat:
`PSTE-0.57.35-CONSOLIDATED-FULL-WORKFLOW-HARDPASS-CANDIDATE.zip`

SHA-256:
`b29b3403863a83d181a0529c4d3504768aca04af03cc298faee3eb5d1e39be98`

0.57.35 konsolidiert:
- Existing-Only-Force-Reaudit aus 0.57.34;
- interne eindeutige Familienidentitäten für die 11 früher doppelt benannten Familien;
- normaler Familien-/Artikeltyp-/Repository-Weg, keine Chat-Entscheidungsdatei;
- keine neue Architektur, keine Providerrecherche, keine Gate-Absenkung.

Vollständige lokale Simulation auf realem 0.57.32-Export:
- **4472/4472 Kandidaten verarbeitet, 0 Fehler**;
- Ergebnis: **86 NORMAL_PASS / 25 RETAINED_NON_PRODUCING / 2622 SANDBOX_REQUIRED / 1739 STRUCTURE_GAP**;
- gespeicherte 695 Titelkandidaten: **3 NORMAL_PASS / 19 RETAINED_NON_PRODUCING / 355 SANDBOX_REQUIRED / 318 STRUCTURE_GAP**.

Existing-Only-Orchestrierung zweimal komplett:
- Run 1: COMPLETE / 4472 verarbeitet / 695 revalidiert / 318 Struktur / 355 Review / 19 nicht produzierend / 3 promoted / 0 Provider / kein Audit-Reuse;
- Run 2: exakt dieselben Werte;
- Driver: IDLE / `PSTE_DRIVER_NO_ACTIVE_WORK`, 113 Ticks, 112 Repository-Batches, kein Research-Job-Restzustand.

Drei lokal promotionfähige Kandidaten bis Compiler-Capability-Check:
1. `Wie striegelt man Pferde am besten?` → Striegel / FAQ / Kategorie 67;
2. `Muss man unter ein Reitpad eine Schabracke tragen?` → Schabracken / FAQ / Kategorie 84;
3. `Ist es sinnvoll, Pferde zu scheren?` → interne Familie `Scheren bei Pferden` / FAQ / Kategorie 714.

Schermaschinen-Trennung:
- produktbezogene Maschinenfragen bleiben interne Familie `Schermaschinen`;
- Gesundheits-/Schurfragen laufen über `Scheren bei Pferden`;
- `Welche Schermaschine für Pferde ist die leiseste?` → `Schermaschinen` / `Produktwahl` / `RETAINED_NON_PRODUCING` wegen weiterhin nicht registriertem Productwahl-Downstream; kein Gesundheits-Misrouting.

Positive/Negative Hardtests:
- Family-Routing **25/25 PASS**;
- bestehende Family-Identity-Fixture-Regressionsmatrix **88/88 PASS**;
- interne Familien-Selfname-Matrix **11/11 PASS**;
- Duplicate-Family-Guard **2/2 PASS**;
- Negativmatrix **15/15 PASS**;
- Repository-Helper **6/6 PASS**;
- UI/Boundary **14/14 PASS**;
- PHP-Lint **81/81 PASS**;
- JSON-Parse **54/54 PASS**;
- Fresh-Unpack byteidentisch zum getesteten Source;
- 0 stray Backup-Dateien.

Registry:
- 1149 Leaf-Kategorien unverändert im Registry-Bestand;
- 256 Familien;
- **0 doppelte interne Familiennamen**;
- 11 Familien intern disambiguiert.

Grenzen:
- Existing-Only macht 0 Providercalls;
- kein Publish;
- keine Artikel-/Taxonomie-Writes;
- kein Produktionshandoff im Existing-Only-Lauf;
- Productwahl bleibt downstream separat geblockt.


## LIVE-READBACK 0.57.35 – REPOSITORY-TITELIMMUTABILITÄT HAT KORREKT GEBLOCKT

Nutzer-Screenshot belegt:
- 0.57.35 aktiv;
- Existing-Only-Lauf real gestartet;
- `PAUSED_ERROR` nach **3680 Bestandszeilen**;
- **387** vorhandene Titelkandidaten neu geprüft;
- **137** Strukturentscheidung nötig;
- **233** Review nötig;
- **16** nicht produzierend;
- Fehler: `PSTE_RETAINED_TITLE_CANDIDATE_PASS_TITLE_MUTATION`.

Exakte Rootcause lokal reproduziert:
- Kandidat: `Ist es sinnvoll, Pferde zu scheren?`;
- 0.57.35: Stored-Title-Validator lehnt die gespeicherte Form ab; der Composer-Fallback erzeugt `Ist es sinnvoll Pferde zu scheren?` ohne Komma;
- derselbe Lauf markiert diese geänderte Form anschließend `NORMAL_PASS`;
- der Repository-Guard blockiert das korrekt, weil ein persistierter Stored-Title-Kandidat bei Revalidierung nicht stillschweigend umgeschrieben werden darf.

Der frühere lokale 0.57.35-Nachweis war an dieser Stelle unvollständig: Der 695er Replay prüfte Normalpfad-Status, aber nicht zusätzlich den Repository-PASS-Invariant `stored editorial_title/evidence immutable`. Der Live-Guard hat genau diese Testlücke offengelegt.

## FINALER KANDIDAT PSTE 0.57.36 – STORED-TITLE IMMUTABILITY ROOTFIX

Kandidat:
`PSTE-0.57.36-FINAL-CONSOLIDATED-LIVEBUG-FIX.zip`

SHA-256:
`6757a1d6f96ff6448ee90b8b87640c5a330e7f5a24df6ebe81bf5f2fc8a99dc3`

KISS-Fix:
- gespeicherte Titelkandidaten werden bei Revalidierung **nie** stillschweigend durch einen neu komponierten Titel ersetzt;
- besteht die exakt gespeicherte Form den harten Titelpfad nicht, bleibt der Originaltitel + seine Evidenz erhalten und der Fall bleibt fail-closed im Review;
- keine Änderung an Queue/Driver/Admin/Repository/Familienmapping/Provider/Publish;
- gegenüber 0.57.35 exakt **2 Dateien** geändert: `class-pste-normal-metadata-path.php` + Versionsdatei.

Positiv/Negativ:
- 0.57.35 Problemfall lokal exakt reproduziert: `NORMAL_PASS` + Titelmutation → Repository-Guard würde werfen;
- 0.57.36 derselbe Fall: `SANDBOX_REQUIRED`, Originaltitel unverändert, Evidenz unverändert, `production_title` leer;
- gesamter 695er Stored-Title-Bestand: **2 NORMAL_PASS / 19 RETAINED_NON_PRODUCING / 356 SANDBOX_REQUIRED / 318 STRUCTURE_GAP**;
- Repository-Immutable-Prüfung über alle 695: **0 Fehler**; beide NORMAL_PASS-Titel byte-/wertgleich zum gespeicherten Titel; alle Nicht-PASS werden durch den vorhandenen Repository-Revalidation-Helper titel-/evidenztreu und ohne Production-Title gehalten;
- kompletter 4472er Normalpfad: **4472/4472**, **0 Fehler**, **83 NORMAL_PASS / 25 RETAINED_NON_PRODUCING / 2625 SANDBOX_REQUIRED / 1739 STRUCTURE_GAP**;
- `Welche Schermaschine für Pferde ist die leiseste?` → `Schermaschinen` / `Produktwahl` / `RETAINED_NON_PRODUCING`; kein Gesundheit/Fell-Misrouting;
- Stored-Title-Fallbacks im gesamten 4472er Replay: **0**;
- PASS-Titelmutationen im gesamten 4472er Replay: **0**;
- PHP-Lint **81/81 PASS**;
- JSON **54/54 PASS**;
- Fresh-Unpack byteidentisch zum getesteten Source;
- Queue/Driver/Admin/Repository-Code gegenüber 0.57.35 unverändert.


## FINALER KISS-KANDIDAT PSTE 0.57.37 – KOMPLETTER LOKALER WORKFLOW POSITIV/NEGATIV

Kandidat:
`PSTE-0.57.37-FINAL-KISS-INCREMENTAL-REENTRY-HARDPASS.zip`

SHA-256:
`84640c9bdd72bad551cc492e87943c8bd9c9684f357335de6c6a6bd0e0916347`

Rootcause der wiederholten Volläufe:
- ein normaler Artikel-Lösch-/Änderungsfall wurde unnötig über manuellen `Gesamtbestand neu abgleichen` geführt;
- 0.57.36 behandelte `trash` im Portal-Kontextbestand noch als existierenden Artikel;
- der UI-Knopf `Gespeicherten Block erneut prüfen` leitete den Existing-Only-PAUSED_ERROR nicht über einen sicheren Rebind-/Resume-Pfad;
- der Context-Browserloop hatte einen festen 900-Schritte-Guard und zwang bei großen Vollabgleichen zu manuellen Fortsetzungen.

0.57.37 KISS:
- WordPress-Inventar für Inhaltsabdeckung berücksichtigt nur `publish` und `draft`; `trash` / `auto-draft` blockieren nicht;
- der gespeicherte Existing-Only-Lauf besitzt einen eigenen sicheren Resume/Rebind-Pfad;
- bei unverändertem Context-Binding läuft er vom gespeicherten Cursor weiter;
- bei geänderter Inventory-/Plan-Bindung wird **nur der providerfreie lokale Bestandsaudit** ab Cursor 0 neu gerechnet, nicht der 4472er Portal-Kontext und nicht die komplette Sandbox-Bindung;
- ein normaler zukünftiger Artikel-Löschfall nutzt Safe-Baseline-Rebase + kompaktes Runtime-Context-Rehydrate und startet **keinen** `PSTE_Context_Refresh::start/processBatch`;
- ein ausdrücklich gestarteter echter Vollabgleich darf weiter voll laufen; sein Browser-Loop besitzt statt des nachweislich zu kleinen 900-Limits einen 12000er Hard-Ceiling plus echten Stall-Guard.

Exakte lokale Simulation des aktuellen realen Szenarios:
- Ausgang: Existing-Only `PAUSED_ERROR` bei 3680 Bestandszeilen + geänderte Inventory/Plan-Bindung;
- Resume/Rebind → lokaler Bestandsaudit sauber neu, **0 Context-Refresh-Starts / 0 Context-Refresh-ProcessBatch / 0 Provider**;
- Abschluss nach 113 Queue-Ticks = 1 providerfreier Sandbox-Reentry-Schritt + 112 lokale 40er Repository-Batches;
- final: COMPLETE / 4472 verarbeitet / 695 gespeicherte Titel neu geprüft;
- gleiche Bindung ab Cursor 3680: nur 20 verbleibende Repository-Batches bis COMPLETE, **kein Neustart**;
- Negativ: Provideraufruf im lokalen Audit → hart `PSTE_RETAINED_BACKLOG_PROVIDER_CALL_CONTRACT_VIOLATION`;
- Negativ: Sandbox-Reentry versucht Provider/Handoff/Artikel-/Taxonomie-Write → hart `PSTE_EXISTING_POTENTIAL_REENTRY_BOUNDARY_VIOLATION`.

Zusätzliche Positiv/Negativ-Nachweise:
- Existing-Only Resume-Matrix **6/6 PASS**;
- normaler Artikel-Lösch-/Änderungsweg **3/3 PASS**: dynamische Rebase ohne Voll-Context; Context unvollständig bzw. Struktur stale blockieren;
- Trash-Semantik **4/4 PASS**: publish/draft blockieren, trash/auto-draft nicht;
- 695 realer Stored-Title-Replay: **2 NORMAL_PASS / 19 RETAINED_NON_PRODUCING / 356 SANDBOX_REQUIRED / 318 STRUCTURE_GAP**, 0 Fehler;
- Repository-Immutable-Invariant 695: **0 Fehler**;
- alter Livebug `Ist es sinnvoll, Pferde zu scheren?`: SANDBOX_REQUIRED, Titel unverändert, kein Repository-Throw;
- `Welche Schermaschine für Pferde ist die leiseste?`: Schermaschinen / Produktwahl / RETAINED_NON_PRODUCING, kein Gesundheit/Fell-Misrouting;
- vollständiger 4472-Semantiknachweis bleibt gültig: Normal-Metadata-/Repository-/Family-/Productwahl-/Normalizer-/Intent-/Quality-Core von 0.57.36 → 0.57.37 byteidentisch; der exakte 0.57.36-4472-Replay war **4472/4472, 0 Fehler** mit 83 NORMAL_PASS / 25 RETAINED_NON_PRODUCING / 2625 SANDBOX_REQUIRED / 1739 STRUCTURE_GAP;
- UI→AJAX→Existing-Only-Resume-Route statisch exakt gebunden;
- PHP-Lint **81/81 PASS**;
- JSON **54/54 PASS**;
- Fresh-Unpack byteidentisch / PHP **81/81 PASS**;
- 0 Backup-/Stray-Dateien.

Testreport:
`PSTE-0.57.37-FINAL-HARDPASS-TESTREPORT.json`.


## LOKALER ROOTFIX PSTE 0.57.38 – PSERC-PLANABDECKUNG 1:1 GEGEN ECHTE DATEN

Realer Live-Beleg aus Export 0.57.36:
- Kandidat `Warum sagt man du alte Schabracke?` war trotz bereits geschriebenem/geplantem Artikel wieder `planning_suitability=YES` / `AUTO_RESOLVED`;
- sein `portal_context.matches` war leer.

Exakte Ursache:
- PSTE erwartete Editorial-Plan-Felder wie `category_name` / `plan_slot_sha256`;
- der reale aktuelle PSERC-Snapshot liefert die 5-Feld-Bindung unter `next_textmachine_metadata_batch.items` mit `category` / `plan_slot`;
- dadurch wurde der reale PSERC-Plan im PSTE-Familienindex faktisch mit **0 Treffern** abgebildet;
- bereits geschriebene/geplante Artikel konnten deshalb erneut als offene Themen erscheinen.

Kandidat:
`PSTE-0.57.38-EDITORIAL-PLAN-COVERAGE-ROOTFIX-HARDPASS.zip`

SHA-256:
`6a6df39e6f66d612fcf998cf3e232bb58056d222ba06679a82af3cfabd288bf8`

KISS-Fix:
- `PSTE_Snapshot::editorialPlan()` akzeptiert und normalisiert die reale PSERC-Struktur `next_textmachine_metadata_batch.items`;
- Kategorie-Slug/-ID/-Name wird gegen die vorhandene PSTE-Struktur aufgelöst;
- `title`, `target_keyword`, `category`, `article_type`, `topic_family`, `plan_slot` werden vollständig in den bestehenden Context-Index überführt;
- der bestehende manuelle Importpfad erhält dieselbe 5-Feld-Unterstützung;
- keine neue Architektur, kein neuer Runner, kein Provider, kein Publish, kein neuer Produktionsweg.

1:1 lokale Positiv/Negativ-Prüfung mit echten Daten:
- echter 0.57.36-Export: **4472 Kandidaten**;
- echter aktueller PSERC-Metadatenbatch: **16 Artikel**;
- alter 0.57.37-Vertrag gegen exakt diesen PSERC-Batch reproduziert: **0 Editorial-Plan-Treffer**;
- 0.57.38: **16/16** PSERC-Artikel werden als `EDITORIAL_PLAN / ANSWER_EQUIVALENT` erkannt und auf `ALREADY_COVERED` / `planning_suitability=NO` gesetzt;
- kompletter 4472er Context-Replay: **4472/4472**, **0 Fehler**, exakt **16** Editorial-Plan-Abdeckungen, **0** zusätzliche falsche Cross-Topic-Treffer;
- `Warum sagt man du alte Schabracke?` wird korrekt geblockt;
- ebenso die beiden weiteren zuvor fälschlich weiterhin planbaren geschriebenen/geplanten Fälle `Pferdehaftpflicht mit Fremdreiterrisiko auswählen` und `So findest du ein optimales Kappzaum für Pferde`;
- Negativtest falsche Familie: kein Treffer;
- Trash-Negativ: trash blockiert nicht;
- publish/draft-Positiv: blockieren;
- 0.57.37 Resume-/Incremental-/Trash-Core gegenüber 0.57.38 byteidentisch.

Regression/Packaging:
- exakt 3 Dateien geändert: `class-pste-snapshot.php`, `class-pste-admin.php`, Versionsdatei;
- PHP-Lint **81/81 PASS**;
- JSON **54/54 PASS**;
- Fresh-Unpack byteidentisch zum getesteten Source;
- 136 Dateien im Paket.

Testreport:
`PSTE-0.57.38-EDITORIAL-PLAN-COVERAGE-ROOTFIX-TESTREPORT.json`
SHA-256:
`1294f0a5334fe0f76e16c43ad5d4e6bec02184515e1039c015d0e2dedb8765db`.


## LOKALER ROOTFIX PSTE 0.57.39 – JOURNAL/MAGAZIN-INVENTAR KATEGORIE + TYP

Screenshot-/Exportbefund:
- In der Themenkarte erscheinen bestehende WordPress-Journalartikel wie `Wie alt werden Pferde?` und `Können Pferde schwimmen?` mit leerer Kategorie und leerem Artikeltyp.
- Im realen 0.57.36-Export sind die bestehenden WordPress-Matches für Post 15974 (`Wie alt werden Pferde?`) und Post 16029 (`Können Pferde schwimmen?`) ebenfalls mit leerem `category_name` gespeichert.
- Gleichzeitig ist die Journal-Zielbindung im selben Export eindeutig vorhanden:
  - `Wie alt werden Pferde?` → term 1486 / `Pferdegesundheit verstehen` / Journal / family `cb4b7270...`;
  - `Können Pferde schwimmen?` → term 1500 / `Pferdewissen & Grundlagen` / Journal / family `3fcebcdb...`.

Exakte Rootcause in 0.57.38:
1. `PSTE_Snapshot::inventory()` und `compilerInventoryPage()` akzeptierten für bestehende WordPress-Posts nur Kategorien aus der **Core-Produktionsstruktur** `structure()['items']`.
2. Die signierten Journal-/Magazin-Kategorien liegen absichtlich im additiven `ARTICLE_TYPE_EXTENSION_MANIFEST_V1` und damit außerhalb dieser Core-Leaf-Struktur.
3. Folge: Ein WordPress-Post in einer gültigen Journal-Kategorie wurde als `category_id=0 / category_name='' / article_type=''` in das PSTE-Inventar aufgenommen.
4. Zusätzlich berechnete `PSTE_Analytics::topicRows()` den Artikeltyp noch einmal aus dem sichtbaren Kategorienamen und ignorierte einen bereits sauber gelieferten Inventory-`article_type`. Für flache Journal-Kategorien wie `Pferdegesundheit verstehen` ergab auch dieser Weg keinen Typ.

Kandidat:
`PSTE-0.57.39-JOURNAL-INVENTORY-CATEGORY-ROOTFIX-HARDPASS.zip`

SHA-256:
`10a6e28e52639071ccde56d4c96f0ae3a37aae1d93bd8e2c51368f13f8e342f9`

KISS-Fix:
- signierte additive Extension-Kategorien werden **nur read-only für das WordPress-Inventar** nach Term-ID aufgelöst;
- sie werden nicht in die Core-Produktionshierarchie hineingeschrieben;
- Journal-Family-Key wird für bestehende WordPress-Artikel exakt mit derselben bereits vorhandenen Formel des Extension-Routers gebildet: `PSTE_EXTENSION_EXPLICIT_SCOPE_V1|journal|<exact topic identity>`;
- Themenkarte übernimmt vorhandenen Inventory-`article_type` und verwendet die alte Namensinferenz nur noch als Fallback;
- unbekannte/nicht signierte Kategorien bleiben fail-closed unzugeordnet;
- Kollision Extension-Term-ID ↔ Core-Produktionskategorie blockiert hart.

1:1 lokale Positiv-/Negativprüfung:
- 0.57.38 exakt reproduziert:
  - Post 15974 → Kategorie leer / Typ leer / 0 Context-Matches;
  - Post 16029 → Kategorie leer / Typ leer / 0 Context-Matches.
- 0.57.39:
  - Post 15974 → `Pferdegesundheit verstehen` / `Journal` / exakt 1 WORDPRESS ANSWER_EQUIVALENT / same_topic_family=true;
  - Post 16029 → `Pferdewissen & Grundlagen` / `Journal` / exakt 1 WORDPRESS ANSWER_EQUIVALENT / same_topic_family=true;
  - regulärer Core-Fall `FAQ Sperrriemen` bleibt unverändert;
  - unbekannte WordPress-Kategorie bleibt leer/unzugeordnet: PASS;
  - Extension/Core-Term-Kollision: harter Block PASS;
  - Themenkarte: 0.57.38 zeigte leeren Typ, 0.57.39 zeigt `Journal`.
- exakt 3 Dateien gegenüber 0.57.38 geändert: Snapshot, Analytics, Versionsdatei;
- Normal-Metadata, Repository, Extension-Router, Family-Identity, Title-Pipeline und Context-Evaluator byteidentisch zu 0.57.38;
- der komplette 0.57.38 Editorial-Plan-Rootfix-Abschnitt ist byteidentisch;
- PHP-Lint **81/81 PASS**;
- JSON **54/54 PASS**;
- Fresh-Unpack **136/136 Dateien byteidentisch**.

Testreport:
`PSTE-0.57.39-JOURNAL-INVENTORY-CATEGORY-ROOTFIX-TESTREPORT.json`
SHA-256:
`005c4a4d5c9ebf1437c0c882e5f00e19d3cea078e86c1bdb54a0e6d1b0c8105e`.


## DELTA 2026-10-05 – MAGAZIN/JOURNAL-BESTANDSARTIKEL OHNE KATEGORIE IN DER THEMENKARTE

Realer Nutzer-Screenshot + realer Export belegen:
- `Wie alt werden Pferde?` erscheint als bestehender `WORDPRESS / PUBLISH`-Artikel, aber in der zentralen Themenkarte mit leerer Kategorie und leerem Artikeltyp;
- realer WordPress-Post: ID **15974**;
- im realen Export erscheint derselbe WordPress-Treffer in `closest_existing_matches` mit `category_name=""`;
- der zugehörige PSTE-Kandidat ist dagegen korrekt und eindeutig als **Journal** geroutet:
  - Kategorie-ID **1486**
  - Kategorie **Pferdegesundheit verstehen**
  - Slug `pferdegesundheit-verstehen`
  - Artikeltyp **Journal**
  - Extension-Route **PASS**.

Exakte Rootcause im 0.57.38-Code:
- `PSTE_Snapshot::inventory()` übernimmt WordPress-Kategorien nur, wenn deren Term-ID in `PSTE_Snapshot::structure()['items']` als reguläre Portal-/Produktionskategorie aufgelöst wurde;
- Journal-/Magazin-Kategorien werden aber über den separaten bestehenden `PSTE_Article_Type_Extension_Router` aufgelöst;
- dadurch kennt der Kandidatenpfad Kategorie 1486 korrekt, während der allgemeine WordPress-Inventarpfad denselben bestehenden Journalartikel kategorielos darstellt.

Einordnung:
- kein Beleg für fehlende WordPress-Kategorie am Artikel;
- kein Beleg für falsches Journal-Routing des Kandidaten;
- **Read-only-Inventarmapping-Gap bestehender Journalartikel**;
- 0.57.38 behebt den PSERC-Plan-Abdeckungsfehler, aber diesen Journal-Inventarfehler noch nicht;
- deshalb ist 0.57.38 **kein finaler Produktionsstand**.

## ERSTER OFFENER BLOCKER

`PSTE_JOURNAL_EXISTING_ARTICLE_CATEGORY_MAPPING_GAP`

Bestehende Journal-/Magazinartikel können im WordPress-Inventar der PSTE ohne Kategorie/Familie/Artikeltyp erscheinen, obwohl dieselbe Journal-Kategorie im Extension-Routing eindeutig registriert und für Kandidaten korrekt auflösbar ist. Das gefährdet Bestands-/Abdeckungslogik und muss vor der nächsten Produktionswelle geschlossen werden.

## GENAU EINE NEXT ACTION

`FIX_JOURNAL_INVENTORY_MAPPING_THEN_FULL_LOCAL_1TO1_POSITIVE_NEGATIVE`

1. Auf Basis von 0.57.38 ausschließlich den bestehenden Read-only-Inventarpfad ergänzen: registrierte Artikeltyp-Erweiterungskategorien müssen bei bestehenden WordPress-Artikeln als gültige Kategorie/Familie/Artikeltyp erkannt werden.
2. Keine Journal-Kategorie in die normale Produktfamilienstruktur zwängen; vorhandenen Extension-Registry-/Router-Weg nutzen.
3. Danach **kompletten betroffenen Workflow lokal 1:1** gegen den realen Export simulieren:
   - bestehender Journalartikel `Wie alt werden Pferde?` → Kategorie 1486 / Journal / Existing;
   - regulärer FAQ/Beratung/etc.-Artikel → unverändert;
   - unbekannte/nicht registrierte Kategorie → weiterhin fail-closed/leer, keine erfundene Zuordnung;
   - mehrere Produktionskategorien → bestehender Hard-Block bleibt;
   - publish/draft zählen, trash/auto-draft nicht;
   - 16/16 PSERC-Plan-Abdeckung aus 0.57.38 bleibt PASS;
   - keine neuen Cross-Topic-Treffer;
   - Resume-/Incremental-/Provider-/Publish-Grenzen unverändert.
4. Erst bei vollständigem Positiv-/Negativ-/Regression-PASS genau **einen konsolidierten Kandidaten** ausgeben.
5. Danach genau ein Live-Readback → Gesamte Themenkarte exportieren → Redaktionsplan → Artikelproduktion.

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
