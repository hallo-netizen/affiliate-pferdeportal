# Hobbydepot Texterstellung 0.4.24.2 – Diagnose ausgewertet, alte Testoberfläche entfernt

**Datum:** 18.11.2026. **Scope:** kein Umbau, kein Neubau, nur vorhandene Bedienoberfläche bereinigt. Aktueller WordPress-Ersatzpfad bleibt `texterstellung-hobbydepot/texterstellung.php` wie installierte 0.4.24 und 0.4.24.1.

## Tatsächlich vorliegende Diagnose
Original: `texterstellung-diagnose-20261118-165236.json` (Erzeugung 16:52:36 UTC, Plugin 0.4.24.1), im Hobbydepot-Dateienbüro archiviert.
- Website `www.hobby-depot.de`, `wp_environment=production`.
- Gleichzeitig `test_mode_admin_confirmed_for_this_site=true`. Dies ist nur der alte gespeicherte Eintrag und keine nachgewiesene Test-WordPress-Instanz. **Die neue Version verändert diesen Eintrag und seine Sicherheitsfunktion nicht.**
- `order_count=0`, `research_count=0`, `saved_state=false`, keine letzten Jobs/Events/Fehler.
- DataForSEO Login/Passwort: keine gespeicherten und keine per Konstanten bereitgestellten Zugangsdaten.
- K0-Artikelarten: `status=BLOCKED`, `reason_code=K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`, `article_types=[]`. Daher **keine K0-Produktionsfreigabe**.

## Exakte minimalinvasive Änderung
**Ausgangs-ZIP** `Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip`; **neue ZIP** `Texterstellung_Hobbydepot_0.4.24.2_TESTOBERFLAECHE_BEREINIGT.zip`, SHA256 `63812431443f8de47a04cbcf3879e3b5fb524c88fb21541562eb28c159ee9293`, **503056 Bytes**.
- **86/87 Dateien bytegenau identisch**, **nur** `texterstellung-hobbydepot/texterstellung.php` geändert.
- Pluginheader-Version auf **0.4.24.2**, gleiche WordPress-Paketidentität (0.4.24.2 höher als 0.4.24.1).
- Altüberschrift `0.4.20 KISS – TEST`, Test-Freischaltmaske mit Haken und Button, Testmodus-Warnbox bei bestätigter Installation und unnötige Testbenennungen im sichtbaren Menü/Text entfernt.
- Bei **nicht bestätigter** Installation stattdessen nur sachliche Sperrmeldung; keine Möglichkeit der ungeprüften Freischaltung über die bereinigte Übersicht. Bestehender Code für Site-Freigabe und die Start-/Bearbeitungsprüfung nicht verändert. **Kein neuer Workflow, keine neuen PHP-Dateien, Methoden oder Hooks.**
- Recherche, MINI-Entscheidungen, Kategoriezuordnung, K0-Regeln, System4-/PSERC-Rückimport und Publish-Entwurfsschutz ausdrücklich nicht angefasst. Der technische Test-Gate bleibt im Quellcode; entfernt ist die **Bedienoberfläche**, nicht die ganze technische Freigabe.

## Prüfung direkt am ZIP
- **87/87 ZIP-CRC**, **78/78 PHP-Lint**, **8/8 JSON** PASS.
- **3/3 lokale PHP-WP-Bootstraps** (Freigabe fehlt, Freigabe vorhanden, Altplugin-Kollision).
- **25/25 bisherige Funktions-/Backend-Prüfungen**, **5/5 Original-Importfälle**, **13/13 zusätzliche UI- und Sperrentests** = insgesamt **46/46 lokal PASS**.
- Entwurfsfiltertest: importierte Posts bleiben Entwürfe; unabhängige Posts dürfen veröffentlicht werden.
- **Kein WordPress-Echtlauf mit neuer ZIP und keine DataForSEO-/K0-Produktionsprobe.** Lokal geprüfte Funktionen nicht als Live-Abnahme ausgeben.

## Archiv und Maßgeblichkeit
- **Aktuelle ZIP im echten zentralen Hobbydepot-Pluginbüro:** `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.2_TESTOBERFLAECHE_BEREINIGT.zip`.
- Fachbüro: `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/Texterstellung_Hobbydepot_0.4.24.2_TESTOBERFLAECHE_BEREINIGT.zip`.
- Eigener Büro-CURRENT: `/Hobby Depot/Plugin-Büro/Texterstellung-CURRENT.md` aktualisiert, altes 0.4.24.1 archiviert. Globale `/Hobby Depot/Plugin-Büro/CURRENT.md` für andere Plugins nicht überschrieben.
- Prüfbeleg `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/HOBBYDEPOT_TEXTERSTELLUNG_04242_DIAGNOSE_UND_UI_PRUEFBERICHT.{md,json}`, Original-JSON dort archiviert.

## Nächster konkreter Schritt für Nutzer
1. WordPress → Plugins → Installieren → Plugin hochladen → **0.4.24.2** → vorhandenes Plugin **ersetzen**, nicht löschen.
2. `Texterstellung → Übersicht`: reine Überschrift „Texterstellung“, **keine Testbestätigung**, die sechs bisherigen Menübereiche weiterhin vorhanden.
3. Noch **keine bezahlte DataForSEO-Recherche und keine K0-Produktion** starten. Diagnose liegt bereits vollständig vor, **kein weiterer JSON-Export nötig**. K0-Typfreigabe und Anbieter-Zugangsdaten sind nicht Bestandteil dieses begrenzten UI-Releases.
