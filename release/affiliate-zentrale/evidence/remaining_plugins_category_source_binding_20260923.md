# Restplugin-Kategorieklassifikation – Quellenbindung – 2026-09-23

Status: BLOCKED_EXACT_SOURCE_BINDING

Scope: ausschließlich statische Pferdeportal-Kategorie-/Portalstruktur-Kopien. Keine Inhalts-, Design-, Performance-, Provider-, Ranking-, Banner- oder sonstige Pluginlogik.

Bereits geschlossen:
- Affiliate-Zentrale 6.72.152: CLOSED PASS
- PPM 6.7.9: CLOSED PASS
- PSERC 0.28.23: dynamischer Kategoriepfad PASS; kein 25er-Codepatch
- PSTE 0.57.6: CLOSED PASS, eine Map 1124 -> 1149

Noch exakt zu binden, bevor eine Kategorieabhängigkeit hart klassifiziert werden darf:
1. Affiliate Portal Template Kit 1.50.559
2. Allgemeine Bildzentrale 2.7.6
3. Portal Link Policy Runtime Verifier 1.0.0
4. Portal Production Center 1.1.1
5. Portal Production Link Policy Gate 1.0.1
6. Portal Category Structure Repair Guard 1.0.1

Geprüfte Quellenwege:
- PLUGINS-Büro: aktuelle installierte Versionen vorhanden, aber keine technischen Vollquellpfade für diese sechs aktuellen Versionen.
- DESIGN-Büro: ältere Template-Kit-Vollquellen/Belege; kein exakt gebundener 1.50.559-Vollbaum.
- BILD-Büro: Bürostand 2.6.9 / historischer Codebeleg 2.4.9; kein exakt gebundener 2.7.6-Vollbaum.
- TEXT-/GEMEINSAM-Büros: keine exakten Vollquellpfade für die vier kleinen aktuellen Plugins.
- main / article-production / aktuelle Produktionsbranches: keine passend benannten Quellordner oder Pakete für die sechs aktuellen Versionen.
- GitHub PR-/Commit-/öffentliche Indexsuche: kein exakter Vollquellbeleg dieser sechs Versionen.
- aktueller Chat/Library: kein vollständiger Quellbaum dieser sechs aktuellen Versionen vorhanden; für Template Kit 1.50.559 ist inzwischen jedoch das exakte historische 1.0.3-Hardtest-/Apply-Hilfsartefakt wiedergefunden (siehe Nachprüfung unten).

Fail-closed:
- Keine Kategorieänderung an diesen sechs Plugins.
- Keine Einstufung "keine statische Kopie" ohne exakte Quellprüfung.
- Keine Rekonstruktion aus älteren Versionen.
- Kein WordPress-Write.

Erster offener Bindungspunkt: Affiliate Portal Template Kit 1.50.559.


## Nachprüfung Template Kit 1.50.559 – PLUGINS-/DESIGN-Büro + vorhandenes Hardtest-Artefakt

PLUGINS-Büro:
- `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/CURRENT_STATE.md` und `PLUGINREGISTER.md` binden 1.50.559 ausschließlich als beobachtete installierte WordPress-Version und routen technisch nach DESIGN.
- Der Eintrag entstand mit Commit `5c151ceffc65659101a054c195e768265ce27281` (`campus: refresh category plugin inventory routing`).
- Dieser Commit ergänzt nur das Installationsinventar; kein 1.50.559-Vollquellpfad, kein Vollbaum-Hash und kein Installer werden dort gebunden.

DESIGN-Büro:
- `CURRENT_STATE.md` / `MASTERDATEIEN_INVENTAR.md` enden technisch bei älteren Ständen und liefern keinen 1.50.559-Vollbaum.
- `WORDPRESS_REGISTER.md` liefert ebenfalls keinen 1.50.559-Installer-/Vollquellbeleg.

Neu wiedergefundenes exaktes historisches Hardtest-Artefakt:
- `PFERDE_ATELIER_PPA013_1.50.558_TO_1.50.559_TEXT30_FINAL_CORRECTIVE_1.0.3_HARDTEST.zip`
- tatsächlicher SHA256: `3600de85fc1a577d8c80ba06c306270c92eafac1144b41b1277b330323778f85`
- stimmt exakt mit der historischen Governance-Bindung überein.
- enthaltene Patcher-PHP SHA256: `428840f989328d9a7bc92b2929498b7a7bff49fca0ba1c000f9ed44f0c7a0878`
- auch dieser Hash stimmt exakt mit der historischen Governance-Bindung überein.
- harte Ausgangsbindung: 1.50.558 / Main SHA256 `840130139597c6152a385475c05b2786c96d08bd137785e127280d9aabe979f1`.
- Zielversion: 1.50.559.
- der Patcher erzwingt für seinen damaligen Apply: nur `pferde-template-kit.php` geändert; keine Datei hinzugefügt/entfernt; Performance-Helfer hashidentisch.
- der 1.50.559-Schritt selbst ersetzt ausschließlich den damaligen Editorial-Overlayblock und die Versionsmarker. Damit ist belegt, dass dieses Delta keine neue separate Kategorie-/Portalstrukturdatei eingeführt hat.

Beweisgrenze:
- Das Hardtest-Artefakt ist **kein vollständiger 1.50.559-Pluginquellbaum**.
- Der spätere Nutzer-Readback bestätigte funktional 30 Texte, Icons und Exact-7; historisch wurde danach jedoch kein vollständiger neuer 1.50.559-Main-SHA-/Vollbaum-Readback dokumentiert.
- Deshalb darf aus dem exakten 1.50.558-Stand plus Patcher **kein Ersatz-Vollbaum rekonstruiert** und nicht behauptet werden, der gesamte 1.50.559-Bestand enthalte keine geerbte statische Kategorie-/Portalstrukturkopie.
- Ergebnis bleibt daher fail-closed: `TEMPLATE_KIT_1_50_559_EXACT_GITHUB_SOURCE_BINDING` offen.


### Harte Kategorieprüfung des hochgeladenen 1.0.3-Hardtest-Artefakts

Direkt geprüftes Artefakt:
- `PFERDE_ATELIER_PPA013_1.50.558_TO_1.50.559_TEXT30_FINAL_CORRECTIVE_1.0.3_HARDTEST.zip`
- ZIP enthält genau drei Dateien: README, HARDTEST_EVIDENCE und den Corrective-Helper.
- Der Helper enthält als reale Kategorie-Slugs ausschließlich die 25 neuen Produktionskategorien der fünf Familien.
- Abgleich gegen die autoritative `CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`:
  - TSV-Gesamtzeilen: 1160
  - geprüfte neue Produktionskategorien: 25
  - Treffer: 25/25
  - fehlend: 0
  - reale Term-IDs: exakt 1577–1601.
- Zusätzlich werden genau die fünf neuen Produktseiten `pferdesaettel`, `trensen`, `offenstallbau`, `paddockbau`, `reitplatzbau` mit den dokumentierten Seiten-IDs 972134/972141/972148/972155/972162 geprüft.
- Im gesamten Helper kommen keine Referenzen auf `portal-structure`, `ebay-portal-catalog`, `category-map`, `KATEGORIEN.tsv`, `complete-portal`, `category-hierarchy`, `wordpress-link-target` oder die Vollcounts 1124/1149/1160/5745/5790 vor.
- Der Preflight bindet den exakten 1.50.558-Main-SHA und prüft die 30 realen Knoten; der Apply erlaubt ausschließlich die Änderung von `pferde-template-kit.php`, keine hinzugefügte oder entfernte Plugin-Datei.
- Der 1.50.558→1.50.559-Transform ersetzt nur den bestehenden Editorial-Overlayblock und Versionsmarker; Grid/Icon-Logik ist VERIFY_ONLY.

Belastbare Aussage:
- Das 1.50.559-Delta selbst führt **keine neue statische Vollkopie** der Pferdeportal-Kategorien oder Portalstruktur ein.
- Das hochgeladene Hardtest-Artefakt enthält **keine zweite 1149/1160-Kategorienwahrheit**, sondern ausschließlich die 30 zielgerichteten Prüfknoten der damaligen Kategorieergänzung.

Weiter bestehende Beweisgrenze:
- Das Artefakt enthält nicht den vollständigen installierten 1.50.559-Vollquellbaum.
- Deshalb ist allein damit nicht bewiesen, ob eine bereits vor 1.50.558 vorhandene statische Vollstruktur irgendwo im unveränderten restlichen Template-Kit-Quellcode existiert.
- Kein Ersatz-Vollbaum wird aus 1.50.558 rekonstruiert.


## Template Kit – statischer Kategorieverbraucher hart gefunden

Direkter Altquellcode-Beleg:
- Datei: `pferde-template-kit_V1.50.421.php`
- Blob SHA: `bd26b65d033160ada9f98d249794b9911ab1fb2c`
- vollständig gelesen: 1.569.800 Bytes.

Gefundener statischer Verbraucher:
- `assets/breadcrumb-portal-map-v150310.json`
- Loadervertrag: `PFTK_BREADCRUMB_PORTAL_MAP_V150310`
- harter erwarteter `category_count`: **1124**
- harter `count(categories)`: **1124**
- der Loader liest diese Datei als statische Breadcrumb-Kategorienkarte.

Weitere harte Altquellprüfung:
- keine Referenz auf `portal-structure-v279.json`
- keine Referenz auf `KATEGORIEN.tsv`
- keine Referenz auf `category-map`
- keine Referenz auf `complete-portal-category-source`
- keine Referenz auf `category-hierarchy`
- keine Referenz auf `wordpress-link-target`
- keine hart codierten Blattkategorie-Slugs der neuen 25 Kategorien im Altquellcode.
- die zahlreichen `term_id`-Vorkommen sind überwiegend Runtime-Termzugriffe bzw. die kleine separate Journal-Konfiguration; sie sind **nicht** die 1124er Portalvollstruktur.

Delta-Beweise:
- 1.50.556 -> 1.50.558: dokumentierter Apply änderte ausschließlich `pferde-template-kit.php`; keine Datei hinzugefügt/entfernt.
- 1.50.558 -> 1.50.559: hochgeladenes 1.0.3-Hardtest-Artefakt erzwingt ebenfalls ausschließlich `pferde-template-kit.php` als geänderte Datei; keine Datei hinzugefügt/entfernt.
- Der 1.0.3-Transform selbst verändert nur Editorial-Overlay + Versionsmarker; keine Asset-Datei.
- Damit wurde die Breadcrumb-Map durch diese beiden Deltas jedenfalls nicht neu erzeugt oder entfernt.

Beweisgrenze / aktueller echter Blocker:
- Die aktuelle 1.50.559-Vollquelle bzw. die reale aktuelle Datei `assets/breadcrumb-portal-map-v150310.json` ist weiterhin nicht direkt gebunden.
- Deshalb darf die alte 1124er Map **nicht aus einer anderen Kategorienquelle rekonstruiert und als aktuelle 1.50.559-Datei ausgegeben** werden.
- Der Verbraucher ist aber nicht mehr ungeklärt: **statische Kategorieabhängigkeit = JA**.
- Nächste technische Bindung innerhalb des Template-Kits: exakte aktuelle `assets/breadcrumb-portal-map-v150310.json` aus dem echten 1.50.559-Pluginbaum beschaffen/hashbinden und gegen die autoritative `KATEGORIEN.tsv` prüfen.
- Falls sie weiterhin 1124 enthält, ausschließlich dieses Breadcrumb-Kategorieasset plus notwendige Count-/Hash-Bindungen auf die neue Kategorienwahrheit nachziehen; sonst nichts am Template-Kit ändern.


## PPA-013 historischer Vollquell-Audit – statischer Breadcrumb-Strukturverbraucher identifiziert

Hard-Baseline:
- Run `35904805135` → SUCCESS
- geprüfter Head: `f1d3225593f5221695bf2770fce5de23e5db8ff4`
- historischer Originalquellstand wurde ausschließlich read-only aus dem bereits gespeicherten 1.50.469-Fixture rekonstruiert.
- exakter historischer PHP-SHA256: `580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`
- Größe: 1,650,857 Bytes.
- Rolle dieses historischen Quellstands: EVIDENCE ONLY, niemals Ersatz-/Current-Quelle für 1.50.559.

Entscheidender Befund:
- PPA-013 referenziert statisch `assets/breadcrumb-portal-map-v150310.json`.
- Vertrag im Quellcode: `PFTK_BREADCRUMB_PORTAL_MAP_V150310`.
- Quellcode verlangt hart:
  - `category_count == 1124`
  - `count(categories) == 1124`.
- Kommentar im Originalquellcode beschreibt die Datei ausdrücklich als vollständigen, sluggebundenen Strukturvertrag für 1.124 Kategorien.
- Nutzung: fachlicher Breadcrumbpfad für technisch flache Artikelkategorien.
- sichtbare Kategorienamen kommen dynamisch aus aktuellem `WP_Term`.
- IDs, Slugs, URLs und Taxonomie-Parents werden durch diesen Vertrag nicht geschrieben/verändert.
- historische Runtime ist read-only gegenüber WordPress:
  - `wp_insert_term`: 0
  - `wp_update_term`: 0
  - `wp_delete_term`: 0
  - `wp_set_object_terms`: 0
  - dynamische Leser vorhanden: `get_terms`, `get_term_by`, `get_term`.

Abgrenzung:
- keine Referenz auf `portal-structure-v279.json`, `ebay-portal-catalog-v2.json`, `KATEGORIEN.tsv`, PPM hierarchy/link snapshots.
- die relevante statische Kopie im Template Kit ist damit **nicht** die komplette Affiliate-/PPM-Struktur, sondern der eigene Breadcrumb-Strukturvertrag `assets/breadcrumb-portal-map-v150310.json`.

Folgerung für den laufenden Kategorieauftrag:
- Die frühere Aussage „im Template Kit keine statische Kategorie-/Portalstruktur-Kopie gefunden“ ist überholt.
- Es existiert mindestens dieser statische 1124er-Verbraucher.
- Der 1.50.558→1.50.559-Hardtest beweist nur, dass dieses Delta keine neue Datei anlegt/entfernt und nur `pferde-template-kit.php` verändert; er bindet den unveränderten Assetbestand nicht vollständig.
- Deshalb bleibt fail-closed offen, ob die aktuell installierte 1.50.559-Datei dieses Assets noch exakt den 1124er-Vertrag enthält.
- Nächster enger Bindungspunkt ist ausschließlich die aktuell installierte 1.50.559-Datei `assets/breadcrumb-portal-map-v150310.json` samt SHA/Count/Schema.
- Falls Current weiterhin 1124 enthält, ist genau diese statische Ableitung auf 1149 gegen die autoritative zentrale Kategorienwahrheit zu aktualisieren; keine Text-/Designarbeit und kein WordPress-Write vor dem vorgeschriebenen Dry-Run.


### Rolle der Breadcrumb-Map im tatsächlichen Runtimepfad

Direkt aus dem historischen, hashgebundenen Template-Kit-Quellcode geprüft:

1. Breadcrumbs:
- Primärquelle ist `breadcrumb_menu_page_chain_v150310()`, also die reale WordPress-Menüstruktur.
- Nur wenn dieser Menüpfad leer bleibt, fällt `breadcrumb_portal_page_chain_v150310()` auf `breadcrumb_contract_page_chain_v150310()` und damit auf `assets/breadcrumb-portal-map-v150310.json` zurück.
- Für einen Slug, der nicht in der Map steht, liefert `breadcrumb_expected_page_slugs_v150310()` eine leere Erwartung; der Menüpfad wird dadurch **nicht** blockiert.
- Das erklärt den Nutzer-Readback: Breadcrumbs funktionieren auch für die neuen Kategorien, obwohl eine alte 1124er Map möglich ist.

2. Leaf-/Hub-Kontext:
- `leaf_category_hub_context_v150396()` liest dieselbe Breadcrumb-Map, um den übergeordneten Hubtitel abzuleiten.
- Fehlt der Slug in der Map, wird nur auf den echten Taxonomie-Parent zurückgefallen.
- Die Portal-Leaf-Kategorien sind im alten Vertrag technisch flach; bei `parent=0` kann dieser Fallback leer bleiben.
- Für die 25 neuen Kategorien ist das im aktuellen 1.50.559-Stand jedoch ohne sichtbare Auswirkung auf den Introtext, weil das 1.0.3-Artefakt 25/25 feste Editorial-Leaftexte in den bestehenden PPA-013-Katalog schreibt und der Hub-Kontext nur für den automatisch generierten Fallback-Introtext verwendet wird.

3. Bestehende Hard-Gates:
- `CATEGORY_INTEGRATION_HOBBYRAUM/audit_current.py` kennt `breadcrumb-portal-map-v150310.json` ausdrücklich als historische Strukturreferenz.
- Der aktuelle Hard-Audit verlangt **keinen** 1124->1149-Countwechsel dieser Datei; er protokolliert die Referenz nur im historischen read-only Template-Kit-Beleg.
- Somit liegt aktuell kein Produktionsfehler und kein bereits vorhandener Gate-FAIL wegen dieser Datei vor.

4. Warum der Verbraucher trotzdem offen bleibt:
- Abschnitt 0A des Category Change Masters verlangt für **jedes tatsächlich installierte Plugin**, das Kategorien/Portalstruktur konsumiert, die exakte aktuelle Quelle.
- Die Breadcrumb-Map ist eine tatsächliche statische Kategorie-/Strukturkopie und damit innerhalb dieses Zielvertrags ein Verbraucher, auch wenn sie nur sekundär verwendet wird.
- Deshalb darf sie nicht allein aufgrund funktionierender Live-Breadcrumbs ignoriert werden.

5. Minimaler möglicher Delta, falls die exakte aktuelle 1.50.559-Datei weiterhin 1124 Kategorien enthält:
- `assets/breadcrumb-portal-map-v150310.json`: 1124 -> 1149 Produktionskategorien.
- die zugehörige harte PHP-Prüfung `category_count === 1124` und `count(categories) === 1124` müsste synchron auf 1149 gebunden werden.
- keine sonstige Design-/Text-/Breadcrumb-Logik ändern.
- Dieser Delta darf **nicht** gebaut werden, bevor die exakte aktuelle 1.50.559-Quelle/Map hashgebunden ist.

6. Exakter Tree-Nachweis:
- Governance-Apply 1.50.556 -> 1.50.558: `plugin_tree_diff.changed = ["pferde-template-kit.php"]`, `added=[]`, `removed=[]`.
- gespeichertes Backup-Manifest: `ppa013-category-completion-manifest-20260922-194858-33451736b021.json`.
- 1.50.558 -> 1.50.559 erzwingt ebenfalls ausschließlich `pferde-template-kit.php` als geänderte Datei.
- Damit ist jede unveränderte Asset-Datei zwischen 1.50.556 und 1.50.559 byteidentisch; der noch fehlende Punkt ist ausschließlich der exakte Hash/Inhalt der aktuellen Breadcrumb-Map aus dem 1.50.556-Tree-Manifest oder einem aktuellen Vollquellbaum.
