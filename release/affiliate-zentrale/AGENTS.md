# Affiliate-Zentrale – externe Release-Kontrollinstanz

Diese Datei steuert **ausschließlich** den Workstream `AFFILIATE_ZENTRALE` einschließlich eBay.

WICHTIG: Für diesen Workstream gilt **nicht** die STARTMASTER-/`.pferde-capsule`-Eingangstür aus dem Root-Workflow.

## Verbindlicher Start

1. `control/release-governance/CURRENT_RELEASE.json` lesen. Diese Datei ist die einzige maschinenlesbare Entscheidungsinstanz für Ziel, Zustand, Arbeitsbranch und Release-Gates.
2. `python3 control/release-governance/release_guard.py governance-check` ausführen.
3. Auf `affiliate-release-current` zusätzlich `python3 control/release-governance/release_guard.py start --branch "$(git branch --show-current)"` ausführen.
4. Einzige aktuelle Quelle ist `release/affiliate-zentrale/current/affiliate-portal-router/` plus `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`.

## KISS-Ausführungszyklus

Es gibt nur diesen Zyklus:

`GESAMTTEST -> ERSTER_ECHTER_FEHLER -> GENAU_DIESEN_FEHLER_FIXEN -> GESAMTTEST`

Wenn der Gesamttest vollständig PASS ist:

`GESAMTTEST -> RELEASE_CHECK -> RELEASE`

Regeln:
- Maximal **ein** Arbeitsstrang.
- Bei einem FAIL nur den **ersten belegten Fehler** bearbeiten.
- Keine neue Architektur, keine neue Version und keine Nebenuntersuchung, solange derselbe Fehler offen ist.
- Für einen belegten Fehler dürfen ausschließlich die direkt betroffenen Dateien im kanonischen Source-Tree geändert werden.
- Danach Source-Manifest aktualisieren und alle Evidence, deren Source-Manifest-Bindung dadurch veraltet ist, als stale behandeln.
- Anschließend wieder **ein einziger Gesamt-Gate-Zyklus**, nicht elf manuelle Einzelprojekte.
- Bereits hash-identisch gültige PASS-Evidence wird wiederverwendet.

## Release-Gates

Die einzelnen Pflichtgates in `CURRENT_RELEASE.json` bleiben als Nachweis-Matrix bestehen. Sie sind **keine separaten Arbeitsstränge**. Ein Gesamtlauf darf mehrere Gates gleichzeitig schließen.

Pflichtlogik:
1. alter Fehlerzustand belegt FAIL,
2. aktueller Stand belegt denselben Fall PASS,
3. relevante Gegen-/Fehlerzustände fail-closed,
4. Gesamtworkflow/WordPress/MariaDB soweit gebunden,
5. Installer/Fresh-Unpack/Byteidentität/Final-SHA erst am Ende.

## Verbote

- Keine Base64-, GZIP-, Chunk-, Patch-, ZIP- oder Historien-Rekonstruktion der aktuellen Quelle.
- Keine Versions-, Staging-, Probe- oder Nebenbranches für Release-Arbeit.
- Keine STARTMASTER-Navigation.
- Keine Änderung fremder Workstreams.
- Keine Release-ZIP vor dem finalen Gate.

## PASS und Release

Jeder PASS benötigt Evidence unter `release/affiliate-zentrale/evidence/` mit Evidence-SHA und Bindung an den aktuellen Source-Manifest-SHA.

Vor Freigabe muss `python3 control/release-governance/release_guard.py release-check` PASS liefern.

Wenn ein Gate FAIL ist, lautet der Zustand **FIX_FIRST_FAILED_GATE**. Wenn alle Pflichtgates PASS sind, lautet der nächste Schritt **RELEASE_CHECK**.
