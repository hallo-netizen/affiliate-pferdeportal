# Pferdeatelier – K0 / MINI Live-Zweiartikelbeleg, 18.11.2026

**Ursache verifiziert, keine Plugin-/Writeränderung.** Die originale Benutzerdatei `texterstellung-k0-export-mit-zuordnung(1).json` enthält `WP_K0_UPLOAD_PACKAGE_V1` mit genau zwei Artikelmetadaten und **bereits** dem gültigen WordPress-Herkunftsbeleg `word_press_order_receipt` (`WP_K0_SOURCE_RECEIPT_V1`, `pferde-atelier.de`). Hashes, beide Auftrag-/Artikel-/Planplatzzuordnungen und beide gespeicherten Suchintentionen **PASS**. Der K0-Blocker `K0_UPSTREAM_SEO_SOURCE_MANIFEST_MISSING` war ein **falscher Eingangsabbruch**, weil der bestehende `engine.k0_wp_upload` diesen WordPress-Beleg in den vorhandenen K0-Standardplatz `PSERC_SOURCE_MANIFEST.json` schreibt und `engine.k0_seo_owner_binding.inspect` ihn bereits akzeptiert. Der K0-Originalablauf am 16.11.2026 hat diese Variante erfolgreich verarbeitet, siehe `real_runs/k0/k0-20261116-txe-4a2e4870-01/PSERC_SOURCE_MANIFEST.json` und `real_runs/k0/batch-20261116-txe-4a2e4870/WORDPRESS_BATCH.json`.

**KISS-Änderung im aktiven Branch `konzept0-portal-neutral-20261002`:** nur `K0_START_HERE.md`, `K0_CURRENT_STATE.json` und die **vorhandenen** Tests `tests/test_wp_k0_wordpress_source.py`. Kein neuer Worker, keine neue PSERC-Datei vom Benutzer, keine zusätzliche fachliche Entscheidung oder Prüfung, keine Änderung an `engine/k0_wp_upload.py`, `engine/k0_seo_owner_binding.py`, `engine/k0_writer_station.py`, `engine/k0_wordpress_export.py` oder `.github/workflows/k0-authoring-context.yml`. Kein Pluginwechsel, keine Änderung am WordPress-Live-Bestand.

**Echte ausgeführte Tests:**
- Gespeicherter MINI-Weg von 0.4.33 `CATEGORY → EDITORIAL → TITLE → Auftragsregal → K0-Export` **48/48 PASS**.
- Laufender MINI bei Übernahme der 61 historischen Aufträge **34/34 PASS**; Migration selbst **34/34 PASS**.
- Original hochgeladener Live-K0-Batch mit zwei Artikeln **2/2 richtige WordPress-Ursprungsbelege und Kanonical-IDs PASS**, ohne eine neue Suchintententscheidung.
- K0 GitHub Selbsttest Lauf **44328442057 SUCCESS, 189/189 Tests**; neuer Test 1/2/3 WordPress-Artikel-Eingang, Hash-/Identitätsbindung, deterministischer Wiederanlauf, erneute komplette WordPress-Zusammenstellung **zweier historisch fertiggestellter K0-Artikel** PASS.

Ausführlicher Prüfbericht in der persönlichen Library unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/PFERDEATELIER-KISS-MINI-K0-GESAMTBEWEIS-20261118.md`.

**Grenze:** Die **zwei aktuellen** Live-Artikel wurden noch **nicht neu von K0 geschrieben**; der echte neue Writer-/LanguageTool-/Entwurfslauf muss mit dem originalen Upload erfolgen. Vollständige Writer-/WP-Output-Verifikation ist für den echten früheren Zweierlauf nachgewiesen. Der ergänzende Main-Router-PR **#826** ist offen, bis die erforderlichen GitHub-Regelprüfungen die Übernahme zulassen.

**Nutzerweg:** Bestehende `texterstellung-k0-export-mit-zuordnung(1).json` im neuen K0-Chat hochladen, `K0:start`. Keine Blockerdatei, keine neue Recherche, kein separates PSERC-Manifest, kein Pluginwechsel, erst nach voller K0-Regelprüfung Entwurf importieren.
