# System 4 – Abschluss-/Nachholprotokoll Handoff-Nachtrag 2026-09-12

Historischer Nachtrag zum bestehenden `PROTOKOLL_CLOSEOUT_20260912.md`. Keine CURRENT_STATE-Autorität. Aktueller Stand bleibt ausschließlich `isolated_system4/README.md`.

## Tatsächlich neu festgestellte Fehler
- Ein realer 7/7-Codex-Lauf erreichte Artikel-/Batch-PASS, aber die finale Datei wurde nur als Codex-task-lokaler `sandbox:/mnt/data/...`-Pfad ausgegeben. Der Elternchat konnte die exakten Bytes nicht abrufen. Gesamtworkflow daher `SYSTEM4_HANDOFF_FAIL`, kein finaler Workflow-PASS.
- Die frühere Annahme, ein Codex-Task-Sandbox-Link oder `View task` sei ein belastbarer Elternchat-Download, war falsch.

## Tatsächlich ausgeführte Änderungen
- Handoff wurde als harte Abschlussbedingung in `isolated_system4/AGENTS.md` und `isolated_system4/FULL_RULE_BATCH_TASK.md` verankert.
- `isolated_system4/handoff_transport.py` ergänzt: striktes JSON-Schema, WordPress-Preimport-Metadaten, Base64-Transport, Byte-Länge, SHA256, exakter Readback.
- `isolated_system4/test_handoff_transport.py` ergänzt: Positivfall exact-bytes pack/unpack sowie Negativfälle Transport-Tamper, Body-Hash, fehlende WordPress-Reviewdaten, falscher Upload-Ready-Claim und falsche Artikelanzahl.
- Handoff-Dateiformat verbindlich: `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json`, UTF-8 JSON / `application/json`.
- WordPress-Prüfinformationen verbindlich: Plugin `Portal SEO Editorial Plan Compiler` Version `0.28.22`, PPM `6.7.9`, `WORDPRESS_PREIMPORT_REVIEW`, `direct_wordpress_upload_ready=false`, notwendige Downstream-Komponenten `fact_pack_bundle`, `production_plan`, `workflow_release`.
- Produktions-PR darf keine Artikel-/Transportdatei tragen. Vorgesehener Transport ist ausschließlich ein temporärer Branch `system4-parent-chat-handoff`, danach exakter Fetch/Unpack/SHA-Vergleich im Elternchat und Reset des Transportbranches.

## Tatsächlich ausgeführte Belege in diesem Chat
- Reale 7/7-Produktion vor der Handoff-Grenze: Codex meldete `SYSTEM4_7_7_REAL_ARTICLE_BATCH_PASS`; die behauptete Handoff-Datei war im Elternchat nicht abrufbar. Dieser Lauf ist deshalb nur Artikel-/Batch-PASS, nicht Gesamtworkflow-PASS.
- Die aktuelle System-4-CURRENT-Wahrheit wurde frisch aus `isolated_system4/README.md` gelesen: STATUS BLOCKED; Ursache Handoff; Next Action vollständige Nicht-Codex-Regression + realer Dummy-Transport vor neuem Codex-Lauf.
- PR #238 frisch geprüft: offen, Draft, unmerged; Head bei Abschlussprüfung `0fcf2dca47d9f817a6e41b1694ece71b37ff74cc`.
- Für diesen Head wurden keine GitHub-Commit-Statuschecks gefunden. Daraus wird kein PASS abgeleitet.
- Ein einfacher JSON-Download-Probe wurde in diesem Chat erzeugt und als Chat-Datei ausgegeben; dies beweist nur die Chat-Dateiausgabe, nicht den vollständigen neuen `handoff_transport.py`-Branch-Roundtrip.

## Noch offen / BLOCKED
- Die vom Nutzer verlangte komplette aktuelle Exact-Head-Regressionsprüfung positiv/negativ von Nullpunkt bis Dateiausgabe wurde nach dem Handoff-Umbau noch nicht vollständig ausgeführt.
- Der neue `handoff_transport.py`-Pfad wurde in diesem Chat noch nicht als vollständiger realer GitHub-Transportbranch -> Elternchat -> unpack -> SHA-identisch -> Download -> Cleanup-End-to-End-Lauf belegt.
- Kein neuer Codex-Lauf zulässig, bevor diese beiden Punkte PASS sind.
- Kein WordPress-Upload-PASS. Die Handoff-Datei ist bewusst nur PREIMPORT-Review; direkter Upload bleibt bis PSERC-Envelope + Supervisor-Authentizität BLOCKED.
- Kein Publish; `publish_allowed=false`.

## Eine Wahrheit / Parallelwege
- `isolated_system4/README.md` bleibt einzige aktuelle System-4-Stand-/Next-Action-Wahrheit.
- Dieser Nachtrag und `PROTOKOLL_CLOSEOUT_20260912.md` sind historische WAS/WARUM-/Testprotokolle, nicht CURRENT.
- PR #238 bleibt nur Wegweiser.
- Main/STARTMASTER0107 und dessen eigener M38-/Hobbyraum-Stand werden durch System 4 nicht überschrieben.
- Keine fremden Parallelbranches wurden verändert.

## Plugins
- In diesem Chat wurde kein Plugin entwickelt oder aktualisiert. Portal SEO Editorial Plan Compiler 0.28.22 wurde nur als bestehende WordPress-Schnittstellen-/Schema-Referenz geprüft. Daher PLUGINS: NICHT BETROFFEN.
