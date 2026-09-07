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


---

# NULL-FREIHEIT / ZWANGSJACKE – HARTE SYSTEMGRENZE 2026-09-07

Unantastbar:
- genau **eine Tür pro Raum**;
- genau **ein dummer, fachblinder Wächter**;
- Chat/Codex hat **keine freie Workflow-, Routing-, State-, Qualitäts-, Prüf-, Publish- oder Ersatzentscheidungsbefugnis**;
- keine neue Capability, kein neuer Executor, kein zweiter Handoff-Weg, kein Parallelpfad;
- Fach-/Inhalts-/SEO-/Design-/Tabellen-/Link-/LanguageTool-/PPM-/PSERC-/PSTE-/Publish-Regeln bleiben unverändert.

Der gebundene Worker darf ausschließlich das erzeugen, was der **bereits gebundene Fachworkflow/Textmaschinenvertrag** als Arbeitsprodukt verlangt. Er darf niemals selbst festlegen, welcher Prüfer gilt, welche Evidence genügt oder wie ein PASS zu begründen ist.

**Harte Ableitung:** Ein Worker-geschriebenes `status=PASS`, `execution_performed=true`, beliebiger 64-Hex-`input_sha256` oder selbst erzeugter Stage-Proof darf niemals allein eine Qualitätsstufe freigeben.

## Exakt gebundene PPM-6.7.9-Prüfung – neue harte Befunde

Bytegenau geprüft wurde das in 107007 gebundene Paket:
`PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`
SHA-256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`.

### Finaler Artikelzustand

`PPM679_Normal_Draft_Pipeline::execute_plan()` übernimmt den in `production_plan_item.canonical_article.body_html` gebundenen Artikel über `PPM679_Content_Generator`, prüft dessen `content_hash` und führt `PPM679_Content_Validator::check()` auf diesem Inhalt aus.

**Positiv:** An dieser PPM-Außengrenze ist Paul F2 nicht reproduziert: PPM validiert den gebundenen finalen Artikelzustand und erzeugt keinen zweiten unabhängigen Artikeltext.

### Tabelle

Für `Beratung` verlangt der aktive Content-Validator eine Pflicht-Tabelle mit semantischer Mindeststruktur.

Zusätzlich existiert der aktive, separate `PPM679_Table_Hard_Rule_Validator` mit härterem Vertrag:
- Klasse `system-129-table comparison-table`;
- keine kollidierenden Inline-Border/Background-Regeln;
- Rendered-Style-Hardrules.

**Harter Negativbefund:** Entfernen der `system-129-table`-Klasse kann im normalen Draft-Content-Validator weiterhin PASSen, während `PPM679_Table_Hard_Rule_Validator::validate_source_html()` denselben Artikel korrekt BLOCKED meldet.

**Folge:** `table_contract` darf nicht durch einen generischen Worker-Proof ersetzt werden. Der vorhandene Hardrule-Validator muss die Autorität bleiben. Kein Tabellenregel-Fix, keine neue Tabellenlogik.

### Interne Links

Der normale Content-Validator prüft exakt die in `runtime_order.links` gebundenen `href`/Anchor-Paare im finalen Artikel.

Der separate `PPM679_WordPress_Link_Target_Validator` prüft zusätzlich reale Ziel-/Snapshotregeln.

Aber: sein aktuell im PPM-Paket fest gebundener `WORDPRESS_LINK_TARGET_SNAPSHOT_V1` ist ein historischer, G9-spezifischer Transport-Snapshot und **kein allgemeines Registry-Set für beliebige neue Artikel**.

Frühere echte Produktionspläne zeigen dagegen bereits den richtigen allgemeinen Datenvertrag pro Artikel:
- `link_bindings` mit Rolle, href, Anchor, section_id, target_type, target_status, hierarchy_path;
- `portal_link_registry`;
- `portal_link_registry_hash`.

**Folge:** Der Chat darf Links nicht frei wählen oder deren Gültigkeit selbst bestätigen. Die Linkauswahl muss aus dem bestehenden Fachworkflow kommen; die technische Schicht darf nur die bereits erzeugte Bindung/Provenienz mechanisch prüfen. Der G9-Spezial-Snapshot darf nicht als allgemeine Ersatzautorität missbraucht werden.

### LanguageTool

Frühere echte Produktionspläne enthalten bereits die benötigte nicht-freie Provenienz:
- Engine `LanguageTool 6.8 / Bestand 43`;
- `executed_commandline_jar_sha256`;
- Installations-/Manifest-SHAs;
- `input_sha256`;
- `raw_stdout_sha256`;
- `return_code`;
- Checked-Text-/Raw-Report-SHAs;
- eigenes Provenienzfile + SHA.

Der aktuelle PPM-Fixture-Builder kann dagegen synthetische LanguageTool-Evidence erzeugen, ohne LanguageTool real aufzurufen.

**Folge:** Der neue Liveblocker `BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING` ist kein Einzelfehler. Er beweist, dass die aktuelle Worker-Anweisung die echte bestehende LT-Provenienz nicht deterministisch bindet. Kein LT-Minifix; reale LT-Evidence muss aus der bereits bestehenden LT-Ausführung stammen.

### Design / Rendered DOM

`PPM679_Rendered_DOM_Validator` verlangt ausdrücklich:
- echten WordPress-Render;
- `post_id`;
- Readback-Content-Hash;
- reale Desktop-/Mobile-Captures;
- Evidence-Class `SERVER_USER_TRIGGERED_TEST`;
- Capture-Source `HTTP_RESPONSE_AFTER_WORDPRESS_RENDER`.

107007 verbietet gleichzeitig WordPress-Schreibvorgänge im aktuellen Lauf.

**Harter Befund:** Ein per Artikel in 107007 behaupteter `design_format`-PASS darf **nicht** so tun, als sei damit ein echter Rendered-DOM-PASS erbracht. Diese Evidence kann in diesem Zustand technisch nicht ehrlich entstehen.

Das bedeutet nicht, dass die Designregel geändert oder entfernt werden darf. Es bedeutet nur: die technische Stage-Bedeutung ist bisher nicht exakt genug gebunden und darf vom Chat nicht interpretiert werden.

## Präzisierte Systemursache

Nicht „Prüfer fehlen“.

Sondern:

**Die vorhandenen echten Prüfer/Evidence-Quellen sind im aktuellen 12-Stage-Handoff nicht eindeutig und modellunabhängig den Stage-Namen zugeordnet.**

Dadurch entstehen:
- Selbstbeglaubigung;
- falsche doppelte PASS-Wahrheiten;
- Spezialvalidator vorhanden, aber Hauptpfad ruft ihn nicht auf;
- Upstream-Evidence wird vom Worker neu behauptet;
- Stage-Name lässt offen, welcher Artefaktzustand / welche Evidence wirklich gemeint ist.

Das verletzt die Zwangsjacke.

## KISS-Ziel – ohne Architekturänderung

Keine neuen Straßen. Keine neuen Prüfer. Keine neuen Executor. Keine intelligente Wächterlogik.

Nur:

**Im bestehenden einen Handoff jeden Stage-Namen fest auf seine bereits vorhandene autoritative Evidence-Quelle binden.**

Der Wächter prüft ausschließlich mechanisch:
- erwartete Evidence-Art / Contract;
- exakte Batch-/Artikel-/Slot-/Beitragsart-Identität;
- exakten Input-/Output-Hash;
- vorhandenes echtes Artefakt;
- unveränderten Prüfer-/Regelpaket-Hash;
- PASS/FAIL des echten Prüfers.

Er interpretiert keine Fachregel. Der Chat wählt keinen Prüfer. Der Chat darf keinen Ersatz-PASS schreiben.

## 7-Punkte-Fix-Sperre – Update

1. Paul-Prüfung: **PASS**
2. Fehlerhistorie: **PASS**
3. letzter funktionierender Stand: **PASS**
4. Vor-/Nachstufen: **WEITGEHEND PASS; zwei Bedeutungsbindungen bleiben formal zu schließen:**
   - allgemeine aktuelle Link-Provenienzquelle im NEW-Fachworkflow;
   - exakte Bedeutung von `design_format` vor WordPress-Render vs. späterem Rendered-DOM-Gate.
5. wiederkehrende Fehlerklasse: **PASS / JA**
6. konsolidierter Positiv-/Negativtest: **NOCH NICHT**
7. unveränderte Qualität/Architektur/Sicherheit: **NOCH NICHT AM KANDIDATEN BEWIESEN**

Aktuell weiterhin:
`FIX_FORBIDDEN`


---

# PUNKT 4 VOLLSTÄNDIG GESCHLOSSEN – 2026-09-07

## A. NEW-Link-Provenienz – harter Istbefund

Aktueller `main`: `f14ccf187b94c4beab9a86d0c69144f792ba2f64`.

Die aktuelle Single-Door-Current-Action bindet je Item ausschließlich:
- `canonical_article_id`;
- `plan_slot`;
- `title`;
- `target_keyword`;
- `category`;
- `article_type`.

Der aktuelle Generation-1-`SOURCE_SNAPSHOT.json` enthält ebenfalls ausschließlich die fünf SEO-Felder je Artikel.

Das aktuelle H8-`PRODUCTION_PACKAGE.json` ist fachlich leer:
- `fact_pack_bundle.fact_packs=[]`;
- `production_plan.items=[]`;
- Workflow Release enthält nur Artikel-/Slot-Identitäten.

Im aktuellen STARTMASTER-/Single-Door-Code existiert **kein allgemeiner NEW-Link-Builder**, der aus diesen Eingaben deterministisch
- `runtime_order.links`;
- `quality_binding.link_bindings`;
- `portal_link_registry`;
- `portal_link_registry_hash`
materialisiert.

Der aktuelle PSERC-Bestand besitzt mit `PSERC_Portal_Structure_Gate` eine echte, hashgebundene Portalstruktur-Autorität. Diese validiert Kategorien/Historie/Struktur, wählt aber nicht die drei semantischen Artikel-Links.

Frühere echte Produktionspläne beweisen den beabsichtigten Datenvertrag:
- genau drei Rollen;
- konkrete href/Anchor/Abschnitt/Reason;
- Live-/Snapshot-Provenienz;
- Registry + Registry-Hash.

Sie sind **nur Historienbeleg** und für NEW keine zulässige Produktionsquelle.

### Schluss

**Aktuell fehlt die deterministische Bindung der bereits bestehenden Fachworkflow-Linkentscheidung an die Current Action.**

Der Worker müsste die drei Links heute selbst auswählen.
Das verletzt die Null-Freiheit-Hardrule.

Kein alter Artikel/Plan darf als Ersatzquelle benutzt werden.
Keine neue Linklogik darf erfunden werden.

Status:
`CURRENT_NEW_LINK_BINDING = BLOCKED_MISSING_EXISTING_DETERMINISTIC_BINDING`

---

## B. design_format – harter Istbefund

Die Stage `design_format` wurde im technischen 12-Stage-Set erstmals als **bloßer Name** eingeführt.

Beim ursprünglichen Handoff gab es für diese Stage:
- keinen fest benannten Validator;
- keinen eigenen Evidence-Contract;
- keinen festgelegten Input-Artefaktzustand;
- keine Abgrenzung Source-Format vs. WordPress-Render.

Der Handoff prüfte ursprünglich lediglich Stage-Datei + Hash; später generische `execution_performed=true`-Evidence.

### Bestehende PPM-Prüfer zeigen zwei verschiedene Ebenen

**Source-/Pre-WordPress:**
- Content-/Structure-Gates;
- `PPM679_Table_Hard_Rule_Validator::validate_source_html()`;
- artikelgebundene Link-/Strukturprüfungen.

**Post-WordPress-Render:**
`PPM679_Rendered_DOM_Validator` verlangt zwingend:
- reale `post_id`;
- Readback-Content-Hash;
- echten HTTP-Render;
- Desktop + Mobile Capture;
- `SERVER_USER_TRIGGERED_TEST`;
- `HTTP_RESPONSE_AFTER_WORDPRESS_RENDER`.

Der 107007-Arbeitsbereich verbietet reale WordPress-Schreibvorgänge und läuft PPM in isolierter Runtime/Fixture-Umgebung.

Daher ist bewiesen:

**Ein 107007-`design_format`-PASS kann nicht ehrlich einen echten Rendered-DOM-PASS bedeuten.**

Der vorhandene lokale Drei-Typ-Source-Validator ist ebenfalls **keine Produktionsautorität**:
- ausdrücklich local/test-only;
- keine WordPress-Runtime;
- kein LT-PASS;
- kein Produktionsrelease.

Er darf nicht heimlich zum neuen Produktionsprüfer gemacht werden.

Der dauerhaft gespeicherte alte 7er-Endstempel enthält ebenfalls:
- keine `design_format`-Evidence;
- keinen Rendered-DOM-Nachweis;
- keine heutige System-129-Tabellenbindung.

### Schluss

`design_format` besitzt im aktuellen 107007-Vertrag **keine ausreichend definierte bestehende technische Evidence-Semantik**.

Eine neue Bedeutung heute festzulegen wäre eine Vertrags-/Autoritätsdefinition und unter aktuellem Scope nicht zulässig.

Status:
`CURRENT_DESIGN_FORMAT_BINDING = BLOCKED_UNDEFINED_EXISTING_STAGE_AUTHORITY`

---

# 7-PUNKTE-FIX-SPERRE – ENDSTAND DER READ-ONLY-PRÜFUNG

1. Paul-Prüfung: **PASS**
2. gesamte Fehlerhistorie: **PASS**
3. letzter funktionierender Stand: **PASS**
4. Vor-/Nachstufen vollständig bestimmt: **PASS – inklusive Nachweis der beiden fehlenden/undefinierten Bindungen**
5. wiederkehrende Fehlerklasse: **PASS / JA – K1/K2/K3/K4 systemisch**
6. konsolidierter Kandidat positiv/negativ: **NICHT ZULÄSSIG VORBEREITBAR**, solange bestehende Link- und design_format-Autorität nicht vorhanden/eindeutig gebunden ist
7. Null-Freiheit + Qualität + Architektur unverändert: **würde durch jede frei erfundene Ersatzdefinition verletzt**

## Entscheidung

`FIX_FORBIDDEN`

Nicht wegen fehlender Analyse, sondern weil die Analyse zwei echte Vertragslücken bewiesen hat, die unter den derzeitigen Hardrules **nicht durch eine bloße technische Hash-/Pfadkorrektur gelöst werden können**.

### Verbotene Scheinlösungen

- Codex Links wählen lassen;
- alte Linklisten aus früheren Artikeln wiederverwenden;
- G9-Spezial-Link-Snapshot generalisieren;
- lokalen Drei-Typ-Testvalidator zur Produktionsautorität erklären;
- `design_format` eigenmächtig als Source- oder Render-PASS definieren;
- Rendered-DOM-PASS ohne echten WordPress-Render behaupten;
- Stage entfernen;
- Prüfer abschwächen;
- neuen Executor/Capability/Runner/zweite Tür bauen.

### Einzige scope-konforme nächste Frage

Nicht „Wie bauen wir einen neuen Prüfer?“

Sondern:

**Existiert außerhalb des aktuell gebundenen STARTMASTER-Pfads bereits eine autoritative, unveränderte Fachworkflow-Quelle, die für NEW exakt**
1. die drei artikelbezogenen Linkbindungen erzeugt und
2. die Bedeutung/Evidence von `design_format` definiert?

Nur wenn diese bestehende Quelle gefunden wird, darf sie technisch an die vorhandene eine Straße zurückgebunden werden.

Wenn sie nicht existiert:
**BLOCKED statt Architektur-/Fachänderung.**
