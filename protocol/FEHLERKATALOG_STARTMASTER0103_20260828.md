# FEHLERKATALOG STARTMASTER0103

| ID | Fehler | Schutz ab STARTMASTER0103 | Negativtest |
|---|---|---|---|
| F-0039-01 | `plan_slot` im PPM-Plan | bestehender 0039-Guard + neuer Preflight | `BOUNDARY_NEGATIVE_BLOCKED` |
| F-FP-01 | Fact-Pack-/Plan-Scope weicht ab | `PRODUCTION_PACKAGE_PREFLIGHT_GUARD_STARTMASTER0103.py` | `SCOPE_NEGATIVE_BLOCKED` |
| F-CAT-01 | sichtbarer WordPress-Kategoriename durch Slug ersetzt | Preflight: `name == hierarchy_path leaf` | `CATEGORY_IDENTITY_NEGATIVE_BLOCKED` |
| F-REL-01 | Supervisor-Release-Bindung fehlt | Preflight | `RELEASE_NEGATIVE_BLOCKED` |
| F-HASH-01 | Komponenten-/Paket-Hash driftet | Preflight | BLOCKED |
| F-NAV-01 | neuer Chat startet am falschen/alten Schritt | Controller prüft ROOT/State-Hash + Step-Gleichheit | `STATE_HASH_NEGATIVE_BLOCKED`, `STEP_NEGATIVE_BLOCKED` |
| F-TOOL-01 | Modell startet Extra-/Nebenprüfung | Step-Tool-Allowlist, Default DENY | `TOOL_NEGATIVE_BLOCKED`, `MODEL_FORBIDDEN_TOOL_NEGATIVE_BLOCKED` |
| F-STATE-01 | Modell versucht State/Navigation selbst zu ändern | `state_write_authority=CONTROLLER_ONLY` | `STATE_WRITE_NEGATIVE_BLOCKED`, `MODEL_STATE_WRITE_CALL_NEGATIVE_BLOCKED` |
| F-RESULT-01 | Modell meldet Ergebnis für anderen Step | festes Result-Schema mit exact step enum | `MODEL_RESULT_STEP_NEGATIVE_BLOCKED` |
| F-CLAIM-01 | nicht ausgeführter Gate wird als Full PASS behauptet | Controller-Evidence-Scope; kein State-Advance durch Modellbehauptung | fail closed |

Historische Protokolle bleiben unverändert erhalten. Keine Fach-, Inhalts-, Qualitäts-, Design- oder Publish-Regel wird durch diesen Katalog geändert.
