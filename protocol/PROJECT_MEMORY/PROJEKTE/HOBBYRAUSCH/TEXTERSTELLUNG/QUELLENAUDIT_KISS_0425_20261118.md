# Hobbydepot Texterstellung – exakter Quellcode-Audit und Korrektur 0.4.25

**18.11.2026 · Status: NUR ARBEITSKOPIE, NICHT INSTALLIEREN.**

## Nachweisstand
- Quellen: vollständig entpackte Hobbydepot 0.4.23-Arbeitskopie, 0.4.24-Installationskandidat und originaler K0-0.4.23-Quellstand. Gegen den verbindlichen MINI-/K0-/Entwurfsimport-Vertrag verglichen.
- 0.4.24 hatte weiterhin ausführbare Pferde-Journalregeln, Pferde-Sonderrouten und Pferde-Titel-Ausnahmen. Außerdem verhinderte ein `wp_insert_post_data`-Filter die spätere bewusste manuelle Veröffentlichung vorhandener Entwürfe; die Diagnose stufte veröffentlichte Artikel als Fehler ein. Die ursprünglich behauptete vollständige Entkopplung war deshalb falsch.
- Hobbydepot HD004 ist die einzig autorisierte Kategorie-/Parent-/WordPress-Mappingquelle. PSTE-Alt-Snapshot verwendet abweichende, nicht verifizierte Fachzuordnung; keine Ableitung aus Kategorientiteln als Ersatz.
- Überarbeitete **HOBBYDEPOT_TEXTERSTELLUNG_0.4.25_ARBEITSKOPIE_NICHT_INSTALLIEREN.zip** liegt im Dateienbüro unter `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/`. SHA256 `d16f0950de6792313a1e9894740a51f15e92b20644d7584d04a06d75b8e2cde7`.
- Prüfbericht MD + JSON: `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/`.
- 88/88 Quelldateien enthalten, 79/79 PHP-Lint PASS, 13 geändert, 75 unverändert, ZIP-CRC PASS und Quellcode-Bytevergleich PASS. 16/16 lokale Vertragsprüfungen, 4/4 Starttests. Kein echter WordPress-E2E-Test.
- Nach fachlichem Volltextscan **genau zwei** historische Pferde-Namensbezüge, beide die identische externe K0-Rückgabekennung `PFERDE_ATELIER_WORDPRESS_IMPORT_V1`: eine Konstante im erhaltenen PSERC-Originalimporter, eine entsprechende Kennung in Texterstellung. Keine Pferde-Sonderfunktion, kein Themen-, Kategorie- oder Seed-Inhalt mehr. K0-Vertragsname NICHT blind umbenennen: Kompatibilität sonst zerstört.
- Original-PSERC-Importer inklusive vier PHP-Quelldateien sowie K0-Fünffeldvertrag byteidentisch erhalten; Pferdeatelier und Original-K0 nicht verändert.
- Journal, Tarife und sonstige fachfremde Routen entfernt; nur K0; manuelle Veröffentlichung wird nicht durch eigenes Plugin geblockt. Die Diagnose behandelt spätere bewusste Publikation nicht mehr als Importfehler.
- Datenseitige und fachliche Verarbeitung bleibt vor der **einmaligen** HD004→PSTE-Portal-Anbindung geschlossen: keine kostenpflichtige Recherche, kein MINI-Ergebnisimport, kein K0-Export und kein Entwurfsimport. Kein Revival eines alten Worker-Auftrags.
- Keine doppelte SEO-/Kategorie-/Titelentscheidung eingeführt; Sperre ist technische Startvoraussetzung. WordPress-/HD004-Echtstand noch nicht unabhängig ausgelesen.

## Genau ein nächster Arbeitsblock
Die tatsächlich aktive HD004-Snapshot-Struktur read-only aus der Zielwebsite mit den echten Zuordnungen zu WP-Kategorien, Hobbyseiten und Artikelarten an das Texterstellungskonzept anbinden. Danach EIN kompletter echter Durchlauf Recherche → MINI → K0 → WordPress-Entwurf + manuelle Veröffentlichungsprobe. Erst anschließend **installationsfähige** eigenständige Hobbydepot-Fassung freigeben. KEINE Installation von 0.4.25.

## Unverändert
Alle 0.4.23- und 0.4.24-ZIPs, Original-Plugin Pferdeatelier, ursprüngliche K0-Regeln, WordPress-Bestandsartikel und HD004-Kategorie-Quelle.
