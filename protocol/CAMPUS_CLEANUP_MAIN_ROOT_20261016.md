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
