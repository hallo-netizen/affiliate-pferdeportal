# PSTE – VORHANDENES POTENZIAL / AUTOMATISCHE EDITORIALISIERUNG – BEFUND 2026-10-01

ROLLE: Fehler-/Arbeitsprotokoll und Nachweis. **Keine CURRENT-Autorität.**
Aktueller Status/NEXT ACTION ausschließlich:
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md`.

## Frisch geprüfter Kernbefund

Die automatische Umwandlung vorhandener Suchbegriffe/Themen in redaktionell nutzbare Metadaten ist **nicht neu zu bauen**. Sie existiert bereits im PSTE-Bestand.

Der bestehende Normalweg `PSTE_Normal_Metadata_Path` ist ausdrücklich für:
- normale Recherche;
- gespeicherte Themen-Rebuilds;
- Sandbox-Normal-Reentry.

Er führt – fail-closed – durch:
1. Portalrelevanz;
2. Familien-/Gruppenzuordnung;
3. Themen-Normalisierung;
4. Intentanalyse;
5. Artikeltyp-Auflösung;
6. Titelpipeline;
7. Zielkeyword;
8. Zielkategorie;
9. nachgelagerte Planning-Readiness / Dubletten-/Kannibalisierungsprüfung.

Bei PASS werden u. a. `editorial_title` / `production_title`, `target_keyword`,
`suggested_article_type` / `proposed_article_type` sowie Ziel-/Vorschlagskategorie gebunden.
Der PASS-Grund enthält `ARTICLE_TYPE_AUTOMATICALLY_RESOLVED`.

## Historischer Beleg – gute Titel waren bereits implementiert

Spätestens PSTE 0.56.25 besaß den expliziten Rootfix für natürliche, grammatisch bessere Titel.
Dabei blieb das exakte Zielkeyword die SEO-Autorität; reine Präsentationswörter durften nur die Lesbarkeit verbessern.
Der gleiche Stand band Retained/Current Backlog vor Provider-Aufrufen an dieselbe Planning-Readiness.

Quelle:
`protocol/STARTMASTER0100_ATTRIBUTE_RICH_COMPILER_READY_BREADTH_ROOTFIX_20260828.md`.

## Frisch geprüfter Retained-Backlog-Weg

`PSTE_Repository::reanalyzeRetainedBacklogBatch()` liest gespeicherte `topic_pool`-Zeilen
(`manual_status=''`) und führt sie erneut durch den bestehenden Normal-Metadata-Pfad.

Dabei gilt bereits:
- kein Provider-Aufruf;
- Rohbegriff bleibt unverändert;
- Normal-Metadata-Pfad darf Familie, Artikeltyp, Titel, Zielkeyword und Kategorie neu auflösen;
- danach Planning-Readiness;
- nur `AUTO_RESOLVED` + gültige Planung darf weiterkommen;
- bestehende Dubletten/Abdeckung werden weiterhin fail-closed demotiert.

## Aktuelles Verwertungsproblem

Das aktuelle Problem ist daher **nicht**:
„Es gibt keinen automatischen Übersetzer von Keywords/Gruppen zu guten Titeln und Kategorien.“

Das aktuelle Problem ist:
**Von dem großen gespeicherten Bestand schaffen es zu wenige Kandidaten durch den bereits vorhandenen automatischen Aufbereitungsweg bis zur realen Planung/READY-Stufe.**

Der letzte reale Ablauf nach abgeschlossenem Portalabgleich zeigte:
- 23 geeignete/geprüfte Themen im PSERC-Lauf;
- davon nur 2 READY;
- diese 2 wurden anschließend vollständig über K9 produziert.

Der Nutzer meldet am 01.10.2026 zusätzlich, dass die aktuell laufende neue Recherchewelle nur geringe Ausbeute liefert.

Ohne terminalen Readback dieser laufenden Welle ist **noch nicht belegt**, an welcher vorhandenen Stufe das meiste Potenzial verloren geht.
Nicht raten.

Zu unterscheiden sind mindestens:
- Rohbegriff/Quelle vorhanden, aber Portalrelevanz nicht bewiesen;
- Familien-/Gruppenzuordnung nicht eindeutig;
- Intent/Artikeltyp nicht eindeutig;
- Titelpipeline nicht PASS;
- Zielkategorie fehlt / STRUCTURE_GAP;
- Planning-Readiness scheitert an Dublette/Kannibalisierung/Abdeckung;
- Kontext nicht CURRENT;
- Sandbox-Fall benötigt Normal-Reentry;
- echte nicht-redaktionelle/alte/irrelevante Begriffe.

## 0.57.18-Kandidat – nur Teilfix, nicht Gesamtlösung

Lokal wurde aus dem geprüften 0.57.17-Paket der Kandidat
`PSTE 0.57.18 – EXISTING POTENTIAL FIRST`
gebaut.

Sein einzig relevanter fachlicher Zusatz:
**bereits sichere `AUTO_REENTRY_ELIGIBLE`-Sandbox-Kandidaten werden vor Retained-Backlog und vor Provider-Recherche über den bestehenden Normal-Reentry geleert.**

Dieser Kandidat ändert **nicht** Titelcomposer, Familienauflösung, Artikeltyp-Auflösung,
Normal-Metadata-Pfad, Dubletten-/Kannibalisierungsregeln oder Qualitätsgates.

Lokale Evidence:
- PHP-Lint 79/79 PASS;
- sicherer Sandbox-Reentry ohne Provider PASS;
- gemischter Positiv-/Negativ-Reentry PASS;
- Provider-Aufruf in Reuse-Phase wird BLOCK;
- keine eligible Sandbox erfindet keinen Kandidaten;
- Fresh-Unpack Wiederholung PASS.

**Wichtig:** 0.57.18 ist ein Teilfix für die Reihenfolge der Verwertung. Er beweist noch nicht,
warum der große gespeicherte Topic-Pool aktuell nur geringe READY-Ausbeute liefert.

## Exakte nächste Diagnose – KISS

Nach Ende der bereits laufenden Recherchewelle:
**keine weitere Provider-Recherche starten.**

Stattdessen den vorhandenen Bestand read-only als Verwertungs-Funnel auswerten:

`GESPEICHERT`
→ `SOURCE QUERY VERWERTBAR`
→ `PORTALRELEVANZ PASS`
→ `FAMILIE/GRUPPE PASS`
→ `ARTIKELTYP PASS`
→ `TITEL + ZIELKEYWORD PASS`
→ `KATEGORIE PASS`
→ `PLANNING-READINESS PASS`
→ `KONTEXT CURRENT`
→ `READY`.

Für jede Verluststufe:
- Anzahl;
- führende Reason-Codes;
- Anteil A / B / C / D gemäß `ZV-PSTE-THEMENVERWERTUNG-001`.

Ziel ist besonders **Lane B**:
vorhandene Evidenz reicht, und nur bestehende automatische Zuordnung/Titel/Reentry muss erneut sauber greifen.

Keine neue Architektur, kein neues Themenlager, kein pauschales Freigeben.


## DELTA 2026-10-02 – ROOTCAUSE BELEGT / TITELFUNDS ERSCHLOSSEN

Realer Live-Readback unter PSTE 0.57.26:
- Bestandsaufbereitung COMPLETE;
- 695 neue Titelkandidaten aus vorhandenem Material;
- 8 davon zusätzlich für PSERC prüfbar;
- 36 vollständig aufbereitet;
- keine Provider-Abfrage;
- Completion: `EXISTING_TITLE_CANDIDATES_GENERATED_NO_PROVIDER_CALL`.

Belegter Rootcause:
Ein vorhandenes aber leeres `editorial_title` konnte im Kontextpfad den Fallback auf vorhandene Query-Felder verhindern. Dadurch entstand `PSTE_CONTEXT_QUERY_MISSING` trotz gespeichertem Recherchematerial. 0.57.26 repariert diesen Fallback und nutzt vorhandene Fragen/redaktionelle Formulierungen als nicht-produktionsautorisierende Titelkandidaten.

UI-Nachbefund:
Wenn die Seite im RUNNING-Zustand gerendert wurde und der AJAX-Status später COMPLETE wird, wird nur der Statuskasten aktualisiert. COMPLETE-Aktionsformulare werden nicht nachträglich in den DOM eingefügt. Ein frischer Seitenrender bei COMPLETE zeigt dagegen den Exportbutton. Lokale Positiv-/Negativsimulation reproduziert beide Wege.

Aktuelle NEXT ACTION steht ausschließlich in TEXT/CURRENT_STATE.md.

## DELTA 2026-10-03 – PRODUKTWAHL-KLASSIFIKATION / LOKALER 0.57.27-KANDIDAT

Nutzerentscheidung:
Die neue Beitragsart heißt **Produktwahl**.

Abgrenzung:
- konkrete kaufbare Produktfamilie muss durch vorhandene Familienzuordnung bewiesen sein;
- die Suchfrage muss auf ein konkretes Produkt bzw. eine sehr kleine Spitzenauswahl hinauslaufen;
- nötig ist ein entscheidendes, prüfbares Auswahlmerkmal wie leiseste, günstigste, leichteste, stärkste, längste Akkulaufzeit oder eng gebundene „beste für X“-Frage;
- direkte A-vs-B-Fälle bleiben **Vergleich**;
- allgemeine Kaufkriterien bleiben **Beratung**;
- reine Informationsfragen bleiben FAQ/Wissen;
- Superlativ ohne bewiesene Produktfamilie darf nicht zu Produktwahl werden.

Lokaler Kandidat:
`PSTE-0.57.27-PRODUCTWAHL-CLASSIFICATION-CANDIDATE.zip`
SHA-256 `414b18f99e676516464790c842eedebc71a72a701c32bb95bd2d924d45ae9c79`.

Exakte Basis:
PSTE 0.57.26, SHA-256 `d7d00c1b13144fc584a593993714721ec9a8679e7d65f017e1bc2ed10c1306d6`.

Exakter Dateidelta:
- neu: `includes/class-pste-product-choice-classifier.php`;
- geändert: `includes/class-pste-admin.php`;
- geändert: `includes/class-pste-repository.php`;
- geändert: `portal-seo-topic-engine.php`;
- übriger Pluginbaum unverändert.

Frische lokale Evidence 03.10.2026:
- ZIP-Integrität PASS;
- PHP-Lint 80/80 PASS;
- Produktwahl Positiv/Negativ inklusive Manual-Override 13/13 PASS;
- realer 326er Sandboxbestand: 0 MATCH / 0 REVIEW_REQUIRED / 326 NO_MATCH;
- Storage-/Normalpfad-Hardlockdateien gegenüber 0.57.26 hashidentisch: Research Archive, Sandbox Record Store, Storage Maintenance, DB Write Guard, Storage Codec, Normal Metadata Path, Title Composer, Title Diversity, Title Pipeline, Intent Profile;
- Exportpfad read-only: keine Provider-Abfrage, kein Artikel-/Kategorie-Write, keine Produktionsautorität;
- manueller Review-Override kopiert kein `payload_json`; er schreibt nur `manual_article_type`, `manual_note`, Review-Zeit/Nutzer und einen History-Eintrag.

Grenzen / ausdrücklich NICHT bewiesen:
- keine 695er Vollklassifikation, weil der reale 695er Export noch nicht als Datei vorliegt;
- kein WordPress-Live-Readback für 0.57.27;
- kein Produktions-PASS für Produktwahl;
- downstream registriert der vorhandene Produktionssnapshot Produktwahl noch nicht;
- keine breite neue FAQ/Pflege/Sicherheit/Journal-Verteilung implementiert oder bewiesen;
- kein 0.57.28-Kandidat vorhanden.

Aktueller Status und genau eine NEXT ACTION ausschließlich aus
`protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/CURRENT_STATE.md`.



## DELTA 2026-10-03 – BESTEHENDER EXPORTWEG FÜR 695ER HANDOFF

Der separate kompakte Exportbutton ist im aktuellen Live-Screenshot nicht sichtbar. Für den benötigten Handoff ist jedoch kein neues Plugin nötig.

Der bereits vorhandene vollständige Exportweg ist in PSTE 0.57.26 belegt:
`SEO Themenengine → Einstellungen → Longtails recherchieren, Titel bilden und Kategorien zuordnen → Gesamte Themenkarte exportieren`.

`Gesamte Themenkarte exportieren` streamt den vollständigen Topic-Pool über `adminTopicPoolPage()`. Die 695 Titelkandidaten lassen sich daraus exakt anhand
`title_candidate_evidence.contract = PSTE_STORED_SOURCE_TITLE_CANDIDATE_V1`
und nichtleerem `editorial_title` herausziehen.

Kein Plugin-Update erforderlich. Keine neue Recherche erforderlich.


## DELTA 2026-10-03 – 694ER FRISCHER NORMALPFAD-REPLAY / ZIELVERTRAGSPRÜFUNG

Basis:
- realer Export `pste-global-seo-topic-map-20261003-194321-utc.json`;
- PSTE 0.57.26;
- 695 Titelkandidaten, nach exakter Titel-Deduplizierung 694;
- exakt vorhandener `PSTE_Normal_Metadata_Path::applyToPayload()`;
- lokaler read-only Replay mit Export-`site_baseline`;
- Provider-Aufrufe 0, Writes 0.

Frisches Ergebnis:
- `NORMAL_PASS`: **0/694**;
- `SANDBOX_REQUIRED`: **694/694**;
- Portalrelevanz nicht bewiesen: **146**;
- Portalrelevanz bewiesen, Familienzuordnung nicht bewiesen: **364**;
- Editorial-Topic-Normalisierung nicht PASS: **172**;
- Typ-/Intent-/Dual-Strand-Block: **11**.

Dubletten:
- 1 exakt gleicher Titel wurde bereits technisch zusammengeführt (695 → 694);
- zusätzlich 6 Kollisionsgruppen mit identischem bestehendem `semantic_fingerprint`;
- keine davon automatisch semantisch gemergt, weil Dubletten-/Kannibalisierungs-Gates erhalten bleiben.

Zielvertragsfolgerung:
Die frühere Arbeitshypothese „694 jetzt manuell semantisch deduplizieren und Beitragsarten verteilen“ darf **nicht** als Ersatzweg verwendet werden. `ZV-PSTE-THEMENVERWERTUNG-001` verlangt ausdrücklich den bestehenden Normal-Metadata-Pfad zu nutzen/reparieren statt einen neuen Keyword→Titel/Typ/Kategorie-Mechanismus daneben zu bauen.

Erster frischer interner Block:
`PSTE_PORTAL_RELEVANCE_PROVEN_FAMILY_ASSIGNMENT_NOT_PROVEN` bei **364** Kandidaten.

Aktueller Status/NEXT ACTION ausschließlich in TEXT/CURRENT_STATE.md.


## DELTA 2026-10-03 – ZIELVERTRAGS-LANES NACH FRISCHEM NORMALPFAD

Aus 694 exakt eindeutigen Titeln und dem frischen 0.57.26-Normalpfad-Replay:

- A DIREKT PLANBAR: **0**
- B OHNE NEUE EXTERNE RECHERCHE REPARIERBAR: **0 aktuell bewiesen**
- C STRUKTUR-/MENSCHENENTSCHEIDUNG: **548**
- D GEPRÜFT PARKEN / NICHT PRODUZIEREN: **146**

D = frische Portalrelevanz nicht bewiesen; gemäß Zielvertrag ohne neue Evidenz parken.

C = Portalrelevanz vorhanden, aber der bestehende Pfad verlangt interne Klärung/Review. Besonders:
- 364 Familienzuordnungsfehler;
- davon frische Familienauflösung 345 NO_MATCH / 19 REVIEW_REQUIRED;
- bevorzugte Familienmitgliedschaft 0 PASS.

Daraus folgt ausdrücklich:
Keine manuelle Beitragsart-/Kategorieverteilung als Ersatzpfad. Zuerst konkrete C-Familien-/Strukturentscheidung, dann normaler Reentry.


## DELTA 2026-10-03 – NACHHALTIGE FAMILIEN-/STRUKTUR-REPARATUR / PSTE 0.57.28

Nutzeranforderung:
Keine Einmalreparatur nur für die aktuellen Begriffe. Die Lösung muss auch zukünftige Begriffe im bestehenden PSTE-Weg behandeln.

Lokaler Kandidat:
`PSTE-0.57.28-SUSTAINABLE-FAMILY-STRUCTURE-ROUTING-CANDIDATE.zip`

SHA-256:
`a8df7248f38eaf2b23ce1fe30020b6c0aa2aef1881be9fe107c12da07ae11c41`

Basis:
0.57.27 Produktwahl-Kandidat / `414b18f99e676516464790c842eedebc71a72a701c32bb95bd2d924d45ae9c79`.

Rootcause-/KISS-Reparatur:
1. Familienidentität:
   - deutsches End-`s` wird nicht mehr aus Doppel-`ss` abgeschnitten; dadurch `Gebiss ↔ Gebisse` korrekt;
   - ausschließlich konservative Verbflexionen `-t/-st` dürfen denselben vorhandenen Subject-Head treffen; dadurch z. B. `striegelt ↔ Striegel`;
   - beliebige unbekannte Kompositpräfixe bleiben verboten.
2. Familien-/Struktur-Routing:
   - nach Portalrelevanz-PASS und echtem Family-V2-`NO_MATCH` ohne sinnvollen bestehenden Familiennachbarn wird der Fall generisch `STRUCTURE_GAP`;
   - REVIEW/nahe bestehende Familie bleibt REVIEW;
   - keine neue Familie/Kategorie wird erzeugt, kein Gate umgangen.
3. Produktwahl:
   - vorhandene 0.57.27-Regel bleibt;
   - konservativer grammatischer Superlativ-Fallback ergänzt Fälle wie `sanfteste`, ohne Familiennomen wie `Pferdebürste` als Kriterium zu missdeuten;
   - im Normalpfad bleiben erkannte Produktwahl-Fälle `RETAINED_NON_PRODUCING`, solange downstream kein Produktwahl-Regelsatz registriert ist.

Exakter Delta 0.57.27 → 0.57.28:
- geändert `class-pste-family-identity-v2.php`;
- neu `class-pste-family-structure-router.php`;
- geändert `class-pste-normal-metadata-path.php`;
- geändert `class-pste-product-choice-classifier.php`;
- geändert `portal-seo-topic-engine.php`;
- sonst unverändert.

Frische lokale Hardtests:
- ZIP PASS;
- Fresh-Unpack PHP **81/81 PASS**;
- 694er realer Read-only-Replay: **320 STRUCTURE_GAP / 371 SANDBOX_REQUIRED / 3 RETAINED_NON_PRODUCING / 0 NORMAL_PASS**;
- 694/694 Write-Flags false;
- bestehende Family-MATCH-Regressionen: **0**;
- zusätzliche konservative Family-Matches: **3**;
- Strukturrouter Zukunfts-/Positiv-/Negativmatrix: **6/6 PASS**;
- Produktwahl Positiv/Negativ: **14/14 PASS**;
- 326er realer Sandboxbestand Produktwahl: **0 MATCH / 326 NO_MATCH**;
- geschützte Repository-/Storage-/Admin-/Provider-/Titel-/Intentpfade gegenüber 0.57.27 unverändert.

Bedeutung:
Der frühere Schritt „364 Familienfälle einmalig von Hand entscheiden“ ist als alleinige Lösung supersediert. 0.57.28 repariert die wiederkehrende Systementscheidung: echte bestehende Familie → konservativ matchen; vorhandene Nähe/Mehrdeutigkeit → REVIEW; keine bestehende semantische Nachbarfamilie bei bewiesener Portalrelevanz → STRUCTURE_GAP. Die anschließende Strukturentscheidung bleibt zielvertragsgemäß menschlich und läuft danach über normalen Reentry.

Grenze:
0.57.28 ist lokal HARD-PASS, aber noch **nicht live installiert**. Keine Release-/Live-Aussage vor WordPress-Readback.


## DELTA 2026-10-04 – AKTIVER EINZELLAUF BLOCKIERT BESTANDSAUFBEREITUNG / 0.57.29 UI-GUARD

Realer 0.57.28-Live-Screenshot:
- Version 0.57.28 aktiv;
- Start Bestandsaufbereitung endet mit `PSTE_RESEARCH_JOB_ALREADY_ACTIVE`.

Codebefund:
`PSTE_Breadth_Research_Queue::startExistingOnly()` blockiert korrekt, sobald `PSTE_Research_Job::peek()` einen aktiven Einzellauf liefert. Parallelität bleibt damit fail-closed.

Der eigentliche neue Fehler ist UI-seitig:
`renderExistingCandidateOverview()` zeigte den Startbutton auch bei aktivem Einzellauf, weil dort nur Storage- und Breadth-Zustände berücksichtigt wurden.

0.57.29 repariert ausschließlich diese Sicht-/Routinglücke:
- aktiven Einzellauf read-only prüfen;
- Startbutton bei aktivem Einzellauf nicht rendern;
- Status/Phase/Fortschritt anzeigen;
- direkter Link auf `Einstellungen` zum vorhandenen Lauf;
- bei ungültigem Jobzustand ebenfalls fail-closed statt Startbutton.

Kandidat:
`PSTE-0.57.29-ACTIVE-JOB-GUARD-CANDIDATE.zip`
SHA-256 `e5baf380157236103a5c15c0cee8da2c750daef207cd4fe9efef6f9791e7f880`.

Tests:
- PHP 81/81 PASS;
- UI-Guard Positiv/Negativ 5/5 PASS;
- exakt 2 Dateien geändert;
- keine Fach-/Research-/Storage-/Provider-/Normalpfadänderung.


## DELTA 2026-10-04 – SANDBOX-DATAFLOW-V2 ROOTCAUSE / PSTE 0.57.30

Live-Fehler:
`PSTE_DRIVER_REPEATED_SYSTEM_FAILURE:PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT`
bei gespeichertem Einzellauf `PAUSED_ERROR`, Abschluss `SANDBOX_BATCH 0/15`.

Rootcause frisch lokal reproduziert:
`fromNormalPath()` berechnete für V2 die Hashes der echten Record-Komponenten. `applyToRecord()` schrieb diese Komponenten aber nur für den Legacy-Vertrag auf den Record. Dadurch entstand bei neuen V2-Admits ein Record mit leeren Portal-/Nearest-/Exclusion-Feldern und gleichzeitig Hashes der echten Komponenten im `sandbox_dataflow`. Der vorhandene Self-Consistency-Guard blockierte deshalb korrekt.

0.57.30:
- transportiert die V2-Komponenten ausschließlich transient vom Producer zu `applyToRecord()`;
- validiert sie vor Persistenz gegen die bestehenden Hashes;
- speichert sie genau einmal auf dem Record;
- entfernt den transienten Transport vor Speicherung des kompakten `sandbox_dataflow`;
- alle Drift-Gates bleiben unverändert aktiv.

Kandidat:
`PSTE-0.57.30-SANDBOX-DATAFLOW-ROOTFIX-CANDIDATE.zip`
SHA-256 `c2f0e9e05f2ffddeea2c7ee022dd18ad04f9f5820ebbab4eabfab1253c235aa4`.

Tests:
- 0.57.29 Vorher-Negativtest: exakter Portal-Component-Drift reproduziert;
- 0.57.30 Positivtest PASS;
- absichtliche nachträgliche Komponentenmutation weiterhin BLOCK;
- UI-Guard 5/5 PASS;
- PHP 81/81 PASS;
- ZIP PASS;
- exakt 2 Dateien geändert;
- fachliche Familien-/Produktwahl-/Normalpfadlogik unverändert.

Live-Readback 0.57.30 noch offen.


## DELTA 2026-10-04 – 0.57.30 RESUME-PFAD NEGATIV / 0.57.31 REPLAY-SAFE-RECOVERY

Nach Nutzerforderung wurde nicht nur der Contract-Fix, sondern der **tatsächliche UI→AJAX→Driver→Job-Pfad lokal simuliert**.

Originalbezeichnung:
`Gespeicherten Block erneut prüfen`.

Befund 0.57.30:
Der Button ruft `pste_research_advance`; dessen Handler kickt nur den Driver. Der Driver sah den gespeicherten Einzellauf als `PAUSED_ERROR` und parkte ihn direkt als `SINGLE_PARKED`, ohne den reparierten lokalen FINALIZE-Schritt erneut auszuführen. Lokale Simulation: current=0 / advance=0 / park=1. Deshalb ist 0.57.30 als Live-Kandidat verworfen.

0.57.31:
- `PSTE_SANDBOX_DATAFLOW_PORTAL_COMPONENT_DRIFT` wird exakt als replay-sicherer lokaler FINALIZE-Code ergänzt;
- der Driver lässt vor dem bisherigen Park-Fallback `PSTE_Research_Job::current()` den bereits vorhandenen sicheren Recovery-Pfad ausführen;
- wird der Job dadurch RUNNING, läuft der normale Driver weiter;
- bleibt er PAUSED/UNKNOWN, greift unverändert das bisherige Park-Fallback.

Lokale Positiv-/Negativmatrix:
- sicherer aktueller Driftfehler: Recovery 1 / Advance 1 / Park 0 = PASS;
- absichtlich unsicherer Providerfehler: Recovery-Check 1 / Advance 0 / Park 1 = FAIL-CLOSED PASS;
- Sandbox-Dataflow-Contract-Fix aus 0.57.30 bleibt PASS;
- absichtliche Komponentenmutation bleibt BLOCK;
- PHP 81/81 PASS.

Kandidat:
`PSTE-0.57.31-REPLAY-SAFE-LOCAL-FINALIZE-RECOVERY-CANDIDATE.zip`
SHA-256 `35f670fc8a44310b1cb858764e506b0af950ac3941790bb1f5ee93e4a4270430`.

0.57.31 noch nicht live installiert.


## DELTA 2026-10-04 – REALER 695ER VERGLEICH / 0.57.32 PERSISTENCE-ROOTFIX

Realer Exportvergleich:
- 0.57.26: `pste-global-seo-topic-map-20261003-194321-utc.json`;
- 0.57.31: `pste-global-seo-topic-map-20261004-074909-utc.json`;
- 4472 Kandidaten in beiden Dateien;
- exakt dieselben 695 `PSTE_STORED_SOURCE_TITLE_CANDIDATE_V1`-Kandidaten;
- **695/695 vollständig unverändert**.

Rootcause:
`reanalyzeRetainedBacklogBatch()` verwirft bei bereits vorhandenem Titel und erneutem Normalpfad-Nicht-PASS das frisch berechnete Payload. Dadurch konnte 0.57.28/31 intern STRUCTURE_GAP/REVIEW/Productwahl-Hold berechnen, ohne dass diese neue Klassifikation für die 695 gespeichert wurde.

0.57.32:
- persistiert ausschließlich fail-closed Revalidierungszustände bereits vorhandener Titelkandidaten;
- Originaltitel und Titelkandidaten-Evidenz unverändert;
- production_title leer;
- Compiler blockiert;
- Raw-Source-Invariant hart;
- NORMAL_PASS-Misrouting hart blockiert;
- zusätzliche UI-Zähler für Revalidierung statt irreführender alleiniger „neue Titel“-Metrik.

Kandidat:
`PSTE-0.57.32-TITLE-CANDIDATE-REVALIDATION-PERSISTENCE-CANDIDATE.zip`
SHA-256 `c021ed852d89b6ae87fb4b6e347f49e6a0906b512671951044ea9a55ee06f772`.

Lokale Tests:
PHP 81/81 PASS; ZIP PASS; Positiv/Negativ-Revalidation PASS. Normal-Metadata-Pfad hashidentisch zu 0.57.28; erwartete 694er fachliche Verteilung bleibt 320 STRUCTURE_GAP / 371 SANDBOX_REQUIRED / 3 RETAINED_NON_PRODUCING.

Live-Readback offen.


## DELTA 2026-10-04 – VOLLSTÄNDIGE A/B/C/D-BESTANDSKLASSIFIZIERUNG NACH 0.57.32

Basis:
- realer 0.57.32-Export `pste-global-seo-topic-map-20261004-082759-utc.json`;
- 695 persistierte Titelkandidaten;
- 694 exakt eindeutige Titel;
- keine neue Provider-/DataForSEO-Recherche.

Ergebnis für die 694 eindeutigen Titel:
- A DIREKT PLANBAR: **0**;
- B OHNE NEUE EXTERNE RECHERCHE REPARIERBAR: **110**;
- C STRUKTUR-/MENSCHENENTSCHEIDUNG: **389**;
- D GEPRÜFT PARKEN / NICHT PRODUZIEREN: **195**.

B = 110:
- 92 vorhandene Familie + vorhandener Titel; redaktionelle Relation aus vorhandenem Bestand bestätigbar, danach normaler Reentry;
- 9 sichere bestehende Familienbindungen aus dem aktuellen Portalbestand;
- 9 konkrete Artikeltyp-/Zielkategorieentscheidungen mit bereits vorhandener Kategorie.

C = 389:
- 269 STRUCTURE_GAP ohne sicheren `structural_context_hint`;
- 51 STRUCTURE_GAP mit vorhandenem `structural_context_hint`;
- 33 Familienzuordnungen ohne sichere aktuelle Bindung;
- 34 redaktionelle Relationsentscheidungen;
- 2 klare Pferdehaftpflicht-Intentionen Kosten/Vergleich, für die in dieser Familie die entsprechende Typkategorie fehlt.

D = 195:
- 145 eindeutige Titel wegen fehlender realer externer Relevanzevidenz weiter geparkt;
- 46 Head-/Keyword-/Transaktionsvarianten `DISCOVERY_ONLY`;
- 1 nicht-redaktioneller Off-topic-Fall;
- 3 Produktwahl-Fälle weiter `RETAINED_NON_PRODUCING`.

Dublette:
`Schritt für Schritt Pferdebürsten waschen` liegt physisch zweimal vor; logisch nur einmal führen, keine automatische DB-Löschung.

Persistierte Entscheidungsartefakte:
- `/Pferdeatelier/PSTE-05732-EXISTING-EVIDENCE-DECISIONS-2026-10-04.json`
- `/Pferdeatelier/PSTE-05732-LANE-B-110-DECISIONS.json`

Die Artefakte erteilen keine Produktionsautorität. Zielvertragsgemäß folgt für B ausschließlich der vorhandene Review-/Normal-Reentry-Weg; kein neues Plugin und keine neue Architektur.


## DELTA 2026-10-04 – WORDPRESS-SAFE GENERISCHE BESTANDS-REENTRY-REPARATUR / PSTE 0.57.33

Die Chat-seitige 110er Klassifikation bleibt ausdrücklich kein Apply-Paket. Operative Autorität bleibt WordPress/PSTE.

Kandidat:
`PSTE-0.57.33-WORDPRESS-SAFE-EXISTING-TOPIC-REENTRY-CANDIDATE.zip`
SHA-256:
`57803212686b7256cf26994bbb25be913c39c757753b9dab92c5e37c34ae1e1b`

KISS-Delta:
- keine neue Architektur, kein neues Plugin, keine zweite DB, kein Chat-Import;
- konservative Portalidentitäts- und Family-V2-Semantik im bestehenden Normalpfad;
- zusätzliche Qualifier bleiben REVIEW;
- reine Familienkopf-/Keywordvarianten ohne Artikelintent werden fail-closed RETAINED_NON_PRODUCING;
- gespeicherte Titel werden nur über die bestehende Title-Pipeline revalidiert;
- Frageerkennung, Target-Keyword-Familiensemantik und Titelqualitätsguards generisch nachgezogen.

Exakter 695er Zielkohorten-Replay:
- vorher: 320 STRUCTURE_GAP / 372 SANDBOX_REQUIRED / 3 RETAINED_NON_PRODUCING / 0 NORMAL_PASS;
- 0.57.33 lokal: 320 STRUCTURE_GAP / 354 SANDBOX_REQUIRED / 19 RETAINED_NON_PRODUCING / 2 NORMAL_PASS.

Neue NORMAL_PASS:
- `Wie striegelt man Pferde am besten?` → Striegel / FAQ / Kategorie 67;
- `Muss man unter ein Reitpad eine Schabracke tragen?` → Schabracken / FAQ / Kategorie 84.

Negativmatrix:
- Decke-unterm-Sattel bleibt REVIEW, keine Unterdecken-Autozuordnung;
- Dressur-Qualifier bleibt REVIEW;
- Balance-Pads-Grammatik bleibt blockiert;
- Stützräder-Titelqualität bleibt blockiert;
- `Pferde Schabracken waschen` bleibt REVIEW;
- falscher Titelkandidatenvertrag bzw. vorhandene Produktions-/Familienautorität verhindert den speziellen Stored-Title-Revalidation-Pfad;
- nicht-fragender unbelegter Superlativ bleibt blockiert.

Tests:
- PHP 81/81 PASS;
- Fresh-Unpack PHP 81/81 PASS;
- ZIP PASS;
- vollständiger 695er Zielkohorten-Replay;
- kein 4472er Vollpool-PASS behauptet, da dieser lokale Vergleich in ein Tool-Timeout lief.

Live-Readback 0.57.33 offen.


## DELTA 2026-10-04 – EXISTING-ONLY AUDIT-REUSE-FEHLER / PSTE 0.57.34

Live-Readback 0.57.33:
- Version 0.57.33 aktiv;
- Existing-Only-Lauf gestartet;
- sofort COMPLETE;
- 0 vorhandene Titelkandidaten neu geprüft;
- alle Revalidierungszähler 0;
- Abschluss EXISTING_POTENTIAL_EXHAUSTED_NO_PROVIDER_CALL.

Rootcause:
`startQueue()` konnte den alten vollständigen Retained-Backlog-Audit wiederverwenden. Die Audit-Hash-Semantik deckte die in 0.57.33 geänderten Normalpfad-Abhängigkeiten nicht vollständig ab. Deshalb wurde `local_backlog_complete` bereits beim Start gesetzt und der lokale Bestandslauf übersprungen.

0.57.34:
- Existing-Only (`provider_fallback_allowed=false`) darf einen vollständigen Audit-Receipt nicht mehr als Grund zum Überspringen des lokalen Bestands verwenden;
- providerfähige Produktionswellen dürfen einen gültigen Audit weiterhin wiederverwenden;
- sichere Cancel-Continuation bleibt unverändert möglich;
- kein neuer Provideraufruf, keine neue Architektur, keine Gate-Absenkung.

Kandidat:
`PSTE-0.57.34-EXISTING-ONLY-FORCE-REAUDIT-CANDIDATE.zip`
SHA-256:
`6e12c2a5f63f353ca93374252bdb0ea6e5dadd0a3e1f1bf9df305077a771568e`

Tests:
- PHP-Lint 81/81 PASS;
- ZIP PASS;
- exakt 2 Dateien geändert;
- Existing-only + valid audit => kein Reuse / Rescan PASS;
- providerfähige Welle + valid audit => Reuse PASS;
- providerfähige Welle + invalid audit => kein Reuse PASS;
- Cancel-Continuation bleibt PASS;
- 0.57.33-Normalpfad-Dateien gegenüber 0.57.34 byteidentisch.

Live-Readback 0.57.34 offen.


## DELTA 2026-10-05 – JOURNAL-/MAGAZIN-BESTANDSARTIKEL VERLIEREN IN DER PSTE-INVENTARANSICHT IHRE KATEGORIE

Realer Beleg:
- WordPress-Beitrag `Wie alt werden Pferde?` / Post-ID 15974 erscheint in der zentralen Themenkarte als `WORDPRESS / PUBLISH`, aber ohne Kategorie und ohne Artikeltyp.
- Im realen Export ist derselbe bestehende Beitrag in `closest_existing_matches` mit `category_name=""` vorhanden.
- Derselbe Themenkandidat besitzt gleichzeitig eine eindeutig belegte Journal-Zuordnung: Kategorie-ID 1486, `Pferdegesundheit verstehen`, Slug `pferdegesundheit-verstehen`, Artikeltyp `Journal`.

Exakte Rootcause im 0.57.38-Code:
- `PSTE_Snapshot::inventory()` liest zwar die WordPress-Kategoriebeziehungen, übernimmt aber nur Kategorien, die in `PSTE_Snapshot::structure()['items']` als reguläre Portal-/Produktionskategorien aufgelöst wurden.
- Journal-/Magazin-Kategorien werden dagegen über den separaten vorhandenen `PSTE_Article_Type_Extension_Router` gebunden.
- Eine gültige Journal-Kategorie wie ID 1486 kann deshalb für Kandidaten korrekt aufgelöst werden, während derselbe bereits veröffentlichte WordPress-Journalartikel im allgemeinen Inventar ohne Kategorie/Familie/Artikeltyp erscheint.
- Das ist kein fehlender WordPress-Beitrag und kein Beleg dafür, dass die Journal-Zuordnung des Kandidaten falsch ist; es ist eine Lücke im Read-only-Inventarmapping bestehender Artikel.

Folge:
- 0.57.38 behebt den PSERC-Plan-Abdeckungsfehler, aber **nicht** dieses Journal-Inventarmapping.
- 0.57.38 darf deshalb nicht als finaler Gesamtstand für die nächste Produktionswelle abgenommen werden.
- Der Fix muss den bestehenden WordPress-Inventarpfad so ergänzen, dass registrierte Artikeltyp-Erweiterungskategorien (aktuell Journal) als gültige bestehende Artikelkategorien gelesen werden, ohne sie künstlich in die normale Portal-/Produktfamilienstruktur umzubauen.
- Danach zwingend 1:1 lokal positiv/negativ gegen den realen Export und die echten bestehenden Journalartikel prüfen; keine neue Architektur und kein Vollabgleich nur wegen dieser Zuordnungslücke.
