# TEXT / STARTMASTER0107 – TECHNICAL CORRIDOR ROOT CAUSE – 2026-09-07

## Zweck

Kein neuer Architekturentwurf und kein Sammelfix.
Dieses Dokument verdichtet Pauls Audit, die komplette Fehlerhistorie B01–B15/M01–M33, den letzten echten 7/7-Stand und den neuen LanguageTool-Livebefund zu einer gemeinsamen technischen Fehlerursache.

## Harte unverhandelbare Grenzen

- Qualität unverändert.
- Inhalt/Fachlogik unverändert.
- Design unverändert.
- Single Door bleibt genau eine Tür.
- Wächter bleibt fachblind/dumm.
- Chat bleibt ohne freie Navigation, State-, Repair- oder Publish-Autorität.
- Keine neue Architektur, kein neuer Runner, kein neuer Workflow, kein neuer separater Executor.
- Kein Auto-Publish.

## 1. Gemeinsame Fehlerklasse aus der Historie

Die bisherigen Livefehler sind überwiegend keine unabhängigen Einzeldefekte. Sie fallen in vier wiederkehrende technische Klassen:

### K1 – Ausführung/Abhängigkeit verlangt, aber nicht eindeutig gebunden
Beispiele:
- B07 PPM/PSERC Runtimepakete fehlten/Env-Pfad unklar.
- B02 Fachworkflow-Ausführungskontext fehlte.
- neuer Livebefund 07.09.: `BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING`.

### K2 – Upstream/Downstream verlangen inkompatible Zustände
Beispiele:
- B01 PPM-Handoff verlangte numerische WP-ID, obwohl gültiger Upstream-Vertrag Name/Slug/Taxonomy bindet.
- B08 Bootstrap-/H8-Paket wurde zeitweise wie fachlicher Produktionskontext behandelt.
- B09 Receipt/Pass-Ref-Umstellungen.
- B10/B11 Release-/Batch-Identitäten an Übergängen.

Pauls direkte Entsprechung:
- F2/A6/A12: Gate A verlangt unresolved placeholder, Gate B braucht resolved HTML.
- F7/A7: Downstream verlangt Tabelle, Rendererpfad kann sie nicht liefern.

### K3 – PASS/Hash bezieht sich nicht mechanisch auf die real ausgeführte Prüfung bzw. den richtigen Artefaktzustand
Beispiele:
- B04 Fake-PPM-PASS.
- Nicht-PPM-Stufen im aktuellen Handoff: `input_sha256` muss nur formal 64 Hex sein; `execution_evidence` ist Text; ein echter stage-spezifischer Executor wird dort nicht ausgeführt.
- Paul A11: derselbe `validated_content_hash` hat zwei verschiedene Bedeutungen.

### K4 – Test beweist nicht denselben realen Pfad
Beispiele:
- B14: M01–M33 / „last real regression“ ist kein echter Replay der 7/7-Strecke.
- Paul A37: grüne Tests, obwohl einzelne reale Stufen effektiv nie laufen.
- neuer LT-Lauf: gleicher STARTMASTER-Code wie vorher, aber Codex interpretiert fehlende LT-Ausführung diesmal korrekt fail-closed statt den Proof selbst zu erzeugen.

## 2. Kritischer aktueller Codebefund

`fachworkflow_proof_handoff.py` behandelt elf von zwölf Pflichtstufen generisch:

- Proof-Datei muss vorhanden/hashkorrekt sein;
- `status=PASS`;
- `execution_performed=true`;
- `input_sha256` muss nur formal 64 Hex sein;
- `execution_evidence` muss nichtleer sein;
- Artefakte müssen existieren/hashkorrekt sein.

Nur `ppm` wird speziell behandelt:
- echte `ppm679_binding`;
- echter PPM-6.7.9-Lauf;
- finaler Artikel und PPM-Report werden real erzeugt/verifiziert;
- PPM `content_hash` muss exakt dem finalen Artikel-SHA entsprechen;
- erst danach PASS/Receipt.

**Schluss:** Der bei B04 für PPM gelöste Selbstbeglaubigungsfehler ist für die übrigen elf Stufen technisch nicht gleichwertig geschlossen.

## 3. Warum der B02-Fix zwar geholfen, aber das Grundproblem nicht gelöst hat

B02 wurde real überwunden, indem Current Codex als gebundener Fachworkflow-Worker festgelegt wurde.

Das war als Rollenbindung wirksam, löste aber die darunterliegende Frage nicht:
**welcher konkrete vorhandene Prüfer / welches konkrete vorhandene Verfahren führt jede einzelne Pflichtstufe aus?**

Damit entstand innerhalb des gebundenen Raums wieder Interpretationsspielraum:
- alter Codex-Lauf erzeugte Nicht-PPM-Proofs und kam bis B01;
- neuer Codex-Lauf verweigert bei LanguageTool die Selbstbeglaubigung und stoppt vorher.

Das ist ein Verhaltensunterschied bei identischer technischer Grundlage und widerspricht dem Ziel „Chat in Zwangsjacke“.

## 4. Ursprungskonzept vs. aktueller Stand

Frühe H8-/STARTMASTER-Unterlagen verlangten:
- keine freie Recherche;
- keine freie Texterstellung;
- keine eigene Paketerzeugung;
- keine Workflowentscheidung;
- nach R_001 nur den bereits bestehenden Fachworkflow;
- fachblinder Wächter.

Aktuell sichtbar:
`CURRENT_CODEX_WORKER_MUST_GENERATE_REAL_CURRENT_OUTPUTS`.

Diese Rollenbindung darf nicht bedeuten, dass Codex selbst entscheidet, wie eine Pflichtprüfung real auszuführen oder zu attestieren ist.

## 5. Paul – was daraus zwingend für STARTMASTER folgt

### F2 / A6 / A12
Jede Stufe braucht einen benannten Artefaktzustand:
- INPUT vor Transformation;
- OUTPUT nach Transformation;
- der nachfolgende Prüfer muss exakt den richtigen Zustand erhalten.

Kein generisches „Artikelhash“ ohne Zustand.

### F7 / A7
Vor Live muss für jede direkte Stufenpaarung geprüft werden:
**Kann der erlaubte Upstream technisch überhaupt den Zustand liefern, den Downstream zwingend verlangt?**

Nicht Inhalt ändern. Nur technische Erfüllbarkeit prüfen.

### A11
Hashfelder dürfen nicht semantisch überladen sein.
Ein Hash muss klar sagen, welches konkrete Artefakt er bindet.

### A37
Ein Test-PASS zählt nicht als Stufenbeweis, wenn der echte Prüfer nicht lief.

### F8 – retracted
Nichts entfernen/vereinfachen, nur weil es redundant aussieht. Erst load-bearing Gegenprüfung.

## 6. 12 Pflichtstufen – aktueller STARTMASTER-Bindungsstatus

| Stufe | Aktuell im Handoff real ausgeführt? | aktueller harter Befund |
|---|---|---|
| research_fact_pack | NEIN, generischer Proof | realer Fact-Pack wird verlangt, aber stage-spezifische Ausführung im Handoff nicht gebunden |
| textmachine_article_type_structure | NEIN, generischer Proof | Prompt/Ruleset gebunden; Ausführungsnachweis nicht mechanisch stage-spezifisch |
| table_contract | NEIN, generischer Proof | inneres PPM/Plugin besitzt Tabellenregeln; Paul F7/A7 zeigt mögliche Erfüllbarkeitskollision |
| internal_links | NEIN, generischer Proof | Paul A13/A16 zeigt zusätzlich Zustand-/Resolver-Risiko |
| languagetool | NEIN, generischer Proof | historischer echter LT-6.8-Weg belegt; aktuelle Runtimebindung fehlt |
| ppm | **JA** | einzig voll real gebundene Stage; B04 hier geschlossen |
| pserc | NEIN als eigene Stage; generischer Proof | PSERC ist innerhalb/außerhalb anderer realer Grenzen vorhanden, aber Stage-Proof selbst führt keinen PSERC-Prüfer aus |
| pste | NEIN, generischer Proof | historisch echte Installer/Checks belegt, aktuelle Stageausführung nicht aus dem Handoff ableitbar |
| duplicate_cannibalization | NEIN, generischer Proof | Paul F4/A37: tatsächliche Ausführung/Testparität besonders kritisch |
| seo | NEIN, generischer Proof | Fachregel bleibt geschützt; stage-spezifische reale Ausführung im Handoff nicht gebunden |
| design_format | NEIN, generischer Proof | historisch PPM-DOM/Design-Gates belegt; generischer Stage-Proof bildet dies nicht mechanisch ab |
| publish_safety | NEIN als Stage; generischer Proof | äußere Publish-Gates sind real vorhanden; Stage-Proof selbst ist trotzdem generisch |

Wichtig:
„NEIN“ bedeutet hier ausschließlich: **der aktuelle STARTMASTER-Handoff führt keinen stage-spezifischen Executor aus.**
Es bedeutet nicht, dass die Fachprüfung im Gesamtprojekt nicht existiert.

## 7. Neuer LanguageTool-Befund im Gesamtbild

LanguageTool ist nicht als isolierter neuer Fehler zu behandeln.

Historisch belegt:
- LanguageTool 6.8 / Bestand 43;
- echte Offline-Abhängigkeit;
- innerer ZIP-SHA `6a7f6b67…`;
- äußerer Bestand-43-SHA `187f7c2e…`;
- Commandline-JAR SHA `2122882e…`;
- reale `--json -l de-DE`-Ausführung;
- Checked-Text-Hash + Raw-Report-Hash + Returncode + Findings wurden in `language_evidence` gebunden;
- PPM kontrollierte diese Evidenz weiter.

Die historische Ausführung wurde am 07.09. lokal reproduziert; alter Raw-Report-Hash war bytegenau reproduzierbar.

**Aber:** der bereits begonnene Branch `hobbyroom/languagetool-runtime-rebind-20260907` ist ab jetzt nur PARKPLATZ, kein Integrationskandidat. Ein isolierter LT-Fix würde die gemeinsame Fehlerklasse K1/K3 nur an einer Stelle schließen.

## 8. Gelernter KISS-Lösungsansatz

Nicht:
LT fixen → live → nächster Stagefehler → nächster Minifix.

Sondern einmalig den bestehenden Fachworkflow technisch vollständig abbilden:

Für jede der 12 bestehenden Stufen nur fünf Dinge feststellen:
1. vorhandener realer Prüfer/Mechanismus;
2. exaktes Eingangsartefakt + Zustand;
3. exakter Ausgang / Evidence;
4. welcher vorhandene nächste Prüfer konsumiert exakt diesen Ausgang;
5. wie der aktuelle Single-Door/Handoff diese bestehende Ausführung ohne Chatentscheidung bindet.

Kein neuer Fachworkflow.
Keine neue Qualitätslogik.
Keine neuen Stufen.

Ziel ist nur:
**bestehende Ausführung mechanisch eindeutig binden statt vom Chat interpretieren lassen.**

## 9. Nächster Test erst nach Corridor-PASS

Vor dem nächsten Codex-Live-Lauf kein weiterer Produktions-Minifix.

Der nächste Kandidat darf erst entstehen, wenn für alle 12 Stufen mindestens positiv feststeht:
- EXISTING_EXECUTOR_OR_VALIDATOR_IDENTIFIED;
- INPUT_STATE_IDENTIFIED;
- OUTPUT_STATE_IDENTIFIED;
- NEXT_CONSUMER_IDENTIFIED;
- NO_CHAT_DECISION_REQUIRED;
- keine direkte Paul-Vertragskollision ungeklärt.

Negativprüfung je Übergang nur gezielt:
- falscher Inputzustand → BLOCK;
- falscher Hash → BLOCK;
- fehlender realer Prüfer → BLOCK;
- selbstbehaupteter Proof ohne Prüfer → BLOCK;
- Output der falschen Transformation → BLOCK.

Kein Voll-7/7-Retest für jede Stufe.

## 10. Konsequenz

Der nächste sinnvolle Arbeitsschritt ist **kein LanguageTool-Merge**.

Es ist die einmalige vollständige technische Corridor-Matrix auf Basis der vorhandenen Maschinen/Verträge.

Erst daraus wird genau ein konsolidierter, kleiner Integrationskandidat abgeleitet.

Damit wird aus der bisherigen Fehlerkette erstmals ein gemeinsamer Root-Cause-Fix statt einer weiteren Folge von Pflastern.
