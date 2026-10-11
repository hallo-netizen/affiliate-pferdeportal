# HOBBYRAUSCH – KATEGORIE-ZENTRALE

ROLLE: zentraler Daten-/Zugriffspunkt innerhalb des bestehenden Büros `SEO_KATEGORIEN`.

**WICHTIG:** Diese Unterzentrale erzeugt KEINE zweite Current-Wahrheit.

Operative Autorität bleibt:
`../CURRENT_STATE.md`

Zielvertrag bleibt:
`../ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`

## Zweck

Hier wird verbindlich festgehalten:
- welche Kategorien/Seiten/Taxonomien zum Hobby-Depot-Zielbaum gehören;
- welche stabile `node_id` ein Objekt besitzt;
- welche Parent-Zuordnung gilt;
- welche WordPress-/Taxonomie-Art gilt;
- wie andere Plugins read-only auf den aktiven Live-Snapshot zugreifen;
- wie der schwere Kategorie-Workflow nur bei echten Strukturänderungen wieder zugeschaltet wird.

## Zentrale Dateien

- `REGISTER.md` – zentrale Datenbindung und Live-Baseline.
- `RUNTIME_API.md` – neutrale Plugin-API.
- `HD001_BETRIEBSMODUS.md` – Deaktivieren/Löschen/Reaktivieren von HD-001.
- `KATEGORIE_REGISTER_MANIFEST.json` – maschinenlesbarer Manifest-/Hashstand.

## Grundregel

Normalbetrieb:
**HD-004 Kategorie-Kern aktiv / HD-001 Kategorie-Workflow darf nach Live-Smoke-Test deaktiviert sein.**

Strukturänderung:
**HD-001 gezielt wieder aktivieren → Delta → Dry-Run → genau ein Sync → Readback → wieder deaktivieren.**

DataForSEO ist dabei nur SEO-Evidence, niemals Strukturautorität.
