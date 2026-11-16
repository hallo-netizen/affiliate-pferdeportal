# QA83 – eBay Pferdeatelier: geprüfter Live-Stand am 16.11.2026

**Prüfumfang:** bestehende GitHub-Arbeitsläufe, bestehende QA69–QA82-Berichte, öffentlich lesbare Schabracken-Kategorieseite. **Kein Plugin geändert, kein WordPress-/eBay-Schreibzugriff, keine neue Suchabfrage ausgelöst.**

## 1. Verifizierte Fakten
- QA82-Bericht und `QA81_to_QA82_RUN.patch` sind unter `QA82_GESAMTSIMULATION_ORIGINAL_283/` auf dem Zweig `affiliate-release-current` vorhanden. QA82 ist eine lokale Korrektur/Simulation, **kein installiertes Live-Release**. 26.967/26.967 lokale Assertions; nicht mit Live-Veröffentlichungen verwechseln.
- **Echter GitHub-Arbeiter:** Main-Workflow-Run [43834993089](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43834993089), Job 133189310848, 16.11.2026 08:53–08:55 UTC. Heartbeat 1: `throttled`. Heartbeat 2 um 08:55:13 UTC (= 09:55:13 MEZ): `status=completed`; danach `terminal heartbeat status=completed; no successor runner required`. GitHub-Job `success`. Die beiden Vorgänger 43830255203 und 43826067954 hatten 30 Schritte mit fortgesetzter Verkettung. **Das beweist einen terminalen REST-Status und die beendete Worker-Kette, nicht den sicheren öffentlichen Endbestand für 283 Familien.**
- **Öffentliche Seite:** [Schabracken](https://pferde-atelier.de/ausruestung/ausruestung-sattel/schabracken/), am 16.11.2026 im lesbaren Seitentext geprüft. Die Abschnitte „Ausgewählter Partner“ und „Produktvorschläge“ erscheinen, aber keine zugehörigen eBay-Produktlinks oder Produktkarten im ausgelesenen Inhalt. Das ist nur ein Einzelseitenbefund, keine 283er-Abdeckungsmessung; dynamische Anzeige wird damit nicht widerlegt.
- **Originalaudit:** QA66/QA69 dokumentieren historischen Zwischenstand `5/283`, `278` offene Familien, `153` nicht materialisierte ausgewählte Angebote. Diese Zahlen stammen aus früheren Originalexports; sie sind **keine aktuelle Live-Abdeckung**. Die 278 Lücken bedeuten nicht automatisch fehlendes eBay-Marktangebot.
- QA70 dokumentiert zwar die Entwicklung eines **einmaligen nur lesenden Echtdatenexports** in Testversion 6.72.349, aber **keine bestätigte Installation** und **keine hier verfügbare vollständige aktuelle NDJSON-Momentaufnahme**. QA81/QA82 dokumentieren ebenfalls nur lokale Änderungen.

## 2. Verbindlicher Stand gegen QA69
**NICHT LIVE ABGENOMMEN**. GitHub-Transport/Beendigung für obigen Lauf sind real nachgewiesen; weiterhin offen ist der zusammenhängende Nachweis vom selben WordPress-Lauf über gespeicherte eBay-Quellen, Fachauswahl, SAFE-Checkpoint, Creatives und veröffentlichte Zielseiten bis zu 283 einzelnen Ergebnissen. Weder neues lokales Simulieren noch eine weitere Vollsuche kann die fehlenden Originaldaten ersetzen.

## 3. EIN nächster Betriebsschritt
Den tatsächlichen WordPress-Bestand **einmalig nur lesend** aus der vorhandenen zentralen eBay-Exportfunktion erfassen (falls auf der installierten Version vorhanden; die Version ist noch unbekannt). Je Familie: gespeicherter bestätigter Artikel, aktueller Quellen-/Frischestatus, veröffentlichte Kampagne, SAFE-Zuordnung, Zielseite oder fachlich belegter Nichtverfügbarkeitsgrund. Den als `completed` gemeldeten Lauf mit Run-ID und öffentlichem Stand abgleichen. **Keine neue eBay-Vollsuche, keine dritte Entscheidung, keine separate Diagnose-Engine.**

**Sicherheitsregel:** Weder die lokale QA82-Funktion noch die eBay-Cron-Umstellung ohne die echte Bestands-/Frischeverteilung als Live-Freigabe deklarieren. GitHub-PR-Hardlock nicht verändern.


## 4. Ergänzende harte Quellenprüfung (Fortsetzung am selben Tag)
**Echte öffentliche Seite:** https://pferde-atelier.de/ausruestung/ausruestung-sattel/schabracken/ wurde direkt erneut geöffnet; die live abgerufene Textausgabe enthält bei den Produktabschnitten auf den Zeilen 812–825 ausschließlich „Ausgewählter Partner“ / „Marken und Angebote ...“ und „Produktvorschläge“ / „Empfehlungen ...“, ohne Produktnamen, eBay-Links oder Karten. Dies ist der Nachweis für die *lesbare Ausgabe dieser konkreten Seite*, nicht für dynamisches Rendering oder alle Familien.

**Tatsächlicher GitHub-Arbeiter:** Job 133189310848, zu Run 43834993089. Aus dem echten Job-Log: `heartbeat 1 status=throttled` (08:54:06 UTC), `heartbeat 2 status=completed` (08:55:13 UTC), unmittelbar danach `terminal heartbeat status=completed; no successor runner required`. Der Job hat **keine Ergebnisartefakte** hochgeladen. Die Response-Zeile `completed` enthält im GitHub-Log keine Familie-zu-Angebot-Liste; die Quellzuordnung der 283 Familien kann aus diesem Log nicht nachträglich abgeleitet werden.

**Quellstand und Unterschiede ausdrücklich verglichen:**
- Die momentan im GitHub-Büro unter `release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php` gespeicherte **Release-Quellkopie** trägt `Version: 6.72.211` (Zeile 5, Konstante Zeile 121).
- Ihre `includes/trait-ppar-ebay-run.php` enthält in `ebay_external_tick_due_operation` (Zeilen 681–692) **`3 * HOUR_IN_SECONDS`** als Wieder-Suchfrist und nur `last_sync.finished_at`; also **nicht** die QA82-Logik mit 7 Tagen und getrennter letzter Such-/Publikationszeit.
- Der Originalcode dieser gespeicherten Release-Quellkopie schließt den kanonischen Lauf in `ebay_run_complete` (Zeilen 947–959) mittels `run.status='completed'` ab; in `ebay_run_tick_public_verify` (Zeilen 1670–1726) wird die Freigabe separat bearbeitet. `completed` allein ist daher kein Ersatz für die konkreten Ergebnisdaten.
- Der **spätere QA82-Quelländerungsstand** liegt im Projekt derzeit dokumentiert als `QA81_to_QA82_RUN.patch` plus Bericht vor, jedoch **nicht** als aktualisierter vollständiger freigegebener Release-Quellbaum am genannten `release/affiliate-zentrale/current`-Pfad.
- **Wichtig:** Aus dem GitHub-Release-Quellbaum folgt NICHT die tatsächlich installierte WordPress-Version. Die öffentliche Website gibt die interne Plugin-Versionsnummer nicht in dem hier geprüften Seiteninhalt preis. Version live bleibt unbewiesen. Der QA82-Diff darf darum **nicht blind** auf diesen älteren GitHub-Release-Quellstand angewendet werden.

**Prüfurteil und KISS-Vorgehen:** Transport/Beendigung nachweisbar. Öffentliche vollständige Angebotsabdeckung nicht nachweisbar, konkrete Schabracken-Seite auslesbar ohne Produkte. Für die Freigabe exakt **eine** bereits vorhandene verbindliche Ergebnisliste aus demselben abgeschlossenen WordPress-Lauf verwenden; keinen neuen fachlichen Prüfer und keinen neuen eBay-Gesamtlauf hinzufügen. Keine Entscheidung auf Grundlage eines grünen GitHub-Jobs oder allein der älteren Release-Quellkopie.
