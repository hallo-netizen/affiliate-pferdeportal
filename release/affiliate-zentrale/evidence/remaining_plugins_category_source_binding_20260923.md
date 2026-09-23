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
