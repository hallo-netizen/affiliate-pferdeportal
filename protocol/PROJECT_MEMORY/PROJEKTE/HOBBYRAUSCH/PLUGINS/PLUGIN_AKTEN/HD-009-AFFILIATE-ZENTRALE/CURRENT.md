# HD-009 – HOBBY DEPOT AFFILIATE-ZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: PORTIERUNG IN ARBEIT / NICHT INSTALLIERBAR / KEIN RELEASE

Plugin-ID: HD-009-AFFILIATE-ZENTRALE
Name: Hobby Depot Affiliate-Zentrale
Art: Portierung der Pferdeatelier Affiliate-Zentrale

Fach-Current:
../../../AFFILIATE/CURRENT_STATE.md

Arbeitsbranch:
`hobbyrausch/hd009-affiliate-port-20261026`

Arbeitsquelle:
`WORKSOURCE/affiliate-portal-router/`

## Exakte Ausgangsbasis

Quelle:
`affiliate-release-current:release/affiliate-zentrale/current/affiliate-portal-router/`

Pferdeatelier-Branch-Head bei Übernahme:
`7375bc46a57ac4c2ff2a74a6dd4919113defd009`

Formaler Pferdeatelier-Kandidat:
6.72.211 / RELEASE BLOCKED durch AFF-ERR-065.

Wichtig:
Die Hobby-Depot-Portierung übernimmt die technische Quelle als Ausgangsbasis, nicht den Pferdeatelier-Release-/Live-PASS-Status.

28/28 Quelldateien wurden zunächst byte-identisch kopiert.
Danach entfernt:
- Pferdeatelier eBay-Zielkatalog;
- Pferdeatelier Portalstruktur;
- historischer Pferdeatelier-Recovery-Produktbestand.

## Provider-Wahrheit

- eBay: aktiv implementiert.
- idealo: aktiv implementiert.
- Amazon: nur vorbereitet; kein realer Adapter vorhanden.
- Awin/ADCELL/Digistore24/Direktpartner-Engine bleibt zunächst Bestandteil der technischen Basis und wird nur fachlich bereinigt, nicht blind entfernt.

## Credentials

Keine Zugangsdaten werden in diese Akte oder Quellkopie hineindokumentiert.
Die vorhandenen Options-/Konstanten-/Secret-Schnittstellen bleiben als Mechanismus erhalten.
Ein späterer Live-Transfer bestehender Zugangsdaten ist ein separater Laufzeit-/WordPress-Schritt.

## Noch nicht freigegeben

- keine Installations-ZIP;
- kein CURRENT.zip;
- kein Liveeinsatz;
- keine Hobby-Depot-Produktdaten;
- keine Amazon-Produktrecherche behaupten;
- keine Pferdeatelier-Zielbestände wiederverwenden.

## ERSTER OFFENER BLOCKER

Verbleibende Pferdeatelier-spezifische Codepfade und Zielannahmen vollständig identifizieren und bereinigen.

## EXAKT EINE NEXT ACTION

Codeinventar nach Pferde-/Portalabhängigkeiten fertigstellen und anschließend die fachlichen Zielquellen für Hobby Depot anbinden.
