# SYSTEM 4 — ROOT-TO-FILE FINALER LOKALNACHWEIS — 2026-09-13

Status dieses Dokuments: **Belegdatei, keine zweite CURRENT_STATE**. Aktuelle System-4-Statuswahrheit bleibt `isolated_system4/README.md`.

## Anlass

Der frühere lokale E2E-Test bewies nur die interne System-4-Kette ab direktem `codex_entry.py`; er enthielt weder die reale Root-Instruktionsgrenze noch einen vollständig echten positiven LT-/PPM-Pfad. Der erste reale 1-Artikel-Codex-Lauf zeigte deshalb anschließend den fehlenden äußeren Einstieg mit `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`.

Eine erste Reparatur änderte Root-`AGENTS.md`. Diese Variante wurde verworfen, weil der echte Immutable-Base-Hardlock sie mit `IMMUTABLE_BASE_CHANGE_DETECTED:AGENTS.md` blockierte.

Die finale lokale Lösung verwendet stattdessen die Codex-Root-Datei `AGENTS.override.md`; Root-`AGENTS.md` bleibt unverändert.

## Bytebindung der geprüften ausführbaren Dateien

Die folgenden lokalen Testbytes wurden mit `git hash-object` gegen den aktuellen PR-Baum abgeglichen und waren identisch:

- `AGENTS.md` -> `8cc0fe89a9103c1e5a836f588b14563be02d3a07`
- `AGENTS.override.md` -> `e657cccf8c796942c0d9017cabadbd101d1cc6ab`
- `isolated_system4/root_entry.py` -> `918ee2e52593cc925c55dfdf4859e4ada95a3982`
- `isolated_system4/test_root_entry.py` -> `ca2dbebd122f448133772ea8e909e170c85dcd28`
- `isolated_system4/full_local_acceptance.py` -> `9ba4bae8568db8ad1669b928b715c32011997d47`
- `isolated_system4/production_checks.py` -> `4968746c7c46ff72778c0e4091e13bd673e39385`
- `isolated_system4/controller.py` -> `3f05125d74aa4b03276cf09dd4a21b2415e7c7e4`
- `isolated_system4/codex_entry.py` -> `e2e45cbed966aee94e57f5f2ed5049e87f3299e8`
- `isolated_system4/content_guard.py` -> `9d3451134866a7e2fdc0422d913619c13e20f29e`
- `isolated_system4/design_guard.py` -> `4a5bb76eff2a40b539aa8ba2a90208e970140154`
- `isolated_system4/batch_gate.py` -> `753dc105b0baacff21b67e0fb91826b5f0a7dcd4`
- `isolated_system4/batch_repetition_guard.py` -> `a4fc80417d485d31d4ce8307a467388968b53a73`
- `isolated_system4/handoff_transport.py` -> `9fa727810dcbfa49cd361e03e59c11f00d3d175b`
- `isolated_system4/LT68Worker.java` -> `8cc820006d0900862aeb15442e4a794d1485a419`
- `isolated_system4/live_fixture/wordpress_snapshot.json` -> `caa39e9b30e4f18a68d5338806dea1f164bf81bc`

Gebundene PPM-Datei:

- Git blob `151e9d6f908453dfc5b4acb497c4927a3f03c940`
- Größe `1614485` Bytes
- SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

Gebundenes LanguageTool 6.8 commandline.jar:

- SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`

## Vollständiger Unittestbestand

Ausgeführt ohne Codex:

`SYSTEM4_LANGUAGETOOL_JAR=<hashgleiches LT68 jar> PYTHONPATH=isolated_system4 python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v`

Ergebnis:

- **93 Tests**
- **93 PASS**
- **0 FAIL**
- **0 ERROR**
- Laufzeit: `11.872s`

Darin enthalten ist die Root-Eingangsprüfung mit positiven und negativen Fällen für `AGENTS.override.md`, Datei-/stdin-Einstieg, Repo-interne verbotene Pfade und ungültigen stdin-Input.

## Kompletter lokaler Root-bis-Datei-Lauf

Ausgeführt:

`SYSTEM4_LANGUAGETOOL_JAR=<hashgleiches LT68 jar> SYSTEM4_ACCEPTANCE_OUTPUT_DIR=<temp output> PYTHONPATH=isolated_system4 python3 isolated_system4/full_local_acceptance.py`

Terminaler Report:

- contract: `SYSTEM4_FULL_LOCAL_ROOT_TO_FILE_ACCEPTANCE_V2`
- status: `PASS`
- test_count: `8`
- `mocks_used=false`
- `codex_used=false`
- `merge_or_publish=false`
- Laufzeit: `19.104s`

### Positiver Gesamtweg

`POS_ROOT_STDIN_TO_FILE = PASS`

Tatsächlich durchlaufen:

`AGENTS.override/root contract -> root_entry start-stdin -> codex_entry/controller ingress -> research -> facts -> context -> draft -> real LT finding -> REPAIR_REQUIRED -> same article repair -> controller fullcheck -> real LT 6.8 PASS -> real PPM 6.7.9 PASS -> OUTPUT_GATE_REQUIRED -> batch_gate -> canonical SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2 -> inline-pack -> inline-unpack -> byte-exakte Parent-Chat-Datei`

Ergebnisdatei:

- SHA256 `997eb66e13ba9cb0f5387896486583b47da4a799e195cea3f98ae13b424cc58f`
- `66753` Bytes
- `1` Artikel
- Revision `2`
- Relay parts `1`

### Negative Gesamtbeweise

Alle PASS im Sinn von korrekt fail-closed:

1. `NEG_ROOT_BAD_STDIN` — kaputter Root-Input erzeugt keinen gültigen State.
2. `NEG_PUBLISH_AUTHORITY` — `publish_allowed=true` wird blockiert.
3. `NEG_FAKE_FACT` — erfundene Evidence wird vor Produktionskontext blockiert.
4. `NEG_DESIGN_DRIFT` — entfernte bestehende Tabellenklasse wird blockiert.
5. `NEG_HANDOFF_TAMPER` — manipuliertes Relay rekonstruiert keine Datei.
6. `NEG_BATCH_STATE_TAMPER` — nachträglich manipulierter Draft-Hash kommt nicht ins Batch-Gate.
7. `NEG_NO_LEGACY_RUNTIME` — System-4-Laufzeit enthält keine zugelassene Legacy-Orchestrierungsabhängigkeit.

## Immutable-Base-Nachweis

Die frühere Variante mit geänderter Root-`AGENTS.md` war korrekt rot und wurde verworfen.

Mit der finalen `AGENTS.override.md`-Lösung blieb Root-`AGENTS.md` bytegleich. Der GitHub-Workflow `Pferde Atelier Immutable Base Hardlock`, Run `34751016605`, Head `1df5de6dbc0bd26cdc2807006d0ce109e795b9ba`, endete **SUCCESS**.

Damit ist die System-4-Eingangslösung lokal bewiesen, ohne die immutable alte Eingangstür zu verändern.

## Beweisgrenze

Lokal bewiesen ist jetzt die komplette technische Kette vom branchgebundenen System-4-Root-Einstieg bis zur bytegenauen finalen WordPress-Datei — positiv und negativ, mit realem LT und realem PPM, ohne Mocking.

Nicht lokal beweisbar ist ausschließlich, ob die reale Codex-Cloud-Ausführung beim Checkout dieses PR-Branches die vorhandene `AGENTS.override.md` tatsächlich als Root-Instruktion lädt. Diese äußere Produkt-/Cloud-Grenze benötigt einen realen Codex-Lauf.

Gemäß `CODEX ECONOMY HARD RULE` wurde **kein** weiterer Codex-Lauf gestartet. Ein neuer Lauf erfordert ausdrückliche Nutzerfreigabe und darf dann ausschließlich der reale gebundene Artikelproduktionsnachweis sein.

Kein Merge. Kein Publish.
