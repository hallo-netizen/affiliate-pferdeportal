# K0 / Texterstellung: MINI-Übergabe korrigiert – 16.11.2026

## Ist-Stand (nachgeprüft)
- **K0**: Vier unveränderte ursprüngliche Schreibarten Beratung, FAQ, Pflege, Vergleich und neu **Anleitung** als eigenes READY-Regelfach `ARTIKELTYPEN/Anleitung.json`; etablierter Worker/Workflow unverändert. Automatische K0-Tests nach Merge bestanden.
- **Texterstellung auf oliver-beil.de**: Zuletzt tatsächlich nachgewiesene installierte Testversion **0.4.22**. **0.4.23** wurde **lokal erstellt und geprüft, nicht installiert**.
- Nachgewiesener Verwechslungsfehler: Kategorie `wassertroege-fuer-weiden-installation`, Kategorienvariante `Installation`; korrekte **Beitragsart `Anleitung`**. Aus der ursprünglichen Datei `texterstellung-mini-gesamtauftrag.json`, Charge `mini-20261116102235-ef146f6d9cfa`.
- Der ursprüngliche Titel **„Einen sicheren Wassertrog für Pferde selber bauen“**, Keyword **„wassertröge selber bauen“**, genehmigte Absicht und der technische K0-Slot bleiben unverändert.

## Umsetzung: ein bestehendes Plugin, keine neue Produktionsstation
- Vorhandene Texterstellung 0.4.22 direkt weitergeführt zu **0.4.23-kiss-einmalige-artikelart-vor-k0-test.1**. Kein zweites Plugin.
- Nur bereits existierender **CATEGORY**-MINI-Schritt legt die K0-Schreibart einmalig fest; WordPress-Kategorienauszeichnungen werden beim MINI-Export sichtbar als `category_variant` statt `article_type` bezeichnet. Kein nachgelagertes Urteil in K0.
- Lesendes, versionsgebundenes Abbild der **READY**-Beitragsarten aus K0: Beratung, FAQ, Pflege, Vergleich, Anleitung. Nicht bekannte/noch nicht fertige Beitragsarten stoppen ausschließlich diesen MINI-Auftrag, statt willkürlich eine andere Schreibart zu erzeugen. Bei zukünftiger K0-Erweiterung wird die Datenliste synchronisiert, kein weiterer PHP-Worker.
- Spezielle **Korrektur nur für nachweislich fehlerhafte alte Kategorie-Checkpoints**, immer im SELBEN CATEGORY-Entscheidungsbesitzer. Kein Titel-/SEO-Neustart, keine neue Artikelkennung, keine Umdeutung bereits importierter WordPress-Entwürfe. Bereits gültige Entscheidungen bleiben gesperrt; Wiederholung derselben Datei ist folgenlos.
- Ein alter K0-Export mit unzulässigem Typ `Installation` wird nicht nochmals für die Produktion freigegeben.
- Der **bereits vorhandene Diagnoseexport** meldet erkannte MINI-Korrekturen, Typenliste und Original-Entwurfsbindungen; beim MINI-Import werden einzelne Fehlerkennungen protokolliert. Keine neue Diagnose-Station oder Zusatzplugin.
- Der Original-PSERC-Import bleibt unverändert. Die bisherige falsche Diagnose auf `_texterstellung_order_id` wurde in dieser Version durch die ursprünglichen `_pserc_import_article_id` und `_pserc_system4_plan_slot` ersetzt. Keine neue Identität erfunden.

## Lokale Prüfung und Dateien
- PHP 8.4: **78/78** PHP-Dateien ohne Syntaxfehler.
- Vom Original ZIP 0.4.22: **86 Bestandsdateien bewahrt, 0 entfernt, 3 geändert, 2 ergänzt; 88 Dateien**.
- Echtes ursprüngliches MINI-3er-Paket + echter alter fehlerhafter WordPress-K0-Export mit unveränderten IDs im **isolierten PHP-Test** simuliert: alte falsche Kategorie gehalten, richtige Schreibart angenommen, ein einzelner K0-Auftrag erzeugt, zweimaliges Einlesen nicht doppelt, eingefrorener Titel/Keyword/Kategorie/Slot unverändert, WP bereits importierter Entwurf geschützt, fehlerhafte Einzelzeile blockiert ohne Sperre der beiden anderen.
- Nachweis neuer Typ durch **reine Ergänzung des Manifest-Datensatzes** und Ablehnung doppelter Typen, ohne PHP-Codewechsel.
- K0-Tests davor: **22/22 Typregaltests, 176/176 Gesamttests** inklusive simuliertem LanguageTool-PASS und WordPress-Exportformat (kein echter LT-Lauf).

**Ablage**: User Library unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`:
1. `Texterstellung_KISS_0.4.23_TEST_MINI_Anleitung_K0_KISS.zip` (SHA256 `c2b5b8f8921cf783da87a28f525ec81b99888277fbe9929a0f8ffccdd659a3ab`).
2. `texterstellung-mini-category-korrigiert-anleitung.json`.
3. `Texterstellung_KISS_0.4.23_Pruefbericht.json`.

## Verbindlicher nächster Realtest
1. **Nur oliver-beil.de**, nach WordPress-Backup **aktualisieren statt löschen** auf Texterstellung 0.4.23. Produktionsdomain pferde-atelier.de unangetastet.
2. **Einmal** die beigefügte korrigierte `CATEGORY`-Checkpoint-JSON über den bestehenden MINI-Import laden; die anderen beiden Redaktionsbürozeilen behalten ihren einmaligen Entscheidungsstand.
3. Den **originalen K0-Export** der Testseite herunterladen und K0 wie bisher mit dem Auftrag `Anleitung` fahren. Danach echten LanguageTool-6.8-Gate und **WordPress-Testentwurf**, keine Publikation. Erst Live-Erfolg im Diagnoseexport nachgewiesen, nicht behauptet.
4. Kein Nachrecherchieren, kein manuelles Umschreiben technischer IDs, keine weiteren Plugin-Schichten.

**Noch offen:** WordPress-Upgrade und echter K0-/LanguageTool-/WordPress-E2E auf der Testseite. Dieses Protokoll darf nicht als erfolgreiche Live-Abnahme ausgelegt werden.
