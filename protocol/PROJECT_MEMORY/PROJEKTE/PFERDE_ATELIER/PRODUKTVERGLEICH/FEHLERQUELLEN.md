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
STATUS: CLOSED / LIVE 0.8.1 UND 0.8.2 BESTÄTIGT / REGRESSION AKTIV

Realer Befund:
0.7.0 meldete bei 0 SEO-PASS / 0 Dossiers fälschlich grün PASS.

Fix:
`NO_ELIGIBLE_COMPARISONS` statt Success.

WordPress 0.8.2:
8 Kandidaten -> 0 Provider-Aufrufe -> $0.0000 -> 0 SEO-PASS -> 8 blockiert -> 0 Dossiers -> `NO_ELIGIBLE_COMPARISONS`.

## PV-ERR-004 – PASS ohne realen Dossier-Receipt
STATUS: CLOSED IM 0.8.1+ / REGRESSION AKTIV

Fix:
- Dossier-Rückgabemenge muss exakt stimmen;
- jedes gemeldete Dossier muss im unabhängigen finalen Audit vorhanden sein.

Blocks:
- `UPC_DOSSIER_MATERIALIZATION_COUNT_MISMATCH`
- `UPC_DOSSIER_FINAL_AUDIT_RECEIPT_MISSING`

## PV-COST-082-001 – bezahlte Produkt-/Paar-Zwischenergebnisse nicht dauerhaft genug gebunden
STATUS: CLOSED / LOKAL + WORDPRESS-LIVE-WIEDERHOLUNG PASS

Fix 0.8.2:
- persistenter Produkt-/Paar-Probe-Store;
- PARTIAL nach jedem bezahlten Endpunkt;
- positiv + negativ;
- 90 Tage;
- exakte Hash-/Kontextbindung;
- Wiederverwendung vor Providerzugriff.

WordPress-Live:
erneuter identischer Workflow -> 0 Provider-Aufrufe / $0.0000.

## PV-FACH-083-001 – Dossier band Fakten, aber keine allgemeine erlaubte fachliche Interpretation

STATUS: CLOSED IM 0.8.3-KANDIDAT / WORDPRESS-LIVE-RETEST OFFEN

Befund gegen 0.8.2:
Das Dossier band Produktfakten, SEO und Audit. Die später schreibende SEO/TEXT-Strecke hätte für Unterschiede jedoch teilweise selbst entscheiden müssen, welche fachliche Aussage oder Bedarfszuordnung daraus zulässig ist.

Das würde eine Freiheitslücke erzeugen.

KISS-Fix 0.8.3:
- vorhandenes Produktgruppenprofil erhält gebundene `decision_policy`;
- exakt 2 Produkte für PRODUCT_COMPARISON V1;
- jedes der 14 Regendecken-Merkmale besitzt genau eine Policy;
- Dossier V2 exportiert strukturierte Entscheidungsklassen, erlaubte Aussagearten, Verbote und feste Need-Codes;
- keine Prosa;
- kein neuer Writer;
- Policy-Hash getrennt vom bezahlten SEO-Binding.

Fail-closed:
- fehlende/abweichende Policy -> BLOCK;
- Policy-Drift nach Dossiererzeugung -> Export BLOCK;
- 3 Produkte im A-vs-B-Typ -> BLOCK;
- Quellenwarnung darf keine Präferenz/Need-Fit erzeugen.

Harter Beleg:
- finale Fresh-ZIP 25/25 PASS;
- PHP-Lint 43/43;
- Source↔ZIP 57/57;
- Report-Hashes 56/56;
- 11 echte herstellerübergreifende UPK-Regendecken-Paare;
- 3 unabhängige 0.8.3-Mutationen korrekt ROT;
- bestehende Regressionen weiter PASS.

Kosten-Gegenbeleg:
0.8.2 und 0.8.3 besitzen denselben echten Laufzeit-SEO-Binding-Hash:
`863a724d9f349770d9f62c7c65ee7c74565d4247f9bf15504984ae4ece2c9003`

Damit kauft eine reine Fachpolicy-Änderung unveränderte SEO-Evidenz nicht neu.

LIVE-GRENZE:
0.8.3 auf echter WordPress-Seite noch offen.

## Regel

Neue Produktvergleichsfehler werden ausschließlich hier ergänzt.
Das zentrale Fehlerregister bleibt Wegweiser.
