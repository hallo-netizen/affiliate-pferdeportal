# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-07
STATUS: V1-PROTOTYP + ZIP-INSTALLATIONSTEST PASS / MANUELLER WP-TEST BEREIT

## AUTORITÄT DIESER DATEI

Diese Datei ist die **einzige aktuelle Campus-Standzusammenfassung dieses Büros**.

- aktuelle Arbeit / NEXT ACTION -> `HOBBYRAUM.md`
- Fehler -> `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` -> autoritative Fehlerquelle
- Zielvertrag -> `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` -> Hauptquelle
- Änderungsgrund -> `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Historie -> `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

Ältere Planungsstände bleiben Git-/Register-Historie und sind **nicht CURRENT**.

## AKTUELLER ARCHITEKTURENTSCHEID

V1 läuft als **eigenständige allgemeine Produktwissen-/Produktvergleichsstraße**.

Keine Laufzeitabhängigkeit von STARTMASTER/TEXT.

Hauptfluss:

`Produktwissen -> Produktvergleich -> gebundener Writer -> WordPress-DRAFT -> Link-/Grafikfinalisierung -> Affiliate Exact Match`

SEO liefert nur optionale read-only Signale.

## ZUSTÄNDIGKEITEN

### PRODUKTWISSEN
Single Writer für:
- eindeutige Produkt-/Variantenidentität;
- Hersteller-/Primärquellenfakten;
- Identifier;
- Quellenstatus/-konflikte;
- Lebenszyklus/Freshness.

### PRODUKTVERGLEICH
Single Writer für:
- Vergleichsauswahl und Vergleichstyp;
- 2–4 Produktpaarung/-gruppe;
- Variantenvergleich;
- Vergleichsmerkmale;
- Ruleset-/Artikelvertrag;
- Vergleichsartikel;
- QA;
- neutrale Grafik;
- internes Vergleichsarchiv;
- Produktvergleich <-> Variantenvergleich-Verlinkung;
- WordPress-DRAFT.

### SEO
Nur read-only Signale:
- Nachfrage/Priorisierung;
- Target Keyword;
- Kannibalisierungshinweise.

SEO darf keinen gebundenen Titel, Body, Ruleset oder Produktbestand überschreiben.

### AFFILIATE
Commerce-Autorität:
- Provider;
- Exact Match;
- Kaufangebote;
- Preis/Verfügbarkeit;
- Tracking/Disclosure/Produktkarten.

Affiliate darf Produktkandidaten melden, aber keine Produktfakten oder Vergleichspaarungen schreiben.

## TECHNISCH BEWIESENER V1-STAND

Branch:
`hobbyroom/productwissen-v1-prototype`

Geprüfter Head:
`109890eb7762bac276bc3f42be618e161b003f57`

Workflow:
`Product Knowledge WordPress DB Smoke` -> PASS.

Erster echter ZIP-Installationssmoke:
- Lauf `34136786494` -> PASS;
- saubere Plugin-ZIP-Struktur -> PASS;
- `universal-product-knowledge` per WordPress ZIP installiert + aktiviert -> PASS;
- `universal-product-comparison` danach installiert + aktiviert -> PASS;
- derselbe Real-WordPress/MySQL-Gesamtlauf -> PASS;
- Publish-Sperre bleibt PASS.

Finaler Branch nach Entfernen aller temporären Workflow-Dateien:
`38ae1137b5d90d64d28b3f02fc31b85f00ee8375`.

`Pferde Atelier Immutable Base Hardlock` -> PASS.

Belegt:
- Universal Product Knowledge WordPress/MySQL-Schema + Positiv-/Negativtests;
- Produkt- und Variantenvergleichsregeln;
- echtes Dossier `PV-REG-001`;
- Zero-Freedom-Writer mit gebundenem Ruleset;
- 100/100 byte-identische Writer-Ausgaben;
- WordPress-DRAFT-Materialisierung;
- keine Publish-Route;
- Affiliate-Brücke read-only und nur GTIN/EAN/echte MPN;
- SEO-Signale read-only;
- gemeinsames Vergleichsarchiv für Produktgruppen-, Produkt- und Variantenvergleiche;
- Produktnavigation/-suche ohne indexierbare Filter-URLs;
- deterministisches Link-Manifest und Link-Finalisierung;
- neutrale SVG-Vergleichsgrafik ohne Produktbilder/Logos/externe Assets;
- 20/20 byte-identische Grafik-Ausgaben;
- finaler WordPress-DRAFT mit exakt gebundenen internen Links + Grafik + Endhash;
- Wiederholungsfinalisierung byte-identisch;
- `publish_allowed=false`.

## FACHLICHE HARD RULES

- Produktvergleich = 2–4 konkrete konkurrierende Produkte aus mindestens zwei Herstellern.
- Variantenvergleich = Varianten desselben Basismodells.
- Produktgruppenvergleich bleibt fachlich getrennt.
- keine Rangliste, Sterne, Punkte oder pauschaler Testsieger.
- keine erfundenen Fakten.
- `NOT_IN_SOURCE`, `SOURCE_CONFLICT`, `CONFIGURATION_DEPENDENT` bleiben sichtbar.
- Affiliate-Verfügbarkeit verändert keine Produktwahrheit.
- kein Ersatzprodukt bei fehlendem Exact Match.
- Hersteller-Artikelnummer ist kein automatischer Affiliate-Exact-Match.
- interne Links nur aus gebundenem Manifest.
- Produktgrafik nur neutral/deterministisch; keine kopierten Hersteller-/Google-Produktfotos.
- kein Auto-Publish.

## SICHTBARES VERGLEICHSKONZEPT

Pro Produktgruppe eine sichtbare WordPress-Kategorie `Vergleich`.

Darin getrennte Beitragsarten:
- Produktgruppenvergleich;
- Produktvergleich;
- Variantenvergleich.

Archiv:
- Hauptfilter: Alle | Produktgruppenvergleiche | Produktvergleiche;
- Unterfilter: Produkte | Varianten;
- Produktnavigation nur für real vorhandene Vergleichsinhalte;
- Produktsuche umfasst Produkt- und Variantenvergleiche;
- mobil kompakte Suche/aufklappbare Navigation;
- keine zusätzliche Varianten-Kategorieebene.

## PRODUKTWISSEN- UND AFFILIATE-RICHTUNG

Hauptrichtung:

`Produktwissen -> Inhalt -> Affiliate Exact Match -> Kaufangebote`

Kurzform:

**Affiliate darf entdecken. Produktwissen entscheidet. Affiliate monetarisiert.**

## NÄCHSTER SCHRITT

Siehe ausschließlich `HOBBYRAUM.md`:
**manuellen WordPress-Test mit den bereits ZIP-geprüften Plugins durchführen.**
