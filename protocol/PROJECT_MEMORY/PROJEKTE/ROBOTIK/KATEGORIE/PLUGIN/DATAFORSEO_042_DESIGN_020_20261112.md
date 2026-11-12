# Robotik – DataForSEO 0.4.2 & Mini-Design 0.2.0 (12.11.2026)

**Status:** Lokale Tests erfolgreich. Installation und echtes WP-/DataForSEO-Live-Ergebnis NOCH NICHT BESTÄTIGT.

## Kategorie-Workflow 0.4.2
- Derselbe WordPress-Pluginordner `robotik-kategorie-workflow`, Update auf 0.4.2.
- Die drei vorhandenen PHP-Module für Bestandsaufnahme, Erstimport und Sammelveröffentlichung gegenüber 0.4.1 **byteidentisch**.
- Neue Admin-Seite **Robotik Kategorie → DataForSEO**: nur hier gespeicherter API-Zugang; kostenloser Verbindungstest `GET /v3/appendix/user_data` und kostenloser Gesamt-Keyword-Preflight mit nur einem Knopf.
- Aus dem unveränderten eingebetteten Importprofil: **72 Produktseiten, 89 Beitragskategorien, 161 unterschiedliche Keyword-Kandidaten** mit jeweiligen fachlichen IDs.
- Drei manuell auszulösende, kostenpflichtige DataForSEO-Labs-Methoden: Google Keyword Overview, Keyword Ideas, Keyword Suggestions für `Germany/de`; ausdrückliche Kosten-Checkbox, begrenzte Anfragen, blockierte Dopplung, kein Auto-Start; letzter Ergebnisbericht als JSON.
- PHP-Lint 5/5 PASS, lokale Datentests 17+ PASS, kostenloser Verbindungstest und Antwortparser lokal mit kontrolliertem Mock getestet; ZIP-CRC PASS.
- **Kein reales API-Konto verwendet; keine bezahlten Daten abgefragt; keine Keyword-Suchvolumina behauptet.**
- **Library-Installer:** `/robotik/Konzeptbüro/ROBOTIK_KATEGORIE_WORKFLOW_0.4.2_DATAFORSEO_TEST.zip` 
- SHA256 `c9e60db33dfb0edbfc5d0b1c0dec266d07e95bc7175de7c60f45c51090775075`.

## Testdesign 0.2.0
- Derselbe WordPress-Pluginordner `robotik-strukturdesign`, Update von 0.1.0.
- Header zeigt `ROBOTIK` und **7 Hauptbereiche in derselben Zeile**; darunter schmale Zusatznavigation.
- Mega-Menü mit WordPress-Seiten aus echten Robotik-Import-Markierungen, darunter Gewerbe → Industrie optisch abgesetzt.
- Footer mit derselben realen Kategorieübersicht, sichtbarem Fußbereich, nur grau/weiß/schwarz, keine Bilder.
- Ursache aus Screenshot adressiert: alte Theme-Header/Footer versteckten Teile des eigenen Designs. JavaScript setzt die eigenen Elemente vor dem Ausblenden der Theme-Container als direkte Kinder von `body`. Geprüft auch wenn `wp_body_open` fehlt und wenn `wp_footer` im alten Theme-Footer liegt.
- Headless Chromium bei 1340px und 400px, Menüklick, Escape, Sichtbarkeit Footer und Industrie PASS; PHP-Lint und JS-Syntax PASS. WP-Live-Frontend bislang offen.
- **Library-Installer:** `/robotik/Designbüro/ROBOTIK_STRUKTURDESIGN_0.2.0_TEST.zip`
- SHA256 `80980b7745e0e92d85fcfed22a57eb556f9a83b8bba3238b91e2525a3e8a5bac`.

## Verbindliche Abnahmegrenzen und nächster Schritt
1. Nutzer aktualisiert vorhandenes Kategorie-Plugin 0.4.1 auf **0.4.2**, vorhandenes Designplugin 0.1.0 auf **0.2.0**. Keine Parallelinstallation; keinen Erstimport wiederholen.
2. Frontend: sieben Menüpunkte, Mega-Menü, Footer visuell kontrollieren.
3. In Kategorie-Plugin → DataForSEO Zugang einmal speichern; kostenloser Verbindungstest plus 161er-Preflight erfolgt in einem Schritt. **Kostenpflichtige Recherchen nur bei gesonderter manueller Freigabe.**
4. Erst der echte WP-Live-Test darf Frontend- und API-Gesamt-PASS behaupten.

**Ausführlicher Bericht und Screenshots:** Library `/robotik/Designbüro/ROBOTIK_DATAFORSEO_DESIGN_PRUEFBERICHT_2026-11-12.md`, `ROBOTIK_TESTDESIGN_020_DESKTOP.png`, `ROBOTIK_TESTDESIGN_020_MEGA_GEWERBE.png`, `ROBOTIK_TESTDESIGN_020_MOBIL.png`.

**GitHub binäre CURRENT.zip-Dateien wurden nicht stillschweigend ersetzt**; dieser Eintrag referenziert die geprüften Installer aus der Robotik-Library. Andere Portale unverändert.
