# Texterstellung: Quellinventur und verbindliche Vorrelease-Prüfung – 14.11.2026

**Status: kein Plugin-Release, keine Live-Änderung. Zielvertrag [Regeln 1–23](2026-11-13_KISS_ZIELVERTRAG_UEBERGABE_NAECHSTER_CHAT.md) vollständig verbindlich.**

## Nachweisbasis
Die drei originalen ZIP-Dateien wurden tatsächlich im Container extrahiert und kontrolliert. Ihre SHA-256-Werte stimmen mit der bisherigen GitHub-Beweisakte überein:
- PSTE QA 0.57.144.50, `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`: **83 PHP, 1.626 Funktionen, 83/83 Syntax bestanden**.
- PSERC QA 0.28.71, `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`: **42 PHP, 332 Funktionen, 42/42 Syntax bestanden**.
- Texterstellung 0.4.1-test, `f34fe278eaca382ca99c7f537463644dbd1508b9fb4198980e173df59edae280`: **6 PHP, 117 Funktionen, 6/6 Syntax bestanden**.

**131/131 PHP-Dateien und 2.075 Funktionsdefinitionen statisch erfasst** (Funktionen durch Quelltextanalyse). Die vollständige maschinenlesbare [Inventur sämtlicher 131 Quelldateien mit SHA-256, Methodennamen und Zeilen](2026-11-14_TEXTERSTELLUNG_VORRELEASE_QUELLINVENTUR_V1.json) ist im selben Büro abgelegt. Syntax und Anwesenheit sind ausdrücklich **kein Funktionsgleichheitsbeweis**. PSTE und PSERC sind **QA-Vorlagen**, nicht nachweislich gleiche Liveversionen.

## Pflichtfunktionen: Originalquelle gegen Texterstellung 0.4.1
| Arbeitsweg | Nachgewiesene Originalquelle | Negativbefund / offene Gleichheit | Gate |
|---|---|---|---|
| Altbestand/Status | PSTE `includes/class-pste-repository.php` (table() Z.4, createSchema() Z.5) | TXE liest nur alte Freigabeoption, nicht vollständigen `pste_topic_pool` | **BLOCKIERT** |
| Recherche, Google-Fragen und Wiederaufnahme | PSTE `includes/class-pste-research-job.php` (start() Z.39, advanceQuestionsTask() Z.207) | TXE ruft nur Keyword-Vorschläge ab; PAA-Job/Kostenführung fehlt im Ablauf | **BLOCKIERT** |
| Recherchestapel | PSTE `includes/class-pste-breadth-research-queue.php` (start() Z.22, advance() Z.464) | keine originale Warteschlangenfunktion im TXE-Ablauf | **OFFEN** |
| Google-Fragen-Client | PSTE `includes/class-pste-dataforseo-client.php` (postPeopleAlsoAskTask() Z.305, peopleAlsoAskTaskReady() Z.317) | Clientmethoden teilweise abgeleitet, aber normaler Aufruf fehlt | **BLOCKIERT** |
| Automatische SEO-Freigabe/Dubletten | PSTE `includes/class-pste-runner.php` (researchFinalizePrepareInit() Z.127, researchFinalizePrepareCandidateBatch() Z.156) | Original-SEO-Funktionen nicht durch TXE aufgerufen | **BLOCKIERT** |
| Suchabsicht/Artikelart | PSTE `includes/class-pste-editorializer.php` (analyze() Z.22, apply() Z.11) | TXE erwartet manuelle SEO-Felder | **BLOCKIERT** |
| Themen-/Artikelentscheidung | PSTE `includes/class-pste-topic-policy.php` (classifyRole() Z.45, planningSuitability() Z.75) | Originalregeln nicht gleichwertig eingebunden | **BLOCKIERT** |
| Portalrelevanz | PSTE `includes/class-pste-portal-relevance-gate.php` (evaluateBeforeAssignment() Z.18, evaluate() Z.50) | Original-Entscheidung nicht gleichwertig eingebunden | **BLOCKIERT** |
| Kategoriebedarf/Nachfrage | PSTE `includes/class-pste-analytics.php` (coverageWithArticleCounts() Z.63, priorities() Z.92) | Original nutzt Suchnachfrage/GSC; TXE zählt eigene Aufträge/Artikel | **BLOCKIERT** |
| Titelweg und Sofortartikel | PSTE `includes/class-pste-mini-workflow.php` (exportKeywords() Z.537, importTitleCorrections() Z.702) | TXE eigene Funktionen, Originalvertrag nicht alt-neu getestet | **OFFEN** |
| K0-Export | PSERC `includes/class-pserc-admin.php` (exportK0Manifest() Z.102) | fünf Feldnamen vorhanden, aber Original-Manifestvertrag nicht erhalten | **BLOCKIERT** |
| K0-Snapshot und Manifestbindung | PSERC `includes/class-pserc-plan-snapshot-store.php` (materializeReadyBatch() Z.124, manifestForSelectedBatch() Z.133) | Originalfunktion nicht eingebunden | **BLOCKIERT** |
| K0-Übergabekontrolle | PSERC `includes/class-pserc-metadata-boundary.php` (validateBatch() Z.22) | Originalfunktion nicht eingebunden | **BLOCKIERT** |
| WordPress-Entwurfsimport | PSERC `includes/class-pserc-system4-import.php` (importPayload() Z.46, normalizePayload() Z.122) | TXE eigener Import; PPM-Vertrag fehlt | **BLOCKIERT** |

**Eindeutige Quellbelege:**
- PSTE `class-pste-research-job.php:85–123,207–235` steuert PAA-Aufgaben, Warten, Rückholung, Wiederaufnahme und Kosten. TXE `texterstellung.php:342–369` nutzt nur `keywordSuggestionsDriverStep()`; dort keine PAA-Aufgabenabwicklung.
- Der WP-Bestand liegt in `PSTE_Repository::table('topic_pool')` plus zugehörigen PSTE-Tabellen, Identitäten und Freigaben. TXE `texterstellung.php:513–532` liest nur `pste_mini_keyword_roundtrip_v1` und verwendet sonst einen eigenen Optionsspeicher: unvollständiger Bestandsabgleich.
- Die automatische Redaktion liegt insbesondere in `PSTE_Runner`, `PSTE_Editorializer`, `PSTE_Topic_Policy` und der Kategorieabdeckung `PSTE_Analytics`. TXE `texterstellung.php:371–386` verlangt Kategorie, Artikelart und Suchabsicht manuell. Der separate **externe** SEO-Entscheidungsweg `PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions()` berechtigt ausdrücklich nicht zum Weglassen der ursprünglichen Automatik.
- Original `PSERC_Admin::exportK0Manifest()` (`class-pserc-admin.php:102–129`) prüft Snapshot, Herkunft, Suchintention, Hash und Manifest. TXE `texterstellung.php:229–248` gibt selbst die fünf Pflichtfelder aus. Namensgleichheit ist keine Format-/Vertragsgleichheit.
- Originalimport `PSERC_System4_Import::importPayload()` (`class-pserc-system4-import.php:46–119`) bindet `PPM679_Editorial_Plan_Runtime_Gate::record_readback()` ein. TXE `texterstellung.php:286–339` schreibt selbst Entwürfe. Ein gleichwertiger PPM-/Publish-/Wiederanlaufvertrag ist **nicht** belegt.

## Sperre für jeden zukünftigen Installer
1. **Original zuerst:** Zu jedem erforderlichen Arbeitsweg sämtliche tatsächlich benutzten Originalfunktionen samt Aufrufen, Daten, Status und direkten Abhängigkeiten nachweisen. Das schließt insbesondere alten Keywordbestand, automatische PAA-/SEO-/Kategorieentscheidung, Titelweg, Sofortartikel, K0-Fünf-Felder, Rückgabe und WordPress-Entwurf ein.
2. **Keine eigene fachliche Neuentwicklung:** Nichts fachlich nachprogrammieren, keine alten Automatismen durch Handfelder/Dateiübergaben ersetzen, keine neuen Entscheidungs-/Prüf-Worker. Originalfunktionen unverändert übernehmen. Wenn rein technische Adapter unumgänglich sind, diese **vorher** mit Zeilen-Diff, Notwendigkeitsbeweis und ausdrücklicher Nutzerfreigabe kennzeichnen. Ohne diese Freigabe **blockieren**.
3. **Für jede kommende ZIP:** 1:1-Dateivergleich und vollständige Zeilen-Diffs, Original- und Zielhashes, Zählung unveränderter/adaptierter/neuer PHP-Dateien, Prüfung aller 23 Zielvertragsregeln, derselbe echte Alt-Neu-Ein-/Ausgabetest. **0.4.1 hat 0/6 dateiidentische PHP-Dateien und darf nicht als Übernahme gelten.**
4. **Erst nach Echttest:** Reale WordPress-Testinstallation und echte bisherige drei Aufträge und 20er-Charge, Google-Fragen, Bestandsschutz, Doppelausgabe, Abbruch, Teilimport 13/20, Wiederaufnahme, externer Titel, unveränderte K0-Verarbeitung und genau ein Entwurf ohne automatische Veröffentlichung. Sicherung und PPM-/Guard-Abhängigkeit beweisen. Keine Nutzung historischer QA-PASS-Zahlen als Livebeweis.
5. **Keine Teilfreigabe:** Alles, was offen oder nicht beweisbar ist, sperrt die Installation. **Kein Installer vor vollständigem Nachweis.** Die Freigabe ist auch bei lokal erfolgreicher Syntax ausdrücklich **NICHT erteilt**.

**Aktueller Schritt:** Vollständiger Datei-/Methodenkatalog abgeschlossen; 14 kritische Originalarbeitswege zugeordnet. Noch offen sind die lückenlose Abhängigkeitskette, die identische Funktionsübernahme und der Echtlauf. Es wurde **kein PHP-Plugin neu erstellt, keine WP-Daten geändert und keine Liveversion angetastet**.

### Ergänzung: grobe Quellabhängigkeits-Reichweite (statische Warnung, kein Beweis notwendiger Dateien)
Eine zusätzliche *rein statische* Verweissuche über die Originalklassen (`Klasse::Methode`, `new`, `class_exists`) erreicht von den 14 ausgewählten Kern-Einstiegsdateien aus **106 von 125** Original-PHP-Dateien (77 PSTE, 29 PSERC) Querverweise. Die Zahl sagt **NICHT**, dass 106 Dateien tatsächlich gebraucht werden oder dass 19 andere gefahrlos löschbar sind: WordPress-Hooks, dynamische Aufrufe, Plugin-Einstiegsdateien und die separate PPM-Implementierung können zusätzliche Laufzeitbezüge haben. **Folge:** Keine voreilige Übernahme isolierter Funktionen und keine Löschung aufgrund statischer Suche; Funktion+direkte Abhängigkeiten bis zum echten Aufrufpfad verifizieren. Kein Umbau erfolgt.
