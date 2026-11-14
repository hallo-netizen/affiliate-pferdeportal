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


## Ergänzung: 31 Original-Aufrufbelege und 23-Regel-Sperrliste

**Neue direkte Quellenprüfung:** [Aufrufstellen-Gegenprobe (JSON)](2026-11-14_TEXTERSTELLUNG_ORIGINAL_AUFRUFWEGE_V1.json), mit **31/31** positiven Quellstellen in den alten PSTE-/PSERC-Dateien. Nachweisbare Kette: `PSTE_Plugin::init → PSTE_Research_Driver::register → cron/Anstoß → PSTE_Breadth_Research_Queue::advance / PSTE_Research_Job::advance → PEOPLE_ALSO_ASK/QUESTIONS → PSTE_Runner → PSTE_Repository`; Titel importiert die Originaldaten aus dem Pool, PSERC-Manifest und -Importer haben weitere identifizierte Originalabhängigkeiten. Es handelt sich um **statische Codebelege**, nicht um einen Live-Erfolg.

Die TXE-Hauptdatei hat vier eigenständige aufgerufene Stellen, aber **keinen** der sechs ausdrücklich geprüften direkten Original-Verbindungen: Treiberregistrierung, PAA-Task-Aufruf, automatische Original-SEO-Klassen, Themenpool-Originaltabellenzugriff, PSERC-System4-Import oder PPM-Rückleseaufruf. Der Code der TXE-Clientmethoden allein ersetzt den Original-Worker **nicht**. Die Suchprüfung gilt für die TXE-Hauptdatei; dynamische Aufrufe über nicht geprüfte Wege sind damit nicht generell ausgeschlossen.

**Zusätzliche Grenze:** Die PPM-6.7.9-Original-ZIP ist auf GitHub nachweisbar (unter `control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`, 1.614.485 Bytes). Ein lesbarer Volltext des PPM-Originals liegt dieser Prüfung weiterhin **nicht** vor. Deshalb keine Behauptung, die notwendige PPM-Importfunktion könne entfallen.

### Verbindlicher Stand aller 23 Zielvertragsregeln für 0.4.1 (keine Freigabe)
| Regel | Ziel | Abnahme aktuell | Nächster notwendiger Beweis |
|---|---|---|---|
| 1 | Originalfunktionen erhalten | **BLOCKIERT** | 0.4.1 ersetzt mehrere Originalarbeitswege |
| 2 | Getrennte Worker | **OFFEN** | Fach- und technische Rollen alt gegen neu abgleichen |
| 3 | Eine vollständige automatische SEO-Entscheidung | **BLOCKIERT** | Original-SEO und PAA nicht im normalen 0.4.1-Lauf |
| 4 | K0 alleinige Textqualität | **OFFEN** | K0 und WP-Rücklauf real prüfen |
| 5 | Nur eine Auftragsquelle, kompletter Altbestand | **BLOCKIERT** | Alte Themen-, Zuordnungs- und Identitätstabellen fehlen im TXE-Abgleich |
| 6 | Reservierung/Doppelexport | **OFFEN** | Nur simulationsnah, kein echter Parallel-WP-Test |
| 7 | Wiederanlauf ohne erneute Freigabe | **OFFEN** | Abbruch/Wiederaufnahme am echten Auftrag nicht bewiesen |
| 8 | Genau ein WP-Entwurf | **OFFEN** | Echter Doppelimport plus Publish-Sperre fehlt |
| 9 | Titel/K0-Schnittstelle unverändert | **BLOCKIERT** | Manifest und PPM-Import ohne Originalbeweis ersetzt |
| 10 | Nur nutzlose Teile entfernen | **OFFEN** | Alle tatsächlichen Abhängigkeiten noch nicht geschlossen |
| 11 | Keine Zusatzinfrastruktur | **OFFEN** | Bis endgültiger Release mit Quelle kontrollieren |
| 12 | Live-Schutz, Testisolierung | **OFFEN** | In diesem Prüfschritt keine Liveänderung; WP-Echtlauf ausstehend |
| 13 | Historische 61 Freigaben respektieren | **OFFEN** | Altbestandsdaten und IDs noch nicht live identisch nachgewiesen |
| 14 | Original-vs-Neu-Echtlauf erforderlich | **BLOCKIERT** | Nicht durchgeführt |
| 15 | Ein zentrales Protokoll | **TEILBELEG** | Nachweis im bestehenden GitHub-Prüf- und Arbeitsprotokoll |
| 16 | Einmalige Zuständigkeit erzwingen | **OFFEN** | Kein vollständiger Callgraph/Negativtest vorliegend |
| 17 | Quellcodebereinigung ohne Verlust | **OFFEN** | Mögliche entfernbare Dateien nicht belegt |
| 18 | Portalneutralität | **OFFEN** | Hobby Depot/Hab & Bewahr noch nicht mit Originaldaten abgenommen |
| 19 | Sofortartikel ohne Nebenplanung | **OFFEN** | Vollständiger Gleichlauf mit Altbestand nicht geprüft |
| 20 | Diagnose ohne zweite Fachprüfung | **OFFEN** | Nur lokaler Nachweis, echter WP-Diagnosebericht fehlt |
| 21 | Vollständiges Backend | **OFFEN** | Menüs existieren im Test-Code, Automatismen fehlen |
| 22 | Sichere Aktivierung ohne Sperrfehler | **OFFEN** | Nur simuliert, realer WP-Aktivierungstest fehlt |
| 23 | Quellcodeidentität und vollständiger Alt-Neu-Diff | **BLOCKIERT** | 0.4.1 0/6 identische PHP-Dateien, kein Funktionsgleichheitsnachweis |

**Zählung:** 6 direkt blockiert, 16 offen, 1 teilweise belegt; **0 vollständig als neuer Zielworkflow abgenommen**. Alle anderen Einzelvorgaben des Regeltextes gelten unverändert, diese Zeilen verkürzen den Vertrag nicht.

**Harte Schlussfolgerung:** **Keine Neuimplementierung, kein Release.** Originaldateien wurden nur gelesen, 0.4.1 unverändert gelassen. Erst die Original-Aufrufkette inkl. PPM vollständig klären, dann nur gezielt unveränderten Originalcode in isolierter Umgebung verwenden; notwendige Anschlussänderungen separat nachweisen und ausdrücklich freigeben. Danach Alt-Neu-Echtlauf, vorher keine neue installierbare ZIP.


### Original-Funktionstests: 44 PASS mit unverändertem Quellcode

- **Im aktuellen Arbeitsgang wirklich ausgeführt:** zwei schon existierende QA-Testdateien, **ohne Änderung der Testdateien oder des Original-PHP-Codes**. Reiner lokaler Testpfad auf die abgelegten PSTE/PSERC-QA-Quellen, PHP 8.4.24.
- `QA_20261113_KISS_30_ORIGINALMINI_TESTS.php`: **30/30 PASS**; echte Original-Methoden von `PSTE_Mini_Workflow`, `PSERC_Slot_Allocator` und `PSERC_Plan_Slot_Identity` mit künstlichen WordPress-/Produktionsplandaten; feste Freigabe, Titel nur extern, PPM-Platzkennung, Schutz vor Doppelvergabe und manipulierten Eingaben.
- `QA_20261113_KISS_PPM_SPAETER_STARTSCHUTZ_TEST.php`: **14/14 PASS**; originale `PSERC_PPM_Bypass_Guard`-Methoden mit nachgebautem WP-Hook-System und simulierten PPM-Klassen; alte direkte PPM-Browseraufrufe werden unter diesem Test blockiert.
- Beide Prozesse mit Exitcode 0. [Maschinenlesbarer Laufnachweis mit Test-/Originaldatei-SHA und deutlichen Grenzen](2026-11-14_TEXTERSTELLUNG_ORIGINAL_QA_TESTLAUF.json).
- **Grenze:** Diese 44 PASS beweisen nur die genannten *alten* Funktionen mit Testdaten, nicht automatische SEO-/PAA-Recherche, echtes WordPress, Datenbankabgleich, reale PPM-6.7.9-Schnittstelle, K0 oder das neue Plugin 0.4.1. **Kein Alt-Neu-Vollvergleich, keinerlei Installationsfreigabe.**
