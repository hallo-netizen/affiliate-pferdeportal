# PRODUKTVERGLEICH – CURRENT STATE

STAND: 2026-09-11
STATUS: AKTIV / 0.8.5 FINAL-FRESH-ZIP LOCAL HARD PASS / WORDPRESS-LIVE-RETEST OFFEN / 175-GRUPPEN-RECHERCHE WEITER OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Büro-Standzusammenfassung.

- aktuelle Arbeit: `HOBBYRAUM.md`
- Fehlerdetails: `FEHLERQUELLEN.md`
- Ziel: `ZIELVERTRAG_V2.md`
- Fachvertrag: `AKTENSCHRANK/05_FACH_DOSSIER_ARTIKELTYP_VERTRAG_V1.md`
- 0.8.4 Live-Beleg: `AKTENSCHRANK/10_V084_WORDPRESS_LIVE_RECEIPT.md`
- 0.8.5 lokaler Prüfbeleg: `AKTENSCHRANK/11_V085_HARD_LOCAL_RELEASE_RECEIPT.md`

## 0.8.5 KANDIDAT

`universal-product-comparison-0.8.5-prototype.zip`

SHA-256:
`0174051e6584902142f5be5787642426b30aab6c7ba15ef0b07ccbdb4a5844fd`

## WAS 0.8.5 FACHLICH ÖFFNET

Die 0.8.4-Registry bleibt vollständig erhalten. Zusätzlich werden aus der bereits vorhandenen, quellengebundenen Product-Knowledge-Recherche fünf weitere echte Mehrhersteller-Gruppen fachlich profiliert:

- Winterdecken: 20 echte Cross-Family-Paare;
- Übergangsdecken: 14;
- Stalldecken: 28;
- Unterdecken: 63;
- Steigbügel: 5.

Zusammen: **130 zusätzliche echte Cross-Family-Paare** neben der Regendecken-Proofgruppe.

Für jede Gruppe gilt weiterhin:
`gesamtes Paaruniversum -> Herstellerfamilie/Sinnprüfung -> nur fachlich zulässige Paare -> erst danach SEO`.

Keine Top-N-/Pair-Cap.
Keine freie fachliche Aussage.
Research-Vollständigkeit bleibt `UNPROVEN`.

## GEFUNDENER URSACHENFEHLER / FIX

`Aesculap/Kerbl` und `Kerbl` waren im alten Recherchekatalog als zwei Herstellerbezeichnungen sichtbar, gehören fachlich aber zur selben Herstellerfamilie.

Der Paarplaner behandelte sie bereits korrekt als eine Familie. Die 0.8.4-Readiness konnte dagegen rohe Herstellerbezeichnungen zählen und dadurch theoretisch falsch `PAIRING_READY` melden.

0.8.5 vereinheitlicht die Herstellerfamilien-Wahrheit:
- Readiness;
- Cross-Brand-Paaruniversum;
- Research-Kandidaten-Herstellerzahl;
- Paarplaner
verwenden dieselbe Herstellerfamilienlogik.

Folge für Schermaschinen:
- vorhandene 4 Produkte;
- `Aesculap/Kerbl` + `Kerbl` = **1 echte Herstellerfamilie**;
- 0 echte Cross-Family-Paare;
- Status muss `INSUFFICIENT_MANUFACTURERS` bleiben;
- erst ein vollständig gebundener echter zweiter Hersteller wie Lister darf diese Gruppe öffnen.

## HARTER LOKALBELEG 0.8.5

Finale Fresh-ZIP:
- 35/35 ausführbare Regressionen PASS;
- PHP-Lint 50/50 PASS;
- Source↔finale ZIP 71/71 exakt;
- Report-Hashbindung 70/70 exakt;
- 175/175 Portalregistry/-coverage unverändert PASS;
- 130/130 aktuelle echte Cross-Family-Paare der fünf neu aktivierten Gruppen erhalten;
- alle neuen Profilmerkmale gegen vorhandene Product-Knowledge-Fakten gebunden;
- Decision-Policies für alle aktuellen 130 Paare vollständig auflösbar;
- Quellenlimits erzeugen keine Präferenz/Bedarfszuordnung;
- Schermaschinen-Familienzählung negativ geprüft;
- synthetischer echter zweiter Hersteller öffnet exakt die erwarteten 4 Cross-Family-Paare;
- drei unabhängige Herstellerfamilien-Rückfallmutationen korrekt ROT;
- bestehende 0.8–0.8.4 Mutations-/Kosten-/SEO-/Dossier-/Auditregeln weiter PASS;
- SEO-Kostenbindung unverändert;
- kein Writer-/Draft-/Publishweg;
- kein Auto-Publish.

## 0.8.4 WORDPRESS-LIVE-BASIS

Weiter gültig:
- 175/175 Gruppen sichtbar;
- Regendecken Proofstand erhalten;
- 0 Provider-Aufrufe / $0.0000 beim identischen Wiederholungslauf;
- korrekt `NO_ELIGIBLE_COMPARISONS` bei 0 SEO-PASS.

## OFFENES GESAMTZIEL

0.8.5 nutzt mehr des bereits vorhandenen Produktwissens, beweist aber **nicht** Markt-Vollständigkeit.

Weiter offen:
1. WordPress-Live-Vorcheck 0.8.5 ohne Providerstart;
2. fehlende Hersteller/Modelle je Gruppe systematisch nachrecherchieren;
3. weitere gruppenspezifische Profile/Decision-Policies binden;
4. alle dadurch entstehenden sinnvollen A-vs-B-Paare vollständig prüfen;
5. Research-Vollständigkeit nur mit echtem Beleg hochstufen;
6. erster echter positiver Dossier-V2-Livefall;
7. später erst SEO/TEXT-/ACM-Anbindung.

Kein Publish.

NEXT ACTION ausschließlich `HOBBYRAUM.md`.
