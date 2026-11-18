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
