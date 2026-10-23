# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **HD-003 1.50.728 + HD-007 1.1.4 ÄNDERUNGSSTUFE 1 LOCAL HARD PASS / LIVE-ABNAHME OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Gemeinsames aktuelles Update

`HOBBY_DEPOT_AKTUELL_20261023_AENDERUNGSSTUFE1.zip`

SHA-256:
`e548be549afe407075c6030c2a96a21813b095da06c9802e8eb96af78c8d645e`

Größe:
610,427 Bytes.

Enthält exakt vier geänderte Dateien unter den zwei bestehenden Pluginwurzeln:
- `affiliate-portal-template-kit/`
- `hd-hobbyregister-core/`

Kein neues Plugin.

## Änderungsstufe 1

Footer:
- Logo kleiner;
- Hauptlogo vollständig sichtbar;
- Untertitel des Logoassets weiterhin ausgeblendet.

Hobbyregister:
- Breadcrumb nicht mehr im Registertemplate, sondern auf der serverseitigen Pferdeatelier/Astra-Breadcrumb-Schiene;
- „Auf einen Blick“ nur Icon + Wert;
- „Zur gleichen Hobbygruppe“ zweizeilig;
- gleiche Hobbygruppe und ähnliche Hobbys disjunkt;
- ähnliche Hobbys ausschließlich außerhalb der primären Hobbygruppe;
- Gruppenbutton und Hobbymagazin-Button identisch in hellem Petrol.

Keine zentrale Datenbankänderung für die Relationsabgrenzung.

## QA

- Fresh-Unpack PASS;
- 4 Paketdateien;
- PHP-Lint PASS;
- HD-007 E2E auf 3D-Druck, Geocaching, Buchbinden, Slacklining PASS;
- kein doppelter Breadcrumb;
- keine sichtbaren Faktenlabels;
- keine Relationsüberschneidung.

## EXAKT EINE NEXT ACTION

**Das aktuelle Update-Bundle per Cyberduck einspielen und danach Footer, Register-Startseite und ein Detailprofil live prüfen.**
