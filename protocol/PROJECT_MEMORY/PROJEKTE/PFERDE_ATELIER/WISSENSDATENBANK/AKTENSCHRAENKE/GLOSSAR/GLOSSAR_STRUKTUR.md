# GLOSSAR – STRUKTUR

STAND: 2026-09-15
STATUS: VERBINDLICHE MASSENSTRUKTUR / ERWEITERBAR

## GRUNDREGEL

Ein Begriff = ein Datensatz. Synonyme bleiben beim Hauptbegriff und erzeugen keinen zweiten Datensatz.

Zulässig ist grundsätzlich jeder sinnvoll erklärbare pferdebezogene Begriff. Der einzige fachliche Ausschluss für einen neuen Begriff ist ein **identischer vorhandener WordPress-Kategoriename** nach rein technischer Normalisierung. Singular/Plural, Portal-Seiten, vorhandene Artikel, ähnliche Suchintentionen oder Kannibalisierung sind keine Ausschlussgründe.

## PFLICHTFELDER

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
- Recht, Kauf, Versicherung & Wirtschaft
- Fachsprache allgemein

Ein Begriff darf mehrere fachliche Bezüge haben, besitzt aber genau einen primären Oberbereich zur Ordnung. Das Startset ist erweiterbar; ein neuer sinnvoller Oberbereich darf ergänzt werden, ohne bestehende Begriffe neu zu erfinden.

## RECHERCHESTATUS

- `KANDIDAT`
- `IN_RECHERCHE`
- `NACHRECHERCHE`
- `GEPRUEFT`

`GEPRUEFT` setzt den verbindlichen WDB-Recherchestandard voraus. Fehlende oder widersprüchliche Quellen werden nicht durch Vermutung geschlossen.

## TEXT-/AUSGABEVERTRAG

Für die spätere Glossarausgabe gelten:
- 150–200 Wörter Fachtext;
- individueller Einstieg;
- klare Erklärung und Abgrenzung;
- natürliche Verwendung von Begriff und Pferdekontext;
- keine wiederkehrenden Generator-/Schablonenphrasen;
- kein Keyword-Stuffing;
- 0 Bodylinks;
- individueller SEO-Titel und individuelle Meta-Description.

Recherche und Formulierung erfolgen im selben Glossar-Worker-Schritt. Die Maschine validiert anschließend Identität, exakten Kategorienamen-Ausschluss, Textvertrag, Quellenbindung, Write und Readback.

## MASSENVERTRAG

Der Kandidatenpool ist eine Warteschlange, keine manuelle Einzelliste. Neue Begriffe dürfen in Batches eingespeist werden. Dubletten/Synonyme und exakte Kategorienamen werden über normalisierte Schlüssel geprüft. Kein paarweiser Vergleich aller Begriffe mit allen Artikeln/Seiten.

## SEO-FELD

`seo_status` ist nur ein interner Hinweis:
- `NICHT_GEPRUEFT`
- `INLINE_KANDIDAT`
- `EIGENE_SEITE_PRUEFEN`
- `IN_ARTIKEL_INTEGRIEREN_PRUEFEN`

Diese Werte ändern den Recherchevertrag nicht.

## DATEIFORM

Ein Datensatz pro Begriff unter `DATEN/`, bevorzugt JSON mit stabiler ID `term-...`. Für die WordPress-Automation gilt das bestehende `uge-json-v1`-/Research-Paket-Schema.
