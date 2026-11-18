# Hab & Bewahr – Texterstellung 0.4.31.3 – komplette Originaleinrichtung

**Datum:** 18.11.2026. **Installationspaket:** `Texterstellung_HAB_UND_BEWAHR_0.4.31.3_VOLLSTAENDIGE_EINRICHTUNG.zip`.

## Nachgewiesener Screenshot-Blocker
- Hab 0.4.31.2 war installiert. Der Screenshot zeigte `PLUGIN_ACTIVATED_MANUAL_START_REQUIRED` und eine unvollständige Original-PSTE-Migration, aber keinen nutzbaren Einrichtungsbutton. Die Version `0.4.31 KISS` war fest in die Adminüberschrift kodiert, nicht der Header der tatsächlich installierten 0.4.31.2.
- Im Code lag die vollständige Originalklasse `PSTE_Safe_Migration_Job::start/advance`, aber kein Admin-Aufruf. Die ursprüngliche Migration und ihre gespeicherten Prüfschritte waren folglich in der Hab-Kopie nicht erreichbar. Zudem war die ursprüngliche PSTE-Recherche-Einstellung standardmäßig `feature_enabled=false`, ohne Bedienmöglichkeit in Hab.

## Exakte Umsetzung ohne neue Architektur
- Grundlage ausschließlich die zuvor gespeicherte Hab-Originalkopie 0.4.31.2. **2 vorhandene Dateien geändert:** `texterstellung.php` und `README-TESTINSTALLATION.txt`; **85/87 unverändert, keine neue Datei oder Klasse**.
- Auf der bestehenden Rechercheseite ein einziger Button `Einrichtung vollständig durchführen`. Er ruft nach Admin- und Nonce-Prüfung den VORHANDENEN Originaljob auf und bearbeitet genau einen ursprünglichen Migrationscheckpoint je Anfrage. Nach Unterbrechung wird derselbe persistierte Originaljob fortgesetzt. Kostenpflichtige API-Aufrufe und WordPress-Beitrags-/Kategorienänderungen sind davon unabhängig und werden nicht ausgelöst.
- Eine fehlende originale PSTE-Grundlage wird im bestehenden System an der Originalphase `EDITORIAL_INIT` einmalig anhand der **vorhandenen** gebundenen WordPress-Kategorien erzeugt; vorhandene Grundlagen werden nicht überschrieben; fehlerhafte Altbestände bleiben gesperrt. Kein neues Kategorienmodell, keine zweiten Fachentscheidungen.
- Die bereits EXISTIERENDE Einstellung `feature_enabled` kann nach Einrichtung über einen einmaligen UI-Klick gesetzt werden. Sie startet niemals eine bezahlte Anfrage; die ursprüngliche gesonderte Kostenbestätigung bleibt zwingend.
- Versionsanzeige aktualisiert. Die irreführende rote Recherchestopp-Meldung bei absichtlich noch nicht gestartetem Neuinstallationsjob ist als neutraler Hinweis dargestellt.
- Kein Eingriff in Original-PSTE-Dateien, das Kategoriesystem von Hab, MINI, K0, DataForSEO-Filter, den Entwurfsimport, Pferdeatelier oder die Universal-Blankokopie.

## Tatsächliche Prüfung
- `78/78 PHP` Syntax, `8/8 JSON`, ZIP CRC `87/87 PASS`.
- WordPress-PHP-Mocks mit ECHTEM originalen `PSTE_Safe_Migration_Job`: Erststart dauerhaft gespeichert, wiederholtes Starten idempotent, ein Original-`PREPARE`-Schritt ausgeführt, Status lesen, Admin- und Nonce-Schutz, falsche Jobkennung verweigert, vorhandene fehlerhafte Grundlage nicht überschrieben, fehlende Grundlage aus bekannten Hab-Term-/R3-Mocks erzeugt, echtes EDITORIAL_INIT vorab abgesichert. Ohne externe HTTP-/DataForSEO-Anfragen.
- Originale Kategoriezuordnung mit echten Hab-Beispielnamen: gültig / inaktiv / fehlende R3-Seite; fünf Rechercheabsichten auf dieselbe echte WordPress-Kategorie. Synthetischer 285/93 Mengentest ohne Quarantäne; originaler MINI-Prüfer mit allen fünf unterstützten Typen und zwei Negativfällen.
- Die reale WordPress-Migration und K0-Annahme sind nicht aus dieser Sitzung extern ausgeführt worden; NICHT als live bestätigt behaupten.

## Belegbarer Datei- und Archivstand
- ZIP SHA256: `a86a9dafbaf7e6604dd1217c428098ec54387d2763165bff47ce41a606a8bafd`, **516355 Byte**.
- Die installierbare ZIP, kompletter Quelldateibestand in der ZIP, Bau-/Diff-Skript, die ausgeführten PHP-Tests, JSON-Testergebnisse und ein umfangreiches Arbeitsprotokoll sind **tatsächlich mit Status `succeeded` im Hab-Büro** archiviert:
  `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEN/04313/`.

## Einziger Nutzerweg
1. In Hab-WordPress die bestehende Texterstellung mit dem 0.4.31.3 ZIP **ersetzen** (nicht löschen).
2. Unter Texterstellung → Recherche `Einrichtung vollständig durchführen` einmal auslösen. Das Plugin führt die vorhandene sichere Einrichtung selbst schrittweise aus; bei Fehler zeigt es einen konkreten Original-Sperrcode und bewahrt seinen Stand.
3. Wenn die Originaleinrichtung READY meldet, die bereits vorhandene Originalrecherche aktivieren. Falls DataForSEO-Zugangsdaten wirklich fehlen, dieselben vorhandenen Felder unter Diagnose verwenden. Eine bezahlte Recherche erfordert weiterhin gesonderte ausdrückliche Bestätigung.

**Ausgaberegel:** Nur vollständig gepackte, lokal geprüfte WordPress-Plugin-ZIPs zum Download; Zwischenstände/Entwicklungsdateien ausschließlich in Büros. Keinen Live-E2E-Nachweis fingieren.