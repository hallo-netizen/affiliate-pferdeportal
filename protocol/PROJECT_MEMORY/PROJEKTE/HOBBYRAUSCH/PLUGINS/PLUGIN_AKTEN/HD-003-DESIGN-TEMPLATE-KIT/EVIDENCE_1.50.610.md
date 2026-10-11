# HD-003 – EVIDENCE 1.50.610

STATUS: LOCAL HARD PASS / LIVE OFFEN

ARTEFAKT:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.610_HOBBY_DEPOT_HOMEPAGE_FINAL_LOCALPASS.zip`

SHA-256:
`c26ff929fa02a451dd4b7e7b9e6b2aa4dd42c2752bd261f13c134401389512a3`

## Fresh-Paket

- ZIP-Integrität: PASS
- Fresh-Unpack PHP-Lint: 9/9 PASS
- Verhaltenstest Positiv/Negativ: PASS

## Sichtbarkeitsmatrix

Öffentlich / Affiliate leer:
- Produkte: unsichtbar PASS
- Affiliate-Banner: unsichtbar PASS
- direkt verkaufbarer Werbeplatz: einmal sichtbar PASS

Eingeloggt / Affiliate leer:
- 3 Produkt-Arbeitsplätze sichtbar PASS
- 1 Banner-Arbeitsplatz sichtbar PASS
- klar als nur eingeloggt sichtbar markiert PASS

Affiliate belegt:
- reale Inhalte sichtbar PASS
- keine Leerplatzhalter zusätzlich PASS

Direktwerbung:
- unverkauft: „Werbeplatz verfügbar“ PASS
- gebucht: Kampagne ersetzt Verfügbarkeitsplatz PASS
- maximal ein Platz pro Request PASS
- keine Anzeige im Header PASS

## Marke / Header

- Logoquelle unverändert: `logo-variant3-v150600.png`
- Topbar-Inhalt unverändert
- Topbar mittig
- Body weiß
- Header warm-off-white
- Suche weiß
- kein Shop-/Community-/Newsletter-Noise

## Hero

- eingebrannter Schriftzug bleibt erhalten
- Desktop-Safe-Crop 1370×620
- Tablet/Mobile-Safe-Crop 1240×620
- unter 1100 px gestapelte Darstellung

## Weltmotive

8/8:
- Gestalten
- Fertigen
- Technik
- Forschen
- Pflanzen
- Tiere
- Bewegen
- Sammeln

Prüfung:
- 8/8 exakt 1400×620
- 8/8 unterschiedliche SHA-256
- native hochauflösende Ausgangsbilder
- fachlich gegen reale Weltinhalte abgeglichen
- als gemeinsame Startseiten-/spätere Heroquelle ausgelegt
- Tiere ohne dekorativen Rahmen und ohne Hund-/Haustierclaim

## Startseitenreihenfolge

Hero → 8 Welten → Editorial → Affiliate-Banner → Magazin/Themen → Produkte → direkt verkaufbarer Werbeplatz → Footer.

PASS lokal.

## Live-Grenze

Kein Live-PASS behauptet.

NEXT:
1.50.610 installieren und vollständige Startseite Desktop/Tablet/Mobile live prüfen.
