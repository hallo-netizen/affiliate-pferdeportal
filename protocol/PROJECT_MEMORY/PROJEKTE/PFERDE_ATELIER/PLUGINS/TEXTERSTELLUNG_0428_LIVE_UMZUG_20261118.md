# Pferdeatelier: Texterstellung Live-Vorbereitung und Migration (18.11.2026)
**Status: vollständiger, isolierter Live-Installationskandidat; NOCH keine verifizierte echte Live-Aktivierung.**

## Belegter Stand aus WP-Exporten
- Live: 163 veröffentlicht, 19 Papierkorb.
- Test: 144 veröffentlicht, 22 Entwürfe, 3 Papierkorb.
- 163 gemeinsame Beitragsslugs: 147 Texte bytegleich, 16 Unterschiede nach Ersetzung `https://oliver-beil.de/` mit `https://pferde-atelier.de/` vollständig identisch.
- 19 der 22 Testentwürfe sind als inhaltlich identische veröffentlichte Live-Beiträge vorhanden; also **keine 19 Duplikate** erzeugen.
- Nur drei neue Testentwürfe, IDs 973841 (Horseware-Regendecken), 973882 (teuerstes Pferd Deutschlands), 973883 (Wasserführanlagen).
- Drei-Artikel-WordPress-Import als DRAFT: `/pferdeatelier/UMZUG-TEST-LIVE/Pferdeatelier-3-neue-Testartikel-ENTWUERFE-20261118.xml`. Die zwei veralteten Sperr-Metadaten der drei Neuimporte sind entfernt; Texte nicht verändert. Vor Veröffentlichung canonical C-Linktext korrigieren. WordPress-Export enthält keine komplette Site-Sicherung!

## Vollständiges Live-Kandidat-Plugin
- `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.28-PFERDEATELIER-LIVE-INSTALLATIONSKANDIDAT.zip`
- SHA256 `e13566bb49c5d94d4b5cabe29860dc914c10c0d3da8dc697ea31170225e7a45f`.
- Original-Basis 0.4.27 (sicheres Diagnosesystem); K0/PSTE/PSERC Originalmodule nicht bearbeitet, insgesamt 88 Dateien, PHP-Lint 78/78, ZIP CRC PASS.
- WordPress auf `pferde-atelier.de` **passiv bis explizite LIVE-Bestätigung** durch Admin (exakte Domain + Checkbox). Eine alte Test-Bestätigung kann LIVE nicht freischalten. Bereits auf Test bestätigte Installation bleibt im Testmodus. Frühere Recherche-Datenbanktabellen und WP-Optionen werden durch Plugin-Austausch nicht gelöscht.
- Auf Live müssen die drei aktiven Legacy-Plugins `Portal SEO Themenengine` (0.57.120), `Portal SEO Redaktionsplan Compiler` (0.28.43), `Portal Production Machine` (6.7.9) **zuerst deaktiviert** werden; nur deaktivieren, erst nach Bestandsabgleich löschen.
- Neue K0-Dokumente bleiben technisch unverändert nur Entwürfe. Kein Auto-Publish, kein stilles Umstellen von bereits veröffentlichten Beiträgen. Getrennte Prüfung der Alt-PSTE-Datenmigration vor Recherche notwendig.
- Abschließende originale WordPress-Integrationsprüfung auf Live fehlt noch und ist nicht zu behaupten.

## Live-Plugin-Cleanup
Bereits deaktiviert, bei Verzicht auf Wiederverwendung löschbar: HivePress Geolocation; HivePress Messages; Pferde Atelier Mail-Absender; Amazon-Ursache (nur Diagnose); eBay Ursachencheck (nur lesen); eBay-Fehler lesen; Portal Production Link Policy Gate.

Aktive rein lesende Analysehilfen nach Sicherung ihrer Arbeit abschaltbar: DBStorage Insights; Performance Diagnose Safe; eBay-Ein-Klick-Sichtbarkeitsdiagnose; WordPress Speicheranalyse; SEO-Quellpaket Exporter.

Unverändert beibehalten: Affiliate-Zentrale 6.72.356, Template Kit 1.50.614, Yoast, Bildzentrale, HivePress und produktive Erweiterungen, WPForms, Suchfunktionen, CookieYes, Backup-Werkzeug, Produktwissen. Kubio/Shortcodes/AJAX-Suche erst nach Frontend-Prüfung.

## K0 Linkregel
Isolierte GitHub-Korrektur auf Branch `work/k0-canonical-c-links-writer-return-20261118` gegen aktiven K0-Zweig `konzept0-portal-neutral-20261002`: offizielle C-Kategorie bzw. veröffentlichter C-Beitrag aus WordPress **vor** dem Schreiben einmalig binden, der Schreiber baut grammatikalischen Satz um exakt diesen Titel; bestehender `links.bound_pairs_exact` ist der einzige Textlinkbeleg. Bei Fehler: `K0_WRITER_REVISION_REQUEST_V1` an denselben Auftrag, kein zweiter Quality Gate. Kein K0-Metadatenvertrag, LT 6.8, PPM679, Design oder Live-WordPress verändert.

## Dokumentation
Prüfbericht und Quell-Exportangaben im persönlichen Pferdeatelier-Büro: `/pferdeatelier/UMZUG-TEST-LIVE/PFERDEATELIER-LIVE-UMZUG-PRUEFBERICHT-20261118.md`.

**Nächster echter Schritt:** Sicherung der Live-Datenbank und Recherchebestände; gezielter Import der drei Entwürfe; kontrollierter Pluginwechsel und einmaliger K0-Entwurfsimport mit Live-Bestandsabgleich, keine Publikation ohne Linkkorrektur.

## Abschluss / nachträgliche technische Freigaben
- K0-Korrektur PR #824 mit SHA `8ef0532e2afb3265fbbae5a26346222aceaa360e` erfolgreich nach `konzept0-portal-neutral-20261002` übernommen. Abschließender vollständiger K0-Selftest-Lauf `44294760802`: **SUCCESS**.
- Texterstellung 0.4.28 gegen vorhandene 0.4.27-Regressionssuite mit beiden echten K0-Artikeln und simuliertem WordPress erneut geprüft: **38/38 PASS**. Drei isolierte Smoke-Checks bestätigten, dass die Live-Seite ohne ausdrückliche Livebestätigung nicht freigeschaltet wird, selbst bei vorhandener alter Testbestätigung.
- Die 16 unterschiedlichen gemeinsamen Artikelinhalte wurden vollständig nach Ersetzung der absoluten Domain geprüft: **16/16 ausschließlich Domain-Unterschiede**.
- Drei-Artikel-WXR nach Erstellung korrigiert: GUIDs und Links der drei neuen Drafts zeigen auf öffentliche Domain, nicht mehr auf Test-URL. XML validiert, SHA256 `b1074308f0b79e416c29c742d9486064dfb5b6ac15c1ffed270a2dd374014714`.
- Kein WordPress-Livezugriff bzw. echter K0-Ende-zu-Ende-Lauf durchgeführt. KEINE Live-Freigabe oder Publikation ohne Bestandsmigration und C-Linkkorrektur.

## KISS-Klarstellung: 3 Testentwürfe und Redaktionsbüro
- **Keine manuelle Zuordnung als Pflichtschritt** nach dem WordPress-XML-Import. Die neue Texterstellung liest in `TXE_Inventory_Reader::read()` veröffentlichte und nicht veröffentlichte WordPress-Posts direkt in den einzigen Bestands-Snapshot ein, einschließlich `_ppm679_canonical_article_id` und `_ppm679_plan_slot_sha256`. Diese Metadaten stehen in der 3-Artikel-XML.
- Die drei Artikel daher genau einmal als Entwürfe importieren; keine separaten K0-Aufträge anlegen oder Texte neu produzieren.
- Strikte Aussagegrenze: Dieser WordPress-Bestandsabgleich setzt einen etwaigen schon bestehenden Auftrag im Auftragsregal `texterstellung_orders_v1` **nicht automatisch** auf erledigt. Das alte Regal wird als separate Quelle gelesen. Mangels geprüftem Live-Regalbestand darf weder seine vollständige Synchronität noch ein nötiger manueller Zuordnungsschritt behauptet werden.
- Keine ungeprüfte automatische Auftragsänderung und keine zusätzliche Prüfstation.

## Aktuelle Version ab 18.11.2026, 12:54 Uhr – Texterstellung **0.4.29 KISS ohne Website-Freigabe**
**Die bisherige 0.4.28 ist durch 0.4.29 als Installationskandidat abgelöst.**
Der Nutzer zeigte einen Screenshot des live installierten Plugins 0.4.28 auf `pferde-atelier.de`: Die Seite zeigte ausschließlich `Live-Seite bewusst freigeben` statt des Redaktionsbüros. Das ursprüngliche 0.4.28-Paket wurde hier vollständig geöffnet und geprüft; im Haupt-Plugin waren die zusätzliche Domain-/Checkbox-Bestätigung, der Site-Fingerprint-Check, ein Bootstrap-Boot-Gate, Admin-POST-Gates, eine AJAX-Zugangssperre und ein UI-Return vorhanden.

**Umgesetzt:** Diese *zusätzliche* Website-Bestätigung einschließlich ihrer unbenutzten Funktionen wurde aus der 0.4.29 vollständig entfernt. Der PSTE-Kern lädt bei normalen WordPress-Requests, sofern die vorhandene Altplugin-Konfliktprüfung erfolgreich ist. Das Redaktionsbüro ist für WordPress-Administratoren direkt zugänglich.

**Unverändert** bleiben: bestehende PSTE-/PSERC-Originale, sämtliche K0-Texte und K0-Tests, bestehende Auftragsregale, DataForSEO-Kostenfreigabe je bewusst gestartetem kostenpflichtigem Lauf, WordPress-Adminschutz und Nonces, der Entwurfsimport und die Regel `keine automatische Veröffentlichung`, bestehende Diagnosen. **Keine Datenbank-/Content-Löschung**, keine Änderung an Hobbydepot oder Hab & Bewahr.

**Dateien im Pferdeatelier-Pluginbüro** `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/`:
- `Texterstellung-0.4.29-KISS-OHNE-LIVE-SPERRE-PFERDEATELIER.zip` – vollständiges Installationspaket
- `Texterstellung-0.4.29-KISS-SPERRFREI-PRUEFBERICHT-20261118.md`
- `Texterstellung-0.4.29-PRUEFRESULTATE.json`

**SHA-256:** `0b11e9f52f86c27d08c1b534909ed1c78a163d0788a3bbc4b523c22dff9c935e`. Gegenüber 0.4.28 genau drei Dateien geändert, 85/88 bytegleich. 78/78 PHP-Syntaxprüfungen, ZIP-CRC und 38/38 vorhandene echte K0-Importregressionen in simulierter WordPress-Umgebung bestanden. Zusätzliche Smoke-Tests: Dashboard auf Test und Live ohne Freigabe sichtbar, unveränderte gespeicherte Aufträge, Schutz vor Nicht-Administratoren, Schutz vor paralleler Legacy-PSTE-Bootstrap, draft-only.

**Statusgrenze:** Keine echte Live-WordPress-Installation oder echter DataForSEO-Lauf durch Entwickler ausgeführt. Nutzer muss die 0.4.28 auf `pferde-atelier.de` unter `Plugins > Plugin hinzufügen > Plugin hochladen > Installieren > bestehendes Plugin ersetzen` durch 0.4.29 aktualisieren; kein Deinstallieren oder Datenreset. Der Warnhinweis `PSTE-Migration fehlt` kann bei noch nicht migrierter alter Datenstruktur legitim weiter bestehen und ist NICHT dieselbe Zusatz-Freigabesperre.

Die Original-0.4.28 bleibt dokumentiert als vormals installierte fehlerhafte Zusatz-Gate-Version. Von einem tatsächlichen 0.4.29-Liveerfolg erst sprechen, wenn WP-Seite den neuen Stand zeigt.
