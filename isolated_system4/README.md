# SYSTEM 4 — TRUE SINGLE ROOM

Status: **TECHNISCHE TESTSTUFE 2 PASS — PRODUKTION WEITER BLOCKED BIS AUSDRÜCKLICHER CODEX-FREIGABE.**

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand bleibt getrennt und ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Aktueller Remote-Stand

PR #238: `System 4 — true single-room article production`

Branch: `hobbyroom/system4-true-single-room-v1`

Kein Merge. Kein Publish. `publish_allowed=false`.

Die lokal vollständig geprüften Teststufe-2-Kritikalbytes sind bytegleich auf dem Remote-Branch gebunden.

Gebundene Kernblobs:

- `isolated_system4/authoring_contract.py` -> `bab5c3bbb6e1440b3d2e8a52e0ee4fe6f5fd7ae4`
- `isolated_system4/controller.py` -> `fe904b29f9d047fb1839c4169a3359d6e4bfc3f6`
- `isolated_system4/batch_gate.py` -> `0b883efe9d3d5396975f7799984473c5ddb62773`
- `isolated_system4/LIVE_BOUND_INPUT_ONE_ARTICLE.json` -> `21dc52de06b296c3e12f893bb7ae38fd8a3fd1ba`

Gebundener Root-Manifestwert im Live-Input:

`38952850721801df0b932fdf7b82deb504c7272445e341b0e61b99ebbcec1f02`

Der Live-Input bleibt exakt ein Artikel:

- Typ `Beratung`
- Kategorie `putzbox-beratung`
- Titel `Putzbox für Pferde richtig auswählen`
- Keyword `Putzbox für Pferde`
- Plan-Slot `88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5`
- `publish_allowed=false`

## Ursache und Fix

Wiederholt aufgetretene Fehlerklasse:

**Eine Übergabe wurde als gültig akzeptiert, obwohl ihr Wert nicht gegen dieselbe autoritative Quelle validiert war, die der spätere echte Prüfer verwendet.**

Der reale Ein-Artikel-Lauf blockierte zuletzt mit:

`PPM679_VALIDATOR_BLOCKED:BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN`

Die Ursache wird jetzt am `Context`-Übergang geschlossen: `validation_contract_version` und die dazugehörigen V5-Section-Requirements werden vor Draft direkt gegen die unveränderte PPM-6.7.9-Autorität geprüft. Ein unbekannter Vertrag erreicht Authoring/Draft/LT/PPM nicht mehr.

Zusätzlich prüft das Batch-Gate die gebundene Input-Reihenfolge. Vertauschte Artikelzustände blockieren jetzt fail-closed mit `STATE_ORDER_MISMATCH:<index>`.

Textmaschine, PPM 6.7.9, PSERC/PSTE, LanguageTool 6.8, Design, WordPress-Plugin und Theme/CSS bleiben READ-ONLY.

## Teststufe 1 — exakter Produktions-Repro ohne Codex

Auf exakt den jetzt remote gebundenen Kritikalbytes erneut ausgeführt:

- gebundener Putzbox-Input -> Root -> Research -> Facts -> Context -> Draft -> echtes LanguageTool 6.8 -> echter PPM 6.7.9 -> Batch -> V2-Handoff -> Unpack/WordPress-Datei: **PASS**;
- Produktionskontext/Draft/Handoff-Bindungen byte-/feldgleich geprüft;
- Codex: **nicht verwendet**.

## Teststufe 2 — Generalisierung ohne Codex

Zweiter anderer kanonischer Beratung-Slot:

- Titel: `Welche Putzbürste passt für welchen Zweck?`
- Kategorie: `pferdebuersten-beratung`
- `canonical_article_id=article:b7c557395d3d298f0193c6c5`
- eigener kanonischer Source-Plan-Item: `beratung-putzbuersten-v4`

Erneut auf exakt denselben remote gebundenen Kritikalbytes ausgeführt:

- Artikel B allein kompletter Weg: **PASS**;
- Artikel A + Artikel B gemeinsam als 2er-Batch: **PASS**;
- echtes LanguageTool 6.8: **PASS**;
- echter PPM 6.7.9: **PASS**;
- Batch -> Handoff -> Unpack: **PASS**;
- 2er-Handoff SHA256: `3baab5c4abc7fe3834c760ac69b2ae82bfafab2ae352671599e6604c6b6282f5`.

Dabei wurde ein neuer realer Fehler entdeckt: Vertauschte Artikelzustände wurden zuvor akzeptiert. Nach Ursachenfix blockiert derselbe Negativfall mit `STATE_ORDER_MISMATCH:0`; der positive 2er-Batch bleibt PASS.

## Fehlerhistorie / Regression

Nach der Remote-Übertragung erneut gegen exakt dieselben Kritikalbytes ausgeführt:

- Workflow-/Context-/Draft-/Batch-/Handoff-Negativfälle: **18/18 PASS**;
- Root-/Manifest-/Publish-Negativfälle: **4/4 PASS**;
- zusammen aktueller bekannter Negativkatalog: **22/22 PASS**.

Unter anderem aktiv provoziert: unbekannte Fact-ID, fehlender Marker, Runtime-Titel/-Link/-Pflichtfeld-Mismatch, Snapshot-Mismatch, unbekannte Validation-Versionen, fehlende/fehlerhafte V5-Requirements, fehlende Fact-Refs/Source-Traces, Source-Trace-Mismatch, fehlender gebundener Link, fehlender Plan-Slot, Batch-State-Tamper, Handoff-Tamper, Manifest missing/mismatch und Publish-Authority-Verstoß.

PPM-6.7.9-SHA256:
`acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

LanguageTool-6.8-SHA256:
`2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`

## Remote-Hardlock

Nach dieser reinen Statusdokumentation muss der reguläre Workflow `Pferde Atelier Immutable Base Hardlock` auf dem finalen Head erneut **SUCCESS** sein. Kein Hardlock-PASS wird aus einem älteren Head übernommen.

## Codex-Regel

**Kein Codex ohne die ausdrückliche Nutzerfreigabe mit den Worten `Starte Codex`.**

`Weiter`, `testen`, `komplett prüfen`, `Null bis Ende` oder ähnliche Formulierungen sind **keine** Codex-Freigabe.

Codex wird ausschließlich für einen konkret gebundenen realen Artikel-/Batch-Produktionslauf verwendet, nicht für Diagnose, Architektur, Patch, Commit, Preflight, Regressionstests oder Dokumentation.

## HOBBYRAUM / NEXT ACTION

Status: **BLOCKED FÜR PRODUKTION / TECHNISCHE TESTSTUFE 2 PASS**.

Nächste Produktionsaktion ausschließlich nach ausdrücklicher Nutzerfreigabe `Starte Codex`:

- real gebundener Artikel-/Batch-Produktionslauf über den vollständigen System-4-Weg;
- kein automatischer zweiter Versuch bei echtem Hardblocker;
- kein Merge;
- kein Publish.

Bis zu dieser ausdrücklichen Freigabe: **kein Codex-Aufruf.**
