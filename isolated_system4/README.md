# SYSTEM 4 — TRUE SINGLE ROOM

Status: **REAL CODEX REACHES SYSTEM-4 ROOT / BLOCKED AT CHECKOUT-BRANCH IDENTITY / isolated prototype / test only.** Kein Merge, kein Publish.

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand in `control/startmaster0107/CURRENT_STATE.json` bleibt getrennt und unverändert.

## Verbindliches Ziel

`gebundene Metadaten -> System-4-Root-Einstieg -> Codex recherchiert -> Research Evidence -> Facts/Fact-Pack -> Context -> Draft -> unveränderte echte Prüfer -> gezielte Same-Article-Reparatur -> Batch-Gate -> V2-Handoff -> Parent-Chat-Rekonstruktion -> exakte WordPress-JSON`

Codex bleibt der eine fachliche Worker. System 4 übernimmt keine Legacy-Orchestrierung. `publish_allowed=false`; Signing/ENDSTEMPEL bleiben für diesen Pfad aus.

## Eintrittsstatus

Historischer erster Real-Lauf:

`isolated_system4/PROTOKOLL_REALRUN_20260913_SINGLE_ARTICLE_ENTRY_BLOCKER_SPEED.md`

Er wurde noch vor System 4 durch die alte Runtime-Entry-Strecke mit `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING` blockiert.

Daraufhin wurde die immutable Root-`AGENTS.md` **nicht** verändert. System 4 bekam stattdessen die branchlokale `AGENTS.override.md`, die Codex auf die System-4-Root-Tür bindet.

### Zweiter realer 1-Artikel-Lauf

Aktueller Beleg:

`isolated_system4/PROTOKOLL_REALRUN_20260913_ONE_ARTICLE_BRANCH_IDENTITY_BLOCKER.md`

Gebundener Artikel:

- `Beratung`;
- `putzbox-beratung`;
- Titel `Putzbox für Pferde richtig auswählen`;
- Keyword `Putzbox für Pferde`;
- exakt 1 Item;
- `publish_allowed=false`.

Der reale Codex-Lauf erreichte diesmal tatsächlich:

`SYSTEM4_ROOT_INDEXED_INGRESS`

und führte aus:

`python3 isolated_system4/root_entry.py start-stdin /tmp/system4-one-article-production`

Terminaler Blocker:

`SYSTEM4_HARD_BLOCKER:ROOT_ENTRY_BRANCH_NOT_SYSTEM4`

Damit ist die frühere Legacy-Entry-Kollision für diesen Lauf **nicht** erneut aufgetreten. Codex kam bis zur System-4-Tür.

Der aktuelle Fehler liegt in `root_entry.py`: Die Datei verlangt über `git branch --show-current` exakt den symbolischen Branch-Namen `hobbyroom/system4-true-single-room-v1`. Diese Bedingung war im realen Codex-Checkout nicht erfüllt.

Nicht behauptet wird, welcher konkrete Branch-String geliefert wurde oder ob der Checkout detached war; dieser Wert wurde im Codex-Abschluss nicht ausgegeben.

Nach dem Root-Blocker wurden korrekt **keine** Recherche, Facts, Drafts, LT-/PPM-Prüfungen, Batch-Gates oder Handoffs gestartet.

## Vollständiger lokaler Nachweis — Beweisgrenze jetzt korrigiert

Beleg:

`isolated_system4/TESTNACHWEIS_20260913_ROOT_TO_FILE_FINAL.md`

Auf den damaligen bytegleich zum PR gebundenen ausführbaren Dateien wurde **ohne Codex und ohne Mocks** ausgeführt:

- kompletter System-4-Unittestbestand: **93/93 PASS**;
- kompletter `full_local_acceptance.py`: **8/8 PASS**;
- echter LanguageTool-6.8-Lauf;
- echter PPM-6.7.9-Lauf;
- Same-Article-Repair;
- Batch-Gate;
- V2-Handoff;
- bytegenaue WordPress-Dateirekonstruktion;
- finaler lokaler WordPress-JSON-SHA256 `997eb66e13ba9cb0f5387896486583b47da4a799e195cea3f98ae13b424cc58f`;
- `mocks_used=false`, `codex_used=false`, `merge_or_publish=false`.

Dieser Nachweis bleibt für die **lokal getestete Checkout-Identität** gültig.

Die positive Root-Teststrecke lief jedoch im vorhandenen lokalen Checkout auf dem erwarteten symbolischen Branch. Sie enthielt keinen positiven Test für eine PR-/Cloud-Checkout-Semantik mit anderer oder fehlender symbolischer Branch-Bezeichnung. Deshalb war der bisherige Beweis für die äußere Cloud-Grenze zu breit interpretiert.

## Immutable Base

Die alte Root-`AGENTS.md` bleibt unverändert. Die aktuelle System-4-Eingangslösung verändert weder diese Datei noch die alte Produktionsschutzlogik.

Textmaschine, LT, PPM, Batch-Gate, Handoff, WordPress und Design sind durch den neuen Real-Run-Blocker **nicht** als Fehlerursache betroffen.

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

Zielvertrag bleibt unverändert:

- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- JSON / `application/json`;
- `WORDPRESS_DIRECT_IMPORT`;
- `Portal SEO Editorial Plan Compiler 0.28.23`;
- PPM 6.7.9;
- `direct_wordpress_upload_ready=true` erst nach vollständigem PASS;
- `publish_allowed=false`.

## Aktueller Blocker

`S4-BLOCK-REAL-ROOT-BRANCH-IDENTITY`

Nicht mehr aktueller Blocker:

`CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING` — dieser trat im zweiten Real-Lauf nicht wieder auf.

Der reale Lauf beweist jetzt:

`Codex Cloud -> AGENTS.override -> System-4 root_entry.py`

Der Lauf beweist **noch nicht**:

`System-4 root_entry PASS -> Research -> Facts -> Draft -> LT/PPM -> Batch -> V2-Datei`

weil die symbolische Branch-Namensprüfung vorher fail-closed stoppte.

## HOBBYRAUM / NEXT ACTION

System-4-Arbeitsraum: **BLOCKED — ROOT CHECKOUT IDENTITY**.

Verbindlicher nächster Schritt:

1. **kein weiterer Codex-Lauf**;
2. keine Änderung an Textmaschine, LT, PPM, Batch-Gate, Handoff, WordPress oder Design;
3. symbolischen Branch-Namen nicht länger als alleinige System-4-Checkout-Identität verwenden;
4. lokal eine fail-closed PR-/Cloud-taugliche Checkout-/Content-Identität bauen;
5. positive und negative Tests ergänzen, die die reale Cloud-Checkout-Grenze abdecken;
6. danach wieder den **kompletten Einstieg-bis-Datei-Lauf** lokal positiv und negativ ausführen;
7. Immutable Base Hardlock erneut PASS;
8. erst danach und nur nach erneuter ausdrücklicher Nutzerfreigabe darf ein weiterer realer 1-Artikel-Codex-Lauf stattfinden.

Kein Merge. Kein Publish.
