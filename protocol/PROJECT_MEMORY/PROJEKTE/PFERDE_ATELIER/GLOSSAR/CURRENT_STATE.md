# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: EINZELARTIKEL LIVE PASS / 0 FLIESSTEXTLINKS LIVE PASS / DUENNE OCKERLINIE LIVE PASS / BREADCRUMB-TOPABSTAND + HERO-UEBERGANG/AUSSCHNITT LIVE FAIL / KACHELKLICK LIVE-NACHPRUEFUNG OFFEN / DESIGN 1.50.492 LOKAL POSITIV+NEGATIV PASS

## Belastbarer aktueller Stand

- Arbeitsbranch: `hobbyroom/glossar-livefail-red-green-20260913`.
- Einzelbegriffe öffnen real: **LIVE PASS**.
- Glossar-Fließtext 0 Links: **LIVE PASS**.
- rechte Ocker-Oberkante dünn: **LIVE PASS**.
- Diese bestätigten PASS-Punkte nicht erneut verändern.

## Aktuell offen – Nutzerreadback 2026-09-14 nach 1.50.491

1. Breadcrumb-Inhalt ist korrekt; **Abstand nach oben ist weiterhin falsch/zu groß**. Nutzerpflicht: an den anderen Seiten orientieren und auf allen Glossarseiten exakt dieselbe zentrale Abstandsteuerung verwenden.
2. Hero: **weicher Übergang zwischen Fläche und Bild fehlt** und Motiv muss **noch weiter herausgezoomt** werden.
3. Ganze Begriffskachel wurde in 1.50.491 technisch als Link umgesetzt, hat aber noch keinen ausdrücklichen LIVE-PASS des Nutzers und bleibt bis Readback in Nachprüfung.

## Nachgewiesene Ursache Breadcrumb-Abstand

Der Glossar-Code 1.50.491 enthielt weiterhin eine eigene feste Regel `padding-top:18px` für `category-glossar`, `tax-uge_group` und `single-uge_term`. Normale Seiten/Kategorien verwenden dagegen zentral `var(--pftk-navigation-content-gap)`. Dadurch konnte Glossar nicht garantiert exakt denselben real konfigurierten Abstand wie andere Seiten übernehmen.

## Lokaler Design-Kandidat 1.50.492

Paket: `PFERDE_ATELIER_DESIGN_V1.50.492_GLOSSAR_SPACING_HERO_HARDFIX_INSTALLIEREN.zip`

SHA-256: `7a016fda183874160fc303e3c6279adc3fec6475cc60cd617159e20913c42161`

Geändert:
- Glossar-Startseite, `uge_group` und `uge_term` verwenden jetzt **dieselbe zentrale Variable `--pftk-navigation-content-gap` wie normale Seiten/Kategorien**; keine eigene 18-px-Sonderregel mehr.
- Hero wird weiter herausgezoomt: Desktop-Skalierung `.86`, mobil `.82`, zusätzlich kleinerer Medienbereich.
- weicher Bild/Fläche-Übergang über CSS-Maskenverlauf plus Creme-Overlay.
- komplette Begriffskachel bleibt vollständiger `<a>`-Link.
- 0-Link-Endschranke und 2-px-Ockerlinie bleiben unverändert.

Hart lokal ausgeführt:
- PHP-Lint → PASS.
- Positivvertrag: zentrale Abstandvariable bei normalen Seiten **und** allen drei Glossarkontexten → PASS.
- Negativvertrag: absichtlich alte `18px`-Sonderregel wieder eingesetzt → Test wird korrekt rot → PASS.
- Hero-Positivvertrag: Zoom-out + Maskenverlauf vorhanden → PASS.
- Hero-Negativvertrag: Maskenverlauf absichtlich entfernt → Test wird korrekt rot → PASS.
- Geometriecheck Asset 1400×560: vorheriger Vollhöhen-Contain ca. 595×238; Kandidat ca. 440×176 → weiter herausgezoomt → PASS.
- komplette Kachel als Anchor, 0-Link-Guard und 2-px-Ockerlinie als Regression geprüft → PASS.
- ZIP-Lesetest → PASS; Version 1.50.492 → PASS.

Marker: `DESIGN_150492_POS_NEG_PASS`.

## Core / neue Beiträge

Core-Kandidat `1.2.3` mit `Aalstrich` (Bestand überschreiben) und `Zuchtbuch` (neu), beide aus WDB `GEPRUEFT`, bleibt unverändert. Kein neuer fachlicher Inhalt aus diesem Design-Fix ableiten.

## Harte Grenze

**1.50.492 ist lokal geprüft, aber noch kein LIVE PASS.** Erst Installation und realer Readback dürfen Breadcrumb-Abstand/Hero schließen.

## Nächster Schritt

1. Design `1.50.492` über 1.50.491 installieren.
2. Glossar-Startseite gegen eine normale Seite/Kategorie vergleichen: Navigationsunterkante → Breadcrumb muss sichtbar denselben Abstand haben.
3. zusätzlich `uge_group` und `Bandmaß` prüfen: derselbe Abstand.
4. Hero prüfen: weicher Übergang links und deutlich mehr Gesamtmotiv.
5. ganze Begriffskachel außerhalb von `Zum Begriff` anklicken.
6. Regression: 0 Fließtextlinks und dünne Ockerlinie bleiben PASS.
