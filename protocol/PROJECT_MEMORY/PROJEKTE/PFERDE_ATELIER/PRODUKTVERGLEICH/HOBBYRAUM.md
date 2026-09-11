# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-11
STATUS: AKTIV / PV-SCALE-084-001

## AUSGANGSBASIS

Exakt geprüfte Basis:
`universal-product-comparison-0.8.3-prototype.zip`

SHA-256:
`4c08ca1df348ab49849ddde8f85980db450694c58010cd0c431575bc6a3cd11e`

0.8.3 bleibt unverändert als Proof-/Regression-Basis.

## AKTUELLER AUFTRAG

Generische Vollabdeckung aller autoritativen Vergleichs-Produktgruppen bauen.

Portalbindung:
- Produktseiten: 329;
- Vergleichs-Produktgruppen: **175**;
- Regendecken: Proofgruppe 1/175.

Ziel pro Gruppe:
`vollständiger Produktbestand -> alle fachlich zulässigen A-vs-B-Paare -> SEO-Prüfung -> terminal BLOCK oder Dossier V2`.

## HARD RULES

- keine Gruppe hartcodiert;
- keine willkürliche Gruppenobergrenze;
- keine willkürliche Paarobergrenze;
- PRODUCT_COMPARISON V1 bleibt exakt 2 Produkte;
- Same Brand/incompatible Profile vor Providerkosten BLOCK;
- fehlendes Gruppenprofil/Decision-Policy/Produktinventar muss sichtbar als Coverage-Lücke erscheinen und darf nicht still verschwinden;
- Batch/Resume zulässig, aber ohne verlorene oder doppelte Paare;
- persistente SEO-Evidenz wiederverwenden;
- keine Providerkosten für bereits gültig vorhandene Evidenz;
- kein Writer-/Draft-/Publishweg;
- kein Auto-Publish.

## NÄCHSTE TECHNISCHE STUFE

0.8.4-Kandidat ausschließlich aus der exakten 0.8.3-ZIP ableiten:
1. portalgebundene 175-Gruppen-Registry;
2. Readiness je Gruppe (`READY`, `PROFILE_MISSING`, `POLICY_MISSING`, `PRODUCT_INVENTORY_MISSING` usw.);
3. vollständige Paar-Coverage je READY-Gruppe;
4. Coverage-Receipt je Gruppe + global;
5. Kostenprognose nur für noch offene Providerarbeit;
6. bestehende 0.8.3-Regeln unverändert erhalten.

## ABNAHME

Vor neuer ZIP zwingend:
- positiv/negativ;
- alle bestehenden Regressionen;
- Gesamtworkflow;
- große synthetische Produktgruppe ohne Paarverlust;
- Resume/Idempotenz/Kostenschutz;
- Coverage-Manipulationen müssen ROT werden;
- Fresh-ZIP erneut komplett PASS.

Vorher keine Ausgabe/Freigabe.
