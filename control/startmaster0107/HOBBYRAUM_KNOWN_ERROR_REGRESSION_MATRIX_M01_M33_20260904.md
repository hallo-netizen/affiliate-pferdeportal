# STARTMASTER0107 – HOBBYRAUM-FEHLERMATRIX M01–M33

Stand: 2026-09-04

## HARD RULE

Verbindliche bekannte Fehler-/Regressionstestliste für den Hobbyraum.

- Nur reale bekannte/historisch belegte Fehlerklassen.
- Keine theoretische Zusatzsuche.
- Kein neuer Runner, Gate, Contract, Signer, Executor oder Parallelweg.
- Keine Architekturänderung.
- Bereits bestandene Punkte nur als Regression prüfen, nicht neu analysieren.
- Jeder einmal real aufgetretene, weiterhin relevante Workflowfehler bleibt dauerhaft in dieser Matrix.
- main bleibt unangetastet, bis die komplette Matrix PASS ist.
- publish_allowed=false bleibt unverändert.

## Bestehende Matrix M01–M25

M01 – State-/Bundle-Hash chain: CURRENT_STATE -> 107007; START_HERE -> CURRENT_STATE; 107007 -> 107008; authorized_inputs exakt.

M02 – Unique article files: exakt 7 ARTICLE_<plan_slot>.md; keine ARTICLE.md-Kollision.

M03 – PREPARED Persist/Restore: 107007 persistiert; 107008 restauriert; keine PREPARED_BINDING_MISSING-Schleife.

M04 – Finalize CLI: finalize RECEIPT_REF real aufrufbar.

M05 – Durable Release/Receipt: Release-Receipt und Outputs dauerhaft; zurückgegeben wird der dauerhafte Receipt-Pfad.

M06 – No fake production contract: Manual-/Recovery-Artefakte dürfen nicht als PSERC_APPROVED_PRODUCTION_PACKAGE_V1 durchgehen.

M07 – Recovery not automatically final: Recovery nur final mit Import-Envelope-/Hash-Nachweis.

M08 – PPM ZIP available: Original PPM 6.7.9 vorhanden; SHA-256 acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1.

M09 – PSERC ZIP available: Original PSERC-FIX vorhanden; SHA-256 77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314.

M10 – Preflight fail-closed: fehlende/falsche Runtime-ZIPs blockieren vor Produktion.

M11 – Real PPM call: PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan.

M12 – Fake PPM blocked: vor-/nachgebauter PPM-Report darf keinen PASS erzeugen.

M13 – PPM content_hash: echter PPM-content_hash entspricht exakt finalem Artikel-SHA-256.

M14 – Current Action Handoff: fachworkflow_handoff sichtbar und ausführbar.

M15 – 107007 Handoff instruction: keine widersprüchliche Handoff-Sperre.

M16 – Signer boundary: Produktionssignierer außerhalb Codex-Worker; keine Signer-Credentials im Worker.

M17 – 107008 fail-closed: kein finaler PASS, wenn erforderliche hostseitige Finalisierung fehlt.

M18 – ENDSTEMPEL constants: IMPORT_ENVELOPE_NAME / IMPORT_ENVELOPE_KEYS definiert.

M19 – Merge trigger: GitHub-ENDSTEMPEL erkennt Merge-Commits korrekt.

M20 – Delivery: 7 Artikel + Import-Envelope + Source-Manifest exakt hashgebunden.

M21 – No auto-publish: publish_allowed=false in Runtime, Bundles, Delivery, ENDSTEMPEL und WP-Test.

M22 – Signed production package / H8: WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED / ED25519 / H8-Binding gültig.

M23 – Preproduction/Runtime Guards: automatischer Produktionspfad akzeptiert nur signierten Produktionsvertrag.

M24 – No H8 rollback.

M25 – Article prompt / Fachworkflow boundary: keine freie Neuplanung; bestehender Fachworkflow bleibt autoritativ.

## Historische Regressionen – neu dauerhaft aufgenommen

M26 – Bound Fachworkflow production context available to real PPM
- Historische Fehler: BOUND_RUNTIME_PRODUCTION_CONTEXT_MISSING / BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING.
- Das H8-Bootstrap-Paket darf fachlich leer bleiben; es ist Herkunfts-/Türbindung und keine Fachquelle.
- Ab R_001 erzeugt der aktuelle unveränderte Fachworkflow für current_item den echten fact_pack, production_plan_v4-Kontext, finalen Artikel und die realen Nicht-PPM-Stage-Ergebnisse.
- Vor dem echten PPM darf weder FACHWORKFLOW_PASS noch ITEM_RECEIPT als Voraussetzung existieren.
- Der bestehende FACHWORKFLOW_HANDOFF_REQUEST_V1 transportiert ausschließlich diese aktuellen Ergebnisse plus einen noch nicht als PASS markierten PPM-Eingang mit final_article_ref/final_article_sha256.
- Erst der bestehende reale PPM-Handoff darf den PPM-Proof vervollständigen und danach FACHWORKFLOW_PASS + ITEM_RECEIPT erzeugen.
- Fact-Pack, production_plan_item, production_plan_header, workflow_release_item und workflow_release_metadata müssen artikel-/Plan-Slot-/Batch-konsistent sein.
- Fehlender oder falscher Fachworkflow-Kontext = BLOCKED.
- Kein Ersatzkontext aus alten Artikeln/Recovery und kein künstlich befülltes H8-Paket.

M27 – Current-main / production environment identity
- Historische Fehler: CODEX_CHECKOUT_NOT_CURRENT_MAIN, CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING.
- Dispatcher/Worker-HEAD muss exakt aktuellem main entsprechen.
- Preflight muss den Produktionsumgebungsnachweis erzeugen; Runtime Entry darf ohne ihn nicht starten.
- Kein git-fetch-/Neben-Worktree-Zwang im Worker als Produktionsvoraussetzung.

M28 – Fachworkflow-Handoff request is materially executable
- Historische Fehler: fehlende FACHWORKFLOW_HANDOFF_REQUEST.json, ITEM_RECEIPT_FIELDS_OR_CONTRACT_INVALID.
- Current Action bindet exakt einen bestehenden FACHWORKFLOW_HANDOFF_REQUEST_V1 als Datenübergabe vor PPM.
- Der Worker schreibt diesen Request aus den realen aktuellen Fachworkflow-Ausgaben; er erzeugt vor PPM weder FACHWORKFLOW_PASS noch ITEM_RECEIPT.
- submission_command verarbeitet exakt diesen gebundenen Request intern über den bestehenden Handoff und reicht danach nur das finale Receipt an die bestehende Tür weiter.
- Keine leere Pflichtstruktur; kein Fake-Receipt; kein zweiter Submit-Pfad.

M29 – Release metadata current-batch identity
- Historischer Fehler: RELEASE_METADATA_INVALID.
- workflow_release_metadata muss exakt an aktuellen runtime batch_sha256 und aktuelle Artikelanzahl gebunden sein.
- Falsche Batch-ID oder falscher Count = BLOCKED.
- Keine zusätzlichen frei erfundenen Releasefelder.

M30 – Final context batch identity
- Historischer Fehler: FINAL_CONTEXT_BATCH_MISMATCH.
- Der aus 107007 übergebene finale Kontext, Release-Receipt und die 107008/PSERC-Finalisierung müssen dieselbe aktuelle Batch-ID und Artikelanzahl tragen.
- Kein Kontextwechsel zwischen 107007, 107008 und Host-Finalisierung.

M31 – Codex-native bound action; no synthetic executor dependency
- Historischer Fehler: gebundener Fachworkflow verlangte eine nicht vorhandene separate execute_bound_action-/Executor-Capability.
- Der vorhandene Worker führt ausschließlich die gebundene aktuelle Facharbeit aus und schreibt den vorhandenen Handoff-Request als Datenübergabe.
- Der Worker führt keinen separaten Handoff-Executor aus; submission_command übernimmt den bestehenden Handoff intern.
- Keine synthetische execute_bound_action-Host-Capability, kein zweiter Fachworkflow-Executor, keine Capability-Suche und kein submit-request-Parallelweg.

M32 – PPM runtime package path is bound without environment-variable dependency
- Historische Fehler: PPM679_PACKAGE_ZIP nicht gesetzt / kein gebundener Paketpfad / echter PPM-Aufruf nicht erreichbar.
- fachworkflow_handoff muss den exakten repositorygebundenen PPM-6.7.9-Pfad und PSERC-FIX-Pfad selbst auflösen.
- PPM679_PACKAGE_ZIP / PSERC_FIX_ZIP dürfen nicht zwingend nötig sein.
- Tatsächlicher PPM-Aufruf bleibt M11; Paket-/Regelhashes bleiben M08/M09/M13.

M33 – GitHub ENDSTEMPEL must not depend on Codex git remote/auth
- Historischer Fehler: Codex-Lauf erreichte 107008, konnte finale GitHub-Datei aber wegen fehlendem git remote / GH_TOKEN / gh auth nicht dauerhaft erzeugen.
- Der vorgesehene ENDSTEMPEL-Weg muss aus dauerhaft auf GitHub vorhandener, hashgebundener Quelle arbeiten.
- Kein Codex-Push als Voraussetzung für den finalen Produktionsendstempel.
- Erfolg nur, wenn GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json dauerhaft entsteht; sonst BLOCKED.

## Abschlussregel

HOBBYRAUM PASS nur wenn M01–M33 + hardlock + hardlock-base auf demselben aktuellen Hobbyraum-Head PASS sind.

Danach erst Merge-Kandidat und danach kompletter frischer 7/7-E2E. Keine Reparatur während des Produktionslaufs.
