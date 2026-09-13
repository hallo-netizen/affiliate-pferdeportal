# SYSTEM 4 — TRUE SINGLE ROOM

Status: **LOCAL COMPLETE ROOT-TO-FILE PASS / REAL CODEX-CLOUD PROOF PENDING / isolated prototype / test only.** Kein Merge, kein Publish.

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand in `control/startmaster0107/CURRENT_STATE.json` bleibt getrennt und unverändert.

## Verbindliches Ziel

`gebundene Metadaten -> System-4-Root-Einstieg -> Codex recherchiert -> Research Evidence -> Facts/Fact-Pack -> Context -> Draft -> unveränderte echte Prüfer -> gezielte Same-Article-Reparatur -> Batch-Gate -> V2-Handoff -> Parent-Chat-Rekonstruktion -> exakte WordPress-JSON`

Codex bleibt der eine fachliche Worker. System 4 übernimmt keine Legacy-Orchestrierung. `publish_allowed=false`; Signing/ENDSTEMPEL bleiben für diesen Pfad aus.

## Eintrittslösung

Der frühere reale 1-Artikel-Codex-Lauf vom 13.09.2026 wurde vor System 4 durch die repositoryweite alte Cloud-Entry-Strecke mit `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING` blockiert. Dieser Lauf bleibt historische Fehler-/Geschwindigkeitsevidenz in:

`PROTOKOLL_REALRUN_20260913_SINGLE_ARTICLE_ENTRY_BLOCKER_SPEED.md`

Die erste Reparatur über eine Änderung der Root-`AGENTS.md` war technisch funktionsfähig, aber unzulässig: der `Pferde Atelier Immutable Base Hardlock` blockierte sie als `IMMUTABLE_BASE_CHANGE_DETECTED:AGENTS.md`. Diese Variante wurde deshalb wieder entfernt.

Die aktuelle Lösung verändert die immutable Root-`AGENTS.md` **nicht**. Der System-4-Testbranch besitzt stattdessen die branchlokale Root-Datei:

`AGENTS.override.md`

Sie bindet Codex auf diesem Branch auf genau eine erste System-4-Tür:

`python3 isolated_system4/root_entry.py start-stdin <WORKSPACE_OUTSIDE_REPO>`

`root_entry.py` prüft Branch, Override-Vertrag, unveränderte alte Root-AGENTS, Workspace-Grenze und Input fail-closed. Kein Legacy-Cloud-Entry-/STARTMASTER-Pfad gehört zur System-4-Laufzeit.

## Vollständiger lokaler Nachweis

Aktueller Beleg:

`isolated_system4/TESTNACHWEIS_20260913_ROOT_TO_FILE_FINAL.md`

Auf den bytegleich zum PR gebundenen ausführbaren Dateien wurde **ohne Codex und ohne Mocks** ausgeführt:

- kompletter System-4-Unittestbestand: **93/93 PASS**;
- Root-Einstieg positive/negative Regression: enthalten und PASS;
- kompletter `full_local_acceptance.py`: **8/8 PASS**;
- echter LanguageTool-6.8-Lauf nach exaktem SHA256;
- echter PPM-6.7.9-Validator nach exaktem SHA256;
- absichtlich fehlerhafter Draft -> realer LT-Fund -> `REPAIR_REQUIRED` -> Same-Article-Repair -> erneuter `fullcheck` -> PASS;
- Batch-Gate PASS;
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` kanonisiert;
- `SYSTEM4_PARENT_CHAT_INLINE_V2` gepackt und wieder entpackt;
- rekonstruierte Datei byteidentisch mit der kanonischen WordPress-Datei;
- finaler lokaler WordPress-JSON-SHA256: `997eb66e13ba9cb0f5387896486583b47da4a799e195cea3f98ae13b424cc58f`;
- Dateigröße: `66753` Bytes;
- `mocks_used=false`, `codex_used=false`, `merge_or_publish=false`.

Negativ nachgewiesen:

- kaputter Root-stdin-Input -> BLOCK;
- `publish_allowed=true` -> BLOCK;
- erfundener Fact/Evidence -> BLOCK;
- Design-/Tabellenklassendrift -> BLOCK;
- manipulierter V2-Handoff -> BLOCK;
- manipulierter geprüfter State vor Batch-Gate -> BLOCK;
- Legacy-Runtime-Abhängigkeit -> nicht zugelassen / NO-LEGACY PASS.

## Immutable Base

Die alte Root-`AGENTS.md` bleibt bytegleich zur immutable Basis. Auf dem System-4-Head mit der neuen `AGENTS.override.md`-Lösung ist der GitHub-Workflow **Pferde Atelier Immutable Base Hardlock PASS**.

Die bestehende Deterministic-Entrance-Gate-CI wurde nicht verändert und muss für diese Änderung nicht umgebaut werden; System 4 verändert keinen ihrer beobachteten Control-/Gate-Pfade.

## Universelle Produktionsgrenze

- gebundene Batchgröße: jede endliche nichtleere Menge `1..N`;
- keine künstliche System-4-Obergrenze;
- 1 / 3 / 7 / 25 / 1000 sind Regressionstestgrößen;
- `article_type` kommt aus den gebundenen Metadaten;
- keine System-4-Beitragsart-Whitelist;
- typabhängige Zulässigkeit bleibt Sache der unveränderten autoritativen Textmaschine-/PPM-/Designregeln.

## Unveränderliche Autoritäten

READ-ONLY bleiben:

- Textmaschine und Contentregeln;
- PPM 6.7.9;
- LanguageTool 6.8 / Bestand 43;
- PSERC/PSTE-/SEO-/Metadatenregeln;
- WordPress-Plugin und Signaturschalter;
- Theme/CSS/Design;
- STARTMASTER0107 und offizieller CURRENT_STATE;
- Main/Merge/Publish.

`controller.py fullcheck` bleibt der einzige Produktionsprüfer-Orchestrator. LT und PPM dürfen im Produktionsweg ausschließlich darüber laufen. Reparatur bleibt am selben Artikel.

## Handoff

Zielvertrag:

- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- JSON / `application/json`;
- `WORDPRESS_DIRECT_IMPORT`;
- `Portal SEO Editorial Plan Compiler 0.28.23`;
- PPM 6.7.9;
- `direct_wordpress_upload_ready=true` erst nach vollständigem PASS;
- `publish_allowed=false`.

Nach dem geprüften Artikel findet keine zweite Text-/HTML-/Designtransformation statt.

## Noch offene Beweisgrenze

**Lokal ist der komplette technische Weg vom System-4-Root-Einstieg bis zur finalen Datei positiv und negativ bewiesen.**

Nicht lokal beweisbar bleibt nur die äußere Produktgrenze: dass die reale Codex-Cloud-Ausführung auf diesem PR-Branch die bereitgestellte `AGENTS.override.md` tatsächlich lädt und deshalb als erste ausführbare Tür `isolated_system4/root_entry.py` benutzt.

Dafür ist genau **ein realer Codex-Produktionslauf** der verbleibende Integrationsnachweis. Er darf gemäß `CODEX ECONOMY HARD RULE` erst nach ausdrücklicher Nutzerfreigabe gestartet werden. Bis dahin wird kein Codex-Token verbraucht.

## HOBBYRAUM / NEXT ACTION

System-4-Arbeitsraum: **LOCAL PASS / LIVE PROOF PENDING**.

Nächster zulässiger Schritt:
1. keinen weiteren Architekturumbau;
2. keinen weiteren lokalen Ersatzworkflow bauen;
3. keine Textmaschine-/PPM-/WordPress-/Designänderung;
4. bei ausdrücklicher Nutzerfreigabe genau einen realen 1-Artikel-Codex-Lauf auf dem dann unveränderten, lokal erneut gebundenen Head starten;
5. dieser Lauf muss ohne Stop bis zum echten V2-Elternchat-Relay und zur bytegenau rekonstruierten WordPress-Datei laufen oder am ersten echten nicht reparierbaren Hard-Blocker stoppen.

Kein Merge. Kein Publish.
