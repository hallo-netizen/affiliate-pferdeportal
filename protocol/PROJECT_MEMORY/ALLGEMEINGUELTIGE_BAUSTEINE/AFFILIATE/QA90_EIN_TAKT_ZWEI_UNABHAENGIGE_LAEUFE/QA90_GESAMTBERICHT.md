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

## Live-Zwischenstand vom 16.11.2026, Screenshot 16:07 MEZ (gesichert)

**Nutzer bestätigt ausdrücklich:** Ein Produkt ist auf der echten Pferdeatelier-Website **im Frontend sichtbar**. Dies ist der erste ausdrücklich bestätigte öffentliche Sichtbarkeitsnachweis des aktuellen Durchgangs, **nicht** der Nachweis für sämtliche Produktfamilien oder dauerhafte Frische.

WordPress-eBay-Screenshot zeigt:
- **Status „Fertig“, Phase `completed`**, neuer Lauf beendet und **als sicherer Frontend-Checkpoint übernommen**.
- **309 gespeicherte BUSINESS-Freigaben** weiterhin erhalten.
- **110** Arbeitsaufrufe; letzter echter Fortschritt laut Backend **16.11.2026 13:41:32**.
- Unabhängige Anbieterprüfung derzeit **„wartet“**, letzte Prüfung **16.11.2026 13:36**, nächste Prüfung **16.11.2026 15:36**, kumulativ **562** überprüft, **35** bisherige Prüfprobleme. Diese Zähler sind keine Anzahl öffentlicher Karten.
- Die Protokollwarnung steht jetzt als **historische** Lücke vom 12.11.2026 14:26, nicht als Behauptung eines aktuellen Fehlers.
- **Weiterhin offen:** Im Screenshot steht, dass der **letzte bestätigte öffentliche 283er-Familienabschluss noch nicht gespeichert** ist. Der sichere technische Checkpoint ist nicht dasselbe wie die vollständig nachgewiesene 283er-Bilanz.

**Das tatsächlich im privaten Plugin-Büro archivierte Vollplugin 6.72.356 wurde unverändert wieder geöffnet und geprüft:** Original-Header 6.72.356; Archiv-CRC gültig; SHA256 `07514e89a721de5a96bd070d83917495352df3b358a86ca62838694052dacdac` stimmt mit dem ursprünglichen QA90-Bericht überein. Verifiziert abgelegt unter `/pferdeatelier/PLUGINS/QA/QA90_EIN_TAKT_ZWEI_UNABHAENGIGE_LAEUFE/QA90_PFERDEATELIER_AFFILIATE_ZENTRALE_6.72.356_EIN_TAKT_ZWEI_UNABHAENGIGE_LAEUFE_STAGING.zip`. Original-Screenshot und ausführlicher Zwischenstandsbericht sind **nur in der privaten Projektbibliothek** in demselben Verzeichnis archiviert.

**Kein neuer Plugin-Build, keine Liveänderung, keine neue Suche, keine zusätzliche Arbeit auf Verdacht.** Stand: öffentlicher Produkttreffer vom Nutzer bestätigt; Auftrag QA69 weiterhin nicht vollständig abgenommen (283er-Status und durchgängig pünktliche Frische noch offen).

## Ergänzung zum tatsächlichen CSV- und Screenshot-Stand 16.11.2026, 16:15 MEZ

**Neue Nutzerdaten:** `pferdeatelier-ebay-lauf-3221f8324c99.csv` (229 Ereigniszeilen, UUID `9ca47b30-...`) und Screenshot der eBay-Adminseite um 16:15 MEZ.

**Direkt aus CSV nachgewiesen:**
- Kanonischer Lauf beginnt 12:23:26 MEZ, Phase `reconcile_local`, wechselt um 13:11:04 MEZ nach `refresh_remote`, beendet um **14:42:45 MEZ** mit `status=completed / phase=completed / progress_seq=110`. Die Zustände wurden tatsächlich mehrfach gespeichert. **Keine zweite Suche aus dieser CSV beweisbar**: Such- und Auswahlzähler sind leer bzw. 0.
- Gesonderte Availability-Checkpoint-Speicherungen: 12:26 Uhr `checked=488`; 12:28 Uhr 508; 12:31 Uhr 521 und Runde `running=0`; 14:31 Uhr 541; 14:33 Uhr 561; um **14:36:19 Uhr** `checked=562`, `running=0`, `next_due_at=16:36:18 MEZ`. Somit ist die Anbieter-Frischrunde **tatsächlich beendet und in Option gespeichert**, der nächste Termin liegt **21 Minuten nach Screenshot**, nicht 39 Minuten davor.
- Screenshot zeigt die Zeiten `letzte Anbieterprüfung 13:36` / `nächste Prüfung 15:36` und den letzten echten Fortschritt als 13:41; gegen die Unix-Zeiten der originalen CSV ist das **exakt eine Stunde zu früh dargestellt** (UTC statt Europe/Berlin). Die relativen Angaben `vor 99 Min.` / `vor 93 Min.` sind dagegen korrekt. **Keinen Fehler oder Stillstand aus dieser falschen Uhrzeit ableiten.**
- Die 562 sind kumulativ bearbeitete Prüfungen, **keine** 562 unabhängigen sichtbaren Artikel. Diese CSV enthält **keinen** 283er-Familien-Abschlussbericht.

**Restwiderspruch zwischen vorliegendem QA90-Paket und echtem Transport:**
- Original-6.72.356-Code enthält `ebay_external_tick_public_freshness_watch()` und soll bei safe Checkpoint + BUSINESS + aktivierter Inventory-Refresh für fertiggestellte Recherche `busy/public_freshness_waiting` zurückgeben, damit der bestehende GitHub-Runner sich fortsetzt.
- Echter Main-GitHub-Lauf `43872846236`, Job `133318218314`, meldete am **16.11.2026 14:42:50 MEZ** für den 29. REST-Takt `status=completed`, dann `terminal heartbeat ... no successor runner required`. **Keine weitere GitHub-Ausführung bis zum letzten verfügbaren Abruf zum Screenshotzeitraum 16:15 MEZ nachgewiesen.**
- Somit ist der beabsichtigte Dauerbereitschaftsvertrag von QA90 auf der tatsächlichen WordPress-Installation **noch nicht nachgewiesen**. **Nicht raten**, ob der exakte QA90-Code tatsächlich installiert ist, die Einstellungen/Checkpoint-Gates anders sind oder eine zwischengespeicherte Providerantwort ausgegeben wurde. Die vorliegenden CSV-Felder liefern weder den REST-`plugin_version` noch die SAFE-Gate-Entscheidung. **Nicht noch einmal den alten 2h-Refresh als neuen Fehler darstellen**: 14:36 war erfolgreich, 16:36 ist nächste normale Fälligkeit.
- **Ein einziger maßgeblicher Praxistest:** die bestehende, schreibgeschützte Sichtbarkeitsdiagnose **nach 16:36 MEZ**, sinnvoll gegen 16:45–17:00, prüfen: `freshness_worker.last_batch_at_utc` muss **später als 13:36:18 UTC** (= 14:36:18 MEZ) sein; `next_due_at` weitergerückt; abgelaufene aktuelle SAFE-Freigaben zurückgegangen und Frontendkarte sichtbar. Falls nein, die tatsächliche REST-Antwortversion/SAFE-Watch-Entscheidung im bestehenden Plugin ermitteln, **kein neuer Suchlauf und keine zweite Uhr**.

**Status:** laufende Availability-Option speichert korrekt; der regelmäßige automatische Aufruf nach Gesamtabschluss bleibt ungeklärt. QA69 nicht vollständig abgenommen.


## Echte Sichtbarkeitsdiagnose 16.11.2026, 19:32 MEZ – keine Live-Abnahme

Verbindlicher neuer, schreibgeschützter Nutzerdatenexport: pferdeatelier-ebay-sichtbarkeit-20261116-183237.json, 16.11.2026 18:32:37 UTC. Gegenprobe: pferdeatelier-ebay-sichtbarkeit-20261116-102018.json, 10:20:18 UTC.

| Kriterium | Vorher | 19:32 MEZ |
|---|---:|---:|
| SAFE-BUSINESS-Kampagnen | 309 | 309 |
| Quelle zeitlich abgelaufen | 293 | 10 |
| Diagnose source_not_available | 8 | **290** |
| Diagnose common_gates_passed_not_frontend_proof | 8 | 9 |
| Kumulative Verfügbarkeitsprüfungen | 448 | 562 |
| Kumulative Prüfprobleme | 24 | 35 |

**Nicht als Verbesserung verkaufen:** Zwar weniger abgelaufene Frische, aber **290/309** sind inzwischen unter der Diagnose-Kategorie nicht im Zustand available. Neun bestehen die grundlegenden Lieferbedingungen; kein vollständiger Live-Frontendbeweis.

**Belegter Diagnose-Semantikfehler:** Die separate Diagnosefunktion pa_ev_reason() schreibt source_not_available, sobald source_state !== available. Sie unterscheidet **nicht** die tatsächlich beendete eBay-Quelle ended von needs_review. Letzteres entsteht im echten Plugin ebay_public_availability_refresh_one(), wenn nach einem positiven getItem-Eingang Item-ID, Verkäufername, normalisierter Titel, Bild-URL oder Artikelzustand nicht exakt mit dem gespeicherten Wert übereinstimmt. Dann werden source_state=needs_review, source_checked_at=now und fresh_until=now gesetzt. Alle fünf Diagnosebeispiele für source_not_available zeigen sekundengenau gleiche Werte für source_checked_at und fresh_until. Das ist **mit needs_review vereinbar**, aber die Rohwerte und einzelnen Abweichungsfelder fehlen im JSON. Nicht behaupten, alle 290 Artikel seien wirklich beendet.

**Gegenbeleg zur voreiligen Ended-Interpretation:** Im bereits gelieferten echten CSV pferdeatelier-ebay-lauf-3221f8324c99.csv beträgt der kumulative ended-Zähler der unabhängigen Frischeprüfung um 14:36 MEZ **8**, available **312**, errors **35**, checked **562**. Also keine belegten 290 expliziten Endsignale in dieser Frischerunde.

**Zeitgeber:** Der letzte durch GitHub Actions nachgewiesene eBay-Run endete am 16.11. 13:42:52 UTC (14:42:52 MEZ) mit completed. Bis zum Vergleich gegen den neuen Export kein neuerer eBay-Run nachgewiesen. Frischeoption am Abend: running=0, last_batch_at=13:36:18 UTC (14:36 MEZ), next_due_at=15:36:18 UTC (16:36 MEZ), also ~2h56min überfällig. Die behauptete dauerhafte Aufrufbereitschaft der Version 6.72.356 ist damit im realen Betrieb weiterhin nicht erfüllt.

**QA69: LIVE NICHT BESTANDEN.** Zwei offene Sachverhalte: (A) kein zuverlässiger Folgeaufruf nach completed; (B) 290 SAFE-Quellen durch source_state != available gesperrt, Status ended versus needs_review **nicht aufgeschlüsselt**. Weder eine pauschale Vollsuche noch das Aufheben der sicheren Quellenidentitätsprüfung ist gerechtfertigt. Vor Codeeingriff tatsächliche Verteilung der gespeicherten source_state-Werte und die pro Quelle abweichenden Identitätsfelder im bestehenden Bestand nachweisen. Keine neue Pluginversion oder Abnahme auf Verdacht.

**Präzisierung zur Reihenfolge:** Der letzte belegte GitHub-Run um 14:42 MEZ kann VOR der anschließenden QA90-Installation (vor dem 16:07-Uhr-Screenshot) stattgefunden haben. Es wäre deshalb falsch, allein aus diesem Run zu behaupten, die NEUE Version 6.72.356 habe bei 14:42 selbst den falschen `completed`-Status geliefert. Nach dem durch Screenshot belegten QA90-Stand wurde bis zum Diagnosezeitpunkt 19:32 MEZ kein erneuter GitHub-eBay-Run nachgewiesen. Die korrigierte `busy`-Antwort der neuen Version wurde im Live-Betrieb damit möglicherweise noch überhaupt nicht aufgerufen. Sicher belegt ist die ausgebliebene Auslösung, **nicht** ein erneuter fehlerhafter QA90-REST-Codepfad.


## Operative Wiederaufnahme und tatsächlich prüfbarer Quellenstatus – 16.11.2026, abends

**Bestehender GitHub-eBay-Arbeiter einmalig wieder angestoßen:** Die vorhandene erfolgreiche Job-ID 133318218314 wurde mit der autorisierten GitHub-Aktion zum erneuten Ausführen gebracht. GitHub bestätigte success=true. Anschließend zeigte die vorhandene Run-ID 43872846236, Versuch 2, status=in_progress; Job-ID 133526997030, Schritt Keep the active canonical eBay run moving ebenfalls in_progress. **Keine neue Workflowdatei, kein neuer Zeitgeber, kein neuer eBay-Suchauftrag durch diesen Eingriff.** Die tatsächliche Verarbeitung der 290 derzeit gesperrten Angebote ist damit noch nicht bestätigt.

**Original-QA90-Code (bereits ausgeliefert, keine Vermutung):**
- In ebay_public_availability_refresh_one() werden auch nach erfolgreichem eBay-getItem die gespeicherten Quellen bei Abweichung von Item-ID, Verkäufername, normalisiertem Titel, Bild-URL oder Zustandsangabe auf source_state=needs_review und fresh_until=now gesetzt. Der bestehende Frontend-Quellenfilter lässt das Produkt dann nicht mehr zu.
- Die unmittelbar dazugehörige SQL-Auswahl des unabhängigen ebay_public_availability_tick() fordert beim NÄCHSTEN Durchgang e.source_state='available'; damit **werden needs_review-Quellen ab jetzt ausgeschlossen**. Das ist ein direkt durch Quellcode bewiesener Wiederaufnahmewiderspruch, kein Live-Beweis für die genaue Aufschlüsselung der 290 source_not_available-Fälle.
- Die bisherige getrennte Ein-Klick-Diagnose meldet für alle source_state != available nur source_not_available. Sie liefert keine Summen pro tatsächlichem Quellstatus. Die Anzahl der 290, die needs_review bzw. truly ended sind, ist aus dem bestehenden Export **nicht exakt bestimmbar**.
- Eine pauschale Freigabe der 290 Produkte oder das Ignorieren aller Bild-/Titel-/Zustandsänderungen wäre **ein Bruch** von QA69 und den Sicherheitsregeln. Vor einer vollständigen Reparatur ist die tatsächliche Änderung und die berechtigte Folgeverarbeitung **im vorhandenen einzigen Entscheidungsweg** zu belegen. Kein neues allgemeines Ranking in der Refresh-Strecke.

**Grenze der operativen Wiederaufnahme:** Die GitHub-Ausführung kann das offene Zeitgeberproblem kurzfristig reaktivieren. Sie reaktiviert **nicht automatisch** source_state=needs_review-Produkte. Auch ein grüner GitHub-Job ist keine öffentliche Produktfreigabe.

**Aktueller Stand:** 309 SAFE-Kampagnen im letzten echten Abendexport; 290 source_not_available, 10 expired, neun mit bestandener Grundprüfung. Automatischer Arbeiter wieder in_progress. QA69-Live-Gesamtabnahme OFFEN, kein weiterer Plugin-Release aus der Diagnose behauptet.
