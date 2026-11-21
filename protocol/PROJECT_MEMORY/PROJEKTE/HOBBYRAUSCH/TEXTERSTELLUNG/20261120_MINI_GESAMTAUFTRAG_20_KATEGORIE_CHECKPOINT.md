# Hobbydepot MINI-Gesamtauftrag, echter Eingang 20.11.2026

**Quelle:** Nutzerdatei `texterstellung-mini-gesamtauftrag.json`, Vertrag `TEXTERSTELLUNG_SINGLE_EDITOR_BATCH_V1`, batch_id `mini-20261120094038-87239ec1a38a`, 20 erhaltene `items`, alle bereits mit ursprünglicher portal-JA-Entscheidung. Die Quelle hat 3520 WordPress-Kategorien und 802 Inventareinträge; `resume_checkpoints[].next` ist bei allen 20 `CATEGORY`.

**Verbindlicher Workflow:** Original-MINI CATEGORY → Rückgabe über Original `txe_seo_import` → erneuter Download desselben Batch → EDITORIAL → Originalimport → TITLE → Originalimport → FINAL. Jede Station muss vor der nächsten in WordPress gespeichert sein. Keine stillschweigende REDAKTION/TITLE Entscheidung vor CATEGORY-Upload. Keine neue DataForSEO-Anfrage.

**Erstellte CATEGORY-Rückgabe:** `Hobbydepot_MINI_CATEGORY_Checkpoint_20261120.json` mit unverändertem `batch_id`, `source_sha256` und allen 20 identischen Ursprungsfeldern, plus exakt den drei CATEGORY-Feldern `route`, `category_slug`, `article_type`. Drei FACH-Einträge:
1. `Ist Bogenschießen ein teures Hobby?` → `bogenschiessen-faq`, `FAQ`
2. `3d bogenschießen regeln` → `3d-bogenschiessen-faq`, `FAQ`
3. `3d-bogenschießen parcours` → `3d-bogenschiessen-faq`, `FAQ`.

Diese Kategorien sind tatsächlich in der mitgelieferten WordPress-Taxonomie mit `PRODUCTION_LEAF` verzeichnet. 17 weitere Keywordzeilen gehen an den ursprünglichen `REDAKTIONSBUERO`-Weg (leer: category_slug, article_type), da sie Marken-/Medien-/Navigationsbegriffe oder nicht eindeutig vorhandene Produktionskategorien betreffen. Das revidiert **nicht** die eingefrorene portal-JA-Entscheidung; es ist die einzige CATEGORY-Zuordnung.

**Lokaler Original-PHP-Test:** Mit installiertem `0.4.24.14`-Code `TXE_Workshop::seoImport` und isoliert nachgebildetem WordPress-Optionsspeicher/Taxonomie **12/12 Assertions PASS**: 20/20 Kategorie-Quittungen gespeichert, Ursprungsfelder unverändert, Quellenbeleg gleich, Idempotenz, manipuliertes Keyword geblockt, falsche source_sha256 als Batch geblockt, ungültiger Slug nur für betroffenen Datensatz geblockt, nicht unterstützte Artikelart geblockt; andere Datensätze bleiben erfolgreich. Keine Live-WP-Änderungen.

**Nächster Nutzer-Klick:** WordPress → Texterstellung → Redaktionsplan → `Ein fertiges MINI-Ergebnis übernehmen` → `Hobbydepot_MINI_CATEGORY_Checkpoint_20261120.json` hochladen. Danach `MINI-Gesamtauftrag herunterladen` erneut und den Resume-Export in den Chat. Kein neues Plugin nötig, keine kostenpflichtige Suche.

**Nicht nachgewiesen:** Live-Übernahme dieser CATEGORY-Rückgabe, EDITORIAL/TITLE-Entscheidungen, echte K0-Artikelproduktion. Keine vollständige K0-Freigabe.
