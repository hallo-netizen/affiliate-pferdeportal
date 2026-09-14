# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-14
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13 – gilt für damaligen Hero-Abstand; aktueller Breadcrumb-Topabstand separat in 011.

## GLOSSAR-FE-002 – Hero-Bild / Bildausschnitt / Übergang
STATUS: LIVE FAIL / 2026-09-14 / KANDIDAT 1.50.492 LOKAL POSITIV+NEGATIV PASS

Aktueller Nutzerreadback nach 1.50.491:
- weicher Übergang zwischen Fläche und Bild fehlt;
- Motiv muss noch weiter herausgezoomt werden.

Kandidat 1.50.492:
- Medienbereich kleiner;
- Bildskalierung `.86` Desktop / `.82` mobil;
- CSS-Maskenverlauf plus Creme-Overlay für weichen Übergang.

Harte lokale Prüfung:
- Positivvertrag Zoom-out + Maskenverlauf → PASS;
- Negativvertrag: Maske absichtlich entfernt → Test wird rot → PASS;
- Geometrie: alter sichtbarer Bildkörper ca. 595×238, Kandidat ca. 440×176 → weiter herausgezoomt.

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung
STATUS: FRÜHER LIVE FAIL / SPÄTERE TECHNISCHE REGRESSION PASS / LIVE-NEUBEWERTUNG OFFEN

## GLOSSAR-ROUTE-004 – Einzelbegriffe öffnen
STATUS: LIVE PASS / 2026-09-14

Nicht anfassen.

## GLOSSAR-SINGLE-011 – Einzelansicht / Glossar-Navigation
STATUS: TEILWEISE LIVE PASS / REST LIVE FAIL / KANDIDAT 1.50.492 LOKAL POSITIV+NEGATIV PASS

### LIVE PASS – nicht regressieren

- Glossar-Fließtext: **0 Links**.
- rechte Ocker-Oberkante: **dünn / PASS**.
- Breadcrumb-Inhalt auf `Bandmaß`: korrekt `Startseite > Glossar > Pferd & Biologie > Bandmaß`.

### REST-LIVE-FAIL

1. **Breadcrumb-Abstand nach oben weiterhin falsch/zu groß.** Nutzerpflicht: auf Glossar-Startseite, `uge_group` und `uge_term` exakt an den anderen Seiten orientieren.
2. Ganze Begriffskachel wurde technisch als vollständiger Anchor umgesetzt, bleibt aber bis ausdrücklichem Nutzerreadback in Nachprüfung.
3. Hero-Übergang/Ausschnitt siehe `GLOSSAR-FE-002`.

### Nachgewiesene Ursache Breadcrumb-Abstand

1.50.491 enthielt trotz vorherigem Fix noch eine eigene feste Glossar-Regel `padding-top:18px`.
Normale Seiten/Kategorien verwenden zentral `var(--pftk-navigation-content-gap)`.
Die Glossar-Sonderregel war deshalb architektonisch falsch: sie folgte nicht zwingend dem real konfigurierten Seitenabstand.

### Lokaler Kandidat 1.50.492

- die drei Glossar-Kontexte verwenden dieselbe zentrale Variable wie normale Seiten/Kategorien;
- keine feste `18px`-Sonderregel mehr;
- ganze Begriffskachel bleibt kompletter `<a>`-Link;
- 0-Link-Endschranke und 2-px-Ockerlinie unverändert.

Harte lokale Prüfung:
- Positiv: zentrale Variable bei normaler Seite/Kategorie + allen Glossarkontexten → PASS;
- Negativ: alte feste 18-px-Regel absichtlich wieder eingebaut → Test erkennt den Fehler → PASS;
- PHP-Lint, ZIP-Lesetest, Version 1.50.492 → PASS;
- Marker `DESIGN_150492_POS_NEG_PASS`.

Paket-SHA-256:
`7a016fda183874160fc303e3c6279adc3fec6475cc60cd617159e20913c42161`.

## GLOSSAR-PROD-012 – Neue Glossarbeiträge nur aus WDB `GEPRUEFT`
STATUS: KANDIDAT 1.2.3 LOKAL PASS / LIVE-NACHPRÜFUNG OFFEN

- `Aalstrich` → WDB `GEPRUEFT`; Bestand aktualisieren.
- `Zuchtbuch` → WDB `GEPRUEFT`; neu ergänzen.

Keine weiteren ungeprüften Begriffe erzeugen.

## PASS-GRENZE

Kein LIVE PASS für Design 1.50.492 vor realer Installation und Readback.
Pflichtreadback:
- Glossar-Startseite, Gruppe und Single: Navigationsunterkante → Breadcrumb entspricht anderen Seiten;
- Hero: weicher Übergang und weiter herausgezoomt;
- Kachel außerhalb des CTA klickbar;
- 0 Fließtextlinks und dünne Ockerlinie bleiben PASS.
