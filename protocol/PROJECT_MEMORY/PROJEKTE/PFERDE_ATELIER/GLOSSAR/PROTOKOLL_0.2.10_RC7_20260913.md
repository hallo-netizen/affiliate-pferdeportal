# GLOSSAR – PROTOKOLL 0.2.10-rc7 – 2026-09-13

ROLLE: technisches Entwicklungs-/Testprotokoll. Keine zweite CURRENT-/LIVE-Wahrheit.

## Ausgangslage

Der reale 0.2.8-Nutzerreadback hatte weiterhin tote Einzelbegriff-Links und weitere Frontendfehler gezeigt. In der 0.2.10-Linie kamen zusätzlich die verbindlichen Produktionsregeln für geschlossene verwandte Begriffscluster, echte `Verwandte Begriffe`-Links, Kategorieverlinkung, Ausschluss von Pferderassen und kurze Artikel ohne erzwungene Zwischenüberschriften hinzu.

## Wesentliche Änderungen bis rc7

- Einzelbegriff-Rendering gegen einen absichtlich geleerten normalen WordPress-Main-Loop abgesichert.
- Glossar-Breadcrumb in die reale Breadcrumb-Achse des Pferde-Designs eingebunden.
- `Verwandte Begriffe` werden als echte Links zu veröffentlichten `uge_term`-Zielen gerendert.
- neuer geschlossener Testcluster: `Hufrehe`, `Strahlfäule`, `Hufabszess`.
- Cluster wird zunächst als Draft-Satz angelegt, vollständig verknüpft/geprüft und erst danach publiziert.
- Pferde-/Ponyrassen bleiben aus dem Glossar ausgeschlossen.
- RC6-Publikationsfehler repariert: die normale UGE-Publikationspolicy verlangt eine gültige primäre Portal-Kategorie; rc7 bindet die reale Portal-Kategorie `Gesundheit` vor der Veröffentlichung und setzt `primary_category_id` für jedes Pack-Mitglied.

## RC6-Fehler

RC6 erzeugte die drei Pack-Mitglieder als plugin-eigene Entwürfe, konnte sie aber nicht vollständig veröffentlichen. Die bestehende Publikationspolicy wurde nicht umgangen; der fehlende Pflichtbeleg war die primäre Portal-Kategorie.

## RC7-Hardtest

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Getesteter Head:
`1e74b7454e84f97182dbb185614371a48157bc21`

Workflow:
`.github/workflows/glossar-0210-rc7-hardtest.yml`

Run:
`34762048546` → SUCCESS

Jobs:
- `103736483729` build → SUCCESS
- `103736483608` fresh → SUCCESS
- `103736483696` real-design-clickability → SUCCESS
- `103736720142` no-package-gate → SUCCESS

## Tatsächlich ausgeführte Positiv-/Negativ-/Regressionstests

Fresh/alte Regression:
- reale WordPress/Astra-Testumgebung bootet;
- Home-Links, A–Z, AJAX Positiv/Negativ, Breadcrumb-/Route-Kollision, primärer Kategorienlink;
- Draft öffentlich 404;
- authentifizierte Draft-Preview PASS;
- Duplicate Guard PASS;
- normale WordPress-Beiträge unverändert;
- Cluster-Beziehungen und Kategorieverlinkung vorhanden;
- Pferderassen-Leak negativ geprüft.

Real Design:
- exakter rekonstruierter Design-Hauptcode 1.50.469, SHA-256 `580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`;
- reale Kategoriehierarchie erkannt;
- WordPress-Main-Loop für Glossar-Einzelroute absichtlich geleert;
- Einzelansicht muss trotzdem realen Artikel/H1/Inhalt liefern;
- Browser prüft reale Breadcrumb-Geometrie.

## Echter Browser-Klickbeweis

Der Browser führte tatsächlich folgende Klicks aus:

1. `/glossar/gesundheit/` → gerenderter vorhandener Link `Hufbein` → echte Einzelansicht mit `FULL-HUFBEIN-SENTINEL`;
2. `/glossar/gesundheit/` → `Hufrehe`;
3. sichtbarer Link unter `Verwandte Begriffe` → `Strahlfäule`;
4. sichtbarer verwandter Link → `Hufabszess`;
5. sichtbarer Kategorienlink → zurück zu `/glossar/gesundheit/`.

PASS-Marker:
- `UGE0210_PFERDE_BREADCRUMB_AXIS_PASS`
- `UGE0210_REJECTED_HERO_FALLBACK_ABSENT_PASS`
- `UGE0210_EXISTING_SINGLE_CLICK_PASS`
- `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`
- `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`
- `UGE0210_BROWSER_PASS`
- `UGE0210RC7_REAL_DESIGN_CLICKABILITY_BREADCRUMB_LOOP_POISON_PASS`

## Was NICHT geprüft/freigegeben wurde

- kein realer Pferde-LIVE-Readback;
- kein rc7-Installationspaket;
- kein rc7-ZIP-SHA;
- kein gated Release-/Paketjob;
- keine Synchronisierung als `PROJEKTE/PFERDE_ATELIER/PLUGINS/ISOLIERTE_PLUGINS/.../CURRENT.zip`.

Der Workflow endet ausdrücklich mit:
`UGE0210RC7_HARD_GATES_PASS_NO_PACKAGE`.

## Abschlussstatus

**Technische rc7-Hardtests: PASS.**

**Klickbarkeitsnachweis im Testsystem: PASS.**

**Paket/Übergabe: BLOCKED bis gated Paket auf exakt gebundenen Bytes vorliegt.**

**Pferde-LIVE: OFFEN.**
