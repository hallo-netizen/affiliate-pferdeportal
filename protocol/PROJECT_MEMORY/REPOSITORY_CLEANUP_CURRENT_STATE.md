# CAMPUS – REPOSITORY-/BRANCH-CLEANUP – CURRENT STATE

STATUS: ACTIVE
SCOPE: CAMPUS_REPOSITORY_CLEANUP
STAND: 2026-10-19

## Auftrag

Repository-/Branch-Aufräumung nach dem bestehenden Campusstandard fortführen, ohne Fachsysteme zu verändern.

Harte Grenzen:
- Projektgebäude strikt getrennt halten.
- Pferdeatelier TEXT: ausschließlich K0 aktiv; K1–K9 nur Archiv/Recherche.
- Archiv/Backup niemals Werkbank.
- K0, Affiliate, Plugins, Fachlogik und Produktionssysteme nicht durch Cleanup verändern.
- Main-Legacy nicht löschen, solange der bestehende Hardlock davon abhängt.
- Branches nur nach negativem Nachweis von aktiver Nutzung, PR, Backup/Gold/Fallback, Security/Hardlock und einzigartigen Commits freigeben.

## Aktueller belastbarer Stand

Repository: `hallo-netizen/affiliate-pferdeportal`

Aktive Registry:
- `main`
- `hobbyroom/project-memory-campus-v1-20260905`
- `konzept0-portal-neutral-20261002`
- `affiliate-release-current`

Frisch geprüft vor Abschluss des Audits:
- physische Branches: **496**
- offene PRs: ausschließlich **#518 – Fix ADCELL banner import basis**
- PR-Branch `fix/banner-import-basis-20261006`: geschützt / nicht Teil dieses Cleanup-Auftrags
- geschützte Branches laut GitHub: `main` und `article-production`
- Release-Targets: keiner der Audit-Kandidaten ist als Release-`target_commitish` gebunden
- Delta nach dem 494er Checkpoint: zwei neue Hobby-Branches vom 18.10.2026:
  - `hobbyroom/hd689-updater-artifact-20261018` → gegenüber Campus **6 eigene Commits**
  - `hobbyroom/hd690-detail-rollout-20261018` → gegenüber Campus **10 eigene Commits**
- beide Delta-Branches sind **NO DELETE** und nicht Teil der 58 Löschkandidaten

Branch-Audit-Beleg:
`protocol/PROJECT_MEMORY/ARCHIV/BRANCH_AUDIT_CHECKPOINT_20261017.md`

## Auditstand – vollständig

Ausgangsprüfmenge: **467**

Ancestry-Prüfung:
- geprüft: **467/467**
- `ahead=0`: **91**
- mit mindestens einem eigenen Commit: **376**
- ungeprüft: **0**

Zweite Schutzprüfung der 91 `ahead=0`-Branches:
- aktive Registry geprüft
- alle im `AUTORITAETSPLAN.json` gebundenen Current-Autoritäten geprüft
- offener PR geprüft
- aktiver Branchschutz / Rulesets geprüft
- Release-Bindungen geprüft
- exakte Branchreferenzen im aktuellen Main geprüft

Ergebnis:
- **58** Branches: `LOESCHKANDIDAT_NACH_NEGATIVPRUEFUNG`
- **33** Branches: `NO_DELETE / ROLLE_NICHT_SICHER_AUSGESCHLOSSEN`
- davon `article-production` ausdrücklich durch aktives GitHub-Ruleset geschützt
- Branch-Löschungen in diesem dokumentierten Audit weiterhin: **0**

Die exakten beiden Listen stehen ausschließlich im Auditcheckpoint.

Der frühere Rückgang von 780 auf 494 physische Branches besitzt weiterhin keinen vollständigen eigenen Löschbeleg. Daraus wird keine zusätzliche Löschannahme abgeleitet.

## Genau eine NEXT ACTION

Vor einem echten Löschbatch den physischen Branchbestand und offene PRs noch einmal frisch gegen diesen Stand prüfen.

Wenn unverändert:
die **58 im Auditcheckpoint ausdrücklich freigegebenen Löschkandidaten** als Branch-Refs löschen.

Nicht löschen:
- die **376** Branches mit eigenen Commits;
- die **33** zurückgestellten Schutz-/Rollenfälle;
- `main`, Campus, K0, Affiliate;
- PR #518;
- Main-Hardlock-Legacy.

Der hier verfügbare GitHub-Zugriff unterstützt keine Branch-Ref-Löschung. Deshalb endet dieser Lauf nach vollständiger Prüfung und verbindlicher Kandidatenliste, nicht mit einer vorgetäuschten Löschung.

## Frischecheck

Vor Löschung:
- Branchzahl frisch messen;
- offene PRs frisch lesen;
- `ACTIVE_BRANCHES.json` frisch lesen;
- Auditcheckpoint unverändert prüfen;
- bei unverändertem Stand keine Ancestry-Prüfung wiederholen, sondern nur Delta prüfen.

CAMPUS_SINGLE_TRUTH_CURRENT_V1
