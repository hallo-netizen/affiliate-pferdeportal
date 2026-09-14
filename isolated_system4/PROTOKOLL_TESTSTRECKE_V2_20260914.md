# PROTOKOLL — SYSTEM 4 TESTSTRECKE V2

Ziel: **derselbe technische Weg wie Produktion vom Point-0 bis zur Parent-Chat-Datei.** Nur die fachliche Codex-Arbeit wird in der Teststrecke durch deterministische externe Research/Facts/Text/Repair-Eingaben ersetzt. Diese Fixtures liegen wie Live-Inputs außerhalb des Repositories und werden für eine reale Abnahme frisch erzeugt. Root, Supervisor, Worker-Dispatch, Controller, LT 6.8, PPM 6.7.9, Repair-Übergang, Batch und Handoff sind dieselben Produktionskomponenten.

## Positivstrecke

Pflichtreihenfolge:
`Machine Point-0 V2 → Root(index) → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → echtes LT/PPM → Same-Article-Repair → OUTPUT_GATE_REQUIRED → echter batch_gate collect → Handoff validate → canonicalize → inline-pack → inline-unpack → Bytegleichheit`.

Der positive Batch-Gate-Aufruf ist zwingend und darf nicht durch den Handoff-Validator ersetzt oder übersprungen werden.

## Historische Pflichtregressionen

Mindestens 22 Klassen bleiben dauerhaft Pflicht: fehlende Manifestbindung, leerer Quellenpool, falscher Source-Hash, HTTP 401, HTTP 403, falscher Head, Point-0-Tamper, Workspace im Repo, nichtleerer Workspace, fehlender Dispatch, Dispatch-Tamper, freie Webfreigabe, Änderung gebundener Quellenbytes, ungebundene Research-Daten, Fact-Quelle außerhalb Research, Evidenz nicht in Quelle, unbekannter PPM-Vertrag, Wortminimum, Inline-Designmutation, externer Link, unbekannte Fact-ID, zu großer Same-Article-Repair.

## Neue V2-Pflichtregressionen

Zusätzlich: Cross-Item-Research, Prewrite-Byte-Tamper, rehashter Linktausch, Runtime-Linktausch, Kategorieänderung, Artikelindex/Pool/Slot-Verwechslung sowie Source-Acquisition 200/401/403.

## Batch/Handoff negativ

Mindestens: vertauschte States, fehlender State, Body-Tamper, `publish_allowed=true`, Direct-Upload-Flag aus, Inline-Payload-Tamper.

Kein einzelner Teiltest ersetzt die Gesamtstrecke. Nach jeder Änderung am kritischen Manifest muss die komplette Positiv- und Negativstrecke erneut auf exakt dem aktuellen Remote-Head laufen.
