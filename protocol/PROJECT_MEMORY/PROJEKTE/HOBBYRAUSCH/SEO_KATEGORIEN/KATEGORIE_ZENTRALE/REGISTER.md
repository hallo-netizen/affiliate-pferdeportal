# HOBBY DEPOT – ZENTRALES KATEGORIE-REGISTER

STAND: 2026-10-16
ROLLE: Datenbindung / KEINE zweite Current-Wahrheit.

## Aktive Live-Baseline – unverändert

Revision:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

Finaler Live-Readback:
`/hobby rausch/KATEGORIE_ZENTRALE/hobby-depot-final-target-readback-20261009-170623-utc.json`

Finaler Zielprofil-Export:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_RULE27_20261009.json`

Zielprofil SHA-256:
`28647e48efc1bb22c4e9d8cc4c0be204cd2a30c24681c2257afad67d11f6226e`

Wiederherstellbares HD-001-Live-Release:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

SHA-256:
`709134631895a901bcb4fc5f5d71889d317954d9928c0ed20700883990a5a52c`

## V3-Strukturkandidat – zentral / NOCH NICHT LIVE

Zielprofil:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V3_20261016.json`

SHA-256:
`6d73e5d4d32e91acf6a5c8dd19dc9e23af4a661dc053fa7a752a4ea4668826e7`

Voll-Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_FULL_STRUCTURE_AUDIT_V3_20261016.json`

Strukturdelta:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGETTREE_DELTA_V3_20261016.json`

Echter HD-001-Synthetic-Dry-Run:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_HD001_SYNTHETIC_DRYRUN_V3_20261016.json`

HD-001-Updatekandidat:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.9_HOBBY_DEPOT_V3_STRUCTURE_DRYRUN_LOCALPASS.zip`

HD-001 1.14.9 ZIP SHA-256:
`a498c84e2f98ce386acbfb04eb1fee0b77c90d33b51cc1b557f477812bd165a3`

## V3-Audit-Ergebnis

- 8/8 Hauptwelten unverändert;
- 2656 logische Knoten im Rohprofil;
- 370 terminale Hobbyseiten;
- 2160 unterste CORE-Inhaltskategorien;
- jede terminale Hobbyseite hat 5–8 Inhaltskategorien;
- keine unterste Inhaltskategorie hat weitere Kategorie-Kinder;
- 2160/2160 unterste Inhaltskategorien grob auf mindestens 3–5 vertiefende Beitragsthemen geprüft: PASS;
- 0 doppelte Node-IDs;
- 0 doppelte Slugs;
- 0 fehlende Parents;
- 0 sibling-name-Dubletten;
- HD-001-TargetTree-Validator: PASS, 0 Errors, 0 Warnings.

Wichtige Änderungen:
- Forschen → Spotting & Verkehr;
- Forschen → Citizen Science;
- Forschen → Natur bestimmen;
- Plane Spotting aus Messen & Analysieren nach Spotting & Verkehr;
- Sammeln → Suchen & Finden;
- Sammeln → Naturfunde erweitert;
- Fertigen → Modellbau;
- Gestalten → Miniaturen & Szenen erweitert;
- Tiere → Wirbellose um Schneckenhaltung erweitert;
- Quilten-Leaf präzisiert zu Quiltmuster & Stichführung.

## HD-001-Delta / Synthetic-Dry-Run

Strukturell gegen Baseline:
- ADD 285 = 45 Seiten + 240 Kategorien;
- UPDATE 2 fachliche Strukturänderungen;
- REMOVE 0.

Mit echter HD-001-Dry-Run-Logik gegen synthetische vollständige Baseline:
- PASS;
- CREATE 282;
- ADOPT 3;
- UPDATE 2357;
- ARCHIVE 0;
- DEMOTE_EDITORIAL 0;
- Provider/DataForSEO Calls 0;
- WordPress-Strukturwrites 0.

ADOPT-Nachweis:
- Trainspotting;
- Modellraketen;
- Pflanzenbestimmung.

Neue deterministische Zielrevision nach Inventory-Auflösung:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+16d1bd25b2adfc26`

## Zentrale Runtime-Wahrheit

WordPress-Optionen:
- `apkw_target_tree_active_revision_v1`
- `apkw_target_tree_active_snapshot_v1`

Andere Plugins lesen diese Wahrheit ausschließlich über HD-004:
`HOBBY_DEPOT_CATEGORY_REGISTRY_RUNTIME_V1`

Keine zweite Strukturwahrheit, keine Design-Sonderlisten, DataForSEO keine Strukturautorität.

## Harte Grenze

**Die Live-Baseline bleibt aktiv, bis HD-001 1.14.9 auf WordPress einen echten Live-Dry-Run PASS liefert. Erst danach darf exakt dieser Plan einmal synchronisiert und anschließend 100 % gelesen werden.**
