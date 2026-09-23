# Pferdeportal Kategorien – Änderungsprotokoll

Status: VERBINDLICHE ZENTRALE ABLAGE.

## Harte Regeln

- Aktuelle WordPress-XML -> genau eine zentrale Kategorienliste.
- Keine Automatik.
- Kein Kategorieplugin.
- Kein erneutes Durchtesten alter Beweise.
- Keine zweite Kategorienquelle.

## 2026-09-23 – Ausgangsstand

Quelle:
- `pferdeatelier.WordPress.2026-09-23.xml`
- WordPress-Export: `2026-09-23 07:14 UTC`
- Quell-SHA256: `d4564160f1a73cd6f6c79b4afa6c53d7e6c0c593d2d9de9c53adbcc5adea3655`

Durchgeführte Änderung:
1. Ausschließlich die `<wp:category>`-Einträge der aktuellen XML übernommen.
2. Pro Kategorie nur `term_id`, `slug`, `name` und `parent_slug` gespeichert.
3. Keine Kategorie ergänzt, umbenannt, verschoben oder gelöscht.
4. Keine Plugin-, PPM-, Affiliate-, PSERC- oder sonstige Logik eingebaut.
5. Zentrale Liste: `KATEGORIEN.tsv`.
6. Der verworfene Kandidat `PFERDEPORTAL_KATEGORIEN_V0.2.0_CANDIDATE_MIN.zip`, seine Statusdatei und sein eigener Workflow wurden entfernt.

Bestand der aktuellen XML:
- Kategorien gesamt: **1160**

Ab jetzt gilt:
Jede spätere Kategorienänderung wird in `KATEGORIEN.tsv` eingetragen und hier protokolliert. Andere Plugins dürfen daraus nur ihren eigenen benötigten Stand ableiten; sie sind keine zweite Kategorienquelle.

## 2026-09-23 – Steuerstand nachgezogen

- `CURRENT_RELEASE.json` bindet die zentrale `KATEGORIEN.tsv` jetzt ausdrücklich als einzige Kategorien-Inhaltsquelle.
- Die bestehende Kategorieakte wurde entsprechend präzisiert.
- PPM-/Plugin-interne Kategorienbestände gelten nur noch als technische Ableitungen, nicht als zweite Wahrheit.
- Keine Kategorie geändert.
