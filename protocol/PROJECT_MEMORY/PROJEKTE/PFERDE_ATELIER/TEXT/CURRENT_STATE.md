# TEXT – CURRENT STATE

STAND: 2026-09-07
STATUS: HOBBYRAUM-HARDLOCK AUF MAIN / RULESET-RESTORE VON hardlock-base AUSSTEHEND

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
