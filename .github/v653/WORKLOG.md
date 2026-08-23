# ARBEITSPROTOKOLL V6.53.0 – Artikel-Produktvorschläge Portalstandard

Stand: 23.08.2026

## Auftrag

Produktvorschläge unter Einzelbeiträgen ausschließlich im Affiliate-Plugin vollständig an den Portalstandard anpassen. Designplugin nicht verändern. Vorhandene `.ppar-article-product-*`-Logik prüfen und Ursache in Markup/CSS beheben. Kein Minifix.

## Nachgewiesene Ursache

Beide Artikel-Produktpfade (`render_article_product_block()` und `article_plan_render_products()`) haben Produktkampagnen über den generischen `render_banner()`-Renderer ausgegeben. Dadurch enthielten die Produktkarten `.ppar-banner-*`-Markup und erbten globale Banner-Geometrie sowie globale Hover-Unterstreichungen. Die vorhandene `.ppar-article-product-card`-CSS versuchte diese Fremdstruktur nur nachträglich zu überschreiben. Das war die Ursache für den im Live-Screenshot sichtbaren FAIL.

## Rootfix

Ein eigener `article_plan_render_product_card_markup()`-Renderer wurde in die vorhandene Article-Plan-Trait eingeführt. Beide Artikel-Produktpfade verwenden ausschließlich diesen Renderer. Produktkarten besitzen eigenes `.ppar-article-product-*`-Markup. Die artikelbezogene CSS hängt nicht mehr an `.ppar-banner-*`-Klassen.

Portalstandard im Produktmodul:
- weiße Karten, ruhiger heller Rahmen;
- Ocker `#C89214` als Überschrift-/Hover-Akzent;
- Dunkeloliv `#35422A` als Standard-CTA;
- keine Unterstreichungen in der gesamten Karte;
- gesamte Karte verlinkt;
- nicht verzerrende Produktbilder mit `object-fit: contain` in definierter Bildfläche;
- kompakter Textbereich mit begrenzter Titel-/Beschreibungshöhe;
- 3/2/1 responsive Spalten;
- ein Einzelprodukt bleibt kompakt statt über die volle Inhaltsbreite zu laufen.

## Schutz vor Seiteneffekten

Produktionsscope V6.52 -> V6.53: exakt vier Dateien im Affiliate-Plugin:
1. `assets/frontend.css`
2. `includes/trait-ppar-article-plans.php`
3. `pferdeportal-affiliate-router.php`
4. `readme.txt`

Das Designplugin ist nicht Bestandteil des Scopes. PRIVATE/BUSINESS/Provider/Safety/Quality/Routing werden nicht verändert. Der eBay-Runtime-Build bleibt absichtlich exakt `6.52.0-core-cron-selfpump-rootfix-20260822`, damit dieser reine Design-/Markup-Release keinen bestehenden eBay-Run migriert oder beendet.

## Prüfstrategie

1. V6.52 bindenden Vorgänger und vollständigen automatischen Releaseworkflow erneut von null ausführen.
2. Neuer Produktvertrag gegen V6.52 muss reproduzierbar RED sein.
3. Rootfix als ein atomarer Produktionsschritt anwenden.
4. Vollständige modifizierte Source-Prüfung: PHP/JSON, neue Architektur-/Markup-Tests, vorhandene Successor-/Workflowtests.
5. Real WordPress 7.0.1 + PHP 8.4 + MariaDB 11.4 inkl. A-H/Concurrency/Stale/CAS/Checkpoint auf dem modifizierten Source-Stand.
6. Installer bauen, Fresh-Unpack-Parität beweisen und dieselben Source-/Workflowtests erneut ausführen.
7. Real WordPress 7.0.1 erneut aus der finalen Installer-ZIP prüfen.
8. WordPress 6.8.3 Produkt-Renderer real prüfen.
9. MASTER bauen, Manifest und Source↔Installer↔MASTER-Parität prüfen.
10. Erst dann automatisches `FINAL_RELEASE_GATE=PASS`.

Kein manueller PASS ersetzt diese Pipeline.
