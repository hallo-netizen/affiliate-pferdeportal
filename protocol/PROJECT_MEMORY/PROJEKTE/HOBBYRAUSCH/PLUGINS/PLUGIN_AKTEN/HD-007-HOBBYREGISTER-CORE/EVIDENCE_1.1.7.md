# HD-007 – EVIDENCE 1.1.7 UI + ARTICLE LOAD CHECK

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE LOAD STATE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.7_FULL_UI_FIX.zip`

SHA-256:
`790fd916f06a65d1b6736968148410470536aecedacfac5ce1b2fb5f24877f65`

Größe:
1,349,633 Bytes.

## Wichtige Diagnose

1.1.6 wurde lokal erneut mit echtem Route-/Render-Harness geprüft.
Der Detailartikel wird weiterhin vollständig erzeugt:
- Route `/hobbyregister/3d-druck/`
- kompletter Hero/Sidebar/Text
- 8 Fließtextabschnitte
- ca. 24 KB HTML.

Damit kann die 1.1.6-Layoutänderung den Artikel lokal nicht entfernt haben.
Wenn live kein Artikel erscheint, wird dort der aktive HD-007-Ladezustand nicht wie im geprüften Paket ausgeführt (z.B. Plugin nach Vollersatz deaktiviert/staler Serverstand).

## 1.1.7 UI-Fix

A–Z:
- aktuiver Buchstabe deutlich petrol gefüllt mit weißer Schrift;
- `Alle` ist sichtbar aktiv, wenn kein Buchstabenfilter gesetzt ist.

Gruppen:
- aktive Hobbygruppe zusätzlich mit sichtbarem Ring.

Treffer:
- nur in gefilterten Ansichten;
- Text `X Hobbys` statt `X Treffer`.

Pagination:
- bei mehr als einer Seite oben und unten.

Rücklink:
- `Filter zurücksetzen` entfernt;
- stattdessen `Zur Register-Startseite`.

## E2E-Simulation 1.1.7

Index:
`/hobbyregister/?hr_letter=S`

PASS:
- Version 1.1.7;
- S aria-current;
- aktiver S-CSS;
- Hobbys-Zähler;
- Pagination oben;
- Pagination unten;
- Register-Startseitenlink;
- alter Reset-Text nicht vorhanden.

Profil:
`/hobbyregister/3d-druck/`

PASS:
- Version 1.1.7;
- Article-Block vorhanden;
- erster Abschnitt vorhanden;
- letzter Abschnitt vorhanden;
- mindestens 8 H2 im Artikel;
- Rendergröße 24.298 Bytes.

PHP-Lint 4/4 + Fresh-Unpack PASS.

## Deployment-Regel

Weil ein vollständiges Löschen/Ersetzen eines aktiven Pluginordners WordPress während des Zwischenzustands deaktivieren kann, 1.1.7 nicht mit einem Löschfenster deployen:
**bestehenden aktiven Ordner `hd-hobbyregister-core` beibehalten und den vollständigen 1.1.7-Ordner darüber kopieren/überschreiben.**

Wenn live danach weiterhin kein Artikel erscheint, ist als Erstes der Aktivstatus von `Hobby Depot Hobbyregister Core` in WordPress zu prüfen.
