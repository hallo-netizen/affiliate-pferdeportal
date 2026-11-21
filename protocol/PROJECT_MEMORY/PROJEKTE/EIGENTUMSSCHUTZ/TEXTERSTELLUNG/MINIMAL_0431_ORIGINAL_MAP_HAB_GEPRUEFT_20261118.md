# Fortsetzung 18.11.2026 – Original-Kategorie-Map Hab direkt geprüft

**Keine Plugin-Funktionsänderung, keine neue Architektur, kein Fix, kein neuer ZIP-Bau.** Die beiden vorhandenen 0.4.31.1 Minimal-Kopien und das 0.4.31-Pferdeatelier-Original sind unverändert. Kein Installationsrelease.

## Archiv und Quellbelege
- Historisches tatsächliches Hab-WP-Readback vom 13.10.2026 (`KATEGORIEN/C22_13OKT_POSTSYNC_93_SEITEN_285_WP_IDS_SLUGS_GESCHUETZT_20261016.json`): 285 Content-`category`-Terme unter 93 R3-Seiten; 87 R3 mit drei, sechs R3 mit vier flachen Kategorien. **0/285** mit `article_type`-Feld im Archiv und **0/285** mit Artikeltyp-Präfix nach der Original-PSTE-Regel. Readback selbst ausdrücklich historisch und nicht aktueller Live-WP-Stand.
- Tatsächlich geprüfte Quellteile des originalen Hab-Kategorie-Workflows: `ORIGINAL_EXTRACT_class-apkw-target-tree-sync.php.txt`, `class-apkw-c22-472-add-only.php`, `class-apkw-insurance-c26-depth.php`. Sie sichern WP-Knoten- und R3-Eltern-Kennungen, aber dort ist kein fertiges `pste_article_type` bzw. `article_type` pro Kategorie zu finden. Das ist eine Aussage **über diese geprüften Quellen, nicht über alle heutigen Live-Metadaten**.
- Original-Plugin 0.4.31 Map-Vertrag `PSTE_PORTAL_CATEGORY_MAP_V1` und Original-`PSTE_Snapshot` direkt ausgeführt; die Karte verlangt exakt Slug, Name, `article_type`, Produkt-/R3-Seitenslug und Name sowie eine gültige Inhaltsprüfsumme.

## Originalfunktionen ohne Änderungen ausgeführt – sechs Tests PASS
- Positive reine Daten-/WordPress-Mock-Probe: HISTORISCHER Hab-Name `Türen & Fenster` + historischer Slug; synthetische dreistufige Seitenkette und ausdrücklich **synthetisch** eingesetzte Artikelart, ohne Hab-Entscheidung vorzutäuschen. Für `Beratung`, `FAQ`, `Pflege`, `Vergleich`, `Anleitung`: **5/5 PASS** mit Original-`PSTE_Portal_Category_Map::load/match` und Original-`PSTE_Snapshot::structure`, validierter Kategorie/Seitenroute; es wurde KEIN PHP-Code des Plugins geändert.
- Negativprobe bei absichtlich fehlender Artikelart: **1/1 PASS**, der Original-Lader verweigert korrekt mit `PSTE_PORTAL_CATEGORY_MAP_ENTRY_INVALID`.
- Der originale `PSTE_Normalizer` erkennt die vier Namenspräfixe Beratung/FAQ/Pflege/Vergleich; `Anleitung` nicht als Präfix, **aber die geschützte Kategoriekarte akzeptiert Anleitung bei expliziter Angabe**. Diese Feststellung ist kein nachgewiesener vollständiger K0-Reallauf.

## Präzisiertes Fazit
**Rein technisch können Hab-Kategorien ohne Codeumbau im Original-Kategoriekarten-Format dargestellt werden, sofern eine valide und verbindliche Kategorie->Artikelart-Entscheidung bereits existiert.** Die bestehende Hab-Kategorieverwaltung liefert in den geprüften Unterlagen WordPress-Knoten und Elternseiten, **aber keine solche Einzelartikelart-Zuordnung**. Hab-Kategorien sind Themenrubriken; die K0-Artikelart wird separat bei der Texterstellung festgelegt. Eine synthetische Festzuweisung an reale Hab-Kategorien wäre eine unzulässige neue fachliche Entscheidung. Daher weiterhin keine Freigabe. Anderslautende pauschale Formulierungen wie 'die Map selbst kann keine Hab-Namen akzeptieren' sind durch die heutige Originalcode-Probe präzisiert: das Format ist kompatibel, die echte Fachzuordnung nicht nachgewiesen.

## Tatsächliche interne Ablage
- Hab-Büro: `/hab-und-bewahr/TEXTERSTELLUNG/ARBEITSKOPIEN/MINIMAL_ORIGINAL_0431/PRUEFUNG_ORIGINAL_MAP_20261118/`.
- Universal-Büro: `/texterstellung-universal/ENTWICKLUNG_20261118/MINIMAL_ORIGINAL_0431/PRUEFUNG_ORIGINAL_MAP_20261118/`.
- Jeweils erfolgreicher Upload von Beweisbericht (MD+JSON) und drei Originalklasse-Testskripten/Bauhilfe; alles **nur intern**, nicht als Download angeboten.

## Konkreter nächster erlaubter Schritt
Nur bereits existierende aktuelle verbindliche Quelle für `WP-Kategorieslug + echte R3-Seite + festgelegte Artikelart` finden, nicht raten. Falls fachlich nie vorgesehen, ist eine einfache Originalkopie zwar möglich, aber NICHT funktionsfertig für Hab; Zielvertrag muss dies offen benennen, keine zweite Architektur durch die Hintertür. Für echte K0-Produktion weiterhin K0-Portalkennung und realer WordPress-Lauf zu bestätigen.

**Unverändert:** Original-ZIP SHA256 `07b99fa549e87d28db53f0fac0b107c92a9f0de4a3de80ad5f31fb3b7b399f7d`; Hab-Minimal-ZIP `3f74e5c47f79ed36571dfc9a2adb63f639bdb9aafa294c19722ad2394fbe48d4`; Blanko-ZIP `cbbca4c2a2f1122198cb3cda927ab739ad94e9df87bf9ace28c9201a4f16dc4d`.

**Ausgabe-Regel:** Nur tatsächlich zur Installation freigegebene Plugins im Chat. Keine QA-/Testdateien als Download.