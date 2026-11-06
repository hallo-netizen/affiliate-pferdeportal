# Abschluss der Diagnoseauswertung: MINI-Titelrückimport vom 06.11.2026

**Auswertung der vorliegenden Daten abgeschlossen. Programmkorrektur und deren Laufzeitnachweis sind offen.** Keine redaktionelle Einzelprüfung und keine Änderung eines Originaltitels.

## Was tatsächlich passiert ist

Die Originaldiagnose meldet PSTE 0.57.144.12. Alle **87 Rücklauf-Fälle wurden verarbeitet**, keine stehen mehr aus. **7 PASS, 78 HELD, 2 BLOCKED.** Die 80 Nicht-PASS werden in der Zusammenfassung zusammen als held=80 geführt. Im Ablauf sind **87 gespeicherte manuelle Titeländerungen** und danach **75 gespeicherte Rücklauf-Neuberechnungen** belegt. Der Titelimport ist als Request abgeschlossen; der Rücklauf erreicht anschließend COMPLETE. Ein fehlender Importtransport ist für die 80 Sperren nicht belegt.

Nachvollziehbarer Ablauf am 06.11.2026, Zeitangaben Berlin:
- 14:18:50: Abschluss PSTE_MINI_TITLE_REPAIR_IMPORT.
- 14:29:06: Abschluss PSTE_MINI_FORWARD_TO_PLAN.
- 14:29:29: Rücklaufstatus COMPLETE mit total=87.

## Warum die 80 Fälle nicht freigegeben wurden

| Anzahl | Tatsächlich gespeicherter Sperrgrund | Einordnung |
|---:|---|---|
| 50 | PSTE_TITLE_READY_CATEGORY_DECISION_OPEN | Titel liegt vor, Kategorieentscheidung offen. Der normale Pfad endet als STRUCTURE_GAP; eine Planungsfreigabe ist nicht gespeichert. |
| 7 | PSTE_PORTAL_RELEVANCE_NOT_PROVEN | Trotz Weitergabe verlangt der Rücklauf weiterhin Relevanz-/Sandbox-Belege: 4 externe Belege, 3 Familienbelege. |
| 6 | PSTE_LANGUAGE_TITLE_REQUIRED | Nach der Titeländerung fordert der Rücklauf weiterhin einen Sprachtitel. |
| 3 | PSTE_TITLE_WORKER_NEEDS_REWRITE und PSTE_EXISTING_EVIDENCE_REENTRY_REVIEW_TITLE_MISMATCH | Rücklauf meldet Abweichung zwischen Titel und vorhandenem Prüfbeleg. |
| 7 | PRE_TITLE_ACTIVE_TITLE_CONTAINS_SOURCE_QUERY | Planungssperre wegen im aktiven Titel gefundener ursprünglicher Suchfrage. Die Diagnose allein belegt keine vollständige fachliche Dublettenidentität. |
| 2 | BROAD_SCOPE_EXISTING_SEO_KEYWORD_UNKNOWN_FAIL_CLOSED | Bestehender SEO-Bezug ist nicht ausreichend bekannt; keine sichere Planungsfreigabe. |
| 1 | QUESTION_TITLE_NOT_FAQ | Gespeicherte Sperre wegen Verhältnis von Fragetitel und Artikeltyp. |
| 1 | CATEGORY_HEAD_INTENT_COLLISION | Gemeldete Kollision mit Kategorie-Hauptabsicht. |
| 1 | NON_EDITORIAL_TRANSACTIONAL_QUERY | Als nicht redaktionell/transaktional eingestuft. |
| 1 | PSTE_PRODUCT_CHOICE_CANDIDATE_RETAINED und PSTE_PRODUCT_CHOICE_DOWNSTREAM_NOT_REGISTERED | Produktwahlfall bleibt zurückgestellt. |
| 1 | PSTE_PORTAL_RELEVANCE_PROVEN_FAMILY_STRUCTURE_GAP | Gemeldete Familienstrukturlücke; gesondert zurückgestellt. |

Die Gruppen sind disjunkt und summieren sich zu **80**. Die sieben PASS sind separat (6 PORTAL_INTERNAL_FAMILY_CONTEXT_CHECKED, 1 PORTAL_INTERNAL_TOPIC_FREE).

## Der gemeinsam sichtbare Fehlverlauf

**50 Fälle bleiben im selben Kategorien-Zwischenzustand hängen.** Die Ablaufspur zeigt für diese Gruppe dieselbe Folge: gespeicherte Titelkorrektur mit CATEGORY_DECISION_OPEN → Rücklauf schreibt DISCOVERY_ONLY, PENDING, Kategorie 0, Planung BLOCKED → Kontextfortschreibung schreibt PROVISIONAL_ACCEPTED, CURRENT, Planung NO mit unverändertem CATEGORY_DECISION_OPEN. CURRENT bezeichnet hier einen gespeicherten Kontextstatus und bedeutet keine redaktionelle Freigabe. Eine Kategorieentscheidung wird in dieser Folge nicht abgeschlossen.

**16 Fälle behalten Anforderungen an bereits extern bearbeitete Relevanz oder Titel.** Die Speicherung des Titels und die spätere Entscheidung konsumieren damit keinen nachweislich durchgängig wirksamen gemeinsamen Freigabestand. Genau die Übergabe von Originalfrage, externem Relevanzentscheid, externem Titel und zugehörigem Prüfbeleg ist als gemeinsamer Reparaturpunkt zu untersuchen. Der Diagnoseexport allein trennt nicht sicher zwischen verlorenem Eingangsbeleg, alter gespeicherter Sperre und einer erneut ausgeführten fachlichen Prüfung. Eine dieser Varianten ohne passenden Quellcode als gesicherte Ursache zu benennen wäre eine Vermutung.

**Die übrigen 14 Sperren sind gesondert begründet.** Sie dürfen nicht pauschal als unerlaubte Doppelprüfung gelöscht werden. Für die zwölf Planungssperren müssen tatsächlicher Bestand und der eine zuständige Planungsentscheider herangezogen werden; die zwei zurückgestellten Sonderfälle bleiben getrennt.

## Was die Diagnose ausdrücklich nicht beweist

- Aus 50 offenen Kategorieentscheidungen folgen nicht 50 fehlende Kategorien. Der Bericht nennt 1.176 Kategorien, enthält aber keinen vollständigen aktuellen Termbaum zur Prüfung passender Zuordnungen.
- Mehrfach kopierte Grundcodes unter SOURCE, NORMAL_PATH, PLAN_GATE oder DUPLICATE_GATE zählen nicht automatisch mehrere Prüferaufrufe.
- Die Bezeichnungen write_code=...FAILED sind die registrierten Schreibfehlercodes. Bei event=PERSISTED und affected=1 belegen diese Namen keinen tatsächlichen Datenbankfehler.
- topic_owner_rerun=false im lesenden Diagnoseabschnitt bedeutet nicht, dass zuvor kein Rücklauf stattgefunden hat.
- Historische Fehler vom 03.11. beweisen nicht die Ursache des abgeschlossenen Rücklaufs vom 06.11.
- Ein Versionsstring ersetzt keine Prüfung der tatsächlich eingesetzten Quelldateien.

## Der ursächliche Reparaturauftrag

Im bestehenden Rücklauf gültig gebundene externe Relevanz-/Titelentscheidungen übernehmen. Fachliche Relevanz und Titelqualität für unveränderte Eingaben nicht durch einen zweiten Entscheider erneut bewerten. Bei geänderten Eingaben dieselbe zuständige Prüfstelle verwenden. Alte Sperrentscheidungen ausschließlich zusammen mit aktueller Quellenbindung ersetzen.

Die vorhandene Kategoriezuordnung muss für die 50 Fälle zu einer nachweisbaren Entscheidung gelangen. Keine erfundenen Kategorien, keine Einzeltitel-Ausnahmen, keine pauschale Freigabe über einen fehlenden Kategorienentscheid hinweg.

Bestands- und Planungsschutz müssen genau einen fachlichen Besitzer haben. Echte Dubletten, Quellenänderungen und technische Titel-/Paketkollisionen bleiben geschützt. Keine Änderung der 87 Originaltitel, keine automatischen Zusatzartikel aus den weiteren Ideen.

**Noch kein Programmcode wurde in diesem Auftrag geändert.** Der vorhandene Diagnoseexport reicht für diese abgeschlossene Auswertung; für einen überprüfbaren Quellpatch ist die passende ausführbare Pluginquelle erforderlich. Die technischen Grenzen sind keine offene Frage der Diagnoseauswertung.

## Einmal gesicherte Quellen

- [Originaldiagnose](pste-gesamtdiagnose-2026-11-06.json), 1.372.286 Bytes, SHA256 5c2b20cdd13c7624790dd12219d3d473b32ec7bed9539b540e9ca98e512db952, Git-Blob 6cc0f1757dd91af540878ba2dd880394a2cb7393. Unverändert in den offiziellen Campus übernommen mit PR #637, Merge 22909573e1c5b7b000237cc299e3fd211f06eee0; dort erneut bytegenau nachgewiesen.
- [Maschinenlesbare ursprüngliche Gruppenauswertung](PSTE_MINI_REIMPORT_URSACHENBEFUND_20261106.json).
- Die aktuelle Zustandsautorität bleibt ausschließlich [../CURRENT_STATE.md](../CURRENT_STATE.md). Dieser Bericht ist Beleg und keine zweite Current- oder Workflow-Autorität.
