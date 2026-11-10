# Pferdeatelier eBay – KISS Gesamtworkflow QA4, 10.11.2026

**Nur isoliertes Staging; nicht installieren; pausierten WordPress-Lauf nicht verändert.**

Die kanonische öffentliche Abdeckungsprüfung `ebay_run_public_business_coverage` las vorher zu jedem veröffentlichten Angebot die zugehörige eBay-Quelle und das Kreativobjekt einzeln aus der Datenbank. Die gleiche Methode lädt diese lesenden Daten nun in **begrenzten Gruppen von 80** aus den vorhandenen Tabellen und führt anschließend **dieselben bisherigen Einzelprüfungen** in derselben Reihenfolge aus (Quellidentität, Policy, Frische, Werbemittel, Kampagne, Zielseite, Mehrfachzuordnung und Kapazitätsgrenze). Kein zweiter Workflow oder zusätzlicher Entscheider.

**Direkter Alt-/Neu-Test derselben echten PHP-Methode:** Auf 168 nachgestellten öffentlichen Kampagnen (darunter ungültiger Hash, fehlende Quelle, fehlendes Werbemittel, aktualisierter Artikel mit gleicher Identität, Mehrfachfamilie und Kapazitätsfehler) exakt gleiche vollständige Ergebnisstruktur; DB-Lesungen **334 vs. 7**. Identische Rückgaben auch bei `allowed_campaign_ids`, Quellenlesefehler und Werbemittellesefehler. Dies ist eine isolierte Testmessung, nicht der WordPress-Live-Lauf. Bei Fehlern wird keine Marktlücke erfunden.

**Bestandsschutz:** Original QA3 und QA4 beide 66/66 Dateien. **Eine einzige vorhandene PHP-Datei** geändert: `includes/trait-ppar-ebay-run.php`. 65 andere Dateien byteidentisch. 23/23 PHP-Lints und 8 vorhandene Regressionstestskripte PASS (inkl. 49 ältere Fachtests, 22 Resume-Fälle und 11 Speichertests). Kein Datenbankschema, keine WordPress-Option, kein Zugang, keine Sicherungsdatei, kein Katalog, keine öffentliche Ausgabe und kein pausierter Run geändert.

**Belege im persönlichen Pluginbüro:**
`/pferdeatelier/PLUGINS/QA/EBAY_319_KISS_EIN_WORKFLOW_QA4_LESEN_STATT_EINZELABFRAGEN_NICHT_INSTALLIEREN_20261110.zip`
SHA-256 `10b2e9c470b560f2130f60d252d3a56ca4ab005da57eca248e4cfefca5d451bb`.
Diff `EBAY_319_KISS_QA4_NUR_GEMEINSAME_DATENLESUNG_20261110.patch`, vollständiges Prüfprotokoll `EBAY_319_KISS_QA4_EFFIZIENZ_AUDIT_20261110.md`, Regressionstest-Log und reproduzierbarer PHP-Paritätstest.

**Freigabegrenze:** Weiterhin keine echte WordPress/MySQL/Praxis-Abnahme. Daher kein Release und keine Installation. Keine Wiederholung bereits abgeschlossener Fehlerisolierung.
