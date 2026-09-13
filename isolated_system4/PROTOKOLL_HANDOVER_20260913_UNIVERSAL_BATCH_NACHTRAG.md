# PROTOKOLL-NACHTRAG / ÜBERGABE — SYSTEM 4 UNIVERSAL BATCH — 2026-09-13

Status dieses Dokuments: **AKTUELLSTER WAS/WARUM-NACHTRAG** zum bestehenden `PROTOKOLL_HANDOVER_20260913_CODEX_STRICT_PIPELINE.md`. Es ist kein CURRENT_STATE. Die einzige aktuelle System-4-Statuswahrheit bleibt `isolated_system4/README.md`; der verbindliche Zielvertrag bleibt `ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`.

## 1. Anlass
Nach erneuter harter Prüfung des aktuellen PR-Heads wurde festgestellt, dass System 4 am Batch-/Ausgangsende noch produktive Altbindungen an **genau sieben Artikel** und an die Beitragsart **`Beratung`** enthielt. Zusätzlich bestanden obsolete Nebenwege für Git-Proof-Persistenz und Signing, die ebenfalls auf sieben Artikel zugeschnitten waren.

Diese Bindungen waren mit dem verlangten universellen Ziel unvereinbar und wurden entfernt.

## 2. Verbindlicher universeller Zustand
- Produktionsmenge = exakt die nichtleere Item-Menge des gebundenen Input-Snapshots.
- System 4 kennt **keine feste Artikelzahl** und **keine künstliche System-4-Obergrenze**: jeder reale endliche Batch `1..N` benutzt denselben Produktionsweg.
- Zahlen wie `1`, `7`, `25` und `1000` sind ausschließlich Regressionstestgrößen und niemals Produktionsvertrag.
- `article_type` kommt ausschließlich aus den gebundenen Metadaten.
- System 4 besitzt **keine Beitragsart-Whitelist**. `Beratung` ist nur ein vorhandener Typ mit bereits bekannten typspezifischen Regeln.
- Neue Beitragsarten dürfen keine Änderung an Controller, Batch-Gate oder Handoff benötigen. Ihre konkrete fachliche/designseitige Gültigkeit entscheiden ausschließlich die unveränderten autoritativen Textmaschine-/PPM-/Designregeln.

## 3. Tatsächlich geänderte aktive System-4-Stellen
### Mengenflexibilität
- `content_guard.py`: Batch-Distinctness akzeptiert Einzelbatches und indexiert Shingles einmalig, damit große Batches nicht durch unnötige Wiederholungsarbeit skaliert werden.
- `batch_repetition_guard.py`: Einzelbatch ist gültig; Paar-/Mehrheitsvergleiche greifen erst dort, wo mehrere Artikel existieren.
- `batch_gate.py`: sammelt exakt die gebundene Snapshot-Menge und gibt `PARENT_CHAT_WORDPRESS_HANDOFF_REQUIRED` statt des veralteten Signing-Nachfolgers zurück.
- `handoff_transport.py`: generischer Vertrag `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`, Artikelzahl `1..N`, kein `len==7`.
- Inline-Handoff V2 ist mehrteilig; die frühere einzelne 60k-Gesamtumschlaggrenze definiert keine maximale Produktionsmenge mehr.

### Beitragsartneutralität
- `design_guard.py`: vorhandene `ppm-type-*`-Bindung wird generisch aus dem gebundenen `article_type` abgeleitet.
- Die dokumentierte Beratung-H2-Regel bleibt eine typspezifische bestehende Schutzregel, aber keine Zulassungsliste.
- `handoff_transport.py` verlangt nur einen nichtleeren gebundenen `article_type`; kein Vergleich mehr gegen `Beratung`.

### Tote / widersprüchliche Nebenwege entfernt
Die folgenden aktiven System-4-Dateien wurden gelöscht, weil sie nicht zum aktuellen direkten unsigned V2-Handoff gehören und feste 7er-Bindungen enthielten:
- `proof_persistence_guard.py`
- `test_proof_persistence_guard.py`
- `signature_bridge.py`
- `test_signature_bridge.py`

Das ist keine Funktionskürzung des aktuellen Zielwegs: Repository-Handoff ist im V2-Vertrag verboten und Signing/ENDSTEMPEL ist für den aktuellen WordPress-Pfad ausgeschaltet.

## 4. Verträge aktualisiert
Aktualisiert wurden insbesondere:
- `AGENTS.md`
- `FULL_RULE_BATCH_TASK.md`
- `ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`
- `README.md`
- PR-Text als reiner Wegweiser
- `test_codex_economy_contract.py`
- Handoff-/Universal-/Batch-Gate-Regressionen

Der alte `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1` ist kein aktueller Produktionsvertrag mehr. Aktuell gilt `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`.

## 5. Bereits tatsächlich ausgeführte Teil-/Skalierungsbelege
Auf lokal rekonstruiertem System-4-Code wurden bereits erfolgreich geprüft:
- Content-/Design-/Universalregressionen: PASS;
- Mengen `1`, `3`, `7`, `25`, `1000` im neuen Handoff-Modell;
- gemischte Typen, darunter `Beratung`, `Produktvergleich`, `Pferderasse`, `Glossar Begriff`;
- `0` Artikel fail-closed;
- 1000er V2-Pack/Unpack mit mehrteiligem Transport;
- `batch_gate.collect_batch` für `1`, `3`, `25` und gemischte Typen.

Diese Teilbelege sind **kein Gesamt-PASS** des finalen Heads.

## 6. Aktuelle offene Beweisgrenze
System 4 bleibt BLOCKED, bis auf dem nach allen Änderungen exakt aktuellen PR-Head nachweislich ausgeführt sind:
1. kompletter `isolated_system4`-Unittestbestand;
2. NO-LEGACY;
3. lokaler positiver/negativer E2E vom Einstieg bis zum rekonstruierten V2-Elternchat-/WordPress-JSON;
4. autoritative PPM-/LanguageTool-Bindungen soweit der lokale Testzugang die unveränderten Pure-Tool-Inputs tatsächlich bereitstellt.

Der gebundene PPM-6.7.9-ZIP ist im Repository nachweislich vorhanden (`control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`, Git-Blob `151e9d6f908453dfc5b4acb497c4927a3f03c940`, Größe 1.614.485 Bytes). Der verbundene GitHub-Textconnector kann Binärblobs jedoch nicht dekodiert in den lokalen Container liefern. Daraus darf kein erfundener Hash-PASS abgeleitet werden; falls kein anderer zulässiger Abrufweg funktioniert, bleibt genau dieser Nachweis als Infrastrukturblocker ausgewiesen.

## 7. NEXT ACTION
- aktuellen PR-Head frisch binden;
- gesamten aktuellen `isolated_system4/**`-Stand bytegenau lokal rekonstruieren;
- vollständigen Testbestand und NO-LEGACY ausführen;
- E2E positiv/negativ ausführen;
- jeden echten FAIL nur an seiner ersten Ursache innerhalb des isolierten System-4-Codes reparieren;
- nach jeder Änderung den vollständigen Testbestand auf dem neuen Head wiederholen;
- erst bei vollständigem Beweis README/Protokoll auf PASS setzen;
- erst danach ausdrückliche Nutzerfreigabe für einen echten Codex-Lauf des konkret gebundenen Input-Batches einholen.

Kein Codex für Diagnose. Kein Merge. Kein Publish. Keine Änderung an Textmaschine, PPM-Fachregeln, PSERC/PSTE, WordPress-Plugin, Signaturschalter, Theme/CSS oder STARTMASTER0107.
