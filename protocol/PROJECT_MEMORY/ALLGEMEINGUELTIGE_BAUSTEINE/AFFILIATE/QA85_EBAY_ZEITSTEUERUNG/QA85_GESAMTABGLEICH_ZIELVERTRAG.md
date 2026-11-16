# Pferdeatelier eBay – verbindlicher QA69-Gesamtabgleich (16.11.2026)

**Ergebnis:** Vorhandene Ursachen, QA9/QA16/QA24/QA77–QA85 und Zielvertrag **gegen den vollständigen Originalcode 6.72.352 zusammengeführt.** Eine einzige KISS-Quellkorrektur mit zwei vorhandenen eBay-PHP-Dateien ist lokal bestanden. **QA69 LIVE: NICHT BESTANDEN; NICHT INSTALLIEREN.** Kein neues Plugin, Zeitgeber oder Produktsuchlauf gestartet.

## Echte aktuelle Beweise

Einziger vorhandener WordPress-Export `pferdeatelier-ebay-sichtbarkeit-20261116-102018.json` (16.11.2026, 10:20:18 UTC): 309 Kampagnen im gespeicherten sicheren öffentlichen Checkpoint; **293** davon mit abgelaufener Quellbestätigung, **8** Quellen nicht verfügbar, **8** grundlegende Ausgabebedingungen bestanden (keine Frontend-Garantie). Lauf `completed`, 139/283 versorgte Familien, 144 offene. Frischearbeiter `running=1`, Cursor 12568, 448 kumulative Prüfungen, 24 Fehler, nächster Termin bereits ~56 Minuten überfällig. 9.792 gespeicherte Quellen und 496 als veröffentlicht markierte Ausgabeobjekte sind **nicht** 9.792 oder 496 sichere öffentliche eBay-Freigaben.

Originalprotokoll QA80: 21/22 Intervalle ~2h zwischen jeweils 5 erfolgreichen Prüfversuchen; reale Rate etwa 2,5 pro Stunde. Die verlässliche Auslösung über GitHub wurde schon am 11.11. unter QA24 als Fehlerquelle nachgewiesen. Der aktuelle Main-GitHub-Lauf 43834993089 endete am 16.11. um 08:55 UTC mit `completed` / `no successor`; der neue 5-Minuten-Takt PR #759 ist **noch gesperrt und nicht übernommen**.

## Fehlerhistorie gegen **einen** Zielvertrag

| Bereits festgelegt | Wiederkehrender Fehler | In derselben Korrektur |
|---|---|---|
| QA9/16: getrennte gespeicherte Recherche und Quellenaktualisierung | Recherche `completed`, `operator_paused` oder `failed` beendete den gemeinsamen Heartbeat, obwohl Availability noch `running` | Reine Verfügbarkeit unabhängig fortsetzen; keine neue Recherche |
| QA24: `idle` darf offene Arbeit nicht als Ende melden | QA84 gab bei abgeschlossener Recherche erneut terminalen Status aus | Heartbeat bleibt `advanced`, solange Frischecursor offen |
| QA69: bereits freigegebener SAFE-Bestand ist maßgeblich | Availability bearbeitete unnötig alte, zwar veröffentlichte, aber nicht mehr SAFE-freigegebene Ausgabeobjekte | Vorhandene **SAFE-Kampagnen-ID-Liste** direkt in die bestehende SQL-Auswahl übernehmen – keine zweite Produktentscheidung |
| QA69: gespeicherter Cursor/Wiederaufnahme statt Neubeginn | Alter Availability-Cursor konnte jenseits der nun maßgeblichen SAFE-Datensätze stehen | **Nur Frische-Cursor** einmal auf den aktuellen bestehenden Checkpoint ausrichten; Recherche-UUID und Recherche-Cursor unverändert |
| QA69: Suche fertig ≠ gesamte Versorgung fertig | Auch der letzte aktive Suchschritt konnte `completed` nach außen melden, während Availability noch `running` ist | Post-Worker-Abschluss respektiert den unabhängig offenen Frischecursor |
| QA77–82: einmalige Auswahl, 7 Tage Suchfrist, nur bestätigte Veröffentlichung, sichere Bereinigung | Wiederholte Entscheidungen, Teilabschlüsse als Publikation, unnötige Suche | Bestehende QA84-Logik unangetastet; alle neun Controller-Modellszenarien erneut getestet |

**Umfang der einen Korrektur:** Nur `includes/trait-ppar-ebay-run.php` und `includes/trait-ppar-ebay.php`. 64 andere Archivdateien unverändert. Kein neuer Worker, kein WP-Cron, keine Tabelle, keine eigene Kategorisierung, kein Reset der eBay-Produkte, keine neue Suchabfrage. Der Patch `QA86_GESAMTPATCH.patch` wurde auf das **unveränderte** QA84-Archiv angewendet und das Ergebnis bytegenau mit der getesteten Arbeitskopie verglichen.

## Gesamtsimulation: Original-PHP, nachgestellte Ein- und Ausgaben

| Vertragsabschnitt | Prüfgrundlage | Ergebnis |
|---|---|---|
| Externer Wecker | GitHub Main + PR #759 | **LIVE OFFEN** – PR blockiert, keine regelmäßige Taktgarantie |
| Recherche / Wiederaufnahme | Originalcontroller, neun Lebenszyklus-Szenarien, 283 tatsächliche Familien-IDs | **LOKAL PASS** – jeweils nur eine Recherche, keine neue Suche bei Quellenauffrischung |
| Fachauswahl / Gegenfälle | QA84 Original-PHP-Regression, 95 historisch echte Item-IDs mit nachgestellten Providerantworten | **LOKAL PASS**, keine aktuelle Anbieterantwort bewiesen |
| Quellenaktualität | 309 SAFE, 496 ältere veröffentlichte und 9.792 historische Quellzeilen *synthetisch angelegt*; aktueller PHP-Refresh-Controller + ursprüngliche SQL-Auswahl | **QA84 RED: 0 Quellen** (alter Cursor), **Korrektur GREEN: 309 Quellen in 16 Paketen**, 0 außerhalb SAFE, 0 Produktsuchen |
| Sichtbarkeitsfilter | Tatsächliche PHP-Basis-Gate-Funktion mit nachgestelltem WordPress-Quellstatus | Vor Ablauf **gesperrt**, nach bestätigter Verfügbarkeit **freigabefähig**, nicht mehr im SAFE **gesperrt**. Kein echter Browser-Frontend-Beweis |
| Öffentliche Veröffentlichung / Cleanup | Neun vorhandene vollständige Controller-Modellszenarien | **5 erwartete Endabschlüsse, 4 erwartete Sicherheitsabbrüche**, SAFE bleibt erhalten; kein öffentlicher Live-Beweis |
| Laufende/pausierte/fehlgeschlagene Recherche + Frische | 15 echte PHP-Handler-Übergangsszenarien | **QA84: 8/15**, **QA85 nur 14/15**, **gebündelte Korrektur 15/15** |
| Abstände/Endstatus | neun vorhandene Fristfälle, 16 vorhandene REST-Statusfälle, 23 PHP-Dateien | **9/9**, **16/16**, **23/23** PASS |
| Keine sicheren Kampagnen | Tatsächlicher Availability-PHP-Code, Checkpoint ohne Kampagnen | **0 Anbieterabrufe**, sicherer Abschluss ohne neue Suche |

**Wichtig zur Simulation:** Die 309 sicheren Kampagnen und 293 Abläufe stammen als Größenangaben aus der echten Diagnose; die 9.792 einzelnen PHP-Modellquellen, ihr Quellstatus und ihre eBay-Antworten sind **nachgestellt**. Die 16 Takte wurden durch Vorziehen des gespeicherten Fälligkeitswertes simuliert. **Keine Live-Dauer- oder eBay-API-Messung.** Die Familie-zu-Angebot-Ergebnisse in den neun Controller-Szenarien sind Modellwerte, nicht öffentlich verifizierte 283 Familien. Nicht als Live-PASS ausgeben.

## Zeitbudget / harte Live-Grenze

Bei einem regelmäßigen *theoretischen* 5-Minuten-Takt und 20 erfolgreichen Quellenprüfungen pro Paket wären 309 Kampagnen nach **16 Paketen, etwa 80 Minuten** einmal durchlaufen. Für den bestehenden Vorlauf von zwei Stunden vor Ablauf der Sechs-Stunden-Bestätigung sind bei 309 gleichzeitig fälligen Quellen aber **mindestens 13 erfolgreiche Prüfungen pro 5-Minuten-Paket** nötig. Mit dem vorhandenen 22-Sekunden-Budget setzt das schnelle eBay-Antworten voraus, die **noch nicht live gemessen** wurden. Bei nur zehn pro Paket dauert die Runde rund 155 Minuten – zu langsam. Deshalb ist die tatsächliche Kapazität und dauerhafte Frontendversorgung **noch offen**, nicht schönzureden.

## Verbindlicher nächster Schritt – KEIN weiterer Konzeptdurchlauf

**Diese eine vorhandene Quellkorrektur** mit dem bereits vorbereiteten [GitHub-PR #759](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/759) **im regulär genehmigten Verfahren** gemeinsam übernehmen (Hardlock nicht umgehen). Danach **am selben bestehenden WordPress-Bestand** ohne neue Suche messen: tatsächlicher GitHub-Takt, API-Quelle-zu-Quelle-Dauer, Rückgang der 293 abgelaufenen sicheren Freigaben, tatsächliche eBay-Karten im Frontend und finaler 283-Familiennachweis. Erst dann QA69 abnehmen. Keine neue Diagnose-Orgie und keine erneute Entwicklung der ganzen Architektur.

**Originale Tests und Daten:** `QA85_GESAMTSIMULATION_BEWEIS.json`, `integration_309.php`, `after_state_transition.php`, `QA86_GESAMTPATCH.patch`, vorhandene QA84-Gesamt- und QA69-Tests. Keine WordPress-, Datenbank- oder eBay-Liveänderungen in dieser Prüfung.