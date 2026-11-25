# Texterstellung 18.11.2026 – Recherche-Anbindung ohne Programmumbau geprüft

**Nutzerauftrag:** Keine neue Architektur, keine Neuentwicklung, keine Fixes, Original 0.4.31 nur portalbezogen säubern. Nur fertige produktive Plugin-ZIPs im Chat zum Download anbieten. Alles im Hab- und Universal-Büro protokollieren.

## Nachweis im aktuellen Arbeitsschritt
- Originalquelle unverändert geprüft: `PSTE_Portal_Category_Map::load`, `PSTE_Snapshot::resolveCategory/structure`, `PSTE_Article_Type_Registry`, `PSTE_Article_Type_Intent_Ontology` und `PSTE_Semantic_Retriever_A::retrieve`.
- Ein Datentrick `article_type = bestehender Hab-Kategoriename` ist **nicht** semantisch gleichwertig mit einer echten Artikelart. Der originale Retriever schätzt Suchabsichten gegen echte Typen wie Beratung/FAQ/Kosten ein.
- Isolierter unveränderter Original-PHP-Test mit Hab-Bestandsnamen `Türen & Fenster` und `Schlüssel & Zutritt` (synthetisches Registry-/WP-Szenario, keine echten Artikelart-Zuordnungen). `Fensterschloss` + Typ `Beratung` => `ASSIGNED`; derselbe Begriff + Typ `Türen & Fenster` => `BLOCKED`. Fragen werden nur mit `FAQ` zugeordnet, Kostenfragen nur mit `Kosten`. Zehn positive/negative Szenarien.
- **Pferdeatelier-Original 0.4.31: 10/10 PASS. Hab 0.4.31.1: 10/10 PASS. Universal 0.4.31.1: 10/10 PASS. Zusammen 30/30.** Tests liefen mit genau denselben vorhandenen PHP-Klassen, keine Änderung am Plugin.
- Alle drei ZIPs erneut ZIP-CRC PASS; SHA-256 erhalten: Original `07b99fa549e87d28db53f0fac0b107c92a9f0de4a3de80ad5f31fb3b7b399f7d`; Hab `3f74e5c47f79ed36571dfc9a2adb63f639bdb9aafa294c19722ad2394fbe48d4`; Blanko `cbbca4c2a2f1122198cb3cda927ab739ad94e9df87bf9ace28c9201a4f16dc4d`.
- **Keine neue Pluginversion, keine WP-Installation, keine K0-Änderung, keine DataForSEO-Anfrage**, keine Datenbank- oder Kategorieänderung.

## Keine falsche Freigabe
Das Original braucht in der *frühen Recherche* einen festgelegten Recherche-Artikeltyp je Kategorie/R3, der mit semantischer Typprüfung genutzt wird. Die vorhandenen Hab-Kategorien sind thematische Unterkategorien; die unabhängige K0-Schreibartikelart wird erst im unveränderten MINI gewählt. Bloßes Auskommentieren oder Befüllen der Konfigurationsdatei mit Kategorienamen stellt die vollständige Recherche nicht her; es würde passende Themen ausfiltern. Ohne zulässige Veränderung der existierenden PSTE-Kategorienlesestelle darf die reine Kopie nicht als voll produktives Hab-Plugin ausgegeben werden.

## Tatsächlich gespeicherte Ablagen
In beiden persönlichen Library-Büros unter `MINIMAL_ORIGINAL_0431/PRUEFUNG_SEMANTIK_OHNE_UMBAU_20261118` sind nach erfolgreichem Upload vorhanden:
- `ARBEITSPROTOKOLL_20261118.md`
- `RECHERCHE_TYPEN_TEST_20261118.json`
- `ORIGINALFUNKTIONEN_TEST_SEMANTIK.php`

Die bisher archivierten Original-/Hab-/Blanko-Plugin-ZIPs bleiben unverändert und nur intern; Downloads ausschließlich bei nachgewiesener voller Funktionsfreigabe.

**Nächster technisch nötiger Punkt, aber aktuell nicht autorisiert:** eine kleine Anpassung der bereits bestehenden PSTE-Kategorie-Lesestelle, nicht ein Neubau. Bis dahin keine falsche feste Typzuweisung und kein Installationsrelease.
