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
Ältere P0–P57-Akten sind Beweis-, Entscheidungs- oder Fortschrittsakten und keine aktuelle Standwahrheit.

Die produktive Wahrheit bleibt separat und unverändert:
`control/startmaster0107/CURRENT_STATE.json`

Die produktive STARTMASTER-Fehlermatrix gehört zur parallelen Reparaturroute und wird von ACM nicht überschrieben:
`control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`

## AKTUELLER STAND

**ACM-PROTOTYP: PASS**
**PRODUKTIONSADOPTION: BLOCKED**

Letzter vollständig getesteter funktionaler ACM-Head:
`06dd9d9009ef3d4e697e6dff7235ab18b8f2020e`

Ausgeführte Tests auf exakt diesem funktionalen Head:
- Alternative SEO Text P3 Isolated Lab – Run `34343563907` – SUCCESS
- Alternative SEO Text P8 Signer Isolation Lab – Run `34343563613` – SUCCESS

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

## HOBBYRAUM / NEXT ACTION

HOBBYRAUM_STATUS: **AKTIV**
PRODUKTIONSADOPTION: **BLOCKED**

**NEXT ACTION – nur erster offener Punkt:**
ACM-WP-01 schließen.

KISS-Arbeitsauftrag:
Den bereits bewiesenen Signatur-/Hash-Verifier **vor den bestehenden WordPress-Normal-Draft-Import** hängen.
Dabei:
- keine zweite Importpipeline
- kein neuer Paketvertrag
- kein neuer Signierer
- kein neuer Controller
- keine Textmaschinenänderung
- weiterhin nur Draft
- positiver Test: eine gültige signierte JSON -> exakt ein Draft + Readback
- negative Tests: Manipulation/falscher Schlüssel/Replay/falsche Bindung -> 0 Write

Erst nach PASS dieses einen Punktes:
ACM-WP-02 prüfen.

## VERBINDLICHER ARBEITSWEG

1. Immer vorhandenen Baustein zuerst prüfen.
2. Nur den ersten offenen Fehler bearbeiten.
3. Kleinste Änderung.
4. Derselbe positive/negative Seam-Test danach.
5. Bei wachsender Sonderlogik STOP statt neue Architektur.
6. Parallelroute nicht anfassen.
7. main/CURRENT_STATE/Zielvertrag nicht verändern, solange ACM nicht ausdrücklich adoptiert wird.
8. Kein Auto-Publish.

## ZIELVERTRAG

Produktiver Zielvertrag: **unverändert**.

ACM-Adoptionskandidat:
`57_PRODUCTION_ADOPTION_CONTRACT_CANDIDATE.md`

Er ist keine zweite produktive Zielwahrheit.
Er beschreibt nur die noch nicht adoptierte Alternative.

## ARCHIV

Keine aktive oder ungeklärte Information wurde archiviert.
P0–P57 bleiben Entwicklungs-/Beweisakten.
Sie dürfen nicht als aktuelle Standquelle verwendet werden.

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
