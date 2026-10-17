# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE NOCH ALTER 330ER SNAPSHOT / V7 CALIBRATED FULL LOCAL PASS / MAGAZIN-WEIRD77 PASS / HD-001 1.14.11 MANUAL-ONLY LOCAL PASS / WORDPRESS-DRY-RUN OFFEN / KEIN SYNC**

## Live-Wahrheit

Aktiv sichtbar ist weiterhin die alte Revision:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

- 8 Hauptwelten;
- 330 terminale CORE-Hobbyseiten;
- V7 ist **noch nicht live**.

## Verbindlicher V7-Zielbaum

Profil:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_V7_CALIBRATED_ROLLOUT_20261017.json`

SHA-256:
`a36a7b1b3639b503028d2339c17fcc04ca349769c4f3d2d5dfdb11f8061325fc`

Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_FULL_LEAF_ROLLOUT_AUDIT_V7_20261017.json`

Resolved-/HD-001-Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_RESOLVED_V7_AUDIT_20261017.json`

V7:
- 3517 Zielknoten;
- 381 terminale Hobbyseiten;
- 381/381 Einstieg/Grundlagen;
- 381/381 FAQ;
- 381/381 Ausrüstung/Kosten-Abdeckung;
- 381/381 Vergleich & Kaufberatung;
- 381/381 mindestens zwei Fach-/Profi-Vertiefungsleafs;
- pro Hobby 6–10 sichtbare Content-Leafs;
- jeder Leaf mindestens 3 eigenständige Beitragsintentionen;
- keine fehlenden Parents;
- keine doppelten Node-IDs/Slugs;
- 0 TargetTree-Errors / 0 Warnings;
- Registry-/Renderer-Simulation 0 Abweichungen.

## Kalibrierte Leaf-Regel

Nicht starr gleich bauen.

Verbindlich:
- bestehende gute Fachleafs bleiben;
- universelle Nutzerbedürfnisse werden sichtbar abgedeckt;
- vorhandener Ausrüstungsleaf übernimmt Kosten, wenn sinnvoll, statt Doppelung;
- FAQ bleibt eigener sichtbarer Bereich;
- Vergleich & Kaufberatung eigener Leaf nur bei >=3 echten Beratungs-/Vergleichsintents;
- Pflege, Wartung, Sicherheit, Probleme, Materialien, Methoden, Projekte, Varianten, Orte, Lernen usw. nur als eigener Leaf bei >=3 echten Intents und ohne Doppelowner.

## Mega-Struktur V7

Echte Mega-Zwischenbereiche:
- Gestalten 7;
- Fertigen 10;
- Technik 9;
- Forschen 8;
- Pflanzen 9;
- Tiere 7;
- Bewegen 8;
- Sammeln 9.

Fertigen:
- `Holz` → `Holz & Natur`;
- Besenbinden, Korbflechten, Weidenflechten dort eingeordnet;
- alter Hub `Naturmaterial` archiviert;
- Modellbau bleibt eigener Zwischenbereich;
- kein Hobby verloren.

Direkte Hobby-/Orientierungsseiten wie Heimwerken/Gärtnern bleiben auf der Weltseite, zählen aber nicht als Mega-Zwischenbereich.

## Identitäten / Overrides

51/51 neue V7-Hobbyseiten stabil gebunden:
- 42 an bestehende Master-IDs;
- 8 neue stabile Master-Identitäten;
- Sondeln + Metalldetektion bewusst zu einer kanonischen Identität zusammengeführt.

Stale Overrides nach Bereinigung:
**0**

Plane Spotting:
`Forschen → Spotting & Verkehr`

Spotting & Verkehr:
Plane Spotting · Trainspotting · Ship Spotting · Car Spotting

## Magazin

Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_MAGAZIN_WEIRD77_ROUTING_AUDIT_20261017.json`

- 12 bestehende Magazin-Kacheln bleiben Einstiegs-/View-Struktur;
- keine zweite konkurrierende Hobby-Taxonomie;
- pro eigenständigem kleinen/skurrilen Hobby zunächst ein kanonisches Hobby-Porträt;
- CORE-Hobby im Magazin nur Relation/View, keine zweite SEO-Hobbyseite;
- 77 ausdrücklich schräge Master-Kandidaten geprüft;
- 37 CORE_RELATION;
- 28 PORTRAIT_CANDIDATE;
- 12 PORTRAIT_ALIAS;
- 35 eindeutige Porträt-Owner nach Merge;
- 0 offene Owner-Reviews.

## DataForSEO

Evidence, Keyword-/Fragen-/Clustering-Hilfe.
Nie Strukturautorität.

## Sicherer HD-001-Kandidat

`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.11_HOBBY_DEPOT_V7_MANUAL_ONLY_LOCALPASS.zip`

SHA-256:
`d441f36899ce8ef6fd8a47051ea066e24aeb41ac6ec07f28c2cae5c11444311e`

- 1.14.9 = verworfen / Timeout-Risiko;
- 1.14.11 = manual-only;
- Installation/Aktivierung: 0 Target-Runner-init-hooks, 0 Writes, 0 Schedules, 0 Network;
- eingebettetes V7-Profil: 3517 Knoten, Hash identisch;
- ZIP 47/47 PASS;
- Dry-Run kann keinen Sync starten;
- Apply bleibt separater bestätigungspflichtiger Weg.

## ERSTER OFFENER BLOCKER

**Der echte manuelle V7-Dry-Run gegen die aktuelle WordPress-Datenbank fehlt. V7 darf vorher nicht synchronisiert werden.**

## EXAKT EINE NEXT ACTION

**Live HD-001 1.14.9 durch 1.14.11 ersetzen und anschließend ausschließlich den manuellen V7-Final-Dry-Run ausführen. Noch keinen Apply/Sync bestätigen.**
