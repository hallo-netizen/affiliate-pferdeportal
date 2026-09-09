# ACM – AKTUELLER ROUTENSTATUS

Stand: 2026-09-09
Route: Alternative Central Machine (ACM)
Branch: `alternative/seo-text-central-machine-20260908`
PR: #195 (Draft)

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standwahrheit der ACM-Route für:
- belastbaren ACM-Status
- offene Integrationspunkte
- NEXT ACTION
- verbindlichen Arbeitsweg

Produktive Wahrheit bleibt separat und unverändert:
`control/startmaster0107/CURRENT_STATE.json`

Produktive Fehlermatrix bleibt separat:
`control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`

Ältere ACM-Akten bleiben Beweis-/Historienquellen und sind keine zweite CURRENT-Wahrheit.

## STATUS

**ACM-KERN: PASS**
**PRODUKTIONSADOPTION: BLOCKED**

Aktueller vollständig getesteter ACM-Head:
`fe9d5dd375c00139f206bf8791104482f357afba`

Harte Gesamtprüfung auf diesem Stand:
- Alternative SEO Text P3 Isolated Lab – Run `34382240065` – SUCCESS
- Alternative SEO Text P8 Signer Isolation Lab – Run `34382240055` – SUCCESS
- ACM Machine Hardlock – PASS
- P0–P47 – PASS
- ACM first full one-article lab test – PASS
- Endstempel-/Preimport positive/negative – PASS
- Zero-freedom / no-text-mutation seam – PASS
- relevante historische Fehlerkette bis M36 – PASS

Produktiver main wurde durch diese Änderung nicht verändert.
Kein WordPress-Produktivwrite.
Kein Publish.

## VERBINDLICHES ZIELBILD

Am Ende des Fachworkflows steht **eine einzige fertige, vollständig maschinell geprüfte Datei**.

Danach:
- keine fachliche Nachbearbeitung;
- keine technische WordPress-Sichtprüfung als Pflichtstufe;
- WordPress ist erst Ziel für den späteren Upload/Import;
- die bisherige menschliche Sichtkontrolle war nur zusätzliche Kontrolle und soll nach mehrfach bewiesenem Workflow entfallen;
- kein Auto-Publish.

Keine WordPress-Zwischenstufe wird in ACM neu erfunden.

## DREIER-ZICKZACK – AKTUELL ADOPTIERTE ACM-ENTSCHEIDUNG

Verbindliches Prinzip:

`Arbeiter -> Zentralmaschine -> fest gebundener vorhandener Prüfer -> Zentralmaschine -> nächster Arbeiter`

Dabei gilt:

1. Die Zentralmaschine besitzt allein Reihenfolge und Zustand.
2. Jeder Worker führt nur seinen gebundenen Mikroschritt aus.
3. Kein Worker darf den nächsten Schritt, Prüfer oder Reparaturweg wählen.
4. Kein Worker darf sich selbst PASS geben.
5. Der vorhandene Prüfer darf nur PASS oder BLOCKED liefern.
6. BLOCKED bedeutet STOP; keine improvisierte Reparaturroute.
7. Fach-, Inhalts- und Qualitätsregeln bleiben unverändert.
8. Keine Worker-zu-Worker-Kommunikation.
9. Kein zweiter Controller.
10. Keine neue Fachprüfung.

## 12 NACHWEISE – CHECKLISTE, NICHT FAHRPLAN

Die 12 bestehenden Pflichtnachweise bleiben vollständig erhalten:

- research_fact_pack
- textmachine_article_type_structure
- table_contract
- internal_links
- languagetool
- ppm
- pserc
- pste
- duplicate_cannibalization
- seo
- design_format
- publish_safety

Neue harte Semantik:

**Die 12 Namen sind eine unveränderliche Pflichtmenge. Sie bestimmen nicht die Laufreihenfolge.**

Die Laufreihenfolge gehört ausschließlich der Zentralmaschine und richtet sich nach den realen technischen Abhängigkeiten.

Implementiert in:
- `prototype/p11_workflow_contract.py`
- `prototype/test_p11_workflow_contract.py`

Positiv:
- alle 12 exakt einmal vorhanden, auch in anderer Reihenfolge -> PASS.

Negativ:
- fehlt -> BLOCKED
- doppelt -> BLOCKED
- unbekannter Nachweis -> BLOCKED
- Status nicht PASS -> BLOCKED
- nicht ausgeführt -> BLOCKED
- Fach-/Qualitätsregel geändert -> BLOCKED
- Publish erlaubt -> BLOCKED
- optional/enabled-Laufzeitschalter eingeschleust -> BLOCKED

Damit kann die 12er-Checkliste nicht als zweiter Workflowcontroller wirken.

## INHALT / QUALITÄT

Unverändert und tabu:
- Textmaschine
- Research-/Fact-Pack-Regeln
- Artikeltyp-/Strukturregeln
- Tabellenregeln
- interne Linkregeln
- LanguageTool-Regeln
- SEO
- Dubletten-/Kannibalisierungsschutz
- PPM
- PSERC
- PSTE
- Publish-Sicherheit

Die aktuelle Änderung betrifft ausschließlich ACM-Orchestrierungssemantik.

## 0,0 FREIHEIT / ZWANGSJACKE

Weiterhin bewiesen:
- keine caller-selected Route
- keine caller-selected Workerwahl
- keine caller-selected Validatorwahl
- keine freie Next-Step-API
- kein freier Reparaturweg
- Chat besitzt keine Fach-/Workflow-/Publish-Autorität
- Worker besitzt keine Publish-Autorität
- externe Signatur bleibt außerhalb des Producers
- Manipulation nach Signatur -> BLOCKED
- Inhalts-/Metadatendrift -> BLOCKED
- unbekannte Zusatzfelder -> BLOCKED
- publish_allowed=true -> BLOCKED

Der externe ACM-Hardlock im separaten Lab-Basisbranch bleibt wirksam und kann vom Kandidaten nicht mitverändert werden.

## EINFLUSSNAHME VON AUSSEN

Externe Recherchequellen sind ausschließlich untrusted data.

Sie dürfen:
- Fakteninhalt für die vorhandene Recherche liefern.

Sie dürfen nicht:
- Workflow bestimmen;
- Folgeaktionen bestimmen;
- Regeln verändern;
- Prüfer auswählen;
- PASS/PUBLISH auslösen.

Provenienz/Hashes bleiben gebunden.
Nach finaler externer Signatur ist jede Byteänderung fail-closed.

## ENDSTRECKE – HARTER AKTUELLER BEWEIS

Der Zielweg ab fertigem Fachprodukt ist technisch bewiesen:

`fertiger geprüfter Artikel/Batch -> neutrale Enddatei -> externer Endstempel -> WordPress-Preimportprüfung -> Draft-only`

Neutraler Dateiname:
`PFERDE_ATELIER_SIGNED_ARTICLE_BATCH_FINAL.json`

Harter Test auf aktuellem ACM-Head:
- Endstempel + echter `ENDSTEMPEL_WORDPRESS_VERIFY.php`: PASS für 1, 3, 25 und 1000 Artikel;
- tatsächliche Artikelzahl ausschließlich dynamisch im Manifest;
- kein 7er-Limit;
- Artikelbytes bleiben unverändert;
- WordPress prüft vor dem ersten Write Signatur, Manifest, Batch, Dateiset, Byte-Längen und SHA-256;
- `publish_allowed=false`.

Negativ jeweils BLOCKED:
- ein Byte verändert;
- Artikel fehlt;
- zusätzlicher Artikel;
- falsche deklarierte Anzahl;
- falsche Signatur;
- Replay/bereits verwendeter Batch.

Der vorhandene PPM-Produktionskern verarbeitet Artikel in seinen bestehenden zulässigen Chunks/Items. Das ist kein Gesamtlimit der Enddatei oder des Systems.

Die 12 Fachnachweise werden nicht an WordPress übergeben und von WordPress nicht erneut fachlich bewertet. Sie gehören an ihre reale Stelle im Fachworkflow.

## KORREKTUR EINES BISHERIGEN ACM-FEHLWEGS

Die frühere ACM-Gleichsetzung

`design_format = zwingender WordPress-DOM-/Draft-Prüfschritt innerhalb der Artikelproduktion`

wird **nicht weiter als aktuelle Wahrheit verwendet**.

Fakt:
Der tatsächlich benutzte Zielablauf liefert zuerst die fertige Datei; WordPress kommt danach.

Folge:
- kein neuer WordPress-Vorschauweg;
- kein Draft/Readback/DOM-Zickzack als neue Pflicht;
- die tatsächliche bestehende Autorität für `design_format` muss ausschließlich aus dem real funktionierenden Fachworkflow abgeleitet werden;
- bis dieser Punkt belegt ist, wird nichts geraten und keine neue Designlogik gebaut.

## AKTUELLER REALER INTEGRATIONSPUNKT

Der Dreier-Zickzack ist als ACM-Prinzip sauber.

Der heute produktive 107007-Weg hat jedoch noch eine andere Proof-Herkunftssemantik:

- der gebundene Codex-Worker erzeugt die Nicht-PPM-Stage-Artefakte/Proof-Dateien;
- der bestehende Handoff prüft Schema, Identität, Hash, PASS-Felder und Artefakte;
- nur die PPM-Stufe wird dort zusätzlich selbst real ausgeführt.

Damit ist für die Nicht-PPM-Nachweise noch nicht allgemein technisch bewiesen:

**PASS stammt zwingend direkt aus dem fest gebundenen echten Prüfer und nicht aus einer vom Worker materialisierten PASS-Datei.**

Das ist der nächste reale Integrationspunkt.

## DIREKTE PRÜFERHERKUNFT – AUTORITATIVER ABGLEICH

Die frühere ACM-Einordnung `8/12 direkt belastbar, research_fact_pack erster Blocker` war zu weitgehend und wird verworfen.

Autoritativer TEXT-`CURRENT_STATE`-Abgleich 09.09.2026:

Bereits eindeutig zugeordnet:
- SEO / PSTE / Duplicate-Cannibalization = vorhandene Upstream-READY-Autorität;
- PPM 6.7.9 = realer gebundener Prüfer;
- PSERC = realer Bestandteil des PPM-/Bridge-Korridors;
- Publish-Safety = reale äußere Guards/Receipts;
- Artikeltyp/Struktur, Tabelle, Linkvalidierung und LanguageTool-Evidence besitzen vorhandene PPM-Fachregeln/Validatoren; deren Lifecycle-Bindung darf nicht durch Worker-Selbst-PASS ersetzt werden.

Die zwei aktuell autoritativ offenen Bedeutungs-/Bindungspunkte sind:

1. `CURRENT_NEW_LINK_BINDING = BLOCKED_MISSING_EXISTING_DETERMINISTIC_BINDING`
   - PPM kann drei gebundene Links hart prüfen;
   - bestehende Rollen: `parent_category`, `semantic_related`, `further_information`;
   - für NEW fehlt im aktuellen gebundenen Pfad die deterministische Quelle, die die drei konkreten Ziele auswählt;
   - Worker/Chat darf diese Auswahl nicht frei erfinden.

2. `design_format` – **ACM-BINDUNG HART PASS**
   - vorhandener echter Prüfer: `PPM679_Rendered_DOM_Validator`;
   - Lifecycle fest: `AFTER_WORDPRESS_DRAFT_READBACK_RENDER`;
   - der Prüfer verlangt u. a. `post_id`, `readback_content_hash`, Desktop- und Mobile-Evidence;
   - ein `design_format`-PASS vor WordPress ist damit technisch unzulässig;
   - vorhandene Positivtests PASS;
   - DOM-/Viewport-/Heading-/Readback-Mutationen BLOCKED;
   - menschliche Sichtprüfung ist keine technische PASS-Autorität;
   - keine Design-/Inhaltsregel geändert.

Research ist nach autoritativem TEXT-Abgleich **nicht der erste aktuelle Corridor-Blocker**.

## KISS-GRENZE

Zur Schließung dieses Punktes gilt zwingend:

Erlaubt:
- vorhandene echte Prüfer und deren vorhandene reale Outputs unverändert wiederverwenden;
- mehrere Nachweise aus demselben vorhandenen Fachvalidator ableiten, wenn dieser sie bereits atomar prüft;
- genau eine kleinste Bindung in der bestehenden ACM-Zentralsteuerung.

Verboten:
- 12 neue Prüfer;
- neuer Runner;
- neuer Executor;
- zweiter Controller;
- neues Handoff;
- neues Übergabeformat;
- neue Fach-/Qualitätslogik;
- Änderung von Textmaschine/PPM/PSERC/PSTE/LanguageTool-Regeln;
- Worker-Selbst-PASS.

Wenn die vorhandene Prüferherkunft nicht ohne einen solchen neuen Baustein bindbar ist:
**STOP statt Architekturumbau.**

## WEITERE OFFENE BESTANDSBEFUNDE

- NEW-internal_links ist im aktuellen grünen Gesamtstand nicht mehr der erste offene ACM-Punkt: vorhandene drei Linkbindungen und reale Link-Target-Validierung laufen im P3-Gesamtlauf positiv; negative Linkfälle blockieren fail-closed.
- Der frühere 25er-Draft-Zählfehler war ein Labortest-/Fixture-Zwischenbefund und ist **kein Mengenvertrag und kein aktueller Produktionsblocker**.
- Finale produktive Übergabe/Adoption bleibt separat zu beweisen.
- Kein Auto-Publish.

## NEXT ACTION

**Aktueller erster echter Realtest-Blocker: `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`.**

Unabhängiger Codex-Realtest am 09.09.2026:
- Thema: `Wie funktioniert ein mechanischer Bleistift?`
- vorhandener Einstieg: `python3 control/cloud-entry-gate/cloud_entry.py start` -> `CODEX_CLOUD_ENTRANCE_PASS`;
- nächster vorhandener Pflichtgate: `python3 control/output-quarantine/runtime_entry_gate.py` -> `OFFICIAL_RUNTIME_ENTRY_BLOCKED`;
- Grund: `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`;
- Artikel erstellt: nein;
- signierte End-JSON erstellt: nein;
- HTML-Artefakt: keines;
- WordPress-Write/Publish: keiner;
- Abschluss über vorhandenen Entry: `STEP_TERMINAL_NONPASS`, Status `BLOCKED`, `state_advanced=false`.

Bewertung:
- Zwangsjacke hat korrekt fail-closed gestoppt;
- Codex hat keine Route, keinen Prüfer und keinen Reparaturweg selbst gewählt;
- Textmaschine / PPM / PSERC / PSTE / Handoff / WordPress-Schnittstellen wurden nicht verändert;
- kein Workaround und keine neue Architektur.

**Nächster zulässiger Arbeitspunkt:** ausschließlich prüfen, warum der bereits bestehende Produktionsumgebungs-Nachweis am offiziellen Runtime-Entry fehlt bzw. nicht gebunden wird. Keine Artikel-/Text- oder Workflowänderung davor.

Separat offen, aber nicht durch diesen ACM-Test verursacht:
- repository-weites `Pferde Atelier Immutable Base Hardlock` ist auf dem ACM-Branch weiterhin rot; vor Merge/Produktionsadoption muss dieser Branch/Basis-Konflikt separat geklärt werden.

## VERBINDLICHER ARBEITSWEG

- KISS
- nur erster offener Fehler
- keine Doppelprüfung
- keine Architektur auf Architektur
- vorhandenen Baustein zuerst
- Inspiration aus Altbestand ja, ungefilterte Workflowübernahme nein
- main/CURRENT_STATE nicht verändern
- kein Auto-Publish
- keine Inhalts-/Qualitätsänderung
- jede technische Änderung positiv + negativ + Gesamtworkflow prüfen
## ABSCHLUSS-/NACHHOLPRÜFUNG DIESES CHATS – 2026-09-09

Frisch gegen ACM-CURRENT, Campus/TEXT-CURRENT, Hobbyraum, Zielvertrag, Fehlerquelle, main-CURRENT und aktuelle GitHub-Runs geprüft.

Tatsächlich in dieser ACM-Route geändert/geprüft:
- 12 Pflichtnachweise als unveränderliche Pflichtmenge statt als zweite Ablaufsteuerung gebunden;
- Dreier-Zickzack als Sollprinzip festgehalten: Worker -> Zentrale -> vorhandener Prüfer -> Zentrale;
- Endstrecke als artikelzahlunabhängige signierte Enddatei gegen den echten WordPress-Preimport-Prüfer positiv/negativ geprüft;
- Zwischenfehler aus 25er-Labortests nicht als Produktionsfehler übernommen; aktuelle Endstreckenbeweise für 1/3/25/1000 sind im grünen Gesamtstand enthalten;
- frühere falsche Einordnung von Research als erstem Blocker verworfen;
- design_format-Lifecycle an den vorhandenen Rendered-DOM-Prüfer gebunden;
- die frühere NEW-Linkbindung ist nach dem späteren grünen Gesamtstand kein aktueller erster Blocker mehr; nächster Arbeitsauftrag ist der unabhängige neue Codex-Realtest.

Aktueller Teststand auf Head `fe9d5dd375c00139f206bf8791104482f357afba`:
- P3 Gesamtworkflow: SUCCESS, Run `34382240065`;
- P8 Signer-Isolation: SUCCESS, Run `34382240055`;
- repository-weites Immutable Base Hardlock: FAILURE, Run `34382238025`; bekannter Branch/Basis-Konflikt, keine Produktionsfreigabe.

Original-TEXT-/Campus-Parallelweg bleibt unverändert BLOCKED/FIX_FORBIDDEN und wurde nicht überschrieben.
Kein main-Write, kein WordPress-Produktivwrite, kein Publish.

