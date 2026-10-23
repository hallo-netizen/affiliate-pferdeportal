# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **HD-003 1.50.725 FOOTER LOCAL HARD PASS / HD-007 1.1.1 REGISTER-KORREKTUR LOCAL HARD PASS / LIVE-ABNAHME OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Footer

1.50.724 hatte einen falschen doppelt verschachtelten Logoassetpfad.
1.50.725 korrigiert ausschließlich diese Pfadbindung; Markenleiste und vier Spalten bleiben bestehen.

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.725_UPDATE_FOOTER_LOGO_FIX.zip`

SHA-256:
`4857b6e57d7a8b155e66e8f211843690f0db4066ced0e925740c06cef32575bf`

## Hobbyregister

1.1.0 wurde live/visuell als nicht ausreichend beanstandet:
- Gruppen als große Kacheln statt Icon-Navigation;
- Breadcrumb-Abstand falsch;
- Nicht-Testprofile nur als vier Kurzzeilen;
- linke Faktenleiste zu klein/trocken;
- ähnliche Hobbys doppelt/zu dominant.

1.1.1 korrigiert:
- Gruppen als reine runde Icon-Navigation nach dem Pferderassen-Prinzip;
- Breadcrumb im Hobby-Depot-Standard;
- alle 862 Detailprofile mit acht Fließtextabschnitten;
- linke Faktenleiste farbig, größere Typografie, eigene Icons;
- gleiche Hobbygruppe links;
- ähnliche Hobbys nur einmal unten.

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.1_FULL_KORREKTUR.zip`

SHA-256:
`f963a0c07a4e5f9275992db8eea82f92721a4c12b62a3a7f0e78ed9b7a094d7c`

QA:
- 862/862 acht Textabschnitte;
- kürzester generierter Detailtext 486 Wörter;
- sechs heterogene Vollrenders PASS;
- Iconnavigation / Breadcrumb / Sidebar PASS;
- PHP-Lint / Fresh-Unpack PASS.

## EXAKT EINE NEXT ACTION

**Das kombinierte Cyberduck-Bundle mit den beiden bestehenden Pluginordnern einspielen und Footer, Register-Startseite sowie eine normale Register-Detailseite live prüfen.**
