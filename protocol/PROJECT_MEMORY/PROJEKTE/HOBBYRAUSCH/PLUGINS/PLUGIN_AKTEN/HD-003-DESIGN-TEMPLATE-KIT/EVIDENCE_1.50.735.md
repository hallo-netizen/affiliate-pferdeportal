# HD-003 – EVIDENCE 1.50.735

STAND: 2026-10-24
STATUS: LOCAL PASS / LIVE SICHTPRÜFUNG OFFEN

Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.735_SERVICE_PAGES_DESIGN_LOCALPASS.zip`

SHA-256:
`105a806d132aac186313c3e95e87e2791dfe9a31926d2924d4f4553a78d6045a`

## Scope
Einheitliches Design für Footer-/Service-Seiten:
Impressum, Disclaimer, Datenschutz, Werbebedingungen, Werben/Werbung im Hobby Depot, Preise, Kontakt, FAQ.

## Technische Änderung
- Service-Seiten erhalten zentrale Body-Klassen.
- gemeinsamer Hero mit bestehendem Asset `hero-masters-v150684/alltagsobjekte.webp`.
- kein Kicker „Hobby Depot“.
- kein Rahmen um Hero/Titel.
- Theme-/Astra-Doppeltitel auf Service-Seiten ausgeblendet.
- Preise: Tabellen + tabellenführende Gutenberg/Kubio-Wrapper 100 % Inhaltsbreite.
- Preise + Disclaimer: h2/h3/h4 sowie alleinstehende strong-Zwischenüberschriften mit definiertem vertikalem Rhythmus.

## QA
- Ziel-Slug-Erkennung PASS, inkl. `werben`, `werbung-im-hobby-depot`, `werbebedingungen`, `werb-anzeigebedingungen`.
- Hero-Asset vorhanden: 1600×587 WebP, 101266 Bytes.
- PHP 11/11 PASS.
- CSS-Brace-Balance PASS.
- ZIP CRC PASS.
- Fresh-Unpack: 936/936 Dateien bytegleich.
- Chromium-Lokaltest nicht als PASS gewertet, da die Laufzeit lokale file/http URLs durch Administratorregel blockiert.
