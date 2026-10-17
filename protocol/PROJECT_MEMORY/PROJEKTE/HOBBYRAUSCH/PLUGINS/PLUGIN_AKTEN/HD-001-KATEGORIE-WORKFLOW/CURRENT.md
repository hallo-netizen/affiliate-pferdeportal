# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.14.15 REAL BLOCKED / REALER JSON-EXPORT AKTION-FÜR-AKTION 1:1 REPLAYED / 1.14.16 FULL-WORKFLOW HARD PASS / ECHTER WP-DRY-RUN OFFEN**

## Reale Ausgangslage

1.14.15 real:
- BLOCKED;
- 3487 Zielobjekte;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2359;
- UNCHANGED 0;
- ARCHIVE 1;
- exakt zwei LIVE_COLLISION;
- kein Apply/Sync.

## 1:1-Ausgangsnachweis

Der vom Nutzer exportierte aktuelle 1.14.15-JSON-Readback wurde vollständig replayed.

Mit dem echten 1.14.15-Dry-Run-Code auf der rekonstruierten Live-Ausgangslage:
- 3486/3486 Aktionen exakt identisch;
- Reihenfolge exakt identisch;
- Objekt-IDs, Aktionsarten und Mismatch-Gründe exakt identisch;
- Summary exakt identisch;
- Fehler exakt identisch;
- `action_exact=true`;
- `diffs=[]`.

Damit ist die lokale Ausgangslage jetzt gegen den realen Lauf kalibriert.

## Ursache

Die beiden tatsächlichen alten Live-Bindungen waren:
- Hummelkästen Objekt 902484 -> `core:entity:b411cdf2ea6046005a4b`;
- Lederprägen Objekt 902560 -> `core:entity:ef539e4fcf98dc1c2437`.

1.14.15 kannte für diese neuen Proposal-Ziele andere Legacy-IDs.

## Einziger Kandidat

`HD001_V1.14.16_HOBBY_DEPOT_V7_1_EXACT_REPLAY_FULL_WORKFLOW_HARDPASS.zip`

ZIP SHA-256:
`bbee98fbf9bbfadf49f18bf64e9f64aba1a274b2266a1473ec89d87996654792`

Profil SHA-256:
`87275396fdd8e2e9d15b0a37a6d17a7a21889825d7cdb3f64f276005c73b99d0`

## Änderungen 1.14.16

Enger Reparaturscope:
- exakt die zwei real belegten alten Target-IDs als zulässige Migrationsbindungen ergänzen;
- Sync-Tiefenberechnung und Indizes vorberechnen;
- Readback-State pro Batch statt pro Objekt speichern;
- Profil separat vom laufenden Sync-State halten;
- Write-State bleibt zur Rollback-Sicherheit abgesichert;
- keine Fach-, Kategorie-, Navigations- oder Architekturänderung.

## Vollworkflow-Positivtest

Exakte Live-Replay-Ausgangslage -> 1.14.16 Dry-Run:
- PASS;
- 3487 Ziele;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2361;
- ARCHIVE 1;
- Errors 0.

Danach tatsächlicher Runner-Weg:
- Start manuell;
- 528 begrenzte Verarbeitungsschritte;
- COMPLETE;
- created 1122;
- updated 2361;
- adopted 4;
- archived 1;
- readback 3487/3487;
- Fehler leer.

Frontend-/Strukturkontrolle:
- 8 Hauptwelten;
- Contentfilter PASS;
- Headerfilter PASS;
- Headernavigation PASS;
- erwartete Header-Einträge 112;
- 381/381 Hobbyseiten PASS;
- Leaf-Verteilung 6–10;
- ungebundene CORE-Seiten 0.

Idempotenz:
- zweiter echter Dry-Run nach COMPLETE:
  CREATE 0 / ADOPT 0 / UPDATE 0 / UNCHANGED 3487 / ARCHIVE 0 / Errors 0.

## Vollworkflow-Negativtests

- Hummelkästen fremd gebunden -> BLOCKED;
- Hummelkästen doppelte Altbindung -> BLOCKED;
- Lederprägen fremd gebunden -> BLOCKED;
- Lederprägen doppelte Altbindung -> BLOCKED;
- Livebestand nach Dry-Run verändert -> echter Apply-Pfad lehnt Plan ab;
- Schreibfehler nach 75 Änderungen injiziert -> ROLLBACK_PENDING -> ROLLED_BACK;
- nach Rollback Dry-Run-Plan exakt wiederhergestellt;
- normaler Admin-Seitenaufruf -> 0 Vollscan-Abfragen;
- manual-only Bootstrap -> 0 Writes / 0 Schedules / 0 Network.

## Performance

Vor Release zusätzlich der Folgeschritt geprüft:
- alter Tiefensortierpfad lokal ca. 24 s;
- vorberechnete Tiefe ca. 0.012 s;
- vollständiger Sync wird in begrenzte kurze Requests geteilt;
- kein einzelner lokaler Verarbeitungsschritt nähert sich einem Timeout.

## Paketprüfung

- PHP 33/33 PASS;
- ZIP 44/44 PASS;
- Unzip PASS;
- Roundtrip-Dateihashes 44/44 identisch.

## Isoliertes Artefakt

`CURRENT.zip` bleibt **noch nicht synchronisiert**.

Grund:
Der echte WordPress-Dry-Run mit 1.14.16 ist weiterhin offen. Erst wenn der reale Lauf exakt den erwarteten PASS liefert, darf über Sync/Artefakt-Synchronisierung entschieden werden.

## EXAKT EINE NEXT ACTION

**1.14.16 installieren -> nur Finalen Delta-Dry-Run ausführen -> keinen Apply/Sync.**

Erwartung:
3487 Ziele / CREATE 1122 / ADOPT 4 / UPDATE 2361 / UNCHANGED 0 / ARCHIVE 1 / Errors 0.
