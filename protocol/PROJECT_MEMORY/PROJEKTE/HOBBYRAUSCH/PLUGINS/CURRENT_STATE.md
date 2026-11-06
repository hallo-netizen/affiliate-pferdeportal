# HOBBY DEPOT – PLUGINBÜRO – AKTUELLER BESTAND

Stand: 02.11.2026. **Nur selbst entwickelte Hobby-Depot-Plugins und eigene Projektwerkzeuge. Keine Fremdplugins.**

Die technische Einzelwahrheit liegt weiterhin ausschließlich in der jeweiligen Plugin-Akte unter `PLUGIN_AKTEN/<Plugin-ID>/CURRENT.md`. Die WordPress-Pluginliste ist ein älterer Betreiberstand vom 01.11.2026; aktuelle Serverdateien wurden nicht selbst ausgelesen.

## Eigene Plugins / Projektwerkzeuge – laut letzter WordPress-Liste aktiv

| Eigenplugin | Belegter Versionsstand | Stand der ORIGINAL-Sicherung im Pluginbüro |
|---|---|---|
| HD-001 – Kategorie-Workflow | 1.14.17 (WordPress-Liste) | Aktuelle Voll-ZIP noch nicht im Büro; ältere 1.14.16 in der Projektkonversation vorhanden |
| HD-003 – Design / Template Kit | 1.50.798, vom Betreiber im Frontend abgenommen | **Voll-ZIP gesichert, unabhängig geöffnet** |
| HD-004 – Kategorie-Kern | 1.0.0 | **Original-Voll-ZIP gesichert, unabhängig geprüft** |
| HD-005 – Glossar Core | 1.0.25 | Aktuelle Voll-ZIP noch nicht im Büro |
| HD-006 – Bildzentrale | 2.7.8 | Aktuelle Voll-ZIP noch nicht im Büro |
| HD-007 – Hobbyregister Core | 1.2.16 in WordPress-Liste, 1.2.17 als neuer Stand freigegeben | **Voll-ZIP 1.2.17 gesichert, unabhängig geöffnet; Serverstand nicht separat geprüft** |
| HD-009 – Affiliate-Zentrale | 0.1.7-dev aktiv gemeldet; hochgeladene Server-ZIP am 06.11. geöffnet und geprüft | **Original-Kopie im Chat vorhanden; GitHub-Original-ZIP noch nicht archiviert; alte 0.1.2-dev aus Current entfernt** |
| Footer-Umzug – Portale | 1.1.1 | **Original-Voll-ZIP im Pluginbüro gesichert und unabhängig wieder geöffnet** |
| Hobby Depot – FAQ Frontend Fix | 1.0.2 | **Original-Voll-ZIP gesichert, unabhängig geprüft** |
| Hobby Depot – Performance Diagnose | 1.1.0 | Aktuelle Voll-ZIP noch nicht im Büro |

Zusätzlich existieren eigenentwickelte, **nicht als aktiv belegte Kandidaten**: HD-002 Text/SEO, HD-008 SEO-Metadaten und HD-008 Anzeigenfüller. Ihre bestehenden Akten bleiben erhalten; die doppelte Kennung HD-008 wird ohne gesicherte Zuordnung nicht geändert.

## Was jetzt tatsächlich gesichert ist

- **HD-003 / 1.50.798:** vollständiges Original-Paket `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip`, unabhängig überprüft.
- **HD-007 / 1.2.17:** vollständiges Original-Paket `ISOLIERTE_PLUGINS/HD-007-HOBBYREGISTER-CORE/CURRENT.zip`, unabhängig überprüft.
- **HD-004 / 1.0.0:** exakte aktuelle Original-ZIP, 3.736 Bytes, vollständiger Bytevergleich erfolgreich.
- **FAQ Frontend Fix / 1.0.2:** exakte aktuelle Original-ZIP, 6.193 Bytes, vollständiger Bytevergleich erfolgreich.
- **HD-009 / 0.1.7-dev:** Original vom Betreiber am 06.11.2026 aus WordPress übergeben; ZIP- und PHP-Syntaxprüfung bestanden. Im Chat bytegleich gesichert. GitHub-Original-ZIP muss weiterhin in das bestehende HD-009-Büro übertragen werden; kein altes 0.1.2-dev als Current. Die fachliche Statusautorität liegt ausschließlich in `../AFFILIATE/CURRENT_STATE.md`.
- **Neu gefunden:** vollständige früher ausgelieferte Originalpakete HD-001 1.14.17 (529.810 Bytes) und HD-006 Bildzentrale 2.7.8 (66.404 Bytes) lokal bytegenau geprüft. Sie sind noch nicht als neue GitHub-ZIP abgelegt, dürfen also nicht als dort gesichert bezeichnet werden.
- **Weitere alte Downloads nachgewiesen:** HD-009 0.1.7-dev, Performance-Diagnose 1.1.0 und Design-Such-Bundle mit Glossar 1.0.25 sind im Library-Inventar vorhanden. Der Rohdatenabruf dieser drei Dateien wird derzeit nicht freigegeben; die Bytes wurden daher nicht auf GitHub übertragen.

**Ausschließlich aktuelle Eigenplugin-Versionen im aktiven Pluginbüro:** Die fünf Fremdplugin-Pakete und die veraltete HD-009 0.1.2-dev-CURRENT.zip samt Manifest sind entfernt. Die Entfernung betrifft ausschließlich GitHub. Weder auf WordPress noch an installierten Fremdplugins wurde etwas geändert. Eine historische Git-Versionsspur bleibt erhalten.

## Einziger nächster Schritt

**Die bereits gefundenen Original-ZIPs der zuletzt bestätigten eigenen Pluginversionen aus den vorhandenen Downloads unverändert in den Campus übertragen; ausschließlich nach Originalhash-/Versions- und ZIP-Prüfung als CURRENT führen.** Fehlende Rohdaten nicht aus älteren Versionen rekonstruieren.


## Nachtrag HD-009 / 06.11.2026

Für **HD-009** ist die originale Version `0.1.7-dev` nun als vollständiger Betreiber-Upload im Chat verfügbar und geprüft (SHA-256 `34c0a9b42c62f71025212bfba3756e48bf4c6ab21fdd000c9894a1ce2bf12cfa`). Die GitHub-Protokollablage ist in `PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/ORIGINAL_SERVER_0.1.7_20261106.md` verknüpft. **Die ZIP ist noch nicht im GitHub-Current gespeichert.** Das fachliche Affiliate-Büro unter `../AFFILIATE/` bleibt einzigartig, während das zentrale Pluginbüro die technische Paketablage führt. Nicht als Doppelbüro zählen.


## HD-009-Harmonisierung (06.11.2026) – Offen für offizielle GitHub-ZIP

Die originale installierte `0.1.7-dev` wurde aus WordPress geliefert und geprüft. Daraus wurde eine **vollständige** lokal geprüfte `0.1.9-dev`-Test-ZIP erstellt (605.968 Bytes; SHA-256 `2e08b52c0f5fd84537683a6a6217a9c62f4ea0025791c0d58a108b9edca90582`). Der **vollständige Quellpatch** und sämtliche Testbelege sind unter `PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/` im Campus gesichert. Die ZIP selbst wurde noch nicht als Github-Blob hochgeladen; **deshalb kein `CURRENT.zip` und keine finale GitHub-Releasefreigabe vortäuschen**. Das eine fachliche Affiliate-Büro bleibt `../AFFILIATE/`; HD009 ist nur die zugehörige technische Pluginakte.
