# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.14.15 REALER DRY-RUN 3487 VOLLSTÄNDIG / 2 ALTBINDUNGEN BLOCKED / KEIN SYNC / WIP-NACHFOLGER VOLLWORKFLOW LOKAL PASS ABER NOCH NICHT 1:1-LIVE-REPLAYED**

## Reales Ergebnis 1.14.15

- BLOCKED;
- 3487 Zielobjekte;
- CREATE 1122;
- ADOPT 4;
- UPDATE 2359;
- UNCHANGED 0;
- ARCHIVE 1;
- exakt 2 Fehler;
- kein Apply/Sync.

Fehler:
- Hummelkästen;
- Lederprägen.

3485 erfolgreiche Zielaktionen + 2 Fehler = 3487. Der echte WordPress-Dry-Run hat damit den gesamten V7.1-Zielbestand abgearbeitet.

## Exakte Ursache

Hummelkästen live:
- Objekt 902484;
- alte Bindung `core:entity:b411cdf2ea6046005a4b`.

Lederprägen live:
- Objekt 902560;
- alte Bindung `core:entity:ef539e4fcf98dc1c2437`.

Diese beiden alten Live-Bindungen fehlten in den Legacy-Listen des 1.14.15-Profils.

## Kein neuer Release

Es wird noch kein Nachfolger ausgegeben.

Vor einem neuen ZIP wurde der komplette weitere Workflow lokal durchgespielt. Dabei fiel zusätzlich auf, dass der Sync selbst nach einem erfolgreichen Dry-Run noch unnötig viel Arbeit/Zustandsspeicherung erzeugt hätte.

WIP-Korrekturen ohne Strukturänderung:
- zwei real belegte Legacy-Bindungen ergänzen;
- Sync-Knotentiefe/Index cachen;
- Sync-Zustand pro begrenztem Verarbeitungsschritt statt pro Knoten speichern;
- keine Fach-, Kategorie-, Navigations- oder Architekturänderung.

## Vollworkflow-Lokalsimulation

Positiv:
- Admin-Aufruf ohne Vollscan;
- Dry-Run 3487 PASS;
- manueller Sync bis COMPLETE;
- Readback 3487/3487;
- Frontend-/Strukturreadback PASS;
- Header-Navigation PASS;
- 381/381 terminale Hobbyseiten mit vollständigen Content-Kategorien PASS;
- ungebundene CORE-Seiten 0;
- zweiter Dry-Run nach COMPLETE: CREATE 0 / ADOPT 0 / UPDATE 0 / UNCHANGED 3487 / ARCHIVE 0.

Negativ:
- fremd gebundener Hummelkästen-Slug -> BLOCKED;
- doppelte alte Hummelkästen-Bindung -> BLOCKED;
- Live-Drift nach gespeichertem Dry-Run -> Fingerprint ändert sich, alter Plan darf nicht angewendet werden;
- injizierter Write-Fehler -> ROLLED_BACK; anschließender Dry-Run wieder identisch zum Ausgangsplan PASS;
- manual-only Bootstrap -> 0 Writes / 0 Schedules / 0 Network.

Performance:
- 1.14.14 alter Dry-Run lokal ~29.8 s;
- 1.14.15 Dry-Run lokal ~1 s;
- WIP-Vollsync nach Sync-Optimierung lokal COMPLETE in wenigen Sekunden über 3487 Ziele;
- Statuspersistenz von tausenden Einzelwrites auf begrenzte Batch-Persistenz reduziert.

## Grenze des Nachweises

Noch kein 1:1-Live-Replay, weil der aktuelle reale 1.14.15-Dry-Run nur als Screenshot vorliegt. Für den wortwörtlichen Replay wird dessen JSON-Export benötigt.

## EXAKT EINE NEXT ACTION

**Kein Plugin installieren. Den aktuellen `Finalen Readback als JSON` herunterladen und bereitstellen. Danach 1:1-Replay gegen genau diesen Live-Plan; erst bei PASS wird überhaupt wieder ein Plugin ausgegeben.**
