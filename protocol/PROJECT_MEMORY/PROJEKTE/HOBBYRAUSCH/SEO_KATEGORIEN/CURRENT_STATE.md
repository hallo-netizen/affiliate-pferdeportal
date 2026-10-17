# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE-BASELINE UNVERÄNDERT / V3 2656-KNOTEN-AUDIT PASS / HD-001 1.14.9 VERWORFEN / 1.14.10 MANUAL-ONLY LOCAL PASS / ECHTER WORDPRESS-DRY-RUN OFFEN**

## Live-Baseline

Produktiv unverändert:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

- 2357 aktive physische Zielobjekte;
- 2357/2357 Readback;
- 8 Hauptwelten;
- 330/330 terminale CORE-Seiten;
- LIVE-PASS.

## Zentraler V3-Kandidat

Profil:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V3_20261016.json`

Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_FULL_STRUCTURE_AUDIT_V3_20261016.json`

Delta:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGETTREE_DELTA_V3_20261016.json`

Synthetic-Dry-Run:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_HD001_SYNTHETIC_DRYRUN_V3_20261016.json`

## Voll-Audit V3

- 8/8 Hauptwelten unverändert;
- 370 terminale Hobbyseiten;
- 2160 unterste Inhaltskategorien;
- je terminaler Hobbyseite 5–8 Inhaltskategorien;
- 2160/2160 Leafs grob mit mindestens 3–5 vertiefenden Beitragsthemen möglich;
- keine Kategorie unter einer untersten Kategorie;
- keine fehlenden Parents;
- keine doppelten Node-IDs/Slugs;
- HD-001 Validator: 0 Errors / 0 Warnings.

Fachlich korrigiert/ergänzt:
- Spotting & Verkehr;
- Citizen Science;
- Natur bestimmen;
- Plane Spotting aus Messen & Analysieren heraus;
- Suchen & Finden;
- Modellbau unter Fertigen;
- Miniaturen & Szenen ergänzt;
- Naturfunde ergänzt;
- Schneckenhaltung ergänzt;
- Quilten-Leaf zu `Quiltmuster & Stichführung` präzisiert.

Bewusste Watchlist ohne automatische Zusammenlegung:
- Asselhaltung / Isopoden-Zucht;
- Münzen / Numismatik;
- Teichwasser-Mikroskopie / Gewässermikroskopie.

## Synthetischer HD-001-Dry-Run

- CREATE 282;
- ADOPT 3;
- UPDATE 2357;
- ARCHIVE 0;
- Provider-/DataForSEO-Aufrufe 0;
- WordPress-Writes 0.

ADOPT statt Dublette:
Trainspotting, Modellraketen, Pflanzenbestimmung.

## Timeout-Korrektur

**HD-001 1.14.9 ist verworfen.**

Ursache:
automatischer Final-Target-Bootstrap auf WordPress-`init` nach Versionswechsel.

Sicherer Kandidat:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.10_MANUAL_ONLY_TIMEOUT_FIX_LOCALPASS.zip`

SHA-256:
`f9500d051249b239ca3215754eff54d37244fb80ef612ce54cfd5f722db7f243`

1.14.10:
- kein automatischer Runner-Bootstrap;
- Installation/Aktivierung startet keine Vollbaum-Verarbeitung;
- Dry-Run nur manuell;
- Sync getrennt und bestätigungspflichtig.

## Betriebsregel

DataForSEO = Evidence, nicht Strukturautorität.

Frontend/Design liest Struktur über HD-004; keine rohen WordPress-`get_pages()`-Kinder als Wahrheit.

## ERSTER OFFENER BLOCKER

**Der echte manuelle V3-Dry-Run gegen die aktuelle WordPress-Datenbank fehlt noch.**

## EXAKT EINE NEXT ACTION

**Für den V3-Dry-Run ausschließlich HD-001 1.14.10 einsetzen und nur den manuellen Finalen Delta-Dry-Run ausführen. Noch nicht synchronisieren.**
