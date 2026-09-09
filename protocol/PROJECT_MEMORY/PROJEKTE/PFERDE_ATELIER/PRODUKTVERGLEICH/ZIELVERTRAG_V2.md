# PRODUKTVERGLEICH – ZIELVERTRAG V2

STAND: 2026-09-09
STATUS: AKTIV

## Ziel

Produktvergleich erzeugt aus eindeutig gebundenem Produktwissen einen fachlich und technisch vollständig gebundenen **Vergleichsdossier-Output**.

Der fertige redaktionelle Produktvergleichsartikel wird anschließend durch den bestehenden SEO/TEXT-Fachworkflow erzeugt und über den bestehenden Produktions-Handoff/ACM-Weg bis zum WordPress-DRAFT geführt.

Pferde-Atelier ist die erste Projektkonfiguration; der Vergleichskern bleibt allgemeingültig.

## Verbindlicher Hauptfluss

`Produktwissen -> Vergleichbarkeit -> SEO-Nachfrage/Kannibalisierung -> gebundenes Vergleichsdossier -> SEO/TEXT-Fachworkflow -> bestehender FACHWORKFLOW_HANDOFF_REQUEST.json -> ACM -> signierter WordPress-DRAFT -> Readback/DOM -> STOP`

Affiliate liest separat exakte Produktidentitäten für aktuelle Kaufangebote.

Kein Auto-Publish.

## Zuständigkeiten

### PRODUKTVERGLEICH
Verantwortet:
- exakte Produkt-/Variantenidentität;
- Vergleichsdefinition;
- Vergleichbarkeit;
- gebundene Herstellerfakten/Quellenstatus;
- Vergleichsmerkmale;
- erlaubte Bedarfszuordnungen;
- verbotene/unbelegte Schlussfolgerungen;
- bidirektionale SEO-Eignung;
- Ruleset;
- gebundenes Vergleichsdossier;
- Vergleichs-QA bis zur Dossiergrenze.

PRODUKTVERGLEICH schreibt im Zielbetrieb **nicht** den fertigen Artikel und erzeugt keinen eigenen produktiven WordPress-DRAFT.

### SEO/TEXT
Verantwortet:
- Artikeltyp-Vertrag `Produktvergleich`;
- Aufbau/Abschnittsreihenfolge;
- Überschriften-/Tabellenvertrag;
- Sprache/Stil;
- SEO-Textproduktion;
- interne Links;
- LanguageTool;
- Dubletten/Kannibalisierung im bestehenden Fachworkflow;
- alle bestehenden allgemeinen Textmaschinen-/Qualitätsregeln.

### ACM
Orchestriert nur den bereits bestehenden gebundenen Produktionsweg.
Keine fachliche Entscheidungsfreiheit.

### AFFILIATE
Liefert separat:
- Angebot;
- Preis;
- Verfügbarkeit;
- Händler;
- Tracking.

Affiliate darf fachliche Produktwahrheit, Paarung oder Vergleichsaussage nicht verändern.

## Harte Fachregeln

- Produktvergleich: 2–4 konkrete konkurrierende Produkte aus mindestens zwei Herstellern.
- Variantenvergleich: Varianten desselben Basismodells.
- keine Rangliste, Sterne, Punkte oder pauschaler Testsieger.
- Quellenstatus wie `NOT_IN_SOURCE`, `SOURCE_CONFLICT`, `CONFIGURATION_DEPENDENT` bleiben sichtbar.
- kein ähnliches Ersatzprodukt bei fehlendem Exact Match.
- nur belegte Herstellerfakten.
- keine freie Produkterfindung.
- fehlende/abweichende Bindung -> BLOCKED.
- keine freie fachliche Schlussfolgerung außerhalb des Rulesets.
- SEO darf Produktidentitäten nicht erfinden.
- Affiliate-Verfügbarkeit ändert keine fachliche Wahrheit.
- kein Auto-Publish.

## Kosten-/Zwischenspeicherregel

Bereits bezahlte Produkt-/Paar-SEO-Evidenz wird innerhalb ihrer gültigen Hash-/Kontextbindung wiederverwendet.

Reihenfolge:
`persistente UPC-Zwischenevidenz -> PSTE-Cache -> nur fehlender Provider-Endpunkt`.

Manipulation -> BLOCK.
Ablauf/Kontextdrift -> frische Recherche.

## Schnittstellengrenze

Einzige Produktions-Eingangswahrheit bleibt der bestehende:

`FACHWORKFLOW_HANDOFF_REQUEST.json`

Kein zweites Handoff-Format.
Kein neues Jobmanifest.
Keine 17. Top-Level-Eigenschaft.

Der Produktvergleichskontext muss innerhalb der bereits bestehenden gebundenen Produktionskontexte untergebracht werden. Die exakte Zuordnung wird erst im SEO/TEXT-Büro gegen das reale Schema festgelegt und positiv/negativ getestet.

## Aktuelle Abnahmegrenze

Bereits belegt:
- Produktvergleich 0.8.2 lokal hart PASS;
- WordPress-Live-Wiederholung mit 0 Provider-Aufrufen / $0.0000 PASS;
- `NO_ELIGIBLE_COMPARISONS` bei 0 geeigneten Vergleichen korrekt;
- kein Auto-Publish.

Noch offen vor Gesamt-PASS:
1. restliche fachliche Artikeltyp-/Dossierregeln im PRODUKTVERGLEICH-Büro schließen;
2. ACM/SEO-TEXT-Nachbarweg vollständig hart freigeben;
3. Produktvergleichsdossier minimal in den bestehenden Handoff abbilden;
4. positiver/negativer Schnittstellentest;
5. ein vollständiger echter Produktvergleich bis signiertem WordPress-DRAFT + Readback;
6. Nutzerreview;
7. nichts automatisch veröffentlichen.

## Ablösung

Dieser Zielvertrag löst `ZIELVERTRAG_V1.md` ab.

WARUM:
V1 beschrieb die inzwischen verworfene eigene Produktvergleichs-Writer/Draft-Straße. Der verbindliche KISS-Zielweg trennt jetzt fachliches Vergleichsdossier und bestehende SEO/TEXT-Produktion, um keine zweite Textmaschine zu betreiben.
