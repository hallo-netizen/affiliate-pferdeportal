# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: V1.9.8 HIERARCHIE-PROTOTYP LOKAL HARD PASS / KEIN RELEASE / BUILDER OFFEN

## Live

Livebestand unverändert.
V1.9.7 NICHT installieren.

## V1.9.8 lokaler Stand

Kein neuer Pluginzweig. Exakte Weiterarbeit auf der bestehenden Linie.

Bewiesen:
- native Page-Hierarchie bleibt `post_parent`;
- Page→Category-Grenze erhält technischen Taxonomie-Bridge;
- sichtbare Leafs hängen nativ unter diesem Bridge;
- logische concept_id-/parent_concept_id-Bindung bleibt;
- Bridge bleibt unsichtbar;
- Frontend-Renderer liest die echte WordPress-Struktur;
- Frontend-Struktur ist Teil des Deployment-Readbacks;
- gleiche kurze Leaf-Namen sind in getrennten Hobby-Kontexten zulässig, bei gleichem Parent weiter BLOCKED;
- Magazin = eigene hierarchische `journal_cat`;
- HivePress = eigene `hp_listing_category`;
- keine Cross-Strang-Leaks.

Tests:
- 270/270 PASS.

Echter Buchbinden-Altbestand aus der realen Preview lokal migriert:
- vier Content-Kategorien behalten ihre IDs;
- werden nativ unter genau einen Bridge verschoben;
- sichtbar danach exakt Einstieg / Ausrüstung / Material / Techniken & Praxis;
- HivePress/Magazin/Bridge unsichtbar im Contentblock;
- PASS.

## Offener Blocker

`HD001_CONCEPT_BUILDER_FULL_HIERARCHY_NOT_YET_RESOLVED`

Der Writer kann die gewünschte Tiefe jetzt korrekt abbilden.
Der alte Builder erzeugt weiterhin nur eine Root-Seite + maximal vier direkte Content-Kategorien.

## NEXT ACTION

Builder auf variable 1–3 Page-Ebenen und evidenzgetriebene Leaf-Struktur umbauen und danach gesamten DataForSEO→Frontend-Workflow lokal positiv/negativ durchlaufen lassen.

Kein Installer vor diesem Gesamt-PASS.
