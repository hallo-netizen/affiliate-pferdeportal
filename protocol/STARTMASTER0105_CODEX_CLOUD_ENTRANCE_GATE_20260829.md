# STARTMASTER0105 – Codex Cloud Deterministic Entrance Gate

Stand: 29.08.2026

## Zweck
STARTMASTER0105 ersetzt ausschließlich die falsche lokale Codex-CLI-Annahme aus STARTMASTER0104 durch einen Cloud-tauglichen, rein technischen Eingangspfad. Keine OpenAI-API, keine lokale Installation.

## Harte Grenze
Die Eingangstür ist fachblind. Sie kennt und bewertet keine Beitragsarten, Titel-, Keyword-, Recherche-, Inhalts-, Qualitäts-, Design-, PSTE-, PSERC-, PPM-, LanguageTool-, Dubletten-/Kannibalisierungs- oder Publish-Regel. Diese Logik bleibt vollständig hinter der Tür im bestehenden Workflow.

## Cloud-Ausführung
- Repositoryweite `AGENTS.md` zwingt Codex Cloud vor jeder Projektarbeit zum technischen Entry-Command.
- `control/cloud-entry-gate/cloud_entry.py` liest ausschließlich den aktuellen STARTMASTER-Pointer, ROOT, CURRENT_STATE und das exakt gebundene Step-Bundle.
- Es erzeugt `.pferde-capsule` nur mit dem aktuellen Step und dessen hashgebundenen Eingaben.
- Worker-Navigation, freie State-Änderung, freie Workflowänderung, API-Abhängigkeit und lokaler Codex-Zwang sind nicht vorgesehen.
- Bereits bestandene Workflowstufen werden nicht zur Navigation erneut eingelesen.

## Zukunftsflexibilität
Neue Beitragsarten sowie spätere Änderungen an Titel-, Keyword-, Such-, Inhalts- oder Qualitätslogik liegen hinter der Eingangstür. Die Eingangstür muss dafür nicht fachlich geändert werden; sie verarbeitet nur neue Step-IDs/Bindings/Hashes.

## Schutz bestehender Fachlogik
STARTMASTER0105 verändert keine bestehenden Portal-/Text-/Qualitäts-/Designkomponenten. Die aktiven PSTE-/PSERC-Stände und die vorhandenen PPM-/LanguageTool-/Dubletten-/Kannibalisierungs-/Publishregeln bleiben unverändert. Die Cloud-Schicht enthält keine dieser Fachlogiken.

## Prüfstand
GitHub Actions `Pferde Atelier Deterministic Entrance Gate`, Run `33238322059`, Commit `f8e9511c8e3b5972b7dc0a038e06af8b71ae980e`: PASS.

PASS-Schritte:
- Legacy deterministic gate regression
- Codex Cloud entrance positive-negative CI
- Assert active gate has no OpenAI API dependency
- Assert active gate stays domain blind

Negative Cloud-Gate-Prüfungen blockieren u. a. freie Chat-Ausführungsautorität, API-Abhängigkeit, falschen Worker-Typ, Side-Jump, Bundle-Tamper und Path-Escape.

## Aktueller Zustand
`NEXT_ALLOWED_STEP = VERIFY_CODEX_CLOUD_ENTRANCE_GATE_SELFTEST_NO_API`

Der einmalige reale Cloud-Selbsttest muss als Codex-Cloud-Aufgabe im verbundenen Repository laufen. Danach ist ausschließlich `ROOTFIX_LIVE_40_40_MAX_FAMILIES_REACHED` vorgebunden.

## Bedienung
Für Codex Cloud wird nur der verbindliche Text aus `control/cloud-entry-gate/CODEX_CLOUD_STARTPROMPT.txt` verwendet. Keine lokale CLI, kein Terminal auf dem Benutzer-Mac, kein API-Key.
