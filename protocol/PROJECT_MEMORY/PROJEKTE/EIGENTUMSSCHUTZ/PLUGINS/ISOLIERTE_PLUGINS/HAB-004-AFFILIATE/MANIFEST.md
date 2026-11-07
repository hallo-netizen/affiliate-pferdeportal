# HAB-004 – Einzige aktuelle WordPress-Affiliate-ZIP

Stand: 07.11.2026.

**HAB-004 Affiliate-Zentrale 0.1.4-rc7**, vollständige einzige `CURRENT.zip`: **616209 Bytes, 28 Dateien**, ZIP-SHA256 `08725e5cf9d18654345b4b18b9f3c63ade54ce7a6da932d9768bc2b9867b1d6e`, GitHub-Binär-Blob `3df1bd941aa051f6706a66fd857a8745d0209420`. Gegen RC6 25/28 Dateien byteidentisch; nur die vorhandene Amazon-Datei, der bisherige Hab-Router und `readme.txt` geändert. Keine Fremdportale.

**Nach Prüfung des wirklichen RC6-Codes:** Die vorhandene Artikelerkennung und Werbeplan-Neuberechnung bei Speicherung blieb unangetastet. Neu nutzt **derselbe DataForSEO-Worker** künftig auch veröffentlichte Artikel, wenn die direkte Hab-Produktkategorie wirklich passt und der Artikel-Titel die konkrete Produktfamilie nennt. Bewusste Ausschlüsse: Entwürfe, allgemeine Ratgeber ohne explizites Produkt, Werbesperren, falsche Produktfamilien. Änderungen an Titel/Kategorie machen alte Treffer sofort ungültig. Alle aktuellen Produkt-/Bannerkampagnen behalten Vorrang; bei fehlenden passenden Produkten nur klar gekennzeichneter Amazon-Suchlink, nach verifiziertem API-Ergebnis reale Amazon-Textlinks. Kein zweiter Worker, keine neue API-Suche beim Beitragsspeichern und keine zusätzliche Datenbank; fünf bezahlte DataForSEO-Aufträge/UTC-Tag bleiben.

**Tests:** Alle 25 PHP-Dateien ohne Syntaxfehler, ZIP-CRC PASS, 23+16+23+34 lokale Assertions PASS (96 nicht notwendigerweise unabhängige Fälle). Echte Artikel-Produktslot-Funktion aus Original-Hauptdatei mit globaler Sperre, bestehender Werbung und Hybrid-/Legacy-Modus geprüft. **Kein** WordPress-/DataForSEO-/echter Produktiv-End-to-End-Test; Portal enthält derzeit noch keine echten Beiträge. RC7 bleibt ein geprüftes Upgrade-Paket, nicht produktiv abgenommen.

**Nächster Schritt:** Auf ausschließlich `hab-und-bewahr.de` das bereits vorhandene HAB-004 mit der RC7-ZIP kontrolliert aktualisieren. Amazon-Partner-ID und gespeicherte Zugangsdaten bleiben über dieselben bestehenden WordPress-Optionen erhalten, deren tatsächliches Fortbestehen nach dem Upgrade zu prüfen ist. Beim nächsten real veröffentlichten, korrekt kategorisierten Produktbeitrag erfolgt die themenbezogene Suche über den bestehenden WP-Cron. Keine manuellen Amazon-Einzelkampagnen, keine neuen Plugins. HAB-001/002/003, Pferdeatelier, Hobbydepot und K0 unverändert.

Quellvergleich, reproduzierbarer PHP-Gegentest und ausführliche Prüfung: `../../../AFFILIATE/IMPLEMENTIERUNG_RC7/RC6_TO_RC7.patch`, `test_hab_rc7.php`, `TESTRESULTS.md`. Vorgängerversion RC6 bleibt in der Git-Historie zur Verfügung.
