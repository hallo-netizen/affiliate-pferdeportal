# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-01
STATUS: V1.9.4 LIVE DEPLOY + READBACK PASS / PRODUKTIVER BUCHBINDEN-BESTAND STEHT / NICHT ZURÜCKROLLEN

## Harte Abnahmeregel

**Keine Abnahme ohne dokumentierte lokale Positiv- UND Negativsimulation.**

## Live-Abnahme

Installiert:
`Affiliate-Portal Kategorie-Workflow V1.9.4`

Der produktive Buchbinden-Pilot wurde nach dem lokal hart getesteten Term-Name-Readback-Fix erneut ausgeführt.

Live sichtbarer Endzustand:
- `Deployment abgeschlossen`
- `✓ Schreiben und Readback erfolgreich.`

Damit ist der produktive 7-Knoten-Buchbinden-Stand live vorhanden und readback-verifiziert.

**Nicht zurückrollen.**
**Arbeitsstand nicht zurücksetzen.**

## Root Cause des vorherigen Fehlers

V1.9.3 diagnostizierte:
`node:hdc-21557545f2e7cc51 | Feld: name`

Knoten:
`Techniken & Praxis`

WordPress speichert den Taxonomie-Namen intern escaped als
`Techniken &amp; Praxis`.

V1.9.4 normalisiert ausschließlich dieses WordPress-Core-Escaping beim Readback.

## Lokale Beweise V1.9.4

- alter Code reproduziert den Livefehler wortgleich;
- echter 7-CREATE-Buchbinden-Pfad PASS;
- echte falsche Namen / doppelte Kodierung / falscher Slug / Parent / Meta bleiben BLOCKED;
- Source 251/251 PASS;
- Fresh Installer 251/251 PASS;
- PHP Source 25/25;
- PHP Installer 17/17;
- Runtime-Parität 22/22.

Installer SHA:
`85990b87f0ef35530b616df7716547cb20974d1c77ca21aa7b3e0edec723f249`

## NEXT ACTION

HD-001 bleibt unverändert live stehen.

Nächster Arbeitsbereich ist HD-002:
produktiven Owner-Handoff read-only übernehmen → Website-Gesamtbestand erfassen.
