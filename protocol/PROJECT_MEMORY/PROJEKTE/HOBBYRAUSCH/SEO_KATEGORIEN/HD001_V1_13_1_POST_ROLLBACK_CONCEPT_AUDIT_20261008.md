# HD-001 V1.13.1 – POST-ROLLBACK-KONZEPTAUDIT

STAND: 2026-10-08
STATUS: BLOCKED_BEFORE_FINAL_SYNC
SCOPE: HOBBYRAUSCH / SEO_KATEGORIEN / HD-001
REGELBASIS:
- `ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md` Fassung 2.5
- `HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json` Version 1.5

## Geprüfte Live-Evidence

Frischer Export:
`hobby-depot-final-target-readback-20261008-083850-utc.json`

Live-Dry-Run:
- Plugin 1.13.1;
- PASS / valid=true;
- Revision `HD-TARGET-3P-V1.13.1-PRACTICAL-20261008+da240c90a8725c4a`;
- 841 kanonische Identitäten;
- 340 CORE;
- 501 Editorial/Finder;
- 440 logische Knoten;
- 431 physische Zielobjekte;
- 356 CREATE;
- 75 ADOPT;
- 0 UPDATE;
- 0 UNCHANGED;
- 0 ARCHIVE;
- 0 Provider-Aufrufe;
- 0 Kosten;
- 0 WordPress-Strukturwrites.

Alter V1.12-Lauf:
- terminal `ROLLED_BACK`;
- Runner `BLOCKED / TARGET_TREE_ROLLBACK_END`;
- alter Fehler `directory:events-reisen [name]` gehört zum abgeschlossenen alten Lauf;
- kein aktiver finaler Snapshot.

## Vollständiger Strukturabgleich gegen das Kategoriekonzept

PASS:
- genau 8 Hauptwelten;
- alle 8 Hauptwelten physische CORE-Roots;
- `Hobbywelten` ist Root/View und kein Parent der 8 Welten;
- keine fehlenden Parent-Knoten;
- keine Parent-Zyklen;
- keine Cross-Pillar-Parent-Beziehungen;
- keine doppelten Node-IDs;
- keine doppelten Slugs innerhalb der jeweiligen Objekttypen;
- 404 Pages;
- 4 WordPress-`category`;
- 15 `journal_cat`;
- 8 `hp_listing_category`;
- maximale physische Tiefe: Welt → Zwischenbereich → Hobby → Kategorie;
- die einzigen vier normalen WordPress-Kategorien liegen unter `Buchbinden`:
  - Einstieg;
  - Ausrüstung;
  - Material;
  - Techniken & Praxis;
- keine Kategorie unter Kategorie;
- CORE-Hobbys benötigen keine künstlichen Leaf-Kategorien zum Start;
- 329 Baseline-CORE + 12 Promotionen - 1 Demotion = 340 CORE;
- Demotion `alte Brettspiele` ist im finalen CORE nicht mehr enthalten;
- die 12 kalibrierten Promotionen sind im finalen CORE enthalten.

## EINZIGER GEFUNDENER STRUKTURBLOCKER

Knoten:
`core:gestalten:materialkunst`

Live-Zielplan:
- action = `CREATE`;
- object_type = `page`;
- display name = `Materialkunst`;
- parent = `core:world:gestalten`;
- bestehende object_id = 0.

Maschineller Vollabgleich des finalen physischen Zielbaums:
- 0 Kindknoten mit `parent_id = core:gestalten:materialkunst`;
- `Materialkunst` ist keine der 841 kanonischen Hobby-Identitäten;
- im gebundenen Inventar existiert 0 Entity-Placement auf `core:gestalten:materialkunst`;
- die neun finalen Relations bestehen aus der bestehenden Magazin→Hobbywelten-Relation plus acht Hobbywelten→Welten-View-Relations; kein belegter Materialkunst-Relationsträger.

Damit ist `Materialkunst` im finalen Zielbaum ein neu anzulegender, strukturell leerer Zwischenknoten.

Das verletzt die weiterhin aktive Zielvertragsregel:
**Keine inhaltsleeren Ebenen.**

Es gibt keine belegte fachliche Grundlage, stattdessen Inhalte oder Hobbys künstlich nach `Materialkunst` umzuhängen.

## ENTSCHEIDUNG

Finalen Sync NICHT starten.

KISS-Korrektur:
`core:gestalten:materialkunst` aus dem finalen V1.13.1-Zielprofil entfernen.

Keine Ersatzkategorie erfinden.
Keine Hobby-Identität umhängen.
Keine DataForSEO-Recherche starten.
Keine andere Struktur ändern.

Danach:
1. Zielprofil erneut lokal hart prüfen;
2. frischen finalen Live-Dry-Run ausführen;
3. neuer JSON-Readback;
4. nur bei PASS genau einen finalen Sync;
5. Struktur-/Frontend-Readback;
6. Backup;
7. HD-001 deaktivieren/deinstallieren.

## Historische Batch-Dateien

Die alte Datei
`HOBBY_MASTER_V2_BATCH_003_FINAL_ASSESSMENT_20261007.json`
ist keine Current-Autorität für die praktische Finalisierung.

Regeln 1.5, Zielvertrag 2.5, Current-Autorität und
`HOBBY_MASTER_V2_PRACTICAL_FINAL_TARGET_AUDIT_20261008.json`
bestimmen den aktuellen Finalisierungsweg.

Historische Batchdaten dürfen den aktuellen Zielbaum nicht rückwirkend überschreiben.
