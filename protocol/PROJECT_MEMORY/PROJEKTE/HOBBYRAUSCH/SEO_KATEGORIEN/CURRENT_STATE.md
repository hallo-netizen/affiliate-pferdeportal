# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE ALTER SNAPSHOT / 1.14.15 REALER V7.1-DRY-RUN 3487 VOLL DURCHGELAUFEN ABER 2 ALTBINDUNGEN BLOCKED / KEIN SYNC / NÄCHSTER KANDIDAT NOCH NICHT FREIGEGEBEN**

## Zielvertrag

Aktiv:
`ZV-HOBBYRAUSCH-HD001-001` – Fassung **2.8 / 2026-10-17**.

Unterste Hobby-Content-Ebene unverändert:
- kein starres Einheitsschema;
- Einstieg/Grundlagen und FAQ sichtbar;
- Vergleich & Kaufberatung je Hobby prüfen, eigener Leaf nur ab >=3 echten Intents;
- Ausrüstung/Kosten sinnvoll abdecken;
- Pflege, Wartung, Sicherheit, Fehler, Materialien, Methoden, Projekte, Orte, Lernen usw. nur bei fachlichem Sinn und ausreichender Tiefe;
- Anfänger und Fortgeschrittene müssen beide sinnvoll bedient werden.

## V7.1-Zielbaum

Unverändert:
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

Vom Nutzer real ausgeführt:
- Status BLOCKED;
- Zielobjekte 3487;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2359;
- UNCHANGED 0;
- ARCHIVE 1;
- EDITORIAL-DEMOTION 0;
- kein Apply/Sync.

Exakt zwei Fehler:
1. `core:proposal:hummelkaesten` – Slug `hummelkaesten` anderweitig gebunden.
2. `core:proposal:lederpraegen` – Slug `lederpraegen` anderweitig gebunden.

Exhaustivitätsnachweis:
1122 + 4 + 2359 = 3485 erfolgreich klassifizierte Zielobjekte.
3485 + exakt 2 Fehler = 3487.
Damit ist der reale Dry-Run über den vollständigen V7.1-Zielbestand gelaufen; es gibt in diesem Lauf keinen versteckten dritten Zielobjekt-Fehler.

Historisch belegte echte alte Live-Bindungen:
- Hummelkästen Objekt 902484: `core:entity:b411cdf2ea6046005a4b`;
- Lederprägen Objekt 902560: `core:entity:ef539e4fcf98dc1c2437`.

Im 1.14.15-Profil standen hierfür andere Legacy-IDs. Das ist die konkrete Ursache der beiden realen Kollisionen.

## Vollworkflow-Nachprüfung vor neuem Release

Es wird ausdrücklich **noch kein neues Plugin freigegeben**.

Die lokale WIP-Reparatur ergänzt nur die zwei real belegten alten Bindungen. Zusätzlich wurde der komplette Weg nach dem Dry-Run getestet, weil sonst der nächste Fehler erst beim Sync sichtbar geworden wäre.

Dabei wurde ein weiterer Performancefehler gefunden und noch vor Release gestoppt:
- der Sync berechnete Knotentiefe wiederholt neu;
- der Sync speicherte seinen großen Zustand nach praktisch jedem einzelnen Knoten;
- dadurch wäre nach einem späteren Dry-Run-PASS die nächste Timeout-/Lastbaustelle wahrscheinlich gewesen.

WIP-Korrektur:
- Knotentiefe/Index einmal vorberechnen;
- Synczustand nur noch pro begrenztem Verarbeitungsschritt speichern, nicht nach jedem einzelnen Knoten;
- Fachbaum, Kategorien und Navigation nicht verändert.

Lokaler Vollworkflow auf dem vollständigen 3487er Zielbaum:
- Dry-Run PASS;
- kompletter Sync COMPLETE;
- Readback 3487/3487;
- Frontend-/Strukturreadback PASS;
- Header-Navigation PASS;
- 381/381 Hobby-Hubs PASS;
- ungebundene CORE-Seiten 0;
- zweiter Dry-Run nach Sync: 3487/3487 UNCHANGED;
- absichtlich fremde Bindung: BLOCKED;
- absichtlich doppelte Legacy-Bindung: BLOCKED;
- absichtlich eingespielter Write-Fehler: ROLLED_BACK; danach ursprünglicher Dry-Run wieder identisch PASS;
- normaler Admin-Aufruf: kein Vollreadback;
- automatischer Start: 0 Writes / 0 Schedules / 0 Network.

Wichtig:
Diese Vollworkflow-Simulation nutzt den vollständigen V7.1-Baum und die real belegten Altbindungen, ist aber **noch keine wortwörtliche Kopie jedes aktuellen WordPress-Datensatzes**. Für diesen letzten 1:1-Nachweis wird der aktuelle JSON-Export des realen 1.14.15-Dry-Runs benötigt.

## Navigation

Keine neue Navigationsidee, keine neue Struktur und kein Architekturumbau.
Live bleibt alter aktiver Snapshot, weil weiterhin kein Sync ausgeführt wurde.

## ERSTER OFFENER BLOCKER

**Der aktuelle reale 1.14.15-Dry-Run-JSON muss gegen den lokal vollständig durchgespielten Reparaturstand 1:1 replayed werden. Vor diesem Nachweis kein neues Plugin an den Nutzer.**

## EXAKT EINE NEXT ACTION

**Aktuellen Button `Finalen Readback als JSON herunterladen` verwenden und genau diese JSON-Datei für den 1:1-Replay bereitstellen. Kein Apply/Sync.**
