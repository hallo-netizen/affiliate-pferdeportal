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
