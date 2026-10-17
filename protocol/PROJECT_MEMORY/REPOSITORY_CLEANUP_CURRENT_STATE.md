# CAMPUS – REPOSITORY-/BRANCH-CLEANUP – CURRENT STATE

STATUS: ACTIVE
SCOPE: CAMPUS_REPOSITORY_CLEANUP
STAND: 2026-10-17

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

Frisch verifizierter physischer Bestand:
- Branches: **494**
- `archive/*`: **21**
- `backup/*`: **1**
- offene PRs: ausschließlich **#518 – Fix ADCELL banner import basis**
- PR-Branch `fix/banner-import-basis-20261006`: geschützt / nicht Teil dieses Cleanup-Auftrags

Branch-Audit-Beleg:
`protocol/PROJECT_MEMORY/ARCHIV/BRANCH_AUDIT_CHECKPOINT_20261017.md`

Auditstand:
- Ausgangsprüfmenge: **467**
- bereits geprüft: **291**
- davon `ahead=0`: **47**
- davon mit mindestens einem eigenen Commit: **244**
- noch ungeprüft: **176**
- Branch-Löschungen im dokumentierten Audit: **0**

Der frühere Rückgang von 780 auf 494 physische Branches besitzt keinen vollständigen eigenen Löschbeleg. Daraus darf keine zusätzliche Löschannahme abgeleitet werden.

## Erster offener Punkt

Kein Architekturblocker mehr: BAU-043 ist durch diese eine Current-Autorität und den Scope `CAMPUS_REPOSITORY_CLEANUP` behoben.

Operativ offen:
1. die exakt 176 Branches aus dem Auditcheckpoint ancestry-prüfen;
2. die 47 vorhandenen `ahead=0`-Treffer zusätzlich auf Referenzen/Rollen prüfen;
3. erst nach vollständigem Negativnachweis echte Löschkandidaten markieren;
4. Main-Hardlock-Legacy separat geschützt lassen.

## Genau eine NEXT ACTION

Die **176 ungeprüften Branches** aus
`protocol/PROJECT_MEMORY/ARCHIV/BRANCH_AUDIT_CHECKPOINT_20261017.md`
in der dort gespeicherten Reihenfolge gegen die fachlich passende aktive Linie prüfen.

Erster Branch:
`docs/concept-agent-closeout-pr413-20260925`

Regel:
`ahead=0` ist nur der erste Filter und niemals allein eine Löschfreigabe.

## Frischecheck

Vor einem späteren Löschbatch:
- physischen Branchbestand und offene PRs frisch prüfen;
- aktive Registry frisch lesen;
- bei unverändertem Auditcheckpoint die bereits geprüften 291 Branches **nicht** neu rekonstruieren;
- nur das Delta seit diesem Current-Stand prüfen.

CAMPUS_SINGLE_TRUTH_CURRENT_V1
