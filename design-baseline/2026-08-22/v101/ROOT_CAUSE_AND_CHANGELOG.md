# V101 – Tabellenabstand Root Cause

## Protokollbeweis
- V83 / Pferde V1.50.452 legte den Abstand nach Einzelbeitragstabellen bereits verbindlich auf **28 px** fest.
- Der allgemeine V83-Designvertrag enthält dieselbe Regel.
- V94 erweiterte die Tabellen-Normalisierung auf WordPress-Wrapper, direkte Tabellen und kompatible Wrapper und sagt ausdrücklich: **Der bestehende verbindliche Abstand von 28 px nach Tabellen bleibt erhalten.**

## Tatsächlicher Codebruch
- Im Pferde-CSS blieb V83 nur für `figure.wp-block-table` / `.wp-block-table` wirksam; `.comparison-table-wrap` fehlte.
- V94 setzte direkte Tabellen später mit `margin: 0 !important` zurück.
- Ergebnis V100 lokal reproduziert: Pferde `.comparison-table-wrap` = 0 px, Pferde direkte Tabelle = 0 px, Universal direkte Tabelle = 0 px.
- Der Rückfall war daher ein Vertrags-/Implementierungsbruch seit V94, nicht ein neuer V100-Journalfehler.

## V101
- äußerer `figure.wp-block-table`: 28 px
- äußere `.wp-block-table`: 28 px
- äußere `.comparison-table-wrap`: 28 px
- direkte Tabelle in `.entry-content`: 28 px
- innere Tabelle innerhalb eines Wrappers: 0 px, damit kein Doppelabstand entsteht
- Scope ausschließlich `body.single-post article .entry-content`

Unverändert: Journal-Root, live freigegebener V100-Journal-Unterkategorie-Owner-Renderer, Tabellenfarben, Zellmaße, Spaltenbreiten, Responsive-Logik, Suche, Anzeigenmarkt und andere Seitentypen.