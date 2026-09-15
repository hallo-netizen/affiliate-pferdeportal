# TESTREPORT – Pferde Atelier – Pferderassen Manager 0.2.7

STAND: 2026-09-15
STATUS: LOKAL HART PASS / WORDPRESS-LIVE OFFEN

## Prüfgegenstand

Plugin: `Pferde Atelier – Pferderassen Manager`
Plugin-Stamm: `pferde-rassen-manager/`
Version: `0.2.7`
Installer: `PFERDE_ATELIER_PFERDERASSEN_MANAGER_0.2.7_INSTALLIEREN.zip`
SHA-256: `5f72308cb922756cac8ffa2a01a27bfc7f1f1cfbabf6fbf5b4a33728fc8e58f1`

## Ursache der Nachbesserung

Die Abschlussprüfung gegen den rekonstruierten WordPress-Bestand ergab 196 veröffentlichte `pa_breed`-Posts, aber nur 194 eindeutige `_prm_source_id`-Werte. Doppelt vorhanden sind:
- `breed-pantaneiro`
- `breed-posavje-horse`

0.2.6 hielt den Snapshot nach `source_id` und ließ dadurch bei jeder doppelten WDB-ID einen realen Post aus dem Reparaturlauf verschwinden. Ein lokaler reproduzierender Test zeigte `ok=true`, obwohl bei einem Doppelpost eine alte Gleichgruppen-Relation stehen blieb.

## Fix 0.2.7

- Snapshot hält jeden veröffentlichten Post separat nach `post_id`.
- Kandidaten für Ähnlichkeitsrelationen bleiben separat als eindeutige WDB-Identitäten nach `source_id` gebunden.
- Doppelte WDB-IDs werden als Warnung ausgegeben, aber kein Post wird aus dem Backfill verschluckt.
- `Ähnliche Rassen` schließen weiterhin jede Rasse derselben `pa_breed_group` hart aus.
- Selbstreferenzen, unbekannte und unveröffentlichte Ziel-IDs bleiben gesperrt.
- Keine zufälligen Ersatzrassen bei Ähnlichkeitsscore 0.
- Relations-Neuaufbau bleibt ausschließlich explizite Backend-Aktion; weder Frontend-`init` noch Plugin-Aktivierung starten einen Backfill.
- Kein `get_post_metadata`-Filter.

## Harte lokale Positivprüfung – exakt gegen fertige ZIP

Testbasis rekonstruiert aus:
- WordPress-Export 2026-09-15: 109 veröffentlichte `pa_breed`;
- veröffentlichter 25er-Batch 08;
- veröffentlichter 25er-Batch 09;
- veröffentlichter 24er-Batch 10;
- letzter 13er-Batch.

Rekonstruktion:
- veröffentlichte Posts: **196**;
- eindeutige `_prm_source_id`: **194**;
- Doppel-IDs: **2** (`breed-pantaneiro`, `breed-posavje-horse`).

Vor dem Test wurden bei allen 196 Posts absichtlich falsche Relationseinträge aus der jeweils eigenen Rassengruppe gesetzt.

Ergebnis mit dem realen 0.2.7-Code aus der fertigen ZIP:
- Backfill `ok=true`: PASS;
- `updated=196`: PASS;
- `get_posts()` für den vollständigen Backfill: 1: PASS;
- beide Doppel-IDs erkannt und mit konkreten Post-IDs gewarnt: PASS;
- beide Posts jeder Doppel-ID tatsächlich repariert: PASS;
- maximal 3 Relations-IDs: PASS;
- keine doppelte Relations-ID: PASS;
- keine Selbstreferenz: PASS;
- keine unbekannte Relations-ID: PASS;
- 0 Überschneidungen mit derselben Rassengruppe: PASS;
- normale `boot()`-Strecke löst 0 Relationsqueries aus: PASS;
- `activate()` löst 0 Relationsqueries aus: PASS;
- kein Frontend-Backfill-/Upgrade-Hook: PASS;
- kein `get_post_metadata`-Filter: PASS.

Direkte Grenzprüfung Aegidienberger:
- Selbstreferenz → BLOCK: PASS;
- Campolina (gleiche Gruppe) → BLOCK: PASS;
- Islandpferd (gleiche Gruppe) → BLOCK: PASS;
- Mangalarga Marchador (gleiche Gruppe) → BLOCK: PASS;
- Dales Pony (andere Gruppe, veröffentlicht) → akzeptiert: PASS;
- unbekannte WDB-ID → BLOCK: PASS.

## Negativ-/Mutationstests

Vier absichtliche Fehler wurden in Kopien des 0.2.7-Codes eingebaut. Jeder Mutant wurde erkannt:
1. Doppelposts wieder aus dem Snapshot herauskollabieren → ROT; nur 194/196 aktualisiert, stale Relations erkannt.
2. beide Same-Group-Sperren entfernen → ROT; Gruppenüberschneidungen erkannt.
3. Backfill wieder an Frontend-`init` hängen → ROT.
4. `get_post_metadata`-Filter wieder einbauen → ROT.

Ergebnis: **4/4 ROT**.

## Paket-/Versionsprüfung

- PHP-Lint Hauptdatei: PASS.
- PHP-Lint Managerklasse: PASS.
- ZIP-Lesetest `unzip -t`: PASS.
- Plugin-Version Hauptdatei: `0.2.7`: PASS.
- `PRM_VERSION`: `0.2.7`: PASS.
- Builddateien ↔ erneut entpackte ZIP-Dateien bytegleich: PASS.
- kompletter Plugin-Stamm vorhanden: PASS.

## Offene Pflichtprüfung

**WORDPRESS-LIVE OFFEN.**

Wegen der real aufgetretenen Frontend-Endlosschleifen in 0.2.4/0.2.5 wird 0.2.7 ausdrücklich nicht als LIVE-PASS bezeichnet. Vor Freigabe sind mindestens erforderlich:
1. Plugin in WordPress installieren;
2. normale Pferderassen-Einzelseite laden – kein Endlosladen;
3. Backend-Relations-Neuaufbau genau einmal manuell starten;
4. Aegidienberger erneut laden;
5. `Zur gleichen Rassengruppe` und `Ähnliche Rassen` dürfen keine gemeinsame Rasse enthalten;
6. weitere Einzelrasse als Gegenprobe;
7. erst dann LIVE-PASS und Artefakt-Sync.
