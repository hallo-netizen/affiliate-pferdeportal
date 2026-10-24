# HD-003 – EVIDENCE 1.50.740

STAND: 2026-10-24
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.740_SERVICE_TEMPLATE_BODY_TABLES_HARDPASS.zip`

SHA-256:
`133db11baf242e9f9a8d9cc17d8fe482bd13fb50af78c16dec49d67445de4825`

## Reproduzierte Live-Abweichung
- serverseitige Inhaltsnormalisierung sichtbar, aber Body blieb schmal;
- Tabellen blieben schmal und nicht hero-buendig;
- aus strong-Zeilen erzeugte h2/h3 waren zu gross.

## Ursache
Die Seiten liefen weiterhin durch das normale WordPress/Theme-Seitentemplate. Damit blieb ausserhalb des normalisierten Inhalts eine schmale Theme-Achse aktiv.

## Korrektur
- eigenes Plugin-Template `hobby-depot-service-v150740.php`;
- Body direkt auf dieselbe Achse wie Service-Hero;
- Zwischenueberschriften = normaler Absatz + strong, keine h2/h3;
- Inline-Hardbreite an Figuren/Tabellen plus zentrale CSS-Regel.

## Fresh-Unpack-Messung
Viewport 1600:
- Hero x=200 / 1200
- Main x=200 / 1200
- Tabellen 3/3 x=200 / 1200

Viewport 1100:
- Hero/Main/Tabellen x=36 / 1028

Viewport 760:
- Hero/Main/Tabellen x=12 / 736

Viewport 390:
- Hero/Main/Tabellen x=12 / 366

Typografie:
- Preise 6/6 Zwischenueberschriften: 15.5 px, strong 15.5 px / 700, margin 30/18.
- Disclaimer 9/9: identisch.
- h2/h3 im normalisierten Service-Inhalt: 0.

QA:
- PHP 12/12 PASS
- ZIP CRC PASS
- Fresh-Unpack 937/937 Dateien bytegleich
