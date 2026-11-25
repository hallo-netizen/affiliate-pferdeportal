# Hobbydepot – real erneut ausgeführter K-Multi-Freigabetest, 21.11.2026

**Technischer Test: 84/84 PASS. Finale Artikel-Freigabe: weiterhin GESPERRT.**

## Ausgeführt

[GitHub Actions: erneut ausgeführter K-Multi-Job 136912190598](https://github.com/hallo-netizen/k0-multiportal/actions/runs/44889447701/job/136912190598), erfolgreich abgeschlossen.

Aus dem **tatsächlichen Jobprotokoll**, nicht aus alten README-Aussagen:

- **31** Eingangs-/Hobby-FAQ-Bridgetests bestanden.
- **25** Freigabe-, Signatur-, Metadaten- und Ein-Datei-Tests bestanden.
- **12** LanguageTool-Adapter- und Fehlerblockadetests bestanden. **Dieser Job ist kein neuer echter Java-LanguageTool-Lauf**.
- **16** Tests der sicheren endgültigen Dateiausgabe bestanden.
- Zusätzlicher wirklicher Sicherheitsnachweis im Job: Wenn kein vertrauenswürdiger QA-Beleg vorliegt, bleibt die Datei gesperrt, und eine absichtlich vorhandene **alte WordPress-Importdatei wird entfernt**.
- Der wirklich im Job ausgeführte Aufruf mit dem **derzeit nicht genehmigten Hobby-FAQ-Regelbuch** antwortete exakt:
  `{"status":"BLOCKED_NO_WORDPRESS_IMPORT_FILE","reason":"HOBBY_FORMAL_RULEBOOK_NOT_APPROVED","portal":"hobby_depot","article_count":3,"old_k0_called":false,"publish_allowed":false}`.

Dieser Test hat die GitHub-Version `1094c8399fae2671ebcd5d12a7c8172d7f7d79d1` ausgecheckt. **Zusätzliche aktuelle Gegenprüfung:** alle neun fachlich relevanten K-Multi-Programm-, Test- und Hobby-FAQ-Kandidatenbuch-Dateien dieser geprüften Version sind **bytegenau identisch** mit denselben Dateien im jetzt gelesenen K-Multi-Zweig. Der erneute Lauf ist deshalb auch für deren aktuellen unveränderten Inhalt repräsentativ.

Die positiven „Freigabe“-Unit-Tests verwenden ausdrücklich **synthetische Schlüssel und erfundene QA-Prüfbelege** ausschließlich als Negativ-/Positivtests für die Sicherheitslogik. Damit wurde **keine echte fachliche Freigabe** nachgewiesen.

## Was bereits separat wirklich geprüft war

- Echte Java-Sprachprüfung, GitHub-Lauf [44889447704](https://github.com/hallo-netizen/k0-multiportal/actions/runs/44889447704): **3/3 Artikel PASS, 0 offene Fehler**.
- Echter Quellenabgleich, [44889232903](https://github.com/hallo-netizen/k0-multiportal/actions/runs/44889232903): **30/30 Absätze**, zehn Originalquellen, 16 Textauszüge. `research_complete=false`.
- Original-Hobbydepot-WordPress-PHP-Importer 0.4.24.18: Drei aktuelle Artikeltexte technisch akzeptiert, **keine** echte WordPress-Live-Importfreigabe; siehe `98_ERSTER_DREI_ARTIKEL_WP_IMPORT_FORMAT_PHP_TEST_20261121.md`.

## Exakt verbleibende Grenze

Die freigabeentscheidenden **eigenständigen vollständigen Quellen-/Autorenbelege, die echte Ausführung aller 121 Inhaltsregeln und die Genehmigung des eigenen Hobby-FAQ-Regelbuchs** fehlen. Das K-Multi-Original bleibt absichtlich `hobby_depot=NO_VALUES_BLOCKED`, `production_enabled=false`. Die zwei technischen Altverweise `Pflege` und `Anleitung` sind unverändert offen, betreffen jedoch **nicht** die drei geprüften FAQ-Artikel.

**Weder K0 noch K-Multi-Programmcode, -Registry, -Werte oder WordPress-Plugin wurden verändert.** Es ist kein Plugin und keine Artikel-Importdatei zu installieren. Dieser Eintrag dokumentiert den **wirklich neu ausgeführten Test**.
