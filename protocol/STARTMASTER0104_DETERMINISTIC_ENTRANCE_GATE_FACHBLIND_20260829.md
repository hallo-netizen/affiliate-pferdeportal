# STARTMASTER0104 – Deterministic Entrance Gate V1

Stand: 29.08.2026

## Zweck
STARTMASTER0104 setzt eine ausschließlich technische, fachblinde Eingangstür vor den bestehenden Pferde-Atelier-Workflow. Ziel ist Zeitgewinn durch erzwungene Navigation: kein Rücksprung, Seitensprung, Überspringen oder Wiederholen bereits gebundener Schritte durch das Modell.

## Harte Trennung
Die Eingangstür kennt und bewertet keine Beitragsart, Titel-, Keyword-, Recherche-, Inhalts-, Qualitäts-, Design-, PSTE-, PSERC-, PPM-, LanguageTool-, Dubletten-/Kannibalisierungs- oder Publish-Regel. Diese Regeln bleiben ausschließlich hinter der Tür im bestehenden Workflow.

Die Tür kennt nur: ROOT/CURRENT_STATE, Step-ID, monotonen Sequence-Wert, Bundle-/Input-Hashes, ein Receipt-Schema und einen bereits vorgebundenen Folgeschritt.

## Ausführungsmodell
- GitHub/MASTER bleibt Navigationsautorität.
- `door.py` validiert den exakt aktuellen Schritt und erzeugt eine isolierte Execution Capsule.
- Der Worker erhält nur Capsule-Eingaben; keine MASTER-Historie und keine Navigationsautorität.
- Worker-Navigation, State-Write oder Workflowänderung werden verworfen.
- State-Fortschreibung ist nur nach PASS-Receipt und nur zu einem bereits vorgebundenen monoton höheren Schritt zulässig.
- Freier Chat ist keine gültige Produktions-Ausführungsautorität.

## Keine OpenAI-API
Der kostenpflichtige API-Pfad aus STARTMASTER0103 ist verworfen und der alte API-Workflow wurde entfernt. Vorgesehener Hard-Worker ist Codex CLI mit ChatGPT-Anmeldung; der MASTER benötigt keinen OpenAI-API-Key.

## Zukunftsflexibilität
Neue Beitragsarten sowie spätere Titel-, Keyword-, Such- oder Inhaltsänderungen werden als normale Workflow-/Maintenance-Schritte hinter der Tür gebunden. Dafür ist keine Änderung an der Eingangstür erforderlich. Lokale synthetische Kompatibilitätstests für neue Beitragsart, Titelregel und Keyword-/Suchlogik sind PASS.

## Schutz des bestehenden Ergebnisses
0103→0104 Protected-Byte-Audit: Alle geerbten Fach-/Inhalts-/Qualitäts-/Design-Dateien byte-identisch. Verändert wurden im geerbten Bestand ausschließlich ROOT und CURRENT_STATE für die technische Navigation. PSTE 0.56.25 und PSERC 0.28.14 bleiben exakt unverändert.

## Prüfstand
30/30 lokale Positiv-/Negativtests der Eingangstür PASS, inklusive Side-jump/Backtrack/Repeat, falschem Ticket/Step/State/Bundle, Worker-State-Write, Worker-Workflowänderung, Input-Tamper, Path-Escape, unbekanntem Step sowie bestehenden Package-Guard-Regressionen.

GitHub Actions `Pferde Atelier Deterministic Entrance Gate`, Run `33218700870`, Commit `2dbb8543454f631d509bbd9f0d4ebf9de695eeed`: PASS. Sowohl `Deterministic entrance gate positive-negative CI` als auch `Assert active gate has no OpenAI API dependency` sind erfolgreich.

## Fail-closed Aktivierung
Der reale Codex-Hard-Worker kann erst auf dem Benutzerrechner mit dessen ChatGPT-Anmeldung bewiesen werden. Deshalb bleibt `hard_worker_runtime_verified=false` und `NEXT_ALLOWED_STEP=ACTIVATE_LOCAL_CODEX_CAPSULE_WORKER_SELFTEST_NO_API`. Vor dessen PASS darf kein weiterer Produktionsblock über die neue Hard-Worker-Schicht freigegeben werden.

Nach PASS ist bereits ausschließlich `ROOTFIX_LIVE_40_40_MAX_FAMILIES_REACHED` vorgebunden.
