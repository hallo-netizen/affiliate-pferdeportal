# TEXT / STARTMASTER0107 – TECHNICAL CORRIDOR MATRIX – 2026-09-07

## Zweck

Einmalige technische Wirkungskarte der 12 bestehenden Pflichtstufen.

**Keine neue Architektur. Keine neue Qualitätslogik. Keine Codefreigabe.**

Grundfrage je Stufe:
1. Wo liegt die echte bestehende Fach-/Prüfautorität?
2. Welches konkrete Input-Artefakt / welcher Zustand wird geprüft?
3. Welcher echte Output / welche Evidence entsteht?
4. Wer konsumiert genau diesen Output?
5. Bindet 107007 das heute mechanisch oder lässt es Codex interpretieren?

## Historische Schlüsselbefunde

### Letzter realer 7/7-PASS
Auf `d841ed7590…` erzeugte Codex selbst im gebundenen Raum:
- frische Artikel;
- 12 Stage-Ergebnisse;
- 12 Stage-Proofs;
- FACHWORKFLOW_PASS;
- ITEM_RECEIPT.

Es existierte **kein separater Fachworkflow-Executor**.
Die Current Action ließ direkten Receipt-Submit zu.

Damit war die Strecke operativ erfolgreich, aber die reale Ausführung der Nicht-PPM-Stufen hing teilweise vom Worker-Verhalten ab.

### Danach
Ab 04.09. wurde PPM als einzige Stage mechanisch real ausgeführt:
`PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan`.

Dafür wurden:
- Fact-Pack;
- Production-Plan-Item/-Header;
- Workflow-Release-Kontext;
- Handoff-Request;
- exakte PPM-/PSERC-Pakete
zwingend.

Die anderen elf Stage-Proofs blieben dagegen generisch.

### Neuer LT-Livebefund
Auf aktuellem main `f14ccf1…` verweigerte Codex einen selbst erzeugten LanguageTool-PASS:
`BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING`.

Gleicher Current-Action-/Prompt-Grundtyp war zuvor bis B01 gelaufen.

**Beweis:** Die aktuelle 107007-Ausführung ist bei Nicht-PPM-Stufen nicht vollständig deterministisch.

---

# 12-STUFEN-AUTORITÄTSMATRIX

| Stufe | Echte bestehende Autorität | Echter Zustand / Evidence | heutige 107007-Bindung | Befund |
|---|---|---|---|---|
| research_fact_pack | bestehender approved Research/Text-Prozess hinter R_001 | aktueller Fact-Pack + Source-Hashes | Codex soll Fact-Pack erzeugen; kein separater ausführbarer Research-Weg mechanisch gebunden | **PARTIAL / K1+K3** |
| textmachine_article_type_structure | gebundener Fachprompt + Article-Type-Regelpaket | finaler Artikel / Struktur gegen festes Regelpaket | Prompt + Article-Type + Template-SHA sind gebunden; Codex erzeugt Text; Stage-PASS bleibt selbst erzeugter Proof | **PARTIAL / K3** |
| table_contract | bestehende Tabellenregel / PPM-Content-/DOM-Gates | gerenderter finaler Artikelzustand nach relevanter Transformation | äußerer Stage-Proof generisch; PPM prüft später eigenen finalen Zustand | **DOPPELTE WAHRHEIT / K2+K3; Paul F7/A7 relevant** |
| internal_links | bestehender Fachworkflow + Link-Bindings/Resolver | Artikel vor/nach Linkauflösung; historisch `link_bindings` | äußerer Stage-Proof generisch; exakte heutige Pre-/Post-Resolver-Bindung nicht mechanisch nachgewiesen | **OPEN / K2+K3; Paul A13/A16 relevant** |
| languagetool | **LanguageTool 6.8 / Bestand 43** | Checked-Text-SHA + Raw-Report-SHA + Returncode + Findings + Tool-Provenienz | echter historische Executor identifiziert/reproduziert, aber in Current Action/Capsule nicht gebunden | **CURRENT_BINDING_MISSING / K1+K3** |
| ppm | PPM 6.7.9 über PSERC-PM Intake Bridge | final article SHA + echter PPM Report + content_hash | **mechanisch real ausgeführt und hashgebunden** | **PASS-BINDUNG** |
| pserc | PSERC ist real Teil des PPM-Bridge-Korridors und besitzt eigene Compiler-/Release-Prüfungen | PSERC Bridge-/Metadata-/Release-Ergebnis | reale PSERC-Ausführung existiert innerhalb PPM; separater äußerer `pserc`-Stage-Proof bleibt generisch | **DUPLIKAT/SEMANTIK UNKLAR / K3** |
| pste | PSTE 0.56.25 / SEO-Planungsstrecke | Planning-/Title-/Cannibalization-/Readiness-Evidence | echte Upstream-Komponente vorhanden; 107007 verlangt trotzdem generischen neuen Stage-Proof | **FALSCHE LIFECYCLE-ZUORDNUNG MÖGLICH / K2+K3** |
| duplicate_cannibalization | Upstream PSERC/PSTE / Existing-Content-Inventar | Original-Snapshot zeigt separate Duplicate-Gates und reale Blocks | 5-Felder-Projektion bindet Snapshot/Manifest nur technisch; Fach-Evidence wird nicht in 107007 mechanisch referenziert; Codex soll erneut Proof erzeugen | **UPSTREAM PASS NICHT DIREKT EVIDENCE-GEBUNDEN / K3+K4** |
| seo | Upstream SEO/PSERC; exakt fünf Felder | READY-Metadaten + Metadata Boundary PASS | fünf Werte + Batch sind hart gebunden; 107007 darf keine neue SEO-Entscheidung treffen; separater Stage-Proof ist generisch | **BINDUNG VORHANDEN, STAGE-PROOF SEMANTISCH DOPPELT / K3** |
| design_format | bestehende PPM DOM-/Design-Gates | gerenderter finaler Artikelzustand | historisch echte PPM-Design-Gates belegt; äußerer Design-Stage-Proof generisch | **DOPPELTE WAHRHEIT / K3; Paul F2/A2/A3 relevant** |
| publish_safety | Runtime Entry / Output Quarantine / Final Review / PPM publish=false | feste State-/Visibility-/Release-Receipts | reale äußere Guards sind vorhanden; Worker erzeugt zusätzlich generischen `publish_safety`-Proof | **DOPPELTE WAHRHEIT / K3** |

---

# WICHTIGE ERKENNTNIS

Die 12 Namen bilden **keine homogene lineare Liste von 12 Worker-Jobs**.

Sie umfassen mindestens vier Autoritätsarten:

## A – Upstream bereits entschieden
- SEO
- PSTE/Planung
- Duplicate/Cannibalization

## B – Fachworkflow erzeugt den Artikelinhalt
- Research/Fact-Pack
- Textmaschine/Artikeltyp
- interne Links

## C – reale gebundene Fach-/Tool-Prüfer
- LanguageTool
- PPM
- PSERC
- Tabellen-/Designprüfungen innerhalb der fachlichen Prüfkette

## D – äußere technische Sicherheitsgrenzen
- Publish-Safety

**Systemischer Fehler:** Der aktuelle 107007-Vertrag behandelt diese verschiedenen Verantwortungen zu stark so, als müsse Current Codex für jede Stufe selbst einen neuen „real ausgeführten“ PASS-Proof erzeugen.

Das erzeugt:
- Selbstbeglaubigungsrisiko;
- doppelte Wahrheiten;
- falsche Lifecycle-Zuordnung;
- Interpretationsspielraum;
- genau die von Paul gefundenen Pre-/Post-State-Konflikte.

---

# PAUL-GEGENCHECK

## F2 / A6 / A12
**BESTÄTIGT ALS FEHLERKLASSE.**
Stage-Namen allein reichen nicht. Für Table/Links/Design muss klar sein, ob Pre- oder Post-Transformation geprüft wird und welcher Zustand tatsächlich weitergegeben wird.

## F7 / A7
**AKTIV OFFEN.**
Kein Tabellen-Fix auf Verdacht.
Vor Integration muss geklärt sein, ob der aktuelle Beratungspfad die im PPM tatsächlich verlangte Tabellenbedingung technisch erfüllen kann.

## A11
**BESTÄTIGT ALS FEHLERKLASSE.**
Generische Hashfelder dürfen nicht verschiedene Artefaktzustände bedeuten.

## A37
**BESTÄTIGT ALS TESTWARNUNG.**
Ein Stage-Proof ist kein Ausführungsbeweis, wenn der echte Prüfer nicht gelaufen ist.

## F8 retracted
**SCHUTZREGEL.**
Keine bestehende Schicht entfernen, bevor ihre load-bearing Wirkung geprüft ist.

---

# FEHLERHISTORIE-GEGENCHECK

B01, B02, B03, B04, B07, B08, B09, B10, B11 und der neue LT-Befund passen alle in dieselben Übergabe-/Bindungsklassen.

Besonders wichtig:
- B04 wurde für **PPM** richtig geschlossen: kein behaupteter PASS, sondern echter Prüfer.
- B02 wurde nur teilweise geschlossen: Codex wurde als Worker gebunden, aber die einzelnen Prüfautoritäten wurden nicht eindeutig zugeordnet.
- B14 erklärt, warum generische Regressionen diesen Unterschied nicht zuverlässig zeigen.

Daher greift die Hobbyraum-Anti-Minifix-Regel:
**kein weiterer LanguageTool-Einzelfix.**

---

# LETZTER FUNKTIONIERENDER STAND

`d841ed…` / `de21f6…` beweisen:
- der 7er-Batch ist produzierbar;
- der gebundene Prompt / Artikeltyp funktioniert;
- der bestehende Fachworkflow konnte operativ 7/7 liefern.

Sie beweisen **nicht**, dass die Nicht-PPM-Ausführung schon damals vollständig mechanisch und modellunabhängig gebunden war.

Genau diese latente Lücke ist jetzt sichtbar.

---

# KISS-ZIEL – OHNE ARCHITEKTURUMBAU

Nicht:
- 11 neue Executor bauen;
- Qualitätsstufen entfernen;
- Wächter intelligent machen;
- neuen Workflow/Runner bauen.

Sondern:
**jede der bestehenden 12 Stufen nur an die bereits vorhandene echte Autorität binden.**

Prinzip:
1. bestehende Upstream-PASS-Evidence → nur hash-/statusgebunden referenzieren;
2. Codex erzeugt nur die echten Facharbeitsprodukte, die tatsächlich sein Auftrag sind;
3. LanguageTool → vorhandene echte LT-6.8-Ausführung;
4. PPM/PSERC/Table/Design → vorhandene echte Prüfresultate auf exakt definiertem Artefaktzustand;
5. Publish-Safety → vorhandene äußere Guards/Receipts;
6. FACHWORKFLOW_PASS wird erst aus diesen echten Evidence-Quellen materialisiert;
7. kein Stage-PASS darf mehr allein aus einem vom Worker geschriebenen `execution_performed=true` entstehen.

Das ist eine **Bindungsbereinigung im bestehenden Handoff**, keine neue Facharchitektur.

---

# 7-PUNKTE-FIX-SPERRE – AKTUELLER STAND

1. Paul-Prüfung gelesen: **PASS**
2. gesamte Fehlerhistorie geprüft: **PASS**
3. letzter funktionierender Stand verglichen: **PASS**
4. unmittelbare Vor-/Nachstufen geprüft: **PARTIAL – für Table/Links/Design und Upstream-Evidence noch endgültig zuzuordnen**
5. gleicher Fehler-Typ wie früher: **PASS / JA → Anti-Minifix aktiv**
6. Positiv + Negativ lokal: **NOCH NICHT – kein konsolidierter Kandidat gebaut**
7. Qualität/Inhalt/Design/Sicherheit unverändert: **ZIEL PASS, aber erst am Kandidaten beweisbar**

Aktuelle Entscheidung:
`FIX_FORBIDDEN`

Kein Produktionscode ändern, bis Punkt 4 vollständig und danach Punkt 6/7 am **einen konsolidierten Kandidaten** bestanden sind.
