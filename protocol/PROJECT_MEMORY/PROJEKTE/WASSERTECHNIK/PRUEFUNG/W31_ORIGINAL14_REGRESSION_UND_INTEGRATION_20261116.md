# W31 – maximal gebündelte Originalquellprüfung + regressionssichere 81er-Einleseprobe
**16.11.2026 · technisches staging, KEIN Plugin zur Installation, KEIN bezahlter SEO-Lauf.**

## Echte Quellen und belastbare Grenzen
- Das **Original WT001 0.1.4** wurde aus der persönlichen Wassertechnik-Plugin-Büro-Dateiablage mit Originalbytes bezogen. SHA-256 der ZIP: `73b50022aecde2e3d7fd805acfeb94c7c588489abe85383da0905a5fd5736fd4`. Entspricht der bisherigen GitHub-Originalidentität.
- Enthält 6 Dateien: Hauptdatei, W4-218er-SEO-Asset, SEO-Preflight, gespeicherte/fortgesetzte DataForSEO-Abfragen und WordPress-Bestandsinventur. Alle Funktionen am tatsächlich entpackten Original-PHP nachvollzogen.
- **W11 WT001 0.1.7** (7 Hauptbereiche/301-/Import-Szenario) wurde im alten Chat als ZIP beschrieben, **liegt aber weder in den GitHub-Bäumen** (einschließlich W11-Branch) **noch unter den Wassertechnik-ZIPs der verfügbaren persönlichen Dateiablage**. Daher kann keine Bytegleichheit oder vollständige Übernahme des dort vorhandenen Menüs/Migrationsverhaltens behauptet werden.
- Import-/Frontendlauf von 0.1.7 ist hier **nicht** reproduziert; eine Version aus 0.1.4 wäre ein unzulässiger Downgrade, daher wird **keine solche ZIP** bereitgestellt.

## In einem gebündelten technischen Versuch tatsächlich erledigt
1. Original 0.1.4 unverändert entpackt und gesichert. In separater temporärer **nur lokalen** Stagingkopie W30-Read-only-Handoff und eine **einzige additive WP-Untermenü-Vorschau für 81 Kandidaten** eingebunden. Originale DataForSEO-/Bestandsquellen blieben bytegleich.
2. 7 bestehende Original-PHP-Dateien? **Nein:** 6 Originaldateien, davon fünf bytegleich und nur die Haupt-Bootstrap-Datei um **3 Zeilen** ergänzt; **zwei neue** getrennte PHP-Quelldateien in der Stagingkopie. Original-ZIP nicht verändert.
3. Alle PHP-Dateien in der Probe syntaxgeprüft (PHP 8.4): **PASS**. Originale `DataForSEO::build_preflight()` sowie `PaidResearch::planned()` in einer WordPress-Mockumgebung **vorher und nachher** ausgeführt: **218 → 218** Begriffe, **identischer Preflight-Fingerabdruck** `9570a11250f6d3684f52af69239a9af2090a292ba1646dafde76380c471b3462`, gleiche 8/19/1/6/79/105 Alt-Ownergruppen. **Keine** verlorenen Alt-Daten.
4. Neue Vorschau mit synthetischen 81 gültigen Produktzeilen und 90 Rubriken tatsächlich ausgeführt: **81 Tabellenzeilen**. Fehlende Datei führt ausschließlich zu `GESPERRT`, falscher Zielhost und fehlendes Adminrecht wurden blockiert. **0** WordPress-Schreibaufrufe; **0** API-/Kostenaufrufe.
5. Echte W28-Datei mit 81 IDs/81 eindeutigen Keywords/90 Rubriken separat bereits in W30 gegengeprüft; W31-Bootstrap wurde hier mit synthetischen 81 Zeilen getestet, da die originale W28-Datei nicht im lokalen Testverzeichnis vorlag. Diese beiden Testarten ausdrücklich nicht vermischen.

## Ein einziger Integrationsweg, statt weitere Pluginzwischenversionen
- `../PLUGINS/QUELLCODE/W31_class-wassertechnik-seo81-preview.php`: getesteter kleiner Lesebereich für die bestehende WT001-Identität; keine SEO-Entscheidung, kein eigener Importer.
- `../PLUGINS/QUELLCODE/W31_bootstrap_delta_nur_staging.patch`: genau die drei geprüften Bootstrap-Zeilen. **Nur Original-0.1.4-Versuch; nicht blind auf 0.1.7 anwenden.** Der erforderliche W30-Reader liegt bereits unter `../PLUGINS/QUELLCODE/W30_seo_handoff_readonly.php`.
- `W31_WT001_014_GESAMT_REGRESSION.php`: derselbe vollständige Test am originalen und modifizierten Verzeichnis, Vergleich identischer Alt-Fingerabdrücke, 81er-Fall, 0 Writes, 0 API.
- Erst wenn **das Original-ZIP 0.1.7** (mit Menü/Migration) tatsächlich vorliegt, dessen vollständigen PHP-/ZIP-Inhalt mit dem W31-Delta **einmal** zusammenführen, tatsächliche W28-Originaldatei als ein Asset beifügen, die Alt-218er-Fortsetzung inklusive DataForSEO, sieben Menüs, Redirects, Importrollback, neue 81er-Eingabe und Negativfälle in **einem** Testlauf durchgehen. **Erst bei vollständigem PASS** installationsfähige WT001-Update-ZIP bereitstellen.

**Status:** Die W30/W31-Einlese- und Regressionstechnik ist fachlich vorbereitet und am originalen 0.1.4-Code erprobt; Installation / Original-0.1.7-Gesamtabnahme noch nicht möglich. Kein neues Plugin, keine WP-Änderung, keine API-Kosten. Keine weiteren K0/W4/SEO-Entscheidungsrunden eröffnet.
