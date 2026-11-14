# QA71 – KISS-Zielvertrag: vollständige Ablauf- und Echtprotokollprüfung

**Datum:** 14. November 2026  
**Verbindlicher Zielvertrag:** QA69 – nur eine fachliche Produktauswahl, ein Aktualitätsarbeiter ohne neue Entscheidung, eine öffentliche Freigabe, ein verifizierter Endbestand, eine spätere Bereinigung, derselbe gespeicherte eBay-Lauf und ein externer GitHub-Zeitgeber.  
**Entscheidung:** **KEINE GESAMTABNAHME** – der echte exportierte Lauf endet noch bei 5/283, vor öffentlicher Endprüfung und Schlussbereinigung. Alle zusätzlich erfundenen Produktantworten sind ausdrücklich nur Testfälle, keine historischen eBay-Artikel.

## 1. Was mit den echten Originaldaten lückenlos geprüft wurde

| Originalquelle | Inhalt | Nachweis |
|---|---|---|
| `pferdeatelier-ebay-lauf-574cb003b132.csv` | 2.769 **echte, zeitlich geordnete** Ereignisse einer UUID | Alle Zeilen, Reihenfolge, gespeicherter Schritt und Lauf-ID geprüft |
| `Pferdeatelier_eBay_fehlende_Produktfamilien_97507628-4f4.csv` | 278 unterschiedliche fehlende Sollfamilien | 215 ohne Einzelabruf im aktuellen Teilstand, 32 akzeptierte Angebote ohne Abdeckung, 31 ohne akzeptierte Angebote |

**Echter gespeicherter Schluss der CSV:** Status `running`, Phase `gapfill_discovery`, Schritt 474, 468 GitHub-Arbeittakte, 5/283 Familien, 155 ausgewählt/gescannt, nur 2 materialisiert, 153 Einzelfehler. Der spätere Screenshot zeigte Schritt 475 und manuellen Stop/Pause. Kein echter `public_verify`-, `checkpoint_cleanup_business`- oder `completed`-Schritt ist in diesen 2.769 Originalereignissen vorhanden.

**Im echten Altverlauf nachgewiesene unnötige Arbeit:** `business_prune` – 395 Protokollzeilen, 196 verschiedene Arbeitstakte über 3 h 38 min 38 s. In der korrigierten Auswahlphase entfällt diese vorzeitige Bestandsrunde; die spätere Bereinigung aus dem endgültig freigegebenen Bestand bleibt. Daraus darf keine garantierte Zeitersparnis von exakt 3 h 38 min für einen neuen Lauf abgeleitet werden.

## 2. Noch ein nachgewiesener Zielvertragsverstoß beseitigt

In **Original-Plugin v6.72.348** rief `ebay_run_public_source_refresh_tick()` für die Schluss-Aktualität das allgemeine `ebay_refresh_process_row()` auf. Dieses führt **erneute** `ebay_business_classify_portal_item_strict()`, `ebay_business_quality_assess()` und `ebay_upsert_item()` aus – also **wiederholte Kategorie-/Rang-/Kandidatendatenentscheidung nach der ursprünglichen Auswahl**. Das widerspricht dem Zielvertrag. Die bisherigen Gesamtsimulationen erfassten diesen **internen** Aufruf nicht.

In **v6.72.350 QA** ruft genau derselbe ursprüngliche Abschlussarbeiter die **bereits existierende** Methode `ebay_public_availability_refresh_one()` auf. **Auch der normale BUSINESS-Bestandsrefresh** delegiert jetzt auf dieselbe reine Verfügbarkeitsmethode, statt erneut Kategorie, Qualitätsrang und Kandidatenstatus zu bestimmen. Der echte Original-PHP-Vergleich reproduziert hier vorher `Klassifikation 1 / Ranking 1 / Kandidatenschreiben 1`, nachher `0 / 0 / 0`, mit weiterhin **einem** aktuellen eBay-Quellabruf je ausgewählter Testzeile. Sie aktualisiert allein Quelle, Angebotende, Preis und Frische; bei geänderter Identität setzt sie `needs_review`, bei Ende deaktiviert sie das Angebot. Keine Neu-Kategorie, kein Neu-Rang, keine neue Auswahl, keine zweite Freigabeentscheidung. Ein geänderter, beendeter oder zwischenzeitlich überschreibender Quellenzustand wird am Abschluss **explizit unbestätigt** markiert. Kurzzeitige Fehler erhalten die bestehenden Wiederholungen; globaler eBay-Zugriffsfehler (HTTP 401/403) bleibt ein harter Stopp. Nur das vorhandene Fehlerprotokoll der reinen Verfügbarkeitsfunktion wurde dazu vervollständigt.

**Unverändert:** alle anderen eBay-Such- und Auswahlpfade, ein kanonischer REST-Tick, aktuelle GitHub-Workflowdatei, SAFE-Checkpoint, endgültiger Cleanup, alter Cursor, alle anderen Partner, WordPress-Core und Frontend. **Keine zweite Uhr, kein neuer Worker, keine Tabelle, kein Datenexport.**

## 3. Der vollständige Ablauf – gemessener Teststatus

| Abschnitt | Nachweis | Ergebnis |
|---|---|---|
| GitHub-Eingang | Original-YAML vorhanden; tatsächliche regelmäßige GitHub-Auslösung blieb historisch aus | **NICHT BESTANDEN im Livebetrieb** |
| Gespeicherter eBay-Cursor | Originalexport 2.769/2.769, eine UUID, keine rückläufigen Zähler | **ECHTPROTOKOLL bestanden** |
| Recherche, Fachauswahl und Frische | Echte Zähler und 278 Familien geprüft; genaue Item-/Providerantworten fehlen im Originalexport | **Echt-Artikelprüfung offen** |
| Vorzeitiger Bestandsdurchlauf | Vorher/nachher derselbe Original-PHP-Test: unnötige Auswahl-Bereinigung 1→0 | **Codeprüfung bestanden** |
| Einmalige öffentliche Entscheidung | Identische SAFE-Test-IDs: erneute Prüfung 1→0; neue Test-ID: 1→1 | **Codeprüfung bestanden** |
| Finale Aktualität ohne neue Rangentscheidung | Original-PHP-Runtime vorher globaler Refresh 1/1, nachher reiner Verfügbarkeitsaufruf 1/1; sieben Fehler-/Identitätspfade getestet | **Codeprüfung bestanden** |
| Öffentlicher Checkpoint & Bereinigung | Sieben vollständige Orchestrator-Modelle mit originalen PHP-Phasen/Checkpoints/Cleanup | **Modellprüfung bestanden, Live offen** |
| Abschluss und Folgelauf | Elf Zeit-/Laufendefälle aus echtem PHP; echter Originalrun endet vor Abschluss | **Modellprüfung bestanden, Live offen** |

**PHP-Modellfälle:**
- `normal`: `completed`, SAFE-Testbestand 580, Worker-Takte 23, Fehler `kein`. **WordPress/eBay-Eingaben dieser Fälle nachgestellt.**
- `old_blocked`: `completed`, SAFE-Testbestand 579, Worker-Takte 23, Fehler `kein`. **WordPress/eBay-Eingaben dieser Fälle nachgestellt.**
- `new_blocked`: `completed`, SAFE-Testbestand 579, Worker-Takte 11, Fehler `kein`. **WordPress/eBay-Eingaben dieser Fälle nachgestellt.**
- `db_down`: `failed`, SAFE-Testbestand 580, Worker-Takte 11, Fehler `business_public_storage_read_failed`. **WordPress/eBay-Eingaben dieser Fälle nachgestellt.**
- `churn`: `completed`, SAFE-Testbestand 579, Worker-Takte 27, Fehler `kein`. **WordPress/eBay-Eingaben dieser Fälle nachgestellt.**
- `no_new`: `completed`, SAFE-Testbestand 578, Worker-Takte 23, Fehler `kein`. **WordPress/eBay-Eingaben dieser Fälle nachgestellt.**
- `save_fail`: `failed`, SAFE-Testbestand 580, Worker-Takte 11, Fehler `public_checkpoint_commit_failed`. **WordPress/eBay-Eingaben dieser Fälle nachgestellt.**


**Weitere Original-PHP-Prüfungen:** ein Original-PHP-Vorher-Nachher-Beweis des BUSINESS-Refresh mit dem unveränderten Cursor und gleich vielen Quellabrufen, sieben finale Frische-/Fehlerzweige, sieben tatsächliche PHP-Verfügbarkeitshelper-Zweige, 16 REST-Laufstatusfälle, elf Zeitpunktfälle, neun ausgewählte Frischefälle (153 **synthetische** `getItem`-Antworten), 23 von 23 PHP-Dateien syntaktisch gültig. Alle Code- und historischen Protokollprüfungen bestanden. Bei dem Szenario mit Datenbank- oder Checkpoint-Schreibfehler ist der erwartete sichere Endzustand **Fehler**, nicht „Fertig“.

**Die vielen einzelnen Integritäts-Assertions** im JSON sind überwiegend monotone Prüfungen jeder Originalprotokollzeile. Sie sind ausdrücklich **keine tausend unabhängigen Produkt-Freigabeprüfungen**.

## 4. Warum noch keine historische 1:1-Produktergebnis-Simulation behauptet wird

Die beiden verfügbaren Original-CSV enthalten keine vollständigen individuellen eBay-Artikelantworten, Ausgangs-WordPress-Tabellenwerte, Produkt-Identitätshashes und öffentlichen Checkpoints pro Entscheidung. Der echte Lauf selbst hat `public_verify` und `checkpoint_cleanup_business` im gespeicherten Originalexport nicht erreicht. Daher kann niemand mit **diesen** Dateien die echten 153 ausgewählten Produkte neu entscheiden und den tatsächlichen späteren Endbestand exakt nachrechnen. Die sieben kompletten PHP-Phasenketten beweisen die Programmführung **für nachgestellte Eingaben**, nicht die historische eBay-Wirklichkeit. Genau deshalb ist die Gesamtabnahme **nicht bestanden**. **Kein erneuter 150-MB-Export oder zusätzlicher Diagnoseworker vorgesehen.**

## 5. Wiederausführbarer Beweis und Paket

- `QA71_GESAMT_SIMULATION.py`: Originalprotokoll und Fehlfamilien **Zeile für Zeile**, Original-PHP alt/neu, alle sieben Phasenketten, Fehlermatrix und alle PHP-Dateien.
- `QA71_FINAL_SOURCE_SINGLE_DECISION.php`: tatsächlicher finaler PHP-Abschlussaufruf, sieben Ausgangs-/Fehlerfälle – Original vorher/nachher.
- `QA71_BUSINESS_REFRESH_NO_REDECISION.php`: direkter Vorher/Nachher-Test der originalen vollständigen BUSINESS-Refresh-Methode, ohne neue Klassifikation/Rang-/Kandidatenschreiben.
- `QA71_REAL_AVAILABILITY_HELPER.php`: wirklich ausgeführte unveränderte Verfügbarkeitsmethode des Plugins, sieben technische Zustände und erlaubte Datenfeldänderungen.
- `QA71_SINGLE_DECISION.patch`: Codeunterschied zwischen 6.72.348 und 6.72.350.
- `QA71_FULL_WORKFLOW.json`: vollständiger maschinenlesbarer Nachweis mit getrennten Echt-/Modellprüfungen.

**QA-Paket:** `Affiliate_6.72.350_KISS_EINMALIGE_PRODUKTENTSCHEIDUNG_QA.zip` (66 Dateien). Die eigentliche fachliche Korrektur betrifft ausschließlich den bestehenden eBay-Run-Trait und eine kleine Fehlerprotokollkorrektur im bestehenden eBay-Trait; Versionskopf, vorhandene Upgrade-Ausnahme und Readme sind reine Paketpflege. **Kein Live-Installationsbeleg, keine Live-Freigabe.**

**SHA256 Test-ZIP:** `e2d04337bf0d2c3ca8176059231b317f3682343239cef03bb68e4a57fa78c6b6`.

## 6. GitHub-Lieferung – gesonderter unveränderter Echtbeleg

Am 14.11.2026 wurden die realen GitHub-Workflow-Läufe aus der Repository-API abgefragt. In den bis **15:14 UTC** gestarteten Workflows blieb der letzte geplante eBay-Heartbeat weiterhin der Aufruf vom **09:25 UTC**. Der Main-Workflow enthält zwar `*/15 * * * *`, aber ein konfigurierte 15-Minuten-Regel ist **kein Nachweis, dass GitHub sie ausgeführt hat**. Der blockierte Schutz-PR #759 wurde nicht umgangen und kein externer Job geändert. Damit bleibt der GitHub-Teil des Zielvertrags **LIVE FAIL**, selbst wenn die lokale PHP-Kette unter Modellinputs korrekt läuft.

**Zusätzliche offene Codegrenze:** Bei einer komplett neuen Quellversion können andere Upsert-/Materialisierungsroutinen bislang noch eine Klassifikation zur Sicherheitsprüfung vornehmen. Die durch QA71 beseitigte verbotene **erneute** Zuordnung in den beiden Aktualitätsarbeitern ist original-php-geprüft; daraus folgt nicht, dass die gesamte umfangreiche alte Engine bereits eine einzige überprüfbare Fachentscheidung pro Artikel besitzt. Auch deswegen ist dies kein vollständiges KISS-Release.