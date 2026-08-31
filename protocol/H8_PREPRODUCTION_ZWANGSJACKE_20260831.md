# H8 – PREPRODUCTION-ZWANGSJACKE / PROTOTYP-PROTOKOLL

Stand: 2026-08-31

## Ziel
Der Chat darf ab der ersten Sekunde keine eigene Workflowentscheidung treffen. Der Wächter bleibt vollständig fachblind und bewertet keine Inhalte oder Qualität.

## Ursache der bisherigen Lücke
`READY_WAITING_PACKAGE -> R_PRE_001` verlangte bereits ein fertiges signiertes Produktionspaket. Dadurch lag dessen Erzeugung vor der wirksamen Pakettür.

## Hart geprüfte Varianten
- Prompt allein: verworfen.
- Bestehende `R_PRE_001`-Tür allein: verworfen.
- Zusätzliche Tür ohne signierte Herkunft: verworfen.
- Gewählt: `R_BOOT_001` vor `R_PRE_001` + signierte H8-Herkunftsbindung + erneute Herkunftsprüfung vor `R_001`.

## Umsetzung
`CURRENT_STARTMASTER -> project_single_door_entry_v2.py -> R_BOOT_001 -> signiert H8-gebundenes Paket -> R_PRE_001 -> runtime_batch_slot_guard_h8.py -> R_001`.

Ein Paket ohne signiertes `h8_bootstrap_binding` oder mit falscher Generation/Batch/Snapshot-Herkunft ist nicht produktionsautoritativ.

H8 prüft ausschließlich technische Herkunft, Bindung, Hash/Signatur und Türfolge. `quality_authority = NONE`; `content_semantics_inspected = false`.

## GitHub-CI-Beweis vor Merge
Temporärer PR #57 war ausschließlich ein nicht zu mergender Testträger.

Run 102 / Job `hardlock`: SUCCESS.
- Legacy gate: PASS
- Codex Cloud gate: PASS
- Production continuity: PASS
- H8 positive/negative test: 8/8 PASS
- realer aktueller Raum: `R_BOOT_001`
- aktive Eingangsschicht bleibt API-frei und fachblind

## Produktiver Stand
PR #58 wurde nach PASS von `hardlock` und `hardlock-base` per Squash auf `main` gemergt.

Merge-Commit: `298711faf3a17ff3faeed53de8276f812523c96d`.

Post-Merge-Push-Run 104: SUCCESS.

`main/control/CURRENT_STARTMASTER.json` bindet `project_single_door_entry_v2.py`; `free_chat_execution_authority=false` bleibt aktiv.

## Externe Restbindung
Der private Workflow-Signer bleibt ausserhalb des Repositorys. Die serverseitig an `R_BOOT_001` gebundene Producer-/Signer-Capability muss die H8-Bindung im signierten Workflow-Release erzeugen. Bis diese Capability in der Laufzeit verfügbar/gebunden ist, bleibt `R_BOOT_001` fail-closed. Kein Chat-Fallback.

Das Repository enthält absichtlich keinen privaten Signierschlüssel und darf keine Ersatzsignatur oder Ersatzproduktion erzeugen.

## Unverändert
Keine Fach-, Inhalts-, Qualitäts-, SEO-, Titel-, Keyword-, LanguageTool-, PPM-, PSERC-, PSTE-, Design-, Dubletten-/Kannibalisierungs- oder Publish-Regel wurde geändert.

Vollständiger Master: `control/startmaster0107/H8_PREPRODUCTION_ZWANGSJACKE_MASTER_20260831.md`.
