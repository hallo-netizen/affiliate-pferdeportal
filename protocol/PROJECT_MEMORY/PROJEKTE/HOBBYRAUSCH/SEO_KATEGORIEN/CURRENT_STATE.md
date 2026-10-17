# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.14.15 REAL BLOCKED / REALER JSON-EXPORT 1:1 REPLAYED / 1.14.16 FULL-WORKFLOW HARD PASS / ECHTER WORDPRESS-DRY-RUN 1.14.16 OFFEN / KEIN SYNC**

## Zielvertrag

Aktiv:
`ZV-HOBBYRAUSCH-HD001-001` – Fassung **2.8 / 2026-10-17**.

Unterste Hobby-Content-Ebene unverändert:
- kein starres Einheitsschema;
- Einstieg/Grundlagen und FAQ sichtbar;
- Vergleich & Kaufberatung je Hobby prüfen; eigener Leaf nur ab mindestens 3 echten Intents;
- Ausrüstung/Kosten sinnvoll abdecken;
- Pflege, Wartung, Sicherheit, Fehler, Materialien, Methoden, Projekte, Orte, Lernen usw. nur bei fachlichem Sinn und ausreichender Tiefe;
- Anfänger und Fortgeschrittene müssen beide sinnvoll bedient werden.

## V7.1-Zielbaum

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
- 381/381 mindestens zwei Fach-/Profi-Vertiefungen;
- 6–10 sichtbare Content-Leafs je Hobby.

## Reales WordPress-Ergebnis 1.14.15

Der echte Nutzerexport `hobby-depot-final-target-readback-20261017-113602-utc.json` wurde vollständig als Referenz übernommen.

Realer Stand:
- Plugin 1.14.15;
- BLOCKED;
- 3517 logisch / 3487 physisch;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2359;
- UNCHANGED 0;
- ARCHIVE 1;
- exakt zwei Fehler;
- kein Apply/Sync.

Fehler:
- Hummelkästen;
- Lederprägen.

## Exakter 1:1-Replay des realen Exports

Der echte 1.14.15-Lauf wurde nicht mehr nur nach Summen, sondern **Aktion für Aktion** lokal reproduziert.

Ergebnis:
- 3486/3486 ausgegebene Aktionen identisch;
- Reihenfolge identisch;
- Objekt-IDs identisch;
- Aktionsarten identisch;
- Mismatch-Gründe identisch;
- Summen identisch;
- genau dieselben zwei Fehler;
- `action_exact = true`;
- `diffs = []`.

Damit ist erstmals belegt, dass die lokale Ausgangslage den realen WordPress-Dry-Run vollständig reproduziert.

## Exakte Ursache der zwei realen Blocker

Historisch belegte alte Live-Bindungen:
- Hummelkästen, Objekt 902484: `core:entity:b411cdf2ea6046005a4b`;
- Lederprägen, Objekt 902560: `core:entity:ef539e4fcf98dc1c2437`.

Diese beiden tatsächlichen alten IDs fehlten in 1.14.15.

1.14.16 ergänzt ausschließlich diese real belegten Altbindungen. Keine Fachkategorie und keine Navigation wurde geändert.

## 1.14.16 – kompletter Workflow vor Freigabe simuliert

Dry-Run auf exakt reproduzierter Ausgangslage:
- PASS;
- 3487 Zielobjekte;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2361;
- UNCHANGED 0;
- ARCHIVE 1;
- Errors 0;
- Hummelkästen wird als vorhandene Seite weiterverwendet;
- Lederprägen wird als vorhandene Seite weiterverwendet.

Danach wurde nicht gestoppt, sondern der komplette Folgeschritt lokal mit dem echten Runner durchgespielt:
- manueller Sync bis COMPLETE;
- Readback 3487/3487;
- Frontend-/Strukturreadback PASS;
- Header-Navigation PASS;
- 381/381 Hobbyseiten PASS;
- ungebundene CORE-Seiten 0;
- zweiter Dry-Run nach COMPLETE: 3487/3487 UNCHANGED.

## Negativ- und Fehlerfälle

Geprüft:
- fremde Hummelkästen-Bindung -> BLOCKED;
- doppelte Hummelkästen-Altbindung -> BLOCKED;
- fremde Lederprägen-Bindung -> BLOCKED;
- doppelte Lederprägen-Altbindung -> BLOCKED;
- Änderung des Livebestands zwischen Dry-Run und Apply -> Apply wird abgelehnt;
- absichtlich injizierter Schreibfehler -> ROLLED_BACK;
- nach Rollback ist der ursprüngliche Dry-Run-Plan wieder exakt identisch;
- normaler Admin-Aufruf -> kein Vollscan;
- manual-only Bootstrap -> 0 Writes / 0 Schedules / 0 Network.

## Performance vor Release

Zusätzlich wurde der spätere Syncpfad geprüft. Dabei wurde ein weiterer möglicher Timeout noch **vor** einem Nutzerlauf beseitigt:
- Knotentiefe wird einmal vorbereitet statt ständig neu berechnet;
- Live-/Zielindizes werden wiederverwendet;
- Readback-Zustand wird gebündelt gespeichert;
- Schreibschritte bleiben aus Rollback-Sicherheitsgründen einzeln abgesichert.

Lokale Lastprüfung:
- 1.14.14 alter Dry-Run ca. 29.8 s;
- 1.14.15 optimierter Dry-Run ca. 1 s;
- 1.14.16 kompletter Sync in begrenzten kurzen Schritten;
- kein einzelner lokaler Sync-Schritt näherte sich einem Timeout.

## Kandidat

`HD001_V1.14.16_HOBBY_DEPOT_V7_1_EXACT_REPLAY_FULL_WORKFLOW_HARDPASS.zip`

ZIP SHA-256:
`bbee98fbf9bbfadf49f18bf64e9f64aba1a274b2266a1473ec89d87996654792`

Profil SHA-256:
`87275396fdd8e2e9d15b0a37a6d17a7a21889825d7cdb3f64f276005c73b99d0`

Paketprüfung:
- PHP 33/33 PASS;
- ZIP 44/44 PASS;
- Unzip PASS;
- Roundtrip-Dateihashes 44/44 identisch.

## Navigation

Keine neue Navigationsidee, keine neue Struktur und kein Architekturumbau.

Live bleibt weiterhin der alte aktive Snapshot, weil noch kein V7.1-Sync durchgeführt wurde. Die Navigation darf erst nach echtem 1.14.16-Dry-Run-PASS synchronisiert werden.

## ERSTER OFFENER BLOCKER

**Der echte WordPress-Dry-Run mit 1.14.16 fehlt noch.**

## EXAKT EINE NEXT ACTION

**HD-001 1.14.16 installieren und ausschließlich den Finalen Delta-Dry-Run ausführen. Keinen Apply/Sync bestätigen.**

Erwarteter echter Lauf:
- 3487 Zielobjekte;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2361;
- UNCHANGED 0;
- ARCHIVE 1;
- Errors 0.

Bei jeder Abweichung: sofort stoppen, kein Sync.
