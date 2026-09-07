# TEXT – CURRENT STATE

STAND: 2026-09-07
STATUS: GOLDMASTER CLOUD-ENTRY RESTORE BEREIT / ADMIN-SELBSTSCHUTZ BLOCKIERT MERGE

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des Büros TEXT.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Fehlerquelle
- Ziel → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- Warum/Änderungen → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Historie → `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

## Aktueller GitHub-Stand

`main`:
`457f33a09751db3acf78246ee394a59141d94d15`

PR #141:
**MERGED** – B01-only-KISS-Fix ist Bestandteil von current main.

PR #107:
OPEN – permanenter Chat→Codex-Dispatcher.
Head:
`f14ccf187b94c4beab9a86d0c69144f792ba2f64`

PR #143:
OPEN / DRAFT – vollständig separierter Plan-B-Shadow.
Head:
`5f7c52a23cb2810724500f00732801be13c43143`
Nicht produktiv verdrahtet, nicht gemergt.

Security-PR #137:
**MERGED** auf main.
Merge-Commit:
`457f33a09751db3acf78246ee394a59141d94d15`
Der `HOBBYROOM_WORK_LOCK_V1` ist damit im serverseitigen Hardlock-Code vorhanden.
Positiv-/Negativ-Selbsttest des Lock-Codes: **PASS 9/9**.
Offen bleibt ausschließlich die Rücksetzung des Repository-Rulesets: `hardlock-base` muss wieder als Required Status Check neben `hardlock` eingetragen werden.

## Aktueller realer Livebefund Plan A

Der erste Codex-Lauf auf current main erreichte:
- Cloud Entry PASS;
- Production Preflight PASS;
- Runtime Entry PASS;
- Current Action READY;
- Single Door READY.

Erster echter technischer STOP:
`BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING`

Folge:
- state_advanced=false;
- 107007 nicht abgeschlossen;
- 107008 nicht erreicht;
- kein Publish;
- keine WordPress-Schreibaktion.

B01 ist in diesem Lauf nicht erneut live bewiesen worden, weil der Lauf vorher bei LanguageTool stoppte.

## Aktuelle Arbeitsgrenze

Der TEXT-Hobbyraum steht auf:
`FIX_FORBIDDEN`

Verbindliche HARD RULE:
1. Hobbyraum technisch dichtmachen.
2. `de21f6cd35c60849c551fd82f78e75ce57c99fab` Goldmaster kopieren.
3. Pflichtänderungen einzeln nachrüsten.
4. Nach jeder Änderung real testen.

Aktuell ist ausschließlich Schritt 1 zulässig; Schritt 2–4 sind bis zur Admin-Aktivierung gesperrt.

Kein neuer technischer Integrationskandidat ist freigegeben.

Der begonnene Branch
`hobbyroom/languagetool-runtime-rebind-20260907`
ist ausschließlich PARKPLATZ / NICHT INTEGRIEREN.

Harte unveränderte Grenzen:
- eine Tür;
- dumme/fachblinde Wächter;
- Chat ohne freie Workflow-/Prüf-/Repair-/Publishentscheidung;
- Qualität, Inhalt, Design und Sicherheitsniveau unverändert;
- keine neue Facharchitektur;
- kein Auto-Publish.

Für alles Weitere gilt ausschließlich der maschinenlesbare Arbeitsstand in `HOBBYRAUM.md`.


## Goldmaster-Rekonstruktion

HARD RULE:
1. Hobbyraum technisch dichtmachen – **PASS**.
2. `de21f6cd35c60849c551fd82f78e75ce57c99fab` Goldmaster – **KANDIDAT BEREIT**.
3. Pflichtänderungen einzeln nachrüsten – **NOCH NICHT**.
4. Nach jedem Einbau Realtest – **VERBINDLICH**.

Aktueller Baseline-Kandidat:
`hobbyroom/goldmaster-main-reconstruction-20260907`
Head:
`482fa8ab71f4f180900707ca2309a5bd87727416`

Befund:
- exakt 14 technische TEXT-Korridor-Dateien geändert;
- alle 14 bytegleich zum bewiesenen `de21f6…`-Stand;
- aktuelle Security-/Campus-Schutzschicht bleibt erhalten;
- kein Publish.


## hardlock-base-Trigger-Befund

Manueller Reopen von PR #148 wurde von GitHub verarbeitet: normaler `hardlock` neu gestartet und PASS.
`Pferde Atelier Immutable Base Hardlock` / `pull_request_target` startete nicht.
Ruleset fordert `hardlock-base` weiterhin; Merge von #148 wird deshalb korrekt blockiert.
Goldmaster-Kandidat bleibt unverändert `482fa8ab71f4f180900707ca2309a5bd87727416`.


## PR #151 – Goldmaster Cloud Entry

Der erste Realtest auf Goldmaster-Baseline wurde ausschließlich durch die nach `de21f6…` eingeführte #137-Origin-Pflicht blockiert.

Daraufhin wurde kein Einzelpatch weitergeführt, sondern der gesamte motornahe Cloud-Entry-Block auf den bewiesenen Stand zurückgesetzt:
- `.github/workflows/pferde-atelier-deterministic-entrance-gate.yml`
- `control/cloud-entry-gate/cloud_entry.py`
- `control/cloud-entry-gate/cloud_repo_ci_test.py`

Alle drei Dateien sind bytegleich zu `de21f6…`.
PR #151 normaler hardlock: PASS.
Einziger Restblocker: absichtliche Immutable-Security-Selbstschutzregel.
