# PROTOKOLL / ÜBERGABE — SYSTEM 4 — FINAL CLOSEOUT 2026-09-13

Dieses Dokument ist das aktuelle Abschluss-/Übergabeprotokoll. Es ist **kein CURRENT_STATE**. Aktuelle System-4-Statuswahrheit bleibt ausschließlich `isolated_system4/README.md`; offizieller Campus-/Projekt-CURRENT bleibt ausschließlich `control/startmaster0107/CURRENT_STATE.json`.

## AKTUELLER REMOTE-STAND

PR #238 bleibt isolierter Draft-PR, unmerged und unpublished.

Branch: `hobbyroom/system4-true-single-room-v1`.

Kein Merge. Kein Publish. `publish_allowed=false`.

Die lokal bewiesenen Teststufe-2-Kritikalbytes wurden bytegleich auf den Remote-Branch übertragen und anschließend nochmals unabhängig per Remote-Git-Blob geprüft.

Gebundene Kernblobs:

- `authoring_contract.py` -> `bab5c3bbb6e1440b3d2e8a52e0ee4fe6f5fd7ae4`
- `controller.py` -> `fe904b29f9d047fb1839c4169a3359d6e4bfc3f6`
- `batch_gate.py` -> `0b883efe9d3d5396975f7799984473c5ddb62773`
- `LIVE_BOUND_INPUT_ONE_ARTICLE.json` -> `21dc52de06b296c3e12f893bb7ae38fd8a3fd1ba`

Root-Manifest des gebundenen Live-Inputs:

`38952850721801df0b932fdf7b82deb504c7272445e341b0e61b99ebbcec1f02`

## URSACHE / REPARATUR

Der reale Produktionslauf blockierte zuletzt nach mehreren Reparaturen mit:

`PPM679_VALIDATOR_BLOCKED:BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN`

Ursache: `validation_contract_version` war gebunden, wurde aber vor Draft nicht gegen dieselbe unveränderte PPM-6.7.9-Autorität geprüft, die später im Fullcheck entschied.

Reparatur: zentraler fail-closed Context-Guard. Unterstützte Validation-Version und zugehörige V5-Section-Requirements/Hashes werden vor Authoring/Draft gegen PPM 6.7.9 geprüft. Ein unbekannter Vertrag erreicht den teuren Draft/LT/PPM-Pfad nicht mehr.

Teststufe 2 fand zusätzlich einen neuen realen Batch-Fehler: vertauschte Artikelzustände wurden akzeptiert. Das Batch-Gate bindet jetzt jeden State zusätzlich an die gebundene Input-Position; Vertauschung blockiert mit `STATE_ORDER_MISMATCH:<index>`.

Keine Änderung an Textmaschine, PPM 6.7.9, PSERC/PSTE, LanguageTool-Regeln, Design, WordPress-Plugin oder Theme/CSS.

## TATSÄCHLICH AUSGEFÜHRTE TESTS — NACH REMOTE-ÜBERTRAGUNG

Die Tests wurden nach der Remote-Übertragung erneut auf einem lokalen Checkout ausgeführt, dessen drei geänderte Git-Blobs exakt den anschließend remote ausgelesenen Blob-SHAs entsprechen.

### Positiv

- Putzbox-Artikel kompletter Null->Datei-Pfad: PASS;
- zweiter anderer kanonischer Beratung-Slot `Welche Putzbürste passt für welchen Zweck?`: Einzelartikel PASS;
- Artikel A + B gemeinsam als 2er-Batch: PASS;
- echtes LanguageTool 6.8: PASS;
- echter PPM 6.7.9: PASS;
- Batch -> V2-Handoff -> Unpack: PASS;
- 2er-Handoff SHA256: `3baab5c4abc7fe3834c760ac69b2ae82bfafab2ae352671599e6604c6b6282f5`;
- Codex verwendet: NEIN.

### Negativ

- Workflow-/Context-/Draft-/Batch-/Handoff-Negativkatalog: 18/18 PASS;
- Root-/Manifest-/Publish-Negativkatalog: 4/4 PASS;
- Gesamt aktueller bekannter Negativkatalog: 22/22 PASS.

Aktiv provoziert wurden unter anderem: unbekannte Fact-ID, interner Marker fehlt, Runtime-Titel/-Link/-Pflichtfeld-Mismatch, Snapshot-Mismatch, unbekannte Validation-Versionen, fehlende/fehlerhafte V5-Requirements, fehlende Fact-Refs/Source-Traces, Source-Trace-Mismatch, fehlender gebundener Link, fehlender Plan-Slot, Batch-State-Tamper, Handoff-Tamper, vertauschte Batch-Reihenfolge, ungültiges Root-STDIN, Manifest missing/mismatch und Publish-Authority-Verstoß.

Echte Prüfer:

- LanguageTool 6.8 SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`
- PPM 6.7.9 SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

## REMOTE-HARDLOCK

Nach diesem Protokoll-Commit ist der reguläre Workflow `Pferde Atelier Immutable Base Hardlock` auf dem dann finalen Head frisch zu prüfen. Ein älterer Hardlock-Lauf gilt nicht als Abschlussbeweis.

## CODEX

In dieser Reparatur, Teststufe 1, Teststufe 2 und Remote-Übertragung wurde **kein Codex-Lauf gestartet**.

Verbindlich bleibt:

**Kein Codex ohne ausdrückliche Nutzerfreigabe mit den Worten `Starte Codex`.**

## STATUS / NEXT ACTION

Technische Teststufe 2: **PASS**.

System 4 bleibt **BLOCKED FÜR PRODUKTION**, bis ein realer Produktionslauf ausdrücklich mit `Starte Codex` freigegeben wird.

Nächste Produktionsaktion nur nach dieser ausdrücklichen Freigabe:

- real gebundener Artikel-/Batch-Produktionslauf;
- kompletter System-4-Weg;
- kein automatischer zweiter Versuch bei echtem Hardblocker;
- kein Merge;
- kein Publish.

## EINE WAHRHEIT

- offizieller Campus-/Projekt-CURRENT: `control/startmaster0107/CURRENT_STATE.json`
- System-4-CURRENT: `isolated_system4/README.md`
- System-4-Ziel: `isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`
- dieses Dokument: Abschluss-/Übergabeprotokoll, keine zweite CURRENT-Wahrheit
- PR-Text: nur Wegweiser

## PLUGINS

NICHT BETROFFEN.
