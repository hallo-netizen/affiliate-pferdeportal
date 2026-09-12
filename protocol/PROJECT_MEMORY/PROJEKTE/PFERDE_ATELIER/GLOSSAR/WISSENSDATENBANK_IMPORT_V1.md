# PFERDE-ATELIER GLOSSAR – WISSENSDATENBANK-IMPORT V1

STAND: 2026-09-12
STATUS: GEBUNDENE PROJEKTBRÜCKE / KEINE ZWEITE FACHWAHRHEIT

## Zweck

Die Wissensdatenbank bleibt die einzige Fachquelle. Dieser Adapter erzeugt daraus ausschließlich eine WordPress-Veröffentlichungsdatei im neutralen Format `uge-json-v1`.

Adapter:
`tools/build_uge_import.py`

Quelle:
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/DATEN/`

## Harte Regeln

- Quelldateien werden niemals verändert.
- Nur `recherche_status = GEPRUEFT` wird in die Importdatei übernommen.
- Ungeprüfte Datensätze werden ausgelassen.
- Fehlende Pflichtfelder brechen die Erzeugung hart ab.
- WordPress-Import bleibt anschließend immer `draft`.
- Keine automatische Veröffentlichung.
- Quellen, Trust, Recherche-/SEO-Status und Prüfdatum bleiben ausschließlich in der Wissensdatenbank.

## Feldabbildung V1

Wissensdatenbank → WordPress-Import:

- `id` → `external_id` + stabiler Slug ohne Präfix `term-`
- `begriff` → Titel
- `oberbereich` → primärer öffentlicher Glossar-Oberbereich
- `kurzdefinition` → Kurzdefinition
- `facherklaerung` → Erklärungstext
- `abgrenzung` → eigener Absatz innerhalb der Veröffentlichungsfassung
- `synonyme[]` → Synonyme
- `verwandte_begriffe[]` → verwandte Begriffe

Nicht kopiert:
- `unterbereich`
- `quellen`
- `recherche_status`
- `seo_status`
- `letzte_pruefung`

Warum `unterbereich` in V1 nicht kopiert wird:
Die öffentliche Startnavigation ist aktuell bewusst auf primäre Oberbereiche begrenzt. Die Wissensdatenbank behält die feinere Einordnung vollständig. Wenn später Unterbereiche öffentlich benötigt werden, kann der Adapter sie ergänzen, ohne die Quelldaten oder den allgemeinen Core umzubauen; die Glossar-Gruppen sind bereits hierarchisch erweiterbar.

## Flexibilitätsregel

Der Adapter ist projektspezifisch und der Core bleibt neutral.

Andere Portale können denselben `MOD-008`-Core mit einem anderen Adapter bzw. bereits nativem `uge-json-v1` nutzen. Neue Fachfelder dürfen später über das erweiterbare Feldschema ergänzt werden, ohne bestehende Glossarbegriffe zu zerstören.
