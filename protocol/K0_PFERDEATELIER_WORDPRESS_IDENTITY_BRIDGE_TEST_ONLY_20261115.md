# Pferdeatelier: WordPress -> K0 technische Zuordnung, isolierter TEST

Stand: 2026-11-15. KEIN Live-Release. KEIN realer K0-Artikel-/LanguageTool-Gesamtlauf.

## Autoritative Quellen

- K0 unveränderter Ausgangszweig: konzept0-portal-neutral-20261002, Commit 83419e7827cbc0ff02bcaef7cefd0bd0900ac93a (12.11.2026).
- Texterstellung 0.4.10: work/pferdeatelier-texterstellung-kiss-final-20261114, Commit 1b31ed50f0c46654c0066278f1cffb583ffa00f9 (15.11.2026).
- Echte WordPress-K0-Datei: 20 Aufträge, 5 Felder, Batch-SHA256 b42c66f32837264bafcd505dd53f0da797e142274ccaefdc2fe882f3352b323b.

## Nachgewiesene Ursache

Texterstellung 0.4.10 vergibt eine stabile Artikel-ID aus dem originalen WordPress-Auftrag; der K0-Canonical-Resolver verlangt fuer die neue Strecke dennoch einen passenden historischen PPM679-Redaktionsplanplatz. Aus dem SHA256-Slot allein ist die urspruengliche Artikel-ID nicht rueckrechenbar. K0 verlangt ausserdem im Authoring-Workflow eine separate PSERC_SOURCE_MANIFEST.json, die der aktuelle WordPress-KISS-Export nicht liefert.

## Testumsetzung auf isoliertem GitHub-Testzweig

Ausschliesslich diese Dateien im K0-Testzweig geaendert oder ergaenzt:
- engine/wp_order_identity_receipt.py (neu): bindet die vom **einen bestehenden WP-Register** gelieferte originale Auftrags-ID, Artikel-ID, vorhandene Suchabsicht und unveraenderte Fuenffelder-Metadaten. Falsche Identitaeten und leere Suchabsichten werden abgewiesen.
- engine/canonical_binding.py: neuer WP-Belegpfad **nur bei ausdruecklich vorhandenem WP-K0-Beleg**. Alte abgeschlossene K0-Laufdaten ohne WP-Beleg folgen weiterhin der urspruenglichen K0-Abfrage; diese wurde nicht geloescht.
- engine/k0_seo_owner_binding.py: dieselbe bereits eingefrorene WP-Suchabsicht wird ohne neue SEO-Entscheidung in den bestehenden K0-Job gebunden. Historische PSERC-Belege bleiben kompatibel.
- engine/k0_wp_upload.py (neu): ein WordPress-K0-Paket in einzelne **unveraenderte** Fuenffelder-K0-Auftraege auffaechern; bei identischen Wiederholungen nur existierende Dateien verwenden, geaenderte Belege blockieren.
- tests/test_wp_k0_wordpress_source.py (neu): originaler WordPress-Auftrag und sieben Negativ-/Wiederholungstests.

**Nicht geaendert:** saemtliche .github/workflows/**, Sicherheitsperren (GitHub Rulesets, Hardlock und Firewall), K0-GOAL, K0-CURRENT_STATE, Writer, 81 Artikelregeln, 104 PPM-Qualitaets-Paritaetsregeln, LanguageTool 6.8, Endkontrolle, Importstruktur, Draft-only-/Publish-Regeln und Original-K0-Prozesskern.

## Isolierte WordPress-Test-ZIP

Private Pluginablage:
`/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung_KISS_0.4.11_TEST_WP_SOURCE_RECEIPT.zip`

SHA256: `605774310ba03394af1ba6c4338490b019fbd4764aea1489b8ae7fdd4a6eb8a7`.

Diese vollstaendige Test-Plugin-ZIP ersetzt **nur auf oliver-beil.de** die bestehende 0.4.10-Installation; NIEMALS das Plugin loeschen oder produktiv einsetzen. Sie laesst den bisherigen K0-Fuenffelder-Export INHALTLICH unveraendert, verpackt ihn aber mit dem aus exakt demselben WP-Auftragsregal stammenden technischen Identitaets-/Suchabsichtsbeleg in eine einzige herunterladbare JSON. Es gibt **keine weitere manuelle Freigabe**. Der gespeicherte 20er-Lauf wird per `Letzte reservierte Datei erneut herunterladen` wiederverwendet.

## Lokal ausgefuehrte QA (keine echte WP/K0-Gesamtabnahme)

- ZIP CRC PASS; 90 Dateien; **81/81 PHP Syntax PASS**.
- Echter originaler WP-Order-ID des ersten Horseware-Artikels: Artikel-ID und bisheriger K0-Slot stimmen mathematisch exakt.
- PHP-Test mit demselben Originalauftrag: einmalige Verpackung, identische Wiederholung, kein neuer Status/Entwurf, fehlende Suchabsicht BLOCK, falsche ID BLOCK.
- 20 synthetische Eintraege mit exakt 20 originalen echten Titeln und 8 originalen Kategorien, aber bewusst **synthetischen** IDs/Slots: alle 20 WP-Paketpositionen und Python-K0-Auftragsauffaecherung PASS. Keine Behauptung ueber 20 originale WP-Order-IDs.
- Acht Python-Positiv-/Negativ-/Replay-Tests PASS; 8/8 echte K0-Kategorien im aktuellen GitHub-Kategorieregister vorhanden.
- Keine K0-Artikelproduktion, kein LanguageTool-6.8-Lauf, kein echter WordPress/MySQL-Rueckimport. Kein Live-GO.

## Naechster ECHTER Test

Auf isolierter Testseite Datenbank sichern, Plugin 0.4.11 ueber **Ersetzen, nicht loeschen** installieren, unter Texterstellung > K0-Export die **letzte reservierte K0-Datei erneut herunterladen**, anschliessend die neue JSON im Chat bereitstellen. Dann 1 Originalartikel durch das unveraenderte K0-Schreib-/Qualitaetsverfahren und als WordPress-ENTWURF zuruecktesten. Erst danach alle 20, inklusive Unterbrechungswiederaufnahme. Keine Liveinstallation.
