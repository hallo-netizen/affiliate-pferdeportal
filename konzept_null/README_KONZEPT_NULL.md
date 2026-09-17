# PFERDE ATELIER – KONZEPT NULL

Abgeschottete Test-Runtime für den historischen STARTMASTER0102-Workflow.

## Bindung
- Branch: `hobbyroom/konzept-null-startmaster0102-isolated`
- historische Autorität: `be89fa13c170700e9753666d1d52bfbd8b28d810`
- historischer Prompt: `protocol/STARTMASTER0102_ARTICLE_TEST_NO_STOP_HANDOFF_20260828.md`
- PSTE 0.56.25
- PSERC 0.28.14
- PPM 6.7.9
- LanguageTool 6.8

## Harte Grenze
KONZEPT NULL endet zwingend `BEFORE_WORDPRESS`.
Es gibt keine Berechtigung für WordPress-Zugriff, Publish, Deploy, Merge, PR, main-Write oder Rückschreiben in Produktionszustände.

## Start
```bash
python3 konzept_null/konzept_null_runner.py preflight
python3 konzept_null/konzept_null_runner.py init /pfad/zur/ein-artikel-metadaten.json
```

Die Eingabedatei muss exakt einen Artikel mit diesen Feldern enthalten:
`title`, `target_keyword`, `category`, `article_type`, `plan_slot`.

Danach werden ausschließlich in dieser Reihenfolge lokale Artefakte angenommen:
`RESEARCH -> FACT_PACK -> TEXTMASCHINE -> LANGUAGETOOL_6_8 -> PPM_6_7_9 -> LOCAL_TEST_PACKAGE`.

Jeder Reihenfolgefehler, falsche Branch, fehlende Bindung oder geöffnete Außenwirkung führt fail-closed zu `KONZEPT_NULL_BLOCKED:*`.

## Selbsttests
```bash
cd konzept_null
python3 -m unittest -v test_konzept_null_runner.py
```

Erst nach `KONZEPT_NULL_PREFLIGHT_PASS` darf ein Testlauf beginnen.
