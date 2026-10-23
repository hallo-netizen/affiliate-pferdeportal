# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **MAGAZIN-ZIELSEITEN 1.50.722 HARDROUTE / BREADCRUMBS LIVE FEHLEND / 1.50.723 LOKAL HARD PASS**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Aktueller Fehler

Magazin-Zielseiten wurden über die 1.50.722-Hardroute korrekt übernommen, aber der Breadcrumb fehlte.

Ursache:
Der Breadcrumb hing noch an der normalen WordPress-`is_singular()`-Klassifikation, während die Zielseiten bewusst unabhängig davon geroutet werden.

## Kandidat 1.50.723

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.723_UPDATE_MAGAZIN_BREADCRUMBS.zip`

SHA-256:
`d0839a73d42008548f777ba0f2d56975ec0f2acef4f921590894ca8f4472d8d0`

Fix:
**Startseite › Magazin › jeweilige Zielseite**

Direkt über dieselbe reale URL-Hardroute wie das Zielseiten-Template.

QA:
**12/12 Zielseiten PASS**, selbst bei absichtlich ausgeschalteter normaler WordPress-Seitenerkennung.

## EXAKT EINE NEXT ACTION

**1.50.723 einspielen und live eine Magazin-Zielseite vollständig abnehmen.**
