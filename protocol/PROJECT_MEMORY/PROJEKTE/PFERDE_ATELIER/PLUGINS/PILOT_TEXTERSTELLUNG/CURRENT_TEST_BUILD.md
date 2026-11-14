# Texterstellung – aktueller Testkandidat, 14.11.2026

**Nur eine aktuelle Testfassung: 0.4.3. Kein Live-Release und keine behauptete 61er-Vollproduktion.**

## ZIP und unveränderte Bausteine
- Library: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung_0.4.3_CategoryWorker_Bindings_NUR_TESTWORDPRESS.zip`
- SHA-256: `55373d1c388db342a2179353eb05676bc9c07aa09f2719a4fde10ea967d5252a`
- Gegen alte 0.4.2-ZIP: 170 von 173 unverändert, **164 von 164 Original-PSTE/PSERC-Dateien unverändert**. Nur `texterstellung.php`, `includes/class-txe-legacy-source-bridge.php` und README angepasst. Keine neue Tabelle, kein neuer fachlicher Worker, kein Frontend-Umbau.
- Genaues vollständiges Delta: `TXE_043_EXACT_DIFF.patch`; genaue beiden Programmquellen: `TXE_043_PLUGIN_MAIN.php`, `TXE_043_LEGACY_SOURCE_BRIDGE.php`.

## Warum 61 historische FREI nicht K0-fertig?
- Der historische 87er-SEO-Bescheid (61 FREI, 20 BELEGT, 6 KLÄRUNG) gab Keyword, Suchabsicht und Titel frei, aber **kein vollständiges K0-Metadatenpaket**.
- Originaler PSTE-Stapelbericht von 09.11.2026 15:47 UTC: 61 Kandidaten, **8 NORMAL_PATH/NORMAL_PASS, davon 7 PASS und 1 HELD; 52 CATEGORY_ROOM_TOPIC_POOL; 1 gesondert BLOCKED**. Letzter echter WP-Diagnoselauf 14.11.2026: 61/61 `METADATEN_OFFEN` und `ORIGINAL_EDITORIAL_METADATA_NOT_FINAL=61`. Zeitstände nicht vermischen.
- Eine konkret nachgewiesene Anschlussursache war `savedMetadata()`: Alter **Kategorie-Worker** speichert bestätigte manuelle Zuordnung in `manual_status=REASSIGNED` mit `manual_category_id` und `manual_article_type`; die 0.4.2-Brücke akzeptierte ausschließlich `manual_status=APPROVED` (welches tatsächlich **keine Kategorie-ID** trägt!) bzw. nur `NORMAL_PASS` mit zusätzlich alter PPM-`planning_suitability=YES`. Damit konnten gültige Originalzuordnungen trotz alter Plan-Sperre unsichtbar bleiben.

## 0.4.3-Korrektur
- Liest bestehende Original-Zuordnung **ohne Zweitentscheidung** bei `REASSIGNED` (gültige Kategorie-ID, mit aktuell übereinstimmendem WordPress-Term, festgelegter Artikelart, echtem Prüfer) oder dem vollständig quell- und strukturgebundenen `PSTE_NORMAL_METADATA_PATH_V2 / NORMAL_PASS`. Die alte PPM-Planungsbereitschaft wird nicht mit einer Kategorieentscheidung verwechselt.
- Bereits FREI-genehmigte Titel und Keywords unverändert. Unbekannte oder widersprüchliche Felder bleiben **offen im bestehenden Redaktionsbüro**, werden nicht erraten oder neu freigegeben.
- Der **gleiche vorhandene Quellabgleich** wird nur nach ausdrücklicher isolierter Testseitenbestätigung als täglicher WP-Cron angelegt; Wiederholung ist lesend zur Originalquelle, aktualisiert die bestehende TXE-Auftragsoption nur bei vorhandenen Werten. Cron wird bei Deaktivierung abgemeldet. Das Cron selbst erzeugt keine Kategorien und ist kein zweiter SEO-Worker.
- **Zukünftige** FREI-Genehmigungen laufen über den unveränderten einzigen PSTE-SEO-Owner: Kategorie und Artikelart sind im bestehenden Normal-Quellweg vor Titelfreigabe Pflicht. Fehlende Kategorie bleibt Büro-Arbeitsfall, kein K0-Release. Keine kostenpflichtige Neu-Recherche nötig.

## Belegte Tests und Grenzen
- **17/17** mit 61 **unveränderten** echten Auftrags- und Titelwerten aus der neuesten hochgeladenen Diagnose und dem originalen MINI-Ergebnis: 0 K0, 0 Entwürfe, erwartete Sperre.
- **12/12** Regressionen technischer Kategorienanbindung (Testterm-Werte **nur** für Gegenbeispiele, **nicht** in die echten 61 geschrieben).
- **27/27** Regresstests mit **synthetischen** 20er-Aufträgen (Original-PSTE-/PSERC-Funktionen, nachgebildete WordPress-Antworten).
- **5/5** planbarer täglicher Abgleich / Testschutz / Deaktivierung.
- **117/117 PHP Syntax**, ZIP-Integrität bestanden.
- Vollständige Nachweise: `TXE_043_QA_SUMMARY.json`, `TXE_043_PRUEFBERICHT.md`, `TXE_043_MANIFEST.json`.

**Nicht abgenommen nach 23-Regel-Zielvertrag:** Die aktuelle echte WP-Pooltabelle liegt nicht als Rohdaten vor; deshalb ist noch unbewiesen, wie viele der 61 unter 0.4.3 wirklich vollständige Kategorie-/Artikelartbindungen erhalten. Historisch 52 Kategorie-Büro-Fälle benötigen den **bestehenden ursprünglichen Kategorie-Worker**, falls eine neue Kategorie gefunden oder später ergänzt wird. Der tägliche Abgleich allein löst deren ursprüngliche Kategorieentscheidung nicht. Externe Google-Fragen, K0-81-Regel-Texte und tatsächlicher WP-Entwurfsimport wurden nicht real im System ausgeführt. Kein Live-Release.

**Testupdate:** Auf der bestehenden **isolierten** WordPress-Testseite 0.4.2 durch die obige ZIP ersetzen, Testmodus beibehalten, `Texterstellung → Redaktionsplan → Bestehende FREI-Freigaben übernehmen`, Diagnose herunterladen. Original-61-Freigaben und bestehende WP-Entwürfe nicht löschen.
