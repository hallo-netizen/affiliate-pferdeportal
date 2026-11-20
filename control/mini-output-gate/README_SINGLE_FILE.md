# MINI – ein Export, eine externe Freigabe, eine Importdatei

## Verbindlicher Auftrag

Ein WordPress-MINI-Gesamtexport wird unverändert gebunden. Die vorhandenen Worker bearbeiten jeweils ausschließlich ihre Stufe: CATEGORY, EDITORIAL, TITLE. Bereits fertig entschiedene Stufen bleiben gesperrt. Bei Fehlern benennt REPARATUR.json nur die fehlende oder fehlerhafte Stufe. Der zuständige Worker repariert ausschließlich diese Stufe, die unveränderte Quelle und andere gültige Entscheidungen bleiben erhalten.

**Ausgabe ausschließlich nach der einen bestehenden technischen Abschlussprüfung** (`mini_release_gate.py`). Das neue `mini_single_release.py` ruft sie in einem isolierten Arbeitsordner auf und erstellt ausschließlich bei PASS eine einzige komprimierte Reimport-JSON in `FREIGABE/MINI_EINMAL_REIMPORT.json`, plus einen separaten Prüfbeleg. Es verteilt NIE CATEGORY/EDITORIAL/TITLE an Benutzer.

Bei jedem Fehler wird eine zuvor freigegebene Importdatei gelöscht. Der Befund ist `REPARATUR`, keine Erfolgsbehauptung. Auch bei einer wiederholten Freigabe entsteht nur eine Datei.

## K0 bleibt unberührt

Kein K0-Code wird verändert. Keine neue Recherche, keine neu erfundene Fachentscheidung, kein nachgelagerter Titelentscheid, keine WordPress-Fachprüfung.

## Ausführung in der vertrauenswürdigen Auslieferungsumgebung

1. Übergib den ursprünglichen WordPress-Export als `ORIGINAL_MINI.json` und die SHA256 der Originalbytes als `ORIGINAL_SHA256.txt` an einen **privaten** Workspace.
2. Die vorhandenen Worker schreiben nur die offenen Dateien `CATEGORY.json`, `EDITORIAL.json`, `TITLE.json` (ohne Wiederholungen alter Entscheidungen).
3. Einziger ausliefernder Befehl: `python mini_single_release.py --workspace /pfad/zum/privaten/mini-arbeitsraum`.
4. Ist das Ergebnis `REPARATUR`, wird der betreffende Worker erneut aufgerufen. Ohne PASS existiert keine Importdatei.
5. Bei PASS wird **nur** `FREIGABE/MINI_EINMAL_REIMPORT.json` verteilt; der separate `NACHWEIS.json` ist ein interner Prüfnachweis.

## Technische Grenzen – nicht als erledigt behaupten

- **WordPress 0.4.38 kann diesen neuen einzelnen Dateivertrag noch nicht importieren.** Das WordPress-Plugin benötigt hierfür eine reine Einmal-Importaufnahme; bisherige Mini-Worker-Entscheidungen dürfen nicht fachlich nachgeprüft oder doppelt entschieden werden.
- Ein GitHub-Repositorieskript kann **nicht** die ChatGPT-Ausgabe beliebiger lokaler Dateien technisch verbieten. Eine nicht umgehbare Zustellung erfordert, dass die Dateien ausschließlich von einem vertrauenswürdigen externen Auslieferungsdienst (z. B. einem privaten GitHub Actions-Lauf) ausgegeben werden und der Benutzer keine beliebigen Chat-Dateien als MINI-Import verwendet. Hier wurde der Produktionsdienst noch nicht aktiviert.
- Das bestehende Repo `hallo-netizen/affiliate-pferdeportal` ist öffentlich. WordPress-Exportdaten daher niemals dort committen oder als öffentliche Actions-Artefakte speichern. GitHub enthält nur den ausführbaren Prüfcode und anonymisierte Tests.
- Erst eine getestete *gesamte* Kette einschließlich echter WordPress-Einmalaufnahme würde den Zielvertrag nachweisbar erfüllen. Ein lokaler `PASS` ist kein Live-Importbeweis.

## Tests

`python -m unittest -v test_mini_single_release.py test_mini_gate.py`

Zusätzlich wurde der konkrete gespeicherte 10-Themen-Export (4) geprüft: Der Freigabedienst meldete `REPARATUR` für 9 noch offene Redaktionsentscheidungen; keine Datei wurde ausgegeben. (Ein Thema ist bereits in die Redaktion geroutet.)