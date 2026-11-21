# 20.11.2026 – Hab Texterstellung 0.4.31.12: Sichtbarer Versions-/Echtdaten-Hinweis korrigiert

## Live-Screenshot 17:00 MEZ und tatsächlich ausgeliefertes 0.4.31.11-ZIP
Im WordPress-Screenshot steht weiterhin `Texterstellung 0.4.31.10 KISS`; `Echtdaten (api.dataforseo.com)` erscheint nicht im Reiter Recherche. Nutzer bestätigt, dass 0.4.31.11 installiert wurde.

Im tatsächlich gespeicherten ZIP 0.4.31.11 nachgeprüft:
- `texterstellung.php::page()`: feste wörtliche Anzeige `0.4.31.10 KISS`, trotz korrektem Plugin-Header `Version: 0.4.31.11`.
- Echtdaten-Hinweis stand irrtümlich allein unter `handle()`, Action `txe_research_enable`. Diese POST-Aktion leitet sofort weiter; die normale Recherche-Seite gibt den Hinweis nicht aus.
- Der zuvor geprüfte Backend-Anbieter-Fix `PSTE_Plugin::migrateSettings()` auf `environment=production` war dagegen tatsächlich im 0.4.31.11-ZIP enthalten.

## Korrektur v0.4.31.12
- Plugin-Header `Version: 0.4.31.12`; `page()` liest per `get_file_data(__FILE__, ['Version'=>'Version'], 'plugin')` direkt diesen einen Header – keine separate feste Versionszahl mehr im Backend.
- Im *sichtbaren* Recherche-Reiter direkt nach `PSTE_Plugin::settings()` read-only effektiven Modus anzeigen: `Echtdaten (api.dataforseo.com)` genau wenn `environment===production`, sonst `Kein Echtdatenmodus`. Die falsch platzierte POST-Ausgabe entfernt.
- Nur `texterstellung.php` und README geändert, 85/87 Dateien byteidentisch zu 0.4.31.11. Insbesondere Originalprovider, Budget, Recherche, MINI, K0, Import und die zuvor reparierte Wiederaufnahme exakt unverändert.

## Belege
- ZIP `Texterstellung_HAB_UND_BEWAHR_0.4.31.12_ANZEIGE_UND_ECHTDATEN_FIX.zip`, SHA256 `08f7deb71e806dda493ac178bb740b9d2038fb91b0e3ed7bcd64e8cee928f401`.
- Im Hab-Büro unter `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/` gespeichert.
- Prüfbericht und QA unter `/hab-und-bewahr/TEXTERSTELLUNG/PRUEFUNG_ANZEIGE_043112_20261120/`.
- Am endgültig entpackten ZIP tatsächlich ausgeführt: **78/78 PHP-Lints**, **87/87 ZIP-Einträge**, **134/134 originale PHP-Regressionstests** aus neun Programmen.
- Kein echter WordPress-Screenshot der neu installierten v0.4.31.12, keine neue DataForSEO-Anfrage und keine nachgewiesene Live-Kandidatenqualität. Diese Grenzen bleiben offen.

## Betreiber nächster Schritt
Bestehendes Plugin **ersetzen, nicht deinstallieren**; in Recherche prüfen, ob `0.4.31.12 KISS` und `DataForSEO: Echtdaten (api.dataforseo.com)` angezeigt werden. Keine neue kostenpflichtige Recherche vor dieser Prüfung.
