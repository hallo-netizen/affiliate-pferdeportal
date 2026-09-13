# SYSTEM 4A — AKTUELLER LOKALER TESTNACHWEIS 2026-09-13

Belegdatei, keine zweite CURRENT_STATE.

## Vergleichsbasis

System 4 PR #238: Head `edfe6049768db68f85bf3babedce3199538217ef`.
4A basiert direkt auf diesem Stand; fachliche, Design-, Qualitäts- und WordPress-Regeln bleiben System 4 und werden nicht kopiert.

## Frischer lokaler 4A-Satz

Ausgeführt nach der Produktions-Autoritätshärtung:

- Python compile der geänderten 4A-Dateien: PASS.
- Unittest-Satz: **31/31 PASS**, 0 Fehler, 0 Failures, Laufzeit **16,792 s**.

Abgedeckt sind unter anderem:
- kompletter positiver Einstieg bis Parent-Chat-Ausgang mit Same-Article-Repair;
- Cross-UID-Supervisor/Worker-Grenze;
- 1 / 3 / 25 externe Vollketten;
- 1 / 3 / 25 / 1000 interne Architekturkette;
- getrennte Worker-Prozesse und isolierte Worker-Räume;
- gemischte/neue `article_type` ohne Controller-Whitelist;
- Worker-State-/PASS-/LT-/PPM-/Production-Evidence-Injektion BLOCK;
- Research/Facts/Context/Design/Checker-Hash/Repair/Batch BLOCK;
- Output- und Parent-Chat-Tamper BLOCK;
- direkter Produktions-Callable BLOCK vor Backend, Worker und Ingress;
- Same-User-Produktion BLOCK vor realem Prüfer-Backend;
- Produktions-Prüfer-Injektion BLOCK.

## Frischer 1000er externer Skalierungslauf

Ausgeführt auf derselben Autoritätsschicht:

- Artikel: **1000**;
- logisch getrennte Artikel-Sessions: **1000**;
- Worker-Runtime-Prozesse: **2**;
- kompletter Architekturweg bis `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` und Parent-Chat-Rekonstruktion: PASS;
- Parent-Chat-Datei byteidentisch: PASS;
- Ausgangsgröße: **3.550.796 Byte**;
- Laufzeit: **7,324 s**.

Dieser Lauf ist ARCHITEKTUR-E2E mit Test-Checkern und bleibt vom echten Produktionsnachweis getrennt.

## Echter lokaler Produktions-Acceptance-Lauf

Ausgeführt mit dem aktuellen 4A-Produktionsrunner und den unveränderten System-4-Prüfern.

Gebundene Abhängigkeiten:

- System-4-Basis: `edfe6049768db68f85bf3babedce3199538217ef`;
- System-4-Critical-Manifest: `3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`;
- LanguageTool 6.8 Commandline-JAR SHA256: `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`;
- PPM 6.7.9 Paket SHA256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`;
- echte System-4-Acceptance-Fixture: `isolated_system4/full_local_acceptance.py` Blob `0fe61d04c8656c87727862d5b587530696d1bf50`;
- 4A-Read-only-Adapter Blob `5b75ab2f95d761595b9e7d7c5b4e7bd073206bed`.

Ergebnis des vollständigen Laufs:

**9/9 PASS**.

Positiv:

- externer Fachinput ohne Kontrollmanifest;
- Supervisor bindet das System-4-Manifest selbst;
- Worker läuft als andere UID (`nobody`) außerhalb der Supervisor-Autorität;
- Research -> Facts -> Context -> Draft;
- echter LanguageTool-6.8-Fund im ersten Draft;
- Same-Article-Repair, finale Revision **2**;
- erneuter echter LanguageTool-6.8-PASS;
- echter PPM-6.7.9-PASS;
- Batch-PASS;
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` PASS;
- Parent-Chat-Rekonstruktion byteidentisch PASS;
- `publish_allowed=false`.

Finaler Test-Handoff:

- Größe: **66.753 Byte**;
- SHA256: `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`.

Negativ jeweils PASS durch korrektes Blockieren:

1. Same-UID-Produktion;
2. extern eingespeistes Kontrollmanifest;
3. Worker-PASS-/Phase-Injektion;
4. Worker erzeugt Fake-`state.json`;
5. ungültige Research-Evidence;
6. ungültige Facts-Evidence;
7. Design-Drift;
8. Parent-Chat-Payload-Tamper.

`mocks_used=false`, `real_languagetool=true`, `real_ppm679=true`, `supervisor_owns_manifest_binding=true`.

## Korrigierter Testfixture-Fehler

Der erste Lauf erreichte sämtliche realen Produktionsstufen und stoppte ausschließlich im letzten Parent-Chat-Negativtest. Ursache war ein Fehler im Test selbst: Der Test veränderte nur das letzte Newline hinter dem `INLINE_END`-Marker und damit keine geschützte Nutzlast.

Der Test wurde ausschließlich so korrigiert, dass ein Zeichen innerhalb von `payload_base64` verändert wird. Danach blockierte der vorhandene Handoff-Prüfer korrekt und der vollständige Lauf erreichte **9/9 PASS**.

Korrektur-Commit auf PR #255:

`1e4571d8196df066a7e35378e62edb79816c10d0`

Korrigierter Runner-Blob:

`7719c42b8779a4cdd26bf78ac5d28f9304cce9a6`

Keine Fach-, Text-, Design-, LT-, PPM-, WordPress- oder Produktionsregel wurde dafür verändert.

## Direkter Vergleich gegen System 4

Danach wurde auf derselben lokalen Basis der unveränderte aktuelle System-4-Runner `isolated_system4/full_local_acceptance.py` gegen exakt dieselben echten LT-/PPM-Abhängigkeiten ausgeführt.

Ergebnis System 4:

**10/10 PASS**, `mocks_used=false`, `codex_used=false`.

Positiver System-4-Ausgang:

- Größe: **66.753 Byte**;
- SHA256: `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`;
- Revision: **2**;
- Artikel: **1**.

Damit sind positiver System-4- und positiver System-4A-Ausgang **byteidentisch**. 4A verändert weder Text, Reparaturergebnis, LT-/PPM-Evidence noch V2-Ausgang. Der nach diesem Vergleich verbleibende 4A-Unterschied ist ausschließlich die Lage der Workflow-/State-Autorität.

## Beweisgrenze

Damit ist jetzt lokal real bewiesen:

- Supervisor-State und Workflow-Autorität liegen außerhalb des Cross-UID-Workers;
- der Worker kann Route/PASS/State nicht setzen;
- die unveränderten System-4-Prüfer laufen vollständig über 4A;
- echter LT-/PPM-Produktionsweg inklusive Same-Article-Repair funktioniert;
- V2-/Parent-Chat-Ausgang bleibt intakt;
- System 4 und 4A erzeugen im identischen positiven Realtest byteidentischen Output.

Noch **nicht** bewiesen ist die operative Produktgrenze mit einem tatsächlich extern betriebenen Codex-/Managed-Agent-Worker. Der vorhandene Managed-Agent-Weg bleibt deshalb separat offen. Ebenfalls wurde kein echter WordPress-Import ausgeführt; WordPress ist kein eigener 4A-Vorteil und sein vorhandener Importvertrag bleibt unverändert.

Kein Merge, kein Publish, kein Codex-Lauf aus diesem Nachweis.
