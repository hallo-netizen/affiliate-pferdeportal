# Hobbydepot Texterstellung – 20.11.2026 Originalübernahme, isolierte 0.4.24.14 und K0-Testzweig

**Status:** noch keine Installations-/Produktionsfreigabe. Live-Diagnose 08:21:11 UTC belegt Hobbydepot 0.4.24.13, original_research=RUNNING, 0 Textaufträge, kein K0-Batch.

## Belegter Recherchefehler und Korrektur
Original-PHP des eingebetteten PSTE erwartet zwei Originaldateien `class-pste-family-structure-router.php` und `class-pste-product-choice-classifier.php`, die im integrierten Hobby- und Pferde-Texterstellungspaket fehlen. Vollständiger Pferdeatelier-PSTE-Originalstand 0.57.144.25 enthält beide. Der Fehler `PSTE_RETAINED_BACKLOG_AUDIT_LOGIC_FILE_MISSING` wird mit echtem Original-PHP reproduziert; Übernahme der zwei Dateien **byteidentisch** nur in eine lokale Hobby-Kopie und Wiederaufruf der unveränderten Methode läuft PASS. Eine einzelne Datei fehlt weiterhin -> der zweite Fehler wird korrekt angezeigt. Negative Fingerabdruck-Manipulation ändert den Audit-Hash.

Lokale **nur intern für QA** 0.4.24.14: Genau 2 zusätzliche unveränderte Originaldateien und 1 Versionszeile ggü. 0.4.24.13, **sonst alle ursprünglichen 87 Dateien unverändert**. 308/308 bestehende angepasste Originalprüfungen erfolgreich (23 Gruppen); zusätzlich 111/111 fokussierte Datei-, Methoden-, Benutzeraktionen, AJAX-, WordPress-Simulationen, Negativ- und PHP-Syntaxprüfungen PASS. Die 111 und 308 Testreihen überschneiden sich. Frühere 302/302 und 63/63 vorliegend. Testpaket **nicht** für Installation freigegeben.

## K0-GitHub-Abgleich
Im aktuell maßgeblichen K0 `konzept0-portal-neutral-20261002`, `.github/workflows/k0-writer-accept.yml`, wurde `k0_portal_resolver` ohne den vorhandenen `PSERC_SOURCE_MANIFEST.json`-Beleg aufgerufen und WordPress-Kategorien immer unter `https://pferde-atelier.de` abgefragt. Für Hobby nicht portalneutral. Exakt diese zwei technischen Stellen sind in **getrenntem Staging-Zweig** `qa/hobby-k0-original-host-only-20261120` angepasst: Original-K0-Resolver erhält den schon vorhandenen signierten WordPress-Beleg; spätere Kategorieabfrage verwendet dessen bereits verifizierten Host aus der bestehenden Registry, Legacy-Pferdeweg bleibt. Kein neues fachliches Routing, keine Änderung an 81 K0-Regeln, PPM, LanguageTool, Writer, Artikel oder Veröffentlichungsregeln. GitHub-Compare: nur **eine** Workflow-Datei, +22/-4 Zeilen. Aktive K0-Branche unverändert. Acht gezielte technische Host-/Sperrtests lokal PASS, noch **keine echte GitHub Writer-Ausführung**.

## Was weiterhin fehlt
- Die Nutzerdiagnose enthält keine Einzelwerte der 223 gespeicherten Keywords. Ein tatsächlich abgeschlossener kostenloser Live-Replay ist nicht bewiesen. Keine kostenpflichtige DataForSEO-Abfrage starten.
- Vollständiges lokales PHP `Relevanz → MINI CATEGORY/EDITORIAL/TITLE → FINAL → K0-Auftragsdatei → WP-Entwurfsimport` mit WordPress-/K0-Schreibtext-Mocks PASS, inklusive gefälschte K0-Slot-Sperre.
- Zwei bereits K0-fertig geschriebene Original-Pferdeartikel wurden im Original-WordPress-Importer erfolgreich zu zwei Entwürfen verarbeitet (reimportiert ohne Dubletten).
- **Neuer echter Hobby-K0-Writer** samt 81 Regeln, PPM 104, echtem LanguageTool 6.8 und fertiger WordPress-Datei für das aktuelle Hobby-Thema wurde **nicht** ausgeführt. GitHub Hobby-Discgolf-Run `44545937080` SUCCESS war nur eine vorhandene Fixture.
- Keine neue installierbare Pluginversion ausgeben, bevor die zwei echten Live-Abschnitte durch den Originalablauf abgenommen wurden.

Lokaler dokumentierter Bericht und ZIP nur mit QA-Beweisen, **ohne Installationsplugin**, im Chat: `hobbydepot_pruefbericht_20261120_final.md`, `hobbydepot_qa_beweise_20261120.zip`.
