# HOBBY DEPOT – ZENTRALES KATEGORIE-REGISTER

STAND: 2026-10-16  
ROLLE: Datenbindung / KEINE zweite Current-Wahrheit.

## Aktive Live-Baseline

Revision:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

Finaler Live-Readback:
`/hobby rausch/KATEGORIE_ZENTRALE/hobby-depot-final-target-readback-20261009-170623-utc.json`

Finaler Zielprofil-Export:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_RULE27_20261009.json`

Zielprofil SHA-256:
`28647e48efc1bb22c4e9d8cc4c0be204cd2a30c24681c2257afad67d11f6226e`

Wiederherstellbares HD-001-Release:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

HD-001 SHA-256:
`709134631895a901bcb4fc5f5d71889d317954d9928c0ed20700883990a5a52c`

## Aktiver WIP-Audit-Kandidat – NOCH NICHT LIVE

Zentral abgelegt:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V3_20261016.json`

SHA-256:
`6d73e5d4d32e91acf6a5c8dd19dc9e23af4a661dc053fa7a752a4ea4668826e7`

Voll-Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_FULL_STRUCTURE_AUDIT_V3_20261016.json`

Status:
- Live-Baseline bleibt unverändert;
- 8 Hauptwelten unverändert;
- 370 terminale Hobbyseiten im Kandidaten;
- 2160 unterste CORE-Inhaltskategorien;
- jede terminale Hobbyseite hat 5–8 Inhaltskategorien;
- keine unterste Inhaltskategorie hat weitere Kategorie-Kinder;
- grobe 3–5+-Beitragspotenzialprüfung: 2160/2160 PASS;
- 0 doppelte Node-IDs;
- 0 doppelte Slugs;
- 0 fehlende Parents;
- HD-001-TargetTree-Validator: PASS, 0 Errors, 0 Warnings.

Wichtige Strukturkorrekturen/Erweiterungen:
- Forschen → Spotting & Verkehr;
- Forschen → Citizen Science;
- Forschen → Natur bestimmen;
- Plane Spotting aus Messen & Analysieren nach Spotting & Verkehr verschoben;
- Sammeln → Suchen & Finden;
- Sammeln → Naturfunde sinnvoll erweitert;
- Fertigen → Modellbau;
- Gestalten → Miniaturen & Szenen sinnvoll erweitert;
- Tiere → Wirbellose um Schneckenhaltung erweitert;
- unterste Kategorie `Quilten` unter Hobby `Quilten` zu `Quiltmuster & Stichführung` präzisiert.

Harte Grenze:
**Dieser WIP-Kandidat ist kein Live-PASS und darf die aktive Baseline erst nach HD-001 Delta/Dry-Run/Regression/Readback ersetzen.**

## Zielbaum – aktive Live-Baseline

Profil:
- 2371 Nodes gesamt;
- 2366 aktive Nodes;
- 2357 aktive physische Zielobjekte;
- 9 aktive Relations.

Aktive physische Typen:
- 416 `page`;
- 1920 `category`;
- 13 `journal_cat`;
- 8 `hp_listing_category`.

Live-Readback:
- 2357/2357 geprüft;
- Runner COMPLETE;
- Fehler leer;
- Frontend valid=true;
- 8 Welten;
- 330/330 terminale CORE-Seiten im Kategorie-Gate.

## Zentrale Runtime-Wahrheit in WordPress

Der produktive HD-001-Abschluss hat den kompletten aktiven Zielstand bereits in WordPress gespeichert:

- Revision:
  `apkw_target_tree_active_revision_v1`
- Snapshot:
  `apkw_target_tree_active_snapshot_v1`

Der Snapshot enthält:
- Nodes mit stabiler `node_id`;
- Pillar;
- `object_type` / Taxonomie;
- Name/Slug;
- Parent-Zuordnung;
- aktiven Status;
- WordPress-Mapping `node_id → object_id/object_type/taxonomy`.

**Diese beiden Optionen bleiben auch bei Deaktivierung des schweren HD-001-Plugins bestehen.**

Andere Plugins greifen NICHT direkt auf APKW-Klassen zu, sondern über den neutralen HD-004-Kategorie-Kern.

## Taxonomie-Ownership

- `category` → WordPress Core
- `journal_cat` → HD-004 Kategorie-Kern im Normalbetrieb
- `hp_listing_category` → HivePress

HD-001 bleibt Bearbeitungs-/Synchronisationswerkzeug, nicht notwendiger Dauer-Frontenddienst.
