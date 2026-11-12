# QA31 KISS – überprüfte Einzelzuständigkeiten und Rückbau (12.11.2026)

**KEINE Live-Abnahme.** Vollständiger lokaler Plugin-Kandidat **6.72.335**, basierend auf installierter 6.72.334; der frühere QA29-Private-Löschbutton ist wegen belegter 0-Altpost-Treffer entfernt. Private Altpost-IDs 12284–12301 (16 Stück) hat Nutzer inzwischen in WordPress **selbst** gelöscht.

## Originalcode-Beweise
- **Doppelte GitHub-Automatik** in `.github/workflows/pferde-atelier-ebay-heartbeat.yml`: GitHub `schedule */15` PLUS automatisches `workflow_dispatch` nach 30 Einzelticks; Ziel stets `POST https://pferde-atelier.de/wp-json/affiliate-zentrale/v1/ebay/tick`. Ein kanonischer PHP-Worker, aber zwei GitHub-Wecker.
- **Echter Live-Beleg:** Actions Run `43223625041`, Job `131201124749` vom 12.11., 13:03–13:37 UTC: 15 abwechselnde `active_idle`-Statusmeldungen und echte `advanced/busy`-Arbeitsschritte, abschließend `successor heartbeat runner dispatched`.
- **Noch offener Widerspruch:** `active_idle` wird in GitHub nur aus Live-Antwort `status=idle, reason=availability_tick, run_status=running|paused` gemacht. Im vorliegenden Original-PHP 6.72.334 ist genau der Verfügbarkeitszweig in `handle_ebay_external_tick` bereits entfernt. Die **tatsächlich von WordPress ausgeführte** Codefassung ist nicht nachgewiesen. Nicht mit GitHub-Statuskosmetik verschleiern.
- **Weitere KISS-Kreuzungen:** gespeicherter eBay-Neulauf hieß `worker_transport=self_drive`, ausgeführt tatsächlich `external_tick`. Generisches Awin/ADCELL-Quellenregister konnte über einen Filter fremde Provider einschleusen, derselbe Quellencheck lief zweimal, manueller Providerstart konnte ungefiltert fremden Queue-Job verarbeiten. Idealo-Manualimport konnte durch Loopback + WordPress-Fallback **nacheinander zweimal** laufen.
- **Awin/ADCELL bleiben noch NICHT separat:** Gemeinsame Auftragsliste, gemeinsame 2-Wochen-Cursor-/Zyklusoption, generischer `AUTOMATION_WORKER_HOOK`, `FULL_POOL_WORKER_HOOK` und eigene ADCELL-Batch-Anstöße. Eine sichere Trennung erfordert echte Migrations-/Bestandsprüfung statt eines blinden Rückbaus.

## Technische direkte Vereinfachung im vollständigen lokalen Plugin 6.72.335
- eBay neuen Run / read-only-Status konsistent `external_tick`; älteren Laufvertrag `self_drive_v1` absichtlich unverändert zur Cursorkompatibilität.
- Generische automatische Quellen fachlich auf `awin` oder `adcell` beschränkt; ein nachfolgender **doppelter** Providerzulässigkeitscheck entfernt.
- Manueller Awin-/ADCELL-Start gibt genau den gewählten Provider an seinen bestehenden Worker weiter.
- Vorhandener idealo-Fallback startet **nur bei weiter `queued`**, keine zweite Importausführung nach Erfolg.
- Unbrauchbaren QA29-Sonder-Löschknopf samt Backend-Routine aus dem bestehendem Plugin entfernt, keine Löschung während Upgrade.
- Amazon, GTIN/ASIN-Matching, eBay-Speicherstand/Lease/Worker, Anzeigen-/Frontend-Entscheidungen und restliche Provider unverändert. Kein neuer Cron, kein separates Zusatzplugin, keine neue Tabelle.

## GitHub-Zeitgeber-Rückbau als PR #759
<Link:https://github.com/hallo-netizen/affiliate-pferdeportal/pull/759>

Nur noch **ein** Zeitplan `schedule */5`, max. **4** REST-Ticks im Zeitfenster, je max. 45 Sekunden plus 30 Sekunden Pause, insgesamt worst case etwa 4,5 Minuten; 10min GitHub-Timeout, unveränderte Serialisierung, alte Selbstverkettung und unnötiges Actions-Write entfernt. **PR OFFEN, NICHT LIVE**. GitHub `hardlock-base` schlägt vorhersagbar fehl: Sicherheitsskript `.github/workflows/pferde-atelier-immutable-base-hardlock.yml` verbietet **jegliche** Änderungen unter `.github/workflows/`, mit Meldung `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`. Schutz nicht umgangen; Freigabe muss ausdrücklich autorisiert werden.

## Tests (originales PHP, lokale Mocks; kein Live-End-to-End)
- eBay-Kanonical-Worker **70/70 PASS**.
- Amazon/ASIN-Freigaben **41/41 PASS** (inkl. sieben echte Diagnosedatensätze).
- idealo/Provider-Verteilung **12/12 PASS**.
- alle **23/23** PHP-Dateien syntaktisch korrekt.
- **66/66** Plugin-ZIP-Einträge CRC gültig.
- Workflow-PR 8/8 lokale strukturelle KISS-Checks, noch kein erfolgreicher Hardlock-Gate.
- Vollständige ZIP **6.72.335** SHA256 `6c1cbfe754fb3a76a1fe7fcc12574cfae457d71fbbbec85ed7326ba597ab1190`, Pfad im persönlichen QA-Pluginbüro `/pferdeatelier/PLUGINS/QA/Pferdeatelier_Affiliate_6.72.335_KISS_EINDEUTIGE_ZUSTAENDIGKEITEN_GESAMT_NICHT_LIVE.zip`. Beweisbericht, Diff, Testprotokolle ebendort.

**Sicherer weiterer Ablauf:** 6.72.334 zunächst nicht ersetzen. Erst Widerspruch zwischen laufendem REST-Transport und Quellcode beweisen; danach geschützte GitHub-PR nur nach autorisierter Hardlock-Entscheidung, Awin/ADCELL unter bekanntem Live-Job-Zustand entflechten, dann tatsächlichen unbeaufsichtigten kompletten Lauf abnehmen. Keine falsche Behauptung vollständiger Umsetzung.
