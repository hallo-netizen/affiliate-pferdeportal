# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.1.4 ÄNDERUNGSSTUFE 1 LOCAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
HD-007-HOBBYREGISTER-CORE

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.4_UPDATE_STAGE1.zip`

SHA-256:
`71d17e0e15433f27685832e5cf91d327a3f93cc44271713efab034b4e46c2929`

Größe:
23,111 Bytes.

Hauptordner:
`hd-hobbyregister-core/`

## Breadcrumb

Der Breadcrumb wird jetzt auf derselben serverseitigen Astra/Pferdeatelier-Schiene ausgegeben und nicht mehr innerhalb des Registerinhalts.

Hierarchie bleibt:
- Startseite › Magazin › Hobbyregister
- Startseite › Magazin › Hobbyregister › Hobby

Kein zweiter Inline-Breadcrumb.

## Auf einen Blick

Sichtbar nur noch:
- Icon;
- Wert.

Die Mini-Labels „Mit wem?“, „Ort“, „Zeit“, „Einstieg“, „Platz“, „Körperlich“, „Lernkurve“ sind aus der sichtbaren Oberfläche entfernt.
Für Barrierefreiheit bleiben ihre Bedeutungen als aria-label erhalten.

## Relationengruppen

„Zur gleichen Hobbygruppe“:
- 3 Hobbys aus derselben primären Hobbygruppe;
- Überschrift zweizeilig: Zur gleichen / Hobbygruppe.

„Ähnliche Hobbys“:
- 4 Hobbys ausschließlich außerhalb der primären Hobbygruppe;
- bereits im Gruppenblock gezeigte IDs zusätzlich ausgeschlossen.

Damit sind beide Blöcke garantiert disjunkt.
Keine Änderung der zentralen Hobby-Datenbank nötig.

## Buttons

„Zur Hobbygruppe“ und „Zum Hobbymagazin“ verwenden dieselbe gemeinsame Button-CSS und dasselbe helle Petrol.

## QA

E2E geprüft:
- 3D-Druck;
- Geocaching;
- Buchbinden;
- Slacklining.

Je Profil:
- serverseitiger Breadcrumb genau einmal;
- kein Inline-Breadcrumb;
- 7 Icon+Wert-Fakten ohne sichtbare Labels;
- Gruppenüberschrift mit Zeilenumbruch;
- 3 Gruppen-Karten + 4 ähnliche Hobbys;
- keine Überschneidung zwischen beiden Relationsblöcken;
- kein zweiter ähnlicher-Hobbys-Block unten.

PHP-Lint / Fresh-Unpack PASS.
862er Core unverändert.

Evidence:
`EVIDENCE_1.1.4.md`

## EXAKT EINE NEXT ACTION

**Gemeinsames Update-Bundle `HOBBY_DEPOT_AKTUELL_20261023_AENDERUNGSSTUFE1.zip` entpacken und `hd-hobbyregister-core` per Cyberduck über den vorhandenen Ordner unter `wp-content/plugins/` zusammenführen.**
