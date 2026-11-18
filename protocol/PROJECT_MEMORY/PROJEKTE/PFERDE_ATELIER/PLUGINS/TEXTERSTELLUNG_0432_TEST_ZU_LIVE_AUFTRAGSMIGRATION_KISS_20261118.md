# Pferdeatelier – Texterstellung 0.4.32 / einmalige Test-zu-Live-Übernahme

**Stand 18.11.2026. Installationskandidat lokal erfolgreich geprüft. Zuletzt bestätigter Live-Stand durch Screenshot: 0.4.31. Noch KEINE echte Live-Übernahme.**

## Nachweis der Ursache
- Testdiagnose `texterstellung-diagnose-20261118-103145.json`: 61 historische WordPress-Aufträge: 3 FREI, 15 EXPORTIERT, 3 IMPORTIERT und 40 METADATEN_OFFEN.
- Live-Diagnose `texterstellung-diagnose-20261118-124900.json`: Auftragsregal 0, aber aktiver MINI-Auftrag (zuletzt CATEGORY gespeichert). Nutzer berichtete später über bereits erledigten EDITORIAL-Schritt; noch keine neue Live-Diagnose dieses Standes.
- Originale Live-Recherche: 5.016 Themen; ist nicht das WordPress-Auftragsregal. ZIP-Wechsel überträgt WP-Optionen von `oliver-beil.de` nicht auf `pferde-atelier.de`.

## Unveränderter Zielvertrag
Eine Originalrecherche → genau ein MINI für Kategorie/Redaktion/Titel → **ein vorhandenes WordPress-Auftragsregal** → bestehender fünfteiliger K0-Vertrag → WordPress-Entwurf. Keine neue fachliche Redaktion, kein zweiter Datenbesitzer, keine zweite Prüfung, keine automatische Veröffentlichung.

## 0.4.32 gegenüber 0.4.31
- Genau **86 bisherige Dateien byte-identisch**, 2 verändert (`texterstellung.php`, README), 1 Datenquelldatei aus der vom Nutzer gelieferten echten Testdiagnose hinzugefügt (`includes/txe-verified-test-61.php`).
- **Ein** einmaliger Übernahmeknopf nur im bestehenden Live-WordPress-Menü Texterstellung → Übersicht; nutzt vorhandenen Adminschutz, Nonce, exklusiven Schreibzugriff und **dasselbe** gespeicherte `texterstellung_orders_v1`-Regal; **keine** neue Datenbanktabelle, kein Zusatzplugin, kein neuer Produktionsplan/Worker.
- Kopiert nur Originalentscheidungen/Quell-ID/Titel/Keywords/Kategorien/Artikelform/ursprünglichen Bearbeitungsstatus. **Niemals Test-WordPress-ID oder alten K0-Planplatz nach Live übernehmen.**
- 15 alte EXPORTIERT nicht erneut freigeben. 3 alte IMPORTIERT nur mit gefundenem wirklichem Live-Artikel verbinden, sonst parken. 40 METADATEN_OFFEN erhalten; sie dürfen nicht frei geraten werden. 3 alte FREI nur mit gültiger, vorhandener Live-Kategorie und K0-fähiger ursprünglicher Artikelart; alter Typ `Journal` bleibt offen, nicht still umwandeln.
- Laufende MINI-Charge (`active_seo_batch`), gespeicherte CATEGORY/EDITORIAL/TITLE-Quittungen, Recherche, vorhandene Live-Aufträge und gefrorene Quellen **bleiben bytegenau unverändert**. Gleicher Keyword-Eigentümer wird nicht ein zweites Mal angelegt. Ein erneuter Übernahmeklick wird nicht erneut schreiben.

## Lokale Beweise
- Echte Originalquelle mit 61 Testaufträgen und aus dem letzten Nutzer-WXR-Export nachgebildeter Live-Artikelbestand mit 163 veröffentlichten Artikeln.
- **34/34** Migrationstests (inkl. 16 ursprüngliche MINI-Tests). 61 historische Aufträge, 2 zunächst K0-bereit, 59 nicht neu freigegeben; Originalstatus für alle 61 erhalten.
- **34/34** Tests mit aktiver MINI-EDITORIAL-Quittung: Übernahme bei bereits offenem TITLE, dann TITLE erfolgreich, **genau 3** unterschiedliche K0-fähige Aufträge, Live-Artikel-ID statt Test-ID, Keyword-Kollision erhält bestehenden Live-Auftrag.
- **48/48** MINI-K0-E2E und **38/38** Original-Importregressionen; **79/79** PHP-Syntaxprüfungen; ZIP-CRC bestanden.
- Diese Nachweise sind lokale WordPress-Simulationen, **keine echte Live-Installation**. Keine Behauptung, dass die neue Canonical-C-Linkregel bereits in einem echten neuen Text unter Live getestet wurde.

## Aktuelles Paket und Büro
`/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.32-KISS-LIVE-AUFTRAEGE-SICHER-UEBERNEHMEN.zip`
SHA-256: `9ac18935d056695d76dd3fbf400e61622baa90335a086b80d3b0123a1328af77`.
Ausführlicher Original-Prüfbericht `PFERDEATELIER-TEXTERSTELLUNG-0432-MIGRATION-KISS-PRUEFBERICHT-20261118.md` und Testlogs liegen ebenfalls in genau diesem Büro.

## Genau ein sicherer Benutzerweg
1. Aktuelle Live-DB-Sicherung mit WPvivid erstellen.
2. WordPress → Plugins → Plugin hinzufügen → ZIP 0.4.32 hochladen → alte Texterstellung **ersetzen, nicht löschen**.
3. Texterstellung → Übersicht → **„61 Testaufträge sicher ins Live-Regal übernehmen“** einmal klicken; tatsächliche Zahlen vor Ort ablesen.
4. Bestehenden MINI-Auftrag bei angezeigt offenem **TITLE** im selben Chat fertigstellen und über MINI-Import zurückgeben.
5. **K0-Export**: die tatsächlich als FREI markierten 1–3 Artikel an K0 übergeben und exakte C-Linktexte im K0-Text testen. Rückimport nur als Entwurf.
