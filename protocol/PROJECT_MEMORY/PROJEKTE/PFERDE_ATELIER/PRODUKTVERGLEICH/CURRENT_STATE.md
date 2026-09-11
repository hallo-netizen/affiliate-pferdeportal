# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / UPC 0.8.5 WORDPRESS-LIVE FAIL-CLOSED PASS / UPC 0.8.6 LOCAL HARD + FRESH-ZIP + READ-ONLY ARCHITEKTURAUDIT PASS, LIVE OFFEN / 175ER FACHDISPOSITION 150 V1-PRODUKTGRUPPEN + 25 V1-NOT-APPLICABLE + 0 UNGEKLÄRT / READINESS-PROFILPHASE AKTIV

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- finale Paar-/Refresh-Autorität: `AKTENSCHRANK/31_ARCHITEKTURENTSCHEIDUNG_PLUGIN_FINAL_AUTHORITY_20260911.md`
- finale 175er V1-Disposition: `AKTENSCHRANK/60_FINAL_COVERAGE_DISPOSITION_175_V1_20260911.md`
- Readiness-Baseline: `AKTENSCHRANK/61_READINESS_BASELINE_V1_150_20260911.md`
- aktuelle source-bound Profilspecs: `AKTENSCHRANK/62_...` bis `78_...`
- UPC-0.8.6 Lifecycle-Hardbeleg: `AKTENSCHRANK/39_V086_LIFECYCLE_REEVALUATION_HARD_LOCAL_RECEIPT.md`
- UPC-0.8.6 Read-only Architektur-Audit: `AKTENSCHRANK/41_V086_READ_ONLY_ARCHITECTURE_AUDIT_RECEIPT.md`

## TECHNISCHER STAND

Letzter WordPress-Live-Stand:
`UPC 0.8.5-prototype`
SHA-256 `0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

Aktueller lokal hart geprüfter Kandidat:
`UPC 0.8.6-prototype`
SHA-256 `6ad160d18fb0973463c214de4356447923cbb728e222725e5407868e580c24f6`

0.8.6 belegt:
- Lifecycle-Gap geschlossen;
- 38/38 Regression PASS;
- 51/51 PHP-Lint PASS;
- Source↔Fresh-ZIP 74/74 exakt;
- Report-Hashes 73/73 exakt;
- 175/175 Portalparität PASS;
- 1000-Pair-No-Cap PASS;
- Research ohne Product Knowledge -> 0 Paare;
- Nicht-V1-Gruppen fail-closed;
- SEO kann fachliches BLOCKED nicht überschreiben;
- Dossier-Neuaudit bei Produktentfall fail-closed.

**WordPress-Live für 0.8.6 wurde noch nicht ausgeführt.**

UPK 0.5.1 bleibt gebunden:
SHA-256 `17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

## 175ER FACHDISPOSITION

- `PRODUCT_EVIDENCE_PRESENT`: **150**
- `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`: **25**
- `UNRESOLVED_COVERAGE`: **0**
- Summe: 175/175.

Die 25 V1-NOT-APPLICABLE-Keys bleiben fail-closed und erzeugen kein Produktpaar.

## READINESS-GAP

Exakter technischer UPC-0.8.6-Stand:
- 175 Registry-Gruppen;
- **7 maschinenfeste** Vergleichsprofile/Decision-Policies;
- **143/150 V1-fähige Gruppen technisch noch offen**.

Seit der Readiness-Baseline wurden source-bound, aber **nicht materialisiert**, zusätzliche Profilspezifikationen für **49 Gruppen** erstellt.

Aktenübersicht:
- 62: High-Neck-Decken;
- 63: Deckenzubehör;
- 64: Halfter;
- 65: Pferdebürsten / Striegel / Kardätschen;
- 66: Satteldecken / Schabracken / Sattelgurte;
- 67: Sattelschränke / Satteltransport / Englische Trensen;
- 68: Gebisse / gebisslose Zäumungen / Zügel;
- 69: Sperrriemen / Reithalfter;
- 70: Liegeflächen / Offenstall-Bodenbefestigung / Fressständer;
- 71: Trennwände / Stalldokumente / Futtertafeln;
- 72: Werkzeughalter / Namensschilder / Stalltafeln;
- 73: Whiteboards / Hoftraktoren / Hoflader-Zubehör;
- 74: Hofbesen / Hofabsperrungen / Rampen;
- 75: Hofbeleuchtung / Stallbeleuchtung / Frostwächter;
- 76: Lüfter / Zeitschaltuhren / Kameras;
- 77: Mobile Unterstände / Windschutz / Dachrinnen;
- 78: Unterstand-Beleuchtung / Boxentüren / Boxenriegel / Boxengitter.

Wichtige Fail-closed-Bindungen der jüngsten Akte 78:
- Unterstand-Beleuchtung = off-grid Solar-System mit separatem Panel; nicht Hof-/Stallbeleuchtung über Standort umbenennen;
- Boxentüren = eigenständige einflügelige Schiebetürklasse; keine komplette Boxenfront;
- Boxenriegel = eigenständiger Doppelhubriegel; aktuell nur eine unabhängige Einzelproduktfamilie -> 0 Cross-Brand-Paare;
- Boxengitter = Pflicht-Subtyp; 500x500-Gittereinsatz und großes Aufsatzgitter sind unterschiedliche Klassen -> 0 Paar.

Diese 49 Specs ändern den technischen Profilbestand nicht.

## AKTUELLER ARBEITSBLOCK

Registry nach `boxengitter` frisch direkt aus der Portalstruktur gelesen:
- `boxenmatten`;
- `krippen-fuer-pferdeboxen`;
- `lecksteinhalter-fuer-boxen`.

Nächster Profilblock:
`boxenmatten` -> `krippen-fuer-pferdeboxen` -> `lecksteinhalter-fuer-boxen`.

Vor Pairing hart zu normalisieren:
- Boxenmatten: Stall-/Boxen-Liegematte nach Material, Stärke, Verlege-/Verbindungsart; nicht Bodenraster oder Offenstall-Liegefläche nur über Standort duplizieren;
- Krippen: konkrete Futterkrippen-/Trogklasse, Material, Volumen und Montage; keine Heuraufe oder Tränke;
- Lecksteinhalter: gleiche Halterklasse, Lecksteinform/-größe und Montage; keine Leckschale oder kompletter Mineralleckstein.

Arbeitsweise:
source-bound Faktenmatrix -> Nutzungsklasse/Pairing-Regeln -> Decision-Policy -> Produktgegenprüfung -> in sinnvollen Blöcken sammeln -> erst dann technische Materialisierung -> kompletter Positiv-/Negativ-/Mutation-/Fresh-ZIP-Test.

Finale konkrete Paarentscheidung bleibt ausschließlich beim Produktvergleichs-Plugin und muss aus aktuellem Product Knowledge regelmäßig neu bewertet werden.

Kein SEO vor fachlich zulässigem Kandidatenuniversum.
Kein Merge.
Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
