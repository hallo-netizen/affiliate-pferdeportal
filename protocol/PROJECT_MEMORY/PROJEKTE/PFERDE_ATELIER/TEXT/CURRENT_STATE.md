# TEXT – CURRENT STATE

STAND: 2026-09-07
STATUS: PLAN A AUF MAIN / ERSTER LIVEBLOCKER LANGUAGETOOL-BINDUNG / HOBBYRAUM-FIXSPERRE AKTIV

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des Büros TEXT.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Fehlerquelle
- Ziel → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
- Warum/Änderungen → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Historie → `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

## Aktueller GitHub-Stand

`main`:
`f14ccf187b94c4beab9a86d0c69144f792ba2f64`

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
OPEN / nicht gemergt.
Aktueller Security-Head:
`5e0547c999a544d57e1891776f2f417e836eb605`
Enthält zusätzlich die serverseitige Prüfung des `HOBBYROOM_WORK_LOCK_V1`.
Normaler hardlock auf diesem Head: PASS.
Aktivierung auf main weiterhin durch den bestehenden immutable Security-Selbstschutz blockiert und erfordert kontrollierte Admin-Wartung.

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
