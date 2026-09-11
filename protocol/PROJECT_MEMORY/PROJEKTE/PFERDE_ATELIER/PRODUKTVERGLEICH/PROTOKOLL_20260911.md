# PRODUKTVERGLEICH – ARBEITSPROTOKOLL 2026-09-11

ROLLE: chronologischer Ausführungs-/Testbeleg. Nicht CURRENT, nicht Zielvertrag, nicht Fehlerhauptquelle.

## 0.8.4 – 175er Infrastruktur

Gebaut/geprüft:
- autoritative 175/175 Vergleichsgruppenregistry aus Portalstruktur;
- jede Gruppe sichtbar mit Readiness/Coverage;
- keine Top-N-/Pair-Cap;
- Research-Kandidaten ≠ Markt vollständig;
- Sinn-/Nutzungsebenenprüfung vor SEO.

Harter lokaler Stand:
- 32/32 Tests PASS;
- 48/48 PHP-Lint PASS;
- Source↔ZIP 67/67;
- Report-Hashes 66/66.

WordPress-Live:
- 175/175 sichtbar;
- Regendecken Proofstand erhalten;
- identischer Wiederholungslauf 0 Provider / $0.0000;
- 8 BLOCKED / 0 Dossiers;
- korrekt `NO_ELIGIBLE_COMPARISONS`.

## 0.8.5 – Herstellerfamilien/Fachprofile

Gefundener Ursachenfehler:
Readiness konnte Herstellerlabels statt Herstellerfamilien zählen.

Fix:
Aesculap/Kerbl + Kerbl werden überall als eine Herstellerfamilie behandelt.

Harter lokaler Stand finaler ZIP:
- 35/35 Regression PASS;
- 50/50 PHP-Lint PASS;
- Source↔ZIP 71/71;
- Report-Hashes 70/70;
- drei Herstellerfamilien-Rückfallmutationen korrekt ROT.

Wichtige Testgrenze:
Die lokal berechneten 130 zusätzlichen Cross-Family-Paare waren Potentiale aus der freigegebenen Research-Basis nach synthetischer Testmaterialisierung, keine vorab belegten WordPress-Live-Paarzahlen.

## 0.8.5 WordPress – fail-closed Gegenbeweis

Nach Installation zeigte Winterdecken:
- Research-Katalog 8 Kandidaten / 3 Hersteller;
- echtes Product-Knowledge-Inventar zunächst 0 / 0;
- `PRODUCT_INVENTORY_MISSING`;
- 0 Paare;
- $0.0000 neue Providerkosten.

Bewertung:
UPC 0.8.5 war fail-closed korrekt; die Release-Erwartung war zu optimistisch.

Fehler-ID:
`PV-TEST-085-003`.

## Universal Product Knowledge 0.5.1

KISS-Fix:
Kein neuer Importer/kein neues Datenmodell.
Nur sequenzielle Batch-Orchestrierung über den vorhandenen kanonischen Weg:
`UPK_Research::run_product_group()`.

Finale Kandidaten-ZIP SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

Lokal geprüft:
- Positiv/Negativ PASS;
- Nonce/Capability PASS;
- Sequenz PASS;
- kanonischer Gruppenlauf PASS;
- 4 Mutationen korrekt ROT;
- PHP-Lint 5/5;
- Source↔ZIP 8/8;
- Report-Hashes 7/7;
- UPC 0.8.5 komplette Regression gegen exakt finale UPK-0.5.1-ZIP 35/35 PASS.

## UPK 0.5.1 WordPress-Live-Batch

Originaloberfläche:
- Hauptmenü `Produktwissen`;
- Seitentitel `Produktrecherche`;
- Bereich `Freigegebene Recherchebasis gesammelt materialisieren`.

Batch real abgeschlossen:
- 17/17 vorhandene Recherchegruppen;
- PASS 6;
- TEIL-PASS 8;
- BLOCKED 3;
- pairing-ready 9.

Aussagegrenze:
Die Alt-Recherchebasis umfasste nur 17 Gruppen / 102 Kandidaten. Der Lauf materialisierte diese Basis; er war keine 175-Gruppen-Marktrecherche.

Dauerbeleg:
`AKTENSCHRANK/23_UPK051_WORDPRESS_LIVE_BATCH_RECEIPT_20260911.md`.

## Zielkorrektur Skalierung

Verbindlich bestätigt:
- Regendecken war Proofgruppe, nicht Umfang;
- Ziel = 175 autoritative Vergleichsgruppen;
- je Gruppe möglichst viele reale relevante Hersteller/Modelle;
- alle fachlich zulässigen A-vs-B-Paare;
- blindes Kreuzprodukt verboten;
- Sinn-/Nutzungsebenenprüfung vor kostenpflichtigem SEO;
- keine künstliche Top-N-/Pair-Cap.

## Research-Arbeit A–J

Auf dem gleichen Hobbybranch wurden zehn Research-Evidence-Akten A–J gesichert:
`AKTENSCHRANK/13_...` bis `22_...`.

Jede Akte bleibt ausdrücklich:
Research Candidate Evidence / nicht Product Knowledge / nicht SEO-freigegeben / keine Markt-Vollständigkeit.

Dauerbeleg des damaligen Zwischenstands:
`AKTENSCHRANK/24_MARKTRECHERCHE_PROGRESS_A_J_20260911.md`.

## Nutzer-Hard-Rule zur Plugin-Übergabe

Verbindlich für Folgearbeit:
Keine Plugin-Übergabe ohne Beweis an der **exakt auszugebenden ZIP**:
- lokaler Positivtest;
- lokaler Negativ-/Mutationstest;
- Gegenprüfung gegen den gesamten aktuellen Produktvergleichsworkflow;
- Fresh-ZIP-/Hashbindung nach betroffenem Releaseweg.

Research-/Datenbatch erzeugt nicht automatisch eine neue Pluginversion.

## A–J-vs-175 Coverage-Checkpoint

Ausgangs-Head:
`95ccb7347fe4b655930da0d751845a8930754a5c`.

Autoritative Registry:
`affiliate-portal-router/assets/portal-structure-v279.json` mit exakt 175 eindeutigen `product_slug`-Identitäten und `theme = Vergleich`.

Source-bound Baseline + A–J:
- `EVIDENCE_PRESENT`: 70;
- `PARTIAL_AMBIGUOUS`: 57;
- `NO_GROUP_EVIDENCE`: 48;
- Summe 175/175.

Der vorher nur als Zwischenwert genannte Stand `129 / 52 / 77 / 46` wurde verworfen.

Dauerbeleg:
`AKTENSCHRANK/25_MARKTRECHERCHE_COVERAGE_175_A_J_20260911.md`.

Negativbefund:
Die sichtbare Bezeichnung `Weidezaungeräte` existiert mit zwei verschiedenen Registry-Keys. Keine stille Deduplizierung.

## Architekturentscheidung – Plugin ist finale Paarinstanz

Verbindlich festgelegt:
- Research/Product Knowledge liefert aktuellen Produktbestand/Fakten;
- SEO liefert Nachfrage-/A-vs-B-/Kannibalisierungssignale;
- die **letzte Paar-/Dossierentscheidung liegt im Produktvergleichs-Plugin**;
- neue, geänderte, ersetzte oder abgekündigte Produkte erzwingen wiederholbare Neubewertung aus aktuellem Product Knowledge;
- SEO darf keine fachlich unzulässige Paarung erzwingen;
- Research legt keine finalen Produktpärchen manuell fest.

WAS/WARUM dauerhaft gebunden in:
`AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`
und `ZIELVERTRAG_V2.md`.

## UPC 0.8.6 – Lifecycle-Neubewertung

Neuer realer technischer Fehler:
`PV-LIFECYCLE-086-001`.

Gegen unveränderte, exakt gebundene UPC-0.8.5-ZIP bewiesen:
Ein `DISCONTINUED`-Produkt blieb im Paaruniversum; Solltest ROT mit 3 statt 1 gültigem Paar und 3 statt 2 Herstellerfamilien.

KISS-Fix 0.8.6:
- `ACTIVE` pairable;
- `TEMPORARILY_UNAVAILABLE` pairable;
- `DISCONTINUED`, `UNKNOWN` und fehlender Lifecycle fail-closed ausgeschlossen;
- kanonische Deduplizierung vor Lifecycle-Gate.

Exakte 0.8.6-Fresh-ZIP SHA-256:
`6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

Tatsächlich ausgeführt:
- Working Tree Regression 38/38 PASS;
- zwei Lifecycle-Mutationen korrekt ROT;
- PHP-Lint 51/51 PASS;
- Source↔Fresh-ZIP 74/74 exakt;
- Report-Hashes 73/73 exakt;
- Fresh-ZIP Regression 38/38 PASS;
- Fresh-ZIP PHP-Lint 51/51 PASS.

Nicht ausgeführt:
- WordPress-Live für UPC 0.8.6.

Dauerbeleg:
`AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`.

## UPC 0.8.6 – Read-only Architektur-Audit

Ohne zweiten Codefix tatsächlich geprüft:
- Research-Evidence ohne materialisiertes Product Knowledge -> 0 Paare;
- Nicht-V1-/Service-/Knowledge-/Checklisten-Keys fail-closed;
- künstliches SEO-PASS überschreibt fachliches BLOCKED nicht;
- vorhandenes Dossier verliert READY, wenn aktuelles Product Knowledge das gebundene Produkt entfallen/abkündigen lässt;
- 1000-Pair-No-Cap-Regel bleibt PASS.

Dauerbeleg:
`AKTENSCHRANK/41_V086_READ_ONLY_ARCHITECTURE_AUDIT_RECEIPT.md`.

## Research-/Fachklärung K–Z und Folgeblöcke

Der 175er Lauf wurde ohne Plugin-Orgie weitergeführt:
- K–T schlossen alle zunächst völlig ungedeckten Registry-Gruppen;
- Partial-Ursachen wurden fail-closed klassifiziert statt blind weiter recherchiert;
- U–Z/W/X/Y/Z bearbeiteten echte Markt-, Zweithersteller-, Horse-Use- und Produktidentitätsgaps;
- Subtyp-/Nutzungsklassen wurden fachlich normalisiert;
- Registry-Overlap und Restidentitäten wurden geklärt;
- Service-/Knowledge-/Checklisten-/Nicht-V1-Fälle wurden bewusst fail-closed disponiert.

Finale 175er V1-Disposition:
- 150 `PRODUCT_EVIDENCE_PRESENT`;
- 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`;
- 0 `UNRESOLVED_COVERAGE`.

Dauerbeleg:
`AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`.

Das ist keine Markt-Vollständigkeit, keine Pairing-Ready-Zahl und kein SEO-PASS.

## Readiness-Baseline und Profilphase

Exakte UPC-0.8.6-Fresh-ZIP read-only geprüft:
- 175 Registry-Gruppen;
- nur 7 maschinenfeste Comparison Profiles/Decision Policies;
- damit 143 der 150 V1-fähigen Gruppen technisch noch ohne maschinenfestes Profil/Policy.

Dauerbeleg:
`AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`.

Danach source-bound Profilspezifikationen erzeugt, **noch nicht materialisiert**:
- Akte 62: `high-neck-decken`;
- Akte 63: `deckengurte`, `deckentaschen-und-aufbewahrung`;
- Akte 64: `stallhalfter`, `knotenhalfter`, `sicherheitshalfter`, `fohlenhalfter`.

Damit sind 7 zusätzliche fachliche Profilspecs vorbereitet; der maschinenfeste 0.8.6-Bestand bleibt technisch unverändert bei 7 Profilen.

Nächster Profilblock in Registry-Reihenfolge:
`pferdebuersten` -> `striegel` -> `kardaetschen`.

## Abschluss-/Nachholprüfung – frisch am Endzustand

Frisch gelesen/gegengeprüft:
- Campus `START_HERE.md`, `HAUPTPFOERTNER.md`, `HANDLUNGSVERZEICHNIS.md`;
- Pferde-Atelier `START_HERE.md`;
- Produktvergleich `START_HERE.md`, `CURRENT_STATE.md`, `HOBBYRAUM.md`, `FEHLERQUELLEN.md`, `ZIELVERTRAG_V2.md`;
- zentrale Fehler-/Ziel-/Änderungs-/Archivquellen;
- finale 175er Disposition und Readiness-Baseline;
- aktuelle Profilspecs 62–64;
- Produktvergleichsbranch frisch;
- ACM-Nachbarbranch read-only frisch;
- Paul-Verzeichnis: kein gebundener Produktvergleichs-Paul-Arbeitsweg gefunden.

Frischer Produktvergleichsbranch vor Nachholung:
`708750eae3726fb03c458630ea6d68c12efbe52a`.

Frischer ACM-Nachbarbranch:
`alternative/seo-text-central-machine-20260908`
Head `ba511c2caec5e970948cf8e5c0139bcfea017ce2`.
Nachbarbranch nicht verändert.

Gefundene Nachholpunkte und jetzt korrigiert:
- `FEHLERQUELLEN.md` enthielt alten 97/78/0-Scale-Stand und einen bereits erledigten Architektur-Audit als NEXT;
- zentrales `FEHLERREGISTER.md` enthielt dynamische/stale Produktvergleichs-Fachstände statt nur Wegweiser;
- `CURRENT_STATE.md` und `HOBBYRAUM.md` waren hinter den bereits angelegten Profilspecs 62–64 zurück;
- dieses Tagesprotokoll endete noch beim alten Deckengurte-Research-Gap.

Zielvertrag:
Keine Zieländerung erforderlich. V2 ist weiterhin aktiv und enthält bereits finale Plugin-Autorität + regelmäßige Neubewertung. Zielregister bleibt Wegweiser.

WARUM/Entscheidung:
Die dauerhafte Entscheidung zur finalen Plugin-Autorität ist source-bound in Akte 31 und im aktiven V2-Zielvertrag enthalten. Kein zweiter konkurrierender Entscheidungsstand angelegt.

Archiv:
Keine aktive/ungeklärte Produktvergleichsarbeit archiviert. Keine Archivänderung erforderlich.

Campus-/Architekturfolge:
Die Regel betrifft den allgemeinen Produktvergleichskern bereits über Geltungsbereich von ZV-PV-002; kein zusätzlicher Campus-Neubau-/Bürostandard erforderlich.

Tests im Abschlusscheck:
Keine neuen Codeänderungen und daher kein neuer technischer Testlauf ausgelöst. Es gelten nur die oben tatsächlich ausgeführten 0.8.6-Hardtests. WordPress-Live 0.8.6 bleibt offen.

Kein Merge.
Kein Publish.
