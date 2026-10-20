# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-20
STATUS: **1.50.703 AKTUELLER DESIGNSTAND / LOCAL PASS / LIVE TEILWEISE VISUELL BESTÄTIGT / VOLL-READBACK OFFEN**

Plugin-ID:
HD-003-DESIGN-TEMPLATE-KIT

Aktuelles Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.703_SERVICE_TITLE_NATIVE_FOOTER_FIX_LOCALPASS.zip`

SHA-256:
`74cb488a891dab9bfff237c3820c05a2cf3dd3651f52a5335e2af671b33ce228`

Größe:
58,673,853 Bytes.

## Rolle

- zentrale visuelle Hobby-Depot-Darstellung;
- Header, Startseite, Hub-/Detaildarstellung, Footer und spätere Finder-Oberfläche;
- **keine eigene Hobby-Datenbank**;
- Finder darf nur aus dem zentralen Hobbyregister lesen.

## Aktueller Stand

1.50.703 basiert auf der stabilen 1.50.699-Laufzeitklasse `Hobby_Depot_Profile_V150699`.
Keine Klassen-/Template-Umbenennung wie beim verworfenen 1.50.700.

Enthalten:
- vereinfachte Startseite mit Hobbyfinder als Hero-CTA;
- 69/69 Hub2-Einstiege unverändert;
- 395 Detail-Hubs unverändert;
- Serviceseiten: genau ein Titel + Breadcrumb, kein generischer Zusatzintroblock;
- ListingHive-`.site-footer` ausgeblendet;
- eigener Hobby-Depot-Footer;
- Reihenfolge Rechtliches → Informationen → Anzeigenmarkt;
- Magazin dedupliziert;
- Anbieter im Informationsblock entfernt;
- Hobbyfinder separat.

## QA

Lokale QA 1.50.703:
- PHP-Lint 135/135 PASS;
- 11/11 Serviceseiten-Harness PASS;
- Footer-Runtime PASS;
- ListingHive-Selektormatch PASS;
- ZIP-Integrität PASS.

Live:
- Nutzer meldete am 2026-10-20, dass der doppelte Footer zunächst nicht mehr sichtbar ist;
- vollständige Live-Abnahme aller 1.50.703-Punkte wurde noch nicht protokolliert;
- daher kein pauschales LIVE PASS.

## Verworfen

- 1.50.700: verworfen wegen Runtime-Klassen-/Template-Mismatch;
- 1.50.701: ersetzt;
- 1.50.702: ersetzt; Serviceseitentitel fehlten.

## ERSTER OFFENER BLOCKER

Der neue Hobbyfinder muss auf Basis 1.50.703 eingebunden werden, **ohne** die 862 Hobbydatensätze in HD-003 zu duplizieren.

## EXAKT EINE NEXT ACTION

**Eine schlanke zentrale Hobbyregister-Laufzeitschnittstelle bereitstellen und HD-003 darauf lesen lassen. Danach Finder lokal positiv/negativ testen; 1.50.703 sonst unverändert lassen.**
