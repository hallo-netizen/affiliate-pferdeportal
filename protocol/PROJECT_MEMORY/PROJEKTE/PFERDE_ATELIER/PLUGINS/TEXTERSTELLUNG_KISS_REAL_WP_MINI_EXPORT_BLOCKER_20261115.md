# Pferdeatelier – echter WordPress-MINI-Exportabbruch (15.11.2026)

**Nur isolierte WordPress-Testinstallation. KEINE Live- oder Produktionsfreigabe.**

## Tatsächlicher Beleg aus Benutzerdiagnose, keine Spekulation
- Die echte WP-Diagnose von oliver-beil.de, erstellt 15.11.2026 um 08:45:15 UTC, zeigt ACTION_FAILED für txe_seo_export um 08:42:13 UTC: MINI_CURRENT_PARKHOUSE_INCOMPLETE, texterstellung.php Zeile 828. Der ZIP-/JSON-Download wurde nicht gestartet.
- Vor Abbruch wurde bereits das Original-WordPress-Regal per einmaligem Originalquellenabgleich aktualisiert: 61 Aufträge, 1 FREI und 60 METADATEN_OFFEN; 20 recherchierte Begriffe. Keine K0-Charge und keine Entwurfsimporte. Bestehende 61 Aufträge dürfen nicht neu entschieden oder gelöscht werden.
- Die angezeigte Pluginversion 0.4.1-test ist in der 0.4.6-Diagnosequelle wörtlich hartcodiert; der 0.4.6-Hauptdatei-Header lautet tatsächlich 0.4.6-kiss-test.1. Die JSON-Version war deshalb eine falsche Anzeige, keine Installationsdiagnose.
- Die eigentliche unvollständige Originalquelle kann aus dem bisherigen Report NICHT bestimmt werden: Der Original-PSTE-Reader liefert status/reason/sources, der Texterstellungs-Export warf nur einen generischen Fehler und verwarf die konkreten Originalbefunde. Es wäre unzulässig, WordPress, PSTE, Editorial Plan, PSERC oder PPM ohne Beweis zu beschuldigen oder die Vollständigkeitssperre zu entfernen.

## Genaue Korrektur ohne neuen Worker/Plan/Gate
Ein vollständiges 0.4.7-kiss-test.1 Test-ZIP wurde aus der nachweislich aktuellen 0.4.6-ZIP erstellt. Genau ZWEI vorhandene Dateien geändert:
1. Texterstellung-Hauptdatei: Die bereits einmalige Original-Parkhaus-Lesung protokolliert beim vorhandenen gesperrten Export genau den vom Original-Reader schon ausgegebenen technischen Grund und Status der Quellbestände. Kein neuer Read, keine Freigabe, keine inhaltliche Entscheidung, Aufträge unangetastet.
2. Bestehende Diagnoseklasse: Versionsnummer wird aus dem Plugin-Kopf gelesen, nicht fest als 0.4.1-test ausgegeben.

Private Büro-Ablage: /pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung_KISS_0.4.7_TEST_QUELLDIAGNOSE.zip
SHA256: 0676a33816839741aa59150b3c9f871c5ba15c007fc6439f810cd20e6d12fccd. Original 0.4.6 SHA256: 42b2832ab030cbdbf2e88dfb0fed744e7856f76b6bbcba62d910bff7ef7f681b.
ZIP: 173 Einträge, 117/117 PHP-Syntaxprüfungen, ZIP-CRC PASS; alle übrigen 171 Datei-Bytes identisch. QA-Bericht, exakter Patch und Beleg im selben vorhandenen Büro gespeichert; ZIP aus Büro erneut lesbar. Separater PHP-Test des vorhandenen Diagnoseschreibers bestätigt: Originalgrund + problematische Quelle erhalten, Regal unverändert, Versionsheader korrekt.

## Nächster echter Schritt
Auf der isolierten Testseite die vollständige 0.4.7-ZIP an Stelle der bisherigen 0.4.6 installieren (bestehendes Plugin ERSETZEN, niemals löschen). Genau EINMAL MINI-Gesamtauftrag herunterladen anklicken. Falls weiterhin kein Download, auf Diagnose klicken und die Diagnose-JSON exportieren. Das neue Ereignis MINI_ORIGINAL_SOURCE_BLOCKED benennt die bisher fehlende technische Originalursache. DANN die tatsächliche Ursache reparieren, statt Sperren zu umgehen. Kein K0 und keine Live-Installation. production_release_allowed=false.
