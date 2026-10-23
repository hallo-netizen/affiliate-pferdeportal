# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **HD-003 1.50.725 FOOTER LOCAL HARD PASS / HD-007 1.1.2 BREADCRUMB + BANNER LOCAL HARD PASS / LIVE-ABNAHME OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Footer

HD-003 1.50.725 bleibt unverändert aktueller Footer-Kandidat.

## Hobbyregister

1.1.2 ist ein kleines Update auf 1.1.1.

Korrigiert:
- Breadcrumb aus dem 1180-px-Registercontainer herausgezogen;
- gleiche 900-px-Achse und vertikale Variablen wie beim bewährten Pferdeatelier-Breadcrumb;
- Detailhierarchie Startseite › Hobbyregister › Hobby;
- Magazin bewusst nicht im Breadcrumb;
- „862 Treffer“ auf ungefilterter Startseite entfernt;
- Trefferzahl bleibt bei echter Filterung;
- ein vorhandener Affiliate-Bannerplatz auf Übersicht und Detailseite ergänzt.

Affiliate:
- bestehender Slot `hub_after_cards`;
- keine neue Affiliate-Architektur.

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.2_UPDATE_BREADCRUMB_BANNER.zip`

SHA-256:
`d83cb6de965f495e07bdc2746013657f864bda93861bfcd188db63a1287ec96e`

QA:
- Breadcrumb-Achse PASS;
- Startseite ohne 862 Treffer PASS;
- gefilterte Trefferzahl PASS;
- Banner Index/Detail PASS;
- 8 Textabschnitte erhalten;
- PHP-Lint/Fresh-Unpack PASS.

## EXAKT EINE NEXT ACTION

**HD-007 1.1.2 einspielen und Register-Startseite plus ein Detailprofil live auf Breadcrumbposition und Banner prüfen.**
