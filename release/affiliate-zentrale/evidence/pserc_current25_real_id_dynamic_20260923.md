# PSERC – 25 neue Kategorien mit echten WordPress-IDs

Stand: 2026-09-23

Rolle: fokussierter Delta-Nachweis. **Keine zweite Kategorienquelle.**

Fachliche Kategorienquelle:
`CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`

Aktuelle WordPress-Strukturquelle für reale Seiten-/Term-IDs:
`pferdeatelier.WordPress.2026-09-23.xml`

## Geprüftes Delta

- exakt 25 neue Produktionskategorien
- reale WordPress-Term-IDs: **1577–1601**
- reale Produktseiten:
  - Pferdesättel: 972134
  - Trensen: 972141
  - Offenstallbau: 972148
  - Paddockbau: 972155
  - Reitplatzbau: 972162
- reale Elternketten aus der aktuellen XML verwendet
- Kategorien bleiben flach (`wp_parent_id=0`)

## Echter vorhandener PSERC-Gate

Verwendet:
- `PSERC_Portal_Structure_Gate` aus dem exakt gebundenen PSERC-FIX-Paket
- `PSERC_Stable_Json` aus demselben Paket
- keine nachgebaute Gate-Logik

Ergebnis:
- `PSERC_PORTAL_STRUCTURE_PASS`
- `category_count=25`
- `dynamic_live_category_count=25`
- alle 25 als `LIVE_DYNAMIC_REGISTERED`
- `write_attempted=false`
- Baseline SHA256: `94afcd85f7c8fbaac286486fc5297a31bc34ee13c7d23905e7fe0382c4f60ade`
- Structure Hash: `8833afb25607e2157b7a03018bf833db4353e0f86d08e77bb0c605dd035413f7`

Altbestand 1124 wurde **nicht erneut vollständig durchgetestet**.

## Konsequenz

Für die 25 neuen Kategorien ist **keine PSERC-Codeänderung und keine 25er-Hardcodierung nötig**.

Offen bleibt nur der reale vollständige Lauf:
1. frischen PSTE-Site-Baseline aus der aktuellen WordPress-Struktur erzeugen;
2. PSERC-Metadaten-Snapshot neu erzeugen;
3. der bisher sichtbare 1124er-Bindewert muss dann auf den aktuellen 1149er Produktionsbestand wechseln.

WordPress-Schreiboperation: **keine**.
