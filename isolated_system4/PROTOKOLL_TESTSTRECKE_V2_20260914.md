# PROTOKOLL — SYSTEM 4 TESTSTRECKE V2

Ziel: **derselbe technische Weg wie Produktion vom Point-0 bis zur Parent-Chat-Datei.** Nur die fachliche Codex-Arbeit wird in der Teststrecke durch deterministische externe Research/Facts/Text/Repair-Eingaben ersetzt. Diese Fixtures liegen wie Live-Inputs außerhalb des Repositories und werden für eine reale Abnahme frisch erzeugt. Root, Supervisor, Worker-Dispatch, Controller, LT 6.8, PPM 6.7.9, Repair-Übergang, Batch und Handoff sind dieselben Produktionskomponenten.

## Positivstrecke

Pflichtreihenfolge:
`Machine Point-0 V2 → Root(index) → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → echtes LT/PPM → Same-Article-Repair → OUTPUT_GATE_REQUIRED → echter batch_gate collect → Handoff validate → canonicalize → inline-pack → inline-unpack → Bytegleichheit`.

Der positive Batch-Gate-Aufruf ist zwingend und darf nicht durch den Handoff-Validator ersetzt oder übersprungen werden.

## Ursächliche Repair-/Owner-Invariante

Ein Befund eines echten späteren Prüfers darf **nicht allein wegen eines unbekannten oder nicht gelisteten Fehlercodes** terminal werden. Die Teststrecke muss zuerst die Fehlerklasse bestimmen und den Befund an den Besitzer der fehlererzeugenden Stufe zurückgeben.

Verbindlicher Ablauf für jeden fachlich bzw. inhaltlich reparierbaren Befund:
`echter Prüfer findet Fehler → Fehlerklasse bestimmen → Repair-Owner bestimmen → exakt zur Erzeugerstufe zurück → dort reparieren → dieselben echten nachgelagerten Prüfer erneut ausführen → erst nach PASS weiter bis Batch/Handoff/bytegleicher Datei`.

Die Zuordnung darf **nicht** als Sammlung einzelner historischer Symptommuster implementiert oder getestet werden. Historische Codes dienen als Testvektoren; die Produktionsentscheidung muss aus Fehlerklasse, Feld/Artefakt und Besitzer folgen.

Mindestens folgende Owner-Klassen müssen positiv und negativ bewiesen werden:
`PARENT_TITLE_MACHINE`, `PARENT_CATEGORY_MACHINE`, `PARENT_ARTICLE_TYPE_MACHINE`, `PARENT_KEYWORD_MACHINE`, `PARENT_SLOT_MACHINE`, `SOURCE_ACQUISITION_MACHINE`, `PORTAL_LINK_MACHINE`, `RESEARCH_WORKER`, `FACTS_WORKER`, `CONTEXT_WORKER`, `DRAFT_WORKER` und `HARD_BLOCK`.

Für **jede** reparierbare Owner-Klasse ist Pflicht: absichtlicher Realfehler → echter Prüfer erkennt ihn → richtige Owner-Rückgabe → Reparatur → erneute Prüfung durch denselben echten Prüfer → vollständiger Lauf bis zur finalen bytegleichen Datei. Ein Test, der nur den Rückgabecode prüft, genügt nicht.

`HARD_BLOCK` bleibt ausschließlich für Manipulation/Tamper, Hash-/Manifest-/Integritätsfehler, ungebundene Daten, Sicherheitsverletzungen, echte Tool-/Validator-Ausführungsfehler sowie unbekannte/nicht sicher klassifizierbare Fehler. Diese Klassen dürfen niemals in einen inhaltlichen Repair umgedeutet werden.

Pflichtregression aus Realrun 2026-09-14: `PPM679_VALIDATOR_BLOCKED:BLOCKED_KNOWN_REGRESSION_PATTERN` nach zulässigen Same-Article-Reparaturen. Dieser konkrete Code ist nur ein Testvektor. Bewiesen werden muss ursächlich, dass ein reparierbarer PPM-Befund am Artikeltext zum `DRAFT_WORKER` zurückkehrt und danach derselbe echte PPM 6.7.9 erneut läuft. Ein bloßes Whitelisting dieses Codes ist ausdrücklich kein PASS.

## Historische Pflichtregressionen

Mindestens 22 Klassen bleiben dauerhaft Pflicht: fehlende Manifestbindung, leerer Quellenpool, falscher Source-Hash, HTTP 401, HTTP 403, falscher Head, Point-0-Tamper, Workspace im Repo, nichtleerer Workspace, fehlender Dispatch, Dispatch-Tamper, freie Webfreigabe, Änderung gebundener Quellenbytes, ungebundene Research-Daten, Fact-Quelle außerhalb Research, Evidenz nicht in Quelle, unbekannter PPM-Vertrag, Wortminimum, Inline-Designmutation, externer Link, unbekannte Fact-ID, zu großer Same-Article-Repair.

## Neue V2-Pflichtregressionen

Zusätzlich: Cross-Item-Research, Prewrite-Byte-Tamper, rehashter Linktausch, Runtime-Linktausch, Kategorieänderung, Artikelindex/Pool/Slot-Verwechslung sowie Source-Acquisition 200/401/403.

Zusätzlich dauerhaft: reparierbarer PPM-Befund ohne bisher bekannten Prefix; falscher Repair-Owner; fehlender Owner; Repair ohne erneuten echten Prüferlauf; Repair mit Überspringen eines späteren Prüfers; unbekannter PPM-Code muss fail-closed bleiben; Integritäts-/Ausführungsfehler dürfen nicht als Content-Repair klassifiziert werden.

## Batch/Handoff negativ

Mindestens: vertauschte States, fehlender State, Body-Tamper, `publish_allowed=true`, Direct-Upload-Flag aus, Inline-Payload-Tamper.

Kein einzelner Teiltest ersetzt die Gesamtstrecke. Nach jeder Änderung am kritischen Manifest muss die komplette Positiv- und Negativstrecke erneut auf exakt dem aktuellen Remote-Head laufen.
