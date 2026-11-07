# Pferdeatelier – PSTE MINI – verbindliche Übergabe 07.11.2026

**Arbeitsstand:** PSTE-Testplugin **0.57.144.16** (NICHT K0 ändern, NICHT LIVE-K0 ausführen); aktuelles GitHub-Test-PR **#656**; Campus-Basis `hobbyroom/project-memory-campus-v1-20260905`.

**Originaldiagnose:** `pste-stapelbericht-2026-11-07.json` (vom 07.11., Version 0.57.144.16), Batch **87/87 COMPLETE**, **7 PASS**, **78 HELD**, **2 BLOCKED**, Übertragungsfehler 0. 100er-MINI: **87 JA, 9 VIELLEICHT, 4 NEIN**, insgesamt 97 Titelideen.

**Beobachtete Grenzen (echter WP-Stapelbericht, nicht synthetisch):**
- **7** `PSTE_PORTAL_RELEVANCE_NOT_PROVEN` trotz MINI-JA.
- **59** `PSTE_TITLE_READY_CATEGORY_DECISION_OPEN` (darunter **50 reine Kategorieöffnungen**, 9 mit zusätzlichen Intent-Fehlmetadaten).
- **12** `PLANNING_READINESS_BLOCK`: darunter 7 bestehende Titel/Suchfrage-Überschneidungen; 2 breites Thema/Bestand nicht sicher beurteilt; 1 Fragetitel-FAQ-Zuordnung; 1 Kategorieseiten-Überschneidung; 1 kommerzielles Suchziel.
- **2** manuelle `BLOCKED`: eine offene Familienstruktur `PSTE_PORTAL_RELEVANCE_PROVEN_FAMILY_STRUCTURE_GAP`, eine nicht abgeschlossene Produktauswahl `PSTE_PRODUCT_CHOICE_CANDIDATE_RETAINED`.
- Ursprünglich 6 erneute Titelanforderungen + 3 widersprüchliche Altbelege sind im 0.57.144.16-Bericht als *diese* Gründe nicht mehr sichtbar, werden teils als offene Kategorie/Intent geführt.
- **Alle 78 HELD** tragen den unspezifischen Rückgabecode `PSTE_TITLE_DESK_REENTRY_OWNER_NOT_READY`, Ursachen anhand genauer reason_codes prüfen.

**Nutzerauftrag ab jetzt:** Eine **gemeinsame Ursache im echten Quellcode** nachweisen und beheben; **keine Einzelfixes**, kein neuer Überbau, alle echten doppelten Titel-/Relevanz-/Kategorieprüfungen streichen. Gültige einmalig getroffene JA-Entscheidungen sicher und unabhängig von Titelbelegen anerkennen; Quellbindung und Nachweisschutz erhalten; fehlende Kategorien an Redaktionsbüro statt künstlicher Freigabe; echte Dubletten und K0-Schutz erhalten. Die **100er-Stapelprüfung** soll weder alle 5.016 Keywords noch historische >20.000 Schritte einlesen (Gesamtdiagnose nur auf Wunsch). Vor Installer: **positiv+negativ** alle echten 100 und weitere Gegenfälle lokal durchlaufen, ZIP-Syntax und Inhalt prüfen, GitHub speichern und danach **eine** neue ZIP.

**Wichtig:** Eine *Code-Hypothese* aus früherem Chat ist, dass die Relevanz-JA-Entscheidung nicht wirksam vom Mini-Transfer zum Normalpfad gelangt. Das ist bis zum erneuten Lesen des echten Codes und der gespeicherten Nachweise **noch nicht nachgewiesen** – nicht einfach Relevanzchecks entfernen. Die Grenzen des kurzen JSON-Berichts dokumentieren; wenn Nachweise fehlen, klar unterscheiden „nicht übergeben“ von „nicht vorhanden“.

**GitHub-Ablagepfad:** `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/`. Dieses Handoff aktualisieren, wenn sich der nachgewiesene Stand ändert. Das ursprüngliche 0.57.144.16 bleibt unverändert; keine produktive Installation durch den Assistenten.


---

## GEPRÜFTE FORTSETZUNG AM 07.11.2026 – CURRENT TEST-WORKBENCH

**NEUER ARBEITSSTAND:** PSTE-Test-ZIP `0.57.144.17`, **genau diese** aktuelle TEST-Version. Frühere 0.57.144.12–.16 nicht mehr neu installieren. Testartefakt im selben Pluginbüro: `INSTALLATIONS_PAKETE/PFERDEATELIER_PSTE_0.57.144.17_KISS_GESAMTWORKFLOW_NUR_TEST.zip`. SHA256 `d80fc159699815dfa6b722c1962f3c908369089ba921811b803a94bca7d65743`, GitHub-Blob `f4f18c53662b822546042dca4124b0ba08b4ceb0` bytegenau geprüft.

**Behobener zentraler Entwurfsmangel:** Die JA-Entscheidung wird nun direkt aus der bereits gespeicherten MINI-Originalquelle gelesen und von dem einen vorhandenen Relevanzprüfer bindungsgeprüft. Entfällt: zusätzliche `mini_relevance_proof`-Kopie als Entscheidungsquelle beim Titelimport und doppelte Sperrabfrage nach der bereits abgelegten Planungsentscheidung. **Nur drei bestehende Dateien geändert; kein neuer Überbau.**

**Lokales QA:** 100 echte Ursprungskeywords, 87 Originaltitel, 9 VIELLEICHT und 4 NEIN; 7 zuvor tatsächlich mit `PSTE_PORTAL_RELEVANCE_NOT_PROVEN` gesperrte Fälle liefern mit der neuen Quelllese-Funktion Relevanz-PASS. **898 Positiv-/Negativprüfungen PASS, 83 PHP-Syntaxprüfungen PASS.** Original-PSTE-0.57.144.16-ZIP und neue ZIP haben exakt gleiche 121 Dateipfade. Ausführlicher Beleg unter `EVIDENCE/PSTE_05714417_KISS_QA_REAL100_20261107.md`.

**Wichtige Grenze:** Es gibt **noch keinen echten WordPress-Prüflauf mit 0.57.144.17**, daher NICHT behaupten, dass 7 echte Fälle im WP-Bericht bereits PASS sind. Bestehender alter realer 87er-Lauf: 7 PASS, 78 HELD, 2 BLOCKED; 59 offene Struktur-/Kategoriefragen; 12 Planungsblockaden; 2 manuelle Schutzfälle. Diese nicht pauschal freigeben. Die 87 echte WordPress-Reanalyse kann erst der Benutzer im TEST-WordPress auslösen. Im Anschluss nur **100er-Stapelbericht**, keine 5.016-Keyword-Gesamtdiagnose. K0/Live/PSERC/Beiträge/Kategorien nicht verändern.

**NEXT ACTION:** Für den einzigen verbleibenden realen WP-Abgleich einmalig `0.57.144.17` als TEST-ZIP installieren und in `SEO Themenengine → Themenprüfung` vorhandene Schaltfläche `Bereits übergebene Titel nach Plugin-Update erneut prüfen` auslösen, danach `Nur aktuellen Stapelbericht herunterladen (max. 100)`. Kein früherer ZIP-Wechsel und keine Nachweis- oder Keyword-Neuimporte. Nicht ungeprüft weiter an der Relevanzlogik drehen.

**Branch:** `fix/pste-mini-workflow-kiss-20261107`; die Quelle der Test-ZIP ist hier bytegenau archiviert. Produktionssystem K0 bleibt unangetastet.
