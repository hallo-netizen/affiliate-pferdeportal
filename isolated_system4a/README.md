# SYSTEM 4A — CURRENT STATE

STATUS: **TEST ONLY / BLOCKED / KEIN MERGE / KEIN PUBLISH**

Diese Datei ist die **eine aktuelle 4A-Statuswahrheit**.

## Aktueller Stand

PR #255, Branch `hobbyroom/system4a-capsule-v1-20260913`, basiert auf dem aktuellen Remote-System-4-Stand von PR #238 (`28b1bd82af5ccbe5869bf83318ae73d2191bd132`).

Der frühere lokal vollständig grüne Punkt-0/Supervisor-Kandidat `cd6c134a3ee27f4535ea91bfe6cc223a34c9eb25` ist als Beweis historisch gültig: 40/40 gezielte Positiv-/Negativfälle, kompletter Null-bis-Datei-Lauf, echter LT 6.8, echter PPM 6.7.9, Batch, V2-Handoff und bytegleiche Parent-Chat-Rekonstruktion. Ein zusätzlicher kompletter 1-Artikel-Lauf ohne Codex war ebenfalls PASS.

Aber: Der exakte finale `controller.py` dieses lokalen Kandidaten ist weder als Remote-Blob noch als Library-/Patch-Artefakt bytegenau wiederherstellbar. Sechs andere neue Runtime-Blobs sind vorhanden, reichen aber allein nicht für einen gültigen Runtime-Tree. Deshalb werden sie **nicht teilweise** an PR #238 gehängt.

Konsequenz: Der alte Kandidat wird nicht nachgebaut und anschließend fälschlich als bytegleich bezeichnet. Es wird ein **neuer Kandidat** erzeugt und vollständig neu bewiesen.

## Verbindliche Teststrecke V3

`isolated_system4a/chat_to_file_full_acceptance.py`

Vertrag: `SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_V3`.

Start ist ausschließlich der **Rohauftrag im Parent-Chat**. Der Testinput darf keine maschineneigenen Produktionsbindungen vorgeben: kein Titel, Target Keyword, Kategorie, Plan-Slot, Linkset, Quality Binding, Prüferfeld oder PASS.

Verbindlicher Zielweg:

`Parent-Chat-Rohauftrag -> Runtime-Identität -> Punkt 0 -> Root start-point0 -> Supervisor -> Worker-Dispatch -> Research -> Facts -> Context -> Maschinen-Bindung Titel/Keyword/Kategorie/Slot/3 Links/Textmaschinenvertrag -> Draft -> echtes LT 6.8 -> Same-Article-Repair -> echtes PPM 6.7.9 -> Same-Article-Repair -> Artikel-PASS -> Batch -> SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2 -> Inline-Pack -> Parent-Chat-Unpack -> bytegleiche Datei im Parent-Chat`

Kein Ersatzweg darf diese Strecke simulieren.

## Neue Freigaberegel

V3 ist absichtlich **nicht mehr auf `cd6c134a…` festgenagelt**. Ein Kandidat wird nur akzeptiert, wenn `isolated_system4/CURRENT_PROVEN_RUNTIME_MANIFEST.json` mit Vertrag `SYSTEM4_PROVEN_RUNTIME_MANIFEST_V2` auf exakt demselben Head bindet:

- alle kritischen Runtime-Dateien einschließlich `controller.py`, Punkt-0, Supervisor, Worker-Dispatch, Checker, Batch und Handoff;
- vollständige historische Fehlermatrix mit mindestens allen 36 bekannten Live-Fluchtklassen, `passed == total`, `failed == 0`;
- vollständiger Null-bis-Datei-PASS auf demselben Head;
- echte LT-6.8-Ausführung;
- echte PPM-6.7.9-Ausführung;
- Batch PASS;
- Inline-Unpack PASS;
- bytegleiche Parent-Chat-Rekonstruktion;
- genau ein hashgebundener `chat_to_file_entry`;
- `simulation_and_live_same_entry=true`.

Erst danach darf die 1–3-Artikel-Simulation starten.

## Historische Fehlerbindung

Der Gate katalogisiert 36 Live-Fluchtklassen. Dazu gehören insbesondere frühere Lücken wie HTTP-401-Webruntime, Root-/Manifest-Abweichungen, Cross-UID-/Python-Pfad, Worker-Factory-Signaturdrift, Worker ohne Antwort, ungebundene Research-Evidence, vorgebundene Quality-/Link-Werte, `PPM679_QUALITY_BINDING_MISSING`, falscher Slot/Kategorie/Link, Fact-ID-/Trace-Probleme, fehlende echte LT-/PPM-Ausführung, Same-Article-Repair-Kontinuität, Batch-Reihenfolge sowie Handoff-/Inline-/Parent-Chat-Manipulation.

## 3-Artikel-Simulation ohne Codex

Rohauftrag:

`isolated_system4a/testdata/CHAT_TRIGGER_3_ARTICLES_NO_CODEX_20260914.json`

1. `Pferd im Regen sicher verladen`
2. `Sattel nach der Winterpause sicher kontrollieren`
3. `Putzzeug hygienisch und trocken lagern`

Der Rohauftrag enthält keine fertigen Produktionsbindungen.

Die Simulation bleibt aktuell korrekt BLOCKED, weil noch kein neuer vollständig bewiesener System-4-Runtime-Head mit `SYSTEM4_PROVEN_RUNTIME_MANIFEST_V2` existiert. Es wurden daher keine Artikel, LT-/PPM-Pässe oder Handoffs vorgetäuscht.

## Prüfabhängigkeiten

Die echten Prüfer bleiben unverändert:

- LanguageTool 6.8 SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`;
- PPM 6.7.9 SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`.

Das PPM-ZIP ist aus dem vorhandenen Library-Manifest und sieben hashgebundenen Teilen vollständig rekonstruierbar. Keine Ersatzprüfung ist zulässig.

## NEXT ACTION

1. Neuen System-4-Kandidaten aus dem letzten exakt bekannten Controller-Stand plus den vorhandenen Punkt-0/Supervisor-Bausteinen erstellen — als **neuen** Kandidaten, nicht als vermeintliche Rekonstruktion von `cd6c134a…`.
2. Lokal komplette historische Positiv-/Negativstrecke und Null-bis-Datei-Strecke mit echten LT-/PPM-Abhängigkeiten ausführen.
3. Erst nach Gesamt-PASS die tatsächlich getesteten Bytes atomar an PR #238 binden und `CURRENT_PROVEN_RUNTIME_MANIFEST.json` aus exakt diesen Bytes erzeugen.
4. Danach V3 auf genau diesem Remote-Head erneut vollständig ausführen.
5. Danach die drei Rohartikel ohne Codex komplett bis zur bytegleichen Parent-Chat-Datei schicken.

Kein Merge. Kein Publish. `publish_allowed=false`.
