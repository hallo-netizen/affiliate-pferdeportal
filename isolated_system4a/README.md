# SYSTEM 4A — CURRENT STATE

STATUS: **TEST ONLY / BLOCKED / KEIN MERGE / KEIN PUBLISH**

Diese Datei ist die **eine aktuelle 4A-Statuswahrheit**.

## Aktueller Remote-Stand

PR #255, Branch `hobbyroom/system4a-capsule-v1-20260913`.

4A wurde technisch auf den aktuellen Remote-Stand von System 4 PR #238, Head `28b1bd82af5ccbe5869bf83318ae73d2191bd132`, gezogen. Das beseitigt die alte 4A-Basisabweichung, ist aber **noch keine Abnahme**.

Der entscheidende Blocker liegt jetzt offen vor: Der lokal vollständig getestete System-4-Punkt-0/Supervisor-Kandidat `cd6c134a3ee27f4535ea91bfe6cc223a34c9eb25` ist weiterhin nicht vollständig atomar auf dem Remote-System-4-Codebaum gebunden. Insbesondere fehlen im aktuellen Remote-Codebaum bereits neue Runtime-Dateien wie `isolated_system4/point0_snapshot.py`; der vollständige getestete `controller.py`-Stand ist ebenfalls nicht durch einen aktuellen Runtime-Manifest gebunden.

Deshalb ist jeder aktuelle Null-bis-Ende-PASS auf dem Remote-Stand verboten.

## Neue verbindliche Teststrecke 2026-09-14

Neu eingerichtet:

`isolated_system4a/chat_to_file_full_acceptance.py`

Vertrag: `SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_V2`.

Die Strecke beginnt ausdrücklich mit dem **Rohauftrag aus dem Parent-Chat**. Der Chat-Testinput darf nur Themenwünsche enthalten. Folgende Produktionsbindungen dürfen NICHT vorgegeben werden:
- Titel;
- Target Keyword;
- Kategorie;
- Plan-Slot;
- interne Links;
- Quality-/Textmaschinen-Bindung;
- Prüfer-/PASS-Felder.

Diese Werte müssen erst innerhalb der maschinellen Live-Strecke entstehen.

Verbindlicher Zielweg:

`Parent-Chat-Rohauftrag -> Runtime-Identität -> Punkt 0 -> Root start-point0 -> Supervisor -> Worker-Dispatch -> Research -> Facts -> Context -> Maschinen-Bindung von Titel/Keyword/Kategorie/Slot/3 Links/Textmaschinenvertrag -> Draft -> echtes LT 6.8 -> Same-Article-Repair falls nötig -> echtes PPM 6.7.9 -> Same-Article-Repair falls nötig -> Artikel-PASS -> Batch -> SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2 -> Inline-Pack -> Parent-Chat-Unpack -> bytegleiche Datei im Parent-Chat`

Kein Test-Ersatzweg darf diesen Pfad nachbilden. Der Gate akzeptiert nach der Runtime-Identitätsprüfung ausschließlich einen hashgebundenen `chat_to_file_entry`, der zugleich der spätere Live-Einstieg ist.

## Historische Fehlerbindung

Der neue Gate katalogisiert **36 Live-Fluchtklassen**, darunter insbesondere die Fehler, die frühere grüne Teststrecken nicht abgedeckt hatten:
- falsche/partielle Runtime-Bytes;
- Root-/Branch-/Manifest-Abweichungen;
- Cross-UID-Workerpfad und privater Python-Interpreter;
- Worker-Factory-Signaturdrift;
- Worker beendet sich ohne Antwort;
- vorgebundene `quality_binding` / Runtime-Links;
- `PPM679_QUALITY_BINDING_MISSING`;
- falsche/nichtkanonische Kategorie bzw. Plan-Slot;
- fremde Fact-ID;
- fehlende echte LT-/PPM-Ausführung;
- synthetischer/vorgefertigter PASS;
- Same-Article-Repair bricht Kontinuität;
- Batch Drop/Duplikat/Reihenfolgefehler;
- Handoff-/Inline-/Parent-Chat-Manipulation;
- `publish_allowed != false`.

## 3-Artikel-Simulation ohne Codex

Rohauftrag angelegt:

`isolated_system4a/testdata/CHAT_TRIGGER_3_ARTICLES_NO_CODEX_20260914.json`

Drei Themen:
1. `Pferd im Regen sicher verladen`
2. `Sattel nach der Winterpause sicher kontrollieren`
3. `Putzzeug hygienisch und trocken lagern`

Der Testinput enthält absichtlich **keine** fertigen Produktionsbindungen.

### Tatsächlicher erster Testbefund

Der Test stoppt korrekt **vor Punkt 0 und vor jeder Artikelarbeit**:

`SYSTEM4A_CHAT_TO_FILE_FULL_ACCEPTANCE_BLOCKED:CURRENT_RUNTIME_FILE_MISSING:point0_snapshot.py`

Zusätzlich fehlt der zwingende `isolated_system4/CURRENT_PROVEN_RUNTIME_MANIFEST.json`, der insbesondere den vollständig getesteten `controller.py` und den identischen späteren `chat_to_file_entry` binden muss.

Das ist ein gewollter fail-closed Befund und **kein PASS**. Die drei Artikel wurden deshalb nicht erzeugt; LT, PPM, Batch und Handoff wurden nicht vorgetäuscht.

## Bisheriger 4A-No-Codex-Beweis — nur historischer Altstand

Für den früher exakt gebundenen 4A-No-Codex-Vertrag wurden 27/27 historische Negativtests, zwei Null-bis-Ende-Läufe, echte LT-6.8-/PPM-6.7.9-Prüfung, Same-Article-Repair, Batch, V2-Handoff und bytegleiche Parent-Chat-Rekonstruktion bewiesen.

Diese Beweise bleiben gültige historische Nachweise ihrer damaligen Bytes. Sie sind **keine aktuelle Abnahme** für den Punkt-0/Supervisor-Zielstand.

## NEXT ACTION

1. Den vollständig lokal getesteten System-4-Kandidaten inklusive des großen `controller.py` atomar und bytegleich auf PR #238 übertragen.
2. Auf genau diesem Remote-Codebaum `CURRENT_PROVEN_RUNTIME_MANIFEST.json` aus den tatsächlich getesteten Git-Blobs erzeugen; nichts schätzen.
3. Darin exakt einen `chat_to_file_entry` binden, der derselbe Einstieg für Simulation und späteren Live-Lauf ist.
4. Danach denselben neuen 4A-Gate erneut ausführen: zuerst komplette historische Negativstrecke, danach die 3-Artikel-No-Codex-Simulation vollständig bis zur Parent-Chat-Datei.
5. Erst wenn echte LT 6.8 + echte PPM 6.7.9 + Batch + V2 + Inline-Unpack + bytegleiche Parent-Chat-Datei auf denselben Bytes PASS sind, darf `TESTS: PASS` gesetzt werden.

Kein Merge. Kein Publish. `publish_allowed=false`.
