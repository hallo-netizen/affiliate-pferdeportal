# PRODUKTVERGLEICH – AUTORITATIVE FEHLERQUELLE

STAND: 2026-09-09
ROLLE: einzige detaillierte Fehlerquelle für den aktuellen PRODUKTVERGLEICH-Arbeitsweg.

## PV-ERR-001 – falsche WordPress-Kategoriehierarchie
STATUS: CLOSED

## PV-ERR-002 – Erst-Draft sprang an Materialisierungsstufe vorbei
STATUS: CLOSED / HISTORISCHER EIGENER DRAFTWEG NICHT MEHR ZIELARCHITEKTUR

## PV-ERR-003 – Hauptmenü-Test war falscher Positivtest
STATUS: CLOSED / ECHTER WP-LIFECYCLE ALS PFLICHTREGEL ERHALTEN

## PV-LIVE-001 – falsches PASS bei null geeigneten Vergleichen
STATUS: CLOSED / LIVE 0.8.1, 0.8.2 UND 0.8.3 BESTÄTIGT / REGRESSION AKTIV

Realer 0.8.3-Livebefund:
8 Kandidaten -> 0 Provider-Aufrufe -> $0.0000 -> 0 SEO-PASS -> 8 blockiert -> 0 Dossiers -> `NO_ELIGIBLE_COMPARISONS`.

## PV-ERR-004 – PASS ohne realen Dossier-Receipt
STATUS: CLOSED IM 0.8.1+ / REGRESSION AKTIV

Blocks:
- `UPC_DOSSIER_MATERIALIZATION_COUNT_MISMATCH`
- `UPC_DOSSIER_FINAL_AUDIT_RECEIPT_MISSING`

## PV-COST-082-001 – bezahlte Produkt-/Paar-Zwischenergebnisse nicht dauerhaft genug gebunden
STATUS: CLOSED / LOKAL + WORDPRESS-LIVE 0.8.2/0.8.3 PASS

WordPress 0.8.3:
erneuter identischer Workflow -> 0 Provider-Aufrufe / $0.0000.

## PV-FACH-083-001 – Dossier band Fakten, aber keine allgemeine erlaubte fachliche Interpretation
STATUS: CLOSED LOKAL / 0.8.3 WORDPRESS-LIVE-REGRESSION PASS

KISS-Fix:
- Decision-Policy im vorhandenen Produktgruppenprofil;
- exakt 2 Produkte für PRODUCT_COMPARISON V1;
- 14/14 Regendecken-Merkmale mit Policy;
- Dossier V2 exportiert strukturierte erlaubte Aussagearten, Verbote und Need-Codes;
- kein Writer;
- Policy-Hash getrennt vom bezahlten SEO-Binding.

Harter lokaler Beleg:
- finale Fresh-ZIP 25/25 PASS;
- PHP-Lint 43/43;
- Source↔ZIP 57/57;
- Report-Hashes 56/56;
- 11 reale herstellerübergreifende UPK-Regendecken-Paare;
- Mutation Guards PASS.

WordPress-Live 0.8.3:
- Installation/Version korrekt;
- alter SEO-Endstand erhalten;
- 0 Provider / $0.0000;
- korrekt 8 BLOCKED / 0 Dossiers / `NO_ELIGIBLE_COMPARISONS`.

### Bedingungsabhängiger Positivbeleg

Ein echter positiver Dossier-V2-Livefall ist aktuell nicht ausführbar, weil kein reales Paar SEO-PASS besitzt.

STATUS:
NICHT FEHLER / NACHHOLBELEG BEI ERSTEM REALEN SEO-PASS.

Keine künstliche Umgehung zulässig.

## AKTUELLER FEHLERSTATUS

Kein offener Produktvergleichs-Reparaturfehler belegt.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
