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
`7aaf0c2ac8ad41523e9afbf49d78b8b9b8d0a1f3`

Harte Gesamtprüfung auf diesem Stand:
- Alternative SEO Text P3 Isolated Lab – Run `34374100752` – SUCCESS
- Alternative SEO Text P8 Signer Isolation Lab – Run `34374100651` – SUCCESS
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

## DIREKTE PRÜFERHERKUNFT – HARTER STAND

Ohne neue Architektur direkt an vorhandene echte Prüfer bindbar:

- `textmachine_article_type_structure` -> PPM Content Validator
- `table_contract` -> PPM Content/Table Validator
- `internal_links` -> PPM Content/Link Validator; konkrete NEW-Linkziel-Erzeugung bleibt separat offen
- `ppm` -> reale PPM-Ausführung
- `pserc` -> PSERC Bridge/Supervisor
- `duplicate_cannibalization` -> Editorial Plan Runtime Gate / Systemwide Duplicate Guard
- `seo` -> PPM Target-Keyword-Check + Keyword-Ownership-Gate
- `publish_safety` -> vorhandene No-Write/No-Publish-/Signer-Grenze

Noch NICHT direkt herkunftssicher bewiesen:

1. `research_fact_pack`
   - Fact-Pack, Status und Hashbindungen werden geprüft.
   - PSERC verlangt `research_evidence_gate_status=PASS` plus Attest-Hash.
   - Im aktuellen Repo wurde aber kein vorhandener Prüfer gefunden, der dieses Research-Attest selbst nachprüft.
   - Daher kein GO für direkte Prüferherkunft.

2. `languagetool`
   - vorhandene Qualitätskomponenten prüfen LanguageTool-Evidence.
   - der ausführbare LT-6.8-Runtime ist aktuell nicht reproduzierbar gebunden.
   - daher kein vollständiger echter Runtime-Nachweis.

3. `pste`
   - historischer PSTE Planning-/Pre-Title-Gate ist positiv/negativ belegt.
   - PSERC blockiert falsche PSTE-Verträge.
   - die aktuelle zwingende ausführbare PSTE-Bindung im produktiven Pfad ist aber noch nicht vollständig belegt.

4. `design_format`
   - keine aktuelle unveränderte eigenständige Stage-Autorität belegt.
   - keine neue Bedeutung und keine WordPress-Zwischenprüfung erfinden.

Damit sind aktuell **8/12 Prüferherkünfte direkt belastbar**, 4/12 offen.

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

- Für NEW internal_links existieren die Regeln/Validatoren; eine unveränderte deterministische Erzeugungsquelle für die konkreten drei neuen Linkziele ist weiterhin nicht abschließend gebunden.
- LanguageTool-Regel/Evidence ist vorhanden; ausführbarer LT-6.8-Runtime ist für unbeaufsichtigte Vollautomatik noch nicht reproduzierbar gebunden.
- Finale produktive Übergabe/Adoption bleibt separat zu beweisen.
- Kein Auto-Publish.

Diese Punkte werden nicht durch neue Architektur verdeckt.

## NEXT ACTION

**STATUS: BLOCKED / KEINE TECHNISCHE ÄNDERUNG.**

Erster offene Punkt ist `research_fact_pack`:
Im aktuellen zulässigen Bestand wurde kein echter Research-Attest-Prüfer gefunden, der den Worker-Selbst-PASS technisch ausschließt.

KISS-Folge:
- keinen neuen Research-Prüfer bauen;
- keinen Adapter/Runner/Handoff ergänzen;
- nur weiter, wenn ein bereits vorhandener autoritativer Research-Prüfpfad gefunden/belegt wird oder eine ausdrückliche Grundsatzentscheidung die aktuelle Architekturgrenze ändert.

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
