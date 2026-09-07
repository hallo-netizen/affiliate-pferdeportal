# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-07
STATUS: V1-PROTOTYP / 0.2.2 GEBUNDENER ERSTDRAFT + CLEAN-ZIP PASS / MANUELLER TEST BEREIT

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

Erster ZIP-Installationssmoke des 0.2.0-Standes war technisch PASS, danach wurde jedoch bei der realen Pferde-Atelier-Bindung eine falsche Taxonomie-Annahme entdeckt: die vorhandenen redaktionellen Vergleichskategorien sind technisch flach (`parent=0`).

Korrigierter Kandidat:
- Universal Product Comparison `0.2.1-prototype`;
- erster gebundener Live-Term: ID `11`, Name `Vergleich Regendecken`, Slug `pferdedecken-regendecken-vergleich`, Parent `0`;
- kein Auto-Anlegen dieser bestehenden Live-Kategorie;
- ID/Name/Slug/Parent müssen exakt stimmen, sonst BLOCKED.

Harter korrigierter ZIP-/WordPress-/MySQL-Lauf:
- Run `34141063395` -> PASS;
- Zero-Freedom Static Guard -> PASS;
- saubere ZIP-Struktur -> PASS;
- ZIP-Installation/Aktivierung -> PASS;
- reale Pferde-Atelier-Regendecken-Konfiguration -> PASS;
- flache Kategorie -> PASS;
- absichtlich falscher Parent -> korrekt BLOCKED;
- vollständige bisherige Regression -> PASS.

Bereinigter Branch nach Entfernen des temporären Workflows:
`89651722cae1fd2c60ddc8a9d288a3d17e71e105`.

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
**Produktvergleich 0.2.1 -> 0.2.2 ersetzen und danach ausschließlich den gebundenen PV-REG-001-Admin-Drafttest ausführen; Produktwissen 0.1.0 unverändert lassen.**


## 0.2.2 – ERSTER GEBUNDENER LIVE-DRAFT TECHNISCH PASS

Stand 2026-09-07.

Neu:
- hashgebundenes PV-REG-001-Dossier;
- transaktionaler/idempotenter Erstimport;
- Admin-Test ohne freie Eingaben;
- feste Reihenfolge Import -> WordPress-DRAFT -> Link-/Grafikfinalisierung;
- keine Publish-Route.

Clean-ZIP-Beleg:
- Run `34142790804` PASS;
- kein `config/test-project` im Benutzerpaket;
- ZIP-Installation/Aktivierung PASS;
- bestehende Regression PASS;
- frische DB: 2 Produkte / 28 Fakten / 1 Vergleich / 14 Merkmale PASS;
- Wiederholungsimport ohne Dubletten PASS;
- reale Kategorie Term-ID 11 PASS;
- finaler WordPress-Draft PASS;
- `publish_allowed=false`;
- Endmarker `UPC_BOUND_LIVE_PV_REG_001_GESAMT_PASS`.

Freigegebene Produktvergleichsversion:
`0.2.2-prototype`.

Produktwissen bleibt:
`0.1.0-prototype`.
