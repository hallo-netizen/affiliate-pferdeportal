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


## Phase 4 – K0 aktive Oberfläche entschlackt

Aus aktivem main entfernt, im Archiv-Snapshot vollständig erhalten:
- sieben alte K0-Test-/Hardlock-/Rendering-Protokolle vom 03.10.2026;
- ein unreferenzierter alter DS24-Evidence-Nachweis.

Bewusst erhalten:
- `K0_START_HERE.md` als aktiver Router;
- `protocol/K0_MAIN_ROUTER_20261003.md` als knapper Navigationsbeleg;
- der komplette produktive K0-Stand auf `konzept0-portal-neutral-20261002`.

Sicherungsanker zusätzlich:
- `archive/campus-main-pre-phase4-20261016`.
