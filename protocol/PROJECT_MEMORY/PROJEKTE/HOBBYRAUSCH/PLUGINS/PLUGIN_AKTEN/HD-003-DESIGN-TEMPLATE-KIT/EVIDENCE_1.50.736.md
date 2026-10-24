# HD-003 – EVIDENCE 1.50.736

STAND: 2026-10-24
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.736_SERVICE_PAGES_LAYOUT_HARDPASS.zip`

SHA-256:
`9f395cc4481e758a675536ab592ac2e686a53d2513ad729f92a22e6c7a678a38`

## Live-Beanstandungen
- zu großer Abstand zwischen Service-Hero und Seiteninhalt;
- Preise: Tabellen schmal, nicht über komplette Inhaltsbreite;
- Preise: Fett-Zwischenüberschriften ohne sauberen Rhythmus;
- Disclaimer: Fett-Zwischenüberschriften ohne Abstand.

## Ursache
- Disclaimer besteht aus einem Kubio-Textblock mit `<strong>Überschrift</strong><br>Text...` statt echten h2/h3-Elementen.
- Preise enthält Tabellen in mehrfach verschachtelten Kubio Section/Row/Column-Hüllen; `width:100%` nur am `table` reichte deshalb nicht.

## Korrektur
- Hero→Inhalt zentral 18 px Desktop / 16 px mobil.
- Preise: komplette DOM-Ahnen der Tabellen bis `.entry-content` werden als breite Tabellenhüllen markiert und auf 100 % gesetzt.
- Tabellen 100 %, linksbündig, responsive horizontal scrollbar.
- Preis-Zwischenüberschriften gezielt per Textidentität erkannt; Inline-Fettungen bleiben unangetastet.
- Disclaimer-`strong+br`-Überschriften strukturell erkannt und als Blocküberschriften formatiert.

## QA
- Testdaten: echter Footer-Umzug `preise` + `disclaimer`.
- Preise: 3/3 Tabellen volle Inhaltsbreite im Chromium-Fixture.
- Preise: 6 relevante Zwischenüberschriften erkannt.
- Disclaimer: 9/9 Zwischenüberschriften erkannt.
- Hero→Inhalt gemessen: 18 px bei 1600/1024, 16 px bei 760/390.
- PHP 11/11 PASS.
- ZIP CRC PASS.
- Fresh-Unpack 936 Dateien Source↔ZIP bytegleich.
