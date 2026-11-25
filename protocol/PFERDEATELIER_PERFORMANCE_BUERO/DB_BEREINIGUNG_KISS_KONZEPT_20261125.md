# Pferdeatelier – KISS-Datenbankbereinigung

Stand: 25.11.2026

## Ziel
Datenbank unter die IONOS-Grenze bringen, ohne fachliche Funktionen, Produktläufe, K0, Relevanssi oder bestehende Affiliate-Ergebnisse zurückzubauen.

## Bewiesene Ausgangslage
- Live reserviert: 2033,28 MB.
- Echter Inhalt: 1489,28 MB.
- Interner Leerraum: 544 MB.
- Test reserviert: 1484,14 MB; interner Leerraum nur 120 MB.
- Hauptunterschied ist damit physische Fragmentierung, nicht grundsätzlich zu viel echter Inhalt.
- Größte Live-Leerräume:
  - slfo_pste_runs: 221 MB
  - slfo_pste_candidates: 115 MB
  - slfo_options: 100 MB
  - slfo_ppar_creative_library: 23 MB
  - zusammen: 459 MB
- Ein OPTIMIZE/Tabellen-Rebuild ist aktuell wegen der IONOS-Sperre blockiert.
- DELETE innerhalb derselben Tabelle vergrößert nur DATA_FREE und senkt die physisch reservierte Größe nicht zuverlässig; deshalb kein weiteres zeilenweises Notfall-Löschen als Hauptweg.

## KISS-Plan

### Phase 1 – einmalig Schreibsperre lösen
Bevor fachliche Daten gelöscht werden: IONOS temporär mindestens ca. 100 MB zusätzlichen DB-Spielraum geben lassen / Datenbank kurzzeitig entsperren. Keine WordPress-Funktion ändern.

Fallback, falls IONOS das nicht ermöglicht: nur nach ausdrücklicher Freigabe einen nachweislich wiederaufbaubaren Index als temporären Türöffner verwenden. Kein automatischer Fallback.

### Phase 2 – physisch komprimieren, ohne Daten zu löschen
Einzeln, nicht parallel:
1. OPTIMIZE TABLE slfo_pste_runs;       Erwarteter Rückgewinn ca. 221 MB.
2. OPTIMIZE TABLE slfo_pste_candidates; Erwarteter Rückgewinn ca. 115 MB.
3. OPTIMIZE TABLE slfo_options;          Erwarteter Rückgewinn ca. 100 MB.
4. OPTIMIZE TABLE slfo_ppar_creative_library; Erwarteter Rückgewinn ca. 23 MB.

Nach Schritt 1 steht bereits >200 MB Headroom zur Verfügung. Danach sollten die weiteren Rebuilds ohne Notfallmodus möglich sein.
Theoretischer Rückgang aus den vier Tabellen: ca. 459 MB, also von 2033 MB Richtung ca. 1574 MB reserviert, ohne fachliche Zeilen zu löschen.

### Phase 3 – echte Altlasten erst danach löschen
Nur mit Nutzungsbeweis:
- alte Backups/Migrationen,
- Transients,
- abgeschlossene Logs/temporäre Diagnosedaten,
- nachweislich verwaiste Options,
- historische Workflow-Daten nur wenn aktive Läufe/Referenzen ausgeschlossen sind.
Nach größeren Löschungen jeweilige betroffene Tabelle erneut optimieren.

Nicht pauschal löschen:
- eBay-Inbox, solange echte Löschanforderungen nicht sicher klassifiziert sind,
- Relevanssi,
- K0/PPM/PSTE/PSERC aktive Bestände,
- Produkt-/Creative-/Output-Bestände.

### Phase 4 – Regrowth verhindern
- WP-Cron bleibt nicht pauschal an/aus verändert.
- Test: cron_disabled=false, 0 overdue.
- Live: cron_disabled=true, 30 overdue.
- Alle nötigen Hintergrundjobs werden einzeln auf vorhandene externe Zeitgeber abgebildet; keine Wiedervermischung paralleler Produktläufe.
- Account-Deletion bekommt einen eigenen unabhängigen Weg, nicht den Produkt-Heartbeat.
- monatliche DB-Grenzen: Warnung ab 1700 MB reserviert oder >15 % DATA_FREE; Wartung vor 1900 MB.

## Weitere Live/Test-Schlüsse
1. options ist nicht grundsätzlich das Problem: Test hat 584,53 MB Inhalt, Live 509,36 MB. Live ist vor allem stärker fragmentiert.
2. pste_runs: Live 139,05 MB Inhalt bei 229 Zeilen; Test 57,55 MB bei deutlich kompakterem Speicher. Nach physischer Kompaktierung separat Payload/Retention prüfen.
3. pste_candidates: Live 303,56 MB bei 6572 Zeilen; Test 141,61 MB bei 8512 Zeilen. Live hat trotz weniger Zeilen deutlich größere Nutzlast pro Zeile; nach Notfall gezielt Spalten/Payload prüfen.
4. ppar_ebay_items: Live 167,36 MB / 8114 Zeilen, Test 85,05 MB / ca. 6077. Danach Duplikate/alte Snapshots prüfen, aber nicht im Notfall löschen.
5. Relevanssi ist mit 35,67 MB kein Haupthebel und bleibt unangetastet.

## Entscheidungsregel
Erst physisch vorhandenen Leerraum zurückholen, dann echte Altlasten löschen. Keine neuen Plugins für die Notfallbereinigung. Keine zeilenweisen Langläufer.
