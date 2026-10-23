# HD-007 – EVIDENCE 1.1.2 BREADCRUMB + BANNER

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.2_UPDATE_BREADCRUMB_BANNER.zip`

SHA-256:
`d83cb6de965f495e07bdc2746013657f864bda93861bfcd188db63a1287ec96e`

Größe:
22.620 Bytes.

UPDATE mit exakt zwei Dateien unter dem bestehenden Hauptordner `hd-hobbyregister-core/`:
- `hobby-depot-hobbyregister-core.php`
- `includes/class-hd-hobbyregister-frontend.php`

## Änderungen

Breadcrumb:
- Register-Breadcrumb liegt nicht mehr im 1180-px-Contentcontainer.
- Eigene Breadcrumb-Achse wie beim bewährten Pferdeatelier:
  - Breite: `min(calc(100vw - 32px), 900px)`
  - oberer Abstand: `var(--pftk-navigation-content-gap,18px)`
  - unterer Abstand: `var(--pftk-global-breadcrumb-content-gap,16px)`
  - 14px / line-height 1.5.
- Hierarchie Detailprofil:
  `Startseite › Hobbyregister › Hobby`
- Magazin wird bewusst nicht dazwischengeschaltet.

Startseite:
- `862 Treffer` wird im ungefilterten Register nicht mehr angezeigt.
- Bei echter Suche/A–Z/Gruppe bleibt die Trefferzahl erhalten.

Werbung:
- bestehende, bereits bewährte Affiliate-Schnittstelle wird genutzt:
  `[pp_affiliate_slot type="hub_after_cards" intent="portal_context"]`
- keine neue Affiliate-Architektur / kein neuer Slot-Typ.
- je ein Bannerbereich:
  - Registerübersicht nach der Hobbyliste;
  - Detailprofil nach dem Haupttext und vor „Ähnliche Hobbys“.
- wenn kein Slot gefüllt ist: ausgeloggt kein Leerraum; eingeloggt Admin-Prüffläche.

## QA

- PHP-Lint beide Dateien PASS.
- Fresh-Unpack PASS.
- ZIP exakt 2 Dateien PASS.
- Core 862/862 unverändert PASS.
- ungefilterte Startseite: kein `862 Treffer` PASS.
- Filteransicht: Trefferzahl weiterhin vorhanden PASS.
- Breadcrumb 900-px-Achse PASS.
- Detail-Breadcrumb: Startseite › Hobbyregister › Geocaching PASS.
- Magazin im Breadcrumb: 0 PASS.
- Bannerübersicht: genau 1 PASS.
- Bannerdetail: genau 1 PASS.
- 8-Fließtextabschnitte auf Detailprofil unverändert PASS.

Kein Live-PASS behaupten.
