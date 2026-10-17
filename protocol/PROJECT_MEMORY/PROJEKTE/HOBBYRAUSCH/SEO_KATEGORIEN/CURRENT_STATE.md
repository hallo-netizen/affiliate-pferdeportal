# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE-BASELINE UNVERÄNDERT / 10ER-PILOT V6 FACHLICH + RENDERER + BROWSER PASS / MAGAZIN-ROUTING KALIBRIERT / IDENTITÄTSBINDUNG NEUER HOBBYS NOCH OFFEN / KEIN WORDPRESS-SYNC**

## Live-Baseline

Produktiv unverändert:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

- 2357 aktive physische Zielobjekte;
- 2357/2357 Readback;
- 8 Hauptwelten;
- 330/330 terminale CORE-Seiten.

## Verbindlicher Zielvertrag

Jeder HOBBY_HUB wird aus zwei Perspektiven geprüft:
1. Anfänger/Neuling;
2. bestehender Nutzer/Fortgeschrittener/Profi.

Pflichtprüfung:
- Einstieg & Grundlagen sichtbar;
- FAQ / Häufige Fragen sichtbar;
- Ausrüstung & Kosten sichtbar, wenn >=3 eigenständige Intents;
- Praxis/Fachvertiefung sichtbar;
- Vergleich & Kaufberatung verpflichtend prüfen;
- jeder sichtbare Leaf mindestens 3 eigenständige Beitragsintentionen;
- vorhandene gute Leafs werden erweitert/umbenannt/zusammengeführt, nicht durch Standardschema dupliziert.

## 10er-Pilot V6 – PASS

Zentral:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_PILOT10_V6_20261017.json`

Kalibrierung:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_PILOT10_CALIBRATION_V6_20261017.json`

Browser:
`/hobby rausch/releases/HOBBY_DEPOT_BROWSER_ACCEPTANCE_PILOT_V6_20261017.json`

Renderer-Simulation:
`/hobby rausch/releases/HOBBY_DEPOT_SIM_PILOT_V6_20261017.txt`

Pilot:
- Buchbinden 7 Leafs;
- Balance Board 8;
- Glasmalerei 9;
- Lasergravieren 9;
- Fledermausbeobachtung 9;
- Hydrokultur 8;
- Riffaquaristik 10;
- Briefmarken sammeln 8;
- Geocaching 9;
- Imkerei 9.

Für alle 10:
- Anfängerabdeckung PASS;
- FAQ PASS;
- Ausrüstung/Kosten PASS;
- Vergleich & Kaufberatung PASS;
- mindestens 2 echte Fach-/Profi-Leafs PASS;
- jeder Leaf >=3 eigenständige Artikelintents PASS.

Wichtige Pilotkorrektur:
- Buchbinden: V5-Doppelung `Ausrüstung & Kosten` + `Ausrüstung` zusammengeführt; bestehender stabile Ausrüstungs-Leaf übernimmt Ausrüstung+Kosten;
- Imkerei: V5-Doppelung `Ausrüstung & Kosten` + `Ausrüstung & Beute` zusammengeführt zu `Ausrüstung, Beuten & Kosten`;
- universelle Nutzerbedürfnisse müssen sichtbar abgedeckt sein, aber nicht durch doppelte Standardschema-Leafs.

## Vergleich & Kaufberatung

Eigenes Büro:
`../PRODUKTVERGLEICH/CURRENT_STATE.md`

Regel:
- Produktgruppen-/Lösungsvergleich;
- Kaufberatung nach Einsatz, Budget, Erfahrung;
- konkrete Produkt-/Modellvergleiche;
- eigener Leaf nur bei >=3 eigenständigen Vergleichs-/Beratungsintents;
- sonst Integration in Ausrüstung/Kosten oder passenden Fachleaf.

Alle 10 Pilot-Hobbys erfüllen die Schwelle.

## Fertigen / Mega-Struktur – fachlich gelöst

V5 hatte mit Modellbau + Naturmaterial 11 echte Mega-Zwischenbereiche.

V6:
- stabiler Hub `Holz` wird zu **Holz & Natur**;
- Besenbinden, Korbflechten, Weidenflechten wechseln von `Naturmaterial` nach `Holz & Natur`;
- `Naturmaterial` wird archiviert;
- Modellbau bleibt unter Fertigen;
- kein Hobby geht verloren.

Ergebnis echte Mega-Zwischenbereiche:
- Gestalten 7;
- Fertigen **10 PASS**;
- Technik 9;
- Forschen 8;
- Pflanzen 9;
- Tiere 7;
- Bewegen 8;
- Sammeln 9.

Direkte Hobby-/Orientierungsseiten wie Heimwerken/Gärtnern bleiben auf der Weltseite erreichbar, zählen aber nicht als Mega-Menü-Zwischenbereich.

## Magazin – kalibriertes Modell

Zentral:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_MAGAZIN_ROUTING_V1_20261017.json`

Die bestehenden 12 Magazin-Kacheln bleiben als Einstiege/Views.

Für kleine/ungewöhnliche echte Hobbys:
- zunächst **ein kanonischer Hobby-Porträt-Artikel pro Hobbyidentität**;
- keine Mini-Taxonomie pro schrägem Hobby;
- zusätzliche Auffindbarkeit über Views/Tags nach Art, Situation, Budget, Saison;
- keine zweite SEO-Kopie eines CORE-Hobbys.

Grobe Art-Views:
- kreativ & handwerk;
- technik & tüfteln;
- natur & forschen;
- tiere;
- bewegung & wettkampf;
- sammeln & suchen;
- genuss & kurioses;
- draußen & abenteuer.

Explizite Masterliste:
- 841 Master-Einträge;
- 77 ausdrücklich als `Besonders schräge Kandidaten / Begriffe` markiert;
- davon 18 bereits exakt als aktive CORE-Hobbys vorhanden → Magazin nur View/Relation, kein zweiter SEO-Artikel;
- übrige Kandidaten vor Artikelproduktion Alias-/Subtopic-Prüfung.

## Identitätsbindung – noch offener Gate

Im V6-Pilotbestand existieren 51 aktive neue `core:proposal:*` Hobbyseiten.

Befund:
- 42/51 lassen sich direkt auf vorhandene Hobby-Master-IDs binden;
- 9 benötigen Intake/Merge:
  - Trainspotting;
  - Ship Spotting;
  - Car Spotting;
  - Sondeln & Metalldetektion;
  - Penjing;
  - Saikei;
  - Kräuteranbau;
  - Obst im Kübel;
  - Terrarienbau.

Besonderheit:
`Sondeln & Metalldetektion` trifft im Master bereits auf getrennte Identitäten `Sondeln` und `Metalldetektion`; hier ist vor Finalisierung eine Merge-/Orientierungsentscheidung nötig.

## Stale-Override-Audit

Vor Finalprofil müssen 9 Altbindungen korrigiert werden:
- Korbflechten, Weidenflechten, Besenbinden zeigen noch auf alten Parent `Naturmaterial`;
- Plane Spotting zeigt im Override noch auf `Messen & Analysieren` statt `Spotting & Verkehr`;
- Lederprägen, Nachtvogel-Beobachtung, Libellenbeobachtung, Wildbienenhotels, Hummelkästen sind im Alt-Override noch EDITORIAL_TOPIC, obwohl sie im Kandidaten CORE sind.

Kein Massensync vor Bereinigung.

## Technische Pilotprüfung

HD-001 TargetTree:
- valid=true;
- 0 Errors;
- 0 Warnings.

Registry-/Design-Vollsimulation:
- 381 terminale Hobbyseiten;
- 0 page-child mismatch;
- 0 category-child mismatch;
- 0 route/world mismatch;
- 0 render mismatch;
- Trainspotting-Negativfall PASS.

Browser:
1920 / 1440 / 1180 / 1024 / 901 / 900 / 768 / 761 / 760 / 390 px:
- alle 8 Mega-Menüs;
- initial 5 gleichmäßige Gruppen;
- `Mehr Kategorien` zeigt sämtliche echten Zwischenbereiche;
- kein horizontaler Overflow;
- direkte Hobbyseiten nicht als Mega-Zwischenbereich;
- Pilot-Leafs vollständig sichtbar.

## Timeout-Korrektur

HD-001 1.14.9 ist verworfen.
Sicherer Kandidat:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.10_MANUAL_ONLY_TIMEOUT_FIX_LOCALPASS.zip`

## ERSTER OFFENER BLOCKER

**Vor Massenausrollung müssen die 51 neuen Proposal-Hobbys an stabile Hobby-Identitäten gebunden und die 9 stale Overrides bereinigt werden.**

## EXAKT EINE NEXT ACTION

**Identitäts-/Override-Bereinigung V6 fertigstellen; danach die im 10er-Pilot bestätigte Leaf-Regel batchweise auf die restlichen HOBBY_HUBs anwenden. Noch kein WordPress-Sync.**
