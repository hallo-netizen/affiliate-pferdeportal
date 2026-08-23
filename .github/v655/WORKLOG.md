# ARBEITSPROTOKOLL V6.55.0 – KISS Public Heartbeat + GitHub Scheduler

Stand: 23.08.2026

## Auftrag
Die in V6.54 noch offen gebliebene Abhängigkeit von einem zusätzlichen externen Cron-Anbieter vollständig beseitigen. Vorhandene GitHub-Infrastruktur verwenden. Kein neuer Account, kein hosterspezifischer Cron, kein Browser-Dauerlauf, kein WP-Cron-Self-Pump. Einzelne kandidatbezogene Fehler dürfen den Gesamtprozess weiterhin nicht stoppen; harte System-/Storage-/Checkpoint-/Invariantenfehler bleiben fail-closed. Jeder Schritt gegen den gesamten Workflow prüfen.

## Rootcause nach V6.54
V6.54 löste die technische Self-Pump-Abhängigkeit, verlangte operativ aber noch einen beliebigen externen HTTP-Cron-Dienst samt geheimer URL. Das widersprach dem KISS-Ziel des Projekts, weil für den Nutzer dadurch ein zusätzlicher externer Account nötig geworden wäre.

## KISS-Ziel V6.55
1. Der Heartbeat bleibt ein einzelner providerneutraler Transport in den bestehenden kanonischen eBay-Worker.
2. Der Heartbeat ist POST-only und enthält keinen Geheimschlüssel.
3. Der Heartbeat kann weder Provider noch Operation noch Konfiguration wählen; er darf ausschließlich bereits autorisierte, fällige kanonische Arbeit um höchstens ein Paket voranbringen.
4. Eine dauerhafte 45-Sekunden-Zulassungssperre begrenzt Wiederholungen vor jeder Facharbeit. Lease/CAS/Checkpoint bleiben zusätzlich maßgeblich.
5. Die bereits vorhandene GitHub-Infrastruktur übernimmt den Takt: GitHub-Schedule alle fünf Minuten, innerhalb eines Jobs fünf begrenzte POST-Ticks im Minutenabstand.
6. Kein zusätzlicher Cron-Anbieter und kein neuer Account.
7. Scheduler-Workflow wird separat vorbereitet. Der Default-Branch `main` wird ohne ausdrückliche Freigabe nicht verändert.

## Fehlervertrag
Kandidatbezogene BUSINESS-/PRIVATE-Fehler bleiben protokollierbar und überspringbar. Globale Creative-Library-, Storage-/Database-, Checkpoint-, Runtime-, CAS/Lease- und Invariantenfehler bleiben hart. Terminal fehlgeschlagene Runs werden durch den Heartbeat nicht automatisch neu gestartet.

## Produktionsscope
Exakt vier Affiliate-Dateien gegenüber final V6.54:
- `pferdeportal-affiliate-router.php`
- `includes/trait-ppar-ebay-run.php`
- `includes/trait-ppar-ebay.php`
- `readme.txt`

Designplugin: 0 Änderungen. V6.54-Produktkarten und unberührte Fachlogik werden regressionsgeprüft.

## Releaseprüfung
Bindung an finales V6.54-Actions-Artefakt `9492368681` samt SHA-/Installer-/MASTER-Belegen. Danach Pre-Fix-RED, atomarer Patch, 4-Dateien-Scope, PHP/JSON, 23 Architekturprüfungen, 55 unberührte Kernworkflow-Paritäten, V6.54-Produktregressionen, Scheduler-Vertrag, Real WordPress 7.0.1/PHP 8.4/MariaDB 11.4, realer GET/POST/Throttle-HTTP-Test, Fresh-Unpack und Wiederholung, Real WordPress aus finalem ZIP, WordPress 6.8.3, MASTER-Manifest und Source↔Fresh↔MASTER↔MASTER-Installer-Parität. Erst dann darf `FINAL_RELEASE_GATE=PASS` entstehen.

Der echte Pferde-Atelier-eBay-Provider-Endlauf bleibt bis Installation und aktivem GitHub-Scheduler `EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED`.
