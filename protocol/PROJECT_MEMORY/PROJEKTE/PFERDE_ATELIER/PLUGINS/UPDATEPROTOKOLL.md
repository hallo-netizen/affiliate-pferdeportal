# PFERDE-ATELIER – PLUGINS – UPDATEPROTOKOLL

STAND: 2026-09-15
ROLLE: ZENTRALES PLUGIN-ÄNDERUNGS-/SYNC-PROTOKOLL

## Regel

Für jede tatsächliche Pluginentwicklung oder jedes tatsächliche Pluginupdate genau ein Vorgang:
`PU-YYYYMMDD-NNN`.

Pflichtfelder:
- Plugin-ID / Name
- ART: ENTWICKLUNG / UPDATE
- Herkunft: EIGENENTWICKLUNG / DRITTANBIETER
- zuständiges Fachbüro
- VON_VERSION / AUF_VERSION
- autoritative Quelle / Branch / Release
- WARUM
- Abhängigkeiten / Schnittstellen
- relevante Fehler-/Rollbackbelege
- tatsächlich ausgeführte Positivprüfung
- tatsächlich ausgeführte Negativprüfung, soweit erforderlich
- Fach-/Regressionstest
- Artefakt-Sync nach `SYNC_VERTRAG.md`
- Ergebnis: PASS / FAIL / ROLLBACK / BLOCKED

## Initialisierung 2026-09-13

Dieser Büroaufbau ist **keine Pluginentwicklung und kein Pluginupdate**. Deshalb wurde dafür bewusst keine `PU-*`-ID erfunden.

Erstbestand inventarisiert und physischer Plugin-Schrank angelegt.

Real synchronisiert/readback-geprüft:
- PPA-001 Affiliate-Zentrale 6.72.19
- PPA-003 Bildzentrale 2.6.9
- PPA-004 Universal Research & Fill 1.9.9
- PPA-005 Portal SEO Topic Engine 0.56.25
- PPA-007 Pferde Atelier HivePress Anzeigensuche 2.1.5

Noch BLOCKED:
PPA-002 / PPA-006 / PPA-008 / PPA-009.

Keine Fach-/LIVE-Wahrheit wurde durch die Initialisierung verändert.

## PU-20260915-001 – Pferde Atelier – Pferderassen Manager

- PLUGIN-ID: `PPA-011`
- NAME: `Pferde Atelier – Pferderassen Manager`
- ART: UPDATE
- HERKUNFT: EIGENENTWICKLUNG
- FACHBÜRO: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`
- VON_VERSION: `0.2.1`
- AUF_VERSION: `0.2.7`
- AUTORITATIVE TECHNISCHE QUELLE: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/TECHNIK_PFERDERASSEN_MANAGER_CURRENT.md`
- CAMPUS-BRANCH: `hobbyroom/project-memory-campus-v1-20260905`
- RELEASEARTEFAKT: `PFERDE_ATELIER_PFERDERASSEN_MANAGER_0.2.7_INSTALLIEREN.zip`
- SHA-256: `5f72308cb922756cac8ffa2a01a27bfc7f1f1cfbabf6fbf5b4a33728fc8e58f1`

WARUM:
Die Pferderassen-Einzelseite besitzt getrennte Module `Zur gleichen Rassengruppe` und `Ähnliche Rassen`. Der Manager musste deshalb strukturierte `_prm_related_source_ids` liefern, ohne dieselbe Rassengruppe erneut als „ähnlich“ auszugeben. Die Zwischenversionen 0.2.2–0.2.6 öffneten nacheinander reale Fehlerklassen; Details bleiben ausschließlich in der Fachfehlerquelle.

ABHÄNGIGKEITEN / SCHNITTSTELLEN:
- WordPress CPT `pa_breed`;
- Taxonomie `pa_breed_group`;
- stabile WDB-ID `_prm_source_id`;
- Relationsfeld `_prm_related_source_ids`;
- Design-Einzelseite löst Relations-IDs gegen `_prm_source_id` auf;
- Relations-Neuaufbau ausschließlich als explizite Backend-Aktion; kein Frontend-`init`, keine Aktivierungsreparatur, kein `get_post_metadata`-Filter.

RELEVANTE FEHLERQUELLE:
`../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/FEHLERQUELLEN.md` → `PR-PLUGIN-001`, inzwischen CLOSED / LIVE PASS.

ROLLBACK-/SICHERHEITSREFERENZ:
Letzter vor dem Relationsumbau belegter Grundstand: 0.2.1. Keine automatische Datenlöschung.

TATSÄCHLICH AUSGEFÜHRTE POSITIVPRÜFUNG 0.2.7:
- exakte fertige ZIP erneut entpackt;
- PHP-Lint Hauptdatei + Managerklasse PASS;
- ZIP-Lesetest PASS;
- Versionsbindung `0.2.7` PASS;
- Source↔ZIP bytegleich PASS;
- realer rekonstruierter 196-Post-Bestand: 196/196 Relationsreparatur;
- zwei doppelte `_prm_source_id` erkannt, beide realen Posts je ID repariert;
- maximal drei eindeutige Relations-IDs, keine Selbstreferenz, keine unbekannte Ziel-ID;
- 0 Überschneidungen mit derselben `pa_breed_group`;
- normaler Boot + Aktivierung: 0 Relationsqueries;
- Aegidienberger-Grenzprüfung: andere veröffentlichte Gruppe akzeptiert.

TATSÄCHLICH AUSGEFÜHRTE NEGATIVPRÜFUNG:
- Aegidienberger Self / Campolina / Islandpferd / Mangalarga Marchador → BLOCK;
- unbekannte WDB-ID → BLOCK;
- Mutation Duplicate-Collapse → ROT;
- Mutation Same-Group-Sperre entfernt → ROT;
- Mutation Frontend-`init`-Backfill → ROT;
- Mutation `get_post_metadata`-Filter → ROT;
- 4/4 Mutationen erkannt.

FACH-/REGRESSIONSTEST:
`../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/TESTREPORT_PFERDERASSEN_MANAGER_0.2.7.md` → lokal hart PASS; WordPress-LIVE am 2026-09-15 durch Nutzer ausdrücklich PASS bestätigt.

ARTEFAKT-SYNC:
- `/Campus-Plugins/PFERDE_ATELIER/PPA-011/CURRENT.zip` vorhanden;
- `/Campus-Plugins/PFERDE_ATELIER/PPA-011/MANIFEST.md` vorhanden;
- persistente `CURRENT.zip` erneut materialisiert;
- SHA-256 `5f72308cb922756cac8ffa2a01a27bfc7f1f1cfbabf6fbf5b4a33728fc8e58f1`: PASS;
- ZIP-Lesetest: PASS;
- Plugin-Version aus persistentem ZIP: `0.2.7`: PASS.

ERGEBNIS: **PASS**
