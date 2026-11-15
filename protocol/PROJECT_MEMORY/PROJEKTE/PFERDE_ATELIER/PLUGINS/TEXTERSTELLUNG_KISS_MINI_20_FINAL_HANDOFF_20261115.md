# MINI 20 Altfreigaben – Kategorie-Checkpoint importiert, finale Quittung vorbereitet (15.11.2026)

Testsite oliver-beil.de; bestehender 0.4.9 KISS HARD RULE Teststand, keine Produktionsfreigabe.

Benutzer meldet, dass das MINI-CATEGORY-Checkpoint-JSON importiert wurde. Das ist die BENUTZERMELDUNG, kein unabhängiger Live-WordPress-Importbeleg.

Ursprünglicher einmal eingefrorener Batch `mini-20261115102911-353bdc69d800`, Source SHA256 `06c8e0e71198386cf76d305e63d0c9d80defbb04568535f6c462734d803fc8a1`, 20 Zeilen, sämtlich `LEGACY_CATEGORY_ONLY`; Originaltitel/Intents/SEO/FREI bereits fest.

Benutzergelieferte/erstellte CATEGORY-Quittung `texterstellung-mini-kategorie-checkpoint-20261115.json` enthält 20 Originalzeilen in unveränderter Reihenfolge; nur route/category_slug/article_type ergänzt. Nach Originalcode ist für LEGACY_CATEGORY_ONLY bei 20 DONE-Category-Quittungen der nächste Status FINAL_IMPORT, keine EDITORIAL/TITLE-Worker erforderlich.

Aus der bestehenden Original-5MB-MINI-Datei und GENAU diesem vorhandenen CATEGORY-Checkpoint wurde einmalig `texterstellung-mini-abschluss-20261115.json` erzeugt. Es enthält alle ursprünglichen Source-Headerfelder (nur das dynamische `resume_checkpoints` entfernt), Original-20-Zeilen + unveränderte Kategorie-Felder, dazu `box=locked_box=FREI`, `intent_summary=locked_intent`, `approved_title=locked_title`. **20/20 Originaltitel und 20/20 Kategoriezuordnungen unverändert, kein SEO-/Titel-/Kategorie-Rerun**. Datei lokal strukturell eingelesen und gegen das originale eingefrorene Feldinventar validiert, 4.198.224 Bytes, SHA256 `17270aaba59409c38699ba4e210882f29cad445ea0d8445033e57a03b4d8df15`.

Original-0.4.9-PHP `seoImport` erwartet genau diesen kompletten, unveränderten Header ohne `resume_checkpoints`, ein Kategorie-Checkpoint `DONE` je LEGACY-Zeile und identische Kategorien. Anschließend versucht es die originale technische K0-Platzbuchung. Ob diese auf echter WP erfolgreich ist, steht AUS. Keine Live-FREI/Slot-Erfolgsaussage vor echtem Test.

**Einziger nächster Nutzerklick:** WordPress → Texterstellung → Redaktionsplan → `Ein fertiges MINI-Ergebnis übernehmen` mit `texterstellung-mini-abschluss-20261115.json`. Die angezeigte Import-Quittung muss 20 frei / 0 gehalten melden; bei technisch fehlenden K0-Slots betroffene Artikel offen, keine zusätzliche Entscheidung. Erst danach zu Texterstellung → K0-Export.

`production_release_allowed=false`.