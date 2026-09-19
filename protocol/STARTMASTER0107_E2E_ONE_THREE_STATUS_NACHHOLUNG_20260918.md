# STARTMASTER0107 — E2E 1+3 Nachholprüfung / belastbarer Status — 18.09.2026

Status dieses Dokuments: **historisches WAS/WARUM-/Fehler-Evidence-Protokoll**. Es ist **keine** CURRENT_STATE und **keine** zweite NEXT-ACTION-Wahrheit. Aktueller operativer Stand ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Frisch geprüfte Autoritäten

- Main: `6a4ce1cecec25a2b228125695bc94d4398d638d3`
- Dispatcher PR #107 Head: `6a4ce1cecec25a2b228125695bc94d4398d638d3`
- Dispatcher Base: `e3ad9d23ca0c6a0bf2158b71b1dfa45e28c93fc0`
- PR #335: gemergt, Merge-Commit `6a4ce1cecec25a2b228125695bc94d4398d638d3`
- PR #335 Final-Head: `34983077bc30465469bcc2406dda4e4d40359893`
- Zielvertrag unverändert: `isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md`
- E2E-Vertrag unverändert: `protocol/STARTMASTER0107_E2E_ONE_THREE_CHAT_FILE_ACCEPTANCE_20260918.md`

## WAS wurde gemacht / real beobachtet?

### Test-only 1-/3-Adapter

PR #335 wurde gemergt. Der Adapter erlaubt nur 1 oder 3 Artikel, verändert den produktiven 7er-Batch nicht und blockiert den isolierten 107008-Übergang absichtlich mit:

`ACCEPTANCE_107008_CANONICAL_BOUNDARY:ISOLATED_TEST_ROUTE_MUST_NOT_REPLACE_OFFICIAL_PRODUCTION_INTAKE`

Auf PR-335-Final-Head waren die Required Checks grün:
- hardlock: Run `35394631714` PASS
- hardlock-base: Run `35394628714` PASS

### Reale Codex-E2E-Abnahme

PR107-Kommentar `5736300968` meldet:
- 1 Artikel: reale Codex-Qualität PASS, LT 6.8 PASS, PPM 6.7.9 PASS, `CONTENT_QUALITY_CHECK_OK`, Batch PASS;
- 3 Artikel: alle drei Einzelartikel PASS, aber Batch Collect fail-closed:
  `BATCH_TEMPLATE_REUSE_BLOCKED:1:2:0.2003`;
- Qualitäts-Negativtest: **nicht ausgeführt** vor dem 3er-Hardblock;
- Technik-Negativmatrix: 23/23 PASS gemeldet;
- 107008-Grenze: BLOCKED_AS_DESIGNED;
- Produktions-7er nicht gestartet; kein Publish.

### Durable Evidence fehlt remote

Codex meldete Evidence-Commit:
`ab748765d60ffa13528c420e20168aa08fec6ddc`
und Branch:
`test-evidence/system4a-e2e-1-3-20260918`.

Frische GitHub-Prüfung: Commit **nicht abrufbar**, Branch **nicht vorhanden**, `test_evidence/system4a_e2e_20260918/` **nicht auf Main vorhanden**. Daher ist die behauptete dauerhafte Evidence nicht rekonstruierbar und darf nicht als vollständiger Beweis behandelt werden.

### Follow-up blockiert

Der angeforderte dauerhafte 1-Artikel- plus Qualitäts-Negativ-Rerun wurde in PR107-Kommentar `5736330732` durch das Codex-Nutzungslimit blockiert.

## Neuer technischer Pflichtblocker

Auf dem aktuellen Dispatcher-Head `6a4ce1cecec25a2b228125695bc94d4398d638d3` ist PR107 hardlock-base Run `35394728634` **FAIL**.

Exakter erster Fehler:
`IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`

Fehlerstep:
`Block immutable security paths and Paul PROJECT_MEMORY writes`

Der Lauf gehört zu PR #107 / Branch `codex-chat-launcher` und vergleicht gegen den historischen Dispatcher-Base `e3ad9d23...`. Der technische Hardlock ist rot und schlägt jede Chat-PASS-Behauptung. Kein Bypass und keine Lockerung zulässig.

## WARUM Status nachgezogen wurde

Die bisherige CURRENT_STATE stand noch auf „E2E 1+3 pending“. Das war nach den oben belegten Ergebnissen nicht mehr belastbar:
- 1er-Lauf wurde ausgeführt;
- 3er-Lauf erreichte einen echten Batch-Hardblock;
- Qualitäts-Negativtest fehlt;
- Remote-Evidence fehlt;
- Codex ist aktuell limit-blockiert;
- PR107 Required Check ist rot.

Darum wurde nur der Status-/Blockerstand nachgezogen. Kein Text-, PPM-, LT-, Design-, Produktions- oder Publish-Vertrag wurde geändert.

## Ziel

Der Zielvertrag bleibt **unverändert**:

`Chat → Point-0 → realer Codex → LT 6.8 → PPM 6.7.9 → Same-Article-Repair → 1..N Batch → V2-Handoff → 107008 → PSERC → GitHub-ENDSTEMPEL → reale WordPress-Importformatprüfung → byte-identische Finaldatei im Parent-Chat`.

Kein Gesamt-PASS vor exakt dieser finalen Datei.

## Exakte nächste Reihenfolge

1. PR107 hardlock-base auf aktuellem Head ohne Sicherheitslockerung wieder grün bekommen.
2. Erst danach und erst bei verfügbarer Codex-Kapazität fehlende dauerhafte Evidence neu erzeugen.
3. Qualitäts-Negativtest real über PPM 6.7.9 ausführen.
4. 3er-Lauf erneut mit remote dauerhaftem Evidence-Satz ausführen; bei erneutem `BATCH_TEMPLATE_REUSE_BLOCKED` Ursache an den realen Artikelbytes analysieren, Schwelle nicht ändern.
5. Isolierte Acceptance weiterhin an 107008 fail-closed stoppen.
6. Für den vom Nutzer verlangten vollständigen Chat-Datei-Test ist danach ein **legaler kanonischer** 107008/PSERC/ENDSTEMPEL-Eingang erforderlich; kein Testadapter-Bypass.

## Nicht geändert

- Zielvertrag
- PPM 6.7.9
- LanguageTool 6.8
- Text-/Design-/Qualitätsgrenzen
- Produktions-7er
- Publish-/WordPress-Schreibstatus
- Paul-Zuständigkeiten
- technische Produktionsarchitektur


## Nachtrag 19.09.2026 — codexfreie Teststrecke abgeschlossen

Dieser Nachtrag ersetzt die oben beschriebenen offenen Teststrecken-Punkte, nicht die getrennten Produktions-/Codex-Blocker.

Aktueller Main nach PR #339:
`a0cb23a1611202fd75395a785385962ce7ae1900`

Beweise:
- PR #339 gemergt: reparierbarer `BATCH_TEMPLATE_REUSE_BLOCKED` führt in der isolierten Acceptance an denselben `DRAFT_WORKER`/Workspace zurück; Schwelle unverändert.
- Post-Merge System-4A-Acceptance Run `35398621624`: **SUCCESS**.
- Echter PPM-6.7.9-Negativbefund im Test: `BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO`, Ist `0.042553...`, erlaubt maximal `0.02`, Repair-Owner `DRAFT_WORKER`.
- Derselbe Testartikel lief über **2 Werkstatt-Rückgaben**, Same-Article-Kontinuität blieb erhalten.
- Danach reales LanguageTool 6.8 **PASS** und realer PPM 6.7.9 **PASS**.
- End-Schlussanteil `0.113268...` und damit über der gebundenen Beratung-Mindestgrenze `0.10`.
- Der 3-Artikel-deterministische Testlauf endete mit LT `PASS/PASS/PASS`, PPM `PASS/PASS/PASS`, Revisionen `[1,2,1]`.
- Kein Codex wurde in diesem Acceptance-Run verwendet.
- Keine Produktions-, Qualitäts-, PPM/LT-, Design-, Workflow- oder Publish-Regel wurde gelockert.

Damit ist die **codexfreie System-4A-Teststrecke PASS**. Nicht damit bewiesen ist `REAL_CODEX_REPAIR_PROVEN`; die dauerhaft unvollständige reale Codex-Evidence bleibt ein separater Punkt.

Operative Wahrheit bleibt ausschließlich:
`control/startmaster0107/CURRENT_STATE.json`
