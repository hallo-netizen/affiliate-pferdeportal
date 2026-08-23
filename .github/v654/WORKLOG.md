# ARBEITSPROTOKOLL V6.54.0 – KISS External Tick + Skip

Stand: 23.08.2026

## Auftrag

Den eBay-Gesamtworkflow nach dem realen V6.52-Live-Fail grundsätzlich vereinfachen. Kein weiterer WP-Cron-/Self-Pump-Minifix. Der Lauf muss browser- und hostingpaketunabhängig fortsetzbar sein. Ein kandidatbezogener Einzelfehler darf den Gesamtlauf nicht stoppen; er wird protokolliert und übersprungen. System-, Speicher-, Checkpoint- und Invariantenfehler bleiben fail-closed. Jeder Schritt wird gegen den vollständigen Workflow geprüft.

## Nachgewiesener Ausgangsfehler

Der reale V6.52-Lauf auf Pferde Atelier blieb trotz lokal grüner Self-Pump-Tests bei `reconcile_local`, `letzter Worker-Tick —`, `Pakete 0`. Ein angenommener nicht-blockierender Cron-/Loopback-Dispatch war kein belastbarer Beweis, dass auf dem Zielhosting tatsächlich ein Worker gestartet wurde. Damit war Hostingverhalten Teil der Korrektheit.

## KISS-Zielarchitektur

1. Genau ein fachlicher kanonischer eBay-Worker bleibt bestehen.
2. Ein provider-neutraler, geheimnisgeschützter REST-Endpunkt `/wp-json/affiliate-zentrale/v1/ebay/tick` ist der einzige Transport für kanonische eBay-Arbeit.
3. Ein HTTP-Aufruf führt höchstens einen kanonischen Paket-Tick aus und beendet sich.
4. Ein beliebiger externer HTTP-Taktgeber kann den Endpunkt einmal pro Minute aufrufen. Kein Browser, kein WP-Cron, kein plugin-eigener Self-HTTP und kein Server-Cron sind Laufvoraussetzung.
5. Ist kein Run aktiv, startet der Tick bei Fälligkeit automatisch den regulären 3h-Sync beziehungsweise den stündlichen Inventory-Refresh. Ist ein Run terminal fehlgeschlagen, startet der externe Tick ihn ausdrücklich nicht automatisch neu.
6. Lease/CAS, sichere öffentliche Checkpoints, Restart-/Build-Schutz, No-Progress, Coverage, Gap-Fill und Public-Verify bleiben die fachliche/sicherheitstechnische Autorität.

## Einzelfehler-Vertrag

- BUSINESS: kandidatbezogene Source-/Klassifikations-/Quality-/Import-/Materialisierungsfehler werden aus der aktiven Auswahl entfernt, dauerhaft als `skipped_item_errors` protokolliert und Coverage/Gap-Fill darf einen Ersatz suchen.
- PRIVATE: bereits paketweise weiterlaufende kandidatbezogene Fehler werden ebenfalls in den kanonischen Skip-Audit übernommen.
- Globale Creative-Library-, Storage-/Database-, Checkpoint-, Runtime- und Invariantenfehler bleiben hart und terminal.
- Abschluss mit übersprungenen Einzelfehlern wird als `completed_with_skips=1` sichtbar; der sichere öffentliche Bestand bleibt weiterhin durch die unveränderten Public-/Checkpoint-Gates geschützt.

## Produktionsscope V6.53 -> V6.54

Exakt vier Dateien im Affiliate-Plugin:
1. `pferdeportal-affiliate-router.php`
2. `includes/trait-ppar-ebay-run.php`
3. `includes/trait-ppar-ebay.php`
4. `readme.txt`

Designplugin: 0 Änderungen. Artikel-Produktkarten aus V6.53 bleiben geschützt und werden separat regressionsgeprüft.

## Gesamtworkflow-Prüfung

Der Release-Gate bindet bytegenau an das final automatisch verifizierte V6.53-Actions-Artefakt `9491717325` und dessen Installer-/MASTER-Hashes. Danach: V6.53-RED-Gegenbeweis; atomarer 4-Dateien-Patch; PHP/JSON; KISS-Architekturtest; exakte Parität für 55 unberührte Kernfunktionen (Checkpoint, Lease/CAS, Phasenticks, Coverage, Gap-Fill, Public Verify, Acceptance, Klassifikation, Provider-/Refresh-Verarbeitung); V6.53-Produktkarten-Regressionsschutz; Real WordPress 7.0.1/PHP 8.4/MariaDB 11.4 inkl. REST/Auth/Due/Build-Change/Checkpoint/Cron-Retirement/Skip-Audit/hard-vs-soft/ein Tick/Failed-No-Autorestart; reale HTTP-Abfrage des REST-Endpunkts; Fresh-Unpack und Wiederholung; Real WordPress aus finalem ZIP; WordPress 6.8.3; MASTER-Manifest und Source↔Fresh↔MASTER↔MASTER-Installer-Parität. Erst danach darf `FINAL_RELEASE_GATE=PASS` entstehen.

Der echte produktive eBay-Provider-Endlauf auf Pferde Atelier bleibt bis nach Installation ausdrücklich `EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED`.

## CI-Lauf 1 – HTTP-Testfixture getrennt

Der erste V6.54-Gesamtlauf erreichte erfolgreich den atomaren Produktionsscope, 31/31 Architekturprüfungen, 55/55 Kernworkflow-Parität, die vollständigen V6.53-Produktregressionen und sämtliche in-process Real-WordPress-Prüfungen. Der anschließende zweite PHP-Prozess des echten HTTP-REST-Tests sah jedoch eine deaktivierte Testkonfiguration (`status=disabled`). Das wurde nicht als PASS übergangen.

Die erste Testkorrektur trennte die Assertion-Zähler sauber über `$GLOBALS` und setzte vor dem separaten HTTP-Prozess einen eigenen Fixture-Zustand. Produktionspatch unverändert.

## CI-Lauf 6 – HTTP-Bootstrap-Normalisierung korrekt erkannt

Der vollständige Lauf erreichte erneut 31/31 Architektur, 55/55 Kernworkflow-Parität, alle Produktregressionen und 37/37 Real-WordPress-Assertions. Er stoppte danach noch vor dem HTTP-Aufruf, weil die Testinfrastruktur verlangte, dass ein künstlich auf `enabled=true` gesetzter eBay-Zustand auch nach einem frischen HTTP-Bootstrap bytegleich `enabled=true` bleibt.

Die gespeicherte Testoption wurde beim frischen WordPress-/Plugin-Bootstrap zulässigerweise auf den realen providerfähigen Zustand normalisiert und ohne Credentials wieder deaktiviert. Das ist kein Produktionsfehler. Die Due-/Autostart-Logik ist bereits im selben echten WordPress mit deterministischem Zustand geprüft; der separate HTTP-Prozess soll ausschließlich beweisen, dass der reale REST-Endpunkt erreichbar ist, einen falschen Schlüssel mit HTTP 403 ablehnt und den korrekten Schlüssel mit HTTP 200 sowie gültigem JSON-Status akzeptiert.

Korrektur ausschließlich in der Prüfinfrastruktur: keine künstliche `enabled=true`-Persistenzannahme über Prozessgrenzen mehr; HTTP-Server-Readiness wird explizit geprüft; falscher Schlüssel muss 403 liefern; korrekter Schlüssel muss 200 und gültiges JSON mit `status` liefern. Produktionspatch bleibt bytegleich. Danach wird der komplette Releaseworkflow erneut von null ausgeführt.

## Gesamtworkflow-Nachprüfung nach erstem FINAL-PASS – widersprüchliche Alt-Dokumentation

Nach dem ersten automatisch grünen V6.54-Endlauf wurde das erzeugte Release-Artefakt zusätzlich als Ganzes gegen den aktuellen Betriebsvertrag gelesen. Dabei blieb im `readme.txt` ein historischer Abschnitt aus einem älteren Browser-/Admin-AJAX-Betriebsmodus erhalten, der ausdrücklich behauptete, Browser-Unabhängigkeit sei nicht erfüllt. Das widerspricht der V6.54-Zielarchitektur und dürfte in einer bindenden MASTER nicht stehen bleiben, obwohl Runtime, Tests und neuer 6.54-Abschnitt korrekt waren.

Die Releasefreigabe wurde deshalb nicht an den Nutzer ausgegeben. Innerhalb des bereits vorhandenen 4-Dateien-Produktionsscopes wird ausschließlich dieser veraltete `readme.txt`-Abschnitt durch den aktuellen externen REST-Taktgeber-Vertrag ersetzt. Zusätzlich prüft die Releasepipeline Source und Fresh-Unpack negativ auf den alten Browser-Text und positiv auf den aktuellen Vertrag; die Korrektur wird als eigener Patch in der MASTER protokolliert und `README_CURRENT_TRANSPORT=PASS` wird Bestandteil der finalen Entscheidung.

Runtime-/Worker-/Providerlogik bleibt hierbei bytegleich. Anschließend läuft der vollständige V6.54-Releaseworkflow erneut von null; erst dessen automatisches `FINAL_RELEASE_GATE=PASS` ist freigabefähig.
