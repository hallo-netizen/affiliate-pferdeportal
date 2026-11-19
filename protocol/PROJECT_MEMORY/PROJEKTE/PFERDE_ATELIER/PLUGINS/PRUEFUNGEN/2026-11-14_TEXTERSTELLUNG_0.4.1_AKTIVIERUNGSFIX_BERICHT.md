# Texterstellung 0.4.1-test – Aktivierungsfehler gezielt behoben

Stand: 14.11.2026. **NUR TESTINSTALLATION, keine Livefreigabe.**

## Belegter Originalfehler
- Auf dem vom Nutzer gelieferten Screenshot von 14.11.2026 erscheint unmittelbar bei der Plugin-Aktivierung: `TEXTERSTELLUNG_TEST_ONLY ... In wp-config.php WP_ENVIRONMENT_TYPE=staging setzen.`
- Im originalen installierten Paket `Texterstellung_0.4.0_TEST_INSTALLIEREN.zip`, Datei `texterstellung/texterstellung.php`, verhinderte `TXE_Workshop::activate()` mittels `wp_die()` die Aktivierung, wenn `permitted()` falsche WordPress-Umgebungskennzeichnung erkannte. Der WordPress-Standardwert ist ohne Einstellung `production`. **Ursache ist der eigene Aktivierungscode, nicht WordPress.**

## Gezielte Lösung (0.4.1)
- **Aktivierung grundsätzlich möglich**, selbst wenn `WP_ENVIRONMENT_TYPE` nicht gesetzt ist. Nichts an `wp-config.php` ändern.
- Bis zur **ausdrücklichen Bestätigung im linken Menü `Texterstellung`** bleiben Recherche, K0-Export/Import, Zugangsdatenänderungen und der Diagnose-Download gesperrt; es werden keine Aufträge automatisch gestartet.
- Ein berechtigter Administrator sieht die genaue Website-Adresse, markiert die Checkbox **„Diese WordPress-Installation ist ausschließlich zum Testen bestimmt“** und schaltet dann den Testmodus einmalig frei. Ohne bestätigte Checkbox, gültige Sicherheitsprüfung und Administratorrechte bleibt das Plugin gesperrt.
- Die Bestätigung wird **nur für diese konkrete WordPress-Adresse und Website-ID** gespeichert. Ein Umzug/eine Domainänderung sperrt die Verarbeitung erneut. **Nicht auf Live-Websites freischalten.**
- Links bleibt ein eigenständiger Hauptmenüpunkt **Texterstellung**, mit allen acht bisherigen Arbeitsbereichen. Kein zusätzliches Plugin.
- Datenbanken/Status der alten PSTE-/PSERC-/PPM-Plugins bleiben unangetastet. Bestehende Texterstellung-Aufträge und Formate bleiben unverändert. Kein Frontend-/WP-Core-Umbau.

## Prüfbelege (keine Live-Tests behaupten)
- **37 PASS** im lokalen WordPress-Funktionsnachbau, darunter echte Aktivierungs-Callback-Ausführung bei `production`, Sperre ohne Zustimmung bei `production` und `staging`, Backend-Bestätigungsformular, verweigerte Nicht-Admin-/fehlende Checkbox-/ungültige Sicherheitsanfragen, danach freigegebener Sofortartikel, unverändertes fünfspaltiges K0-Manifest und reservierte Charge, Doppel-Export-Sperre, identischer Wiederdownload, gesperrte Weiterverarbeitung nach Site-Wechsel.
- **6/6 PHP-Syntaxprüfungen PASS**; ZIP-CRC aller Dateien PASS; WordPress-ZIP-Struktur unverändert.
- Gegen Original 0.4.0 **nur drei Dateien verändert:** `texterstellung.php` (Aktivierungsweg + Bestätigung), `includes/class-txe-diagnose.php` (Versionsnummer und ehrlicher Nachweis „Admin bestätigt“), `README-TESTINSTALLATION.txt` (korrekte Anleitung). Alle anderen fünf Paketdateien bitgleich.
- **Keine echte WordPress-Testinstallation durchgeführt;** der Screenshotfehler wurde in der Simulation nachgestellt. Noch nicht die echte externe K0-Produktionskette nachgewiesen.

## Release
- Paket: `Texterstellung_0.4.1_TEST_INSTALLIEREN.zip`
- Größe: 35.228 Bytes
- SHA-256: `f34fe278eaca382ca99c7f537463644dbd1508b9fb4198980e173df59edae280`
- Basis: Original-ZIP `Texterstellung_0.4.0_TEST_INSTALLIEREN.zip`, Quelle unverändert

## Nächster echter Schritt
1. Ausschließlich auf der bereits verwendeten **separaten WordPress-Testinstallation** unter Plugins die Version **0.4.1** hochladen; bei Nachfrage bestehende Plugin-Version ersetzen und aktivieren.
2. **Links „Texterstellung“** öffnen, dort **Adresse prüfen, Checkbox ankreuzen, Testmodus freischalten**. Nicht `wp-config.php` bearbeiten.
3. Danach unter `Texterstellung → Diagnose` den **JSON-Bericht herunterladen** und für weitere Ursachenprüfungen bereitstellen.

**Weitere bekannte Grenze (aus 0.4.0, nicht durch diesen Fix geändert):** Die automatische semantische PSTE-Freigabe ist noch nicht 1:1 übernommen. Das neue Plugin nutzt eine einmalige manuelle oder externe redaktionelle Entscheidung. Echte DataForSEO-/K0-/WordPress-Durchläufe stehen aus.
