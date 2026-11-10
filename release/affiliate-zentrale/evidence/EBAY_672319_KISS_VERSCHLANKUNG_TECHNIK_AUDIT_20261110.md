# Pferdeatelier – KISS-Verschlankung gemeinsam mit eBay-Workflow
Datum: 10.11.2026. Grundlage physisch überprüfte ZIP **Pferdeatelier_Affiliate_6.72.319_LOKALER_BESTANDSFIX_NUR_TEST.zip** (66 ZIP-Dateien); Quellkopie `/mnt/data/ebay_work319/affiliate-portal-router/` **bytegenau** mit Original der drei Hauptdateien abgeglichen. **ARBEITSSTAND: nicht freigegeben, nicht auf WordPress installiert, kein Current-Update.**

## Zielvertrag/Schutz
Fachliche Funktionen (Amazon, idealo, Awin, eBay, Banner, Kontroll-/Veto, Textlinks, Partner, HivePress) sowie öffentliche Ausgabe und vorhandene DB-Optionen bleiben erhalten. K0/Hobby/Hab unberührt. Keine neue Tabelle, keine zweite eBay-Entscheidungsinstanz. Manuell pausierten eBay-Lauf ohne Freigabe nicht automatisch starten.

## Strukturmessung und Befunde (319)
- **23 PHP-Dateien; rund 49.680 PHP-Zeilen**, **33 registrierte Menüeinträge** aus PHP-Routen einschließlich Provider-Fachseiten und KISS-Seiten.
- `pferdeportal-affiliate-router.php:8945–8949` registriert zusätzlich zur KISS-Navigation noch drei **direkt sichtbare** ältere Untermenüs (Werbemittel, Rechner & Textlinks, Amazon-Suchlinks). `includes/class-ppar-admin-kiss.php:39–45` registriert die fünf funktional gebündelten KISS-Bereiche. Diese drei extra Menüzeilen sind eine **nachgewiesene Navigationsdopplung**, keine zusätzliche fachliche Funktion.
- eBay `includes/trait-ppar-ebay.php:10451+` implementiert seit 319 einen **parallelen Bestandslauf** mit eigener Option `ppar_ebay_local_reuse_v319`, eigenem Status/Tick und zusätzlicher Starttaste. Kanonischer Run speichert separat `ppar_ebay_run_state_v1`. Der zusätzliche Lauf darf **nicht** als zweite entscheidungsführende Engine bestehen bleiben: Bestandszuordnung in die kanonische Auswahl integrieren; gespeicherte Optionen nicht löschen.
- `pferdeportal-affiliate-router.php:483` registriert `wp_ajax_ppar_ebay_local_reuse` **innerhalb** der Bedingung `is_admin() && !$is_ajax_request`. Ein echter WordPress-AJAX-Request erfüllt `!$is_ajax_request` nicht: Der AJAX-Handler der 319-Zusatztaste ist so **nicht erreichbar**. Nicht als weiteren Mini-Fix separat registrieren, sondern den zweiten Steuerweg im Gesamtumbau abschaffen. Das erklärt, warum der Klick keine verlässliche Aktion gestartet hat, ersetzt jedoch keine WordPress-Live-Fehlerlogprüfung.
- Als zentrale Entscheidungsmethoden vorhanden: `ebay_business_classify_portal_item_strict`, `ebay_business_quality_assess`; zusätzliche 319-Klassifizierungs-/Auswahlpfade müssen diese Autorität wiederverwenden, ohne eigene Freigaberegeln.
- **Nicht löschen:** `recovery/aff043-historical-product-state-20260915.json` (rund 1,36 MB) ist im Quellcode über `AFF043_SNAPSHOT_REL` und `aff043_snapshot()` samt Wiederherstellungsfunktion referenziert. `assets/portal-structure-v279.json` und `assets/ebay-portal-catalog-v2.json` werden live gelesen und sind keine ungenutzten Beigaben. Bilder teilweise dynamisch referenziert; simple Textsuche genügt nicht, um sie als unbenutzt zu markieren.
- Alte versteckte Admin-Routen müssen so lange bleiben, wie interne Formulare und Direktlinks sie nutzen. Unreferenzierte alte Altansichten sind **Kandidaten**, aber noch nicht freigegeben, weil externe Bookmarks/Protokolle nicht hinreichend geprüft sind.

## Bereits umgesetzte Änderung in isolierter Arbeitskopie (KEINE Pluginfreigabe)
Pfad: `/mnt/data/ebay_kiss_integrated_stage/affiliate-portal-router/`, aus bitgleich verifiziertem 319-Original kopiert.
1. Drei zusätzlich sichtbare Untermenüs nur im Parent von `affiliate-portal-zentrale` auf `null` geändert; Page-Slugs, Handler und alle Routen **unverändert**.
2. Im vorhandenen KISS-Bereich **Produkte & Deals** fehlende zwei Links zu `Rechner & Textlinks` und `Amazon-Suchlinks` ergänzt. Der Werbemittel-Link bestand bereits.
3. In der Arbeitskopie per echtem PHP-Aufruf von `admin_menu()` und `register_visible_navigation()` geprüft: **6 sichtbare Menüpunkte (Übersicht + fünf KISS-Bereiche), 26 versteckte aber registrierte Fachseiten, 33 insgesamt; alle Callback-Funktionen aufrufbar.**
4. **23/23 PHP-Syntaxprüfungen PASS; 25/25 originale Startfreigabe-Gates PASS; 39 kanonische Start-Prüfungen PASS.** Noch keine eBay-End-to-End-Live-Abnahme. Diese Navigation wird nicht als separates 320-Update ausgegeben.

## Einzuhaltende Umbau-Reihenfolge
1. 319-Zusatzauswahl in den vorhandenen kanonischen Ablauf integrieren, eigene Start-/Tick-Steuerung ablösen, ohne die gespeicherten Altoptionen zu löschen.
2. Eine einzige fachliche Produktentscheidung und eine einzige Auswahl/Zuordnung je Kategorie; Fehler je Angebot/Familie isolieren, nur globale Integritätsfehler hart stoppen.
3. Sicheren Last-Good-Publikationsstand und pausierten Lauf fortschreiben; nach jeder Speicherung tatsächlichen Stand rücklesen.
4. Direkt sichtbare Frontend-Produkte auf konkreten Produktseiten nachweisen und nur für verbleibende Warenthemen bedarfsgerecht suchen; keine Befüllungsquote erzwingen.
5. Kandidaten für alte Routen, alte Daten/Assets nach harter Referenz-/Rückfallprüfung entfernen, sonst beibehalten; keine willkürliche Löschung.
6. Erst gesamter WP-Test einschließlich fehlgeschlagener Einzelfälle, Fortsetzung, Doppelartikel, Multi-Zuordnung, öffentlichem Produkt auf korrekter Seite; eine einzige gebündelte Test-/Freigabeversion.

**Grenze:** Bisher ist die Backend-Navigation in der isolierten Arbeitskopie tatsächlich geändert und geprüft. Die zentrale eBay-Engine ist **noch nicht zusammengeführt**. Keine Behauptung, dass diese Änderungen bereits live sind.


## Folgearbeit 10.11.2026 – isolierte Umsetzung und harter Referenzvergleich

**Staging, NICHT installiert, NICHT freigegeben.** Vollständige 66-Dateien-Arbeitskopie in der persönlichen Library:
`/pferdeatelier/PLUGINS/QA/EBAY_319_KISS_GESAMTUMBAU_STAGING_NICHT_INSTALLIEREN_20261110.zip`
(SHA-256 `8de2872b6dbec09db0bbbaa2d5667c31ffc070ac8a12bff9512d273f8f70aa07`).
Diff/Prüfakte am selben Ort:
`EBAY_319_KISS_STAGING_20261110.patch` (SHA-256 `52d1ba538b42200c41c7a1c71000b48e0728a2c770acd4ce5d270097a22ed82c`),
`EBAY_319_KISS_GESAMTUMBAU_QA_20261110.md`.

**Implementiert:**
- In `includes/trait-ppar-ebay.php` prüft der bestehende kanonische BUSINESS-Gapfill-Plan bei fehlenden Gewinnern **begrenzt die bereits gespeicherten Angebote**, mit derselben strengen Quell-/Klassifizierungs-/Qualitätsregel; der reguläre Auswahl-/Materialisierungsweg entscheidet weiter. Kein neuer API-Aufruf, Worker, Datenbankschema oder eigener Laufzustand.
- Die bisherige 319-Zusatzauswahl verwendet nun **dieselbe** Kandidatenprüfung, damit zumindest keine zweite fachliche Kandidatenentscheidung mehr besteht. **Ihre eigene UI und Start-/Tick-Steuerung sind als Übergang noch vorhanden** und müssen VOR endgültiger Freigabe funktional ersetzt werden. Keine Funktionslöschung/Deaktivierung.
- Exakt **43 unerreichbare Zeilen** nach der unbedingten `return disabled` in `ebay_run_verify_private_public` entfernt. Gleiches Funktionsverhalten, Signatur erhalten.
- Die schon dokumentierte, nur optische Verringerung um drei doppelte Menüpunkte erhalten.

**Gesamtvergleich zum 319-Original:** **66/66 Dateien vorhanden**, **1.561/1.561 ursprüngliche PHP-Funktionen erhalten**, genau eine gemeinsame Hilfsfunktion zusätzlich, alle registrierten Hooks unverändert. **41 Assets/1 Recovery-JSON byteidentisch**, übrige 62 Originaldateien unverändert; nur vier PHP-Dateien geändert. Keine Migration, `delete_option`, Credential-Änderung oder Veränderung von WordPress-Daten.

**QA:** 23 PHP-Lints PASS; 16/16 neue isolierte Tests (kanonische Auswahl, fachliche Ablehnung, Datenbanklesefehler einzelner Kategorie ohne globalen Abbruch, Drei-Angebote-Limit, Normalweg ohne weitere Suche) PASS; historische 49/49 PHP-Tests, 14 HTTP-Szenarien, kanonische Orchestrator-Simulation, Bootstrap (342 Methoden/143 Hooks) und Frontend-Quellgate PASS. **Keine echte WordPress-Datenbank-End-to-End-Abnahme**. Der Nutzer hat ausdrücklich 100% Funktionserhalt und keinen Daten-/Credentials-Verlust gefordert: bei ungesichertem Altcode bleibt dieser unverändert. Nicht als installierbares neues Release bezeichnen.

**Offen:** 319-Zusatzsteuerung vollständig in den einen kanonischen Checkpoint überführen, alte Option behalten; Speicherung mit tatsächlichem WP-Readback sowie reales Frontend auf der richtigen Produktseite abnehmen. Erst danach über die nächsten kleinen, nachweislich redundanten Bestandteile entscheiden.
