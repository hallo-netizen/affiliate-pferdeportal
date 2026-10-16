# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-16
STATUS: **LIVE-BASELINE UNVERÄNDERT / V3 2656-KNOTEN-AUDIT PASS / HD-001 1.14.9 LOCAL DRY-RUN PASS / ECHTER WORDPRESS-DRY-RUN OFFEN**

## Live-Baseline

Weiterhin produktiv:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

- 2357 aktive physische Zielobjekte;
- 2357/2357 Readback;
- 8 Hauptwelten;
- 330/330 terminale CORE-Seiten;
- LIVE-PASS.

## Zentraler V3-Kandidat

Profil:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V3_20261016.json`

SHA-256:
`6d73e5d4d32e91acf6a5c8dd19dc9e23af4a661dc053fa7a752a4ea4668826e7`

Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_FULL_STRUCTURE_AUDIT_V3_20261016.json`

Delta:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGETTREE_DELTA_V3_20261016.json`

HD-001 Synthetic-Dry-Run:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_HD001_SYNTHETIC_DRYRUN_V3_20261016.json`

HD-001-Kandidat:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.9_HOBBY_DEPOT_V3_STRUCTURE_DRYRUN_LOCALPASS.zip`

ZIP SHA-256:
`a498c84e2f98ce386acbfb04eb1fee0b77c90d33b51cc1b557f477812bd165a3`

## Voll-Audit

- 8/8 Hauptwelten unverändert;
- 370 terminale Hobbyseiten;
- 2160 unterste Inhaltskategorien;
- je terminaler Hobbyseite 5–8 Inhaltskategorien;
- 2160/2160 Leafs grob mit mindestens 3–5 vertiefenden Beitragsthemen möglich;
- keine Kategorie unter einer untersten Kategorie;
- keine fehlenden Parents;
- keine doppelten Node-IDs/Slugs;
- keine frageartigen Artikelüberschriften als Kategorien;
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
- Quilten-Leaf präzisiert.

Bewusst nicht automatisch zusammengelegt:
- Asselhaltung / Isopoden-Zucht;
- Münzen / Numismatik;
- Teichwasser-Mikroskopie / Gewässermikroskopie.

## Echte HD-001-Logik lokal simuliert

Resolved Profile:
- Revision `...+16d1bd25b2adfc26`;
- 2656 logische Knoten;
- Validator PASS.

Vollständige synthetische Live-Baseline + Altseiten:
- CREATE 282;
- ADOPT 3;
- UPDATE 2357;
- ARCHIVE 0;
- DEMOTE_EDITORIAL 0;
- 0 Provider-/DataForSEO-Aufrufe;
- 0 Writes im Dry-Run.

ADOPT statt Dublette:
Trainspotting, Modellraketen und Pflanzenbestimmung.

## Betriebsregel

DataForSEO = SEO-/Demand-/Intent-Evidence, **keine Strukturautorität**.

Live-Änderungen ausschließlich:
HD-001 → echter WordPress-Dry-Run → Fingerprint PASS → exakt ein Sync → 100%-Readback.

Frontend/Design liest danach ausschließlich HD-004 und niemals rohe `get_pages()`-Kinder als Strukturwahrheit.

## ERSTER OFFENER BLOCKER

**Der echte kostenlose HD-001-Dry-Run gegen die aktuelle WordPress-Datenbank fehlt noch.**

## EXAKT EINE NEXT ACTION

**HD-001 1.14.9 installieren/aktivieren und im bestehenden Menü „Finaler Zielbaum“ ausschließlich den Dry-Run ausführen. Noch NICHT synchronisieren.**
