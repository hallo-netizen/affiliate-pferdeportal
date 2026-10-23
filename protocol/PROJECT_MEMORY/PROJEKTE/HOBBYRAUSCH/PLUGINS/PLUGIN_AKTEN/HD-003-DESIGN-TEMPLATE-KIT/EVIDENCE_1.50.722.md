# HD-003 – EVIDENCE 1.50.722

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.722_UPDATE_MAGAZIN_ZIELSEITEN_HARDROUTE.zip`

SHA-256:
`15e0bfa3fc861cf1dee11c8a8059d10dad4c743d4f52efeff28f091a233b184e`

Größe:
2,104,172 Bytes.

## Live beanstandeter Fehler

1.50.721 zeigte auf den Magazin-Zielseiten weiterhin das alte Layout.
Hero, Zielseiten-Template und grüne Intro-/Aufklappdarstellung griffen dort live nicht.

## Reproduzierter Ausfallmodus

Die bisherige Zielseitenbindung hing an der WordPress-Seitenklassifikation:
`is_singular('page')` + Queried Object.

Explizite Fehlersimulation:
- `is_singular('page') = false`
- reale URL `/magazin/<zielslug>/`

Ergebnis mit 1.50.721:
**0/12 Zielseiten übernehmen das HD-003-Content-Template.**

Damit ist genau ein realer Ausfallmodus der bisherigen Architektur reproduziert.

## Fix 1.50.722

Die 12 bekannten Magazin-Zielseiten werden zusätzlich eng über ihre realen URL-Pfade gebunden:

`/magazin/<zielslug>/`
oder historisch/fallback
`/journal/<zielslug>/`

Nur die exakt 12 definierten Zielslugs werden akzeptiert.

Die URL-Erkennung läuft vor der WordPress-Seitenklassifikation in:
- `template_include` / Owned-Route;
- `render_owned_content()`;
- `the_content`-Fallback.

Damit ist die Zielseitenausgabe nicht mehr davon abhängig, ob ein anderer Bestandteil die Query-Klassifikation verändert.

## Harte Simulation nach Fix

Gleicher Failure-Mode-Test mit `is_singular('page') = false`:

- Hobbyfinder PASS
- Alter & Lebensphasen PASS
- Geschichte & Herkunft PASS
- Hobby-Porträts PASS
- Hobby-Ideen & Inspiration PASS
- Menschen & Geschichten PASS
- Neue Hobbys & Trends PASS
- Saison, drinnen & draußen PASS
- Ungewöhnliche & skurrile Hobbys PASS
- Vergleiche & Alternativen PASS
- Wissen & Glossar PASS
- Zeit, Budget & Platz PASS

**12/12 PASS.**

Negativtest:
`/irgendwas/geschichte-herkunft/` wird nicht übernommen: PASS.

## Zielseiten-Renderprüfung

11 normale Magazin-Zielseiten wurden ohne WordPress-Seitenerkennung direkt aus ihrem URL-Slug gerendert.

Je Seite geprüft:
- Hardroute-Marker;
- Hero;
- Hero-Bild;
- Brush/Schreibschrift;
- grüne Lead-Box;
- nativer Details-Aufklapper;
- Magazin-CSS.

Ergebnis:
**11/11 vollständig PASS.**

Hobbyfinder wurde separat in der 12/12-Routenprüfung erfasst; sein Funnel bleibt Sonderinhalt unter derselben Magazinhülle.

## Paket

16 Dateien, Hauptordner unverändert:
`affiliate-portal-template-kit/`

- 2 PHP-Dateien;
- 1 Content-Template;
- 12 Magazin-Hero/Kachelbilder;
- 1 Brush-Asset.

Fresh-Unpack:
- PHP-Lint PASS;
- 13/13 Assets vorhanden;
- Hauptordner PASS.

Kein Live-PASS behaupten.
