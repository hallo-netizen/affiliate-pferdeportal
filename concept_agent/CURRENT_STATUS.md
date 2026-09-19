# CONCEPT AGENT — CURRENT STATUS

Status: FIRST_REAL_CHECKER_TESTRUN_PASS

## Erster echter Testlauf erreicht
Artikel:
`Das Wichtigste über Hindernisstangen für Pferde`

Frischer Testkandidat:
`87acfa973423d20678509f3f3d49e90613d4c34266a9ddd27055dc71b9a43b13`

### Echte Prüfer
LanguageTool 6.8:
- 0 Findings
- PASS
- JAR SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`

PPM 6.7.9:
- TECHNICAL_CHECK_OK
- CONTENT_QUALITY_CHECK_OK
- fail_closed_aggregate_status PASS
- PASS
- Package SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

### Negativ- und Reparaturprobe
- Tippfehler `Stangenarbiet` -> LanguageTool BLOCK / GERMAN_SPELLER_RULE
- Tabelle entfernt -> PPM BLOCK
- gebundenen internen Link durch externen Link ersetzt -> PPM BLOCK
- Reparatur auf frischen Kandidaten -> LanguageTool PASS + PPM PASS

### Reale interne Links
1. `/training/`
2. `/training/training-reitplatz-training/`
3. `/training/training-reitplatz-training/hindernisstangen/`

## Harte Grenzen
- kein Codex
- kein Merge
- kein Publish
- kein WordPress-Write
- keine Änderung anderer Konzepte

## Nachweis
`concept_agent/FIRST_REAL_CHECKER_RUN_V1.json`
`concept_agent/test_output/FIRST_REAL_CHECKER_CANDIDATE.html`
