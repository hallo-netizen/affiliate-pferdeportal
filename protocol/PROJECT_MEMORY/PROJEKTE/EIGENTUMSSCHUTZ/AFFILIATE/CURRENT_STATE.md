# HAB & BEWAHR – AFFILIATE CURRENT

STAND: 2026-10-26
STATUS: NEUTRALER STAMM GESICHERT / NO LIVE PASS / HAB-&-BEWAHR-ANPASSUNG NOCH OFFEN

## Verbindlicher Stand

Für Hab & Bewahr wurde ein eigenes Affiliate-Büro angelegt.

Gesicherte technische Ausgangsbasis:
`NEUTRAL_STAMM/affiliate-portal-router/`

Der Stamm basiert auf der bereits pferdeatelier-bereinigten HD-009-Engine, wurde aber vor Ablage hier zusätzlich von Hobby-Depot-spezifischer Bindung getrennt.

Entfernt bzw. neutralisiert wurden insbesondere:
- Hobby-Depot-Pluginidentität und Routerklassenbindung
- HD-004-Kategorie-/Zielquellenbindung
- HD-003/Hobby-Depot-Designprofilbindung
- fest verdrahtete Hobby-Depot-Slotmatrix
- Hobby-Depot-spezifische eBay-/idealo-Zieltexte, Defaults und Zielquellenklassen
- Hobby-Depot-spezifische Provider-/Deal-Radar-Bezeichnungen

Erhalten wurden:
- allgemeine Affiliate-Engine
- eBay- und idealo-Providerlogik
- Awin / ADCELL / Digistore24 / Direktpartner-Basis
- Kontroll-, Veto-, Output- und Automationslogik
- bestehende Credential-/Konfigurationsschnittstellen

Zugangsdaten sind nicht im Campus gespeichert.

## Wichtig

Der neutrale Stamm ist **keine installierbare Hab-&-Bewahr-Livefreigabe**.
Die Portal-Zielquelle ist absichtlich ungebunden und fail-closed.

## Herkunft

Hobby-Depot-Arbeitsquelle:
`hobbyrausch/hd009-affiliate-port-20261026`
Head bei Ableitung:
`56b91b171cb68129369b67e411da5345957af4f2`

Die Hobby-Depot-Entwicklung bleibt davon getrennt und wird nicht zurückgesetzt.

## NEXT ACTION

Für den späteren Hab-&-Bewahr-Chat:

1. Hab-&-Bewahr-Zielquelle aus dem zuständigen Kategorie-/Portal-Current anbinden.
2. Hab-&-Bewahr-Design-/Slotvertrag separat anbinden.
3. Portalnamen und projektspezifische Defaults setzen.
4. Positiv-, Negativ-, Regression-, Installations- und Runtimeprüfung durchführen.
5. Erst danach einen Hab-&-Bewahr-Installationskandidaten bauen.

Nicht HD-004 übernehmen. Nicht Hobby-Depot-Slotmatrix übernehmen. Nicht wieder aus Pferdeatelier kopieren.
