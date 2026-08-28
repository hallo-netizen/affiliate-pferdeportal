# STARTMASTER0102 – Wiederholungsfehler Kategorie-Identität – Hardlock

Stand: 28.08.2026

## Wiederholter Fehler
Beim 6er-Artikeltest wurde erneut ein Produktionspaket freigegeben, obwohl im `quality_binding.wordpress_category.name` fälschlich der Kategorie-Slug statt des sichtbaren WordPress-Kategorienamens stand.

Live-Fehler: `BLOCKED_NORMAL_DRAFT_CATEGORY_IDENTITY` / `NORMAL_DRAFT_CATEGORY_NAME_SLUG_AND_TAXONOMY_MUST_MATCH`.

Beispiele:
- FALSCH: `name=pferdebuersten-pflege`, `slug=pferdebuersten-pflege`
- RICHTIG: `name=Pflege Pferdebürsten`, `slug=pferdebuersten-pflege`
- FALSCH: `name=rampenmatten-beratung`, `slug=rampenmatten-beratung`
- RICHTIG: `name=Beratung Rampenmatten`, `slug=rampenmatten-beratung`

## Historischer Beleg
Bereits erfolgreiche Produktionspakete verwenden im selben Feld den sichtbaren WordPress-Kategorienamen, z. B. `Beratung Boxenmatten`, `Beratung Futterautomaten`, `Beratung Hafer`, jeweils bei separatem Slug.

## Ab sofort bindender Paket-Hardlock
Vor jeder Produktionspaket-Freigabe muss für JEDES Planitem gelten:
1. `quality_binding.wordpress_category.name` = exakter sichtbarer WordPress-Kategoriename aus der gebundenen Kategoriequelle; niemals aus dem Slug synthetisieren.
2. `quality_binding.wordpress_category.slug` = exakter WordPress-Slug.
3. `taxonomy` = `category`.
4. Der konkrete PPM-6.7.9-Normal-Draft-Kategorie-Identitätspfad ist Bestandteil der Freigabe. Ein vorgelagerter Paket-/Generator-PASS darf NICHT als vollständiger Normal-Draft-PASS bezeichnet werden.
5. Bei Änderung des Kategorie-Bindings müssen `quality_binding_hash`, `workflow_release.items[].quality_evidence_sha256`, Produktionsplan-Hash, signierte Supervisor-Freigabe und Paket-Hashes deterministisch neu gebildet werden.

## Prozessfehler
Die vorherige Aussage „kompletter lokaler Durchlauf PASS“ war falsch, weil der reale `normal_draft_create`-Kategorie-Identitätsgate nicht tatsächlich abgedeckt war. Künftig darf ein Prüfstand nur mit dem Namen des tatsächlich ausgeführten Gates bezeichnet werden; keine Hochstufung zu einem nicht ausgeführten Downstream-PASS.

## Keine Workflowänderung
Keine Fach-, Text-, Qualitäts-, PSTE-, PSERC-, PPM-, LanguageTool- oder Publikationsregel wird verändert. Dies ist ausschließlich eine Präzisierung der bereits vorhandenen Produktionspaket-Bindung und Freigabebezeichnung.