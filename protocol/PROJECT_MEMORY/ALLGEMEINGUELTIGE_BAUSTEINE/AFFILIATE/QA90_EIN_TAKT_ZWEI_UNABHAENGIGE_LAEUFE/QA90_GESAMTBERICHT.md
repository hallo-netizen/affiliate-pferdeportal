# QA90 – QA69 KISS, ein vorhandener Takt und zwei unabhängig fortsetzbare Arbeiten

**16.11.2026. Status: vollständiger installierbarer QA-Kandidat 6.72.356; lokale Original-PHP-Gesamtprüfung PASS; echte Live-Abnahme offen.**

## Warum das bisherige System erneut stehenblieb

Der tatsächlich vorhandene GitHub-91Heartbeat92 auf `main` beendete bei `idle|completed|failed|disabled` seine Selbstkette. Am 16.11.2026 08:55:16 UTC bis 11:23:12 UTC war die dadurch notwendige nächste periodische `schedule`-Ausführung **147,9 Minuten ausgeblieben**. Eine Verfügbarkeitsprüfung beginnt aber zwei Stunden vor `fresh_until`, sodass dieses Vorlauffenster von der Lücke bereits überschritten wurde. Die ursprüngliche QA89-Quelle gibt bei **abgeschlossener Recherche UND abgeschlossener einzelner Availability-Runde** `idle`/`completed` zurück, obwohl sie bestehende SAFE-Freigaben in sechs Stunden erneut prüfen muss. In 5 von 19 echten PHP-Testfällen gibt die Quelle daher einen terminalen Status zurück, obwohl eine nächste Quellenprüfung ansteht.

## KISS-Änderung am vorhandenen Programm

- Bestehende REST-Route und bestehender GitHub-Workflow **unverändert**. Kein neuer Wecker, Worker, Cronjob, API-Endpoint, DB-Tabelle, Agent oder selbstständiger fachlicher Entscheider.
- Solange der bestehende **SAFE-Checkpoint** nachweislich BUSINESS-Freigaben enthält, signalisiert der vorhandene externe Heartbeat **`busy/public_freshness_waiting`** auch zwischen zwei Quellenprüfungen. Das ist ausdrücklich **Transport wartet**, kein behaupteter Produkt-/Veröffentlichungserfolg. Main-GitHub-Workflow akzeptiert `busy` als aktiven Status und startet den bestehenden nächsten Runner nach 30 Ticks. Damit entfällt die Abhängigkeit von einem verpassten Schedule-Start in den Leerlaufphasen.
- Der unveränderte Frischearbeiter bearbeitet weiterhin nur die bereits freigegebenen SAFE-Quellen, bis zu 20 pro Paket mit 22-Sekunden-Zeitbudget. Der bisherige unabhängige Frischecursor wird fortgeführt. Die wöchentliche Produktsuche behält ihre **einzige** Fach-/Ranking-Entscheidung und wird nicht bei Frischebedarf neu gestartet.
- Bei manueller Pause / Fehler / Abschluss der Suche arbeitet nur Verfügbarkeit weiter. Nach echter Produkt- und Quellen-Sperre gelten weiterhin alle vorhandenen Frontend-Gates. Bei leerem oder ungültigem SAFE-Checkpoint bleibt die bisherige Terminalmeldung erhalten – kein endloser leerer Worker.
- Auf der vorhandenen eBay-Adminseite werden Recherchefortschritt, letzte *angenommene* automatische Anfrage (aus dem bereits vorhandenen Ratenlimit-Speicher), bisherige Anbieterprüfungen und der nächste Termin aus den **bestehenden** Optionen getrennt angezeigt. Keine API-Abfrage aus dem Browser, kein neuer Prüfer. Veraltete Backend-Hilfe ("stündlich / alle drei Stunden") berichtigt auf bestehenden QA69-Vertrag.

## Direkt aus der endgültig gepackten ZIP geprüfte Tests

- 66 originale Plugin-Dateien; 23/23 PHP-Syntaxprüfungen PASS; ZIP CRC und Byte-für-Byte-Dateiabgleich PASS; JS-Syntax geprüft; nur die zwei existierenden eBay-Traits und Versions-/Readme-Einträge geändert.
- Neue Live-Takt-Vertragsfälle: **alte QA89 14/19, neue 6.72.356 19/19**. Frühere unabhängige Statusfälle **15/15** weiterhin PASS.
- Modell aus WordPress-Snapshot-Größen 309 SAFE-Kampagnen, 496 historisch ausgegebene Objekte, 9.792 historische Quellen: **309/309** gezielt in **16 simulierten Paketen**, kein Nicht-SAFE-Angebot, kein erneuter Produkt-Rechercheaufruf, gleiche Run-UUID und gleicher SAFE-Checkpoint. Leeres SAFE-Checkpoint-Modell: 0 Anbieterprüfungen.
- **9/9 Original-Controller-Gesamtszenarien**: fünf erwartete komplette Abschlüsse und vier korrekte Sicherheitsabbrüche; keine doppelte Produktsuche. **95/95 historische echte Artikelkennungen**, aber ausdrücklich **nachgestellte** Anbieterantworten und WordPress-Zeilen.
- Die GitHub-Heartbeat-Kette ist im existierenden main-Workflow bereits selbstfortsetzend; kein Workflow-Dateieingriff oder Hardlock-Bypass. Die direkte Server-Ausführung und ein echter Provider-/Frontend-Abgleich sind noch nicht erfolgt. GitHub-Runner kann im Betrieb unterbrochen werden; bei echten GH-Ausfällen ist eine zuverlässige Lücke nicht ausschließbar.

## Übergabe / harte Vertragsgrenze

**Datei:** `QA90_PFERDEATELIER_AFFILIATE_ZENTRALE_6.72.356_EIN_TAKT_ZWEI_UNABHAENGIGE_LAEUFE_STAGING.zip` (vollständiges Plugin als Ersatz derselben Affiliate-Zentrale; niemals zusätzlich installieren). **SHA256:** `07514e89a721de5a96bd070d83917495352df3b358a86ca62838694052dacdac`.

Ablage im Pferdeatelier-Pluginbüro. **Vor Live-Einsatz WordPress-Datenbank sichern.** Plugin-Aktualisierung selbst startet **keine** neue Suche, löscht/ändert **keine** gespeicherte SAFE-Freigabe oder Produktliste, legt **keine** zusätzlichen Zeitgeber an. Bereits laufende Arbeit wird nicht brutal abgebrochen. Keinerlei GitHub-/Hosting-Handaktion erforderlich.

**QA69-LIVE noch offen:** Nach tatsächlicher Installation ist anhand der vorhandenen Leseseite und der öffentlichen eBay-Karten zu bestätigen, dass die Ausgabegates echte frische Produkte freigeben, die laufende Nachprüfung innerhalb der Frist bleibt, und der 283er-Familienabschluss mit gespeicherter Publikationsliste vorliegt. Weder Simulation noch 91busy92 sind dafür ausreichender Beleg.