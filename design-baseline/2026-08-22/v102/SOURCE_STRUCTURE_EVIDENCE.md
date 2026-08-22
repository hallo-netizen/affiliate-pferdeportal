# Source Structure Evidence V102

Aus fünf realen Produktionsplan-Dateien wurden 17 Artikel ausgewertet:
- Beratung: 4
- FAQ: 4
- Pflege: 4
- Vergleich: 5

Alle 17 besitzen einen `article.ppm-generated`-Root und einen Tabellenblock `section[data-block="table"]`.
Alle 17 besitzen darin unmittelbar einen Wrapper `.pm-table-wrap.wp-block-table`.
Bei allen 17 ist der unmittelbar folgende Geschwisterknoten des Wrappers ein Absatz `<p>`.

Selektornachweis:
- V101 späte Direct-Child-Invariante: 0/17 Treffer
- V102 PPM-Strukturinvariante: 17/17 Treffer

## Reproduzierbare Quellen (SHA-256)
- `c6a984d73fb197211dc52d80217bb15a2c62cc1966848290e7e5c44a67d655fc`  `GESTREUTE_NAECHSTE_WELLE_4_ARTIKEL_PRODUKTIONSPLAN(2).json`
- `8905006190895f0ee955f00a9b288fd7b373f6b3fd5795a592316865130e8519`  `NAECHSTE_BREIT_GESTREUTE_WELLE_4_ARTIKEL_PRODUKTIONSPLAN.json`
- `c09c202eaf8dd019dd8a711145dbf768264e5245f6b3a6ad0b572bed841cc0d5`  `NAECHSTE_WELLE_4_ARTIKEL_PRODUKTIONSPLAN.json`
- `51ea1eb493a0ce03dfc06d7fabd0263c7ea8287f5477d30307b53a003ad518a9`  `SEMANTIK_TEST_1_ARTIKEL_PRODUKTIONSPLAN.json`
- `ce60ad7cfd80a954ad1caa545cd920923112560299da4f6ba4306eb42a1bd08c`  `WINTERDECKEN_4_ARTIKEL_PRODUKTIONSPLAN.json`
