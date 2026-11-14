# WASSERTECHNIK / PLUGINS – einzige aktuelle Büroautorität

**Stand:** 14.11.2026 · **Status:** WT001 **0.1.3 SEO-SAMMELRECHERCHE FERTIG GEBAUT, OFFLINE/NEGATIVTEST PASS**, WordPress-Update und reale DataForSEO-Kostenabfrage OFFEN. Keine Importe.

**Aktiver ZIP-Kandidat:** `WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.3_SEO_GESAMTRECHERCHE_NUR_TEST.zip` (SHA256 `272403e8c094825c918db65a01a78321baf59ac19af07bc05d089c2cdaa0bb5c`, Git-Blob `44fb42a6a52718b645ae79003e36640fb38d7e2e`). **Ein Update derselben Pluginidentität**, kein zweites Plugin. WordPress-Anbindung ist hart auf die bereits im Testexport bestätigte Ziel-Website `wasser.oliver-beil.de` begrenzt; fremde Portale können die Bezahlfunktion nicht ausführen. Plugin 0.1.2 ist im echten WP-Export nachgewiesen, **0.1.3 noch nicht**.

**Ein Gesamtauftrag im vorhandenen Kategorieplugin:**
1. Vorhandenes W4-Manifest 218/218 (8 Hauptbereiche, 19 Untergruppen, 1 Industrieeinstieg, 6 Industrie-Landings, 79 Produktseiten, 105 Rubriken) ohne neue Keyword-Entscheidung übernehmen.
2. DataForSEO Google Ads Search Volume Live: eine Sammel-POST-Anfrage für alle 218 Keywords; Ergebnis ist Suchvolumen, CPC, **nur Anzeigenwettbewerb**.
3. DataForSEO Labs Google Bulk Keyword Difficulty Live: eine Sammel-POST-Anfrage für organische Rankingschwierigkeit.
4. DataForSEO Labs Google Search Intent Live: eine Sammel-POST-Anfrage für Informations-/Kaufabsicht.
5. Resultate zentral in **einem** 218-Zeilen-JSON-Bericht mit ursprünglichem Owner, tatsächlich gemeldeten Anbieterkosten und Nullwerten für unbeantwortete Begriffe. **Kein automatischer Kategorieentscheid, kein WP-Import.**

**Kosten/Sicherheit:** Auf Basis der DataForSEO-Anbieterpreise vom 14.11.2026 ungefähr **0,16632 USD** (0,09 + 2×(0,012 + 218×0,00012)). Administrativer Haken plus eigener Button und Nonce **vor** der kostenpflichtigen Aktion; ohne Zustimmung keine API-Anfragen. Budgetprüfwert 0,25 USD: das Plugin stoppt weitere Calls, wenn der bereits gemeldete Anbieterpreis plus nächste Schätzung den Budgetwert übersteigen würde. **Keine Garantie einer absoluten Preisobergrenze:** Der Anbieter meldet den tatsächlichen Preis jeweils erst nach dem Aufruf. Dauerhafte atomare Einmalsperre verhindert doppelte Kosten selbst bei Fehler/Timeout/Mehrfachklick. Keine Auto-Retries/Cron/Schleife; Teilergebnisse werden nach jedem Anbieteraufruf gespeichert.

**Offline-QA:** PHP-Lint 4/4 PASS, ZIP 6/6 und CRC PASS, WP-CLI-Simulation: 3 Sammelanfragen × 218, alle 218 Result-Owner mit Volumen/organischer Schwierigkeit/Suchintention korrekt verbunden. Negativtests: teurer erster Aufruf → keine weiteren POSTs, unerreichbarer Server → keine Wiederholung, falsche Website → 0 POSTs, Duplikatklick → 0 POSTs. Kein `wp_insert_post`, `wp_insert_term`, Publish-/WP-Importschreiber. Siehe `../PRUEFUNG/WT001_013_EINMALIGE_GESAMTABNAHME_20261114.md`. **Noch kein echter WP-Live-Test oder Anbieter-POST.**

**NEXT ACTION:** Diese einzige neue Version **0.1.3** als Update auf `wasser.oliver-beil.de` installieren, im vorhandenen **Wassertechnik Kategorie → DataForSEO** die Kostenfreigabe ausdrücklich erteilen und den **einen** Gesamt-Button ausführen. Danach dort **ein** Ergebnis-JSON herunterladen und zur zentralen W4-Auswertung übergeben. Vor diesem Klick **keine** kostenpflichtigen Abfragen, keine weiteren WP-Schreibaktionen.
