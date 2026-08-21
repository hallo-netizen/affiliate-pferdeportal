# V98 Hard Local QA

- PHP-Lint Pferde: 4/4 PHP-Dateien PASS.
- PHP-Lint Universal: 11/11 PHP-Dateien PASS.
- JSON Pferde: 15/15 PASS.
- Scope-Harness positiv: registrierte Journal-Kategorie erhält `remove-featured-img-padding` und `pftk-journal-card-v150463`.
- Scope-Harness negativ: fremde Kategorie bleibt unverändert.
- Journal-Root-Quellblock bestätigt `padding:20px` als Referenztoken.
- Browser-Geometrie-Fixture mit simuliertem Astra-20-px-Wrapper: Bild bündig zur Karteninnenkante; Bild → Meta exakt 20 px; Button → Kartenunterkante 21 px inklusive 1-px-Rahmen.
- Negative Browser-Fixture: Fremdkategorie behält das simulierte Astra-Padding (21 px inklusive Rahmen).
- Fresh-Unpack Pferde: 492/492 Source-Dateien byteidentisch.
- Fresh-Unpack Universal: 15/15 Source-Dateien byteidentisch.
- Pferde-Master-Manifest: 716/716 verifiziert.
- Universal-Master-Manifest: 238/238 verifiziert.
- Journal-Root-Styleblock: byteidentisch zu V97.
- Single-Post-Tabellen-CSS: byteidentisch zu V97.

Reale Live-Sichtprüfung bleibt nach Installation erforderlich; vorher kein endgültiger Live-PASS.