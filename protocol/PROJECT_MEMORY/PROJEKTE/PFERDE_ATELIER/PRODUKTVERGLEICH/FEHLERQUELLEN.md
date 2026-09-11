# PRODUKTVERGLEICH – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-11
ROLLE: einzige detaillierte Fehlerquelle für den aktuellen PRODUKTVERGLEICH-Arbeitsweg.

## PV-ERR-001 – falsche WordPress-Kategoriehierarchie
STATUS: CLOSED

## PV-ERR-002 – historischer eigener Draftweg
STATUS: CLOSED / NICHT MEHR ZIELARCHITEKTUR

## PV-ERR-003 – falscher Hauptmenü-Positivtest
STATUS: CLOSED / ECHTER WP-LIFECYCLE ALS PFLICHT ERHALTEN

## PV-LIVE-001 – falsches PASS bei null geeigneten Vergleichen
STATUS: CLOSED / LIVE 0.8.1–0.8.4 BESTÄTIGT / REGRESSION AKTIV

## PV-ERR-004 – PASS ohne realen Dossier-Receipt
STATUS: CLOSED IM 0.8.1+ / REGRESSION AKTIV

## PV-COST-082-001 – bezahlte Produkt-/Paar-Zwischenergebnisse nicht dauerhaft genug gebunden
STATUS: CLOSED / LOKAL + WORDPRESS-LIVE 0.8.2–0.8.4 PASS

## PV-FACH-083-001 – Fachinterpretation nicht vollständig im Dossier gebunden
STATUS: CLOSED / 0.8.3 LOCAL HARD + WORDPRESS-LIVE-REGRESSION PASS

## PV-SCALE-084-001 – Proofgruppe statt vollständiger Vergleichsgruppen-Abdeckung
STATUS: INFRASTRUKTUR CLOSED / 0.8.4 LOCAL HARD + WORDPRESS-LIVE PASS / FACHLICHE 175-GRUPPEN-RECHERCHE WEITER OFFEN

0.8.4 bindet 175/175 Portalgruppen, vollständige Paar-Coverage ohne Top-N und Research-Vollständigkeit fail-closed `UNPROVEN`.

## PV-FAMILY-085-001 – Readiness zählte Herstellerbezeichnungen statt Herstellerfamilien
STATUS: CLOSED IM 0.8.5 / LOKAL HART PASS

KISS-Fix:
Eine Herstellerfamilien-Wahrheit für Research-Zählung, Inventar-Readiness, Paaruniversum und Planner.

Harter Beleg:
- Aesculap/Kerbl + Kerbl => 1 Familie;
- synthetischer echter zweiter Hersteller => erwartete Cross-Family-Paare;
- drei Mutationen korrekt ROT;
- finale 0.8.5-Regression 35/35 PASS.

## PV-FACH-085-002 – Fachprofile für vorhandene Mehrhersteller-Recherche
STATUS: PROFILE/POLICY LOCAL PASS / LIVE-INVENTAR NICHT MATERIALISIERT / MARKTVOLLSTÄNDIGKEIT UNPROVEN

Fachprofile/Policies sind lokal gegen freigegebene Recherchekandidaten geprüft für:
- Winterdecken;
- Übergangsdecken;
- Stalldecken;
- Unterdecken;
- Steigbügel.

Die daraus berechneten 130 Cross-Family-Paare sind **Katalogpotential nach erfolgreicher Materialisierung**, nicht bereits live vorhandene Paarzahl.

## PV-TEST-085-003 – Recherchekandidaten im Lokaltest als materialisiertes Inventar behandelt

STATUS: ROOT CAUSE GEFUNDEN / TESTGRENZE KORRIGIERT / UPK 0.5.1 LOCAL HARD PASS / WORDPRESS-MATERIALISIERUNG OFFEN

### Live-Befund

0.8.5 auf WordPress:
- `PAIRING_READY: 1`;
- `PROFILE_MISSING: 166`;
- `PRODUCT_INVENTORY_MISSING: 6`;
- 2 Key-Kollisionen;
- $0.0000 maximale neue Providerkosten.

Winterdecken:
- Research-Katalog 8 Kandidaten / 3 Hersteller;
- echtes Product-Knowledge-Inventar 0 / 0;
- Cross-Family-Paare 0;
- korrekt `PRODUCT_INVENTORY_MISSING`.

### Ursache

Der lokale 0.8.5-Fachtest materialisierte seine freigegebenen Research-Kandidaten **nur innerhalb des Tests** als Laufzeitprodukte, um Profile, Policies und Paarlogik zu prüfen.

Das bewies nicht, dass die Produkte bereits in der echten WordPress-Product-Knowledge-Datenbank importiert waren.

Die Release-Erwartung `PAIRING_READY: 6` war deshalb falsch.

### Wichtiger Gegenbeleg

Der Live-Produktvergleich selbst reagierte korrekt fail-closed:
- kein Produkt erfunden;
- kein Paar erfunden;
- kein SEO-/Providerlauf;
- $0.0000.

Damit ist dies primär eine **Test-/Freigabegrenzen-Lücke**, nicht ein fail-open Laufzeitfehler von UPC 0.8.5.

### KISS-Fix UPK 0.5.1

Kein neuer Importer.
Kein neues Datenmodell.
Kein Parallelweg.

0.5.1 ergänzt nur einen sequenziellen Batch-Aufruf über den bestehenden kanonischen Product-Knowledge-Weg:
`UPK_Research::run_product_group()`.

Pro vorhandener freigegebener Recherchegruppe:
1. echte Herstellerquelle neu prüfen;
2. nur PASS-Produkte/Fakten verwenden;
3. bestehenden Importpfad verwenden;
4. BLOCKED sichtbar lassen;
5. nächste Gruppe sequenziell;
6. Security-/Transportfehler stoppt fail-closed.

### Harter lokaler Beleg UPK 0.5.1

Finale ZIP:
`universal-product-knowledge-0.5.1-prototype.zip`

SHA-256:
`17ba686ebbfeac774de5224a042e8ea5fcc472b91774c47271e6b585d74960a1`

PASS:
- Batch Positiv/Negativ;
- Nonce/Capability;
- sequenzielle Verarbeitung;
- kanonischer `run_product_group()`-Pfad;
- 4 unabhängige Rückfallmutationen korrekt ROT;
- PHP-Lint 5/5;
- Source↔ZIP 8/8;
- Report-Hashes 7/7;
- keine SEO-/UPC-/Writer-/Publish-Autorität.

Gesamtgegenprüfung:
UPC 0.8.5 gegen exakt finale UPK-0.5.1-ZIP = **35/35 PASS**.

## Aktueller erster offener Arbeitsblock

WordPress-Live:
UPK 0.5.1 installieren -> Oberfläche/Batchbutton read-only prüfen -> danach einmal sequenziell materialisieren -> echte Ergebnisse auslesen.

Keine festen Produkt-/Paarzahlen vor dem echten Quellenlauf behaupten.
Research-Vollständigkeit bleibt `UNPROVEN`.
Kein Produktvergleich-Gesamtworkflow vor dieser Materialisierung.
Kein Writer/Draft/Publish.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
