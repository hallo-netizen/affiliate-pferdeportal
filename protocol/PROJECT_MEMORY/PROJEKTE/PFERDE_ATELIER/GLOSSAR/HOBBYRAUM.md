# GLOSSAR – HOBBYRAUM

STAND: 2026-09-14
STATUS: BLOCKED

## AKTUELLER SICHERER BEFUND

LIVE PASS und **nicht mehr anfassen**:
- Einzelartikel öffnen;
- Glossar-Fließtext enthält 0 Links;
- rechte Ockerlinie ist dünn.

LIVE offen nach Nutzerreadback 1.50.491:
- Breadcrumb-Abstand nach oben weiterhin falsch/zu groß;
- Hero-Übergang Fläche→Bild fehlt; noch weiter herauszoomen;
- komplette Begriffskachel bleibt bis ausdrücklichem Nutzerreadback in Nachprüfung.

## NACHGEWIESENE URSACHE BREADCRUMB

1.50.491 hatte für die drei Glossar-Kontexte weiterhin eine feste Sonderregel `padding-top:18px`.
Andere Seiten/Kategorien verwenden zentral `var(--pftk-navigation-content-gap)`.
Damit konnte Glossar trotz gleichem Zahlenwert nicht verbindlich der realen Seitenkonfiguration folgen.

## ARBEITSORT

Branch: `hobbyroom/glossar-livefail-red-green-20260913`

Autorität:
- `CURRENT_STATE.md`
- `FEHLERQUELLEN.md`
- `TEXT_UND_LINKREGELN.md`
- Fachfakten ausschließlich WDB Glossar.

## LOKALER DESIGN-KANDIDAT 1.50.492

`PFERDE_ATELIER_DESIGN_V1.50.492_GLOSSAR_SPACING_HERO_HARDFIX_INSTALLIEREN.zip`

SHA-256: `7a016fda183874160fc303e3c6279adc3fec6475cc60cd617159e20913c42161`

- Glossar übernimmt nun dieselbe zentrale Topabstandsvariable wie normale Seiten/Kategorien; keine 18-px-Sonderregel mehr.
- Hero weiter herausgezoomt (`.86` Desktop / `.82` mobil) und kleinerer Bildbereich.
- weicher Bildübergang per Maskenverlauf + Creme-Overlay.
- ganze Begriffskachel bleibt vollständiger Link.
- 0-Link-Regel und 2-px-Ockerlinie unverändert.

## HARTE LOKALE PRÜFUNG

PASS:
- PHP-Lint.
- Positiv: normale Seiten und alle Glossarkontexte nutzen dieselbe zentrale Abstandvariable.
- Negativ: alte `18px`-Sonderregel absichtlich wieder eingesetzt → Test erkennt Fehler.
- Positiv Hero: Zoom-out + Übergangsmaske vorhanden.
- Negativ Hero: Maske absichtlich entfernt → Test erkennt Fehler.
- Hero-Geometrie: vorher ca. 595×238 sichtbarer Bildkörper, Kandidat ca. 440×176.
- Regression: ganze Kachel Anchor, 0-Link-Guard, 2-px-Ockerlinie.
- ZIP-Lesetest und Version 1.50.492.

Marker: `DESIGN_150492_POS_NEG_PASS`.

## CORE / BEITRÄGE

Core 1.2.3 bleibt unverändert: `Aalstrich` WDB-geprüft aktualisieren, `Zuchtbuch` WDB-geprüft neu. Dieser Design-Fix erzeugt keine zusätzlichen Fachbegriffe.

## NEXT ACTION – EXAKT

1. Design `1.50.492` über 1.50.491 installieren.
2. Glossar-Startseite direkt mit einer normalen Seite/Kategorie vergleichen: Abstand Navigationsunterkante → Breadcrumb muss identisch sein.
3. eine Glossar-Gruppe und `Bandmaß` gegenprüfen: derselbe Abstand.
4. Hero prüfen: weicher Übergang und klar weiter herausgezoomtes Motiv.
5. Kachel außerhalb `Zum Begriff` klicken.
6. Regression: 0 Fließtextlinks und dünne Ockerlinie bleiben PASS.
7. Erst nach Nutzerreadback LIVE PASS.

## NICHT ANFASSEN

- funktionierenden Routingweg;
- normale Posts/Seiten;
- 0-Link-Regel;
- dünne Ockerlinie;
- ungeprüfte WDB-Begriffe.
