# ACM – AKTUELLER ROUTENSTATUS / ABSCHLUSS- UND NACHHOLPRÜFUNG

Stand: 2026-09-09
Route: Alternative Central Machine (ACM)
Branch: `alternative/seo-text-central-machine-20260908`
PR: #195 (Draft)

## Autorität

Diese Datei ist die **einzige aktuelle Standwahrheit der ACM-Route** für:
- belastbaren Status
- offene ACM-Integrationsfehler
- NEXT ACTION
- verbindlichen Arbeitsweg

`00_MASTER_KONZEPTLOG.md` ist nur Wegweiser/Entwicklungslog.
Ältere P0–P57-Akten sowie `59_INTERFACE_TABOO_ENTRYPOINT_REASSESSMENT.md` sind Beweis-/Entscheidungsakten und keine zweite aktuelle Standwahrheit.

Die produktive Wahrheit bleibt separat und unverändert:
`control/startmaster0107/CURRENT_STATE.json`

Die produktive STARTMASTER-Fehlermatrix gehört zur parallelen Reparaturroute und wird von ACM nicht überschrieben:
`control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`

## AKTUELLER STAND

**ACM-PROTOTYP: PASS**
**PRODUKTIONSADOPTION: BLOCKED**

Letzter vollständig getesteter funktionaler ACM-Head:
`c6f38f0c1ad1c992f3738d83c342dfd9a5637272`

Ausgeführte Tests auf exakt diesem funktionalen Head:
- Alternative SEO Text P3 Isolated Lab – Run `34346471176` – SUCCESS – 61/61 Schritte abgeschlossen
- Alternative SEO Text P8 Signer Isolation Lab – Run `34346471175` – SUCCESS

Frisch geprüfter produktiver main:
`93ba987c56f7b08ffba009210e3012c036fec18d`

Frisch gelesener Produktionsstatus:
- `IMMUTABLE_BASE_HARDLOCK_ACTIVE_H8_PREPRODUCTION_OUTPUT_LOCKED`
- next_allowed_step: `RUN_NEW_ARTICLE_BATCH_NO_STOP`
- publish_allowed: false

Parallelroute:
- aktuelle bekannte Regressionen reichen bis M36
- ACM hat diese Wahrheit nicht verändert
- im ACM-Lauf wurden die ausgewählten relevanten historischen Seam-Fälle bis M36 gegen den aktuellen main wiederverwendet und bestanden
- kein Merge, kein Schreibzugriff auf main, kein CURRENT_STATE-Update

## ZIELBILD – EINFACH

`Redaktionsplan -> gebundener Fachworkflow/Codex -> Research/Fact-Pack -> unveränderte Textmaschine und alle Qualitätsgates -> PPM prepare(no write) -> eine signierte JSON -> WordPress prüft Signatur/Hashes vor dem ersten Write -> Entwurf -> Readback/DOM -> menschliche Sichtprüfung -> manuelle Freigabe`

Kein Auto-Publish.

## REDAKTIONSPLAN

Harte Prüfung PASS:
- realer SEO-Redaktionsplan-Snapshot ist gebunden
- Beitragsart, Kategorie, plan_slot, Target Keyword und Titel werden daraus übernommen
- plan_slot ist eindeutig
- plan_slot ist an canonical_article_id gebunden
- WordPress-Inventar für draft/publish/trash wird read-only abgeglichen
- systemweiter Dubletten-/Keyword-Ownership-Guard ist vorhanden
- bereits vorhandener regulärer Draft oder veröffentlichter Artikel blockiert stille Neuproduktion

Real gebundenes aktuelles Beispiel:
- canonical_article_id: `article:a8282e69ecd43b615de17eb1`
- plan_slot: `9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56`
- Titel: `Das Wichtigste über Hindernisstangen für Pferde`
- Target Keyword: `Hindernisstangen für Pferde`
- Kategorie: `hindernisstangen-beratung`
- Beitragsart: `Beratung`

## TEXTMASCHINE / CODEX / CHAT

Unverändert:
- Textmaschine
- Research-/Fact-Pack-Regeln
- Artikeltyp-/Strukturregeln
- Tabellen
- interne Links
- SEO/Target Keyword
- LanguageTool-Vertrag
- PPM
- PSERC
- PSTE
- Dubletten-/Kannibalisierungsschutz
- Design/DOM/Readback
- Publish-Sicherheit

Chat/KI:
- keine Workflow-/Navigations-/State-/Publish-Autorität
- keine freie Route
- keine freie Validatorwahl
- keine freie Workerwahl
- keine freie Reparaturroute

Codex:
- nur gebundener Fachworkflow-Worker
- darf Fachprodukte für das gebundene Item erzeugen
- darf PASS/PUBLISH nicht frei bestimmen

## CLAUDE – DAUERHAFTE ENTSCHEIDUNG

Claude gehört **nicht** zum ACM-Zielsystem.

Grund:
Claude war ausschließlich externe Zusatzberatung und hatte keine strukturelle Workflowfunktion.

Folge:
- keine Claude-Abhängigkeit in ACM
- kein Claude-Reviewer als Pflicht
- keine Claude-Freigabe
- kein Claude-Gate
- normaler Beratungspfad ist mit LanguageTool + bestehendem Content Validator ohne Claude PASS bewiesen

Im unveränderten historischen PPM existiert noch ein explizit aktivierbarer alter Sonderzweig mit Claude-Bezeichnung.
Er ist im normalen Beratungspfad nicht aktiv und wird von ACM nicht gebunden.
Nur wegen dieses historischen Namens wird die Textmaschine/PPM **nicht** verändert.

## LANGUAGETOOL

Vertrag/Qualitätsweg: PASS.
- `LanguageTool 6.8 / Bestand 43`
- Raw Evidence gebunden
- 0 ungelöste Findings
- normaler Beratungspfad ohne Claude PASS

Nachholbefund:
Im Repository ist aktuell **kein ausführbarer LanguageTool-Runtime (JAR/Runner) gebündelt**.
Vor unbeaufsichtigter Vollautomatik muss die bereits fest gehashte LanguageTool-6.8-Abhängigkeit reproduzierbar bereitgestellt/gebunden sein.
Keine neue Architektur und kein Fallback-Provider.

## DATEI / SIGNATUR

Ziel-Enddatei:
`PFERDE_ATELIER_SIGNED_ARTICLE_BATCH_FINAL.json`

Eigenschaften:
- Artikelzahl nicht im Dateinamen
- tatsächliche article_count dynamisch im Manifest
- vorhandener allgemeiner Endstempel wird wiederverwendet
- privater Ed25519-Schlüssel bleibt beim externen/GitHub-Signer
- WordPress besitzt nur den vertrauenswürdigen Public Key
- falsche Signatur/Schlüssel/Batch/Dateien/Replay/Manipulation => BLOCK
- import failure => 0 committed writes

## WORDPRESS-SEAM

Isolierter technischer Beweis: PASS.

`ACM_SINGLE_SIGNED_JSON_WORDPRESS_SEAM_PASS`:
- vorhandener `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`
- genau eine JSON
- Signaturprüfung vor Write
- vorhandener Fact-Pack-Import
- vorhandene Normal-Draft-Pipeline
- exakt ein Draft
- Readback PASS
- Publish-Zahl unverändert
- 14 gezielte Negativtests BLOCK
- keine neue Importlogik
- kein neuer Paketvertrag

KISS-Fixes auf dem Weg:
1. WordPress-Kandidat musste vorhandene Fact-Pack-Bindung `production_plan.source_snapshot_id -> fact_pack.fact_pack_id` verwenden.
2. Negativtest musste den realen Fact-Pack-Pfad `claims[].statement` statt erfundenem `facts[].claim` verwenden.
3. Kanonische JSON-Prüfung musste Objekt-/Listenidentität erhalten.
4. LanguageTool-Inventar darf gespeicherte JSON/TXT-Evidence nicht als ausführbare Runtime zählen.

Diese Punkte waren Test-/Adapterannahmen, keine neue Facharchitektur.

## OFFENE ACM-INTEGRATIONSFEHLER / BLOCKER

### ACM-WP-01 – echte One-JSON-WordPress-Runtime-Anbindung fehlt
Audit:
- `single_final_signed_json_wp_upload_wired=false`
- vorhandener Verifier und isolierter Seam funktionieren
- aber kein echter WordPress-Admin-/Runtime-Handler ruft den Verifier derzeit vor dem Import auf

**Status nach Schnittpunkt-Neubewertung: `BLOCKED_BY_INTERFACE_TABOO`**

Frisch geprüft:
- `WORDPRESS_SIGNATURE_ENTRY_LOCK_V1` erlaubt Verification-only und verbietet `IMPORT_LOGIC_CHANGE` sowie `WORKFLOW_ARCHITECTURE_CHANGE`
- vorhandener `production_package_release_gate.py` prüft die vollständige Produktionspaket-Datei, endet aber vor WordPress
- vorhandener WordPress-Endstempel-Verifier und vorhandener Normal-Draft-Import besitzen unterschiedliche bestehende Eingangsverträge
- eine direkte bereits verdrahtete One-JSON-Runtime-Schnittstelle existiert nicht

Folge:
- WP-01 bleibt Produktionsadoptionsblocker
- in ACM kein Wrapper, kein neuer Handler, kein neuer Importer und kein neues Übergabeformat
- der Schnittpunkt wird nicht verändert oder umgangen

### ACM-WP-02 – kontrollierter manueller Publish-/Freigabeweg nicht nachgewiesen
Audit:
- `manual_publish_release_wired=false`
- Draft-only-Kern ist vorhanden
- Nutzerreview ist vorgesehen
- der anschließende kontrollierte manuelle Freigabepunkt ist im Repo noch nicht als gebundener Weg bewiesen

### ACM-LT-01 – ausführbarer LanguageTool-Runtime nicht im Repository gebunden
- Vertrags-/Evidence-Seite vorhanden und PASS
- ausführbarer Runtime-Kandidat: 0
- vor unbeaufsichtigter Vollautomatik zu schließen

### ACM-ADOPT-01 – Produktions-Zielvertrag noch nicht versioniert/adoptiert
- ACM-Kandidat positioniert externe Signatur vor dem ersten WordPress-Draft-Write
- produktiver Zielvertrag wurde bewusst nicht verändert
- Adoption erst nach ausdrücklichem kontrolliertem Produktionsentscheid

### ACM-REAL-01 – echter workflow-produzierter Artikel-Handoff noch nicht vollständig durch ACM-Endkette gelaufen
- echter aktuelle Einstieg/Item ist gebunden
- Fixture-/isolierter Komplettweg ist PASS
- real erzeugtes Fact-Pack + Production-Plan + LanguageTool-Evidence des aktuellen Hindernisstangen-Items bis zur finalen signierten JSON/WordPress-Runtime ist noch offen

## AUFGELÖSTE FEHLER DIESES ARBEITSBLOCKS

Keine davon ist ein neuer Produktionsfehler:
- P47 erwartete falsche generische PASS-Strings -> Testannahme korrigiert
- Echt-Einstieg-Probe: fehlender vorgeschalteter offizieller Preflight -> vorhandenen Preflight wiederverwendet
- Echt-Einstieg-Probe: verschachteltes JSON falsch ausgewählt -> Parser korrigiert
- WordPress-Seam: falsche Fact-Pack-Feldbindung -> auf bestehenden `fact_pack_id`-Vertrag korrigiert
- Fact-Pack-Tampertest: erfundenes `facts`-Feld -> realen `claims`-Vertrag verwendet
- LanguageTool-Inventar: Evidence-Dateien fälschlich als Runtime gezählt -> getrennt
- keine neue Route/kein neuer Runner/kein neuer Signer/kein neuer Fachvertrag erforderlich

## UNABHÄNGIGER 7/7-ABNAHMETEST – HARD RULE

Für die harte ACM-Konzeptabnahme gilt:

- alle 7 Artikel vollständig neu von null erzeugen
- keine alten 7/7-Artikel als Produktionsquelle
- keine alten Fact-Packs
- keine alten Rechercheergebnisse
- keine alten JSON-/Proof-/Recovery-/Quarantäne-/Release-Artefakte als Produktionsquelle
- wiederverwendet werden ausschließlich die unveränderten bestehenden Regeln, Verträge, Gates und Schnittstellen
- erst NACH abgeschlossenem frischem Test dürfen die alten 7/7 als Vergleichs-/Goldstandard herangezogen werden
- der Vergleich darf den Nulltest nicht beeinflussen

Zweck:
Der Test soll beweisen, dass ACM unabhängig neue Artikel erzeugen und durch den gebundenen Workflow führen kann – nicht, dass vorhandene Artikel erfolgreich weiterverarbeitet werden.

Aktueller frischer Nulltest:
- Start über bestehenden permanenten Chat→Codex-Dispatcher PR #107
- Dispatcher-Head = current main `93ba987c56f7b08ffba009210e3012c036fec18d`
- vorhandener Codex-Cloud-Worker
- kein neuer Startweg
- keine Schnittstellenänderung
- keine Reparatur während des Tests
- Stop nur am ersten echten BLOCKED/USER_ACTION_REQUIRED oder bei 7/7-Ende
- kein Publish

## KORREKTUR NACH AUTORITATIVER ORIGINALWEG-ÜBERGABE / 12-STAGE-CORRIDOR

Frisch gegen die autoritativen TEXT-Quellen geprüft:
- `CURRENT_STATE.md`
- `HOBBYRAUM.md`
- `04_FEHLERLISTE_KOMPLETT_AKTUELL_20260905.md`
- `TECHNICAL_CORRIDOR_ROOTCAUSE_20260907.md`
- `TECHNICAL_CORRIDOR_MATRIX_20260907.md`
- `PAUL_PIPELINE_AUDIT_20260906.md`

### Harter Befund

Der aktuelle frische Nulltest-Stop
`BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING`
darf **nicht** als isolierter LanguageTool-Minifix behandelt werden.

Grund:
Der produktive 107007-Handoff verlangt 12 Stage-Proofs. Im realen
`fachworkflow_proof_handoff.py` wird nur die Stage `ppm` selbst mechanisch durch einen echten Stage-spezifischen Executor ausgeführt. Die übrigen Stage-Proofs werden überwiegend generisch als Dateien/Hashes/PASS-Evidence validiert.

Das erzeugt genau den bereits historisch dokumentierten K1/K3-Interpretationsspielraum.

### Alternativ-Labor korrekt eingeordnet

Der bisherige P40/P22-Ein-Artikel-PASS bleibt gültig für seine eigentliche Aussage:
`prepare(no write) -> externe Signatur -> genau ein Draft -> Readback -> kein Publish`.

Er ist aber **kein Beweis eines vollständigen frischen 12-Stage-Codex-Laufs**:
- P22 benutzt die vorhandene PPM-Test-/Fixture-Umgebung (`fixture-builder.php`);
- P40 prüft bei `stage_proofs` nur Vorhandensein/Anzahl 12, nicht die reale stage-spezifische Ausführung;
- deshalb darf aus dem Labor-PASS keine Produktionsbindung aller 12 Stufen abgeleitet werden.

### Zwei bereits bekannte Autoritätslücken bleiben auch für ACM relevant

1. `CURRENT_NEW_LINK_BINDING = BLOCKED_MISSING_EXISTING_DETERMINISTIC_BINDING`
   - ACM hat bisher vorhandene Link-Validatoren inventarisiert;
   - keine unveränderte deterministische NEW-Quelle gefunden, die die artikelbezogenen Linkbindungen ohne freie Worker-/Chatentscheidung erzeugt.

2. `CURRENT_DESIGN_FORMAT_BINDING = BLOCKED_UNDEFINED_EXISTING_STAGE_AUTHORITY`
   - ACM hat den vorhandenen Rendered-DOM-/Style-Validator sauber identifiziert;
   - dieser ist sinnvoll **nach** Draft/Readback;
   - der reale bestehende Handoff verlangt `design_format` aber bereits als Teil der 12 Stage-Proofs **vor** Abschluss des Handoffs/realen Draftwegs;
   - `design_format` darf nicht eigenmächtig in einen Source-PASS umdefiniert werden.

### KISS-Folge

- kein LT-Einzelfix;
- geparkter `hobbyroom/languagetool-runtime-rebind-20260907` bleibt nur historische Beweisquelle;
- kein neuer Executor;
- kein neuer Handoff;
- kein zweiter Controller;
- keine neue Linklogik;
- keine neue `design_format`-Bedeutung;
- keine alten Artikel/Pläne als NEW-Produktionsquelle;
- keine Änderung an Textmaschine/PPM/PSERC/PSTE/WordPress/Publish.

Status für realen ACM-Nulltest:
`ACM_REAL_STAGE_CORRIDOR_BLOCKED`

Der erste sichtbare Stop ist LanguageTool; der **Root Cause darf aber nicht auf LanguageTool verengt werden**.

## READ-ONLY-CORRIDOR-ENTSCHEIDUNG – ENDSTAND

Die in der autoritativen Übergabe verlangte read-only Frage ist geschlossen.

### NEW internal_links
Im aktuellen unveränderten PPM/Fachworkflow wurden gefunden:
- `PPM679_WordPress_Link_Target_Validator`
- `Content_Structure_Language_Gate::check_links`
- `Content_Validator`
- weitere Link-/Known-Error-Prüfer

Diese Komponenten validieren bereits gebundene Links.
Es wurde kein unveränderter allgemeiner deterministischer NEW-Erzeuger gefunden, der für einen frischen Artikel die drei artikelbezogenen `quality_binding.link_bindings` / Registry-Bindungen ohne Worker-/Chatentscheidung erzeugt.

Ergebnis:
`CURRENT_NEW_LINK_BINDING = BLOCKED_MISSING_EXISTING_DETERMINISTIC_BINDING`

### design_format
Vorhandene echte Autorität:
- Rendered-DOM-/Computed-Style-/Readback-Prüfung nach Draft/WordPress-Render.

Der produktive 107007-Handoff verlangt `design_format` jedoch bereits als Teil der 12 Stage-Proofs vor Abschluss des Handoffs.
Ein echter Rendered-DOM-PASS kann dort nicht ehrlich vorliegen.

Keine vorhandene unveränderte Produktionsautorität wurde gefunden, die `design_format` im Prewrite-Handoff eindeutig anders definiert.
Eine Umdeutung auf Source-Format wäre eine neue Vertrags-/Autoritätsentscheidung und ist verboten.

Ergebnis:
`CURRENT_DESIGN_FORMAT_BINDING = BLOCKED_UNDEFINED_EXISTING_STAGE_AUTHORITY`

### Konsequenz

`ACM_REAL_STAGE_CORRIDOR_BLOCKED`

Kein LanguageTool-Einzelfix.
Kein Produktkandidat.
Kein neuer 7/7-Realtest.
Kein neuer Runner/Executor/Handoff/Controller.
Keine neue Link- oder Designlogik.
Keine Änderung an bestehenden Schnittpunkten.

Der ACM-Laborkern `prepare(no write) -> externe Signatur -> Draft -> Readback` bleibt als isolierter technischer PASS bestehen.
Nicht bewiesen ist die vollständige frische 12-Stage-Produktion ohne freie Workerentscheidung.

## HARTE ZWANGSJACKE FÜR JEDE WEITERE ACM-ARBEIT

Die Route darf keinen Fix-/Testkandidaten erzeugen, bevor das in `00_ROUTE_BOUNDARY.md` definierte
`PRE-CHANGE-ZWANGSGATE – FAIL CLOSED`
vollständig bestanden ist.

Verbindliche Entscheidung:
- `4x NEIN + SYSTEMWIRKUNG BELEGT` => genau eine kleinste Änderung darf geprüft werden.
- jedes `JA`, `UNKLAR`, `NICHT BELEGT` => **STOP**.
- kein Chat-/Worker-Ermessen darf diese Entscheidung überschreiben.
- kein Einzeltest-PASS darf die verpflichtende Positiv-/Negativ-/Gesamtworkflow-/Gesamtsystemprüfung ersetzen.
- keine Änderung darf neue Freiheitsgrade erzeugen oder das Ergebnis fachlich beeinflussen.

Diese Regel gilt vor Codeänderung, Handoff-Anbindung, Testkandidat, Runtime-Bindung, WordPress-Anbindung und Produktionsadoption gleichermaßen.

## HOBBYRAUM / NEXT ACTION

HOBBYRAUM_STATUS: **BLOCKED**
PRODUKTIONSADOPTION: **BLOCKED**

**WP-01 bleibt BLOCKED und wird in dieser Route nicht angefasst.**

Das ist kein Produktions-Bypass. Solange WP-01 ungelöst ist, gibt es keine Produktionsadoption.

**NEXT ACTION:**

Keine technische Reparatur zulässig.

Die read-only Suche ist abgeschlossen und hat beide fehlenden Autoritäten bestätigt.
Unter den aktuellen Hard Rules bleibt die reale ACM-Integration BLOCKED, bis eine bereits bestehende autoritative Quelle nachgewiesen wird oder eine spätere ausdrücklich freigegebene Ziel-/Schnittstellenentscheidung erfolgt.

Verbindlicher Einstieg:
`offizieller Runtime-Start -> CURRENT_BOUND_ACTION_READY -> aktuelles gebundenes Hindernisstangen-Item -> bestehende FACHWORKFLOW_HANDOFF_REQUEST.json`

KISS-Arbeitsauftrag:
- nur den bereits vorhandenen Chat/Codex-/Runtime-Einstieg benutzen
- genau das gebundene aktuelle Item verwenden
- reale Fachprodukte/Fact-Pack über den bestehenden Fachworkflow erzeugen
- bestehendes 16-Feld-Handoff unverändert verwenden
- danach nur die bereits bewiesene unveränderte ACM-Laborkette prüfen
- beim ersten echten Block STOP
- kein neuer Handoff
- kein neuer Controller
- keine neue PPM-API
- kein WordPress-Runtime-Handler
- kein WordPress-Write
- keine Schnittstellenänderung
- kein Auto-Publish

Wenn der reale Lauf an LanguageTool oder einer anderen vorhandenen Pflichtabhängigkeit blockiert, ist genau dieser erste reale Block der nächste Befund.

## VERBINDLICHER ARBEITSWEG

1. Immer vorhandenen Baustein zuerst prüfen.
2. Nur den ersten offenen Fehler bearbeiten.
3. Kleinste Änderung.
4. Derselbe positive/negative Seam-Test danach.
5. Bei wachsender Sonderlogik STOP statt neue Architektur.
6. Parallelroute nicht anfassen.
7. main/CURRENT_STATE/Zielvertrag nicht verändern, solange ACM nicht ausdrücklich adoptiert wird.
8. Kein Auto-Publish.
9. Bestehende Schnittpunkte sind absolut tabu: nur unverändert benutzen oder read-only prüfen; keine neuen Wrapper/Handler/Übergabeformate als Umgehung.

## ZIELVERTRAG

Produktiver Zielvertrag: **unverändert**.

ACM-Adoptionskandidat:
`57_PRODUCTION_ADOPTION_CONTRACT_CANDIDATE.md`

Er ist keine zweite produktive Zielwahrheit.
Er beschreibt nur die noch nicht adoptierte Alternative.

## ARCHIV

Keine aktive oder ungeklärte Information wurde archiviert.
P0–P57 sowie P59 bleiben Entwicklungs-/Beweis-/Entscheidungsakten.
Sie dürfen nicht als aktuelle Standquelle verwendet werden.

## ABSCHLUSSPRÜFUNG DES SCHNITTPUNKT-TABU-STANDS

PASS auf Head `c6f38f0c1ad1c992f3738d83c342dfd9a5637272`:
- kompletter bestehender P3-Laborlauf SUCCESS
- P8 Producer/External-Signer/Importer-Isolation SUCCESS
- P47 bestehendes Handoff unverändert PASS
- One-Article-End-to-End-Labortest PASS
- Endstempel-/WordPress-Preimport positive/negative PASS
- keine Änderung außerhalb `control/seo-text-buero/alternative-central-machine/`
- keine Schnittstellenänderung
- kein WordPress-Write auf Produktion
- kein Publish

## EINE WAHRHEIT – NEGATIVPRÜFUNG

PASS:
- keine zweite produktive CURRENT_STATE erzeugt
- keine ACM-Änderung an produktiver Fehlermatrix
- kein zweiter produktiver Zielvertrag
- Master ist nur Wegweiser auf diese Datei
- ältere Fortschrittsakten sind keine aktuelle Standwahrheit
- Parallelroute bleibt separat
- kein Archiv als Current
- kein Auto-Publish

## CAMPUS-/ARCHITEKTURFOLGE

Die ACM-Erkenntnis ist allgemeingültig:
`bestehende Fachlogik behalten -> technische Orchestrierung vereinfachen -> eine signierte Übergabedatei -> fail-closed Draft-Import`.

Sie wird **noch nicht** in einen allgemeinen Campus-/Neubau-Standard propagiert, weil ACM noch nicht produktiv adoptiert ist.

Status:
`CAMPUS_PROPAGATION_BLOCKED_UNTIL_ALTERNATIVE_ARCHITECTURE_APPROVED`

Nach späterer Adoption ist genau dieses KISS-Prinzip als Neubau-Standard zu übernehmen.
