# H7 PROTOTYP – HARD AUDIT „ZWANGSJACKE“
Stand: 2026-08-31

## Ziel
Ab der ersten Sekunde darf kein frei erzeugtes oder frei umgeleitetes Fachartefakt autoritativ in die Artikelproduktion gelangen. Chat-/Host-Aktionen ausserhalb der Single-Door-Kette duerfen niemals Produktionsautoritaet erhalten.

## Einfacher Begriff „Produktionspaket“
Das Produktionspaket ist der versiegelte Arbeitskoffer fuer einen gebundenen Batch. Es enthaelt die gebundenen Recherche-/Fact-Pack-, Produktionsplan- und Workflow-Freigabe-Bestandteile samt Hashes und Signatur. Es ist kein freier Chattext und kein beliebiger Import.

## Harte Ist-Pruefung
1. `single_door_boundary.py` gibt dem Worker nur den opaken ROOM_TOKEN plus exakt eine erzwungene parameterlose Capability. Freier semantischer Worker-Input und Parallelaufrufe sind ausgeschlossen.
2. `H7_PROJECT_EXECUTION_BOUNDARY.json` weist korrekt darauf hin, dass Repository-Code vom ChatGPT-Host bereitgestellte Tools nicht physisch abschalten kann. Deshalb muss die Garantie auf Akzeptanzebene gelten: ausserhalb der Single-Door-Kette erzeugte Artefakte bleiben nicht autoritativ.
3. Aktuelle Luecke: `READY_WAITING_PACKAGE` fuehrt nach `R_PRE_001`, aber `R_PRE_001` verlangt bereits ein signiertes `PSERC_APPROVED_PRODUCTION_PACKAGE_V1`. Der Erzeugungsweg dieses Pakets liegt damit vor dem heute wirksamen produktiven Single-Door-Pfad.
4. `production_continuity_guard.py` beweist Reihenfolge/Vollstaendigkeit des Batches, aber nicht selbst, dass fuer jedes Item alle Fach-/Qualitaetsgates tatsaechlich PASS geliefert haben. Ein reines „completed_item_id“ ist daher als Qualitaetsbeweis nicht ausreichend.
5. Signatur/Hash beweisen Integritaet und Authentizitaet eines Pakets, aber nicht automatisch seine fachliche Qualitaet. Die Signierfreigabe muss deshalb an vollstaendige Gate-Receipts gebunden sein.
6. Gegen Replay/Stale-Artefakte muss das akzeptierte Paket zusaetzlich exakt an aktuellen Batch, Generation, Source-Snapshot und die fuer diesen Lauf gueltigen Regel-/Gate-Hashes gebunden sein.

## Optimierter allererster Schritt
Keine Voranalyse, kein Protokoll, kein Branch, keine Dateisuche vor dem Einstieg.

Erster technischer Befehl eines Produktionschats:

`python3 control/single-door-boundary/project_single_door_entry.py status`

Dieser Entry validiert intern `control/CURRENT_STARTMASTER.json`, `free_chat_execution_authority=false`, den gebundenen `gate_ref` und den Runtime-State. Dadurch entfaellt die vorherige manuelle Navigationssuche.

## Prototyp-Zielbild ohne Inhaltsaenderung
A. Der erste gebundene Raum muss einen bereits gebundenen Batch-/Snapshot-Handle akzeptieren, NICHT ein vom Chat angeliefertes fertiges Produktionspaket.
B. Jede eventuell vor `R_001` notwendige Preproduction-Arbeit wird serverseitig in eine geschlossene Single-Door-Unterkette verschoben.
C. Kein semantisches Artefakt darf in einen Folgeraum gelangen, wenn es nicht den Hash/Receipt seines direkten gebundenen Vorgaengers traegt.
D. Die Signierstelle darf ein Produktionspaket nur dann signieren, wenn die fuer diesen Paketstand vorgeschriebenen Gate-Receipts vollstaendig und PASS sind.
E. Der Runtime-Attach akzeptiert nur ein Paket mit gueltiger Signatur UND gueltiger Herkunftskette fuer den exakt aktuellen Batch/Generation/Snapshot/Ruleset.
F. WordPress-/Publish-Schreiben bleibt erst hinter der vorhandenen finalen Review-/Publish-Freigabe moeglich.
G. BLOCKED oder USER_ACTION_REQUIRED besitzen keinen alternativen Erfolgsweg.

## Muss vor Implementierung bewiesen werden
- Positivtest: echter Batch von leerem Preproduction-State bis `RUNTIME_INPUTS_BOUND` ausschliesslich ueber gebundene Raeume.
- Negativtest: frei im Chat erzeugtes Paket wird trotz formal gueltiger JSON-Struktur abgelehnt.
- Negativtest: altes gueltiges Paket eines anderen Laufs/Generation wird abgelehnt.
- Negativtest: fehlendes einzelnes Qualitaets-/Fach-Receipt verhindert Signatur und Fortschritt.
- Negativtest: manipuliertes Ruleset / geaenderter Snapshot / geaenderte Batch-Metadaten blockieren.
- Negativtest: Chatwechsel ohne gueltiges letztes Receipt kann keinen Raum ueberspringen.
- Gesamtworkflowtest: echter 7er-Batch bis finalem Review; keine Fachregel wird geaendert und kein Auto-Publish erfolgt.

## Kritische Schlussfolgerung
Nur das Verschieben der Paketbildung „hinter die erste Tuer“ reicht NICHT. Zusaetzlich muss die Herkunfts-/Receipt-Kette bis zur Qualitaetsfreigabe geschlossen sein. Erst dann kann ein frei handelnder Chat zwar ausserhalb des Systems Text erzeugen, aber diesen technisch nicht mehr in den autoritativen Produktionslauf einschleusen.
