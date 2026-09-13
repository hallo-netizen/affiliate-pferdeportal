# SYSTEM 4 — TESTNACHWEIS UNIVERSAL PREFLIGHT — 2026-09-13

Status dieses Dokuments: **Belegdatei, keine zweite CURRENT_STATE**. Die aktuelle System-4-Statuswahrheit bleibt ausschließlich `isolated_system4/README.md`.

## Gebundener Prüfstand

Ausgangspunkt des vollständigen Prüfversuchs war PR #238, Branch `hobbyroom/system4-true-single-room-v1`, Head `8da5a3f45ff42d3fae652d0a64071a9ea10770a4`.

Der ausführbare System-4-Kern und die aktuellen `test_*.py`-Dateien wurden gegen ihre GitHub-Blob-SHAs abgeglichen. Insbesondere wurde die zunächst lokal abweichende `batch_gate.py` anschließend bytegleich auf Blob `753dc105b0baacff21b67e0fb91826b5f0a7dcd4` rekonstruiert; `test_draft_bound_rebind.py` wurde bytegleich auf `f7f43264de3f50d90fb58558df00a6d590507771` nachgezogen.

## Tatsächlich ausgeführte Prüfungen

### Universalität
Frisch positiv geprüft:
- 1 Artikel;
- 3 Artikel;
- historische 7er-Fixture;
- 25 Artikel;
- 1000 Artikel;
- gemischte Beitragsarten;
- neue, nicht in System 4 vorab freigeschaltete Beitragsarten;
- 0 Artikel als Negativfall -> fail-closed.

Damit ist die frühere feste Bindung auf `7` bzw. `Beratung` im aktuellen System-4-Laufzeit-/Handoffvertrag nicht mehr vorhanden. Die 7er-`Beratung`-Fixture bleibt ausschließlich Regressionsevidenz.

### NO-LEGACY
Frisch ausgeführt über `production_checks.no_legacy_runtime_dependencies(...)`:
- `status = PASS`
- `legacy_import_count = 0`

### Einzelne aktuelle Tests
Vor dem Gesamtlauf wurden die aktuellen Teilstrecken separat ausgeführt, darunter:
- Content-/Design-/Universal-/Codex-Economy-Tests;
- Indexed Ingress;
- Draft-Rebind;
- Release Boundary;
- Repair Continuity;
- Batch Gate;
- Handoff Transport;
- lokaler positiver/negativer E2E.

Alle ausführbaren Logikpfade waren PASS.

### Vollständiger Testlauf
Ausgeführt:

`PYTHONPATH=isolated_system4 python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v`

Ergebnis:
- **87 Tests insgesamt**
- **86 PASS**
- **1 FAIL**
- kein zweiter Fehler/Fail.

Einziger FAIL:
`test_authoritative_textmachine_bindings_are_unchanged_from_proven_full_rule_pass`

Konkrete Ursache:
`ppm_path.is_file() == False`

Der Testcontainer enthält die gebundene Binärdatei
`control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`
nicht physisch.

GitHub bestätigt die Datei im gebundenen Repository/Head als Blob `151e9d6f908453dfc5b4acb497c4927a3f03c940`. Der aktuelle System-4-Code bindet den erwarteten Paket-SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`. Der verfügbare GitHub-Connector kann die Binärbytes jedoch nicht in den lokalen Testcontainer materialisieren; `fetch_blob` endet beim Binärinhalt mit UTF-8-Decodierfehler. Auch im lokalen Arbeitsumfeld wurde keine vorhandene Kopie gefunden.

Das ist deshalb **kein behaupteter PPM-PASS und kein System-4-Gesamt-PASS**. Es ist ein konkreter lokaler Infrastruktur-/Materialisierungsblocker für genau einen Bindungsnachweis.

## Lokaler E2E-Befund
Der aktuelle `test_local_end_to_end_chat_handoff.py` wurde ausgeführt.

Ausführbare E2E-Logik:
- positiver Weg vom Codex-Einstieg über gebundene Research/Facts/Context/Draft/Fullcheck-Mocks bis Batch-Gate und exakter V2-Elternchat-Rekonstruktion: PASS;
- erfundener Fact: BLOCKED/PASS des Negativtests;
- Design-Drift vor Fullcheck: BLOCKED/PASS des Negativtests;
- historische artikelübergreifende Template-Wiederholung am finalen Handoff: BLOCKED/PASS des Negativtests.

Der fünfte E2E-Test ist ausschließlich an der fehlenden lokalen PPM-ZIP-Datei blockiert.

## Beweisgrenze
Daraus darf aktuell nur gefolgert werden:
- Universalitätskorrektur 1..N: lokal bewiesen;
- keine System-4-Beitragsart-Whitelist: lokal bewiesen;
- aktuelle System-4-Logiktests: 86/86 ausführbare Tests PASS;
- NO-LEGACY: PASS;
- vollständiger Gesamt-PASS: **NEIN**, weil der reale lokale PPM-Paket-Bindungsnachweis in diesem Container mangels Binärdatei nicht ausgeführt werden konnte.

Kein Codex-Produktionslauf wurde gestartet. Kein Merge. Kein Publish. Textmaschine, PPM, PSERC/PSTE, WordPress-Plugin und Design wurden nicht verändert.
