# PFERDE ATELIER – KONZEPT NULL

Vollständig abgeschottete Rekonstruktion des historischen Text-/Artikelworkflows ab dem gebundenen PSERC-Metadaten-Handoff.

## Autorität
- Branch: `hobbyroom/konzept-null-startmaster0102-isolated`
- historische Autorität: STARTMASTER0102, Commit `be89fa13c170700e9753666d1d52bfbd8b28d810`
- zusätzliche Rekonstruktionsquelle: hochgeladener STARTMASTER0039 für die ursprüngliche Chat-Zwangsführung und eingefrorene Workflow-Semantik
- Laufzeitautorität: `PFERDE_ATELIER_START_HERE.json -> CURRENT_STATE.json -> NEXT_ALLOWED_STEP`

## Harte Chat-Führung
Der Chat darf den Workflow nicht selbst wählen. Nach jedem belegten Schritt existiert genau ein `NEXT_ALLOWED_STEP`.
Erinnerung, Chat-Historie, Vermutung oder ein späteres Nachbarsystem sind keine Navigationsquelle.

Gebundene Kette:
`METADATA -> SOURCE_ORDER -> RESEARCH -> SOURCE_SNAPSHOT -> FACT_PACK -> CLAIM_BINDING -> CANONICAL_ARTICLE -> PRODUCTION_PLAN_V4 -> LANGUAGETOOL_6_8 -> PPM_6_7_9 -> LOCAL_TEST_PACKAGE`

Interne PASS-Schritte sind kein Stoppgrund. Fail-closed bei Sprung, fehlender Bindung, falscher Reihenfolge oder Außenwirkung.

## Runtime
- PPM 6.7.9: exakte ZIP-Identität `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`
- PPM-Hauptdatei: `0874f26f21e471007922cf759ea5ad52bdc61a5975931898e83e9ff8f6418906`
- LanguageTool 6.8: exakte ZIP-/JAR-Identität und reale Ausführung im GitHub-Hardtest
- historischer PSERC 0.28.14: erwarteter Hash `a5008fc463c78f919a1dc03a510e681c426d97b5f3785de820169805dab3b988`
- die spätere PSERC-0.28.18-ZIP wurde aus Konzept Null entfernt und wird nicht verwendet

Konzept Null beginnt absichtlich **nach** dem historischen PSERC-0.28.14-Metadaten-Handoff. Deshalb wird PSERC selbst in dieser isolierten Text-Runtime nicht ausgeführt.

## Harte Grenze
Ende zwingend `BEFORE_WORDPRESS`.
Kein WordPress-Zugriff, Publish, Deploy, Merge, PR, main-Write oder Rückschreiben in Produktionszustände.

## Start
```bash
python3 konzept_null/konzept_null_runner.py preflight
python3 konzept_null/konzept_null_runner.py root
python3 konzept_null/konzept_null_runner.py init /pfad/zur/metadaten-batch.json
python3 konzept_null/konzept_null_runner.py next /pfad/zur/RUN_STATE.json
```

Danach ausschließlich den ausgegebenen nächsten Schritt ausführen und das zugehörige Artefakt mit `stage` binden.

## Beweis
GitHub-Hardtest Run **35396990143**: PASS.
Geprüft: Isolation, komplette Schrittfolge, 1/7/25 Artikel, Negativfälle, PPM-Identität und sechs PPM-Normal-Draft-Tests, LanguageTool 6.8 real, falsche spätere PSERC-Abhängigkeit ausgeschlossen.

`RECONSTRUCTION_COMPLETE.json` ist der Abschlussnachweis.
