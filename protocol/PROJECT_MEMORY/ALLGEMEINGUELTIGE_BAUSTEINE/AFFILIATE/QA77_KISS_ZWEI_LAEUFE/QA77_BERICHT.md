# QA77 – Pferdeatelier eBay: KISS-Zwei-Läufe, lokale Originaldatenprüfung
Stand: 15.11.2026. **KEINE LIVE-FREIGABE, keine WordPress-Installation, kein neuer Worker, keine neuen Tabellen.**

## Tatsächlich gefundene Ursachen (Original-Quellstand QA76 / PHP 6.72.351)

1. Die große `sync`-Recherche ist fest auf **3 Stunden** programmiert (`sync_interval_hours` normalisiert auf 3 und externer Fälligkeitstest ebenfalls konstant 3h). Die `last_sync.finished_at`-Zeit wird bereits durch einen **untergeordneten** Discovery-Lauf geschrieben, bevor die vollständige öffentliche Kontrolle und Schlussbereinigung fertig ist. Nach einem späteren `refresh`-Lauf kann dies erneut verfrühte Suchläufe auslösen.
2. Der stündliche `refresh`-Kontrolllauf geht im unveränderten Originalcode nach `refresh_remote` in **`selection_prepare`**, `coverage_verify` und nötigenfalls `gapfill_discovery`. Damit wählt er erneut aus und sucht fehlende Produktfamilien, obwohl er bloß Verfügbarkeit prüfen sollte. **Dieser Ablaufbruch ist im Original-PHP belegt.**
3. `0/298` ist ein **fest eingebauter Anzeige-Text** bei noch unberechneter Abdeckung; der tatsächliche QA76-Katalog führt 283 Warenfamilien.

## Gebündelter KISS-Kandidat – nur lokal

Die lokale Variante verändert ausschließlich die beiden bestehenden Dateien `includes/trait-ppar-ebay-run.php` und `includes/trait-ppar-ebay.php`:

- `refresh`: startet direkt in `refresh_remote`; nach dem bestehenden Anbieter-Update sofort `completed`. **Keine zweite Fachauswahl, kein erneuter 283er Suchlauf, kein neuer Public-Checkpoint.** Einzelne GetItem-Fehler werden als Warnung ausgewiesen; bisheriger SAFE-Bestand bleibt unverändert und die vorhandene Frischeprüfung der Anzeige gilt weiterhin.
- `sync`: behält genau die bestehende Fachauswahl, Freigabe und Schlussbereinigung. Der Abstand wird in demselben vorhandenen normalisierten Einstellungsfeld auf **168h/7 Tage** gesetzt; Fälligkeit nutzt diesen einen Wert. `last_sync.finished_at` bzw. `last_refresh.finished_at` wird erst bei dauerhaft gespeichertem Gesamtabschluss auf dessen echte Schlusszeit gesetzt.
- Bei noch unberechneter Abdeckung wird statt festem `0/298` die dynamische Pflichtfamilienzahl und „noch nicht berechnet“ gezeigt.
- K0, andere Partner, Pluginarchitektur, Produkt-Ranking, Kapazitätsgrenze, öffentliche SAFE- und Frische-Gates sowie GitHub-Workflow sind **nicht verändert**.

## Lokal belegte RED/GREEN-Ergebnisse

| Echter Original-PHP-Funktionstest (mit modellierten WP/eBay-Antworten) | QA76-Ausgang | QA77-Kandidat |
|---|---:|---:|
| Fälligkeit / nur ein Zeitgeber / Zeit erst ab Gesamtabschluss | **9/12** | **12/12** |
| Verfügbarkeitslauf ohne zweite Produktauswahl, SAFE-Bestand erhalten, Anbieterfehler gekennzeichnet | **3/11** | **11/11** |

Zusätzlich: **95/95** echte historische Artikel-IDs mit **explizit simulierten** GetItem-/Datenbankantworten, **9/9** ausgewählte Sechs-Stunden-Frischefälle, **16** tatsächliche REST-PHP-Fälle, **8** vollständige Hauptlauf-Szenarien mit simulierten Provider-/WP-Daten (inklusive sicherer Fehlerstopps). **26.967 lokale Assertions ohne Abweichung**, davon der Großteil chronologische Einzelzeilenkontrolle, nicht unterschiedliche Produkttests.

**Echte Originaleingaben**: frühe 2.811 und späte 3.832 Ereignisse derselben alten Run-ID, neuer 87-Ereignis-Run, ursprüngliche 278 Fehlfamilien, originale 283er-Katalog-IDs, 95 echte individuell benannte der 153 Materialisierungsfehler. Das 283-Regalbuch trennt **historisch**: 5 gemeldet abgedeckt, 32 mit angenommenen Angeboten aber ohne Abdeckung, 31 ohne angenommene Angebote, 215 damals ohne eigenen Einzelabruf. Eine **heutige öffentliche** Abdeckung lässt sich aus diesen Dateien nicht beweisen.

## Offene harte Abnahmegrenze

Der Live-WordPress-Pluginstand ist weiterhin **unbestätigt**. Im Audit fehlen die tatsächlichen vollständigen WordPress-Quell-/Ausgabe-/SAFE-Daten und zugehörigen echten eBay-GetItem-Antworten. Auch der vom GitHub-Runner am 15.11. um 15:31:54 Uhr gemeldete technische `completed`-Abschluss enthält keinen vollständigen realen 283er SAFE-Anzeigenbeweis. **KEIN INSTALLATIONSPAKET und keine Live-Abnahme**, bis der bestehende Zielvertrag QA69 auf realen Live-/Testdaten erfüllt ist.

Wichtig: Die periodische Produktsuche wäre nach KISS-Kandidat **wöchentlich**, nicht nach jeder Verfügbarkeitskontrolle. Verlorene Produkte bleiben unsichtbar, bis die nächste echte Suche passenden Ersatz findet. Keine erfundene vorgezogene Ersatzsuchautomatik.
