# Pferdeatelier – eBay-Startschaltfläche dauerhaft gesperrt: bestätigter KISS-Ursachenfix 6.72.313

**Stand 09.11.2026 – TEST-ZIP erstellt und lokal geprüft, kein Live-Release.**

## Echte Ursache anhand des vom Nutzer gezeigten WordPress-Screenshots und der 312-Pluginquelle

Auf `admin.php?page=affiliate-portal-automation` zeigt eBay „Verbunden“, gleichzeitig ist „eBay-Lauf starten“ deaktiviert und die Meldung lautet „Zugang oder eBay-Vertrags-/Datenschutzbestätigung noch unvollständig.“

Die sichtbare WordPress-Seite war **pferde-atelier.de (Produktivseite)**. Die dort tatsächlich installierte Pluginversion ist allein anhand des Screenshots **NICHT** feststellbar.

Die 312-Quellprüfung hat einen eindeutigen Quellfehler gezeigt: Der Startbutton prüfte `$ebay_settings['contract_confirmed']` und `$ebay_settings['privacy_confirmed']`, **beide Schlüssel existieren nicht in `ebay_settings_defaults()`, `ebay_normalize_settings()`, `handle_ebay_save_settings()` oder dem eBay-Fachformular**. Die wirklich gespeicherten und zur eBay-Laufprüfung verwendeten Felder heißen `api_terms_confirmed` und `privacy_policy_confirmed`. Dadurch konnte der Startbutton trotz wahrer Bestätigungen dauerhaft disabled sein.

## Fix

- Version **6.72.313**, basierend auf **6.72.312 Original-308-KISS-Gesamtworkflow**.
- Nur genau **zwei Dateien geändert**: `includes/trait-ppar-automation-suite.php` (korrekte Felder + präzise Blockadeanzeige + Link zur bestehenden eBay-Fachseite) und `pferdeportal-affiliate-router.php` (Versionsheader/Konstante).
- Kein Setzen von Zustimmungen, kein Sicherheits-Bypass. Ohne API-Zugang oder echte Bestätigungen bleibt die Schaltfläche **gesperrt**. Die eigentliche zentrale eBay-Lauffreigabe und Compliance-Regeln bleiben unverändert.
- Keine neue DB-Tabelle, kein neuer Worker, kein Eingriff in andere Provider.

## Nachweise an der fertigen ZIP

- 66/66 ZIP-Dateien, CRC PASS; 23/23 PHP-Dateien Syntax PASS.
- 49/49 fachliche Quellprüfungen PASS.
- 333 explizite Worker-/311-Paket-Simulationschecks PASS.
- 17 HTTP-/Folgeseitenchecks PASS.
- 5 echte Quellfrontend-Filterchecks PASS.
- 6 dynamisch in PHP ausgeführte Gate-Fälle: korrekt entsperrt / Vertragsbestätigung fehlt / Datenschutz fehlt / Zugang fehlt / alte falsche Aliasse / beide fehlen: alle PASS.
- 143 WordPress-ähnliche Hooks erfolgreich registriert.
- SHA256 ZIP: `570726376892ac728fd31451eaa7732a849393b6b0fc8ac7adc8884db9480ff1`.

## Persistente Dateiablage und nächste Prüfung

- **ZIP**: ChatGPT-Dateibibliothek `/pferdeatelier/PLUGINS/QA/Pferdeatelier_Affiliate_6.72.313_TEST.zip`.
- **Protokoll**: `/pferdeatelier/PLUGINS/QA/EBAY_6.72.313_PRUEFPROTOKOLL.txt`.
- **Keine Produktionsfreigabe**: Echte WordPress/MariaDB/eBay-Browse-End-to-End-Liveprüfung fehlt weiterhin.
- Bestehender eBay-Fachpfad auf WordPress: `Affiliate-Zentrale > Anbieter & APIs > eBay > 2. Betriebsprofil und automatische Abrufprofile > Vertragsbestätigung / Datenschutz und Kennzeichnung > eBay-Betriebsprofil speichern`. Zustimmungen **nur bei tatsächlicher Erfüllung** prüfen/setzen. Die Quellkorrektur allein kann den tatsächlich auf der Website installierten alten Pluginstand nicht ändern. Auf der Produktivseite NICHT eigenmächtig das QA-Paket installieren.
- GitHub `CURRENT_RELEASE.json` und offizielle Releases bleiben unverändert. **Das ZIP liegt in Library, nicht als binäre GitHub-Datei**.
