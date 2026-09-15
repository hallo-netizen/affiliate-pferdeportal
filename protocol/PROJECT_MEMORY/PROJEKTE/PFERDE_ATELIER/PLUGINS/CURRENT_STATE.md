# PFERDE-ATELIER – PLUGINS – CURRENT_STATE

STAND: 2026-09-15
STATUS: BLOCKED / DESIGN-PLUGIN-INCIDENT AKTIV

## Belastbarer Stand

Physischer Plugin-Schrank:
`/Campus-Plugins/PFERDE_ATELIER/`

Real als isolierte `CURRENT.zip` synchronisiert und readback-geprüft:
- PPA-001 Affiliate-Zentrale 6.72.19
- PPA-003 Bildzentrale 2.6.9
- PPA-004 Universal Research & Fill 1.9.9
- PPA-005 Portal SEO Topic Engine 0.56.25
- PPA-007 Pferde Atelier HivePress Anzeigensuche 2.1.5
- PPA-011 Pferde Atelier – Pferderassen Manager 0.2.7

Für diese sechs gilt weiterhin nur der jeweils fachlich belegte Status aus den autoritativen Fachquellen.

## AKTIVER BLOCKER PPA-002

PPA-002 Pferde Atelier Design ist **BLOCKED**.

Aktuelle Fachautorität:
`../DESIGN/CURRENT_STATE.md` + `../DESIGN/FEHLERQUELLEN.md`.

- 1.50.529: realer LIVE-FAIL laut Nutzer;
- 1.50.530: nur Fixkandidat, nicht abgenommen;
- real installierte WordPress-Version: noch frisch zu bestimmen;
- Universal Design 2.2.42: mögliche Interaktion ungeklärt.

**Kein Designkandidat aus diesem Fehlerzug darf als `CURRENT.zip` synchronisiert werden.**

Updatevorgang: `PU-20260915-002`.

## Weitere offene Einträge

- PPA-006 Portal SEO Editorial Plan Compiler: Versionsbindung offen.
- PPA-008 Universal Product Comparison 0.8.0-prototype: aktuelle ZIP nicht erreichbar.
- PPA-009 Universal Product Knowledge: exakte aktuelle Installer-ZIP + Hash nicht CURRENT-gebunden.

## NEXT ACTION

Vorrangig `PU-20260915-002` schließen: reale Design-Plugin-Kombination bestimmen, Fehler reproduzieren, positiv/negativ gemeinsam testen, minimal reparieren und LIVE readbacken. Erst danach PPA-002-Artefaktsync.

## Nicht anfassen

- keine fehlerhaften oder nur lokal behaupteten Designkandidaten als CURRENT setzen;
- keine Pluginversion aus Erinnerung ableiten;
- keine Fach-/LIVE-Wahrheit in dieses Inventarbüro verlagern;
- keine Secrets.
