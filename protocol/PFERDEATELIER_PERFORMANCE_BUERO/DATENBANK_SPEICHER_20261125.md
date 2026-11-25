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


## 2026-11-25 11:51 – erster großer Altbestand gelöscht
- SQL: DELETE FROM slfo_options WHERE option_name LIKE 'txe_legacy_shelf_backup_v1_%';
- Ergebnis laut phpMyAdmin: 1 Datensatz betroffen.
- gelöschter Alt-/Migrationsbackupwert zuvor ca. 83,45 MB.
- aktive txe_frozen_mini_v1_*-Aufträge, PSTE-Sandbox und PSERC-Workflowdaten ausdrücklich nicht angefasst.
- nächster Schritt: slfo_options Größe + data_free unmittelbar neu messen; danach entscheiden, ob Löschung bereits Quota reduziert oder zunächst nur internen freien Platz erzeugt hat.


## 2026-11-25 11:52 – Wirkung der 83,45-MB-Löschung gemessen
- slfo_options nach Löschung: Inhalt weiterhin ca. 509,4 MB.
- data_free stieg von ca. 5 MB auf ca. 100 MB.
- Schluss: Datensatz ist logisch entfernt, aber InnoDB hat den Tabellenplatz nur intern freigegeben; physische Tabellenbelegung/Quota wurde noch nicht reduziert.
- Damit reicht weiteres DELETE allein voraussichtlich nicht, um IONOS-Speicherquota sofort freizugeben.
- nächster KISS-Schritt: nach der großen Löschung OPTIMIZE erneut testen. Falls IONOS die Schreibsperre weiterhin blockiert, ist physische Freigabe nur über eine DDL-Operation (Rebuild/Truncate/Drop einer nachweislich entbehrlichen Tabelle) möglich; keine produktive Tabelle blind anfassen.


## 2026-11-25 11:54 – physische Gesamtbelegung gemessen
- Belegt inkl. intern freiem Tabellenplatz: 2033,3 MB.
- echter Tabelleninhalt: 1489,3 MB.
- intern frei/reserviert: 544,0 MB.
- Schluss: Quota-Problem ist überwiegend reservierter InnoDB-Platz, nicht 2+ GB echte Nutzdaten.
- Ziel zur Entsperrung: ca. 35–50 MB physisch freigeben; danach OPTIMIZE der großen Tabellen möglich.
- kleinster sicherer Kandidat: slfo_relevanssi, ca. 35,7 MB reserviert; reine Relevanssi-Suchindextabelle, aus WordPress-Inhalten neu aufbaubar.
- geplanter KISS-Schritt: TRUNCATE TABLE slfo_relevanssi; Schema bleibt bestehen, nur Suchindex wird geleert. Danach Gesamtbelegung neu messen und Relevanssi nach Entsperrung neu indizieren.


## 2026-11-25 – Relevanssi verworfen, Legacy-PPM/POC als nächster Kandidat
- Relevanssi NICHT löschen/truncaten: aktive Nutzung der Suchfunktion nicht eindeutig ausgeschlossen.
- neuer KISS-Kandidat: alte Tabellenfamilien slfo_ppm*, slfo_ppm679*, slfo_poc100*.
- aktueller GitHub-Codebestand vollständig nach exakten Namen durchsucht:
  ppm679_runs, ppm679_items, ppm679_fact_packs, ppm679_tombstones,
  ppm_batches, ppm_bootstraps, ppm_certifications, ppm_plans,
  poc100_authorizations, poc100_events, poc100_evidence_refs.
- Ergebnis: 0 aktuelle Code-Treffer auf diese Tabellennamen.
- zusätzliche Suche nach dynamischer Bildung mit $wpdb->prefix + ppm_/ppm679_/poc100_ sowie table('plans'/'certifications'/'runs'/'items'/'fact_packs'): 0 Treffer.
- aktuelle aktive WordPress-Pluginliste enthält kein eigenständiges PPM/POC-Plugin.
- letzter Diagnosebestand enthält 7 PPM-Tabellen mit zusammen ca. 14,2 MiB Nutzdaten+Index; aktuelle phpMyAdmin-Seitenleiste zeigt zusätzlich weitere Legacy-PPM/POC-Tabellen.
- nächster Schritt: aktuelle physische Belegung dieser Legacy-Tabellenfamilien direkt in information_schema summieren; erst danach gebündelte Löschfreigabe.


## 2026-11-25 – GRUNDDIAGNOSE DATENBANK

### Harte Zahlen
- physisch/reserviert belegt: 2033,3 MB.
- echter Inhalt nach erster Bereinigung: 1489,3 MB.
- intern frei/reserviert: 544,0 MB.
- damit besteht das IONOS-Limitproblem primär aus nicht zurückgegebenem InnoDB-Speicher, nicht aus >2 GB echtem Inhalt.

### Größte Fragmentierungsblöcke
- slfo_pste_runs: ca. 221 MB intern frei.
- slfo_pste_candidates: ca. 115 MB intern frei.
- slfo_options: nach Löschung des TXE-Legacy-Backups ca. 100 MB intern frei.
- slfo_ppar_creative_library: ca. 23 MB intern frei.
- diese vier Blöcke erklären zusammen ca. 459 MB bzw. rund 84 % des gesamten internen Leerraums.

### Wachstum Live 21.11. -> 25.11.
Vergleich derselben Live-Datenbank aus Diagnose 20261121-082829 gegen 20261125-102437:
- slfo_options: + ca. 104 MB physischer Daten+Index.
- slfo_relevanssi: + ca. 15 MB.
- slfo_posts: + ca. 5,1 MB.
- slfo_postmeta: + ca. 4,0 MB.
- slfo_pste_candidates: 0 MB Wachstum.
- slfo_pste_runs: 0 MB Wachstum.
- slfo_pste_topic_pool: 0 MB Wachstum.
- slfo_ppar_ebay_items: 0 MB Wachstum.
=> jüngstes reales Wachstum kommt fast vollständig aus slfo_options; die sehr großen PSTE/eBay-Tabellen sind aktuell groß, aber im Messfenster nicht weiter gewachsen.

### Options-Aufteilung aktuell
- PPAR / Affiliate: ca. 110,4 MB Option-Werte.
- PSTE: ca. 99,0 MB.
- TXE / Texterstellung: ca. 93,0 MB.
- PSERC: ca. 60,1 MB.
- damit liegen rund 362,5 MB der großen Options-Werte in eigenen Portal-/Workflow-Systemen.

### Wichtigster Ursachenbefund
1. Langfristige Ursache A: Systeme mit häufigem Schreiben/Löschen/Umschreiben erzeugen große InnoDB-Tabellen mit starkem internem Leerraum; Speicher wird ohne Rebuild/Optimize nicht an IONOS zurückgegeben.
2. Langfristige Ursache B: slfo_options wird als Ablage für sehr große Zustands-, Backup-, Sandbox- und Workflowobjekte benutzt. Das ist für dauerhaft große Daten ungeeignet und erzeugt zusätzlich Wachstum/Fragmentierung.
3. Das aktuelle Limitproblem ist daher eine Kombination aus:
   - echtem Wachstum insbesondere in slfo_options,
   - plus rund 544 MB nicht zurückgegebenem Leerraum.
4. Weitere DELETEs allein senken die IONOS-Belegung nicht zuverlässig; sie erhöhen zunächst nur data_free.
5. Der nachhaltige Fix muss deshalb beides lösen:
   - große/temporäre Workflowdaten begrenzen/aus options heraus bzw. automatisch bereinigen,
   - regelmäßige kontrollierte physische Tabellenkompaktierung bzw. Speicherrückgabe ermöglichen.

### Aktueller Handlungsweg
- keine Relevanssi-Aktion als Standardlösung.
- keine PPM/K0-Tabellen löschen.
- zuerst minimal physisch unter IONOS-Limit kommen, aber nur mit nachweislich entbehrlicher/rekonstruierbarer Struktur.
- danach sofort die großen Fragmentierungsblöcke optimieren, insbesondere pste_runs, pste_candidates und options.
- anschließend Ursachenfix in den erzeugenden Plugins: Aufbewahrungslimits/Rotation für Backups, Sandbox-/Run-Historie und große Option-Objekte.


## 2026-11-25 – DB-Notfall-Diagnoseplugin 1.0.0 erstellt
- Zweck: eine einzige read-only Grunddiagnose statt weiterer manueller SQL-Einzelschritte.
- Plugin: PFERDEATELIER_DB_NOTFALL_DIAGNOSE_1.0.0.zip
- SHA-256: 669e8a64e7d8d3ba19b1b943299d8ac6d936e7a2583543a0d95fec24f6184f5c
- PHP-Syntax geprüft: PASS.
- ZIP-Integrität geprüft: PASS.
- keinerlei DELETE/TRUNCATE/OPTIMIZE/ALTER/INSERT/UPDATE im Plugin.
- Diagnoseinhalt:
  - komplette Tabellenbelegung inkl. data_free,
  - grosse Options-Werte und Gruppen,
  - Workflow-Tabellenstatus/Zeitbereiche,
  - auffällige Backup-/Temp-/Alt-Tabellen,
  - aktive Plugin-/Theme-Codeprüfung auf Tabellenreferenzen,
  - Kandidatenliste nur zur manuellen Prüfung, keine automatische Löschfreigabe.
- im Büro gesichert unter PERFORMANCE_BUERO/DB_NOTFALL/.
- nächster Schritt: installieren -> Werkzeuge -> DB-Notfall -> Diagnose als JSON herunterladen -> auswerten -> genau einen gezielten Bereinigungsschritt freigeben.


## 2026-11-25 – Live/Test-Vergleich + PPAR-Schreibpfade
- Live DB-Notfall: 2033,28 MB reserviert, 1489,28 MB Inhalt, 544 MB intern frei.
- Test: 1484,14 MB reserviert, 1364,14 MB Inhalt, 120 MB intern frei.
- Live PPAR-Options: 103.925 Eintraege / 110,382 MB.
- Test PPAR-Options: 158 Eintraege / 3,687 MB.
- Live/Test-Abweichung PPAR: +103.767 Optionszeilen / ca. +106,7 MB.
- Quellcodepruefung der dynamischen PPAR-Options-Schluessel:
  - eBay-Audit: ppar_ebay_audit_r_<run-hash>_meta + _cN; pro Lauf eigener Namensraum.
  - Codekommentar und Exportlogik bestaetigen: historische Run-Audits werden nicht rotiert/geloescht.
  - weitere dynamische Schluessel sind begrenzt bzw. pro Konzept/Token und erklaeren 100k Eintraege nicht ohne DB-Nachweis.
- Ursache noch NICHT endgueltig behauptet. Naechster Beweis: Live-PPAR-Optionen nach Namensmuster zaehlen/summieren.


## 2026-11-25 12:31 – PPAR/eBay-Ursache weiter eingegrenzt
phpMyAdmin-Gruppenabfrage Live:
- EBAY_SONSTIGE: 103.567 Optionen / 84,76 MB
- EBAY_AUDIT: 200 Optionen / 22,09 MB
- PPAR_SONSTIGE: 88 Optionen / 3,52 MB
- ALTE_VERSIONEN: 37 Optionen / ~0 MB
- EBAY_BUSINESS_EXTRA: 25 Optionen / ~0 MB
- AUTOMATION: 5 Optionen / ~0 MB
Schluss:
- vorheriger Audit-Verdacht widerlegt: Audit ist nicht Hauptverursacher der 103k Optionen.
- Hauptblock liegt in sonstigen dynamischen ppar_ebay_* Optionsnamen.
- noch keine Löschfreigabe; nächster Beweis ist Namensmuster-Aufteilung innerhalb EBAY_SONSTIGE.
