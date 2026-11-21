# Hab & Bewahr – 21.11.2026 – Originalablauf vor kostenloser Bestandsprüfung korrekt verbinden (0.4.31.17)

**Status: ausschließlich lokal geprüfter Installationskandidat, keine Live-Abnahme. K0 vollständig außerhalb des Auftrags und unangetastet.**

## Echte Fehlerkette
Live 0.4.31.16: zweimal Abbruch der kostenlosen gespeicherten Keyword-Nachprüfung mit `PSTE_PRODUCTION_WAVE_CONTEXT_COMPLETE_REQUIRED`. Die 192 gespeicherten Abholbox-Rohbegriffe und 163 Kandidaten wurden nicht neu bewertet. Das ursprüngliche Testskript täuschte `PSTE_Context_Refresh::status=COMPLETE` vor und übersprang so die konkrete Voraussetzung.
Vergleich mit den echten Originaldateien: Hobbydepot führt bei Setup zusätzlich die originale `PSTE_Context_Refresh::start/processBatch`-Vorbereitung bis `COMPLETE` aus, Hab beendete Setup dagegen schon nach der Plugin-Bereitschaft. Pferdeatelier startet diese Vorbereitung im Original-Baseline-Pfad. Originalklasse `class-pste-context-refresh.php` ist zwischen Hobby und Hab bytegleich. Weitere historische Fehler aus den echten Hobbydepot-Berichten abgeglichen: kein Portalname in Suchseeds; Provider/PAA-Auftrag anhand gespeicherter ID lesen statt erneut kostenpflichtig POST; keine Doppelaufträge; fehlende Originaldateien; zuerst Original-Voraussetzungen, danach kostenlose Neuprüfung.

## Reparatur in bestehendem Originalablauf, KISS
0.4.31.17 führt im bereits vorhandenen `TXE_Workshop::safeMigrationAjax` nach dem normalen Setup die bereits existierenden Originalfunktionen für Kontextvorbereitung aus, mit signierter UUID, Wiederaufnahme und Statuskontrolle. Die vorhandene Rechercheoberfläche startet bei kostenloser Nachprüfung erst dieses Original-Setup und sendet den bisherigen Original-Formularauftrag genau einmal, **nur bei tatsächlichem COMPLETE**. Original-Queue, Forschungsfunktionen, DataForSEO 4 Methoden, Portalrelevanz, MINI und K0 unverändert. Nur `texterstellung.php` und README geändert; 85/87 Dateien bitidentisch. Keine neuen Tabellen, kein neuer Entscheider, kein Zusatzplugin.

## Ausgeführter **Original-PHP**-Simulationsbeweis
- Ursprünglicher v0.4.31.16-Start ohne COMPLETE reproduziert exakten Live-STOP.
- Aus der finalen 0.4.31.17 PHP-Hauptdatei wird die tatsächliche AJAX-Funktion übernommen und zusammen mit den echten originalen PHP-Klassen `PSTE_Context_Refresh` und `PSTE_Breadth_Research_Queue` ausgeführt. **Nicht** bloß COMPLETE vorgegeben.
- Ausgang `NOT_STARTED`: 60 echte Schritte inklusive Inventar-/Kontext-/Freigabephasen und Verarbeitung von 163 **synthetischen isolierten** WP-Testdatensätzen, finaler vom Original gespeicherter Status `COMPLETE`. Erst danach `startExistingOnly` aus dem Original; 163er freie Test-Queue erfolgreich angelegt und signiert aus dem isolierten Speicher zurückgelesen, 0 Anbieteraufrufe, 0 Kosten.
- 5 Original-Fehlerfälle `ORIGINAL_STOP`, `BLOCKED`, `WRONG_UUID`, `RESUME`, `ALREADY_COMPLETE`: jeweils bestanden; kein falsches Überspringen von Sperren, keine Dubletten.
- Echte extrahierte Browser-JavaScript-Steuerung mit 3 Fällen geprüft: freigegeben -> 1 Originalsubmit, gesperrt -> kein Submit, kein Fortschritt -> Stop ohne Submit.
- 19/19 Regression-/Integrationsgruppen bestanden (einschließlich vorhandener originalen vier Recherchewege, bestehender Offline-Replays über 192 Abholbox-RAW und 100 Kamera-RAW, Original-Recherche- und MINI-Vorlagen); 78/78 PHP-Lint, 87/87 ZIP-CRC und komplettes neues Auspacken/Bytevergleich, SHA256 final `aaf8f86f2b5ca4d4b315e2465fc50c537df971ef0b19193844696512987f77c6`.

## Wichtige Grenze
WordPress-Live-Datenbank und vollständige 2128er Kategorie-Livemomentaufnahme stehen nicht in isolierter Entwicklungsumgebung zur Verfügung. Die 163 beim Test vorbereiteten Datensätze waren **Testdaten**, nicht der echte WordPress-Bestand; der anschließende vollständige echte Bestandslauf und MINI auf WordPress ist **nicht** nachgewiesen. Frühere gesamte Abnahme-Aussagen werden ausdrücklich nicht wiederholt. Keine vorgebliche Live-Erfolgsmeldung.

## Ablage und weiterer Schritt
ZIP `Hab_Bewahr_0.4.31.17_LOKAL_GEPRUEFTER_KANDIDAT.zip` im Hab-Büro unter `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/`; vollständiger Bericht, QA-JSON, echte Original-PHP-Replays und UI-Test unter `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_ORIGINAL_KONTEXT_043117_20261121/`. Erst nach WP-Backup und Ersetzung des bestehenden Plugins (nicht deinstallieren) ist eine **kostenlose** Live-Bestandsprüfung sinnvoll; ausdrücklich **keine neue bezahlte Recherche**. K0 nicht ausführen.