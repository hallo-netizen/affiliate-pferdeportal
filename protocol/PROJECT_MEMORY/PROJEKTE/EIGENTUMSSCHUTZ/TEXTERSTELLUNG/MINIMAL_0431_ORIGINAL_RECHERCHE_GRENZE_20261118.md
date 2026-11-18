# 18.11.2026 – Fortsetzung ohne Zwischenstopp: Original-Recherchevertrag vollständig abgegrenzt

**Nur bestehende Originalfunktionen ausgeführt. Keine Änderung am Plugincode, keine neuen Klassen, keine Architekturänderung, keine Fixes, keine Freigabe.** Nutzervorgabe: als reine Minimal-Kopien aus dem Pferdeatelier-0.4.31-Original fortsetzen, nur Pferdebezüge neutralisieren.

## Durchgeführte tatsächliche Arbeit
- Drei Quellen unverändert nachgeprüft: Pferdeatelier-Original 0.4.31, Hab-Minimal-Kopie 0.4.31.1 und Universal-Blanko 0.4.31.1.
- Bestehendes Hab-Kategorienmaterial verwendet. Nutzer bestätigt ausdrücklich, dass seit dem gespeicherten Stand keine neuen Kategorien hinzugekommen sind. Vorhandener archivierter WP-Readback: 285 flache Fachkategorien, 93 R3-Themenseiten; keine feste `article_type`-Angabe pro Term. Keine neue Bestandsaufnahme verlangt, keine Kategorie ergänzt.
- Original-`PSTE_Portal_Category_Map::load()` benötigt eine nichtleere Prüfsummen-Karte mit `article_type` je Term. `PSTE_Snapshot::structure()` verwendet sie vor MINI und DataForSEO. Der original bewahrte `TXE_Workshop` kann im MINI dagegen Kategorie und K0-Schreibartikelart unabhängig auswählen. Der bereits frühere 21/21-MINI-Test bleibt gültig. MINI und K0 brauchen **keinen** Umbau.
- Neuer isolierter realistischer R3-Gegenversuch: die echten Hab-Termnamen `Türen & Fenster` (WP-Term 183) und `Schlüssel & Zutritt` (WP-Term 185) unter echter R3-Seite `Mechanik & Zugang` (WP-Page 157). **Nur Testdaten**, keine echten Artikelartentscheidungen. Haben beide die künstlich pauschale Artikelart `Wissen`, nimmt Original-`PSTE_Snapshot` genau einen Term auf und quarantänisiert den anderen mit `PSTE_PORTAL_CATEGORY_DUPLICATE_FAMILY_TYPE_QUARANTINED`. Mit *zwei unterschiedlichen ebenfalls künstlich zugewiesenen* Typen nimmt es beide auf. Das beweist: Pauschaltypen würden originale Kategorien **still verlieren**, nicht die Hab-Anbindung lösen.
- Derselbe unveränderte PHP-Test erfolgreich mit **Original, Hab und Blanko**: jeweils 2 Szenarien, insgesamt **6/6 PASS**.
- Zweiter belegt fehlender Datenanschluss: originale `PSTE_Journal_Article_Type`-Definition hat 9 fest gebundene Kategorien; Hab- und Blanko-Kopie haben nach Entfernung der Pferdedefinitionen **0**. `TXE_Workshop::magazineCategoriesFromTree` kann daraus keinen zulässigen MAGAZIN-Unterkategorien-Slug liefern. Keine falsche Magazinzuordnung erfunden.
- Alle drei bestehenden ZIPs neuerlich CRC-PASS: Original SHA256 `07b99fa549e87d28db53f0fac0b107c92a9f0de4a3de80ad5f31fb3b7b399f7d` (88 Dateien); Hab `3f74e5c47f79ed36571dfc9a2adb63f639bdb9aafa294c19722ad2394fbe48d4` (87 Dateien); Blanko `cbbca4c2a2f1122198cb3cda927ab739ad94e9df87bf9ace28c9201a4f16dc4d` (87 Dateien). Keine neue Pluginversion erstellt.

## Tatsächlich gespeicherte Testdokumente
- Hab-Büro: `/hab-und-bewahr/TEXTERSTELLUNG/ARBEITSKOPIEN/MINIMAL_ORIGINAL_0431/PRUEFUNG_ORIGINAL_RECHERCHE_20261118/`.
- Universal-Büro: `/texterstellung-universal/ENTWICKLUNG_20261118/MINIMAL_ORIGINAL_0431/PRUEFUNG_ORIGINAL_RECHERCHE_20261118/`.
- In beiden: `PRUEFPROTOKOLL_ORIGINAL_VERTRAEGE_20261118.md`, `ORIGINALTEST_VERGLEICH_20261118.json`, `run_and_log.py`, `test_original_siblings.php`, `build_fixtures.py` – jeweils Upload mit `succeeded` bestätigt. Test-Fixtures liegen separat lokal, **nie** in einem Plugin.

## Abschließende technische Grenze der beauftragten reinen Kopie
Eine **vollständige** Hab-Textproduktion ist mit *ausschließlich Pferdebegriffe auskommentieren* nachweislich nicht möglich. Grund: Original-PSTE verlangt eine feste Kategorievariante je Hab-Fachkategorie und untersagt doppelte Varianten pro R3; Hab hat thematische Kategorien und wählt K0-Schreibartikelart erst einmalig im unveränderten MINI. Zusätzlich sind alte signierte Magazin-Definitionen portalgebunden. Die bisherigen Originalkopien sind korrekte **Blanko-Quellkopien**, aber keine freigegebene Produktionslösung.

Die fachlich nötige Portalanpassung wäre eine *minimal begrenzte Änderung der bestehenden Original-Kategorien-Lesestelle* und anschließender Magazin-Anschluss, **nicht** neue Architektur oder ein zweites System. Der Nutzer hat jedoch ausdrücklich `keine Fixes, keine neue Architektur, nur auskommentieren` angeordnet. Daher **nicht eigenmächtig umgebaut**, keine Fantasie-Artikeltypen und keine falsche Freigabe erteilt.

**Ausgaberegel bleibt:** nur tatsächliche fertig freigegebene installierbare Plugin-ZIPs zum Download im Chat. QA-Dateien und Entwicklungsarchive nur im Büro. Original-Pferdeatelier, K0, DataForSEO, WordPress und Bestandsdaten unverändert.