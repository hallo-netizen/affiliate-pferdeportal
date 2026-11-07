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

## 07.11.2026 – zusätzlicher nachgewiesener Doppelprüfungsfehler (NICHT released)

Die v18-WordPress-Stapelberichte zeigten den Fehler fortbestehend. Der Codeweg ist jetzt reproduziert: `reanalyzeRetainedBacklogBatch` wertet MINI-JA aus, danach führt `refreshPortalContextForRow` erneut `prepareEditorialPayload` ohne JA aus und bei NORMAL_PASS denselben Planungsgate nochmals. In isolierter QA-Kopie **nur eine bestehende Datei** angepasst. Original: **7 von 87 JA-Themen verlieren Relevanz** beim Refresh, QA: **0 von 87**; **24/24** Testdubletten bleiben gesperrt; **87/87** falsche JA-Suchfragen abgewiesen; **13/13** Nicht-JA nicht autorisiert; 83/83 PHP-Lints PASS. Bericht: `EVIDENCE/PSTE_KISS_QA_BEWEIS_20261107.md`; diff: `EVIDENCE/PSTE_KISS_QA_PATCH_NUR_PRUEFUNG_20261107.diff`.

**Freigabe BLOCKED:** bisher KEIN wirklicher 1:1-WordPress-End-to-End-Test mit aktuellem WP-Datenbankklon, keine Feststellung „alle Doppelprüfungen im gesamten Plugin entfernt“, deshalb noch KEINE neue Installer-ZIP. K0/PSERC unverändert.

## 07.11.2026 – aktueller KISS-Stand nach vollständiger lokaler Kontextprobe (maßgeblich)

**Original-Installer bleibt 0.57.144.18; KEIN neuer Installer und keine Live-Änderung.** Der frühere QA-Patch `PSTE_KISS_QA_PATCH_NUR_PRUEFUNG_20261107.diff` war für eigenständige Vollaktualisierungen **zu pauschal** und ist durch den neu geprüften, ausdrücklich getrennten QA-Diff **ersetzt**. Nie den früheren Patch unbesehen als Plugin freigeben.

**Aktuell verbindlicher QA-Bericht**: `EVIDENCE/PSTE_KISS_GESAMTWORKFLOW_QA_20261107.md`; **alleine autorisierter, nicht installierbarer Quelldiff**: `EVIDENCE/PSTE_KISS_GESAMTWORKFLOW_QA_20261107.diff`.

In der neuen *isolierten* QA-Arbeitskopie wird der gezielte MINI-87er-Wiederanlauf nach dem ersten Normalpfad + Planungsentscheid nur noch per Kontextbeobachtung aktualisiert (zwei direkte Doppelaufrufe entfernt), während die **separate** Vollaktualisierung mit neuen Bestandsdaten eine erforderliche neue Prüfung ausführen darf. Dabei nimmt sie **immer** das vorhandene MINI-JA als Quelle, statt es erneut zu verlangen. Drei ältere eigenständige Reparatur-/Migrationswege wurden ebenfalls an den gleichen Ursprungsbeleg gebunden. Genau **eine** vorhandene PHP-Quelldatei geändert: `includes/class-pste-repository.php`, Original SHA256 `15344794337def5392b7dd06c1516a6680f0ba2f32ce19477b20076069eb0554`, QA SHA256 `76707c0f7a378284dcdea638e72db664a11cc5eac8289f33100bc7f310d6f985`.

**Tests mit echten PHP-Klassen, aber simulierter Datenbank:** 87/87 JA-Übernahmen und Titel korrekt nach gezieltem Refresh; 0 zweite Bestandsabrufe; 87/87 JA+Titel nach eigenständiger Kontext-Neuberechnung; 24/24 bewusst eingefügte SEO-Dubletten bleiben gesperrt; ungültiger gespeicherter Zustand, fehlender Planungsgate und gefälschter MINI-Rohtext werden ohne Schreibvorgang abgelehnt; gelöschte Kategorie führt im unabhängigen Neuaufbau zu neuer Strukturentscheidung (nicht zur Wiederverwendung der gelöschten ID); 83/83 PHP-Syntaxprüfung PASS. Testeingaben: 100 ursprüngliche MINI-Ergebnisse (aus zwei Nutzerdateien) + tatsächlicher 87er WordPress-Bericht, historische 1.165-Kategorie-Fixture mit *simulierten Term-IDs*.

**Strikte Freigabesperre:** kein nachgewiesener echter 1:1-WP-Test, da aktueller DB-Klon, echte WP-Cron-/SQL-Transaktionen und reale Term-/Post-IDs fehlen. **Keine neue Version ausgeben oder 1:1 behaupten.** Die übrigen Kategorie-/Planungs-Sperrgründe aus dem 40/87-WP-Zwischenbericht sind nicht automatisch behoben. K0 / PSERC / Produktion unverändert. Für wahre Vollfreigabe wäre ein isoliertes echtes WP-Staging mit aktueller Datenspiegelung nötig.


## 07.11.2026 — PSTE 0.57.144.20, Redaktionsbüro-KISS, lokale Gesamtprüfung

**Neueste lokale Testversion:** `PSTE-0.57.144.20-NUR-TEST.zip`, SHA-256 `6631dda5298be101e999f5e2c2ec63ce6352545395c83a2cbe9a3832bf6c9f79`. Existierende Plugin-ZIP v19 als Basis; **nur zwei vorhandene PHP-Funktionen/Dateien und der Versionsheader** geändert, K0/PSERC unangetastet. Die tatsächlichen 21 erledigten WordPress-STRUCURE_GAP-Fälle bekamen lokal bisher keinen Room-Marker, weil `attachWorkerFlow` irrtümlich fertige Fach-/Magazin- und Typentscheidungen VOR der Redaktionsbüro-Zuweisung verlangte (18 UNDECIDED, 3 Typ offen). Nun 21/21 Raumzuweisungen. **Zweimal** echter `PSTE_Repository::reanalyzeRetainedBacklogBatch` mit 87 Originalthemen, lokaler WP-Tabellen-/Index-Nachbildung, speichern/lesen/kontextrefresh; 2×87 ohne Verlust der JA/Titel/Raumfelder. 24/24 echte simulierte Keywordduplikate bleiben gesperrt, Negativcases bestanden, ZIP validiert und 83/83 PHP-Lint. Nachweis: `EVIDENCE/PSTE_05714420_KATEGORIE_KISS_WORKFLOW_QA_20261107.md` (GitHub). 

**NICHT behaupten:** Kein produktiver 1:1-Test mit echter WP-DB, 11 aktuelle Planungsstopps nur aus WordPress-Fehlercodes bekannt, nicht mit echten Beiträgen verifiziert; 47/87 im Bericht noch PENDING. Keine Garantie „87 echte PASS“. Testinstallation und aktueller 87er-Bericht bleiben zum echten Abgleich notwendig.


**EXAKTE ZIP AUF GITHUB (07.11.2026):** [PSTE 0.57.144.20](https://github.com/hallo-netizen/affiliate-pferdeportal/blob/archive/pferdeatelier-pste-05714420-20261107/protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/INSTALLATIONS_PAKETE/PSTE-0.57.144.20-NUR-TEST.zip), Archivbranch `archive/pferdeatelier-pste-05714420-20261107`. GitHub-Blob `de00b33afc7f98997e2d98549c66736926b393b6`, lokale ZIP-SHA256 `6631dda5298be101e999f5e2c2ec63ce6352545395c83a2cbe9a3832bf6c9f79` / 621792 Bytes; beide Angaben nach GitHub-Rücklesen bestätigt. Die vorliegende offene PR #663 enthält **nur die Dokumentation**, die binäre ZIP ist im separat verifizierten Archivbranch gespeichert. Testversion, nicht Live-freigegeben.


## 07.11.2026 — PSTE 0.57.144.21: EIN zentraler Planungsowner, 3 Ausgänge

**Aktuelles TEST-Plugin exakt in GitHub:** `INSTALLATIONS_PAKETE/PSTE-0.57.144.21-NUR-TEST.zip`; SHA-256 `e7c31de26437c52ce80962a2ce46782641d518b30d7974ff462c40c8ae37dc7e`; Git-Blob SHA1 `fb20054e06ce910d0147bd1e551082d0ef95d90c`, **nach Upload byteidentisch bestätigt**. Testprotokoll: `EVIDENCE/PSTE_05714421_KISS_ZENTRALE_PRUEFUNG_NACHWEIS_20261107.md`.

**Belegte Altfehler:** In v20 wurde die komplette Rohfrage im vorhandenen Titel als **sichere Dublette** gesperrt, auch wenn der Titel eine andere Zielgruppe/Zweck beschrieb. Eine gleich gemeinte, anders formulierte Überschrift konnte ohne gespeichertes SEO-Keyword passieren. Neues KISS: **EIN bestehender** `PSTE_Planning_Readiness_Gate`, ohne zusätzliche Instanz: `PASS` für kein belegten Konflikt, `BLOCKED` für belegte Dublette/andere eindeutige Sperre, `REVIEW_REQUIRED` für bloße Titelformulierung oder dieselbe Artikel-Familie/Art mit unbekanntem Alt-SEO-Keyword. Dritter Ausgang heißt **nur mögliche andere Suchintention**, nicht „Titel umschreiben“ und NICHT automatische Produktionsfreigabe. Alter Sperrcode wird beim Reentry **aus dem vorherigen Gate entfernt** und vom neuen ersetzt; fremde Codes bleiben. Die vorhandene Admin-Diagnose gibt gespeicherte Treffertitel/IDs und `next_action` zur Kontrolle aus; sie führt **keine zweite Prüfung** aus.

**Nachgewiesene lokale Tests** (aus fertigem ZIP neu entpackt): 13/13 Positiv-/Negativfälle, zweimal 87 tatsächlich ausgeführte Reanalysefunktionen und lokales Speichern, 87 Kontext-Refresh ohne erneuten Bestandsabruf im gezielten Lauf, 63 simulierte Redaktionsbüro/24 normale Kategorien, Altstatus-Migration, Berichtsausgabe, 13 NICHT-JA-Fälle, 83/83 PHP-Lints, nur 5 v20-Dateien verändert. K0/PSERC NICHT verändert. **Keine echte WordPress-Live-DB**: Im 42/87-Bericht v20 fehlten konkrete Treffer-Beitrags-IDs für 7 frühe Titeltreffer; sie können erst mit dem ergänzten v21-Report live nachgewiesen werden. Deshalb nicht „alle 87 live fertig“ oder „keine falschen Sperren im echten WP“ behaupten.
