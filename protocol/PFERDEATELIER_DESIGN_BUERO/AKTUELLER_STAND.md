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
