# STARTMASTER0107 – Pre-Codex ready 2026-09-19

## Ergebnis

Der Stand ist bis direkt vor einen neuen realen Codex-Lauf vorbereitet. Codex wurde auf ausdrückliche Nutzeranweisung **nicht gestartet**.

## Belegte technische Basis

- Main: `a0cb23a1611202fd75395a785385962ce7ae1900`
- PR #339 hardlock: Run `35398343067` PASS
- PR #339 hardlock-base: Run `35398339671` PASS
- Post-Merge System4A Acceptance: Run `35398621624` PASS
- Permanenter Dispatcher PR #107 Head: `a0cb23a1611202fd75395a785385962ce7ae1900`
- Dispatcher-Basis nachgezogen auf den bereits akzeptierten Main vor PR #339: `4a8d91185d9cd58c3d425ed23c5c0daddc603e9a`
- Frischer PR107 hardlock-base: Run `35427592803` PASS

Die Basis wurde nachgezogen, damit hardlock-base nicht die gesamte historische Differenz seit dem 4. September erneut als aktuelle Änderung bewertet. Der Schutz selbst und seine Regeln wurden nicht verändert oder gelockert.

## Batch-Werkstatt

PR #339 ist gemergt. `BATCH_TEMPLATE_REUSE_BLOCKED` bleibt bei unveränderter 20-%-Grenze. Ein reparierbarer Befund geht auf denselben Artikel/denselben Workspace zurück; Revision und Draft-Hash müssen sich ändern, danach wird der Batch erneut geprüft.

## Noch real mit Codex zu beweisen

1. frischer realer 1-Artikel-Lauf mit dauerhaften Artikelbytes und LT 6.8 / PPM 6.7.9;
2. separater echter PPM-Qualitäts-Negativtest;
3. frischer realer 3-Artikel-Lauf mit dauerhaften Dateien und realem Batch-Repair, falls nötig;
4. isolierte 107008-Grenze muss weiterhin fail-closed bleiben;
5. kein Produktions-7er und kein Publish.

## Exakter Stop

`USER_EXPLICITLY_FORBIDS_CODEX_START_CURRENT_TURN`

Nächster Schritt erst nach einer neuen ausdrücklichen Nutzerfreigabe: Main und PR #107 frisch auf Gleichheit prüfen, Pflichtchecks grün bestätigen und dann den realen Codex-Acceptance-Lauf starten.
