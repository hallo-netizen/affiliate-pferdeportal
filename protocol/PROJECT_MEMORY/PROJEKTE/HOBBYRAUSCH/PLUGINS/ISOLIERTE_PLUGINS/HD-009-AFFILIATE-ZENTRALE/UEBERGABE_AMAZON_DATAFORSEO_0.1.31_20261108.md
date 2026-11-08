# Hobbydepot – HD009 Amazon/DataForSEO – verbindliche Übergabe 08.11.2026

## Wo stehen wir?
- **Aktuelle GitHub-Version:** `HD009 Affiliate-Zentrale 0.1.31`; originales WordPress-Plugin bleibt `affiliate-portal-router/`.
- **Installationsdatei:** `HOBBY_DEPOT_AFFILIATE_HD009_0.1.31.zip` und `CURRENT.zip` **byteidentisch im selben Plugin-Büro**; Git-Blob `1e3a1370d22de5a54717ff960fccacd10366bfc1`, Größe **1.563.011 Bytes**, SHA-256 `3b3d65bd534a249c6ac645a20eac3da9aae68c7e82e52ad7e121639399b46e87`.
- Hauptprotokolle: `PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/MANIFEST.md`, `PLUGINS/PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/CURRENT.md`, `AFFILIATE/CURRENT_STATE.md`, `AFFILIATE/DATAFORSEO_HAB_ABGLEICH_HD009_0.1.31_20261108.md`.
- **KISS und Portaltrennung:** Kein neues Plugin, keine WordPress-Core-Änderungen, keine neue Produkttabelle und keine Hab-Datenübernahme. HD003 Design **1.50.806** (Nutzer: „erst einmal okay, bis auf Kleinigkeiten“) und HD006 **Bildzentrale** strikt getrennt und unverändert.

## Geprüft und umgesetzt
- Die bestehende Amazon/DataForSEO-Funktion wurde im HD009 um einen **standardmäßig ausgeschalteten** automatisch wiederholten Rechercheablauf ergänzt. Zuerst ein **kostenfreier Prüfknopf** im vorhandenen Amazon-Backend, der den nächsten tatsächlich zugeordneten Beitrag und dessen Ausrüstungssuchwort anzeigt.
- Die ausdrücklich freizugebende Automatik nutzt `task_post` für maximal **5 neue bezahlte Aufgaben pro UTC-Tag** (vor dem POST reserviert) und `task_get/advanced` zum Abruf offener Aufgaben. Keine doppelte Bezahlung, bei Fehlern Sperre, sichtbarer Status.
- Fachquelle: **HD007** 862 Hobbyregister-Einträge; **HD003** 381 aktive Hobbyziele. Strenger Filter: **235 mögliche Suchwort-Kandidaten**. Veröffentlichung nur bei tatsächlicher Ziel-/Titelpassung und amazon.de-Host, gültiger ASIN; max. drei passende ASINs im **bestehenden** Produktspeicher. Keine DataForSEO-Bilder oder -Preise übernehmen.
- **Harter Offline-Test:** GitHub Action **42496624037**: 41/41 ZIP-CRC, 24/24 PHP-Syntax, tatsächliche PHP-Ausführung mit Original-Hobbydaten und simuliertem DataForSEO POST/GET; freies Prüfen, Tageslimit, Doppelaufrufsperre und Fehlerabschaltung PASS.
- **Weder produktiv installiert noch live abgenommen**, keine echten DataForSEO-Abfragen oder Gebühren bei den Tests nachgewiesen.

## Noch offen / nicht behaupten
1. **Zulässige automatische Amazon-Produktbildquelle** über tatsächlich autorisierten Amazon-Zugang/Feed; ohne diesen sind die von DataForSEO gelieferten ASINs noch keine bebilderten Amazon-Produktkacheln.
2. **eBay/Idealo-Vorrang und korrektes Kartenlayout**: Quellbilder bei beiden Anbietern grundsätzlich vorhanden, aber der gemeinsame Produktkarten-/Vorrangablauf ist noch nicht durchgängig live belegt. Experiment HD009 **0.1.30** auf separatem Branch war **fehlgeschlagen** und ist NICHT CURRENT.
3. Kostenfreie Vorprüfung nach Installation im Backend; anschließend **nur bei ausdrücklich bewusster Freigabe** maximal einen kostenpflichtigen Testauftrag durchführen. Frontend erst nach echten freigegebenen Produktdaten und Bildern beurteilen.
4. WordPress-Live-Installation 0.1.31, bestehende Amazon-/DataForSEO-Zugänge, Freigaben und API-Verfügbarkeit sind **nicht** durch die Offline-Tests verifiziert.

## Nächster Arbeitsauftrag
Zuerst aktuelle Original-Quellen/Status in **diesem** HD009-Büro kontrollieren, dann den kompletten Weg **Hobbyregister-Ausrüstung → konkretes Suchwort → DataForSEO-Auftrag → gültige Amazon-ASIN → lizenzierte Produktbildquelle → richtige echte Artikelproduktkarte → Anbieterpriorität eBay/Idealo** testen und vervollständigen. **Ursachen statt einzelne Symptome**, keine falschen/verwandten Fotos, keine leeren Werbekacheln und keine zusätzlichen Parallel-Workflows. Erreichten Design-PASS nicht versehentlich zerstören.
