# V99 – Journal-Unterkategorie exakt gegen Journal-Root

## Ausgangslage
V98 war live weiterhin FAIL. Die sichtbare ockerfarbene Kategorienzeile blieb praktisch direkt am Bild, obwohl der lokale V98-Harness einen 20-px-Abstand meldete. Damit war der Harness nicht repräsentativ genug für die reale Astra-Archivstruktur.

## Tatsächliche Ursache
1. Der sichtbare Kategoriename im Astra-Archiv stammt nicht zuverlässig aus genau dem Meta-Element, dessen Abstand V97/V98 verändert hatten. Der Harness prüfte deshalb ein falsches DOM-Modell.
2. Die Journal-Root-Karte reserviert für den Titel `min-height: 2.55em`. Die native Archivkarte hatte diese Reserve nicht. Dadurch war die Karte sichtbar kürzer und die gesamte Vertikalgeometrie entsprach nicht dem Standard.

## V99 Pferde-Plugin
Version: 1.50.464 / Contract V99.

- Native Astra-Meta wird ausschließlich in exakt registrierten Journal-Unterkategoriearchiven visuell unterdrückt.
- Das sichtbare ockerfarbene Journal-Kategorielabel wird kontrolliert aus dem aktuell abgefragten Journal-Term über den offiziellen Astra-Hook `astra_entry_header_before` ausgegeben.
- Der sichtbare Abstand ist damit nicht mehr von wechselndem Theme-Meta-Markup abhängig.
- Innengeometrie wird exakt auf die bestätigte Journal-Root-Karte gespiegelt:
  - Bild -> Label: 20 px
  - Label -> Titel: 7 px
  - Titelreserve: 2.55em
  - Titel -> Auszug: 10 px
  - Auszug-Abstand: 17 px
  - CTA: min. 150 x 42 px
  - CTA -> Kartenunterkante: 20 px Innenabstand + 1 px Rahmen
- Raster, Bildhöhe 205 px, object-fit cover, Farben und Hover bleiben im bestehenden Journal-Standard.
- Scope fail-closed: nur exakt registrierte Journal-Unterkategorien.

## Universal-Plugin
Version: 2.2.35 / Contract V99.

- Opt-in Journal-Term-Beitragskarten erhalten das Term-Label als eigenes `upds-card-meta`.
- Generic cards erhalten kein Meta-Label.
- Journal-Term-Karten übernehmen denselben 20/7/2.55em/10/17/150x42-Abstandsvertrag.

## Unverändert
- Journal-Root-Styleblöcke sind gegenüber V98 byteidentisch.
- `assets/single-post-locked-v15083.css` und damit der Tabellenfix sind gegenüber V98 byteidentisch.
- Suche, Breadcrumbs, Anzeigenmarkt, Inhalte, Titelentscheidungen und andere Kartenraster bleiben unberührt.

## Harte lokale Referenzprüfung
Eine Journal-Root-Referenzkarte und die V99-Archiv-Zielkarte wurden mit identischem Inhalt im Chromium-Browser gerendert. Nicht nur einzelne CSS-Tokens, sondern die reale Geometrie wurde verglichen.

Ergebnis:
- Bildhöhe: identisch
- Bildbreite: identisch
- Bild -> sichtbarer Meta-Text: 20 px / 20 px
- Meta -> Titel: 7 px / 7 px
- Titel -> Text: 10 px / 10 px
- Button -> Kartenunterkante: 21 px / 21 px inklusive 1-px-Rahmen
- Text-Innenkante: 21 px / 21 px inklusive Rahmen
- Gesamtkartenhöhe: identisch
- vollständiger Pixelvergleich: 0 unterschiedliche Pixel von 175680

Negativtest Fremdkategorie: keine Journal-Klasse, kein künstliches Meta, kein CTA, kein Journal-CSS.

## Paketprüfung
- Pferde Source: 492 Dateien
- Pferde Fresh-Unpack: 492/492 byteidentisch
- Universal Source: 15 Dateien
- Universal Fresh-Unpack: 15/15 byteidentisch
- Pferde-Master Fresh-Unpack: 727/727 Dateien byteidentisch
- Pferde-Master Manifest: 726/726 Einträge PASS
- Universal-Master Fresh-Unpack: 245/245 Dateien byteidentisch
- Universal-Master Manifest: 244/244 Einträge PASS
- Embedded Installer == Standalone Installer: PASS
- CURRENT_PLUGIN_SOURCE == embedded Installer: PASS
- ZIP-Tests aller vier Ausgaben: PASS

Live-WordPress-Akzeptanz bleibt bis zum Nutzer-Screenshot ausdrücklich PENDING.