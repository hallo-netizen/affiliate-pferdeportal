# Pferdeatelier PSTE 0.57.144.20 – lokaler Gesamtworkflow-Nachweis

**Datum:** 07.11.2026. **Status:** TEST-ZIP nach lokaler PHP-/WordPress-Simulation. Keine echte produktive WordPress-Datenbank eingelesen; deshalb kein Live-Freigabebeweis.

## 1. Nachgewiesene gemeinsame Ursache

Ausgangsbasis: genuine WordPress-Stapelberichte 0.57.144.19, 40/87 verarbeitet, 7 PASS, 32 HELD, 1 BLOCKED, 47 pending, 0 Relevanzsperren unter bearbeiteten Themen. **21 der 33 Nicht-PASS** betreffen Kategorieentscheidung/Artikelart. Das frühere `PSTE_Normal_Metadata_Path::attachWorkerFlow()` verlangte für einen Redaktionsbüro-Auftrag `$areaProven && $type!==''`. Von den 21 real gelisteten Kandidaten ergab die lokale Wiederholung mit den echten Original-Keywords, Sprachtiteln und dem vorhandenen Kategorien-Fixture: **18 `UNDECIDED` bei der redaktionellen Ebene, 3 FACH ohne abgeschlossene Artikelart**. Somit wurden sie nicht mit `CATEGORY_ROOM_TOPIC_POOL`, sondern mit `EXISTING_STRUCTURE_BACKLOG` markiert. Die eigentliche offene Entscheidung verhinderte ihre Weitergabe an den Entscheidungsort. Das ist eine unnötige Bedingung, keine fehlende Kategorie-Datenbank.

**Einzige fachliche Vereinfachung:** Ein bereits nachgewiesen relevantes Thema mit gültigem Sprachtitel, `STRUCTURE_GAP` und offener Zielkategorie darf **ohne vorherige abschließende Entscheidung Fach/Magazin/Artikelart** in das **bestehende** Redaktionsbüro. Der Kategorie-Owner entscheidet dort Fach oben, Magazin unten oder offen behalten. Kein zweiter Prüfer, keine neue Tabelle, keine automatische Kategorieanlage, keine Freigabe zur Artikelproduktion.

## 2. Vergleich: unveränderte Ausgangsdaten gegen vereinfachten Code

Daten: **87 Original-JA-Themen**, alle Originalrohfragen und 87 sprachlich bestätigten Titel; weitere **13 VIELLEICHT/NEIN** als Negativfälle, 1.165 historische Kategoriedefinitionen aus vorhandener Plugin-Fixture mit **simulierten** WordPress-Termnummern. Reale WordPress-Artikel-/Kategorie-IDs stehen nicht zur Verfügung.

- **21/21** bereits im echten Bericht verzeichnete Kategorie-/Artikelart-Haltefälle erhalten nun `category_backlog_required=true`, `work_destination=CATEGORY_ROOM_TOPIC_POOL`.
- Bei allen **87/87** Probeläufen bleibt die verifizierte JA-Relevanz PROVEN, **87/87** Titel unverändert. In der historischen Testkategorieauswahl: **24 NORMAL_PASS**, **63 STRUCTURE_GAP → Redaktionsbüro**. Andere Fälle können bei echten aktuellen WordPress-Term-IDs anders verteilt sein.
- Nachweis des **minimalen Eingriffs**: Gegen die v19-Berechnung änderten sich nur drei Felder (`category_backlog_required` oben und im Pfad, sowie `worker_flow.storage`) bei 63 Testkandidaten. Keine Änderungen an Relevanz, Titel, Artikelart, Familie oder Kategorieentscheidung.

## 3. Ganze lokale Aufruf- und Speicherstrecke geprüft

Aus der **fertigen, erneut entpackten ZIP** wurden echte Plugin-PHP-Klassen geladen. WordPress-Optionen, Tabellen und Datenbankrückgaben wurden lokal ersetzt; PHP-Auswertung und aufrufende Methoden sind unverändert:

1. Original-MINI-JA aus der vorhandenen abgeschlossenen 100er-Entscheidung durch `PSTE_Mini_Workflow::approvedRelevanceFor`.
2. Originaltitel/Typ/Fach/Magazin/Kategorien durch `PSTE_Normal_Metadata_Path::applyToPayload`.
3. **Vollständiger Aufruf** von `PSTE_Repository::reanalyzeRetainedBacklogBatch` **87/87** mit echtem Plugin-Code, gebundenem (simuliertem) Kontextindex, simulierten WP-Tabellen, Speicherung und anschließendem Kontext-Refresh.
4. **Wiederholung mit den gespeicherten 87 Themen** nochmals **87/87**. Die Relevanz, Titel und Redaktionsbüro-Zuordnung blieben identisch. Kein Provideraufruf und keine WordPress-Artikel-/Kategorieänderung.
5. **Echter Admin-Bericht-Erzeuger** `PSTE_Admin::titleDeskReentryDiagnostics` mit 40 erledigten / 47 offenen Vorgängen, 21 erledigte Redaktionsbüro-Aufträge ausgewiesen. Nur LESEN.
6. **Kontext-Aktualisierung:** Ein gezielter Durchlauf übernimmt vorhandene geprüfte Entscheidungen ohne Doppelprüfung; eigenständige vollständige Aktualisierung prüft geänderte Bestände. Absichtlich entfernte Kategorie führt korrekt ins Redaktionsbüro.
7. **Sicherheitsprüfungen:** 24/24 gezielt eingefügte echte SEO-Dubletten blockiert; eine bereits durch einen bestehenden Artikeltitel abgedeckte Suchanfrage gesperrt; nicht passender Titel nicht gesperrt. Ungültige Quellnachweise, 13 fremde NICHT-JA-Kandidaten und manipulierte Titel werden nicht durch die MINI-JA-Berechtigung geschleust. Fehlendes Planungsurteil wird abgewiesen. Die bestehenden drei UI-Aktionen (`ROUTE_FACH`, `ROUTE_MAGAZIN`, `ROUTE_REVIEW`) bleiben erhalten.
8. **Bestehender Planungsgate mit belegter Herkunft:** Von 24 testweise NORMAL_PASS-Kandidaten sind 20 bei leerem Bestandsbild PASS, vier bleiben durch fachliche Sperren blockiert (FAQ-Frage, Kategorie-Überschneidung, reine Kaufabsicht). Das ist **keine** Behauptung, alle 24 dürften in WordPress produziert werden.

## 4. Archiv- und Installationsprüfung

- **PSTE-0.57.144.20-NUR-TEST.zip**; **SHA256 `6631dda5298be101e999f5e2c2ec63ce6352545395c83a2cbe9a3832bf6c9f79`**.
- ZIP-Integrität PASS, ZIP-Inhalt gegen Arbeitskopie Byte-für-Byte PASS, WordPress-Plugin-Hauptdatei und `PSTE_VERSION` = `0.57.144.20`.
- 121 Dateien/Einträge exakt wie bei `.19`. **Nur drei existierende Dateien** geändert: `includes/class-pste-normal-metadata-path.php`, `includes/class-pste-admin.php` (reiner Status-/Berichtszusatz), `portal-seo-topic-engine.php` (Version).
- **83/83 PHP-Dateien** syntaktisch geprüft. Keine Datei aus K0 oder PSERC verändert.

## 5. Was nicht bewiesen ist – kein Raten

**Keine 1:1-Wiedergabe der produktiven WordPress-Instanz:** Die aktuellen bestehenden WordPress-Beiträge, echten Kategorienummern, vorhandene Redaktionspläne und Plugin-/Datenbankzustände liegen nicht als vollständiger Datenbankklon vor. Deshalb können die konkreten **11 Planungssperren** des echten Stapelberichts (u. a. 7 angebliche Titelüberschneidungen) **nicht** als richtig oder falsch gegen echte Artikel bestimmt werden. Sie werden bewusst nicht weggepatcht oder automatisch freigegeben; die bestehende Planungsschutzfunktion ist am Testbestand funktionsfähig. Das eine `PRODUCT_CHOICE_CANDIDATE_RETAINED`-Thema bleibt im bisherigen sicheren Sonderweg – nicht künstlich als normalen Artikel zulassen. Auch der produktive 87er-Lauf ist zum Zeitpunkt des letzten Berichts **erst bei 40/87**, die letzten 47 echten Einzelresultate stehen aus.

**Fazit:** Der gemeinsam nachgewiesene **Redaktionsbüro-Routingfehler** ist im bestehenden Normalweg vereinfacht und über 87 echte Originalthemen, WordPress-Mocks, den vollen ursprünglichen Reanalysecode, wiederholtes Speichern und Erneuern sowie Sicherheitstests nachgewiesen. Das Plugin ist eine **Testversion**, nicht eine unbewiesen 100-prozentige Live-Freigabe.