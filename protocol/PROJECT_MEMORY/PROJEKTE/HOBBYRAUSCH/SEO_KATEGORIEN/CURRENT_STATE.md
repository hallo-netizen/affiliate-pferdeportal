# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE NOCH ALTER 330ER SNAPSHOT / V7.1 FULL LOCAL + ECHTER DRY-RUN-SIM PASS / MAGAZIN-WEIRD77 PASS / HD-001 1.14.12 MANUAL-ONLY LOCAL HARD PASS / WORDPRESS-DRY-RUN OFFEN / KEIN SYNC**

## Zielvertrag

Aktiv:
`ZV-HOBBYRAUSCH-HD001-001` – Fassung **2.8 / 2026-10-17**.

Neu gegenüber 2.7:
`Vergleich & Kaufberatung` ist verbindliche Affiliate-Prüfung je HOBBY_HUB; eigener Leaf nur ab mindestens 3 eigenständigen Beratungs-/Vergleichsintents, sonst Integration ohne künstliche Doppelung.

## Live-Wahrheit

Aktiv sichtbar ist weiterhin die alte 330er Revision.

Vom Nutzer bestätigt:
- HD-001 live = **1.14.9**;
- 1.14.9 ist wegen Auto-Bootstrap/Timeout verworfen.

## Verbindlicher V7.1-Zielbaum

Profil:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_TARGET_PROFILE_V7_1_DRYRUNFIX_20261017.json`

SHA-256:
`14b7b4b66310ccf19e51e9a4e403628af8705a5ae6f1e14e03f5c87f0991bc7e`

Inhaltlich identisch zum kalibrierten V7-Baum; V7.1 korrigiert ausschließlich die internen Dry-Run-Kontrollzahlen auf den tatsächlich aufgelösten Endbestand.

V7.1:
- 3517 logische Zielknoten;
- 3487 physische Zielobjekte;
- 862 aufgelöste Hobbyidentitäten;
- 383 CORE-Identitäten;
- 381 terminale Hobbyseiten;
- 2995 sichtbare CORE-Content-Kategorien;
- 381/381 Einstieg/Grundlagen;
- 381/381 FAQ;
- 381/381 Ausrüstung/Kosten-Abdeckung;
- 381/381 Vergleich & Kaufberatung;
- 381/381 mindestens zwei Fach-/Profi-Vertiefungsleafs;
- pro Hobby 6–10 sichtbare Content-Leafs;
- jeder Leaf mindestens 3 eigenständige Beitragsintentionen;
- 0 TargetTree-Errors / 0 Warnings;
- Registry-/Renderer-Simulation 0 Abweichungen.

## Echter HD-001-Dry-Run-Algorithmus lokal

Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_V7_1_ACTUAL_DRYRUN_SIM.json`

1:1 gegen simulierten alten 330er Live-Zielbestand:
- Status PASS;
- CREATE 1128;
- ADOPT 3;
- UPDATE 2356;
- ARCHIVE 1;
- DEMOTE_EDITORIAL 0;
- Actions 3488;
- Errors 0;
- Provider Calls 0;
- WordPress Structure Writes 0.

Bekannte ADOPT-Kandidaten der Simulation:
Trainspotting · Modellraketen · Pflanzenbestimmung.

Diese Zahlen sind die **Baseline-Erwartung**. Der echte WordPress-Dry-Run darf abweichen, falls 1.14.9 vor dem Gateway Timeout bereits Drift/Teilzustand hinterlassen hat; deshalb ist der echte Dry-Run zwingend vor Apply.

## Kalibrierte Leaf-Regel

Nicht starr gleich bauen.

Verbindlich:
- bestehende gute Fachleafs bleiben;
- universelle Nutzerbedürfnisse werden sichtbar abgedeckt;
- vorhandener Ausrüstungsleaf übernimmt Kosten, wenn sinnvoll, statt Doppelung;
- FAQ eigener sichtbarer Bereich;
- Vergleich & Kaufberatung eigener Leaf bei >=3 echten Beratungs-/Vergleichsintents;
- Pflege, Wartung, Sicherheit, Probleme, Materialien, Methoden, Projekte, Varianten, Orte, Lernen usw. nur als eigener Leaf bei >=3 echten Intents und ohne Doppelowner.

## Mega-Struktur

Echte Mega-Zwischenbereiche:
Gestalten 7 · Fertigen 10 · Technik 9 · Forschen 8 · Pflanzen 9 · Tiere 7 · Bewegen 8 · Sammeln 9.

Direkte Hobby-/Orientierungsseiten wie Heimwerken/Gärtnern bleiben auf der Weltseite und zählen nicht als Mega-Zwischenbereich.

## Identitäten / Magazin

- 51/51 neue CORE-Hobbyseiten stabil gebunden;
- stale Overrides: 0;
- Plane Spotting → Spotting & Verkehr;
- Sondeln + Metalldetektion = eine kanonische Hobbyidentität.

Magazin-Audit:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_MAGAZIN_WEIRD77_ROUTING_AUDIT_20261017.json`

- 77 ausdrücklich schräge Kandidaten geprüft;
- 37 CORE_RELATION;
- 28 PORTRAIT_CANDIDATE;
- 12 PORTRAIT_ALIAS;
- 35 eindeutige Porträt-Owner;
- 0 offene Owner-Reviews.

## Sicherer HD-001-Kandidat

`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.12_HOBBY_DEPOT_V7_1_MANUAL_ONLY_LOCALPASS.zip`

SHA-256:
`2a0ac6e936628baf7aff3b0ed67bdecd60a9ca9ba23d992396fa4d0abf2b0a5f`

Safety:
- PHP 33/33 PASS;
- ZIP PASS;
- manual-only true;
- Target-Runner-init-hooks 0;
- Installation/Aktivierung: Writes 0 / Schedules 0 / Network 0;
- echter Plugin-Resolver: 3517 Knoten / 862 Entities / 0 Errors / 0 Warnings;
- echter Dry-Run-Algorithmus gegen Baseline: PASS;
- Dry-Run startet keinen Apply.

## DataForSEO

Evidence, Keyword-/Fragen-/Clustering-Hilfe.
Nie Strukturautorität.

## ERSTER OFFENER BLOCKER

**Der echte manuelle V7.1-Dry-Run gegen die aktuelle WordPress-Datenbank fehlt.**

## EXAKT EINE NEXT ACTION

**Live HD-001 1.14.9 durch 1.14.12 ersetzen und danach ausschließlich den manuellen Finalen Delta-Dry-Run ausführen. Noch keinen Apply/Sync bestätigen.**
