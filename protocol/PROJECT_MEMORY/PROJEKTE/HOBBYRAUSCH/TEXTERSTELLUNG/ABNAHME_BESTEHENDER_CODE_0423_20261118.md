# Hobbydepot Texterstellung 0.4.23 – Bestandsabnahme ohne Codeänderung

**Datum 18.11.2026 · Nur Pferdeatelier-Bereinigung; keine neue Architektur/Pluginversion.**

## Tatsächlich überprüfte Dateien
- ZIP `Texterstellung_Hobbydepot_0.4.23_BEREINIGT_TEST.zip`, SHA-256 `c50caa2ed263fb1f42f4cd485ecb2d23bbece6df072d9cf8f55774161aa6e715`, unverändert im Hobbydepot-Büro `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/`.
- Paket **87/87 CRC PASS**; **78/78 PHP-Lint PASS**; **8/8 JSON gültig**; gegenüber ursprünglicher Hobbydepot-0.4.23-Kopie **71 identisch, 16 bereinigt**; keine neuen Quellpfade.
- Pferde-Fachbezüge in PHP/JSON: keine mehr; nur zwei historische Import-Kennungen `PFERDE_ATELIER_WORDPRESS_IMPORT_V1` in PHP plus README-Hinweis (Kompatibilitätsvertrag). Vier Original-PSERC-PHP unverändert.

## Funktionstests – Quellcode, nur isolierte WordPress-Mocks
- Drei Startfälle PASS (ungeprüfte Testsite, bestätigte Testsite, Konflikt zu Legacy Plugin). In lokalen Startfällen 0 WordPress-Updates.
- 24/25 Funktions-/Backend-Fälle PASS; **1 FAIL: Seite Diagnose** wirft `K0_ARTICLE_TYPE_AUTHORITY_UNAVAILABLE`, da das Hobbydepot-Arbeitskopien-Manifest `K0_PORTAL_ADAPTER_PENDING` enthält.
- Unveränderter PSERC-Importer 5/5 PASS: validieren, Fehleingabe/Duplikat/Unbekanntes ablehnen, gültigen Artikel **als Entwurf** simuliert einfügen.
- **Zusätzlicher, neu nachgewiesener Ist-Zustand:** Beide tatsächlichen `wp_insert_post_data`-Filter halten einen vorhandenen mit `_texterstellung_order_id`/`_pserc_publish_blocked` markierten importierten Beitrag auch bei bewusstem Publish/Schedule auf `draft`. In vollständiger Filter-Mocksimulation: importierter Beitrag `publish → draft`; `future → draft`; anderer Beitrag `publish → publish`. Testschutz, keine Live-Veröffentlichungsfähigkeit.
- Keine reale WordPress-/DataForSEO-/MINI-/K0-End-to-End-Abnahme. K0-Hobby-Portalregistrierung ist im originalen K0-Current nur für `discgolf-beratung` belegt. Keine flächendeckende Freigabe.

## Ergebnis und nächster Schritt
Die **reine Bereinigung ist abgeschlossen**; unter dem vom Betreiber ausdrücklich auf Säuberung begrenzten Auftrag werden **keine** Änderungen an K0, Kategoriezuordnung, Diagnose oder Publish-Filtern vorgenommen. Die bereinigte 0.4.23-ZIP bleibt Testkandidat, **nicht auf Live installieren**. Nutzbare Produktionsfassung erfordert separaten, eng begrenzten Fehlerbehebungsauftrag und echte WordPress-Staging-/K0-Abnahme. Keine neue Pluginversion erzeugt.

Ausführliche Dateiberichte MD/JSON: `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/HOBBYDEPOT_0423_ECHTE_ABNAHMEGRENZEN_20261118.*`.
