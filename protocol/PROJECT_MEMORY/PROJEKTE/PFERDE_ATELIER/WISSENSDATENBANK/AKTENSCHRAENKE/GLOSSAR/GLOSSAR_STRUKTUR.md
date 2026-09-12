# GLOSSAR – STRUKTUR

STAND: 2026-09-12
STATUS: VERBINDLICHE V1-STRUKTUR / ERWEITERBAR

## HIERARCHIE

Jeder Begriff erhält mindestens:
- `oberbereich`
- optional `unterbereich`
- `begriff`
- `synonyme`
- `kurzdefinition`
- `facherklaerung`
- `abgrenzung`
- `verwandte_begriffe`
- `quellen`
- `recherche_status`
- `seo_status`

## OBERBEREICHE – STARTSET

- Anatomie
- Exterieur
- Maße
- Farben & Genetik
- Zucht & Zuchtbuchwesen
- Haltung
- Fütterung
- Gesundheit
- Huf & Gliedmaßen
- Verhalten & Ethologie
- Gangarten & Bewegung
- Sport & Ausbildung
- Ausrüstung
- Geschichte & Kultur
- Fachsprache allgemein

Ein Begriff darf mehrere fachliche Bezüge haben, besitzt aber genau einen primären Oberbereich zur Ordnung.

## SEO-FELD

`seo_status` ist nur ein interner Hinweis:
- `NICHT_GEPRUEFT`
- `INLINE_KANDIDAT`
- `EIGENE_SEITE_PRUEFEN`
- `IN_ARTIKEL_INTEGRIEREN_PRUEFEN`

Diese Werte sind **keine SEO-Freigabe** und erzeugen keine URL.

## DATEIFORM

Ein Datensatz pro Begriff unter `DATEN/`, bevorzugt JSON mit stabiler ID `term-...`.
