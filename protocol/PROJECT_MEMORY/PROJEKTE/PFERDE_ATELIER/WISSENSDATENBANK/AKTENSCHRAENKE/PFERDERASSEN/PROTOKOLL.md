# PFERDERASSEN – PROTOKOLL

## 2026-09-12 – ursprüngliche Rassenbasis angelegt

AUSLÖSER:
Pferde- und Ponyrassen sollen vollständig, strukturiert, flexibel und quellengebunden als Recherchegrundlage aufgebaut werden.

ENTSCHEIDUNG:
- keine getrennte Pony-Datenbank;
- keine WordPress-Live-Datenbank;
- ein Datensatz pro Rasse;
- flexible Schemaerweiterung;
- keine automatische Artikelproduktion.

## 2026-09-12 – in WISSENSDATENBANK integriert

WAS:
Die zuvor als eigenes Büro angelegte Rassenbasis wird zum ersten Aktenschrank des zentralen Büros `WISSENSDATENBANK`.

WARUM:
Mehrere künftige Forschungsgebiete benötigen eine gemeinsame Themen-, Status- und Trust-Steuerung. Ein eigenes Büro pro Recherchethema würde die Campusstruktur unnötig aufblasen.

EINE WAHRHEIT:
- Arbeitsstatus/NEXT ACTION nur in `../../HOBBYRAUM.md`;
- Gesamtstatus nur in `../../CURRENT_STATE.md`;
- Rassenfakten nur in diesem Aktenschrank;
- alte Adresse `PFERDERASSEN/START_HERE.md` bleibt lediglich als Weiterweiser.

## 2026-09-15 – Artikelserie und WordPress-Manager nachgeprüft

AUSGEFÜHRT:
- WordPress-Export mit 109 veröffentlichten `pa_breed` gegen die danach veröffentlichten 25er-, 25er-, 24er- und 13er-Batches rekonstruiert;
- Ergebnis: 196 veröffentlichte Posts / 194 eindeutige `_prm_source_id`;
- doppelte IDs entdeckt: `breed-pantaneiro`, `breed-posavje-horse`;
- den letzten 13er-Batch erneut gegen den verbindlichen Schreibvertrag und die aktuellen WDB-Datensätze geprüft;
- Ergebnis: alle 13 `rassengruppe_slug`-Zuordnungen sind durch `typ`/`rassegruppen` nicht eindeutig als eine der sechs Managergruppen getragen; daher kein Schreibvertrags-PASS;
- Relationsschnittstelle des Designs bestätigt: `_prm_related_source_ids` wird gegen `_prm_source_id` aufgelöst;
- Manager-Versionen 0.2.2 bis 0.2.6 gebaut/repariert; reale Fehler 0.2.4/0.2.5 wurden durch Nutzer-Livebefund sichtbar;
- Abschlussprüfung entdeckte zusätzlich den Duplicate-Collapse-Fehler in 0.2.6;
- Manager 0.2.7 als neuer lokaler Kandidat gebaut und exakt gegen die fertige ZIP geprüft.

WICHTIGE FEHLERKETTE:
- 0.2.2: ähnliche Rassen = gleiche Gruppe; fachlich falsch;
- 0.2.3: vorhandene alte Relationen nicht zuverlässig ersetzt;
- 0.2.4: rekursiver `get_post_metadata`-Pfad → Frontend-Endlosladen;
- 0.2.5: Vollbackfill auf `init`/Aktivierung → Frontend-Endlosladen;
- 0.2.6: Frontendlast entfernt, aber doppelte `_prm_source_id` wurden im Snapshot kollabiert;
- 0.2.7: jeder reale Post bleibt separat; Doppel-IDs werden gewarnt; Backfill nur Backend; Same-Group/Self-Hardlock aktiv.

HARTE LOKALE PRÜFUNG 0.2.7:
- reale 196-Post-Rekonstruktion;
- bei allen 196 absichtlich falsche Same-Group-Relation vorab gesetzt;
- 196/196 repariert;
- 2 Doppel-IDs erkannt;
- 1 `get_posts()`-Snapshot für Gesamtbackfill;
- 0 Same-Group-Überschneidungen nach Backfill;
- Aegidienberger-Grenztest: Self/Campolina/Islandpferd/Mangalarga BLOCK, Dales Pony andere Gruppe akzeptiert, unbekannte ID BLOCK;
- Frontend-Boot und Aktivierung: 0 Relationsqueries;
- vier Negativ-/Mutationstests: 4/4 ROT;
- PHP-Lint, ZIP-Lesetest, Version, kompletter Pluginbaum, Source↔ZIP-Bytes: PASS.

BELEGE:
- `FEHLERQUELLEN.md`
- `ZIELVERTRAG_RELATIONEN.md`
- `TECHNIK_PFERDERASSEN_MANAGER_CURRENT.md`
- `TESTREPORT_PFERDERASSEN_MANAGER_0.2.7.md`

OFFEN:
- direkter WordPress-Readback und Bereinigung der zwei Doppel-IDs;
- autoritative Sechs-Gruppen-Zuordnung der 13 letzten Identitäten;
- WordPress-LIVE-Test des Manager 0.2.7. Kein LIVE-PASS vor diesem Test.

## 2026-09-15 – Plugin-Kandidat dauerhaft im Plugin-Schrank abgelegt

AUSGEFÜHRT:
- `/Campus-Plugins/PFERDE_ATELIER/PPA-011/` angelegt;
- geprüfte ZIP als `CANDIDATE_0.2.7.zip` abgelegt;
- `CANDIDATE_MANIFEST.md` mit Version, SHA-256, technischer Hauptquelle und Prüfgrenze abgelegt;
- Library-Readback bestätigt beide Dateien am Zielpfad.

WICHTIG:
- bewusst **keine** `CURRENT.zip` und kein finales `MANIFEST.md` erzeugt;
- Grund: WordPress-LIVE-Test bleibt offen;
- Fach-/Technikwahrheit bleibt `TECHNIK_PFERDERASSEN_MANAGER_CURRENT.md`, nicht der Plugin-Schrank.
