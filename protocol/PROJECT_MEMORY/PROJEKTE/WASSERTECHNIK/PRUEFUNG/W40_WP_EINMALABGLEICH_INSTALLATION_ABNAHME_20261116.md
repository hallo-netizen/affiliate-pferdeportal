# Wassertechnik W40 – sicherer einmaliger WordPress-Gesamtbestandsabgleich vor echtem WT001-Gesamtupdate
**Stand 16.11.2026 · INSTALLIERBARES HILFSPAKET FÜR EINMALIGE BESTANDSLESUNG · kein WT001-Ersatz**

## Was bei der tatsächlichen Quell-/Büroprüfung bestätigt wurde
- Die vorhandene Wassertechnik-Library `/Wassertechnik/Plugin-Büro` wurde direkt geprüft, **nicht aus Protokollen geraten**. Sie enthält Original-ZIPs WT001 **0.1.0, 0.1.1, 0.1.2, 0.1.3, 0.1.4**. WT001-Original 0.1.4 wurde für diese Prüfung als echte ZIP-Datei materialisiert und entpackt (sechs Originaldateien, Ordner `wassertechnik-kategorie-workflow`). Die spätere W11-0.1.7 ist laut PR #785 als damaliger Chat-Anhang erstellt und dokumentiert; eine identische ZIP-Datei konnte **nicht** in diesem Library-Plugin-Büro oder den geprüften GitHub-W11-Änderungen verifiziert werden. Dies ist **keine** Aussage über den installierten Live-WordPress-Stand.
- GitHub PR #817: WT001 0.1.10 mit W39 neuen 81er-DataForSEO-Quellen/SEO-Messwertanzeige und W35-219er-Import, 15/15 SEO-/Provider-/Anzeigetests, 10/10 Import-/Rollback-Tests bestanden, aber weiterhin offline. Kein Ersatz/Upload unbekannter Originalinstallation ohne echten WP-Abgleich.
- Zielvertrag, W27-Fachmaster, bestehende 218 W5-SEO-Owner, 81 neue Kandidaten, 7 Hauptbereiche und Industrie-Fachzugang bleiben unverändert. Keine SEO-Kosten, kein WordPress-Live-Schreiben.

## Der eine reale WordPress-Übergang jetzt
Da Chat/GitHub **keinen WordPress-Admin-Zugriff** besitzen und der Nutzer selbst die Plugins installiert, wurde ein **eigenständiges, ausschließlich lesendes einmaliges Prüfplugin** erstellt:
- Dateiname: `WASSERTECHNIK_WT001_EINMALABGLEICH_1.0.0_INSTALLIEREN.zip`
- SHA256: `4e59f64dd60e3ee44d6c9763238e705981fc6af3bc257f30c5bfb4408f83d4a6`
- Ablage als **echte ZIP-Datei**: `/Wassertechnik/Plugin-Büro/WASSERTECHNIK_WT001_EINMALABGLEICH_1.0.0_INSTALLIEREN.zip`
- Zugehörige echte Quell-/Anleitungsdateien: `/Wassertechnik/Plugin-Büro/Quellcode/W40_wassertechnik-einmaliger-gesamtbestand.php` und `W40_README.txt`.

Dieses Prüfplugin ist **nicht** der neue WT001-Kategorie-Workflow. Es ersetzt, verändert, deaktiviert und aktualisiert WT001 **nicht**. Einmal unter WordPress > Plugins installieren/aktivieren; anschließend **Werkzeuge > Wassertechnik Einmalabgleich** und dort **einen ZIP-Gesamtbericht herunterladen**. Keine weiteren Probeläufe/prüfbezogenen Pluginversionen einführen.

## Inhalt des einzigen Rückgabepakets
`WASSERTECHNIK_WT001_EINMAL_GESAMTABGLEICH.zip` enthält:
1. `gesamtbestand.json`: live installierte WT001-Pluginkennung/Version/Aktivstatus, WordPress-/PHP-Version, die exakten Dateinamen/Hashes, tatsächlich vorhandene WP-Seiten inkl. Entwürfe/Owner/Eltern/URLs, alle WP-Inhaltskategorien/Owner-Zuordnung, Beitragsanzahlen; gespeicherter DataForSEO-Auftragsstatus/Quellenfingerprints und nur **ausgewählte sichere** Keyword-Ergebnisfelder. Keine WP-Benutzer, Artikeltexte, wp-config oder gespeicherten DataForSEO-Zugangsdaten.
2. `installed-wt001/wassertechnik-kategorie-workflow/*`: tatsächlich installierter kompletter WT001-Quell- und zugehöriger Datenbestand innerhalb der vorgegebenen Größen-/Dateitypgrenzen, **nur** aus dem einen WT001-Pluginverzeichnis. Keine fremden Plugins.

Administratorrechte, Nonce, exakter Websitehost `wasser.oliver-beil.de`, eindeutiger installierter WT001-Pluginordner, Pfadgrenzen, Datei-Hashes während Export und Größenlimits müssen stimmen. Bei Widerspruch wird ohne Datei-/WordPress-Änderung abgebrochen. Kein PHP-ZIP-Modul erforderlich, der Export funktioniert mit WordPress/PHP-Bordmitteln.

## Tatsächliche Tests vor Installationsfreigabe
- PHP 8.4-Syntax `No syntax errors`.
- Originale echte WT001-0.1.4-ZIP mit sechs Dateien in einen lokalen WordPress-Mock entpackt: gesamtes WP-Seiten-/Kategorie-/SEO-/Originalquelldateien-Readback PASS.
- Falscher Host und fehlende Adminrechte: jeweils vor jeder Datenausgabe blockiert: PASS.
- ZIP-Export ohne PHP-ZipArchive aus demselben Mock tatsächlich ausgeführt: 8 Archivmitglieder (2 Bericht/README + 6 original WT001), Dateiintegrität/CRC Python-zipfile PASS, exportierte echte 0.1.4-Version und Original-SEO-Daten korrekt, explizite Test-Geheimwerte **nicht** im Bericht: PASS.
- Ausgabepaket für den Nutzer tatsächlich gebaut: genau ein gültiges WordPress-Pluginverzeichnis, Haupt-PHP und README, ZIP-CRC PASS.
- **Nicht** getestet oder behauptet: Live-Installation, WP-Live-Version, tatsächliche Live-Plugin-Parität, 81 neue DataForSEO-Kostenabfragen oder Veröffentlichung.

## Verbindlicher nächster Schritt
Der Nutzer installiert **nur dieses einmalige read-only-Prüfplugin**, lädt den **einen** vollständigen Gesamtbericht als ZIP herunter und gibt genau diesen Bericht hier zurück. Erst **dann** werden Original-WT001-Dateien und WP-Bestand tatsächlich gegen den bereits vollständigen W39-Entwicklungsbau bytegenau und funktional abgeglichen. Darauf folgt **eine** installationsreife WT001-Gesamt-Update-ZIP, keine weiteren Zwischen-/Diagnose-Plugins und keine neuen Kategorien-Entscheidungsstellen. Der spätere aktive SEO-Lauf (81) benötigt ausdrückliche Kostenfreigabe, der eigentliche WP-Import danach eigene Freigabe.

**Status:** W40-Read-only-Einmalplugin tatsächlich freigegeben, ausgabefähig und im Wassertechnik-Pluginbüro abgelegt. Das spätere produktive WT001 0.1.10 bleibt bis Rückgabe des WordPress-Gesamtbestands NICHT INSTALLIEREN.
