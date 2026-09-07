# PRODUKTVERGLEICH – ZIELVERTRAG V1

STAND: 2026-09-07
STATUS: AKTIV

## Ziel

Eine eigenständige, allgemeingültige Produktvergleichsstraße erzeugt aus eindeutig gebundenem Produktwissen reproduzierbare Produkt- und Variantenvergleichsartikel als WordPress-DRAFT.

Pferde-Atelier ist erste Projektkonfiguration, nicht Teil des allgemeinen Kerns.

## Verbindlicher Hauptfluss

`Produktwissen -> Vergleichsdefinition -> gebundenes Dossier -> Zero-Freedom-Renderer -> Validator -> WordPress-DRAFT -> interne Linkbindung -> neutrale Vergleichsgrafik -> finaler Draft-Hash`

Affiliate liest danach exakte Produktidentitäten für aktuelle Kaufangebote.
SEO darf ausschließlich read-only Signale liefern.

## Oberste Writer-Regel

**Der Produktions-Writer hat null freie Autorität.**

Gleicher gebundener Input + gleiche Vertrags-/Renderer-Version = byte-identischer Output.

Verboten:
- freie Recherche im Writer;
- erfundene oder ergänzte Fakten;
- freie Bewertung;
- freie Produktauswahl;
- freie Struktur;
- freie Formulierungsvariation;
- freie Fallbacks;
- freier Publishweg.

Fehlende oder widersprüchliche Bindung -> BLOCKED.

## Fachliche Regeln

- Produktvergleich: 2–4 konkrete konkurrierende Produkte aus mindestens zwei Herstellern.
- Variantenvergleich: Varianten desselben Basismodells.
- keine Rangliste, Sterne, Punkte oder pauschaler Testsieger.
- Quellenstatus wie `NOT_IN_SOURCE`, `SOURCE_CONFLICT`, `CONFIGURATION_DEPENDENT` bleiben sichtbar.
- Affiliate-Verfügbarkeit ändert keine fachliche Produktwahrheit.
- kein ähnliches Ersatzprodukt bei fehlendem Exact Match.
- interne Links nur aus gebundener Relation.
- Vergleichsgrafik neutral/deterministisch; keine kopierten Hersteller-/Google-Produktfotos.
- kein Auto-Publish.

## V1-Grenzen

- keine Laufzeitabhängigkeit von STARTMASTER/TEXT;
- bestehendes TEXT-System wird nicht verändert;
- Produktwissen ist Single Writer für Produkt-/Variantenidentität und Herstellerfakten;
- Produktvergleich ist Single Writer für Vergleichsdefinition, Ruleset, Vergleichsartikel, QA, Grafik, Archiv und Draft;
- Affiliate bleibt Commerce-Schicht;
- SEO bleibt read-only Signalquelle.

## Aktuelle Abnahmegrenze

Technischer 0.2.4-Kandidat ist im echten WordPress-Admin-Lifecycle und im gebundenen `PV-REG-001`-Drafttest PASS.

V1 ist **noch nicht LIVE-abgenommen**, solange 0.2.4 auf der echten Pferde-Atelier-Seite nicht manuell bestätigt wurde.

Nächste Abnahme:
1. 0.2.4 auf der echten Seite installieren/ersetzen;
2. Hauptmenü `Produktvergleich` sichtbar bestätigen;
3. `PV-REG-001 als Draft testen`;
4. erzeugten Draft fachlich/visuell prüfen;
5. nichts veröffentlichen.
