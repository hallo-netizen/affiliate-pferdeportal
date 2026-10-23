# HD-003 – EVIDENCE 1.50.721

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / NICHT LIVE ABGENOMMEN

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.721_UPDATE_MAGAZIN_BANNER_ZIELSEITEN_FIX.zip`

SHA-256:
`c81f278aec7b4f80a57045269877f5df760d7e97cc4d2bace07e79e1320a93bd`

Größe:
2,103,461 Bytes.

## Korrektur gegenüber 1.50.720

### Magazin-Startseite
- Die 12 Themenkacheln werden jetzt wirklich von Werbeflächen durchsetzt.
- Entscheidung: durchgehende Werbeflächen statt Ersetzen einzelner Themenkacheln.
- Reihenfolge Desktop:
  - 6 Themenkacheln;
  - `journal_banner` über volle Rasterbreite;
  - 3 Themenkacheln;
  - direkte Werbefläche `journal` über volle Rasterbreite;
  - 3 Themenkacheln.
- Auf Mobil bleiben beide Werbeflächen ebenfalls über die volle Kachelbreite.
- Der Banner im Bereich "Neu im Magazin" wird auf der Magazin-Startseite nicht zusätzlich dupliziert.
- Auf den Magazin-Zielseiten bleibt der Banner zwischen den Beitragsreihen erhalten.

### Magazin-Zielseiten
- Alle 12 Zielseiten bleiben eigene bestehende Editorial-Seiten.
- Hero wird weiterhin aus exakt derselben zentralen Bilddefinition wie die jeweilige Startseitenkachel erzeugt.
- Zusätzlich liegt jetzt ein `the_content`-Fallback vor, falls das Theme/Template-Routing die Owned-Content-Route nicht übernimmt.
- Target-Hero-Medien werden gegen Legacy-CSS explizit sichtbar gehalten.
- Der bestehende grüne Lead-Bereich und der native Aufklapper bleiben direkt unter dem Hero.
- Schreibschrift/Brush wird weiterhin über denselben bestehenden Hub2-Hero-Vertrag erzeugt.

## Bildsicherheit

Das UPDATE liefert diesmal die 12 verwendeten Magazin-Hero/Kachelbilder physisch mit, zusätzlich den bestehenden Brush:
- suchen-finden.webp
- alltagsobjekte.webp
- papier-dokumente.webp
- citizen-science.webp
- werbung-design.webp
- naturbeobachtung.webp
- digitale-fertigung.webp
- outdoor.webp
- ameisen-insekten.webp
- spielzeug-spiele.webp
- buch-papier.webp
- mechanik-uhren.webp
- brush-underline-v150641.webp

Damit hängt der Hero nicht davon ab, ob diese Assets bereits im älteren FULL-Stand auf dem Server vorhanden sind.

## Paket

Fester Hauptordner:
`affiliate-portal-template-kit/`

16 Dateien:
- 2 geänderte PHP-Dateien;
- 1 vorhandenes Content-Template zur Routing-Absicherung;
- 12 Hero/Kachelbilder;
- 1 Brush-Asset.

## QA

- PHP-Lint vor Packen: PASS.
- Fresh-Unpack + PHP-Lint: PASS.
- 12/12 Magazin-Definitionen vorhanden.
- 12/12 definierte Bildassets physisch im UPDATE vorhanden.
- exemplarischer Zielseiten-Render `Menschen & Geschichten`:
  - Hero-IMG PASS;
  - identisches Asset `naturbeobachtung.webp` PASS;
  - Brush-Claim PASS;
  - Hero-Titel PASS;
  - grüne Lead-Box-Klasse PASS;
  - `details`-Aufklapper PASS.
- Kachel-Ads nach 6 und 9 Elementen im Code gebunden: PASS.
- Root-Feed dupliziert den Journal-Banner nicht: PASS.
- FAQ/PB-one-Änderungen bleiben erhalten.

Kein Live-PASS behaupten.
