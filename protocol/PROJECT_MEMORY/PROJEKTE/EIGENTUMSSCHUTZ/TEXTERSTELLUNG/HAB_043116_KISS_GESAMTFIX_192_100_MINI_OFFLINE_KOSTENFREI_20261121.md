# Hab & Bewahr 0.4.31.16 – einheitlicher KISS-Workflow, lokal geprüft

**Nur lokal getestet, keine Live-WordPress-Abnahme.** Ohne neue DataForSEO-Kosten. Neues Originalplugin-ZIP, SHA256 `814df2c3095c9adcab082503f86c7d8f9e3e7a51ac5d412ad42377066a44af87`, gespeichert unter `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/`.

### Gesamtablauf und Ursachen

Die ersten zwei Anbieterwege und PAA bleiben breit; der vierte originale Weg `Keyword Ideas` bleibt erhalten, erhält jedoch ausschließlich fachlich mit dem originalen Produktseed verbundene Folgebegriffe. Die originale Auswahl `PSTE_Research_Job::discoverySeeds()` ist der einzige Eigentümer dieser Auswahl. Die vorherige Fehlantwort zu Abholbox kam von 17/20 IKEA-Anschlüssen und enthielt 99/100 IKEA-Ideen. Offline-Replay aus genau 77 gespeicherten Suggestion/Related-Rohdaten: 7 an Abholbox gebundene Folgebegriffe, kein bloßes `IKEA Leipzig` oder `IKEA Produkte`; neue Anbieterantwort ausdrücklich **nicht** vorausgesagt.

In der vorhandenen `PSTE_Category_Context::portalContextEvidence()` werden lange C23-Artikelanweisungen nicht als verpflichtende Keyword-Wörter behandelt. Echte R3-Produktthemen und ein eigenständiges Sicherheitsmerkmal aus dem bestehenden Domain-Vertrag ergeben gemeinsam einen Portaleignungsbeleg. Unsichere Fremd-/Marken-/Ortsbezüge bleiben zur Klärung, keine zweite Prüfung. Die echte `PSTE_Normal_Metadata_Path` und unveränderte Original-MINI-Übernahme bestätigen `abholbox mit code`; IKEA-Abholbox, Interspar-Abholbox, Medikamenten-Abholbox bleiben nicht autorisiert. **192** echte Abholbox-RAWs: **1** eindeutiger positiver, **191** Review (kein pauschales Löschen), 0 Fremd-PASS. **100** echte Kamera-RAWs: 3 positive unter **synthetischen R3-Beispielen**, 97 Review. Das sind keine WordPress-live-2128er-Taxonomie-Nachweise.

### Bereits bezahlte Daten

Kein weiterer DataForSEO-Aufruf nötig. Die vorhandene original PSTE `startExistingOnly()`-Warteschlange und `reanalyzeRetainedBacklogBatch()` sind per einem einzigen WordPress-Admin-Knopf **`Gespeicherte Keywords kostenlos erneut prüfen`** erreichbar. Original-Warteschlange getestet: 163 gespeicherte Themen, `provider_fallback_allowed=false`, 0 Anbieter-Jobs. Der bestehende serverseitige Research-Driver führt die Schritte aus. Kein zweiter SEO-/Kategorie-/MINI-/K0-Owner, keine neue Datenbank.

### QA

134/134 vorhandene Original-PHP-Regressionen (darunter 48 DataForSEO-Methoden, Queue, MINI, K0, Import, PAA), 192 und 100 echte Rohdaten, 14 Abholbox- und 8 Kamera-Gegenfälle, 3 Original-Existing-Only-Queue-Starttests, 78/78 PHP-Lint, 87/87 ZIP CRC. 82/87 Quelldateien identisch zur Vorversion, 5 Dateien verändert: `texterstellung.php`, `README-TESTINSTALLATION.txt`, Original-Domainvertrag, Original-Keyword-Ideas-Auswahl, Original-Portal-Kontext-Evidenz. **Original-MINI, K0, Export, Import unverändert.** Keine echte WordPress-Datenbankmigration oder DataForSEO-Liveabnahme durchgeführt.

### Bedienung / freizugebender Schritt

Nach WordPress-Backup vorhandenes Plugin durch 0.4.31.16 **ersetzen, nicht deinstallieren**. Einmal WordPress → Texterstellung → Recherche → **`Gespeicherte Keywords kostenlos erneut prüfen`**. Im selben Reiter kostenlosen Status bis `COMPLETE` verfolgen, dann **MINI-Export** und Diagnosedatei prüfen. Das Anzeige-Feld `0 direkt artikelbereit` aus einem älteren abgeschlossenen Lauf ist **kein Beweis** für weiterhin fehlenden Portaleignungsbeleg: Der Titel und die konkrete Kategorie entstehen erst im unveränderten MINI. Keinen weiteren bezahlten Anbieter-Test vor Abnahme.

Prüfbericht, Einzeltests und QA-JSON im Hab-Büro: `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_KISS_GESAMTFIX_043116_20261121/`. Kein Erfolg behauptet, bevor der kostenlose Live-Bestandslauf abgeschlossen ist.
