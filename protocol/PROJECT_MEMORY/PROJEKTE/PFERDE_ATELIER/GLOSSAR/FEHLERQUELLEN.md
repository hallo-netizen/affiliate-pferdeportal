# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-14
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13 – gilt für damaligen Hero-Abstand; neuer Breadcrumb-Topabstand separat in 011.

## GLOSSAR-FE-002 – Hero-Bild / Bildausschnitt
STATUS: LIVE FAIL / 2026-09-14

Aktueller Nutzerreadback: Hero-Bild ist zu stark beschnitten/zu nah; Motiv ist nicht ausreichend erkennbar. Kandidat 1.50.491 stellt von `cover` auf `contain`, rechts ausgerichtet.

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung
STATUS: FRÜHER LIVE FAIL / SPÄTERE TECHNISCHE REGRESSION PASS / LIVE-NEUBEWERTUNG OFFEN

## GLOSSAR-ROUTE-004 – Einzelbegriffe öffnen
STATUS: LIVE PASS / 2026-09-14

Nicht anfassen.

## GLOSSAR-SINGLE-011 – Einzelansicht / Glossar-Navigation
STATUS: TEILWEISE LIVE PASS / REST LIVE FAIL / KANDIDAT 1.50.491 LOKAL PASS

### LIVE PASS – nicht regressieren

- Glossar-Fließtext: **0 Links**.
- rechte Ocker-Oberkante: **dünn / PASS**.
- Breadcrumb-Inhalt auf `Bandmaß`: korrekt `Startseite > Glossar > Pferd & Biologie > Bandmaß`.

### REST-LIVE-FAIL

1. **Breadcrumb-Abstand nach oben zu groß.** Pflicht: auf Glossar-Startseite, `uge_group` und `uge_term` einheitlicher Abstand.
2. **Begriffskacheln nur teilweise klickbar.** Pflicht: gesamte Kachel als Link.
3. **Hero-Ausschnitt zu nah/beschnitten.** Pflicht: herauszoomen, Gesamtmotiv verständlich sichtbar.

### Lokaler Kandidat 1.50.491

- einheitlicher `.site-content`-Topabstand 18 px für die drei Glossar-Seitentypen;
- Single-Innenpadding verhindert doppelte Topaddition;
- `<article>`-Kachel zu vollständigem Link umgebaut;
- Hero `object-fit: contain; object-position: right center`;
- 0-Link-Endschranke und 2-px-Ockerlinie unverändert erhalten;
- PHP-Lint / statischer Positiv-Negativvertrag / ZIP-Lesetest PASS.

## GLOSSAR-PROD-012 – Neue Glossarbeiträge nur aus WDB `GEPRUEFT`
STATUS: KANDIDAT 1.2.3 LOKAL PASS / LIVE OFFEN

Frisch aus der autoritativen WDB gelesen:
- `Aalstrich` → `GEPRUEFT`; wird als Bestandsbegriff überschrieben/aktualisiert.
- `Zuchtbuch` → `GEPRUEFT`; wird neu ergänzt.

Kandidat 1.2.3 enthält damit 16 gebundene Begriffe. Beide neuen/ergänzten Texte: 150–200 Wörter, 0 Fließtextlinks, lokale Syntax-/Vertrags-/ZIP-Prüfung PASS.

## PASS-GRENZE

Kein LIVE PASS für 1.2.3 / 1.50.491 vor realer Installation und Readback.
