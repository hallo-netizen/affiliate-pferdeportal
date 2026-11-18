# Hobbydepot – Texterstellung 0.4.26 | 18.11.2026

**Status: QUELLE VORBEREITET, NICHT INSTALLIEREN, KEINE PRODUKTIONSFREIGABE.**

## Belegt
- Original-HD004-Plugin 1.0.0 `CURRENT.zip` vollständig aus dem GitHub-Blob geöffnet und tatsächlichen PHP-Quellcode gelesen: API `hd_category_registry_contract/ready/revision/snapshot/node/mapping` vorhanden. Es liest ausschließlich `apkw_target_tree_active_revision_v1` und `apkw_target_tree_active_snapshot_v1`.
- HD004 `ready()` bestätigt bei aktiver Revision nur Grundstruktur (`nodes` und `mapping`), **nicht** fachliche Artikelart-Anbindung und nicht die tatsächlich aktuellen WordPress-Inhalte.
- In der separaten Hobbydepot-Texterstellungs-Arbeitskopie 0.4.26 wurde eine **read-only-Bestandsaufnahme in die vorhandene Diagnose integriert** (kein weiteres Plugin). Meldet nur Knoten, Kategorien, WordPress-Objektbezüge, fehlende Eltern, doppelte IDs, Revisionskonflikte. Keine zweite Freigabe, keine Taxonomie-Schreiboperation, kein DataForSEO-Aufruf.
- **PHP-Lint 80/80 PASS**, **ZIP 89/89 PASS**, **10/10** neue synthetische HD004-Vertragsproben, **16/16** bestehende statische Vertragstests und **4/4** Bootstrap-Domain-Tests bestanden.
- **Vier PSERC-Originalimportdateien identisch** zur 0.4.25; zwei historische `PFERDE_ATELIER_WORDPRESS_IMPORT_V1`-Kennungen absichtlich unverändert als externes K0-Rückgabeformat. Pferde-Sonderregeln werden nicht wiedereingeführt.
- Separate Arbeitskopie `HOBBYDEPOT_TEXTERSTELLUNG_0.4.26_QUELLE_NICHT_INSTALLIEREN.zip` im Dateienbüro `/hobbydepot/TEXTERSTELLUNG/ARBEITSKOPIEN/` (497bec8ecc2b4df3f971f0802fb07abd183129b5c2b8051a85f6fc20607eeaef SHA-256).
- Ausführlicher Bericht als MD + JSON unter `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/`.

## Der eine offene Block
Die tatsächlich aktiven, ausgefüllten HD004-Knoten und Zuordnungen aus hobbydepot.de sind bislang NICHT live ausgelesen. Die alte PSTE-Recherche leitet ihre Kategorien teils aus einer Pferde-Drei-Seiten-Struktur ab. Diese ist für Hobbydepot nicht bewiesen. **0.4.26 setzt binding_ready niemals auf true; sämtliche produktiven Aktionen bleiben gesperrt.** Keine reale WordPress-/DataForSEO-/MINI-/K0-/WP-Import-Abnahme.

## Wer macht was
1. Entwickler/Assistent: **eine einzige** kategorieneutrale HD004→PSTE-Fachbindung aus dem echten HD004-Kategorieregister ohne zweiten Kategoriemaster erstellen und lokal testen; den bisherigen zentralen K0-Vertrag beibehalten.
2. Betreiber: jetzt **nichts installieren** und keinen neuen paid Providerlauf auslösen. Falls der exakte Live-Snapshot zur Abnahme gebraucht wird: bestehende WordPress-/HD001-Exportfunktion anhand konkreten echten Klickpfades verwenden, nicht ungeprüfte Backend-Menüs oder zusätzliche Diagnose-Plugins erfinden.
3. Bei einer tatsächlich getesteten Installationsfassung: eine Installation und ein realer Testlauf; Assistent wertet dessen Bericht aus und aktualisiert **dieses** Protokoll.

## Unverändert
Hobbydepot-HD004, HD001, WordPress-Artikel, PSTE/PSERC/K0-Originalworkflow, Versionen 0.4.23 bis 0.4.25.
