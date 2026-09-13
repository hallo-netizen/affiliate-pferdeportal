# SYSTEM 4A — ISOLIERTER KAPSEL-/AUTORITÄTS-PROTOTYP

STATUS: **TEST ONLY / PRODUKTION BLOCKED / KEIN MERGE / KEIN PUBLISH**

Diese Datei ist die eine aktuelle 4A-Statuswahrheit.

## Zweck

4A ist keine neue Textmaschine. Einziger Unterschied zu System 4 ist die Autoritätsgrenze:

- äußerer Supervisor besitzt Workflow-State, Route, Kontrollbindung und PASS-Verwendung;
- Worker/Codex liefert ausschließlich Fachinhalt;
- System-4-Prüfer, Design-, Qualitäts- und WordPress-Regeln bleiben unverändert;
- FAIL bleibt derselbe Artikel;
- Ausgang bleibt `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` plus Parent-Chat-Readback.

Wenn diese Trennung nur mit neuer Signer-/Token-/Room-/Receipt-/Package-Kaskade möglich wäre, 4A stoppen.

## Aktuelle Vergleichsbasis

System 4 PR #238 Head: `89b2e8eeb928f744e8814b2c79966672db2e308a`.

Die fünf Änderungen seit `edfe6049768db68f85bf3babedce3199538217ef` betreffen nur zusätzliche System-4-Transportdateien. Der für den lokalen Realtest verwendete Fach-/Design-/LT-/PPM-Prüfercode blieb unverändert.

4A liegt direkt auf diesem Head. Der Vergleich System 4 -> 4A enthält ausschließlich `isolated_system4a/**`.

Nicht als 4A-Vorteil gewertet: Artikelzahl, Beitragsart, Fach-/Textregeln, Design, LT, PPM oder WordPress-Handoff.

## Lokaler Gesamtstand

### Architektur / Eingang / Ausgang / Skalierung

Frisch lokal mit Warnings als Fehler:

**41/41 PASS**.

Enthalten:

- kompletter Einstieg -> Parent-Chat-Ausgang;
- Same-Article-Repair;
- 1 / 3 / 25 / 1000 Artikel;
- neue/gemischte Beitragsarten;
- Managed-Session-Grenze;
- Cross-UID-Prozessgrenze;
- State-/PASS-/Manifest-/Publish-Injektionen BLOCK;
- Research/Facts/Context/Design/Checker/Repair/Batch BLOCK;
- JSON-/Inline-Tamper BLOCK;
- privates Codex-artiges `0700`-Worker-Quellverzeichnis;
- Supervisor-Staging dieses privaten Bundles;
- `state.json`, Authority-Dateien und Symlinks im Worker-Bundle BLOCK;
- Worker-Absturz liefert Exit-Code + `stderr` statt stummem `WORKER_EXITED_WITHOUT_RESPONSE`.

### Echter lokaler Produktionslauf

Echte, hashgebundene Abhängigkeiten:

- LanguageTool 6.8 JAR SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`;
- PPM 6.7.9 Paket SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`;
- mocks=false.

Kompletter 4A-Produktions-Acceptance-Lauf mit Supervisor-eigenem Staging eines privaten `0700`-Worker-Bundles:

**10/10 PASS**.

Positiv:

`Fachinput -> Supervisor-Ingress -> Cross-UID-Worker -> Research -> Facts -> Context -> Draft -> echter LT-Fail -> Same-Article-Repair -> echter LT-PASS -> echter PPM-PASS -> Batch -> V2 -> Parent-Chat byteidentisch`

Negativ korrekt geblockt:

1. Same-UID-Produktion;
2. externes Kontrollmanifest;
3. direkter ungestagter Cross-UID-Worker unter privatem Pfad;
4. Worker-PASS-/Phase-Injektion;
5. Fake-`state.json`;
6. ungültige Research-Evidence;
7. ungültige Facts-Evidence;
8. Design-Drift;
9. Parent-Chat-Payload-Tamper.

Finaler positive Test-Handoff:

- Größe: **66.753 Byte**;
- SHA256: `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`;
- Revision: **2**;
- `publish_allowed=false`.

Der positive System-4- und System-4A-Realtest erzeugen weiterhin byteidentischen Output.

## Erkenntnis aus dem freigegebenen Codex-Probelauf

Der einmal ausdrücklich freigegebene Codex-Probelauf mit dem Titel `Pferdeanhänger im Herbst sicher vorbereiten` erreichte:

`ROOT_ENTRY_PASS -> PRODUCTION_INGRESS_BOUND -> RESEARCH_REQUEST`

und stoppte bei:

`WORKER_EXITED_WITHOUT_RESPONSE`.

Lokale Reproduktion ergab die konkrete Ursache: Der Codex-artige Worker lag in einem `0700 root`-Tempverzeichnis und war für `nobody` nicht les-/traversierbar. Der damalige Host verwarf zusätzlich `stderr`.

Diese Lücke ist lokal geschlossen:

- Supervisor staged private Worker-Bundles selbst in einen kontrollierten read-only Bereich;
- Cross-UID-Zugänglichkeit wird vor Start geprüft;
- Worker-`stderr` und Exit-Code werden bei Absturz ausgegeben;
- der komplette echte LT/PPM-Produktionslauf bleibt danach 10/10 PASS.

Kein zweiter Codex-Lauf wurde gestartet.

## Codex-Regel

**Kein Codex-Lauf ohne ausdrückliche vorherige Freigabe des Users.**

Aktuell:

`REAL_CODEX_4A_RETEST = NOT AUTHORIZED`

## Beweisgrenze / NEXT ACTION

Lokal ist die vollständige Produktionskette inklusive realem LT/PPM und realitätsgleichem privaten Worker-Staging bewiesen.

Noch offen ist ausschließlich der operative Wiederholungsbeweis mit einem echten Codex-/Managed-Agent-Worker auf dieser korrigierten Grenze.

Bis zu einer ausdrücklichen User-Freigabe:

1. kein Codex-Lauf;
2. nur lokale Positiv-/Negativtests und Synchronisierung mit System 4;
3. keine Änderung an Fach-, Design-, LT-, PPM- oder WordPress-Regeln;
4. kein Merge, kein Publish.

## Abbruchregel

Wenn System 4 State/Route/PASS ebenfalls technisch aus der Worker-Autorität entfernt, verliert 4A seinen einzigen strukturellen Vorteil und wird als eigenes Konzept beendet.
