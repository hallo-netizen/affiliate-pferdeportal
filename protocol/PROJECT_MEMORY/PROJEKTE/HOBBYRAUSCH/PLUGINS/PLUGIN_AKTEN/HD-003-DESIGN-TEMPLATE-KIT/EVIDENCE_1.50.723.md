# HD-003 – EVIDENCE 1.50.723

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.723_UPDATE_MAGAZIN_BREADCRUMBS.zip`

SHA-256:
`d0839a73d42008548f777ba0f2d56975ec0f2acef4f921590894ca8f4472d8d0`

Größe:
586,379 Bytes.

## Live beanstandeter Fehler

Auf den Magazin-Zielseiten fehlten nach der 1.50.722-Hardroute die Breadcrumbs.

## Ursache

Die Zielseiten-Hardroute funktioniert absichtlich auch dann, wenn WordPress den Request nicht als `is_singular('page')` klassifiziert.

Die Breadcrumb-Funktion hing jedoch weiterhin an `is_singular()`.
Im Hardroute-Fall blieb deshalb nur der Startseiten-Eintrag übrig; bei weniger als zwei Einträgen wurde der komplette Breadcrumb ausgeblendet.

## Fix

`breadcrumb_items()` verwendet für die 12 Magazin-Zielseiten jetzt dieselbe URL-Hardroute wie das Zielseiten-Template.

Ausgabe:
`Startseite › Magazin › <Zielseite>`

Die Magazin-Hub-URL wird aus der bestehenden Seite `magazin`/Fallback `journal` ermittelt. Der aktuelle Zielseitentitel wird aus der realen Seite gelesen, mit Definition als Fallback.

## QA

Failure-Mode wie beim Zielseitenfehler:
- `is_singular() = false`
- echte URL `/magazin/<slug>/`

Ergebnis:
**12/12 Magazin-Zielseiten Breadcrumb PASS.**

Zusätzlich:
- Fresh-Unpack PASS
- PHP-Lint beide Dateien PASS
- ZIP exakt 2 Dateien PASS
- Hauptordner `affiliate-portal-template-kit` PASS

Kein Live-PASS behaupten.
