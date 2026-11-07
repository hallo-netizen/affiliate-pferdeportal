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

---

## 07.11.2026 – NEUE GEPRÜFTE FORTSETZUNG: v18 ersetzt v17 im TESTBÜRO

**Realbericht v17:** 29/87 bearbeitet (58 PENDING), 3 PASS, 25 HELD, 1 BLOCKED, 4 bereits erneut festgestellte Relevanzsperren. Kein Endbericht. Die Code-Ursache lag im Repository: ein gültiges MINI-JA wurde weiter nur dann erkannt, wenn der bereits gespeicherte Titel den Marker `LANGUAGE_TITLE_DESK_IMPORT` besaß. Das ist eine weiterhin bestehende Titeldoppelabhängigkeit, NICHT sieben isolierte Keywordfehler.

**KISS-Korrektur v18:** Die Titelbedingung an dieser einzigen bestehenden Übergabestelle entfernt. Der Original-MINI-JA-Beleg wird bei übereinstimmender ursprünglicher Suchfrage immer durch den einen vorhandenen Relevanzprüfer anerkannt. Negativentscheidungen und manipulierte Quellen weiter gesperrt. Keine zusätzlichen Regeln, Klassen, Tabellen oder Producer. Nur zwei bestehende Dateien der v17-ZIP geändert (Repository + Versionsnummer).

**Gegenprobe mit 100 Originalthemen:** 500 Aufrufe des echten Repository-Ablaufs mit jeweils 5 unterschiedlichen Titelzuständen; v17 erkannte nur 87/435 echte JA-Kombinationen, v18 435/435; alle 65 VIELLEICHT-/NEIN-Varianten und geänderte Quelle sicher abgewiesen. Vorherige 898 Kontrollen weiter PASS; 83/83 PHP-Lints; ZIP-Dateiliste identisch. Prüfung benutzte vereinfachtes WordPress-Umfeld, der spätere Kategorie-/Planungsprozess wurde bewusst noch vor Schreiben angehalten – keine Behauptung eines produktiven E2E-Tests.

**AKTUELLE TEST-ZIP:** `INSTALLATIONS_PAKETE/PFERDEATELIER_PSTE_0.57.144.18_KISS_RELEVANZ_OHNE_TITELBEDINGUNG_NUR_TEST.zip`; SHA256 `3b0ce3971326753a44274a4d00b0a329e824df954f35e784db762f5935628abf`; GitHub-Blob `f530c4b95cd75b7296cf14dde056b4c4726fe6b5`. Nachvollziehbare Gegenprobe: `EVIDENCE/PSTE_05714418_KISS_RELEVANCE_INTEGRATION_20261107.md`. **v17 gilt nicht mehr als aktuell.**

**OFFEN:** Reale 87/87 Reanalyse mit v18 im Test-WordPress; dort prüfen, ob echte Relevanzsperren fallen. 59 Struktur-/Kategorien-/Intentfälle, 12 Planungssperren, zwei manuelle Schutzfälle sind nicht durch Titel/Relevanz automatisch freizugeben. Nur 100er-Stapelbericht verwenden; kein 5.016er-Gesamtscan erforderlich. K0/PSERC/Live unangetastet. Ohne neuen WP-Bericht keine definitive Erfolgsmeldung.
