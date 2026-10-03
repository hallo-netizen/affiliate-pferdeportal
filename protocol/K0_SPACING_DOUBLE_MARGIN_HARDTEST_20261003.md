# K0 spacing double-margin hard test — 2026-10-03

Scope: structured single-post vertical spacing only.

Observed cause reproduced locally:
- existing final child margin: 32 px;
- existing next-section margin-top: 32 px;
- in a non-collapsing runtime layout this becomes 64 px above the next H2/Fazit;
- H2-to-first-text remains 32 px.

NEGATIVE current main:
- ordinary above H2: 64 px;
- ordinary below H2: 32 px;
- list to Fazit box: 64 px;
- Fazit H2 to text: 32 px.

POSITIVE candidate:
- ordinary above H2: 32 px;
- ordinary below H2: 32 px;
- list to Fazit box: 32 px;
- Fazit H2 to text: 32 px.

Product change is only this selector:
`body.single-post .entry-content article.ppm-generated>section[data-block]:not([data-block="conclusion"])>:last-child{margin-bottom:0!important;}`

No heading decoration, Fazit styling, content, table, links, LanguageTool, PPM, importer, canonical IDs or publish behavior changed.
