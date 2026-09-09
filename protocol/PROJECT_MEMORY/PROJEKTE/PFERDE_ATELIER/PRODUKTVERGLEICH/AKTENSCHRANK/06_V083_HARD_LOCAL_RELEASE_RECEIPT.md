# PRODUKTVERGLEICH 0.8.3 – HARD LOCAL RELEASE RECEIPT

Stand: 2026-09-09
Status: LOCAL + FINAL-FRESH-ZIP HARD PASS / WORDPRESS-LIVE-RETEST OFFEN

Artefakt:
`universal-product-comparison-0.8.3-prototype.zip`

SHA-256:
`4c08ca1df348ab49849ddde8f85980db450694c58010cd0c431575bc6a3cd11e`

## Geschlossene Lücke

PV-FACH-083-001:
0.8.2 band Fakten + SEO + Dossier-Audit, aber noch keine allgemeine paaraufgelöste Fachpolicy für die spätere SEO/TEXT-Produktion.

0.8.3 bindet diese Fachentscheidung in das bestehende Produktgruppenprofil und exportiert sie strukturiert im Dossier V2.

## KISS-Änderung

Kein neuer Writer.
Kein zweites Dossier.
Keine neue Datenbank.
Kein neuer SEO-Providerweg.
Kein ACM-/TEXT-Umbau.

Nur:
- `comparison-profiles.json`: gebundene Decision-Policy;
- Planner: deterministische Policy-Auflösung;
- Dossier-Registry: eigener Policy-Hash + V2-Export;
- Dossier-Admin: read-only Sichtbarkeit;
- Tests.

Aktiver PRODUCT_COMPARISON V1:
**exakt zwei Produkte / A gegen B**.

## Fachpolicy

Alle 14 Regendecken-Merkmale besitzen genau eine gebundene Regel.

Erlaubt werden ausschließlich strukturierte Aussagearten/Need-Codes.

Beispiele:
- höhere deklarierte Denierzahl kann benannt werden;
- daraus keine Haltbarkeit/Qualität/Robustheit ableiten;
- abnehmbares Halsteil nur als gebundener Bedarf;
- Beingurt-/Fillet-Strap-Bedarfe nur bei exaktem dokumentiertem Merkmal;
- Größen ohne normierte Abbildung nicht ranken;
- Quellenlücken/Konflikte erzeugen keine Präferenz.

## Harte lokale Prüfung

Finale Fresh-ZIP:
- ausführbare Regression: 25/25 PASS;
- PHP-Lint: 43/43 PASS;
- Source↔ZIP: 57/57 exakt;
- Report-Hashbindung: 56/56 exakt;
- echte UPK 0.5.0 SHA:
  `80218ec721631353d62a7e3058e76d9c4a4829802c4d5c6bd6f1f2014b6879e3`;
- echte PSTE 0.56.25 SHA:
  `8122e3fa2273fe4d8e53476f557ed0ddd99a197e8b1c40302f35db245ebb0f95`;
- alle 11 realen herstellerübergreifenden 0g-Regendecken-Paare aus dem echten UPK-Katalog policy-aufgelöst;
- keine freie fachliche Aussageart;
- Quellengrenzen fail-neutral;
- Policy-Drift fail-closed;
- Dossier V2 bindet beide Titelprodukte, Zielkeyword, Artikeltyp und Policy-Hash;
- bestehende 0.8 Kosten-/SEO-/Readiness-/Audit-Negativtests weiter PASS.

## Kostenbindung

Eine reine Fachpolicy-Änderung invalidiert die bezahlte SEO-Evidenz nicht.

Echter Laufzeit-SEO-Binding-Hash:
0.8.2 = 0.8.3 =
`863a724d9f349770d9f62c7c65ee7c74565d4247f9bf15504984ae4ece2c9003`

## Unabhängige Rückfallmutationen

Alle korrekt ROT:
- drei Produkte im A-vs-B-Typ zulassen;
- Policy-Hash konstant/falsch entkoppeln;
- Policy-Drift beim Export ignorieren.

Bestehende 0.8-Mutationen ebenfalls weiter erkannt.

## PSTE-Realbeleg

Der externe reale 0.8.2-PSTE-Themenmap-False-Pair-Test wurde nicht nachgebaut.

Er wird nur weitergeführt, weil die allein dafür zuständige Produktvergleichs-Discovery-Datei zwischen real getesteter 0.8.2-Quelle und 0.8.3 byte-identisch ist.

SHA-256:
`bba970b7135671cb1d09f5f33fe29598b2a44b8328153597cd3347bb4acdbdf4`

## Gesamtworkflow-Grenzen

Weiter eingehalten:
`Produktwissen -> Vergleichbarkeit -> bidirektionales SEO -> persistente Evidenz -> Readiness/Kannibalisierung -> gebundene Fachpolicy -> Dossier V2 -> unabhängiger Audit`

Writer/Draft/Publish dormant.
Affiliate getrennt.
Kein Auto-Publish.

## Live-Grenze

Noch kein WordPress-LIVE-PASS für 0.8.3.
Nächster Schritt ausschließlich gemäß HOBBYRAUM.
