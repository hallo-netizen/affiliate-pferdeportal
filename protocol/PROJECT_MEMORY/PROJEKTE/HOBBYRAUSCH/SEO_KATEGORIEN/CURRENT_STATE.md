# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-16
STATUS: **LIVE-BASELINE 2026-10-09 UNVERÄNDERT / V3-VOLLAUDIT-KANDIDAT ZENTRAL ABGELEGT / HD-001 TARGETTREE VALIDATOR PASS / NOCH KEIN LIVE-SYNC**

## Autoritative Bindung

Zielvertrag:
`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md` – Fassung 2.7.

Zentrale Kategorie-Unterzentrale:
`KATEGORIE_ZENTRALE/START_HERE.md`

Technische Plugin-Wahrheiten:
- Bearbeiten/Sync: `../PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`
- schlanker Runtime-Kern: `../PLUGINS/PLUGIN_AKTEN/HD-004-KATEGORIE-KERN/CURRENT.md`

Finale Live-Evidence:
`HD001_FINAL_LIVE_ACCEPTANCE_20261009.md`.

## Produktive Live-Baseline – unverändert

- Live-Profilrevision `HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`;
- 2371 logische Knoten;
- 2366 aktive Nodes;
- 2357 aktive physische Zielobjekte;
- 2357/2357 Readback;
- Runner COMPLETE / `TARGET_TREE_SYNC_AND_READBACK_PASS`;
- Frontend valid=true;
- 8 Welten;
- 330/330 terminale CORE-Seiten im Kategorie-Gate;
- 1920 aktive CORE-Content-Kategorien.

## V3-Voll-Audit-Kandidat – zentral / NOCH NICHT LIVE

Kandidat:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_AUDIT_CANDIDATE_V3_20261016.json`

SHA-256:
`6d73e5d4d32e91acf6a5c8dd19dc9e23af4a661dc053fa7a752a4ea4668826e7`

Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_FULL_STRUCTURE_AUDIT_V3_20261016.json`

Lokaler Befund:
- 8/8 Hauptwelten unverändert;
- 370 terminale Hobbyseiten;
- 2160 unterste CORE-Inhaltskategorien;
- jede terminale Hobbyseite hat 5–8 Inhaltskategorien;
- keine unterste Inhaltskategorie hat weitere Kategorie-Kinder;
- 2160/2160 unterste Inhaltskategorien grob auf mindestens 3–5 vertiefende Beitragsthemen geprüft: PASS;
- 120 besonders kurze/enge Kategorien zusätzlich manuell semantisch gegengeprüft;
- 0 doppelte Node-IDs;
- 0 doppelte Slugs;
- 0 fehlende Parents;
- 0 sibling-name-Dubletten;
- 0 frageartige Artikelüberschriften als Kategorien;
- HD-001 `APKW_TargetTree::validate`: VALID / 0 Errors / 0 Warnings.

Wesentliche Korrekturen:
- Plane Spotting aus `Messen & Analysieren` nach `Spotting & Verkehr`;
- `Messen & Analysieren` danach: Wasseranalyse, Bodenanalyse, Spektroskopie, Elektrochemie als Hobby;
- neue Forschen-Hubs: `Spotting & Verkehr`, `Citizen Science`, `Natur bestimmen`;
- neue Sammeln-Struktur: `Suchen & Finden` plus Erweiterung `Naturfunde`;
- `Modellbau` nach erneuter Prüfung unter `Fertigen`, nicht unter Technik;
- Gestalten `Miniaturen & Szenen` erweitert;
- Tiere `Wirbellose` um Schneckenhaltung erweitert;
- tautologische Leaf-Kategorie `Quilten → Quilten` ersetzt durch `Quiltmuster & Stichführung`.

Keine automatische Änderung:
- Asselhaltung / Isopoden-Zucht bleiben vorerst getrennt: Haltung vs Zucht;
- Münzen / Numismatik bleiben vorerst getrennt: späterer Kannibalisierungscheck;
- Teichwasser-Mikroskopie / Gewässermikroskopie bleiben vorerst getrennt.

## Kategorie-Zentrale

Verbindliches Register:
`KATEGORIE_ZENTRALE/REGISTER.md`

Dort liegen:
- aktive Live-Baseline;
- V3-Audit-Kandidat;
- Voll-Audit;
- HD-001 1.14.8;
- HD-004 1.0.0;
- stabile Runtime-/Snapshot-Bindung.

## Harte Betriebsregel

DataForSEO:
- SEO-/Demand-/Intent-Evidence;
- **keine Strukturautorität**;
- darf keine Welt, keinen Parent und keine neue Kategorie erfinden.

Strukturänderungen:
HD-001 1.14.8 gezielt aktivieren → Delta/Dry-Run → POS+NEG-Regressionsprüfung → genau ein Sync → 100%-Readback.

Frontend/Design:
muss anschließend ausschließlich den neutralen HD-004-Runtime-Vertrag verwenden und darf keine rohen WordPress-`get_pages()`-Kinder als Strukturwahrheit verwenden.

## ERSTER OFFENER BLOCKER

**Der V3-Kandidat ist vollständig lokal validiert, aber noch nicht durch den HD-001-Delta-/Dry-Run gegen die produktive Live-Baseline gelaufen.**

## EXAKT EINE NEXT ACTION

**V3 gegen die aktive Live-Baseline als HD-001-Delta/Dry-Run prüfen; NOCH KEIN Live-Sync.**
