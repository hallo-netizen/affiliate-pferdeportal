# V102 – Root Cause / Tabellenabstand bei neuen Produktionsbeiträgen

## Ausgangslage
Der seit Contract V83 bindende Tabellenabstand beträgt 28 px. Altbeiträge zeigen den gewünschten Abstand weiterhin korrekt. V101 sollte den Abstand erneut absichern, hatte auf den neuen Produktionsbeiträgen live aber keine sichtbare Wirkung.

## Harte Ursache
V101 setzte seine neue, späte Abstandsinvariante ausschließlich auf Tabellenblöcke, die **unmittelbare Kinder von `.entry-content`** sind.

Die neuen Produktionsbeiträge besitzen jedoch durchgängig eine andere Struktur:

`entry-content > article.ppm-generated > section[data-block="table"] > div.pm-table-wrap.wp-block-table > table`

und direkt danach:

`div.pm-table-wrap.wp-block-table + p`

Die V101-Spätregel trifft diese verschachtelte Form deshalb nicht. In 17 realen Produktionsplan-Artikeln aller aktuell vorhandenen Kernarten traf der V101-Selektor exakt **0/17** Tabellenwrapper. Damit konnte V101 bei genau den neuen Beiträgen keine Änderung bewirken.

## V102-Ursachenfix
V102 ändert **nicht** die alte Tabellenlogik und **nicht** die Inhalte. Stattdessen wird ausschließlich für die nachgewiesene neue Struktur eine späte, fail-closed Darstellungsinvariante ausgegeben:

- `article.ppm-generated section[data-block="table"] > .pm-table-wrap.wp-block-table` → `margin-bottom: 0`
- unmittelbar folgender Absatz `+ p` → `margin-top: 28px`

Dadurch gehört der sichtbare Abstand dem tatsächlich folgenden Text und ist nicht mehr vom Außenmargin des verschachtelten Tabellenwrappers, Margin-Collapse oder einer früher geladenen Tabellenregel abhängig.

## Scope
Nur:
- WordPress-Einzelbeitrag
- `article.ppm-generated`
- `section[data-block="table"]`
- `.pm-table-wrap.wp-block-table`
- unmittelbar folgender Absatz

Nicht geändert:
- Alt-/Legacy-Beiträge
- Tabellenoptik, Linien, responsive Tabellenlogik
- Journal-Hauptseite und Journal-Unterkategorien
- Suche, Anzeigenmarkt, Kategorie-/Portalraster
- Inhalte, Textmaschine, Produktionspläne

## Versionen
- Pferde Atelier Design: 1.50.467
- Universal Portal Design Suite: 2.2.38
- Contract: V102
