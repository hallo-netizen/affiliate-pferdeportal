# ALLGEMEINES DESIGN – CURRENT STATE

STAND: 2026-09-15

## Aktueller Stand

Plugin:
**Universal Portal Design Suite 2.2.41**

Contract:
**V104**

## Aktuelle Änderung

Ausschließlich die Geometrie zwischen Breadcrumb-Unterkante und erstem sichtbaren Inhalts-/Hero-/Titelblock wurde zentralisiert.

Verbindlich:
- Desktop: **15 px**
- Mobil bis 544 px: **10 px**
- keine individuelle `breadcrumb_gap`-Einstellung mehr
- keine seitentyp-spezifischen Breadcrumb-Abstandswerte mehr
- Strukturwrapper zwischen Breadcrumb und erstem sichtbaren Block werden zentral neutralisiert
- interne Designabstände des sichtbaren Zielblocks bleiben erhalten

Nicht verändert:
- Typografie
- Farben
- Breiten
- Karten
- Tabellenlogik
- Suche
- Affiliate
- sonstige Design-/Funktionslogik

## V104 Bestandsschutz

Der bestehende V104-DOM-Ursachenfix für generierte Tabellen bleibt unverändert erhalten:
`comparison-table` / `system-129-table` + direkt folgender Absatz
→ reales nicht kollabierendes 28-px-Spacerelement.

## Prüfstand 2.2.41

- Source-Audit alte Breadcrumb-Abstandautoritäten: PASS
- Chromium Desktop 1440: 6/6 exakt 15 px PASS
- Chromium Mobil 390: 6/6 exakt 10 px PASS
- Negativmutation zentrale Autorität = 0: ROT wie erwartet
- interne Hero-/Intro-Paddings unverändert: PASS
- PHP-Lint 11/11: PASS
- JS-Syntax: PASS
- ZIP-Tree bytegleich zum geprüften Build: PASS
- Overwrite 2.2.40 → 2.2.41: bytegleicher Zielbaum PASS
- Mastermanifest 2.2.41: 301/301 PASS

## Beleggrenze

**LOKAL HART PASS / LIVE OFFEN.**
Kein Universal-Live-PASS ohne Installation und Sichtprüfung im realen Zielportal.

## Artefakte

Plugin:
`UNIVERSAL_PORTAL_DESIGN_SUITE_V2.2.41_GLOBAL_BREADCRUMB_GAP_15_10_INSTALLIEREN.zip`

SHA-256:
`2bc9e9327601f8e1f1cf2cb1d299f9ec120994e325abb5d676fd347005e55512`

Master:
`MASTER_ALLGEMEINGUELTIG_DESIGN_V2_2_41_CONTRACT_V104_20260915.zip`

SHA-256:
`a6486b41e786ad53a90d5203720244f4055b52dd359779cd31b5a5444e380da3`

Persistenter Artefaktort:
`/Campus-Archiv/ALLGEMEINGUELTIGE_BAUSTEINE/DESIGN/2026-09-15/`
