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
STATUS: INFRASTRUKTUR CLOSED / FACHLICHE 175-GRUPPEN-MARKTRECHERCHE AKTIV OFFEN

Geschlossen:
- 175/175 Portalgruppen in Registry;
- jede Gruppe sichtbar;
- keine stille Top-N-/Pair-Cap;
- Research-Vollständigkeit fail-closed `UNPROVEN`;
- WordPress-Live 0.8.4 PASS.

Weiter offen:
- Markt-/Produktrecherche über alle 175 Gruppen;
- Hersteller-/Modell-/Fakten-/Nutzungsklassenabdeckung;
- gruppenspezifische Profile/Policies;
- alle daraus entstehenden fachlich zulässigen Paare.

Aktueller Research-Stand:
- alte Basis: 17 Recherchegruppen / 102 Kandidaten;
- diese Basis wurde mit UPK 0.5.1 live sequenziell geprüft/materialisiert;
- zusätzlich Research-Evidence Batches A–J im Aktenschrank gesichert;
- Coverage A–J gegen 175 noch nicht konsolidiert; daher keine Vollständigkeitszahl behaupten.

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
STATUS: PROFILE/POLICY LOCAL PASS / ALT-BASIS LIVE MATERIALISIERT / REALE POST-BATCH-PAARZAHL NOCH NICHT SEPARAT ABGELESEN / MARKTVOLLSTÄNDIGKEIT UNPROVEN

Fachprofile/Policies sind lokal gegen freigegebene Recherchekandidaten geprüft für:
- Winterdecken;
- Übergangsdecken;
- Stalldecken;
- Unterdecken;
- Steigbügel.

Die lokal berechneten 130 Cross-Family-Paare waren **Katalogpotential nach erfolgreicher Materialisierung**, nicht vorab bewiesene Live-Paarzahlen.

Der 0.5.1-Live-Batch hat die alte Recherchebasis inzwischen real geprüft/materialisiert. Eine globale tatsächliche Live-Paarzahl nach diesem Batch wurde im Produktvergleich noch nicht separat abgelesen und wird daher nicht behauptet.

## PV-TEST-085-003 – Recherchekandidaten im Lokaltest als materialisiertes Inventar behandelt
STATUS: CLOSED / TESTGRENZE KORRIGIERT / UPK 0.5.1 LOCAL HARD + WORDPRESS-LIVE-BATCH ABGESCHLOSSEN

### Ursprünglicher Befund

Der lokale 0.8.5-Fachtest materialisierte freigegebene Research-Kandidaten nur innerhalb des Tests als Laufzeitprodukte.
Das bewies Profile/Policies/Paarlogik, aber nicht bereits vorhandenes echtes WordPress-Inventar.

Die damalige Release-Erwartung `PAIRING_READY: 6` war deshalb falsch.

### Live-Gegenbeleg UPC 0.8.5

WordPress reagierte korrekt fail-closed:
- Research-Kandidaten wurden nicht als Product Knowledge ausgegeben;
- fehlendes Inventar blieb `PRODUCT_INVENTORY_MISSING`;
- kein Paar/SEO-/Providerlauf wurde erfunden;
- Kosten blieben $0.0000.

### KISS-Fix UPK 0.5.1

Kein neuer Importer, kein neues Datenmodell, kein Parallelweg.
Nur sequenzielle Admin-Orchestrierung über den vorhandenen kanonischen Weg:
`UPK_Research::run_product_group()`.

Lokaler Beleg:
- Positiv/Negativ PASS;
- Nonce/Capability PASS;
- sequenziell PASS;
- 4 Mutationen korrekt ROT;
- PHP-Lint 5/5;
- Source↔ZIP 8/8;
- Report-Hashes 7/7;
- UPC 0.8.5 gegen exakt finale UPK-0.5.1-ZIP 35/35 PASS.

### WordPress-Live 0.5.1

Batchsummary:
- 17/17 alte Recherchegruppen verarbeitet;
- PASS 6;
- TEIL-PASS 8;
- BLOCKED 3;
- pairing-ready 9.

Damit ist die Materialisierungslücke geschlossen.
Die kleine Alt-Recherchebasis selbst bleibt jedoch unvollständig; das ist Bestandteil von PV-SCALE-084-001.

## AKTUELLER ERSTER OFFENER ARBEITSBLOCK

Kein neuer Plugin-Reparaturfehler belegt.

Aktive Arbeit:
**Research-Evidence A–J gegen die autoritative 175er Registry konsolidieren und anschließend ausschließlich an tatsächlich ungedeckten Gruppen weiterrecherchieren.**

Keine neue Plugin-Version im Researchblock.
Keine künstlichen SEO-PASS-Werte.
Kein SEO-/Providerstart aus bloßer Research-Evidence.
Kein Writer/Draft/Publish.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
