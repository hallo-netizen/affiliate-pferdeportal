# QA85 – bestehende Zeitsteuerung wiederhergestellt (nur Quellkorrektur, 16.11.2026)

**Status: lokal geprüft, nicht live installiert, GitHub-Zeitgeber auf main unverändert. Keine neue Plugin-ZIP und KEIN neues Regelwerk.**

## Originalbeweise

- Originale Sichtbarkeitsdiagnose vom 16.11.2026, 10:20:18 UTC: 309 sichere Kampagnenkennungen, davon **293 wegen fehlender Frische**, acht nicht verfügbar, acht grundlegend zulässig. Verfügbarkeits-Cursor `12568`, `checked=448`, `running=1`, letzter Batch 09:22:53 UTC, `next_due_at` 09:24:23 UTC – beim Export **55,9 Minuten überfällig**.
- Historischer QA80-Originalstand: 15.11.2026, 16:22 MEZ, `checked=403`. Seitdem bis 16.11., 10:22 MEZ nur **45 zusätzliche Prüfungen in rund 18 Stunden** = **2,5 Prüfungen pro Stunde**; damit besteht der frühere Stau objektiv weiter.
- Main-GitHub-Job **43834993089** meldete am 16.11. 08:55 UTC `completed` / `no successor runner required`. Kein weiterer GitHub-eBay-Run zwischen diesem Abschluss und dem Abgleich des Diagnoseexports nachweisbar.
- Das hier benutzte ursprüngliche QA84-Installationsarchiv hat SHA256 `acf8aedb1c21c75742107f07eb8b9e8c2964a5faebabc52e72d331c05cea9ce3`.

## Zielvertrag / wiederverwendete Lösungen

- **QA9:** Anzeige bereits bestätigter Produkte unabhängig von Recherche, getrennte Verfügbarkeits-Arbeit mit eigenem gespeichertem Cursor, selbst bei Recherchepause/-fehler.
- **QA16/17:** derselbe vorhandene externe Heartbeat kann Verfügbarkeitsarbeit unabhängig vom Recherchezustand anstoßen.
- **QA24:** ein `idle` während offener Arbeit darf die GitHub-Kette nicht beenden; früherer Originalnachweis am 11.11.2026.
- **QA69:** ein externer Zeitgeber, keine zweite Produktauswahl, keine zweite Veröffentlichung, kein neuer Worker; nur die beiden schon vorhandenen Arbeitsanteile mit getrennten gespeicherten Fortschritten.
- **QA80:** höchstens 20 fällige veröffentlichte Quellen pro Paket, 22 Sekunden Zeitbudget, Cursor nur nach abgeschlossener Bearbeitung, kein Frischeverlust durch verfrühten Rücksprung.

## QA84-Gesamtfehler – direkt im vorhandenen PHP nachgestellt

In `includes/trait-ppar-ebay-run.php::handle_ebay_external_tick` wird vor dem Verfügbarkeitsaufruf bei `operator_paused` oder `failed` verlassen. Bei abgeschlossenem Recherchelauf wird trotz `availability.running=1` anschließend `idle/no_due_operation` gemeldet. Dazu entfernt QA84 den vorherigen WordPress-Availability-Cron. Der Main-GitHub-Runner beendet seine Kette auf `idle|completed|failed|disabled`. Damit kann eine Frischearbeit mit offenem Cursor liegenbleiben. Das **verletzt bereits geprüfte frühere Lösungen**, statt einen neuen Fehler zu begründen.

## Bereits vorhandener Code korrigiert – NUR lokale Arbeitskopie

Einziger geänderter Produktionscode: `includes/trait-ppar-ebay-run.php`.
- Den bereits vorhandenen Availability-Aufruf auch bei abgeschlossener, pausierter oder fehlgeschlagener Recherche zulassen.
- Solange derselbe gespeicherte Availability-Cursor `running` bleibt, `advanced/availability_tick` statt terminales `idle` oder `completed` melden; das gilt auch für den 90-Sekunden-Abstand zwischen Paketen.
- Gespeicherte Recherche-UUID, Recherche-Fehler/Pause und zuletzt gültiger SAFE-Checkpoint bleiben unverändert; kein weiterer Anbieterarbeiter, keine neue Recherche, kein neuer Cron.
- Wenn Availability tatsächlich fertig und Recherche nicht fällig ist, bleibt normales `idle`; ein echter Recherchefehler ohne offene Availability bleibt `failed`.

**Direkter RED/GREEN-Test der echten PHP-Heartbeat-Methode mit nachgestellten WordPress-Speichern:**
- QA84 **6/12 PASS**, korrigierte Quelle **12/12 PASS** für abgeschlossen, pausiert, fehlgeschlagen, aktive Recherche, Verfügbarkeitsarbeit fällig, 90s-Wartefenster und tatsächlich vollständig.
- Alte 16 REST-Statusfälle unverändert, neun Fristfälle bestanden, normaler Worker-Fairness-Test bestanden.
- Neun Gesamtläufe gegen 283 Originalfamilien im vorhandenen Modell: fünf `completed`, vier erwartete `failed`; 23 PHP-Dateien syntaktisch gültig.
- Delta-Patch 1:1 auf unveränderte QA84-Quelldatei angewendet; bytegleich mit getesteter Korrektur.

**Artefakte in diesem Ordner:** `QA85_HEARTBEAT_KORREKTUR.patch`, `QA85_BEWEIS.json`. Keine neue Live-Freigabe allein durch lokale Tests.

## Noch erforderliche echte Übernahme – ein Gesamtvorgang

1. Bestehende Heartbeat-Korrektur in die **eine bestehende Affiliate-Zentrale** integrieren; keine doppelte Steuerung installieren.
2. Die bereits geprüfte GitHub-5-Minuten-Uhr in [PR #759](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/759) **nur im regulären Freigabeverfahren** übernehmen. Der PR ist `open / blocked / unmerged`; Hardlock nicht umgehen. Ohne zuverlässigen externen Takt bleibt die Korrektur unvollständig.
3. Nach zulässiger Freigabe **nur die gespeicherten Quellen des bestehenden SAFE-Bestands** frisch bestätigen; in einem einzigen realen Durchlauf messen, dass 293 abgelaufene und andere noch gültige Produktslots wieder aktuell/korrekt gesperrt sind, ohne Katalog-Vollsuche oder neue Fachentscheidung.

**Wichtig:** Der Screenshot/Export beweist den aktuellen Live-Stau, nicht die genau installierte Versionsidentität. Kein neues Plugin oder Produktionsstart aus nur einem Mock-Ergebnis.


## Verbindliche zusammengefasste Anschlussprüfung – nicht erneut separate Fixes bauen

Der vollständige QA69-Gesamtabgleich gegen das echte QA84-Archiv, die alte QA9/QA16/QA24/QA77–QA85-Fehlerkette und den WordPress-Sichtbarkeitsexport liegt **im selben Ordner** unter `QA85_GESAMTABGLEICH_ZIELVERTRAG.md`.

**Einziger gesamte Quelländerung gegenüber 6.72.352:** `QA85_GESAMTPATCH_GEGEN_QA84.patch` (zwei vorhandene eBay-Traits; keine weiteren 64 Originaldateien). Ergänzt gegenüber dem ersten QA85-Einzeldiff sind: (1) terminaler Workerabschluss darf offene Verfügbarkeitsarbeit nicht beenden; (2) Quellepakete nur aus der **bestehenden** SAFE-Kampagnenliste statt aus historischen veröffentlichten Datensätzen; (3) nur der unabhängige Quellenprüf-Cursor wird beim Wechsel auf diesen bestehenden SAFE-Checkpoint ausgerichtet.

**Lokal originale PHP-Funktionen mit simulierten WP/eBay-Daten:** 15/15 gekoppelte Laufstatusübergänge PASS (QA84 8/15, QA85-Vorversion 14/15); bei aus dem Export abgeleitetem Lastmodell 309 aktuelle SAFE-Produkte, 496 historische veröffentlichte Objektzeilen und 9.792 historische Quellen: 309/309 gültige SAFE-Quellen in 16 simulierten Paketen, 0 weitere, 0 neue Produktsuchen, SAFE/Recherchecursor unverändert; einfacher öffentlicher PHP-Lieferfilter vor Verfügbarkeit BLOCK, nach frischer Verfügbarkeit ALLOW (kein Beweis für reale Frontend-Rangfolge); 283 Originalfamilien in neun vorhandenen Controller-Modellszenarien, fünf erwartete Endabschlüsse/vier kontrollierte Fehler; neun Fälligkeitsfälle, 16 REST-Statusfälle, 95 historische Artikel-IDs mit nachgestellten Antworten, 23 PHP-Syntaxdateien PASS. Komplett reproduzierbare Beweise und die zwei direkten Testskripte sind im selben Ordner.

**QA69 LIVE weiterhin NICHT BESTANDEN:** echte GetItem-Dauern und öffentliche 283er-Endbilanz fehlen; der einzige neue externe 5-Minuten-Takt [PR #759](https://github.com/hallo-netizen/affiliate-pferdeportal/pull/759) ist unmerged und blockiert. Bei 309 gleichzeitig fälligen SAFE-Quellen wären im 2h-Vorlauf mindestens 13 erfolgreiche Prüfpunkte pro 5-Minuten-Takt nötig. Keine Installationsfreigabe allein aus den Modellresultaten, kein Liveeingriff, kein Hardlock-Bypass, keine neue Vollsuche.

**Dieses Protokoll verweist auf EIN konsolidiertes QA85-Gesamtergebnis. Der frühere schmale QA85-Patch ist Historie, nicht die nun zu installierende Gesamtversion.**
