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
