# HOBBYRAUSCH – AFFILIATE – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-26
STATUS: AKTIV / PORTIERUNG LÄUFT / NICHT INSTALLIERBAR

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_AFFILIATE`.

## Gebundener Nutzerauftrag

Die bestehende Pferdeatelier-Affiliate-Zentrale als technische Basis für Hobby Depot übernehmen.

Verbindlich:
- Hobby Depot bleibt fachlich vollständig vom Pferdeatelier getrennt.
- Pferde-Banner, Pferde-Produkte, Pferde-Artikel, Pferde-Kataloge, Pferde-Taxonomien und sonstige Pferde-Fachbezüge dürfen nicht übernommen werden.
- allgemeine Engine, Providerlogik, Ausgabesystem, Veto-/Kontrolllogik und Partneranbindungen bleiben erhalten.
- Zugangsdaten/Secrets dürfen niemals in Campus, Git oder Protokollen offengelegt werden.
- vorhandene Credential-/Optionspfade werden bis zu einem getesteten Migrationsweg nicht unnötig umbenannt.
- Produktrecherche für Hobby Depot muss Amazon, eBay und idealo fachlich korrekt neu anbinden.

## Aktueller belastbarer Stand

Pferdeatelier-Referenz frisch gelesen:
- Branch: `affiliate-release-current`
- Current-Autorität: `control/release-governance/CURRENT_RELEASE.json`
- Generation: 313
- Kandidat: 6.72.211
- Source-Manifest: `f11687daa1f11d8ff98a3c0d62a720dac170dd95edddf39eba04530e858c44cf`
- Referenz-Head: `7375bc46a57ac4c2ff2a74a6dd4919113defd009`
- Pferdeatelier bleibt selbst unverändert.

Hobby-Depot-Arbeitsbranch:
`hobbyrausch-affiliate-current`

Aktueller Workbench-Commit:
`be76ac860272628b3f2ecf66cb8c95ffcc92d29f`

Arbeitsquelle:
`work/hobbyrausch-affiliate/porting/hobby-depot-affiliate-router/`

Kopiert:
- 24 Engine-/Provider-Dateien als technische Ausgangsbasis.

Bewusst NICHT übernommen:
- Pferde-eBay-Katalog;
- Pferde-Portalstruktur;
- historischer Pferde-Produkt-Recoverybestand;
- Pferde-spezifisches Readme.

An Stelle der beiden Katalogdateien liegen fail-closed Hobby-Depot-Portierungsplatzhalter. Der Workbench ist ausdrücklich noch nicht installierbar.

## Providerbefund

- eBay: echter Browse-API/EPN-Adapter vorhanden, aber seine Relevanz- und Zielkataloglogik ist noch hart auf Pferde/Reitsport ausgerichtet.
- idealo: echter iPN/Feed-Adapter vorhanden, aber Teile der Produkt-/Konzeptzuordnung sind noch hart auf Pferdeportal-Konzeptdaten ausgerichtet.
- Amazon: im Altplugin nur als `prepared` registriert; kein fertiger Amazon-Produktadapter vorhanden.
- Awin/ADCELL/Digistore24 und allgemeine Creative-/Output-/Veto-Logik bleiben als technische Partnerbasis erhalten.
- OTTO/Awin-Pferde-Sonderlogik ist keine Hobby-Depot-Fachwahrheit und muss aus dem neuen Produktrecherchepfad entfernt bzw. neutralisiert werden.

## Credential-Regel

Secrets werden nicht aus Git gelesen, nicht in Campusdateien kopiert und nicht protokolliert.
Die technische Portierung erhält die bestehenden Settings-/Constant-Schnittstellen zunächst kompatibel, damit reale Zugangsdaten später ohne Offenlegung übernommen bzw. wieder gebunden werden können.
Ein funktionsfähiger Secret-Migrationsnachweis existiert für Hobby Depot noch nicht und darf nicht behauptet werden.

## Erster offener Blocker

In den kopierten PHP-Dateien existieren noch Pferdeatelier-spezifische Fachpfade und sichtbare Bezüge, insbesondere in:
- Hauptplugin;
- eBay-Adapter;
- idealo-Adapter;
- Automatisierung/OTTO-Sonderlogik.

Diese müssen entfernt oder durch Hobby-Depot-Datenverträge ersetzt werden, bevor ein Installationskandidat entstehen darf.

## NEXT ACTION

Die Pferdeatelier-spezifischen Fachpfade im Hobby-Depot-Workbench vollständig inventarisieren und auf neutrale Hobby-Depot-Verträge umstellen; dabei die Provider-/Credential-/Output-Engine unverändert erhalten. Danach erst Amazon Creators API als dritten echten Produktadapter ergänzen.
