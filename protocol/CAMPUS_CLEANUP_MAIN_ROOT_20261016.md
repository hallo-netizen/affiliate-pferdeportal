# Campus cleanup – main root – 2026-10-16

Rolle: Aufräumbeleg, keine Current- oder Fachautorität.

Vorbedingungen:
- lokales vollständiges GitHub-Backup durch Nutzer bestätigt;
- Git-Snapshot `archive/campus-pre-cleanup-20261016` bindet den vollständigen main-Vorstand;
- K0, aktive Workflows, Controls, Pluginquellen und Fachlogik bleiben unangetastet.

Entfernt:
- 27 unreferenzierte historische Root-Artefakte;
- 9 bereits zuvor als Repository-Löschkandidaten isolierte ZIPs plus deren README.

Prüfung:
- exakte Dateinamen gegen aktuellen main-Code gesucht: 0 aktive Referenzen für die entfernten Root-Artefakte;
- 9 Löschkandidaten: 0 aktive Referenzen;
- keine Datei unter `.github/workflows/**`, `control/**`, `release/**`, `affiliate-portal-router/**` oder `K0_START_HERE.md` verändert;
- Wiederherstellung jederzeit aus lokalem Backup oder Archiv-Snapshot möglich.

Ziel: aktive Oberfläche verkleinern, historische Suchtreffer reduzieren, keine Produktionsänderung.


## Phase 3 – aktive Oberfläche weiter bereinigt

Zusätzlich aus aktivem main entfernt und ausschließlich über Archiv-Snapshots/Backup erhalten:
- 5 unreferenzierte historische Protokoll-/Governance-Dateien;
- kompletter Ordner `isolated_system4a/` (nur historische Nachweise, keine aktive Referenz);
- kompletter Ordner `recovery/current16-input/` (16 historische Recovery-Artikel, keine aktive Referenz);
- kompletter `control/startmaster0103/`-Stand (keine aktive Pfadreferenz).

Bewusst NICHT entfernt:
- `isolated_system4/`, weil aktuelle Required-Check-/Hardlock-Regeln diesen Pfad noch explizit schützen;
- `control/startmaster0104/` bis `0106/`, weil der aktive Hardlock-Workflow sie noch referenziert;
- K8-Dateien und die zwei noch von `control/startmaster0107/CURRENT_STATE.json` referenzierten K7/REAL7-Protokolle;
- aktuelle K0-, Affiliate-, Release-, Workflow- und Pluginquellen.

Sicherungsanker:
- lokales Nutzerbackup vor Bereinigung;
- `archive/campus-pre-cleanup-20261016`;
- `archive/campus-main-pre-phase3-20261016`.

Hardlock-Nachprüfung Phase 3: erforderlicher PROJECT_MEMORY-Protokollcheck ist im PR gebunden.
