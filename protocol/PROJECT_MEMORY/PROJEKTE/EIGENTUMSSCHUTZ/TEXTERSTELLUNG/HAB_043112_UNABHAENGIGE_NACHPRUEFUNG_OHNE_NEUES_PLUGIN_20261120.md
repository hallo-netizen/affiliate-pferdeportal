# Hab & Bewahr – unabhängige Nachprüfung v0.4.31.12, 20.11.2026

Es wurde **kein neues Plugin gebaut** und **keine kostenpflichtige DataForSEO-Anfrage** durchgeführt.

Direkt geprüftes ausgeliefertes ZIP: `Texterstellung_HAB_UND_BEWAHR_0.4.31.12_ANZEIGE_UND_ECHTDATEN_FIX.zip`, SHA256 `08f7deb71e806dda493ac178bb740b9d2038fb91b0e3ed7bcd64e8cee928f401`. 87 ZIP-Einträge, CRC fehlerfrei, 78/78 PHP-Dateien fehlerfrei unter PHP 8.4.24.

**Original PHP-Tests am erneut entpackten 0.4.31.12-Plugin:** 48/48 vier Recherchewege, 9/9 FINALIZE-Job, 11/11 Queue, 5/5 kombinierte Klasse, 17/17 MINI, 14/14 K0-/Import-Mock, 11/11 PAA-GET, 8/8 PAA-Queue, 11/11 PAA-Restore = **134/134**. Zusätzliche direkte Originalklassen-Tests für `PSTE_Plugin::settings()` und `PSTE_DataForSEO_Client`: **30/30**, inklusive altem gespeichertem `sandbox`-Wert, produktiver Host `https://api.dataforseo.com`, getrenntem Cache, geprüften Endpunkten; Netzwerk bei Test abgefangen. Total 164/164.

**Dreifacher ZIP-Quellvergleich:** Hobbydepot 0.4.24.17 und Hab 0.4.31.12 haben exakt dieselben Bytes für die effektive DataForSEO-Produktionskonfiguration in `class-pste-plugin.php` und dieselbe originale DataForSEO-Client-Klasse. Pferdeatelier 0.4.39 verwendet dieselbe Auswahl zwischen Sandbox/Produktions-Host, erlaubt jedoch noch einen konfigurierbaren Standard `sandbox`; sein tatsächlicher Live-WordPress-Wert wurde nicht ausgelesen. Alle tatsächlich gefundenen Aufrufe des DataForSEO-Clients in Hab geben die Umgebung explizit an, der Recherchejob speichert die Umgebung aus `PSTE_Plugin::settings()`. Ein *neuer* Hab-Job würde daher `production` verwenden. Die alten abgeschlossenen Sandbox-Aufträge bleiben als Nachweis erhalten.

**UI geprüft:** PHP-Plugin-Header `Version: 0.4.31.12`; im Admin-HTML keine feste `0.4.31.10`/`0.4.31.11` mehr; UI-Version wird per `get_file_data(__FILE__)` gelesen. Effektiver Provider-Hinweis steht in `page() → recherche`, nicht nur in einer unsichtbaren POST-Aktion. 0.4.31.10 → 0.4.31.11 hat vier Dateien geändert; 0.4.31.11 → 0.4.31.12 nur Hauptdatei und README. Kein K0-/MINI-/Research-Job-Code in 0.4.31.12 verändert.

**Grenze:** Keine echte WordPress-Ausführung und keine produktive DataForSEO-Antwort in dieser Prüfung; die Behauptung „kompletter Live-Workflow bestanden“ wäre falsch. Die Tests nutzen PHP 8.4.24, der letzte WordPress-Export nennt PHP 8.5.13. Es ist kein weiterer Plugin-Build nötig, solange kein neuer konkreter Fehler nachgewiesen wird.

Nächste Aktion: keine weitere Installation auf Verdacht. Zuerst den installierten Admin-Stand prüfen; erst bei korrektem Versions-/Providerhinweis nach ausdrücklicher Freigabe einen einzigen kostenpflichtigen Echtlauf für **eine** offene Kategorie.
