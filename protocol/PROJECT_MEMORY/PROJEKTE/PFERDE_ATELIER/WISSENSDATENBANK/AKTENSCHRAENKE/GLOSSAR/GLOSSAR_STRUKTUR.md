# GLOSSAR – STRUKTUR

STAND: 2026-09-15
STATUS: VERBINDLICHE FACHWÖRTERBUCH-STRUKTUR

## GRUNDREGEL

Ein Begriff = ein Datensatz. Synonyme bleiben beim Hauptbegriff.

Eine eigene Glossarseite entsteht nur, wenn **die Erklärung des Fachbegriffs selbst der Hauptzweck** ist. Größere Themenfelder, Portal-/Kategorie-/Rassengruppenseiten und eigenständige Ratgebergegenstände werden nicht als zweite Glossarseite dupliziert.

## PFLICHTFELDER

Jeder Glossarbegriff erhält mindestens:
- `external_id` / stabile `term-*`-ID
- `begriff`
- `slug`
- genau eine `themenwelt` / `uge_group`
- `synonyme`
- `kurzdefinition`
- `facherklaerung`
- `abgrenzung`
- mindestens einen Eintrag `verwandte_begriffe`
- `verwandte_slugs`
- `quellen`
- `recherche_status`
- `last_verified_at`
- `review_interval_months`
- `seo_title`
- `seo_description`
- optional `primary_target` mit Typ `page` oder `category` und realer ID

## THEMENWELTEN

WordPress verwendet dafür die vorhandene Taxonomie `uge_group`. Ein Begriff besitzt genau eine primäre Themenwelt.

Verbindliche Navigationswelten:
- Pferd & Biologie
- Gesundheit & Medizin
- Haltung & Fütterung
- Verhalten & Pferd-Mensch
- Reiten & Ausbildung
- Pferdesport & Disziplinen
- Zucht & Genetik
- Ausrüstung & Praxis
- Geschichte, Kultur & Gesellschaft
- Recht, Kauf, Versicherung & Wirtschaft

## BEZIEHUNGEN

### Themenwelt
Pflicht. Dient der fachlichen Einordnung und der Glossarnavigation.

### Verwandte Begriffe
Pflicht. Mindestens ein direkter fachlicher Bezug. Existiert der verwandte Glossarbegriff bereits öffentlich, wird er im Frontend verlinkt. Noch nicht vorhandene zugeordnete Begriffe dürfen als Beziehung gespeichert werden, werden aber nicht auf eine erfundene URL verlinkt.

### Passende Hauptseite
Optional. Genau eine starke vorhandene WordPress-Seite oder Kategorie, wenn sie die fachliche Hauptheimat des Begriffs bildet. Keine beliebige Artikellinkliste.

## RECHERCHESTATUS

- `KANDIDAT`
- `IN_RECHERCHE`
- `NACHRECHERCHE`
- `GEPRUEFT`

`GEPRUEFT` setzt den verbindlichen WDB-Recherchestandard voraus.

## TEXTVERTRAG

- 150–200 Wörter Fachtext
- individueller Einstieg
- Definition + fachliche Einordnung + Abgrenzung
- natürliche Sprache
- keine Generator-/Schablonenphrasen
- kein Keyword-Stuffing
- 0 Bodylinks
- individueller SEO-Titel + Meta-Description

## AKTUALISIERUNG

- Medizin/Gesundheit und andere risikosensitive Fachthemen: 6 Monate
- normale Fachbegriffe: 12 Monate
- ausdrücklich stabile historische/terminologische Inhalte: 24 Monate

Fälligkeit = `last_verified_at + review_interval_months`.

Die Fälligkeit erzeugt nur Prüfbedarf. Keine automatische inhaltliche Änderung und kein Auto-Publish.

## WORDPRESS-VERTRAG

Neuproduktion über `PA_GLOSSARY_BATCH_V2`:

`Campus-Datensatz → JSON-Staging → Validator → Draft-Write → Feld-/Taxonomie-Readback → PASS oder kompletter neuer Batch-Rollback`

Maximal 25 neue Begriffe je Batch. Kein Auto-Publish.

## DATEIFORM

Ein Datensatz pro Begriff unter `DATEN/`. Autoritative Technik: `TECHNIK_GLOSSAR_MANAGER_CURRENT.md`.
