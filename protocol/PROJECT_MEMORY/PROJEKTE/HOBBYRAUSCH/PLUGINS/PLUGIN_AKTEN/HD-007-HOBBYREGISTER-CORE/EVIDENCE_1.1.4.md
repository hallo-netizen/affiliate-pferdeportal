# HD-007 – EVIDENCE 1.1.4 ÄNDERUNGSSTUFE 1

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.4_UPDATE_STAGE1.zip`

SHA-256:
`71d17e0e15433f27685832e5cf91d327a3f93cc44271713efab034b4e46c2929`

Größe:
23,111 Bytes.

## Änderungen

### Breadcrumb
Der Register-Breadcrumb wird nicht mehr innerhalb des Register-Templates ausgegeben.
Er wird über `astra_content_before` auf derselben serverseitigen Breadcrumb-Schiene wie das Pferdeatelier gemountet.

Hierarchie:
- Register: Startseite › Magazin › Hobbyregister
- Profil: Startseite › Magazin › Hobbyregister › Hobby

Der Registerinhalt enthält keinen zweiten Inline-Breadcrumb.

### Auf einen Blick
Sichtbar nur noch:
- Icon;
- Wert.

Die sichtbaren Mini-Labels wie „Mit wem?“, „Ort“, „Zeit“, „Einstieg“, „Platz“, „Körperlich“, „Lernkurve“ sind entfernt.
Die Bedeutung bleibt als aria-label für Barrierefreiheit erhalten.

### Relationengruppen
„Zur gleichen Hobbygruppe“:
- ausschließlich Hobbys aus derselben primären Hobbygruppe;
- Überschrift bewusst zweizeilig: „Zur gleichen / Hobbygruppe“.

„Ähnliche Hobbys“:
- ausschließlich Hobbys außerhalb der primären Hobbygruppe;
- zusätzlich werden bereits im gleichen-Hobbygruppe-Block gezeigte IDs ausgeschlossen.

Damit sind beide Blöcke garantiert disjunkt; keine zentrale Datenbankänderung nötig.

### Buttons
„Zur Hobbygruppe“ und „Zum Hobbymagazin“ verwenden dieselbe gemeinsame Button-CSS und dasselbe helle Petrol `#2f969d`.

## QA

E2E geprüft auf:
- 3D-Druck;
- Geocaching;
- Buchbinden;
- Slacklining.

Jeweils:
- serverseitiger Breadcrumb genau einmal;
- kein Inline-Breadcrumb;
- keine sichtbaren Faktenlabels;
- 7 Faktenwerte;
- Gruppenüberschrift mit Zeilenumbruch;
- 3 gleiche-Hobbygruppe-Karten;
- 4 ähnliche Hobby-Karten;
- keine URL-Überschneidung zwischen beiden Blöcken;
- kein zusätzlicher ähnlicher-Hobbys-Block unten.

PHP-Lint / Fresh-Unpack PASS.
862er Core bleibt unverändert.
