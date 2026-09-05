# STARTMASTER0107 – VERBINDLICHER ZIELVERTRAG – 05.09.2026

## Endziel

Exakt den bestehenden Generation-1-7er-Batch vollständig über den bestehenden Produktionsweg bis
`107008 – FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH` führen.

Kein Auto-Publish. Veröffentlichung ausschließlich nach ausdrücklicher Nutzerfreigabe.

## Kanonischer Ablauf

1. SEO-Maschine liefert exakt fünf Metadatenfelder:
   `title`, `target_keyword`, `category`, `article_type`, `plan_slot`.
2. Danach bestehende Textmaschine / bestehender Fachworkflow.
3. Current Codex ist der gebundene ausführende Fachworkflow-Worker.
4. Reale Recherche / Fact-Pack / Artikel / Nicht-PPM-Stage-Artefakte entstehen im bestehenden Fachworkflow.
5. Echter PPM 6.7.9 wird real ausgeführt.
6. PPM `content_hash` muss exakt SHA-256 des finalen Artikels entsprechen.
7. Erst nach echtem PPM dürfen finaler `FACHWORKFLOW_PASS` und finales `ITEM_RECEIPT` entstehen.
8. Bestehende Single-Door-Submission.
9. Nach 7/7 → 107008 Final Review.
10. Halt vor Nutzer-Publish.

## Harte Nicht-Ziele

- keine Änderung der SEO-Maschine;
- keine Erweiterung des 5-Felder-Handoffs;
- keine WordPress-ID als sechstes Feld;
- keine Änderung der Textmaschine;
- keine neue Fachworkflow-Architektur;
- kein neuer Executor / Runner / Gate / Contract / Parallelweg;
- keine Recovery-/Altartikel als Produktionsquelle;
- keine Lockerung von Link-/Tabellen-/LanguageTool-/PPM-/PSERC-/PSTE-/SEO-/Designregeln;
- kein Signer/Private Key im Codex-Worker;
- keine WordPress-Schreibaktion im Test;
- kein Auto-Publish.

## Testvertrag

Ein Test darf nur das behaupten, was er tatsächlich ausgeführt hat.

- Unit-/Regression-PASS ≠ Live-PASS.
- M01–M33-PASS ≠ 7/7-PASS.
- PPM-Prinzip-PASS ≠ Gesamtworkflow-PASS.
- `GESAMT PASS` für die Produktion nur nach echtem 7/7 + 107008 auf demselben produktiven Stand.

## Änderungsregel

Jede technische Kontrollschicht darf den dokumentierten Fachablauf nur kontrollieren, nicht seine Eingaben, Verantwortlichkeiten oder Reihenfolge neu definieren.