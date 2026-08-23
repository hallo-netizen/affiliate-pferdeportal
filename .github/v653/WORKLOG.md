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

## Release-Gate-Härtung während V6.53

### Lauf 1

Der erste V6.53-CI-Lauf wurde korrekt BLOCKED, weil die neue Prüfinfrastruktur einen falschen Blob-Hash für den bindenden V6.52-Runner erwartete. Es wurde ausschließlich die Prüfinfrastruktur korrigiert; Produktionscode blieb unverändert.

### Lauf 3/5 – nachgewiesener zweiter Infrastrukturfehler

Der V6.52-Vorgängerworkflow wurde im V6.53-Gate erneut ausgeführt und erzeugte einen inhaltlich neu gepackten V6.52-Installer. Anschließend verlangte der V6.53-Runner trotzdem den historischen Byte-SHA des bereits am 23.08.2026 verifizierten Release-Archivs. Dieser Ansatz ist als Bindungsprüfung ungeeignet: der historische Release-Beleg muss als unveränderliches Artefakt geprüft werden, nicht durch Neuerzeugung und Vergleich des ZIP-Containers ersetzt werden. Der Gate-Lauf stoppte korrekt und erzeugte kein V6.53-Release.

Korrektur der Prüfinfrastruktur: V6.53 bindet ab Runner v4 direkt an das unveränderliche, bereits automatisch verifizierte GitHub-Actions-Artefakt V6.52 `9489291638`. Geprüft werden:
- äußerer Artifact-SHA-256 `1a691c0ef5930a462e7ac8176e051c30b219066e9f14dfab4a91440a2391389b`;
- V6.52-Installer-SHA-256 `e8090b31c853031bbc65492845672d5e2ab1268452ac7c944e3459873a7684b2`;
- V6.52-MASTER-SHA-256 `517b0939fe042ace8ab093efc86f754d340c80cb5ba543ff10d61b087fbc7778`;
- `FINAL_RELEASE_GATE=PASS` aus dem originalen Release-Evidence;
- `EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED` bleibt ausdrücklich erhalten.

Damit wird die bindende MASTER tatsächlich bytegenau als Ausgangspunkt verwendet. Danach läuft der vollständige V6.53-Successor-/Real-WordPress-/Fresh-Unpack-/Paritätsworkflow gegen den geänderten Source-Stand und erneut gegen den finalen Installer.

## Prüfstrategie

1. Bindende V6.52-Freigabe als unveränderliches verifiziertes GitHub-Artefakt inklusive Artifact-, Installer-, MASTER-Hash und originalem `FINAL_RELEASE_GATE=PASS` prüfen.
2. Neuer Produktvertrag gegen genau diese V6.52-MASTER reproduzierbar RED.
3. Rootfix als ein atomarer Produktionsschritt anwenden.
4. Vollständige modifizierte Source-Prüfung: PHP/JSON, neue Architektur-/Markup-Tests, vorhandene Successor-/Workflowtests.
5. Real WordPress 7.0.1 + PHP 8.4 + MariaDB 11.4 inkl. A-H/Concurrency/Stale/CAS/Checkpoint auf dem modifizierten Source-Stand.
6. Installer bauen, Fresh-Unpack-Parität beweisen und dieselben Source-/Workflowtests erneut ausführen.
7. Real WordPress 7.0.1 erneut aus der finalen Installer-ZIP prüfen.
8. WordPress 6.8.3 Produkt-Renderer real prüfen.
9. MASTER bauen, Manifest und Source↔Installer↔MASTER-Parität prüfen.
10. Erst dann automatisches `FINAL_RELEASE_GATE=PASS`.

Kein manueller PASS ersetzt diese Pipeline. Jeder CI-Fail bleibt BLOCKED und erzeugt kein freigegebenes Release.
