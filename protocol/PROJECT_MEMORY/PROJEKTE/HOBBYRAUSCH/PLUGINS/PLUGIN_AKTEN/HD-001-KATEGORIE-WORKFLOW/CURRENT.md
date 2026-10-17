# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.14.12 REAL BLOCKED / 1.14.13 + 1.14.14 VERWORFEN / 1.14.15 HARD E2E-SIM PASS / ECHTER WORDPRESS-DRY-RUN OFFEN**

## Reale Ausgangslage

1.14.12:
- BLOCKED;
- 2642 Zielobjekte;
- CREATE 279 / ADOPT 4 / UPDATE 2357 / ARCHIVE 0;
- Kollisionen Libellenbeobachtung und Nachtvogel-Beobachtung;
- kein Apply/Sync.

## Fehlerkette

1.14.13:
- Adminseite führte beim bloßen Öffnen Vollreadback aus;
- verworfen.

1.14.14:
- Adminseite entlastet;
- Dry-Run selbst weiterhin zu langsam;
- harte vollständige Simulation: 29.8 s lokal;
- 402892 Post-Metalesungen;
- 11530381 Term-Metalesungen;
- verworfen.

Ursache 1.14.14:
- Live-Objektindizes wurden für jeden der 3487 Zielknoten erneut aufgebaut;
- Knotentiefe wurde während der Sortierung bei jedem Vergleich erneut über den gesamten Baum berechnet.

## Einziger Kandidat

`HD001_V1.14.15_HOBBY_DEPOT_V7_1_DRYRUN_TIMEOUT_FIX_HARDPASS.zip`

SHA-256:
`29289c8ef70469d036be42b1d3ce3401a57a15f298201d099263bba9d61f4165`

Profil-SHA:
`23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`

## Änderung 1.14.15

Nur enger Performance-Fix:
- Live-Objekte einmal indizieren;
- Zielknotentiefe einmal vorberechnen;
- gespeicherten Dry-Run ohne redundantes komplettes Zielprofil ablegen;
- 1.14.14 Admin-Load-Fix, V7.1-Hardbinding und Legacy-Reuse unverändert übernehmen;
- keine Fach-, Kategorie-, Navigations- oder Architekturänderung.

## Harte Positivprüfung

Vollständiger `APKW_TargetTreeDryRun::build()` gegen realitätsnahe 2357er Baseline plus die beiden real beobachteten Altseiten:

1.14.14:
- 29.775 s;
- get_post_meta 402892;
- get_term_meta 11530381.

1.14.15:
- 1.113 s;
- get_post_meta 6310;
- get_term_meta 29115;
- get_posts 2;
- get_terms 6.

Ergebnis 1.14.15:
- PASS;
- 3487 Zielobjekte;
- CREATE 1126;
- ADOPT 3;
- UPDATE 2358;
- ARCHIVE 1;
- Errors 0;
- Libellenbeobachtung → vorhandene Seite UPDATE/reuse;
- Nachtvogel-Beobachtung → vorhandene Seite UPDATE/reuse.

## Harte Negativprüfung

- fremd gebundener Slug → BLOCKED;
- doppelte Legacy-Target-Bindung → BLOCKED;
- alter gespeicherter Dry-Run → nicht als aktuell angezeigt;
- normaler Admin-Aufruf → keine Vollprüfung.

## Technik

- PHP 33/33 PASS;
- ZIP 47/47 PASS;
- ZIP-Test ohne Fehler;
- Dry-Run 0 Strukturwrites;
- Provider Calls 0;
- kein Apply/Sync automatisch.

## Isoliertes Artefakt

`CURRENT.zip` bleibt noch nicht synchronisiert.

Grund:
Der echte WordPress-Dry-Run mit 1.14.15 ist noch offen.

## EXAKT EINE NEXT ACTION

**1.14.15 installieren → ausschließlich Finalen Delta-Dry-Run ausführen → keinen Apply/Sync.**
