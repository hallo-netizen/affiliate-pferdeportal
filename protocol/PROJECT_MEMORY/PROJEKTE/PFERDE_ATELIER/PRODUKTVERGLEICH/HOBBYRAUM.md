# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-09
STATUS: AKTIV / 0.8.0 WORDPRESS-RETEST

## AKTUELLER AUFTRAG

Einmaliger Realtest des vollständig source- und Fresh-ZIP-geprüften 0.8.0-Gesamtworkflows.

## GEBUNDENER WORKFLOW

`SEO ↔ Produktwissen → Vergleichbarkeit → direkte Paar-Nachfrage ODER Nachfrage A+B → aktuelle Planning-/Kannibalisierungsprüfung → Dossier → Audit`

## TESTKANDIDAT

`Universal Product Comparison 0.8.0-prototype`

SHA-256:
`c9eec5b4c7faafa23af6bd5c554d85c2c4d1763e4c618fbd49c3e04dd45abb66`

## VOR AUSGABE REAL GEPRÜFT

- komplette bestehende Regression;
- direkter A-gegen-B-Positivfall;
- A+B-Produktnachfrage ohne direkte Paaranfrage positiv;
- nur ein Produkt negativ;
- keine Nachfrage negativ;
- generische Gruppenanfrage negativ;
- Same-Brand negativ;
- Vergleichbarkeit negativ;
- Provider-PARTIAL negativ;
- alte 0.7.x-Signale stale;
- Ablaufzeit stale;
- aktuelle Readiness/Kannibalisierung revalidiert;
- Inventory/Structure-Drift bindet Dossier neu;
- idempotenter Wiederholungslauf;
- autoritative PSTE-Kostenrechnung;
- Mutationstests;
- PHP-Lint 39/39;
- Fresh-ZIP vollständig erneut getestet;
- Source↔Fresh-ZIP byte-identisch (50 Dateien).

## NEXT ACTION

**Nur:**

WordPress → vorhandenes `Universal Product Comparison` durch 0.8.0 ersetzen.

Dann:
**Produktvergleich → Vergleichsplanung → Regendecken**.

Vor dem Lauf prüfen:
- alte 0.7.x-Signale müssen als offen/stale neu bewertet werden;
- maximale Providerkosten dürfen bei 8 Paaren / 5 Produkten bis zu **$0.4056** anzeigen.

Dann **Gesamtworkflow starten** und Screenshot zurückgeben.

Kein weiterer Pluginstand vor diesem Realtest.
