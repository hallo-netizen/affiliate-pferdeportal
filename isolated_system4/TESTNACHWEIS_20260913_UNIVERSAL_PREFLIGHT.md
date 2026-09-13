# SYSTEM 4 — TESTNACHWEIS UNIVERSAL PREFLIGHT — 2026-09-13

Status dieses Dokuments: **Belegdatei, keine zweite CURRENT_STATE**. Die aktuelle System-4-Statuswahrheit bleibt ausschließlich `isolated_system4/README.md`.

## Gebundener Prüfstand

PR #238, Branch `hobbyroom/system4-true-single-room-v1`.

Der ausführbare System-4-Kern und die aktuellen `test_*.py`-Dateien wurden vor dem finalen Preflight gegen ihre GitHub-Blob-SHAs abgeglichen. Seit dem vollständig geprüften Code-Head wurden bis zur Auflösung des PPM-Blockers ausschließlich Status-/Belegdokumente verändert; kein System-4-Ausführungscode und kein Test wurde dafür umgeschrieben.

## Universalitätsnachweis

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

## Historischer letzter Blocker und dessen reale Auflösung

Der erste vollständige Gesamtlauf hatte **87 Tests, 86 PASS, 1 FAIL**. Der einzige FAIL war:

`test_authoritative_textmachine_bindings_are_unchanged_from_proven_full_rule_pass`

Ursache war ausschließlich, dass die gebundene Binärdatei
`control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`
im lokalen Testcontainer physisch fehlte.

Die Repo-Historie wurde anschließend geprüft:
- Commit `63162490c344f056d033ec5e82cf94fdbddf204d` legte die **exakten PPM-6.7.9-Runtime-Chunks** `ppm.00` bis `ppm.06` an;
- Commit `17f4c92fc00a7bb59c6169bb1a9fefbd9b7aa659` materialisierte daraus die gebundene ZIP und entfernte die Chunks;
- Ziel-Git-Blob der fertigen ZIP: `151e9d6f908453dfc5b4acb497c4927a3f03c940`.

In der vorhandenen Dateibibliothek wurden die historischen Original-Zwischendateien `ppm.00.b64` bis `ppm.06.b64` gefunden und lokal materialisiert. Es wurde **kein PPM-Inhalt erfunden, repariert oder verändert**.

Nach Base64-Decodierung wurden alle sieben Chunks mit `git hash-object` gegen ihre historischen Repo-Blob-SHAs geprüft:
- `ppm.00` -> `e8d476663493d7b8e008889641fcfe377c204b57` PASS;
- `ppm.01` -> `298b49b36cb4602bf6162a198dcf6cde70fcd738` PASS;
- `ppm.02` -> `b7050533358d07bc4b06582735fff220146cba54` PASS;
- `ppm.03` -> `0acb16054565941d5c1ab935673ecd2aed1db25e` PASS;
- `ppm.04` -> `fce1a3984fdad769c1bbc9d47bde9cf259940cb9` PASS;
- `ppm.05` -> `7059c230dd6b2e65c4beb562eaa7cd7d892b0c1b` PASS;
- `ppm.06` -> `cfdc5cf0a6fe9512932b6c1db128165b47e4e66e` PASS.

Die unverändert zusammengesetzte PPM-ZIP ergibt:
- Größe: `1614485` Bytes;
- Git-Blob: `151e9d6f908453dfc5b4acb497c4927a3f03c940` PASS;
- SHA256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1` PASS;
- `unzip -t`: PASS, keine Fehler im komprimierten Inhalt.

Damit ist nachgewiesen, dass lokal exakt die bereits gebundene PPM-6.7.9-Datei geprüft wurde.

## Finaler vollständiger Testlauf

Nach Einbringen ausschließlich dieser unveränderten, hashgleichen PPM-Datei in den lokalen Prüfpfad ausgeführt:

`PYTHONPATH=isolated_system4 python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v`

Ergebnis:
- **87 Tests insgesamt**;
- **87 PASS**;
- **0 FAIL**;
- **0 ERROR**.

Der zuvor einzige PPM-Bindungstest ist dabei ausdrücklich PASS:
`test_authoritative_textmachine_bindings_are_unchanged_from_proven_full_rule_pass`.

## Finaler lokaler E2E

Separat ausgeführt:

`PYTHONPATH=isolated_system4 python3 -m unittest isolated_system4.test_local_end_to_end_chat_handoff -v`

Ergebnis:
- **5/5 PASS**.

### Wichtige Beweisgrenze dieses E2E-Tests

Dieser Test bildet **nur die interne `isolated_system4`-Kette** nach. Er startet **nicht** am echten repositoryweiten Codex-Cloud-Eingang.

Konkret:
- `codex_entry.py` wird im Test direkt aufgerufen;
- die Research-Evidence wird aus lokalen Testdaten mit `example.org` erzeugt und ist keine echte Webrecherche;
- im positiven Hauptpfad wird `production_checks.run_all` gemockt und mit einer synthetischen PASS-Evidence ersetzt;
- Root-`AGENTS.md`, `control/output-quarantine/runtime_entry_gate.py`, `worker_freshness_guard.py` und der reale Codex-Cloud-Start werden in diesem E2E-Test **nicht ausgeführt**.

Deshalb darf `5/5 PASS` nur so interpretiert werden:
**interner System-4-Pfad vom direkten System-4-Einstieg bis zur exakten V2-Elternchat-Rekonstruktion PASS**.

Es beweist ausdrücklich **nicht**:
- dass Codex Cloud den System-4-Einstieg überhaupt erreicht;
- dass die repositoryweite Root-Instruktion System 4 nicht vorher abfängt;
- dass echte Webrecherche im Codex-Lauf erfolgt;
- dass der reale Codex-Produktionslauf vom Repository-Eingang bis zur Chat-Datei funktioniert.

Der zusätzlich enthaltene Test `test_authoritative_textmachine_bindings_are_unchanged_from_proven_full_rule_pass` prüft zwar die reale PPM-Paketbindung und LT-/PPM-Identitäten, schließt diese Codex-Cloud-Eingangslücke aber nicht.

Enthalten sind damit korrekt beschrieben:
- reale PPM-/Textmaschinen-Bindungsidentität: PASS;
- interner positiver System-4-Weg ab direktem System-4-Einstieg bis zur exakten V2-Elternchat-Rekonstruktion: PASS;
- Fake-Fact-Negativtest: BLOCKED/PASS;
- Design-Drift-Negativtest: BLOCKED/PASS;
- historische artikelübergreifende Template-Wiederholung: BLOCKED/PASS.

## Finaler NO-LEGACY-Nachweis

Frisch ausgeführt über:
`production_checks.no_legacy_runtime_dependencies(...)`

Ergebnis:
- `status = PASS`;
- `legacy_import_count = 0`;
- Allowlist ausschließlich gebundene PPM-ZIP und LanguageTool 6.8 commandline.jar nach exaktem SHA256.

## Beweisgrenze / Schlussstatus

Lokal nachgewiesen:
- universeller nichtleerer Batch `1..N` ohne künstliche System-4-Obergrenze: PASS;
- keine System-4-Beitragsart-Whitelist: PASS;
- kompletter aktueller Unittestbestand: **87/87 PASS**;
- lokaler interner E2E ab direktem System-4-Einstieg: **5/5 PASS**;
- NO-LEGACY innerhalb des System-4-Laufzeitcodes: PASS;
- reale gebundene PPM-6.7.9-ZIP: Hash-/Blob-/ZIP-Integrität PASS.

Nicht durch diesen lokalen Preflight bewiesen wurde der **echte repositoryweite Codex-Cloud-Einstieg vor `isolated_system4`**.

Diese Lücke wurde im ersten realen 1-Artikel-Codex-Lauf am 2026-09-13 tatsächlich sichtbar: Codex wurde vor System-4-ingress durch die repositoryweite offizielle Runtime-Eingangsstrecke mit `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING` blockiert. Siehe `PROTOKOLL_REALRUN_20260913_SINGLE_ARTICLE_ENTRY_BLOCKER_SPEED.md` und die aktuelle Statuswahrheit `README.md`.

Kein Merge. Kein Publish. Textmaschine, PPM, PSERC/PSTE, WordPress-Plugin und Design wurden nicht verändert.
