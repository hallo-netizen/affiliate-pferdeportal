# Hobbydepot Texterstellung 0.4.24.15 – getrennte MINI-Reiter wie Pferdeatelier (20.11.2026)

## Nutzerauftrag
MINI-Import und MINI-Export im WordPress-Backend trennen, jeweils eigenes Untermenü und eigener Reiter; am bestehenden Pferdeatelier orientieren. Keine neue Fachlogik, keine Neuinstallation.

## Tatsächlich verwendete Quellen
- Pferdeatelier Original `Texterstellung-0.4.34-MANUELLES-VEROEFFENTLICHEN.zip`: bestehende Reiter `mini-export` und `mini-import`, getrennte Formulare, Reihenfolge, navigierbare Schritte, Alias `redaktion` → `mini-export`.
- Bereits installierte Hobbyversion `Texterstellung_Hobbydepot_0.4.24.14_ORIGINAL_RECHERCHE_FIX.zip`.
- Neuer User-Export `texterstellung-mini-gesamtauftrag (1).json`, Batch `mini-20261120094038-87239ec1a38a`: 20 Items, `resume_checkpoints[].next=EDITORIAL` für alle 20; Kategorie bereits bei 3 FACH / 17 REDAKTIONSBUERO im bisherigen MINI-Import bestätigt.

## Änderung, ohne neue Fachentscheidung
Eine einzige geänderte Datei `texterstellung-hobbydepot/texterstellung.php` (Version 0.4.24.14→0.4.24.15, getrennte Admin-Reiter, Formulare und Links). Alle übrigen 88 Dateien byteidentisch. Originale Worker `seoExport`, `seoImport`, Recherche, PAA, K0 und PSERC-Import unverändert. MINI-Export ruft bestehendes `txe_seo_export` auf; bei aktivem Batch lädt dieselbe Originalfunktion den gespeicherten Frozen-Batch ohne Mutation. MINI-Import verwendet dasselbe `txe_seo_import` und JSON-Feld `mini_file`. Die Redaktionsplan-Leseansicht wird wie Pferdeatelier auf `mini-export` abgebildet. Kein zweiter MINI-Auftrag, keine Providerkosten.

## Lokal ausgeführte Tests
- **23/23 Prüfgruppen PASS**; 80/80 PHP-Dateien Syntax PASS; ZIP 89 Dateien, CRC PASS.
- PHP-Rendering mit tatsächlicher `TXE_Workshop::page()`: 2 neue WP-Untermenüs/2 Reiter, korrekte Reihenfolge, nur Exportformular auf Export, nur Importformular auf Import, gesetzter Reiter, vorhandene alte Redaktionsplan-View, leerer Stand.
- Originaler `seoExport` mit gespeichertem 20er Batch: exakt dieselbe Batch-ID, Quelle und Items, 20 × EDITORIAL, kein State-Write.
- Original `seoImport` 20er CATEGORY-Checkpoint inkl. Wiederholung, manipuliertem Keyword, falschem Hash, ungültiger Kategorie, nicht unterstütztem K0-Typ besteht.
- Original technische Recherche→MINI→K0→WP-Entwurf-Integration, Queue-Aktionen, Ajax und negative Tests laufen nach UI-Änderung weiterhin.
- 88/89 Quelldateien unverändert, alle `original/pste` Bytes identisch.

## Release
Personal Library `/Hobby Depot/Plugin-Büro/Texterstellung_Hobbydepot_0.4.24.15_MINI_EXPORT_IMPORT_GETRENNT.zip` (519326 Bytes, SHA256 `655e5510df4355c0ba1ba3c807ff83c004002eab47626411481b08a3f3a5e5bd`).
Prüfprotokoll `Hobbydepot_0.4.24.15_MINI_UI_PRUEFBERICHT.json` und Installationshinweis `Hobbydepot_0.4.24.15_INSTALLATION_UND_PRUEFUNG.md` ebenfalls abgelegt. **Ersatz über denselben WP-Pluginordner** `texterstellung-hobbydepot/`, kein weiteres Plugin.

## Exakte Grenze
Echte Live-Installation der neuen UI noch durch Nutzer notwendig, dann Frontend ansehen. Keine Behauptung eines neu geschriebenen K0-Hobbyartikels; K0 Writer/LanguageTool 6.8 für diesen aktuellen Batch weiterhin nicht live bestätigt. MINI nächster Worker **EDITORIAL**, nicht CATEGORY erneut.
