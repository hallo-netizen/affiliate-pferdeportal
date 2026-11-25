# Pferdeatelier – Datenbank-Speicherbereinigung

Stand: 25.11.2026, fortlaufendes Protokoll

## Ausgangslage
- IONOS meldet Datenbank > 2 GB und hat neue Schreibvorgänge/INSERTs gesperrt.
- phpMyAdmin-Live-Datenbank: dbs15807722.
- WordPress-Datenbank laut Site Health zuvor ca. 1,45 GB Nutzdaten.
- IONOS zählt offenbar zusätzlich reservierten/freien Tabellenplatz.

## Größte Tabellen vor Bereinigung
- slfo_options: ca. 509,4 MB Inhalt + 5 MB frei.
- slfo_pste_candidates: ca. 303,6 MB Inhalt + 115 MB frei = ca. 418,6 MB reserviert.
- slfo_pste_runs: ca. 139,0 MB Inhalt + 221 MB frei = ca. 360,0 MB reserviert.
- slfo_ppar_ebay_items: ca. 167,4 MB Inhalt + 8 MB frei.
- slfo_pste_topic_pool: ca. 164,3 MB Inhalt + 4 MB frei.
- allein pste_candidates + pste_runs enthalten ca. 336 MB intern freien/reservierten Platz.

## Schreibsperre
- OPTIMIZE TABLE slfo_pste_runs scheiterte mit MySQL #1142: INSERT nicht erlaubt.
- Schluss: DELETE ist erlaubt, Neuaufbau/INSERT derzeit nicht.

## Bereits durchgeführt
1. WordPress-Transients aus slfo_options gelöscht:
   - DELETE auf _transient_% und _site_transient_%.
   - Ergebnis: 107 Datensätze gelöscht.
   - Funktion: temporäre Cache-Daten; keine Beiträge/Benutzer/normalen Einstellungen.

## Ursachenanalyse slfo_options
Größte Einzelwerte sichtbar:
- txe_legacy_shelf_backup_v1_... ca. 83,45 MB.
- pste_semantic_review_sandbox_v1 ca. 58,23 MB.
- mehrere pserc_plan_*_bootstrap_* jeweils ca. 9,90 MB.
- ppar_category_product_readonly_snapshot_v672124 ca. 3,34 MB.
- pste_site_baseline_v1 ca. 2,79 MB.
- ppm_v6_last_production_state_registry_export ca. 2,32 MB.
- wppd_last_report ca. 2,07 MB.
- zahlreiche txe_frozen_mini_v1_* ca. 0,4–0,5 MB pro Eintrag.

## Gruppenanalyse slfo_options
Aktueller Screenshot:
- PPAR / Affiliate: 103.925 Einträge, ca. 110,4 MB Werte.
- PSTE: 5.022 Einträge, ca. 99,0 MB.
- TXE / Texterstellung: 26 Einträge, ca. 93,0 MB.
- PSERC: 2.449 Einträge, ca. 60,1 MB.
- Sonstige: 607 Einträge, ca. 4,3 MB.
- PFTK: 38 Einträge, ca. 2,6 MB.
- PPM: 22 Einträge, ca. 2,4 MB.
- PABZ: 31 Einträge, ca. 1,7 MB.
- URF: 10 Einträge, ca. 0,7 MB.

Hinweis:
- InnoDB-Zeilenangaben in Tabellenübersichten können Schätzwerte sein; für Löschentscheidungen zählen konkrete Schlüssel/Datensätze und Byte-Summen.
- Noch keine großen Fach-/Produktivdaten gelöscht.
- Ziel bleibt KISS: erst schnell sicheren Platz schaffen, danach Ursachenbegrenzung im erzeugenden System.


## 2026-11-25 – Löschkandidaten nach Funktionsprüfung
- PSERC-Plan-Bootstrapdaten NICHT löschen: Projektquellen zeigen sie als aktive Compiler-/Workflow-Records.
- PSTE-Semantic-Sandbox NICHT blind löschen: Diagnosen zeigen aktive Nutzung durch den Recherche-/Sandbox-Workflow.
- txe_frozen_mini_v1_* NICHT löschen: gespeicherte/frozen MINI-Aufträge, Wiederaufnahmefunktion muss erhalten bleiben.
- txe_legacy_shelf_backup_v1_* als erster großer Löschkandidat freigegeben:
  - sichtbare Größe ca. 83,45 MB.
  - 0.4.55-Migrationsprüfung: Altarchiv wird auf kompakten Bestand reduziert (Test 156.486.315 -> 1.179.315 Bytes), der Backupstand bleibt dabei ausdrücklich separat erhalten.
  - aktive MINI/K0-Semantik wurde nach Kompaktierung unverändert geprüft; Backup ist Rückfall-/Archivstand, nicht der kompakte aktive Bestand.
- nachhaltige Ursache für diesen Block: Migrationsbackup wird nach erfolgreicher Kompaktierung nicht automatisch entfernt/begrenzt.
- nächster operativer Schritt: ausschließlich txe_legacy_shelf_backup_v1_* löschen; danach Speicherstand erneut messen.
