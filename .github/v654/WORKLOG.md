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
