# QA91 – eBay-KISS: erneute Prüfung bereits gesperrter SAFE-Quellen, 16.11.2026

## Echte Ursache im ausgelieferten QA90-Original und Gegenprobe

Die am 16.11., 19:32 MEZ gelieferte **echte** WordPress-Diagnose umfasst 309 SAFE-Freigaben: 290 mit Diagnose 'source_not_available', 10 abgelaufene Gültigkeiten, 9 Grundprüfung bestanden. Die Diagnose gruppiert alle source_state != available in EINEN Topf; die Rohverteilung 'needs_review' vs 'ended' ist **nicht** bekannt. Keine Behauptung, dass alle 290 'needs_review' sind.

**Zwingender Programmfehler aus vollständig vorliegender Original-6.72.356:**
- ebay_public_availability_refresh_one() markiert eine Quelle mit getItem-Datenabweichung als source_state='needs_review' und fresh_until=now. Damit bleibt sie aus Sicherheitsgründen zu Recht vorübergehend unsichtbar.
- Der unmittelbar nächste getItem-Verfügbarkeitslauf ebay_public_availability_tick() nimmt aber per SQL ausschließlich e.source_state='available' in seine Quellenliste auf. Die zuvor zur Nachprüfung gesperrte Quelle kann im selben unabhängigen Lauf NIE wieder zur Verfügung gestellt werden, selbst wenn eBay bei der nächsten Abfrage die alte, verifizierte Identität zurückliefert.
- Rote Original-PHP-Gegenprobe QA90: Der Handler erhält für needs_review 0 Datensätze und führt 0 Anbieterprüfungen aus. Grüne Gegenprobe QA91: die ursprüngliche Funktion prüft genau einmal erneut und setzt ausschließlich bei nachgewiesener unveränderter Artikel-ID, Verkäufername, normalisiertem Titel, Bild-URL und Zustandsangabe auf available. Bei tatsächlich geänderter Identität bleibt sie needs_review/unsichtbar.

## Eine einzige sichere Korrektur der bereits bestehenden Quellenabfrage

Ausgangs-ZIP: QA90 6.72.356, SHA256 07514e89a721de5a96bd070d83917495352df3b358a86ca62838694052dacdac.

In EINER vorhandenen SQL-Zeile nur den Quellenstatus von e.source_state='available' zu e.source_state IN ('available','needs_review') erweitert. Unverändert: ebay_public_availability_refresh_one (einschließlich der strengen Quellidentitäts- und Sperrprüfung), Pflichtzielkatalog, Produkt-/Rankingentscheidung, eigener Availability-Cursor, GitHub-Wecker, Update- und SAFE-Checkpoint-Logik, Frischegrenze, Webhoster, Suchintervalle, K0 und sämtliche anderen Partner. Nur Hauptversionsnummer und Readme zusätzlich geändert; von 66 Archivdateien sind genau 3 verschieden.

**Wichtig:** Die Maßnahme ist KEINE pauschale Wiederfreigabe der 290 Produkte. Tatsächlich veränderte Angebotsidentität bleibt sicher gesperrt und wird nur durch den zuständigen Auswahlablauf neu entschieden. Ob Bild-/Titelunterschiede die derzeitigen 290 Sperren verursacht haben, kann der alte Datenexport nicht belegen.

## Harte Tests direkt auf den echten Original-PHP-Traits, ohne echte Anbieterabfragen

- QA90 echte Verfügbarkeitsfunktion bei needs_review: Gegenprobe FAIL, kein erneuter getItem-Aufruf; QA91: 10/10 direkter PHP-Quellenidentitäts-Tests PASS, einschließlich 'gleiche Identität -> frei', 'veränderte Identität -> gesperrt'.
- Originales 309er-SAFE-Modell mit 290 needs_review-Testquellen, 496 historischen veröffentlichten Ausgaben, 9.792 historischen Quellzeilen: 309/309 gespeicherte Quellen in derselben bisherigen Workerkette verarbeitet, 0 Quellen außerhalb SAFE, 0 neue Produktsuche; ursprüngliche SAFE-Mitgliedschaft und Recherche-UUID erhalten.
- Unveränderte bestehende 309er-SAFE-Regressionsprobe ebenfalls PASS; 19/19 ursprüngliche QA90-Heartbeat/Leerlauf-Testfälle; 15/15 QA89-Statusfälle; neun vollständige QA89-Controller-Szenarien: fünf kontrollierte Erfolge und vier erwartete Daten-/Commitfehler; 23 PHP-Dateien im frisch entpackten Plugin syntaktisch gültig.
- Archiv 66/66 Dateien gelesen, CRC ohne Fehler und frisch entpackte Daten bytegleich mit dem geprüften Verzeichnis.
- Im 309er-Modell sind Anbieterantworten simuliert, bei den echten 290 Quellen **nicht** abgefragt; **das beweist NICHT, dass alle 290 im echten Portal wieder sichtbar werden.**

## Echtes Betriebsereignis – nicht als Live-Fertigstellung ausgeben

Die bereits bestehende GitHub-eBay-Heartbeat-Job-ID 133318218314 wurde über den regulären, autorisierten GitHub-App-Aufruf **einmal erneut gestartet**, kein neues Workflowfile, kein neuer Worker. GitHub bestätigte Erfolg und anschließend Run 43872846236 Versuch 2, Job 133526997030 status=in_progress. Es wurde **kein neuer Katalogsync angeordnet**. Dieser wiederhergestellte Zeitgeber kann mit der derzeit installierten QA90-Version die needs_review-Quellen aber noch nicht im vorhandenen SQL auswählen.

## Paket und harte Grenzen

Vollständiger installierbarer **TESTKANDIDAT**, NICHT als QA69-Live-Erfolg freigegeben:
QA91_PFERDEATELIER_AFFILIATE_ZENTRALE_6.72.357_QUELLEN_RECHECK_NUR_TEST.zip
SHA256 82d6567fd009bfecef0cd4e817df8a7214ba08e5d4adbcca46dde6beba32c5a6.
Private Pluginbüro-Ablage: /pferdeatelier/PLUGINS/QA/QA91_QUELLEN_RECHECK_GESAMT/. Hier liegen außerdem Quellidentität-Gegenprobe, 309er-Gesamttest und Prüfprotokoll.

**Zum echten Abschluss:** Einmalige Sicherung und Update der bestehenden Affiliate-Zentrale (kein zusätzliches Plugin), ohne Suche/Reset; dann echte Anzahl geänderter Quellen vs tatsächlich wieder bestätigte identische eBay-Artikel, periodischer Takt und öffentlich sichtbare Karten im selben unveränderten SAFE-Bestand. Ohne diese echte Provider-/Frontend-Prüfung QA69 NICHT BESTANDEN.

**Keine neuen Behauptungen:** GitHub-Wecker selbst kann trotz neuem Worker in Zukunft ausfallen. Der aktuelle Stand ist eine korrekt wieder gestartete bestehende Uhr und ein geprüfter Quell-Pfadfix, keine garantierte dauerhafte Serviceverfügbarkeit.