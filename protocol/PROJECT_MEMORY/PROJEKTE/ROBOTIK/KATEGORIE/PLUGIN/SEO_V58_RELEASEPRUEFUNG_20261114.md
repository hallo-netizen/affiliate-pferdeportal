# Robotik V58 – Bestehendes Kategorie-Plugin 0.4.5: gezielte sichere Wiederaufnahme nach DataForSEO 50000
Datum: 14.11.2026 – ausschließlich TEST; keine WordPress-Liveänderung, kein API-Aufruf durch Assistent.

## Belegte Ursache und Grenze
WP-Admin 0.4.4: kostenloser DataForSEO-Test PASS, 437 Kandidaten vorhanden, Sammellauf bei BLOCKED_UNCERTAIN / 0 von 38, erster Auftrag `keyword_overview/live`, HTTP 500. Das DataForSEO-Dashboard zeigt 14.11.2026 10:49:20 lokaler Nutzerzeit den Anbieterstatus 50000 „Internal Error“. Der originale Auftrag mit 437 Begriffen liegt vor; keine Leerbegriffe/Dubletten; DataForSEO erlaubt bis zu 700. Anbieter empfiehlt für einen einzelnen 50000-Fehler eine Wiederholung mit identischem Payload. Die genaue interne Ursache und die Gebühren des ersten Aufrufs sind nicht belegt.

Belege Anbieter:
- https://docs.dataforseo.com/v3/appendix/errors/
- https://dataforseo.com/help-center/best-practices-live-endpoints-in-dataforseo-api

## Änderungsumfang
Aus dem originalen 0.4.4-Installer nur geändert:
- `robotik-kategorie-workflow.php`: Versionsnummer 0.4.5
- `includes/class-robotik-dataforseo.php`: ein **einmaliges, vom Administrator ausdrücklich kostenbestätigtes** Wiederaufnahmeformular, neue Aktion und Sperrbedingung bei bekanntem HTTP-500-Abbruch **des ersten von 38 Aufträgen**; setzt nicht den gesamten Lauf zurück. Nur für `BLOCKED_UNCERTAIN`, `index=0`, `total=38`, `last_started` Auftrag 0 `overview`, gespeicherte Fehlermeldung `DataForSEO: HTTP 500`, noch keine Wiederholung. Prüft unveränderten SEO-Plan sowie fehlende Resultate und aktive Sperre. Nach expliziter Zustimmung setzt genau einmal auf `RUNNING` zurück, bewahrt ursprüngliche Run-ID, 38er-Aufträge und Budget, protokolliert Vorgang. Bei weiterem Fehler stoppt die Wiederholung dauerhaft. Browser führt die bestehenden 38 Aufgaben dann wie zuvor nach einmaligem Klick weiter.
- `README.txt`: Dokumentation.

Die vier Dateien für WP-Bestandsaufnahme, Erstimport, Veröffentlichung und alte Importplan-Daten sind **byte-identisch**; ebenso das vollständige V52-SEO-Manifest. Keine neue Datenbanktabelle, kein zweites Plugin, kein automatischer Retry, keine WordPress-/Frontendänderung.

## Prüfungen
- PHP-Syntaxprüfung: 5/5 PASS
- ZIP CRC: PASS; identische 8 Pfade wie 0.4.4; nur 3 exakt benannte Dateien geändert
- PHP-WordPress-Mock: 7/7 Sperrbedingungen der Wiederholbarkeit; sechs getrennte vollständige Admin-Aktions-Szenarien PASS (gültiger Lauf, fehlende Freigabe, aktive Sperre, abgelaufene Sperre, geänderter SEO-Plan, bereits vorhandene Resultate). Keine echte Anbieteranfrage und kein echtes WordPress zur Testzeit.
- Einziger Rückkanal: Wenn `BLOCKED_UNCERTAIN 0/38` im bisherigen WordPress, erscheint nach Installation derselben Pluginidentität 0.4.5 die neue Option `Einmalige Wiederaufnahme des bisherigen Laufs` inklusive **neuer ausdrücklicher Kostenbestätigung**. Keine anderen Knöpfe anklicken. Anbieter-Kosten alter Versuch unbekannt; erneuter Versuch könnte eine weitere Abbuchung verursachen. Der vorhandene Budgetrahmen schützt nur weitere vom Plugin bekannte Kosten, nicht die unbestätigte Altbuchung.
- Installer ZIP: 55.146 Bytes; SHA256 `3dc302127eba6150cafb920304a12159cc494b13beca1fa5d64c9c619ed5f1fe`.

## Offene Grenze
Das ist ein **einmaliger fehlerbezogener Wiederherstellungsweg**, keine Behauptung, der Anbieter habe die Störung bereits behoben. Nutzer entscheidet über eventuelle erneute Kosten. Weiterer HTTP 500 bleibt BLOCKED und verlangt eine Supportklärung, keine erneute Änderung des Kategoriekonzepts.