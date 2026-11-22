# Pferdeatelier Design-Büro – aktueller Stand

Stand: 22.11.2026

## Verbindliche Basis

Aktuelles Designplugin: **1.50.632 – LIVE PASS**

Archivpfad:
`/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.632_LIVE_PASS.zip`

Prüfnachweis:
`/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.632_LIVE_PASS_PRUEFNACHWEIS.json`

## Abgenommener Zustand

- 1.50.628: konsolidierte Basis aus Template-Kit + Breadcrumb-Helfer + Canonical Table Contract.
- 1.50.629: Journal-Unterseiten – Überschrift ins Hero, Banner nach oben, Paginierung oben/unten.
- 1.50.630: Journal – Banner auf Inhaltsbreite, Amazon-Kachel in Kartenraster, Paginierungsdesign, Ziel 8 Beiträge + 1 Amazon-Kachel.
- 1.50.631: Paginierungsdesign vom Nutzer PASS bestätigt; Beitragszahl weiterhin fehlerhaft.
- 1.50.632: harte 8-Beiträge-Begrenzung mit synchroner Seitenlogik; Nutzer hat anschließend **PASS** bestätigt.
- Journal-Design insgesamt: **PASS**.
- Glossar und Pferderassen waren von diesem Journal-Umbau ausgeschlossen.
- Hero, Banner, Amazon-Kachel und Paginierung sind im aktuellen Stand visuell abgenommen.
- Aktuelle Journal-Grenze: maximal **8 echte Beiträge pro Seite**; Amazon-Kachel zusätzlich im Raster.

## Regel für weitere Änderungen

Alle weiteren Designänderungen bauen ausschließlich auf **1.50.632 LIVE PASS** auf.
Keine Rückkehr zu 1.50.631 oder älter, außer ausdrücklich als Fallback.
Performance-Arbeiten bleiben getrennt vom Design.

## Live

1.50.632 ist nach Nutzerprüfung für Live freigegeben.
Nach Live-Installation dient 1.50.632 als gemeinsame Basis für Live und Test.


## 2026-11-22 – 1.50.633 Einzelbeitrag rechte Begleitspalte – NUR TEST

- Ausgangsbasis: **1.50.632 LIVE PASS**. Diese bleibt der letzte abgenommene Live-Fallback.
- Scope: ausschließlich klassische WordPress-Einzelbeiträge (`post`).
- Desktop + Tablet ab 768 px: rechte Begleitspalte nach Hab-&-Bewahr-Vorbild.
- Mobil unter 768 px: keine aktive Sidebar; alle Originalelemente bleiben bzw. werden beim Verkleinern an exakt ihre ursprünglichen DOM-Stellen zurückgesetzt.
- Rechte Spalte nutzt ausschließlich bereits gerenderte Originalelemente:
  - vorhandene Amazon-Anzeige wird bevorzugt; falls im Artikel keine vorhandene Amazon-Anzeige existiert, wird die vorhandene Artikelanzeige verwendet,
  - vorhandener Produktblock mit bis zu drei durch die Affiliate-Zentrale bereits geprüften Produkten,
  - Astras vorhandene gleichkategorische Empfehlung; rechts wird genau ein weiterführender Beitrag gezeigt.
- Keine neue Affiliate-URL, keine neue Produktauswahl, keine neue Empfehlungsquery, kein neuer Shortcode, keine Änderung am Affiliate-Router.
- Kein Sticky-Verhalten.
- Diff gegen 1.50.632: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert; keine Datei hinzugefügt oder entfernt.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.633_EINZELBEITRAG_SIDEBAR_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.633_PRUEFNACHWEIS.json`
- Status: **NUR TEST**. Visuelle Abnahme Desktop/Tablet steht aus; 1.50.632 bleibt bis dahin LIVE PASS.


## 2026-11-22 – 1.50.633 FAIL / 1.50.634 Reparatur – NUR TEST

- 1.50.633 wurde vom Nutzer sichtbar als **FAIL** bewertet: Einzelbeitrag deutlich zerschossen, linke Inhaltsspalte zu schmal, Seitenachse im weiteren Verlauf gebrochen.
- Nachgewiesene Ursache: 1.50.633 verschob `entry-header` und `entry-content` aus Astras Original-DOM in einen neu erzeugten Layoutcontainer.
- 1.50.633 ist damit verworfen und darf nicht Live gehen.
- 1.50.634 wurde **direkt aus 1.50.632 LIVE PASS** gebaut, nicht aus 1.50.633.
- Reparaturprinzip 1.50.634:
  - Artikel, Überschrift, Hero und kompletter Fließtext bleiben vollständig in Astras Originalstruktur.
  - Rechte Spalte wird nur als Geschwister von `#primary` in der bestehenden `.ast-container`-Struktur ergänzt.
  - Vorhandene Anzeige und vorhandener Produktblock werden nur geklont; die Originale bleiben im DOM und werden nur Desktop/Tablet verborgen.
  - Weiterführender Beitrag verwendet ausschließlich den bereits von Astra ermittelten gleichkategorischen Link; keine neue Query.
  - Kein neuer Affiliate-Shortcode, keine neue Produktlogik, keine URL-Neuerzeugung, kein Sticky.
  - Mobil unter 768 px erzeugt keinen aktiven Sidebar-Zustand und bleibt beim Originalstand.
- Diff zu 1.50.632: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert.
- PHP 9/9 PASS, JS-Syntax PASS, ZIP-CRC PASS, statischer Sicherheitsvertrag PASS.
- Artefakt: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.634_EINZELBEITRAG_SIDEBAR_REPARATUR_NUR_TEST.zip`
- Prüfnachweis: `/pferdeatelier/PLUGINS/PPA-002-DESIGN/PFERDE_ATELIER_DESIGN_1.50.634_PRUEFNACHWEIS.json`
- **1.50.632 bleibt weiterhin der letzte LIVE-PASS-Fallback.**
