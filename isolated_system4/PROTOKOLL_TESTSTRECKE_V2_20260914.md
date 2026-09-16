# PROTOKOLL — SYSTEM 4 TESTSTRECKE V2

Ziel: **derselbe technische Weg wie Produktion vom Point-0 bis zur tatsächlich im Parent-Chat ausgegebenen WordPress-Importdatei.** Nur die fachliche Codex-Arbeit wird in der Teststrecke durch deterministische externe Research/Facts/Text/Repair-Eingaben ersetzt. Diese Fixtures liegen wie Live-Inputs außerhalb des Repositories und werden für eine reale Abnahme frisch erzeugt. Root, Supervisor, Worker-Dispatch, Controller, LT 6.8, PPM 6.7.9, Repair-Übergang, Batch, V2-Handoff, 107008 Final Review/Output Release, gebundener Chat-Delivery-Transport, PSERC-Import-Envelope/Recovery-Manifest, GitHub-ENDSTEMPEL und WordPress-Importformat-Prüfung bleiben die bestehenden Produktionskomponenten.

## Harte Abschlussbedingung — KEIN PASS OHNE CHAT-DATEI

Ein GitHub-Run, lokaler Lauf, Batch-/Handoff-PASS, Inline-Unpack oder eine bytegleiche Datei in `/tmp`, in einem Artifact oder im Repository ist **noch kein bestandener Gesamttest**. Solche Ergebnisse sind ausschließlich **TESTKANDIDAT / BRANCH_PREQUALIFICATION_PASS_PENDING_CANONICAL_107008_ENDSTEMPEL_CHAT**.

Der Gesamttest ist erst **PASS**, wenn **dieselbe finale, signierte ENDSTEMPEL-Importdatei tatsächlich im Parent-Chat als herunterladbare Datei ausgegeben wurde** und unmittelbar davor maschinell geprüft wurde, dass sie das korrekte WordPress-Importformat und alle für den direkten WordPress-Import erforderlichen Informationen enthält.

Verbindliche letzte Strecke:
`... → Batch → V2-Handoff → 107008 Final Review/Output Release → gebundener Chat-Delivery-Transport → bestehendes PSERC-Import-Envelope + Recovery-Manifest → signierter GitHub-ENDSTEMPEL → WordPress-Importformat-Prüfung → Chat-Datei-Ausgabe → Chat-Datei identisch zur geprüften Finaldatei → PASS`.

Pflichtbedingungen der Chat-Datei:
- echte finale signierte ENDSTEMPEL-Importdatei, keine Proof-/Log-/Wrapper-Datei, kein rohes `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` und kein ZIP als Ersatz;
- MIME/Dateiformat gemäß realem WordPress-Importvertrag;
- vollständiger Import-Payload einschließlich aller vom WordPress-Importer verlangten Artikel-, Identitäts-, Metadaten-, Produktionskontext- und Prüf-/Versionsinformationen;
- `publish_allowed=false` bleibt unverändert;
- Dateibytes bzw. SHA-256 müssen mit der unmittelbar zuvor geprüften Finaldatei übereinstimmen;
- die Chat-Antwort muss die Datei als tatsächlichen Download/Attachment bereitstellen. Ein Pfad, Dateiname, GitHub-Artifact oder behaupteter PASS genügt nicht.

Fehlt irgendeiner dieser Punkte, lautet der Status zwingend **NICHT BESTANDEN / CHAT_DELIVERY_PENDING**. Kein Worker, GitHub-Workflow, Testskript oder Nachbarchat darf vorher `PASS` für den Gesamttest behaupten.

## Branch-Vorqualifikation und kanonische Abschlussabnahme

Der System-4A-Hobbyraum-Branch darf die Produktionssicherheit nicht umgehen. Insbesondere bleiben die bestehenden Grenzen verbindlich:

- `output_release_gate.py` verlangt für die reale 107007/107008-Release-Strecke einen als aktuell bewiesenen `main`-Checkout;
- der 107007-Receipt-`batch_sha256` muss exakt dem offiziell gebundenen aktuellen Runtime-Batch entsprechen;
- die CURRENT_STATE darf nur durch den bestehenden Entrance-Gate-/State-Owner-Weg fortgeschrieben werden;
- der produktive PSERC-Signer darf nicht durch einen Testschlüssel ersetzt werden;
- der private ENDSTEMPEL-Schlüssel bleibt ausschließlich im vorhandenen GitHub-ENDSTEMPEL-Weg;
- kein manueller State-Umbau, keine Branch-Ausnahme, keine Receipt-Rekonstruktion und keine Alternativroute sind zulässig.

Daraus folgen zwei klar getrennte Stufen:

1. **Branch-Vorqualifikation:** kompletter System-4A-Weg bis zum validierten V2-Handoff einschließlich echter LT-/PPM-Läufe, Repair-, Batch-/Handoff-, 1..N-, WordPress-Importer-Vertrags- sowie positiver/negativer Downstream-Sicherheitsprüfungen. Ergebnis höchstens `BRANCH_PREQUALIFICATION_PASS_PENDING_CANONICAL_107008_ENDSTEMPEL_CHAT`.
2. **Gesamtabschluss:** erst auf einem sauber an den dann aktuellen `main` gebundenen Kandidaten und einem frisch über den bestehenden Intake gebundenen Runtime-Batch darf die reale Strecke 107007 → 107008 → PSERC-Finalpaket → Chat-Delivery → Recovery-Manifest → GitHub-ENDSTEMPEL → WordPress-Importformat-Prüfung → bytegleiche Parent-Chat-Datei ausgeführt werden. Erst danach ist `PASS` zulässig.

Ein Merge, Rebase oder eine Main-Neubindung ist **nicht** durch einen grünen Hobbyraum-Run ersetzt. Vor der kanonischen Abschlussabnahme müssen `main` und Kandidat frisch gegeneinander geprüft und ohne Überschreiben aktueller Main-Änderungen zusammengeführt werden.

## Positivstrecke

Pflichtreihenfolge für den Gesamtabschluss:
`Machine Point-0 V2 → Root(index) → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → echtes LT/PPM → Same-Article-Repair → OUTPUT_GATE_REQUIRED → echter batch_gate collect → V2-Handoff validate → 107008 Final Review/Output Release → gebundener Chat-Delivery-Transport → bestehendes PSERC-Import-Envelope + Recovery-Manifest → signierter GitHub-ENDSTEMPEL → WordPress-Importformat-Prüfung → Ausgabe derselben Datei im Parent-Chat → PASS`.

Der positive Batch-Gate-Aufruf ist zwingend und darf nicht durch den Handoff-Validator ersetzt oder übersprungen werden. Ebenso dürfen 107008, PSERC-Finalisierung, ENDSTEMPEL und reale WordPress-Importformat-Prüfung nicht durch einen lokalen Wrapper, ein Testsignat oder ein rohes Handoff ersetzt werden.

## Ursächliche Repair-/Owner-Invariante

Ein Befund eines echten späteren Prüfers darf **nicht allein wegen eines unbekannten oder nicht gelisteten Fehlercodes** terminal werden. Die Teststrecke muss zuerst die Fehlerklasse bestimmen und den Befund an den Besitzer der fehlererzeugenden Stufe zurückgeben.

Verbindlicher Ablauf für jeden fachlich bzw. inhaltlich reparierbaren Befund:
`echter Prüfer findet Fehler → Fehlerklasse bestimmen → Repair-Owner bestimmen → reale Erzeugerautorität dieses Owners nachweisen → exakt zur Erzeugerstufe zurück → dort reparieren/neuerzeugen → dieselben echten nachgelagerten Prüfer erneut ausführen → erst nach PASS der Prüfer weiter bis Batch/V2-Handoff/107008/PSERC/ENDSTEMPEL/finaler bytegleicher Datei → WordPress-Importformat-Prüfung → Chat-Datei-Ausgabe`.

**Owner bedeutet nicht automatisch reparierbar.** Ein Owner-Name ohne verfügbare reale Erzeugerautorität ist kein PASS. Fehlt die Autorität oder kann die gebundene Quelle den Fehler nicht selbst beheben, muss die Strecke zur nächsthöheren autoritativen Quelle zurück oder fail-closed blockieren. Ein Validator darf niemals durch sein Feld `expected`, einen Fehlertext oder einen historischen Code zum Erzeuger des Ersatzwerts werden.

Die Zuordnung darf **nicht** als Sammlung einzelner historischer Symptommuster implementiert oder getestet werden. Historische Codes dienen als Testvektoren; die Produktionsentscheidung muss aus Fehlerklasse, Feld/Artefakt und Besitzer folgen.

Mindestens folgende Owner-Klassen müssen positiv und negativ bewiesen werden:
`PARENT_TITLE_MACHINE`, `PARENT_CATEGORY_MACHINE`, `PARENT_ARTICLE_TYPE_MACHINE`, `PARENT_KEYWORD_MACHINE`, `PARENT_SLOT_MACHINE`, `SOURCE_ACQUISITION_MACHINE`, `PORTAL_LINK_MACHINE`, `RESEARCH_WORKER`, `FACTS_WORKER`, `CONTEXT_WORKER`, `DRAFT_WORKER` und `HARD_BLOCK`.

Für **jede tatsächlich reparierbare** Owner-Klasse ist Pflicht: absichtlicher Realfehler → echter Prüfer erkennt ihn → richtige Owner-Rückgabe → Reparatur durch die reale Erzeugerautorität → erneute Prüfung durch denselben echten Prüfer → vollständiger Lauf bis zur finalen bytegleichen ENDSTEMPEL-Datei → WordPress-Importformat-Prüfung → Ausgabe derselben Datei im Parent-Chat. Ein Test, der nur den Rückgabecode oder nur eine Remote-Datei prüft, genügt nicht.

Für Parent-Metadaten gilt zusätzlich die jetzt bewiesene Quellenhierarchie:
- `PARENT_TITLE_MACHINE`: nur deterministische Regelreparatur aus bereits gebundenem Titel/Keyword/Artikeltyp; keine freie Neuformulierung.
- `PARENT_CATEGORY_MACHINE`, `PARENT_ARTICLE_TYPE_MACHINE`, `PARENT_KEYWORD_MACHINE`, `PARENT_SLOT_MACHINE`: ein späterer Drift darf ausschließlich aus der **hashgebundenen Upstream-Metadaten-Projection** wiederhergestellt werden.
- Ist der vom echten Prüfer beanstandete Wert bereits byte-/wertgleich in dieser Upstream-Projection enthalten, kann die Projection sich nicht selbst korrigieren. Dann ist verbindlich `UPSTREAM_METADATA_SOURCE_REBUILD_REQUIRED` und der Rücksprung muss bis zum echten Redaktionsplan-/Fachworkflow-Producer gehen. Kein Chat-, Codex-, Validator-`expected`- oder Rekonstruktionsersatz.
- Die historische STARTMASTER0107-Herkunft belegt diese Trennung: Runtime-Snapshot = Projection mit `source_snapshot_filename`/`source_snapshot_sha256`; H8 Producer/Signer = Herkunfts-/Integritätsautorität, ausdrücklich keine Fach-/Qualitätsautorität.

`HARD_BLOCK` bleibt für Manipulation/Tamper, Hash-/Manifest-/Integritätsfehler, ungebundene Daten, Sicherheitsverletzungen, echte Tool-/Validator-Ausführungsfehler sowie unbekannte/nicht sicher klassifizierbare Fehler. Diese Klassen dürfen niemals in einen inhaltlichen Repair umgedeutet werden. Ebenso fail-closed: ein fachlich ungültiger Upstream-Metadatenwert, solange die echte weiter vorgelagerte Producer-Autorität nicht verfügbar ist.

Pflichtregression aus Realrun 2026-09-14: `PPM679_VALIDATOR_BLOCKED:BLOCKED_KNOWN_REGRESSION_PATTERN` nach zulässigen Same-Article-Reparaturen. Dieser konkrete Code ist nur ein Testvektor. Bewiesen werden muss ursächlich, dass ein reparierbarer PPM-Befund am Artikeltext zum `DRAFT_WORKER` zurückkehrt und danach derselbe echte PPM 6.7.9 erneut läuft. Ein bloßes Whitelisting dieses Codes ist ausdrücklich kein PASS.

Pflichtregression Parent-Titel: konsistent vor Point-0 gebundener Doppelpunkt-Titel → echter PPM 6.7.9 → `PARENT_TITLE_MACHINE`/`PARENT_LAUNCH` → deterministische Titelreparatur → alter versiegelter Point-0 bleibt unverändert → komplett neuer Point-0 → kompletter realer Weg erneut bis LT/PPM PASS, Batch, V2-Handoff und anschließendem kanonischem 107008/PSERC/ENDSTEMPEL-Abschluss → WordPress-Importformat-Prüfung → Chat-Datei-Ausgabe.

## Historische Pflichtregressionen

Mindestens 22 Klassen bleiben dauerhaft Pflicht: fehlende Manifestbindung, leerer Quellenpool, falscher Source-Hash, HTTP 401, HTTP 403, falscher Head, Point-0-Tamper, Workspace im Repo, nichtleerer Workspace, fehlender Dispatch, Dispatch-Tamper, freie Webfreigabe, Änderung gebundener Quellenbytes, ungebundene Research-Daten, Fact-Quelle außerhalb Research, Evidenz nicht in Quelle, unbekannter PPM-Vertrag, Wortminimum, Inline-Designmutation, externer Link, unbekannte Fact-ID, zu großer Same-Article-Repair.

## Neue V2-Pflichtregressionen

Zusätzlich: Cross-Item-Research, Prewrite-Byte-Tamper, rehashter Linktausch, Runtime-Linktausch, Kategorieänderung, Artikelindex/Pool/Slot-Verwechslung sowie Source-Acquisition 200/401/403.

Zusätzlich dauerhaft: reparierbarer PPM-Befund ohne bisher bekannten Prefix; falscher Repair-Owner; fehlender Owner; Repair ohne erneuten echten Prüferlauf; Repair mit Überspringen eines späteren Prüfers; unbekannter PPM-Code muss fail-closed bleiben; Integritäts-/Ausführungsfehler dürfen nicht als Content-Repair klassifiziert werden; Parent-Metadaten-Drift darf nur aus hashgebundener Upstream-Projection restauriert werden; falscher Projection-Hash blockiert; Non-Owner-Metadatenänderung blockiert; bereits in der Projection falscher Parent-Metadatenwert erzwingt Upstream-Producer-Rebuild.

## Batch/Handoff/Downstream negativ

Mindestens: vertauschte States, fehlender State, Body-Tamper, `publish_allowed=true`, Direct-Upload-Flag aus, Inline-Payload-Tamper, rohes V2-Handoff als WordPress-Import, falsches/mangelhaftes WordPress-Importformat, fehlende Importpflichtfelder, falscher Runtime-`batch_sha256`, nicht als aktueller `main` bewiesener Output-Release-Lauf, Testsignierer im produktiven PSERC-Finalizer, manipuliertes Recovery-Manifest/Import-Envelope/ENDSTEMPEL sowie Chat-Ausgabe einer Datei mit abweichenden Bytes/SHA-256.

Kein einzelner Teiltest ersetzt die Gesamtstrecke. Nach jeder Änderung am kritischen Manifest muss die komplette Positiv- und Negativstrecke erneut auf exakt dem aktuellen Remote-Head laufen. **Auch ein vollständig grüner Remote-Lauf auf dem Hobbyraum bleibt bis zur kanonischen 107008/PSERC/ENDSTEMPEL-Strecke und geprüften Dateiausgabe im Parent-Chat lediglich BRANCH-VORQUALIFIKATION / TESTKANDIDAT.**
