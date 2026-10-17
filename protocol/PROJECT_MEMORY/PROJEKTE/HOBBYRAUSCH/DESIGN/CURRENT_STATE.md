# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.50.668 + ALTER 330ER SNAPSHOT / 1.50.669 V7-MEGA-RENDERER LOCAL PASS / NICHT RELEASED / V7 NICHT LIVE**

## Live-Wahrheit

WordPress bestätigt:
`Affiliate Portal Template Kit 1.50.668` aktiv.

1.50.668 nutzt HD-004 als Strukturquelle. Solange HD-004 die alte 330er Revision liefert, bleibt der sichtbare Strukturinhalt weitgehend alt.

Die terminale `category`-Ebene funktioniert bereits; Beispiel Ameisenhaltung zeigt die echte letzte Content-Kategorieebene.

## Lokaler WIP 1.50.669

Arbeitsbasis:
1.50.668.

Änderung:
Mega-Menü unterscheidet jetzt korrekt:
- echte Zwischenbereiche = Mega-Spalten;
- direkte Hobbys/Orientierungsseiten wie Heimwerken/Gärtnern = nur Weltseite, keine zusätzliche Mega-Spalte.

V7-Mega-Zahlen:
Gestalten 7 · Fertigen 10 · Technik 9 · Forschen 8 · Pflanzen 9 · Tiere 7 · Bewegen 8 · Sammeln 9.

Darstellung:
- initial 5 gleichmäßige Gruppen;
- `Mehr Kategorien` öffnet restliche echte Zwischenbereiche im selben Flyout;
- genau eine weitere kompakte Orientierungsebene;
- kein Vollbaum;
- keine Roh-`get_pages()`-Struktur;
- Registry fail-closed.

## Local QA V7

V7-Profil:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_V7_CALIBRATED_ROLLOUT_20261017.json`

Browser-QA:
`/hobby rausch/releases/HOBBY_DEPOT_BROWSER_ACCEPTANCE_V7_20261017.json`

Renderer-QA:
`/hobby rausch/releases/HOBBY_DEPOT_SIM_V7_20261017.txt`

PASS:
- 381 Hobbyseiten;
- komplette terminale Category-Ebene;
- 0 Struktur-/Route-/Render-Mismatches;
- Trainspotting-Falschparent ausgeschlossen;
- alle 8 Mega-Menüs;
- 1920 / 1440 / 1180 / 1024 / 901 / 900 / 768 / 761 / 760 / 390 px;
- kein horizontaler Overflow;
- Fertigen: 10 echte Zwischenbereiche;
- Pflanzen: direkte Gärtnern-Hobbyseite nicht als Mega-Zwischenbereich;
- PHP 61/61 PASS.

## 1.50.669 Fail-closed QA

QA:
`/hobby rausch/releases/HOBBY_DEPOT_1.50.669_WIP_FAILCLOSED_QA.json`

Bildbriefs:
`/hobby rausch/releases/HOBBY_DEPOT_V7_HUB2_IMAGE_BRIEFS_20261017.json`

PASS:
- PHP 61/61;
- Hub2-Weltbild-Fallback im aktiven 1.50.669-Renderer entfernt;
- exakt 5 neue Hub2 sind noch unmapped: Modellbau, Spotting & Verkehr, Citizen Science, Natur bestimmen, Suchen & Finden;
- Holz & Natur besitzt zwar ein altes Holzmotiv, dieses ist semantisch zu eng und deshalb REPLACE_REQUIRED;
- insgesamt exakt 6 neue Hero+Preview-Paare nötig.



1.50.668 enthält die bisherige zentrale Hero-/Preview-Logik.

Vor V7-Live-Sync brauchen neue direkte Hub2 gemäß Bildvertrag eigenes geprüftes Hero + daraus abgeleitete Preview:
- Spotting & Verkehr;
- Citizen Science;
- Natur bestimmen;
- Suchen & Finden;
- Modellbau.

`Holz & Natur` ist geprüft: das vorhandene Holzwerkstatt-Motiv ist für Holz + Besenbinden + Korbflechten + Weidenflechten zu eng und damit FAIL. Neues eigenes Motiv erforderlich.

Kein generischer Weltbild-Fallback.

## Alte Patchplugins

Hero-Patcher 1.50.659 / 1.50.661 / 1.50.662 sind Übergangsstände und sollen nach kontrollierter Bereinigung nicht parallel die Bildwahrheit überlagern.

## PASS-GRENZE

1.50.669 ist **noch kein Release**.
Kein Live-PASS ohne:
- V7 WordPress-Dry-Run;
- Bilder für neue Hub2;
- finalen ZIP-/Browsercheck;
- echten Live-Readback.

## EXAKT EINE NEXT ACTION

**Zuerst den V7-Dry-Run mit HD-001 1.14.11 durchführen. Parallel lokal die sechs erforderlichen Hub2-Hero/Preview-Paare abschließen; erst danach 1.50.669 als Release packen.**
