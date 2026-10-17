# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE ALTER SNAPSHOT / 1.14.12 REAL BLOCKED / 1.14.13 UND 1.14.14 VERWORFEN / 1.14.15 HARD E2E-SIM PASS / KEIN SYNC**

## Zielvertrag

Aktiv:
`ZV-HOBBYRAUSCH-HD001-001` – Fassung **2.8 / 2026-10-17**.

Verbindlich für die unterste Hobby-Content-Ebene:
- kein starres Einheitsschema;
- bestehende gute Fachbereiche bleiben erhalten;
- Einstieg/Grundlagen und FAQ werden sichtbar abgedeckt;
- Vergleich & Kaufberatung wird bei jedem Hobby geprüft; eigener Leaf nur bei mindestens 3 eigenständigen Beratungs-/Vergleichsintents;
- Ausrüstung/Kosten wird sinnvoll abgedeckt, ohne künstliche Doppelung;
- Pflege, Wartung, Sicherheit, Fehler, Materialien, Methoden, Projekte, Orte, Lernen usw. nur, wenn sie fachlich zum Hobby passen, mindestens 3 eigenständige Intents tragen und keinen vorhandenen Bereich duplizieren;
- Anfänger und Fortgeschrittene müssen beide einen sichtbaren sinnvollen Pfad erhalten.

## Verbindlicher V7.1-Zielbaum

Fachlich unverändert:
- 3517 logische Zielknoten;
- 3487 physische Zielobjekte;
- 862 Hobbyidentitäten;
- 383 CORE-Identitäten;
- 381 terminale Hobbyseiten;
- 2995 sichtbare CORE-Content-Kategorien;
- 381/381 Einstieg/Grundlagen;
- 381/381 FAQ;
- 381/381 Ausrüstung/Kosten-Abdeckung;
- 381/381 Vergleich & Kaufberatung;
- 381/381 mindestens zwei Fach-/Profi-Vertiefungsbereiche;
- pro Hobby 6–10 sichtbare Content-Leafs;
- jeder Leaf mindestens 3 eigenständige Beitragsintentionen.

## Reale Ausgangslage

1.14.12 wurde real ausgeführt:
- BLOCKED;
- 2642 Zielobjekte;
- CREATE 279;
- ADOPT 4;
- UPDATE 2357;
- ARCHIVE 0;
- kein Apply/Sync;
- Kollisionen Libellenbeobachtung und Nachtvogel-Beobachtung.

## Verworfen

### 1.14.13
Verworfen, weil der normale Admin-Seitenaufruf einen vollständigen Frontend-/Struktur-Readback auslöste.

### 1.14.14
Der Admin-Seitenaufruf wurde entlastet, aber der **Dry-Run selbst** war weiterhin zu teuer.

Harte E2E-Simulation des vollständigen V7.1-Dry-Runs mit dem letzten 2357er Bestand plus den beiden real beobachteten Altbindungen:
- Laufzeit lokal: **29.8 s**;
- get_post_meta: **402892**;
- get_term_meta: **11530381**;
- Ursache: der komplette Livebestand wurde für jeden Zielknoten erneut indiziert und die komplette Knotentiefe bei jedem Sortiervergleich neu berechnet.

Damit ist die Timeout-Ursache der 1.14.14 reproduziert. 1.14.14 ist verworfen.

## Einziger Kandidat 1.14.15

Artefakt:
`HD001_V1.14.15_HOBBY_DEPOT_V7_1_DRYRUN_TIMEOUT_FIX_HARDPASS.zip`

SHA-256:
`29289c8ef70469d036be42b1d3ce3401a57a15f298201d099263bba9d61f4165`

V7.1-Profil unverändert:
`23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`

Änderung ausschließlich Performance:
- Live-Bestand wird einmal indiziert statt tausendfach neu;
- Knotentiefe wird einmal berechnet statt bei jedem Sortiervergleich;
- gespeicherter Dry-Run enthält nicht mehr zusätzlich das komplette Zielprofil;
- Admin-Lastfix und Legacy-Reuse aus 1.14.14 bleiben erhalten;
- keine Kategorie, kein Leaf, keine Navigation und keine Architektur geändert.

## Harte E2E-Simulation 1.14.15

Gleiche Ausgangsdaten wie bei 1.14.14:
- Laufzeit lokal: **1.11 s** statt 29.8 s;
- get_post_meta: **6310** statt 402892;
- get_term_meta: **29115** statt 11530381;
- 3517 logisch;
- 3487 physisch;
- CREATE 1126;
- ADOPT 3;
- UPDATE 2358;
- ARCHIVE 1;
- Errors 0;
- Libellenbeobachtung: vorhandene Altseite wird korrekt weiterverwendet;
- Nachtvogel-Beobachtung: vorhandene Altseite wird korrekt weiterverwendet;
- Trainspotting / Modellraketen / Pflanzenbestimmung: ADOPT.

Negativtests:
- fremd gebundener gleicher Slug: BLOCKED;
- doppelte Legacy-Target-Bindung: BLOCKED.

Admin-Aufruf:
- alter 2642er Prüflauf wird nicht als aktueller Nachweis angezeigt;
- keine Seiten-/Term-Vollprüfung beim bloßen Aufruf.

Technik:
- PHP 33/33 PASS;
- ZIP 47/47 PASS;
- Provider Calls 0;
- Dry-Run 0 WordPress-Strukturwrites;
- kein automatischer Apply/Sync.

## Navigation

Keine neue Navigationsidee und kein Umbau.

Live zeigt weiterhin den alten aktiven Snapshot. Die V7.1-Navigation wird erst nach einem sauberen echten Dry-Run und anschließend ausdrücklich bestätigtem Sync aktiv.

## ERSTER OFFENER BLOCKER

**Echter WordPress-V7.1-Dry-Run mit 1.14.15 fehlt.**

## EXAKT EINE NEXT ACTION

**1.14.15 über die aktuell installierte Fassung installieren und ausschließlich den Finalen Delta-Dry-Run ausführen. Keinen Apply/Sync bestätigen.**

Abnahme:
- neuer Dry-Run nutzt 3487 Zielobjekte;
- keine LIVE_COLLISION bei Libellenbeobachtung/Nachtvogel-Beobachtung;
- kein Gateway Timeout.
