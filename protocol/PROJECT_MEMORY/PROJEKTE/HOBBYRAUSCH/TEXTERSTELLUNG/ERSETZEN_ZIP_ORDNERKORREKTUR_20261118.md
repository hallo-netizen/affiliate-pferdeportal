# Hobbydepot Texterstellung – Ersatz-ZIP Ordnerkorrektur (18.11.2026)

## Verbindliche Nutzerinformation
Die **erste Texterstellungsfassung ist bereits in WordPress installiert**. Im WordPress-Uploader erscheint bei dem bisher bereitgestellten bereinigten ZIP **kein „Ersetzen“-Dialog**. Die Empfehlung, das Plugin zunächst zu löschen, war unbegründet und wird nicht wiederholt.

## Eindeutige technische Ursache im Paketvergleich
- Erster Hobbydepot-WordPress-Installationskandidat: `Texterstellung_Hobbydepot_0.4.24_INSTALLATIONSKANDIDAT.zip` → Wurzelordner `texterstellung-hobbydepot/` → Hauptdatei `texterstellung.php`.
- Bereinigte und bereits lokal getestete ZIP `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_DIAGNOSE_TEST.zip` → Wurzelordner `texterstellung/` → Hauptdatei `texterstellung.php`.
- **Die verschiedenen Pluginordner sind die nachgewiesene Paket-Ursache dafür, dass WordPress diese beiden ZIPs nicht als denselben Installationsort erkennt.** Der WordPress-Serverordner der Nutzerinstallation selbst wurde nicht live ausgelesen.

## Exakt eine Verpackungskorrektur, 0 Quelländerungen
- **Neue Ersatz-ZIP:** `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_DIAGNOSE_ERSETZEN.zip`
- Ablage: `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/`
- Inhalt des ZIPs exakt gleich wie bereits geprüfter Stand `...BEREINIGT_DIAGNOSE_TEST.zip`. **87 von 87 Datei-Inhalten byteidentisch**, nur die Pfade der Zip-Einträge mit Wurzelordner `texterstellung-hobbydepot/` statt `texterstellung/`.
- Hauptdatei jetzt `texterstellung-hobbydepot/texterstellung.php`, entsprechend dem ersten Hobbydepot-Installationskandidaten.
- ZIP-Prüfung: PASS; 78/78 PHP-Lint PASS; keine weiteren Code- oder Konfigurationsänderungen, K0 und Pferdeatelier original unverändert.
- SHA-256 der korrigierten ZIP: `a4356ec3db1263179a8aa12397418ea4efddab138f1abbe80ccfe8417f586a67`, Größe 503446 Bytes.
- Der Name der internen Pluginversion bleibt `0.4.23-hobbydepot-bereinigung.2` (älter als 0.4.24, weil ausdrücklich kein Plugin-Code geändert wurde).

## Nächste Aktion
Neue Ersatz-ZIP in WordPress unter `Plugins → Installieren → Plugin hochladen` auswählen. **Falls die installierte erste Fassung aus dem 0.4.24-Paket mit Pluginordner `texterstellung-hobbydepot` stammt, sollte WordPress jetzt den Ersetzen-Dialog anbieten.** Keine Deinstallation, kein neues Plugin, keine DataForSEO-/K0-Produktion. Die tatsächlich aktuell installierten Live-Bytes waren nicht über einen WordPress-Zugang prüfbar; daher keine unbedingte Live-Ersetzungsbehauptung.

## Schutzgrenzen
Vorhandene K0-Artikelart-/Portalregistrierungs-Sperre bleibt; keine vollständige Live-Produktionsfreigabe. Reine Bereinigung und minimaler bereits dokumentierter Diagnosefehlerfix; kein Umbau, Neubau, Adapter oder Plugin-Neufassung.
