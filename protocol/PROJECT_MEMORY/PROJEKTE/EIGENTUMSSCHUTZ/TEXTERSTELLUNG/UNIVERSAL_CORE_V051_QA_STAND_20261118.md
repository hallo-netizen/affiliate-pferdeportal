# Texterstellung 0.5.1-dev.1 – Gebündelter nächster Arbeitsschritt 18.11.2026

**Nur interner Entwicklungsstand, ausdrücklich NICHT für WordPress installieren.** User-Regel bleibt: nur installationsfähige Plugin-ZIPs als Chat-Downloads; Quell-/QA-Archive und Berichte ausschließlich im Büro.

## Geprüfte Ausgangsbasis
- Beide 0.5.0-qa.1-Varianten + gemeinsame Quelle vom 18.11. aus dem Hab-/Universal-Büro, kein Eingriff in Pferdeatelier Original, K0 oder Live-WP.
- Hab Kategorie-Workflow Quellverträge unter EIGENTUMSSCHUTZ/KATEGORIEN/...: aktive WP Option `apkw_target_tree_active_snapshot_v1` mit `mapping`, Option `apkw_target_tree_active_revision_v1`; `get_term_meta` `_apkw_target_node_id`,`_apkw_parent_concept_id` und `get_post_meta` `_apkw_target_node_id` belegt.
- GitHub k0-multiportal/main quarantined registry weiterhin ohne Hab; K0 ist nicht automatisch für Hab freigeschaltet. Vier Kernartikeltypen in historischer RULE_VALUES, lokale Testkopie fünf – Produktionsstand nicht behaupten.

## Geänderte 6 gemeinsame Quelldateien
1. `includes/class-txe-universal-catalog.php`: Hab prüft Revision und reale WordPress-Knoten-ID gegen das aktive Workflow-Snapshot. Fehlende/abweichende Zuordnung wird **ausgeschlossen**, nicht aus Namen erraten. Fremde nicht gebundene Kategorien blockieren andere gültige Kategorien nicht.
2. `texterstellung.php`: eigene Universal-Orderoption statt historischer Pferdeatelier-Shelf; eigener Stopstatus; keine Veränderung alter Stop-/Auftragsoptionen beim Aktivieren ohne Freigabe. Historischer MINI-Speicher für Universal getrennt.
3. `includes/class-txe-inventory-reader.php`: einziges WordPress-Regal liest künftig die neue Universal-Option.
4. `includes/class-txe-historical-proof-reader.php`: alter Pferdeatelier-MINI-Entscheidungsspeicher wird nicht als neue Portal-Wahrheit übernommen.
5. `includes/class-txe-diagnose.php`: getrennte Universal-Diagnose und getrennter künftiger Zugangskontext, keine Statusverwechslung mit originalen Pferdeatelier-Zugängen.
6. `includes/class-txe-universal-portal.php`: beim einmaligen bestätigten Setup eigenes, **leeres** WordPress-Auftragsregal initialisiert; bestehender eigener Zustand wird beim erneuten Setup nicht gelöscht. Übersicht zeigt nutzbare und ungebundene Kategorien getrennt.

## Reproduzierbare lokale QA
- Zwei WordPress-konforme internen ZIPs, ein gemeinsamer Kern; der Dateivergleich zeigt ausschließlich eigene `portal-distribution.json` und Plugin-Header-Zeile als Unterschiede.
- Je ZIP **80/80 PHP-Syntax und 9/9 JSON**, ZIP-CRC PASS, keine doppelten Dateinamen.
- **Hab 39 Funktionschecks PASS**, einschließlich stale snapshot, falsche Term-ID, unverknüpfte WP-Kategorie, andere gültige Kategorie bleibt verfügbar, leere Neuinitialisierung, keine Übernahme von Pferdeatelier-Aufträgen.
- **Universal 28 Funktionschecks PASS**, einschließlich generischer Robotik-/Wasser-Beispielkategorien, Website-Bindung, leeres eigenes Regal, kein alter WP-Optionswrite.
- Zwei technische `PFERDE_ATELIER_WORDPRESS_IMPORT_V1`-Kennungen im noch inaktiven historischen Importvertrag vorhanden; keine aktiven Pferde-Fachregeln.
- Hash Hab ZIP `e1333dfec47f755a7a2516234dad376524b472cb1e42435de790ec5706b76eec`; Universal `a27a07d2501f38200c25f27274a457517175a0775f37c919047cf9e7d59a1e79`. ZIP-Bau reproduzierbar: zwei unabhängige Builds ergaben identische SHA256.

## Gesicherte tatsächliche Artefakte
- `/hab-und-bewahr/TEXTERSTELLUNG/UNIVERSAL_ENTWICKLUNG_20261118/V051/` enthält Hab 0.5.1 Entwicklungs-ZIP, denselben QA-Bericht und Protokoll.
- `/texterstellung-universal/ENTWICKLUNG_20261118/V051/` enthält Universal 0.5.1 Entwicklungs-ZIP, QA-Bericht und Protokoll. In **beiden** Büros ist jetzt zusätzlich dieselbe vollständige gemeinsame Quelle samt Build-Skript und ausführbaren Tests archiviert (`TEXTERSTELLUNG_0.5.1_GEMEINSAME_QUELLE_UND_TESTS_NICHT_INSTALLIEREN.zip`), SHA256 `1a96fa1d9e618ebd2cf8988fec1a748c372624aa2bcc129adbea388e4c9a28fe`.
- Persönliche Dateiablagen erfolgreich hochgeladen, beide Originalpakete 0.5.0 bleiben unverändert.

## Offene technische Blockaden / nächste Arbeit
- Ursprüngliche PSTE-Recherche verwendet nachweislich `PSTE_Article_Type_Registry::build/resolve` und eine Artikeltyp-im-Kategoriennamen-Zuordnung. Die neue WP-Katalog-Entscheidung ist getrennt; originale Recherche/Provider/Fakten-/SEO-Pipeline müssen auf denselben einmaligen redaktionellen Entscheid umgestellt werden, ohne zweiten Fachprüfer und ohne Qualitätsverlust.
- K0-Portal-Registrierung und vier/fünf Artikeltypen mit der aktuell aktiven K0-Produktion abgleichen, nicht raten oder eigenmächtig K0 verändern.
- Reale WordPress-/DataForSEO-/K0-End-to-End-Abnahme steht noch aus. `productionReady()` bleibt nachweislich gesperrt. Keine der beiden ZIPs als Chat-Download anbieten.
- Danach **eine gemeinsame Codeänderung**, zwei Varianten durch denselben Build; nur nach vollständiger Abnahme installierbare Releases.

**Nicht verändert:** Pferdeatelier, K0-Repository, Webserver und Live-WordPress, veröffentlichte Artikel oder bisherige Redaktionspläne.
## Nachtrag: Portalwechsel dauerhaft abgesichert
- Das einmal eingerichtete eigene Universal-Auftragsregal trägt `portal_id`, Website-Fingerprint und Vertragskennung. Ein Portalwechsel auf derselben WP-Installation ohne gesonderte Migration wird verweigert, auch bei Wechsel zwischen Hab- und Blanko-Paket. Keine stillen Übernahmen, keine stillen Löschungen.
- Aufruf des Inventur-Lesers prüft dieselbe Bindung, nicht nur die Anzeige im Einrichtungsmenü.
- Beide Pakete erneut lokal getestet; Hab 39 und Blanko 28 Funktionschecks PASS. Zwei deterministische ZIP-Builds bytegleich.
