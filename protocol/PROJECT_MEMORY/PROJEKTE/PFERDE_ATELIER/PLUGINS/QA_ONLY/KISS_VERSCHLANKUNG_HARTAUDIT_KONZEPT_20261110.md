# Pferdeatelier PSTE/PSERC – KISS-Verschlankung, Hartprüfung und Test→Live-Fahrplan
**Stand:** 10.11.2026, isolierte QA; **kein Plugin installiert oder Live verändert**, K0 nicht verändert.

## Arbeitsgrundsatz
Nur nachweislich überflüssige Abläufe/Anzeige oder codeinterne Nicht-Funktionen entfernen. Bestehende WordPress-Actions, AJAX, Cron, GSC, Recherche, Historie, Themen-/Kategoriearbeit, Daten, K0-Export, Rückimport und Sicherheitssperren nicht abschalten. Keine neue Architektur, Tabellen, Dispatcher, Owner oder Worker; keine Migration aus einer Codebereinigung heraus.

## Physisch geprüfte Ausgangsdateien
- Original aus privatem Pluginbüro PSTE **0.57.144.32**, 121 Dateipfade, 83 PHP-Dateien, 23.926 PHP-Zeilen, 3.268.400 ungepackte Bytes.
- PSERC **0.28.60**, 63 Dateipfade, 43 PHP-Dateien, 5.424 PHP-Zeilen, 1.448.488 ungepackte Bytes.
- Echte WordPress-TEST-K0-Datei (3 Artikel) gegen ursprünglichen PSERC- und K0-Format-/Hashvertrag abgenommen; **keine Artikelproduktion, kein Live-Test**.
- Auf Live laut Betreiber: PSTE **0.57.120**, PSERC **0.28.43**. Originalversionen .120/.43 und aktueller LIVE-Datenbankstand nicht als Originalbytequellen vorhanden; daher **kein unverprobter Direktupgrade**.

## Bestätigte Navigations- und Funktionslage
- PSTE definiert exakt **vier** WP-Unterseiten: Produktion, Themenprüfung, Datenquellen, Einstellungen. Dieselben vier werden ein zweites Mal als **In-Page-Tab-Leiste** ausgegeben. Der einzige Aufrufer ist `PSTE_Admin::render()`, die Tab-Routine ist `private`. Die Seiten-Callbacks bleiben separat registriert. Das vorhandene Vertragsdokument `contracts/admin-navigation-v1.json` nennt beide Leisten, wird von PSTE/PSERC zur Laufzeit aber nirgends eingelesen; ein UI-Wechsel muss dort entsprechend kommentiert werden.
- PSERC erzeugt das erforderliche Untermenü „SEO Redaktionsplan“ bei `admin_menu` **Priorität 1000**. PSTE versucht bei **999**, diesen Menüpunkt zu entfernen: der Aufruf ist für genau dieses Menü **wirkungslos**. Eine simple Prioritätserhöhung wäre **schädlich**, weil sie den tatsächlich genutzten Redaktionsplan unsichtbar machen würde.
- PSERC-Speicherwartung wird bereits bei Priorität 41 hinzugefügt und bei 999 aus dem Menü entfernt; registrierte Wartungs-AJAX-Funktionen bleiben. **Diese Entfernung wird nicht verändert**.
- Zwei K0-Ausgabeaktionen bleiben vorhanden: PSTE `pste_export_planning_topics` und PSERC `pserc_export_live_preview`; beide benutzen den vorhandenen PSERC-Snapshot/Batch statt eines neuen Exporters. Die Bedienwege dürfen zusammengefasst werden, **ohne** ihre Rückwärtskompatibilität zu löschen.
- `PSTE_Plugin::maybeMigrate` und `maybeRunOwnAdminMaintenance` sind im installierbaren PSTE .32 **öffentliche leere Kompatibilitätsmethoden**, ohne interne Aufrufe in PSTE/PSERC. **NICHT gelöscht**, solange externe dynamische Referenzen auf der echten LIVE-Seite nicht geprüft sind. Gleiches gilt für alten MINI-Legacy-Rebind, Speicherwartung und PSERC-Legacy-Gates (nachweislich registriert/verwendet).
- PSERC `System4_Import::renderPanel()` ist schon unter „Nach K0: ... importieren“ eingeklappt: **nicht nochmals umbauen**.
- PSTE `cleanupRemovedLiveWorkflow()` in späterer manueller Migration archiviert sechs ältere Rechercheoptionen und **löscht anschließend deren ursprüngliche Schlüssel**. Für Live gilt ausdrücklich: Ohne echten Options-/Archiv-/Reader-Vergleich keine Migration oder Alt-Datenbereinigung. Aktivierungsprüfung allein beweist nicht die Upgrade-Sicherheit.

## Erste echte minimal-invasive Verschlankung als QA – KEIN Release
Auf isolierter unverpackter Kopie von PSTE .32:
1. **Doppelte Tab-Leiste entfernt**: exakt eine Anzeigezeile in `PSTE_Admin::render`, ihre nur intern genutzte private `tabs`-Methode und ausschließlich deren CSS-Selektor entfernt. **Alle vier ursprünglichen WordPress-Unterseiten unverändert**.
2. **Wirkungslosen** `remove_submenu_page(...,'portal-seo-editorial-plan-compiler')`-Aufruf entfernt. Priorität **999** und effektive Entfernung der Speicherwartung bleiben erhalten; PSERC Hauptmenü bleibt erreichbar.
3. Im vorhandenen `admin-navigation-v1.json` NUR die Präsentationsregel ergänzt; vorhandene bisherigen Felder unverändert gelassen, damit das Dokument den UI-Wechsel offenlegt.

**Exakter Differenzbeweis:** 121/121 Dateipfade identisch, **119 Dateien byteidentisch**, nur `includes/class-pste-admin.php` und `contracts/admin-navigation-v1.json` verändert. PHP-Code -517 Byte, Gesamtpaket ungepackt -242 Byte (kein Fake-"riesiges" Schrumpfen).
**Echte Menu-PHP-Simulation** der **unveränderten Originalklassen** gegen QA-Admin: **5/5 identische Menüziel-Slugs und Labels**, inklusive PSERC Redaktionsplan; Speicherwartung wie bisher versteckt.
**Registrierung vor/nach (exakte Text-/Listenparität):** 34 gemappte Admin-POST-Aktionen, 23 AJAX-Zuordnungen, 29 `add_action`-Aufrufe, 1 `add_filter`, 57 Admin-Berechtigungsaufrufe. Alle gleich. **83/83 PHP-Syntaxchecks PASS**. Die echte ursprüngliche Drei-Themen-Datei erfüllt weiter den **unveränderten K0-SHA256-Eingangsvertrag**, und PSERC-Quellen wurden nicht verändert.

QA-Diff lokal: `/mnt/data/kiss_audit_20261110/KISS_NAVIGATION_ONLY_QA.patch`. Noch keine installierbare neue Versionsnummer und kein vollständiger WordPress-Test, weil **zunächst das Konzept** angefordert wurde.

## Behalten, weil nicht redundant
- Eingebundenes MINI-System (externes SEO-Ergebnis / Titel / Kategorie / Planweitergabe) und ursprüngliche Legacy-Import-/Aufräumaktionen: echte WordPress-Hooks bzw. gespeicherte Inhalte können sie benötigen.
- Aktive GSC-Anbindung, DataForSEO, Thema-Pool, Research-Queue, Context-Index, Kategorien-/Artikeltypen, PPM-Slot, K0-V2-Export und finaler System4-Rückimport.
- PSERC-Frische-/Sicherheitsprüfungen, Snapshots, Archiv/Fallback-Generationen, Speicherwartung, interner Hardlock; niemals nur wegen geringer Nutzungsfrequenz löschen.
- Alle öffentlichen leeren Kompatibilitätsmethoden bis zum Live-Referenzbeweis.

## Abfolge: zielgerichtet, nicht zehnmal dieselben Tests
1. **QA-Navigation** in einer isolierten PSTE-Paketkopie unter neuer Testversionsnummer verpacken; Original-PSTE 0.57.144.32 + Original-PSERC 0.28.60 unverändert und rollbackfähig ablegen. Alle Hooks/Dateipfade/V2-K0-Probe bestätigen.
2. **Ein** WordPress-TEST-Lauf mit beiden Plugins: fünf Menüzielseiten öffnen, MINI-Daten/FREI/Artikelplan lesen, eine vorhandene 3-READY-Datei ohne Neurecherche nach K0-V2 erneut herunterladen, kein Datenverlust, gespeicherte Last-Version/Status unverändert.
3. Weiterer **Code-Abbau erst nach harter Referenzinventur**: Definition → interner Aufruf → WP-Hook/AJAX/Cron/CLI → externer WordPress-Plugin-Referenz → Option/DB/Archiv → Sicherheits-/Fallback-Pfad. Echte 0-Referenz-Kandidaten *in separatem* QA-Patch, nicht alle alten Funktionen blind entfernen.
4. Für LIVE isolierte **1:1-Kopie des echten Live-Bestandes** sichern (WordPress DB + Original-Dateien .120/.43), auf Kopie Upgrade und spätere Migration mit Daten-/Referenzzählung durchführen; insbesondere 6 archivierte Legacy-Optionen müssen vollständig zurücklesbar bleiben. Negative Tests und K0-Datei müssen PASS liefern.
5. Erst nach TEST- und LIVE-KOPIE-Nachweis kontrolliertes Update auf echter Live-Seite, Rückweg vorhanden; **kein Löschen der Plugins im WP-Backend**.

## Freigabestatus
`NAV_UI_CODE_QA=PASS`; `FUNCTION_REGISTRY_PARITY_QA=PASS`; `K0_METADATA_EXPORT_CONTRACT=PASS`; `WP_TEST_SIMULATION_OF_NEW_NAV=NOT_RUN`; `LIVE_UPDATE_APPROVED=NO`. Keine Behauptung über unbekannte LIVE-Datenbestände.
