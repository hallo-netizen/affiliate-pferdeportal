# STARTMASTER0107 – Reparaturrückgabe / Validator-Livekette – Protokoll 2026-09-11

**STATUS DIESER DATEI:** HISTORISCHES PROTOKOLL / WAS-WARUM-NACHWEIS. **KEINE CURRENT-AUTORITÄT.** Aktueller Status ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Tatsächlich ausgeführte Änderungen

- PR #223 (`5f996d5574b5b4bb33bac917c375d9539d7bf8a8`): einfachen gebundenen 107007-Einstieg wiederhergestellt; der unabhängige Aggregate-/Fachprüfer blieb erhalten; Worker/Codex besitzt keine PASS-Autorität; `stage_proofs=[]`; kein neuer Runner/Gate/Controller/Contract; kein Publish.
- PR #224 (`c4938879bdb467b068bce86c98d605782369b992`): im bestehenden `fachworkflow_proof_handoff.py` maschinenfeste `FACHWORKFLOW_REPAIR_REQUIRED`-Rückgabe eingeführt. Reparierbare LanguageTool-/PPM-Inhaltsbefunde geben denselben gebundenen `current_item` zur Korrektur zurück. Kein PASS, keine Submission und kein Raumwechsel durch die Rückgabe. Technische/Binding/Hash/Identity/Publish-Fehler bleiben terminal.
- PR #226 (`2c6ec14711b9451c551f7855c224ea1bd58cef42`): bestehende PPM-Reparaturbefunde aus `reason_codes`/`errors` werden nur unter den bereits festgelegten reparierbaren Präfixen an denselben Rückkanal weitergereicht. Keine PPM-Regeländerung.
- PR #228 (`2d7c43b726926be83b1fd5159d8592d4c40bd994`): LanguageTool erhält temporär nur sichtbaren Klartext aus dem unveränderten gebundenen HTML. Das HTML selbst bleibt unverändert und geht weiter an PPM.
- PR #230 (`66c4224d68532307f6c7f69aff81d1da04cae4e7`): `fact_pack.fact_pack_id` wird zusätzlich exakt an dieselbe bereits gebundene `source_snapshot_id` gekoppelt. Keine neue Quelle und kein neuer Pfad.

## WAS / WARUM

Der alte funktionierende Arbeitsrhythmus erlaubte dem gebundenen Worker, am selben Artikel weiterzuarbeiten, bevor die endgültige Freigabe erfolgte. Der neue Aggregate-Prüfer sollte die unabhängige PASS-Autorität übernehmen, machte reparierbare reale Validatorbefunde zunächst jedoch terminal.

Die KISS-Korrektur war deshalb **kein zweiter Prüfer und kein Prompt**, sondern nur: derselbe bestehende Prüfer kann reparierbare Fachbefunde als `FACHWORKFLOW_REPAIR_REQUIRED` an exakt denselben gebundenen Artikel zurückgeben. PASS bleibt ausschließlich beim bestehenden hash-gebundenen Handoff.

Wichtig: Der historische 7/7-Lauf vor PR217 beweist **keine unabhängige reale LanguageTool-Endprüfung**; die damaligen generischen Stage-Proofs waren überwiegend Worker-Nachweise. PPM war eine reale Ausnahme. Deshalb wird der alte Code nicht zurückgebaut; übernommen wurde nur das funktionierende Prinzip „gleicher gebundener Worker darf korrigieren, finale Freigabe bleibt extern“.

## Tatsächliche Prüfungen / Live-Ergebnis

- PR #230 Head: `Pferde Atelier Deterministic Entrance Gate` = SUCCESS.
- PR #230 Head: `Pferde Atelier Immutable Base Hardlock` = SUCCESS.
- Danach realer produktiver 7/7-Lauf über PR107 auf Main `66c4224d68532307f6c7f69aff81d1da04cae4e7`.
- Ergebnis: **KEIN 7/7-PASS.** Erster sichtbarer terminaler Befund: `PPM679_REAL_EXECUTION_BLOCKED` / `FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`.
- Die sichtbare Terminalausgabe enthält **nicht** den ersten verschachtelten PPM-Grund. Dieser Grund darf nicht geraten werden.
- 107008 wurde nicht erreicht. Publish blieb gesperrt.

## CURRENT / NEXT ACTION

`CURRENT_STATE.json` muss daher `BLOCKED` auf 107007 mit `PPM679_REAL_EXECUTION_BLOCKED` führen.

Nächster zulässiger Schritt: im **gleichen bestehenden gebundenen PPM/Handoff-Pfad** den ersten verschachtelten PPM-Grund sichtbar machen. Ist er bereits reparierbar klassifiziert, darf nur derselbe `current_item` über den bestehenden Repair-Return korrigiert und erneut geprüft werden. Ist er technisch/Binding/Hash/Identity/Publish-bezogen, bleibt er terminal und nur diese Ursache darf repariert werden.

Keine neue Architektur, kein neuer Prüfer, kein neuer Runner/Gate/Controller/Sidecar, keine Regelabschwächung, kein Worker-PASS.

## Ziel / Parallelwege / Archiv

- Zielvertrag `ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json` bleibt unverändert.
- Permanenter Dispatcher PR107 bleibt nur Startweg und ist auf den aktuellen Main synchronisiert.
- Separater Draft-PR #231 „System 3 Codex normal-parent realtest“ ist ein fremder Parallelweg und bleibt vollständig getrennt; kein Merge/Überschreiben aus diesem Arbeitsweg.
- PR #225 ist durch den sauberen gemergten PR #226 abgelöst und nur Historie.
- Das Protokoll vom 10.09.2026 bleibt Historie und darf nicht als CURRENT verwendet werden.

## Nicht anfassen

Textmaschine, Inhalts-/Qualitätsregeln, PPM 6.7.9-Regeln, PSERC, PSTE, LanguageTool-Regeln, SEO/Links/Tabellen/Dubletten/Design, WordPress-Fachlogik, Endstempel-/Publish-Sicherheit, offizieller Cloud-Entry und Single-Door-Navigation. `publish_allowed=false`.
