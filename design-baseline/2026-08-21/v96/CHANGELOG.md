# V96 – Journal-Unterkategorien-Fix

Datum: 2026-08-21

## Referenz
Verbindliche visuelle Referenz ist die bereits freigegebene Beitragskarte auf `/journal/`.

## Fehler in V95
- Einzelne Journal-Kategorie-Beitragskarten wurden zentriert statt im ersten Rasterplatz links angeordnet.
- Der native Astra-Archivpfad lieferte keinen zuverlässigen `Weiterlesen`-CTA.
- Damit wich die Unterkategorie trotz korrektem Tabellen- und Journal-Root-Stand vom bestätigten Standard ab.

## Pferde V1.50.461 / Contract V96
- Desktop 3 Spalten, Tablet 2, Mobil 1.
- Einzelkarte bleibt im ersten Rasterplatz links.
- Medienhöhe 205 px mit `object-fit: cover`.
- Kategorie-/Meta-Label `#C89214`.
- Titel, Auszug und CTA folgen der bestätigten Journal-Root-Kartensprache.
- Genau ein `Weiterlesen`-CTA wird über den offiziellen Astra-Hook `astra_entry_content_after` ergänzt.
- Eventuelle native Read-more-Doppelung wird ausschließlich im registrierten Journal-Kategorie-Scope ausgeblendet.
- Scope bleibt fail-closed über das bestehende exakte Journal-Kategorieregister.

## Universal V2.2.32 / Contract V96
- Journal-/Magazin-Term-Postgrid ebenfalls 3/2/1 statt zentriertem auto-fit-Einzelkartenlayout.
- Andere Archive und Grids bleiben unverändert.

## Preservation
- Pferde: 489/492 Produktionsdateien zu V95 byteidentisch.
- `single-post-locked-v15083.css` byteidentisch: Tabellenfix bleibt unverändert.
- kompletter `print_journal_system_css_v150368()`-Block byteidentisch: Journal-Root bleibt unverändert.
- Universal: 11/15 Dateien zu V95 byteidentisch; CSS-Diff ausschließlich Journal-Term-Grid plus Versionskommentar.

## QA
- PHP-Lint Source/Fresh-Unpack: PASS.
- Pferde Source↔Installer: 492/492 byteidentisch.
- Universal Source↔Installer: 15/15 byteidentisch.
- CTA-Scope-Harness: registrierte Journal-Kategorie erzeugt genau einen CTA; Fremdkategorie keinen – PASS.
- Browser-Fixture 1280 px: Grid und Einzelkarte gleicher linker X-Wert; CTA vorhanden; Meta-Farbe `rgb(200,146,20)` – PASS.
- Master-Manifeste Fresh-Unpack: Pferde 707/707 PASS; Universal 231/231 PASS.

## Live
Live-Sichtprüfung nach Installation bleibt bis zum Nutzerscreenshot PENDING.