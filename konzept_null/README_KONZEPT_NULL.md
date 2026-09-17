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
- Batchgröße: beliebig `1..N`

## Harte Grenze
KONZEPT NULL endet zwingend `BEFORE_WORDPRESS`.
Es gibt keine Berechtigung für WordPress-Zugriff, Publish, Deploy, Merge, PR, main-Write oder Rückschreiben in Produktionszustände.

## Start
```bash
python3 konzept_null/konzept_null_runner.py preflight
python3 konzept_null/konzept_null_runner.py init /pfad/zur/metadaten-batch.json
```

Die Eingabedatei darf jede Batchgröße ab 1 Artikel enthalten. Jeder Artikel muss diese Metadatenfelder besitzen:
`title`, `target_keyword`, `category`, `article_type`, `plan_slot`.

Danach werden ausschließlich in dieser Reihenfolge lokale Batch-Artefakte angenommen:
`RESEARCH -> FACT_PACK -> TEXTMASCHINE -> LANGUAGETOOL_6_8 -> PPM_6_7_9 -> LOCAL_TEST_PACKAGE`.

Alle Artikel eines gestarteten Laufs bleiben während dieses Laufs als ein gebundener Batch zusammen. Titel, Keywords, Kategorien, Artikeltypen und Planslots dürfen innerhalb des Laufs nicht geändert werden.

`INPUT_7_ARTIKEL.json` ist nur ein vorhandenes Testbeispiel für einen 7er-Lauf und besitzt keinerlei Sonderstatus oder feste Systembindung.

Jeder Reihenfolgefehler, falsche Branch, leere Batch, doppelter Planslot, fehlende Metadatenbindung oder geöffnete Außenwirkung führt fail-closed zu `KONZEPT_NULL_BLOCKED:*`.

## Selbsttests
```bash
cd konzept_null
python3 -m unittest -v test_konzept_null_runner.py
```

Die Tests decken mindestens Batchgrößen 1, 7 und 25 sowie Negativfälle ab. Erst nach `KONZEPT_NULL_PREFLIGHT_PASS` darf ein Testlauf beginnen.
