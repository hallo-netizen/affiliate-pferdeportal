# MASTER016-R7 – Finaler harter Endvertrag / GitHub-Sicherung

Datum: 2026-08-21
Branch: `category-master016-r7-finite-correction-contract-20260821`
Basis: `category-master016-r5-specialization-coverage-20260821`
`main`: unverändert, kein Merge.

## Bindender Stand
- MASTER-Revision: `016-R7`
- Plugin: `affiliate-portal-kategorie-workflow` V1.7.2
- Aktive normative Dateien: 13/13 PASS
- Aktive Regeln: 145/145 ACTIVE
- Workflow: 14/14
- Stage 12: `PASS_READ_ONLY_TOTAL_AUDIT`
- Stage 13: `PENDING_HUMAN_VISIBLE_REVIEW`
- Stage-13-Review-Scope: `da9d3989c15b67daf507a9f5b1d1f073f86901bae1064731b7be39f906853757`
- `FINAL_APPROVED`: nein
- `APKW_CONTENT_WRITE_CAPABILITY=false`

## Realer Gaumen-Stand
- finaler Research: 138/138
- aktive Content-Kategorien: 121
- Spezialisierungsabdeckung: 121/121
- weitere Paid Calls: 0
- Validator: PASS
- Research-Evidence: PASS
- Comparator: PASS_READ_ONLY_PREVIEW
- Blocker: 0
- sichtbare Roh-Longtails/Providerphrasen in Stage 13: 0

## Produktionsdelta R7
1. `affiliate-portal-kategorie-workflow.php`
2. `includes/class-apkw-admin.php`
3. `includes/class-apkw-research-evidence.php`
4. `includes/class-apkw-research.php`
5. `includes/class-apkw-validator.php`
6. `schema-category-v1.4.json`
7. `schema-research-v1.4.json`
8. `docs/FINITE_CORRECTION_ROOTFIX.md`

R7 korrigiert ausschließlich die endliche Stage10→Stage11-Bindung: gleiche `concept_id` + gleicher `research_cluster_id` behalten den unveränderlichen Stage-10-Research-Anker; Stage-11-Primärkeywordkorrekturen lösen keine rekursive Paid-Schleife aus. Alle exakten Suggestions bleiben verlustfrei Research-Evidenz, aber nur explizit promovierte Strukturkandidaten brauchen eine Kategorieentscheidung.

## Harte Prüfungen
- Active/Master Source: 183/183 PASS
- finaler Fresh-MASTER Source: 183/183 PASS
- aus finalem Fresh-MASTER entpacktes Source-ZIP: 183/183 PASS
- aus finalem Fresh-MASTER entpackter Installer: 183/183 PASS
- Source-Manifest je Kopie: 46/46 PASS
- PHP-Lint: 10/10 PASS
- JSON: 14/14 PASS
- verbotene Portal-Write-APIs: 0 Treffer
- DataForSEO-Endpunkte: exakt 4 erlaubte Endpunkte
- Version Header/Runtime: 1.7.2 / 1.7.2 PASS
- Source ↔ Installer ↔ MASTER: 0 Diff
- vollständiges MASTER-Manifest nach finalem Fresh-Unpack: 653/653 PASS
- finaler MASTER-Fresh-Unpack: vollständiger Baum 0 Diff

## Artefakte / SHA-256
- `AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.7.2_MASTER016_R7_FINITE_CORRECTION_ROOTFIX.zip`
  - `789e760ced34223132cf5456967f7775704908f51f98f3b5d626e86677aa2d19`
- `QUELLCODE_KATEGORIE_WORKFLOW_V1.7.2_MASTER016_R7_FINITE_CORRECTION_ROOTFIX.zip`
  - `374e1a8fcda02db0a1343fa1ebf6d84affcf81273c8bae32c21d137f7c316da1`
- `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R7_WORKFLOW_HARDLOCK.zip`
  - `5cd3b569a635477ccab596a4384e0dbc9662b57cc2182aeb12a696cdf7ed749b`

## Abgrenzung
Der technische/read-only Endvertrag ist PASS. Eine menschliche Stage-13-Sichtfreigabe wird ausdrücklich nicht simuliert. Erst nach dieser Freigabe darf Stage 14 `FINAL_APPROVED` validieren; erst danach ist der separate Post-FINAL-WordPress-Import zulässig.
