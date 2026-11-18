# Hobbydepot Texterstellung – Versionskorrektur 0.4.24.1 (18.11.2026)

**Benutzerbefund:** WordPress-Ersatzanzeige zeigt aktuell installiertes Plugin 0.4.24 und hochgeladenes Plugin 0.4.23-hobbydepot-bereinigung.2 als niedrigere Version.

## Exakt eine Korrektur am bereits gepackten Ersatzplugin
- Vorherige ZIP: `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_DIAGNOSE_ERSETZEN.zip` (korrekter Wurzelordner `texterstellung-hobbydepot/`).
- Neue ZIP: `Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip`; Wurzelverzeichnis weiterhin `texterstellung-hobbydepot/`, Hauptdatei `texterstellung-hobbydepot/texterstellung.php`.
- **Genau eine Inhaltsänderung:** WordPress-Pluginheader `Version: 0.4.23-hobbydepot-bereinigung.2` → `Version: 0.4.24.1` in `texterstellung.php`. Kein anderer Quelltext, keine andere Konfiguration, kein K0-/Recherche-/Importumbau.
- Bytevergleich: 86/87 ZIP-Dateiinhalte identisch; nur die Pluginheader-Hauptdatei abweichend. 87/87 ZIP CRC, 78/78 PHP-Lint, 8/8 JSON PASS. `php version_compare('0.4.24.1','0.4.24','>')` PASS.
- SHA-256 neue ZIP `55eeeb3beabeac2c316617cdb67e3934d51ae75b6d3568e0e3fb0a1147426b36`, 503435 Bytes.

## Ablage
- **Pluginbüro (Zentrale):** `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip`
- **Fachbüro (Archiv):** `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip`

## Konkreter Bedienpfad nach Update (noch NICHT als auf WP installiert behauptet)
1. In bereits geöffnetem WordPress-Dialog hochgeladene niedrigere Version **nicht** bestätigen; stattdessen die **0.4.24.1** ZIP hochladen und vorhandene Version ersetzen.
2. Nach erfolgreichem Upload WordPress **Plugins → Installierte Plugins**: `Texterstellung – Hobbydepot`, `0.4.24.1`, aktiv.
3. Im Backend `Texterstellung → Diagnose → Diagnosebericht für die Fehlersuche herunterladen (JSON)` klicken und JSON im Chat hochladen.
4. **Nicht** jetzt Recherche/DataForSEO/K0-Export/Rückimport starten. Der bestehende K0-Portalstatus ist für Hobbydepot weiterhin `K0_PORTAL_ADAPTER_PENDING`; keine Produktionsfreigabe. Kein Live-Artikelpublishing.

**Status:** ZIP vollständig lokal geprüft und archiviert; WordPress-Liveinstallation und Diagnose-Export vom Nutzer noch offen. Kein Umbau/Neubau.
