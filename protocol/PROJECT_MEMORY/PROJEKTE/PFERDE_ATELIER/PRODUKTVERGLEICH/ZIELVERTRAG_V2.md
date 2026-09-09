# PRODUKTVERGLEICH – ZIELVERTRAG V2

STAND: 2026-09-09
STATUS: AKTIV

## Ziel

PRODUKTVERGLEICH erzeugt aus eindeutig gebundenem Produktwissen einen fachlich und technisch vollständig gebundenen **A-vs-B-Vergleichsdossier-Output**.

Der fertige redaktionelle Artikel wird später durch den bestehenden SEO/TEXT-Fachworkflow erzeugt und über den bestehenden Produktions-Handoff/ACM-Weg bis zum WordPress-DRAFT geführt.

Pferde-Atelier ist die erste Projektkonfiguration; der Vergleichskern bleibt allgemeingültig.

## Verbindlicher Hauptfluss

`Produktwissen -> Vergleichbarkeit -> SEO-Nachfrage/Kannibalisierung -> gebundene Fachpolicy -> Vergleichsdossier V2 -> SEO/TEXT-Fachworkflow -> bestehender FACHWORKFLOW_HANDOFF_REQUEST.json -> ACM -> signierter WordPress-DRAFT -> Readback/DOM -> STOP`

Affiliate liest separat exakte Produktidentitäten für aktuelle Kaufangebote.

Kein Auto-Publish.

## Aktiver Artikeltyp-Scope

### PRODUCT_COMPARISON V1
- exakt **2 konkrete Produkte**;
- A gegen B;
- mindestens zwei Hersteller;
- gleiche Produktgruppe;
- gleiche fachliche Nutzungsebene;
- keine künstliche Paarung wegen Affiliate-Verfügbarkeit.

### Nicht Teil dieses aktiven Vertrags
- 3–4-Produkte-Gruppenvergleich;
- Variantenvergleich als eigener Artikeltyp.

Diese können später separat gebunden werden, dürfen aber nicht still die A-vs-B-Regeln erweitern.

## Zuständigkeiten

### PRODUKTVERGLEICH
Verantwortet:
- exakte Produktidentität;
- Vergleichsdefinition;
- Vergleichbarkeit;
- gebundene Herstellerfakten/Quellenstatus;
- Vergleichsmerkmale;
- gebundene Decision-Policy;
- erlaubte Aussagearten;
- feste Bedarfs-Codes;
- verbotene/unbelegte Schlussfolgerungen;
- bidirektionale SEO-Eignung;
- gebundenes Vergleichsdossier;
- Vergleichs-QA bis zur Dossiergrenze.

PRODUKTVERGLEICH schreibt im Zielbetrieb **nicht** den fertigen Artikel und erzeugt keinen eigenen produktiven WordPress-DRAFT.

### SEO/TEXT
Verantwortet später:
- Artikeltyp-Textvertrag `Produktvergleich`;
- Aufbau/Abschnittsreihenfolge;
- Überschriften-/Tabellenvertrag;
- Sprache/Stil;
- SEO-Textproduktion;
- interne Links;
- LanguageTool;
- allgemeine bestehende Qualitätsregeln.

SEO/TEXT darf keine fachliche Produktbedeutung ergänzen, die im Dossier nicht gebunden ist.

### ACM
Orchestriert nur den bestehenden gebundenen Produktionsweg.
Keine fachliche Entscheidungsfreiheit.

### AFFILIATE
Liefert separat:
- Angebot;
- Preis;
- Verfügbarkeit;
- Händler;
- Tracking.

Affiliate darf Produktwahrheit, Paarung oder Vergleichsaussage nicht verändern.

## Harte Fachregeln

- exakt zwei gebundene Produkte;
- keine Rangliste, Sterne, Punkte oder pauschaler Testsieger;
- Quellenstatus wie `NOT_IN_SOURCE`, `SOURCE_CONFLICT`, `CONFIGURATION_DEPENDENT` bleiben fachlich wirksam;
- Quellenlimit erzeugt keine Präferenz;
- kein ähnliches Ersatzprodukt;
- nur belegte Herstellerfakten;
- keine freie Produkterfindung;
- keine freie fachliche Schlussfolgerung außerhalb der Decision-Policy;
- technische Andersartigkeit ist nicht automatisch Vorteil/Nachteil;
- SEO darf Produktidentitäten nicht erfinden;
- Affiliate-Verfügbarkeit ändert keine fachliche Wahrheit;
- fehlende/abweichende Bindung -> BLOCKED;
- kein Auto-Publish.

## Decision-Policy / Dossier V2

Dossier-Vertrag:
`UPC_BOUND_COMPARISON_DOSSIER_V2`

Gebunden werden:
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

Fachvertrag:
`AKTENSCHRANK/05_FACH_DOSSIER_ARTIKELTYP_VERTRAG_V1.md`

## Kosten-/Zwischenspeicherregel

Bereits bezahlte Produkt-/Paar-SEO-Evidenz wird innerhalb ihrer gültigen Hash-/Kontextbindung wiederverwendet.

Reihenfolge:
`persistente UPC-Zwischenevidenz -> PSTE-Cache -> nur fehlender Provider-Endpunkt`.

Decision-Policy besitzt eine getrennte Bindung.
Eine reine Fachpolicy-Änderung:
- erzwingt Dossier-Neuprüfung;
- darf unveränderte bezahlte SEO-Evidenz nicht erneut kaufen.

0.8.2/0.8.3 echter Laufzeit-SEO-Binding-Hash:
`863a724d9f349770d9f62c7c65ee7c74565d4247f9bf15504984ae4ece2c9003`

Manipulation -> BLOCK.
Ablauf/echte Kontextdrift -> frische Recherche.

## Schnittstellengrenze

Einzige spätere Produktions-Eingangswahrheit bleibt:

`FACHWORKFLOW_HANDOFF_REQUEST.json`

Kein zweites Handoff-Format.
Kein neues Jobmanifest.
Keine 17. Top-Level-Eigenschaft.

Die exakte Dossier-Abbildung in bestehende Produktionskontexte wird ausschließlich im SEO/TEXT-Büro gegen das reale Schema festgelegt und positiv/negativ getestet.

## Aktuelle Abnahmegrenze

Im PRODUKTVERGLEICH-Büro bereits belegt:
- 0.8.2 WordPress-Live-Kostenwiederholung PASS;
- 0.8.3 finale Fresh-ZIP lokal hart PASS;
- 25/25 Tests;
- 43/43 PHP-Lint;
- 11 reale herstellerübergreifende UPK-Regendecken-Paare;
- Decision-Policy/Dossier V2 fail-closed;
- Fachvertrag geschlossen;
- kein Auto-Publish.

Noch offen:
1. 0.8.3 WordPress-Live-Retest auf unverändertem Bestand;
2. positiver Dossier-V2-Livefall erst bei realem SEO-geeignetem A-vs-B-Paar;
3. ACM/SEO-TEXT-Nachbarweg vollständig hart freigeben;
4. danach read-only Übergabevertrag im Nachbarbüro prüfen lassen;
5. minimale Dossier-Abbildung in bestehenden Handoff;
6. positiver/negativer Schnittstellentest;
7. ein vollständiger echter Produktvergleich bis signiertem WordPress-DRAFT + Readback;
8. Nutzerreview;
9. kein Auto-Publish.

## Ablösung

Dieser Zielvertrag löst `ZIELVERTRAG_V1.md` ab.

WARUM:
V1 beschrieb die verworfene eigene Produktvergleichs-Writer/Draft-Straße. V2 trennt Fach-Dossier und bestehende Textproduktion und verhindert damit eine zweite Textmaschine.
