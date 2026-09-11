# PRODUKTVERGLEICH – ZIELVERTRAG V2

STAND: 2026-09-11
STATUS: AKTIV

## Ziel

PRODUKTVERGLEICH erzeugt für **alle relevanten Pferde-Atelier-Produktgruppen mit eigener Vergleichskategorie** aus eindeutig gebundenem Produktwissen fachlich und technisch vollständig gebundene A-vs-B-Vergleichsdossiers.

Autoritative Portalbasis:
- 329 Produktseiten;
- 1124 Artikelkategorien;
- **175 eindeutige Produktgruppen mit `theme = Vergleich`**.

Regendecken ist nur die erste Proofgruppe, nicht der Zielumfang.

## Verbindlicher Gesamtfluss

`alle Vergleichsgruppen -> möglichst vollständiges Produktwissen je Gruppe -> alle fachlich zulässigen A-vs-B-Paare -> SEO-Nachfrage/Kannibalisierung -> gebundene Fachpolicy -> Vergleichsdossier V2 -> später SEO/TEXT -> bestehender Handoff -> ACM -> signierter WordPress-DRAFT -> STOP`

Kein Auto-Publish.

## Vollständigkeitsvertrag

Für jede autoritative Vergleichsgruppe muss ein expliziter Status existieren.
Keine Gruppe darf still fehlen.

READY erst wenn:
- Produktgruppenidentität portalgebunden;
- Produktinventar ausreichend/aktuell recherchiert;
- Vergleichsprofil vollständig;
- Decision-Policy vollständig;
- erforderliche Produktfakten gebunden.

Andere Zustände müssen sichtbar sein, z. B.:
- `PROFILE_MISSING`;
- `POLICY_MISSING`;
- `PRODUCT_INVENTORY_MISSING`;
- `RESEARCH_INCOMPLETE`;
- `BLOCKED`.

## Kandidatenabdeckung

Pro READY-Gruppe:
- PRODUCT_COMPARISON V1 = exakt 2 Produkte, A gegen B;
- mindestens zwei Herstellerfamilien;
- gleiche Produktgruppe/Nutzungsebene;
- alle fachlich zulässigen Cross-Brand-Paare werden erzeugt;
- Same Brand/Same Family/incompatible Profile werden vor kostenpflichtigem SEO ausgeschlossen;
- keine willkürliche Top-N-/Pair-/Group-Grenze;
- technische Batchverarbeitung ist zulässig, darf Coverage aber nicht reduzieren;
- Resume muss vollständig/idempotent sein.

Coverage muss pro Gruppe und global nachweisen:
- bekannte Produkte;
- Herstellerfamilien;
- mathematisches Paaruniversum;
- fachlich zulässige Kandidaten;
- terminal geprüfte Paare;
- offene Paare;
- BLOCKED nach Grund;
- SEO-PASS;
- Dossiers;
- neue Providerkosten.

## Research-/Product-Knowledge-Grenze

Research-Evidence ist **nicht** automatisch Product Knowledge.

Vor Übernahme zwingend:
- exakte Produktidentität;
- belastbare Herstellerquelle;
- gruppenspezifische gemeinsame Faktenmatrix;
- Nutzungsebene/Sinnprüfung;
- Quellen-/Konfliktstatus.

Markt-Vollständigkeit darf nie aus bloßer Kandidatenzahl oder einem Importlauf abgeleitet werden.

Research darf in großen Datenblöcken gesammelt werden. Es ist **kein** eigener Plugin-Release pro Produktgruppe oder Research-Batch erforderlich.

## Zuständigkeiten

### PRODUKTVERGLEICH
Verantwortet:
- vollständige Gruppenregistry;
- Produkt-/Variantenidentität;
- Vergleichbarkeit;
- Herstellerfakten/Quellenstatus;
- Vergleichsprofile;
- Decision-Policies;
- alle fachlich zulässigen A-vs-B-Kandidaten;
- bidirektionale SEO-Eignung;
- Coverage-Nachweis;
- Dossier V2.

PRODUKTVERGLEICH schreibt keinen fertigen Produktionsartikel.

### SEO/TEXT
Verantwortet später Sprache, Struktur, Tabellen, Links, LanguageTool und eigentliche Textproduktion. Es darf keine fachliche Produktbedeutung erfinden.

### ACM
Orchestriert nur den gebundenen bestehenden Produktionsweg.

### AFFILIATE
Liefert separat Angebot, Preis, Verfügbarkeit, Händler und Tracking. Commerce darf Fachauswahl/Fazit nicht verändern.

## Fachregeln je Artikel

- exakt zwei gebundene Produkte;
- keine Rangliste/Punkte/Sterne/pauschaler Testsieger;
- Quellenlücken erzeugen keine Präferenz;
- kein ähnliches Ersatzprodukt;
- nur belegte Herstellerfakten;
- keine freie Schlussfolgerung außerhalb der Decision-Policy;
- technische Andersartigkeit ist nicht automatisch Vorteil/Nachteil;
- fehlende/abweichende Bindung -> BLOCKED.

## Dossier

Vertrag:
`UPC_BOUND_COMPARISON_DOSSIER_V2`

Gebunden werden u. a.:
- beide Produktidentitäten;
- Fakten/Quellenstatus;
- SEO-Evidenz;
- Zielkeyword;
- Readiness/Kannibalisierung;
- Decision-Policy-Hash;
- erlaubte Aussagearten;
- Verbote;
- feste Need-Codes;
- Abschluss-Audit.

Keine Prosa aus PRODUKTVERGLEICH.

## Kostenregel

`persistente UPC-Zwischenevidenz -> PSTE-Cache -> nur fehlender Provider-Endpunkt`.

Bereits gültig bezahlte Produkt-/Paar-Evidenz wird wiederverwendet.
Reine Fachpolicy-Änderung darf unveränderte SEO-Evidenz nicht neu kaufen.

## Plugin-/Freigaberegel

Research-/Datenarbeit löst nicht automatisch eine neue Pluginversion aus.

Wenn eine technische Änderung tatsächlich nötig wird, darf ein Plugin erst an den Nutzer übergeben werden, wenn die **exakt auszugebende ZIP** belegt hat:
- lokalen Positivtest;
- lokalen Negativ-/Mutationstest;
- Gegenprüfung gegen den gesamten aktuellen Produktvergleichsworkflow;
- Fresh-ZIP-/Hashbindung entsprechend dem betroffenen Releaseweg.

Kein PASS nur aus Codeansicht.

## Schnittstellengrenze

Spätere einzige Produktions-Eingangswahrheit bleibt:
`FACHWORKFLOW_HANDOFF_REQUEST.json`

Kein neues Handoff, kein neues Jobmanifest, keine 17. Top-Level-Eigenschaft, keine zweite Textmaschine.

## Abnahmebedingungen

Gesamtfreigabe erst wenn:
1. 175/175 Vergleichsgruppen ohne stille Lücke geführt werden;
2. Markt-/Produktrecherche je Gruppe belastbar genug oder explizit offen/blockiert ist;
3. Profile/Policies je READY-Gruppe vollständig gebunden sind;
4. alle fachlich zulässigen Paare je READY-Gruppe vollständig abgedeckt sind;
5. globale Coverage-/Resume-/Idempotenzprüfung PASS ist;
6. Kosten-/SEO-/Dossier-/Audit-Schutzregeln PASS bleiben;
7. mindestens ein echter positiver Dossier-V2-Livefall vorliegt;
8. spätere SEO/TEXT-/ACM-Anbindung separat im zuständigen Nachbarweg freigegeben und positiv/negativ geprüft ist;
9. kein Auto-Publish entsteht.

**Dynamischer Fortschritt gehört ausschließlich in `CURRENT_STATE.md` und `HOBBYRAUM.md`, nicht in diesen Zielvertrag.**

## Ablösung

`ZIELVERTRAG_V1.md` bleibt abgelöst.
