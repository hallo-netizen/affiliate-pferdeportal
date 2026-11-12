# BESTÄTIGTER BLOCKER: Gesamtdiagnose scannt unnötig ~5.014 Themen (11.11.2026)

**Kein neuer Plugin-Release. Befund aus der tatsächlich ausgelieferten PSTE 0.57.144.35 ZIP.**

## Was passiert im echten Code?
- Der sichtbare Button „Gesamtdiagnose herunterladen (nur lesen)“ startet die JavaScript-Funktion scanTopics(), sofern kein Scan im temporären Browserzustand abgeschlossen ist.
- scanTopics() ruft per Ajax pste_evidence_read_batch wiederholt auf; PSTE_Evidence_Audit::batch() liest mit PAGE_SIZE=40 jeweils die gespeicherten topic_pool.payload_json-Zeilen.
- Bei 5.014 Themen bedeutet das mindestens 126 aufeinanderfolgende Serveranfragen, zuzüglich Abruf der Historie. Nach einem Seiten-Neuladen beginnt der Scan neu.
- Dies sind **Lesezugriffe**, keine neue Themenbewertung, keine DataForSEO-Recherche und keine WordPress-Schreibzugriffe. Der Download ist für eine bloße Fehlersuche dennoch unnötig schwer und wiederholt den schon oft beanstandeten Ablauf.
- Der PHP-Code enthält bereits workflowDiagnosticsSnapshot() und PSTE_Flight_Recorder::report(150). Der bestehende Export pste_export_flight_protocol ist registriert, hat in PSTE .35 jedoch keinen sichtbaren Direktknopf. Der QA-Entwurf .36 fügt einen Knopf hinzu, beseitigt jedoch nicht die falsche Voreinstellung des Gesamtdiagnoseknopfs.

## Verbindliche KISS-Korrektur, bündeln statt neue Einzelplugins
1. Für einen STOP-Fehler ist **ein sofortiger Download bereits gespeicherter Status-/Fehler-/Flugschreiber-Ereignisse** der Standard. Keine topic_pool-Einzelzeilen, kein scanTopics(), keine 126 Serveranfragen, keine Anbieteraufrufe.
2. Einen detaillierten Gesamtbestand mit allen einzelnen Zeilen nur als freiwillige, klar als langwierig bezeichnete Zusatzdiagnose anbieten – nie als Pflichtschritt.
3. Bereits gespeicherte Fehler ohne Neustart ausgeben. Bei fehlendem historischen Detail dieses ehrlich als nicht gespeichert kennzeichnen.
4. Die Ursache der echten WordPress-Sperre PSTE_EXISTING_ONLY_LOGIC_RECHECK_SOURCE_CHANGED_* bleibt offen. Keine Sicherheitsprüfungen aushebeln, kein Reset.
5. Vor Freigabe zusammen testen: Status-Download ein Klick nach Seitenreload, 0 Themen-Single-Batch-Aufrufe, 0 Schreibzugriffe, 0 Provider, prüfbarer Dateiinhalt. In einem gemeinsamen Release mit der Ursachenbehebung; keine weitere Mini-ZIP.

**Stand: SOURCE_RESCAN_CONFIRMED; NO_NEW_PLUGIN; REAL_WP_STOP_OPEN; K0_UNTOUCHED.**