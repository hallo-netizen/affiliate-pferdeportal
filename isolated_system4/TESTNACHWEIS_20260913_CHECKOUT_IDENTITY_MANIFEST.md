# SYSTEM 4 — CHECKOUT-IDENTITY / ROOT-EINSTIEG — TESTNACHWEIS 2026-09-13

Status dieses Dokuments: **Belegdatei, keine zweite CURRENT_STATE**. Aktuelle Statuswahrheit bleibt `isolated_system4/README.md`.

## Ausgangsfehler aus realem Codex-Lauf

Der reale 1-Artikel-Lauf erreichte die System-4-Tür, stoppte aber bei:

`SYSTEM4_HARD_BLOCKER:ROOT_ENTRY_BRANCH_NOT_SYSTEM4`

Quelle im Lauf:

`python3 isolated_system4/root_entry.py start-stdin /tmp/system4-one-article-production`

Danach wurden keine Recherche, Facts, Drafts, Prüfer, Batch-Gates oder Handoffs gestartet.

Der vorherige lokale Test war an dieser Stelle unvollständig: Implementierung und Acceptance-Test verlangten beide den symbolischen Branchnamen `hobbyroom/system4-true-single-room-v1`. Ein Codex-/PR-Checkout ohne genau diesen symbolischen Namen war nicht positiv getestet worden.

## Korrektur

Die symbolische Branch-Namensprüfung wurde vollständig aus dem Root-Einstieg entfernt.

Die Checkout-Identität wird jetzt fail-closed über den **tatsächlich geladenen kritischen System-4-Inhalt** gebunden.

Der Root-Einstieg berechnet einen SHA256-Manifestwert über die kritischen Dateien:

- `AGENTS.md`
- `AGENTS.override.md`
- `isolated_system4/root_entry.py`
- `isolated_system4/codex_entry.py`
- `isolated_system4/controller.py`
- `isolated_system4/content_guard.py`
- `isolated_system4/design_guard.py`
- `isolated_system4/production_checks.py`
- `isolated_system4/batch_gate.py`
- `isolated_system4/batch_repetition_guard.py`
- `isolated_system4/handoff_transport.py`
- `isolated_system4/LT68Worker.java`

Zusätzlich gilt:

- Git-Root muss exakt das Repository sein;
- HEAD muss existieren;
- alle kritischen Dateien müssen getrackt sein;
- jede Änderung an einer kritischen Datei blockiert;
- der gebundene Snapshot muss `system4_root_manifest_sha256` enthalten;
- fehlender, ungültiger oder abweichender Manifestwert blockiert;
- der symbolische Branchname ist **keine** Zulassungsbedingung mehr.

Gebundener Manifestwert des geprüften Kandidaten:

`3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

## Dauerhafte Root-Tests

`isolated_system4/test_root_entry.py`

Positiv ausgeführt:

1. kanonischer benannter System-4-Branch;
2. beliebiger anderer symbolischer Branchname (`codex/pr-238-checkout`);
3. **detached HEAD / leerer Branchname**;
4. anderer Commit bei identischen kritischen System-4-Bytes;
5. Datei-Einstieg mit externem Snapshot/Workspace;
6. unveränderte Root-AGENTS plus System-4-Override-Bindung.

Negativ/fail-closed ausgeführt:

1. Manifest-Bindung fehlt;
2. Manifest-Bindung stimmt nicht;
3. `AGENTS.override.md` manipuliert/dirty;
4. `controller.py` manipuliert/dirty;
5. Override fehlt;
6. Snapshot innerhalb des Repositories;
7. Workspace innerhalb des Repositories;
8. ungültiger stdin-JSON-Input ohne gültigen State.

Ergebnis Root-Testgruppe:

**14/14 PASS**.

## Gesamte Regression unter detached HEAD

Auf dem selben Kandidaten, während `git branch --show-current` leer war:

- Root-Gruppe: **14/14 PASS**;
- übrige Regression Gruppe A: **63/63 PASS**;
- übrige Regression Gruppe B: **24/24 PASS**.

Gesamt:

**101/101 PASS, 0 FAIL, 0 ERROR.**

## Kompletter Root-bis-Datei-Acceptance-Lauf

Der korrigierte `isolated_system4/full_local_acceptance.py` enthält keine Branch-Namensannahme mehr und bindet den Root-Manifestwert in den Snapshot.

Zusätzliche E2E-Negativfälle:

- `NEG_ROOT_MANIFEST_MISSING`
- `NEG_ROOT_MANIFEST_MISMATCH`

### Sichtbarer Branchname

Ergebnis: **10/10 PASS**.

### Detached HEAD

Ergebnis: **10/10 PASS**.

Beide Läufe durchliefen:

`Root -> Research -> Facts -> Context -> Draft -> echter LT-Fund -> REPAIR_REQUIRED -> Same-Article-Repair -> echter LT 6.8 PASS -> echter PPM 6.7.9 PASS -> Batch-Gate -> SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2 -> Inline-Pack -> Inline-Unpack -> bytegenaue WordPress-Datei`

Beide erzeugten dieselbe Enddatei:

- 1 Artikel
- Revision 2
- 66753 Bytes
- SHA256 `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`

`mocks_used=false`

`codex_used=false`

`merge_or_publish=false`

Gebundener LanguageTool-6.8-JAR-SHA256:

`2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`

Gebundener PPM-6.7.9-SHA256:

`acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

## GitHub-Bytebindung

Geprüfte Remote-Blobs des Code-Heads `18f16610e72e9d32f46827cd0c801786f79a0320`:

- `isolated_system4/root_entry.py` -> `7624a851432f7e0a8575a8421e33cfabfe29794d`
- `isolated_system4/test_root_entry.py` -> `593a39d78b396515e72015d85ac7488637073d5b`
- `isolated_system4/full_local_acceptance.py` -> `0fe61d04c8656c87727862d5b587530696d1bf50`

Diese Blobs sind bytegleich mit dem lokal ausgeführten Prüfstand.

## Immutable Base

GitHub-Workflow `Pferde Atelier Immutable Base Hardlock`, Run `34752658005`, Code-Head `18f16610e72e9d32f46827cd0c801786f79a0320`: **SUCCESS**.

Root-`AGENTS.md` wurde nicht verändert.

## Beweisgrenze

Bewiesen ist lokal ausdrücklich der zuvor fehlende Checkout-Zustand: **anderer symbolischer Branchname und detached HEAD** funktionieren mit denselben kritischen Bytes; manipulierte/fehlende Bindung blockiert fail-closed. Zusätzlich ist die komplette technische Kette bis zur bytegenauen Datei unter detached HEAD durchlaufen worden.

**Nicht bewiesen** ist damit ein neuer realer Codex-Artikel-PASS. Nach dieser Korrektur wurde kein weiterer Codex-Lauf gestartet.

Kein Merge. Kein Publish.