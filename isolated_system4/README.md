# System 4 — Point-0 V2

Aktuelle Architektur: **Maschine setzt die Schienen → Codex recherchiert fachlich/schreibt → Maschine prüft und entscheidet PASS/BLOCK.**

Produktionsweg:

`Chat → machine-owned sources + prewrite rails → Point-0 V2 → Root → Supervisor → Worker-Dispatch → Codex Research/Facts/Context/Draft → LT 6.8 + PPM 6.7.9 → Repair → Batch → V2-Handoff → bytegleiche Parent-Chat-Datei`

Wesentliche V2-Eigenschaften:
- eigener Source-Pool pro Artikel;
- Kategorie, Links und Quality-Binding vor Codex versiegelt;
- freie Codex-Websuche aus;
- Prewrite-Mutation aus;
- Root/Supervisor/Dispatch binden Artikelindex und `plan_slot`;
- gleicher Pfad für `1..N`;
- kein Merge/Publish ohne separate Freigabe.

## Teststrecke

`live_parity_v2.py` ist die verbindliche Nullpunkt→Datei-Paritätsstrecke. Sie ersetzt nur Codex durch die eingecheckten deterministischen Testarbeiter-Eingaben. Die echten Root-/Supervisor-/Controller-/LT-/PPM-/Batch-/Handoff-Komponenten bleiben unverändert.

Ausführung:

`SYSTEM4_LANGUAGETOOL_JAR=/path/to/hash-bound/languagetool-commandline.jar SYSTEM4_LIVE_PARITY_FIXTURE=/path/outside/repo python3 isolated_system4/live_parity_v2.py prepare /tmp/system4-run`

Danach `item ... 0..N-1` und abschließend `finalize ...`. Die Fixture-Eingaben liegen bewusst außerhalb des Repositories und werden für reale Abnahmen frisch erzeugt.

Pflicht zusätzlich:

`python3 isolated_system4/test_point0_v2.py`

Der historische Negativkatalog ist in `PROTOKOLL_TESTSTRECKE_V2_20260914.md` festgeschrieben und darf bei späteren Änderungen nicht reduziert werden.
