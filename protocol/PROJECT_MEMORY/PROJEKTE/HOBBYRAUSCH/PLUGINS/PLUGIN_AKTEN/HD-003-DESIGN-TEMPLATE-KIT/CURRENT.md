# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.50.670 BILDTEIL VERWORFEN / 1.50.671 SHARP-MASTER-HERO TARGETED LOCAL HARD PASS / LIVE OFFEN**

## Ursache 1.50.670

1.50.670 hatte die richtige Mega-Menü-Regel, aber einen falschen Bildworkflow:
- Hero-Dateien nur 600×320;
- sichtbare Unschärfe bei großer Darstellung;
- teilweise zu enge Ausschnitte;
- Vorschau-/Hero-Denke faktisch in falscher Richtung.

## Einziger Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.671_HOBBY_DEPOT_SHARP_MASTER_HERO_TARGETED_HARDPASS.zip`

SHA-256:
`be1e2ed9d82ee290e3744fd23f2c882849e612f768a820868703c50a46c8a606`

## Bildworkflow 1.50.671

- großes Hero-Master 1600×853;
- Vorschau 600×320 ausschließlich daraus abgeleitet;
- keine Collagen;
- kein Preview-Upscaling;
- klare, weiter gefasste Szenerie.

## Exakter Scope

Nur 19 benannte Bereiche:
Modellbau; Computer & Retro; Audio & HiFi; Spotting & Verkehr; Citizen Science; Natur bestimmen; Bonsai & Miniatur; Zimmerpflanzen; Hydroponik & Indoor; Terraristik; Münzen & Geld; Papier & Dokumente; Technik & Medien; Spielzeug & Spiele; Naturfunde; Werbung & Design; Werkzeuge & Geräte; Alltagsobjekte; Suchen & Finden.

Nicht geändert:
- Gestalten komplett;
- Orchideen & Exoten;
- Aquaristik;
- Holz & Natur;
- alle anderen Kategorien.

Mega-Menü-Code gegenüber 1.50.670 inhaltlich unverändert.

## QA

- PHP 61/61 PASS;
- 19/19 Hero 1600×853;
- 19/19 Preview 600×320;
- 0 exakte Hero-Duplikate;
- Hero-Map außerhalb der 19 Schlüssel unverändert;
- Cards-Map unverändert;
- Gestalten byte-identisch;
- Orchideen & Exoten byte-identisch;
- Klassenlogik gegenüber 1.50.670 außer Version identisch;
- ZIP PASS;
- Roundtrip 1029/1029 identisch.

## Isoliertes Artefakt

`CURRENT.zip` bleibt bis zum echten Frontend-Check noch nicht synchronisiert.

## EXAKT EINE NEXT ACTION

**1.50.671 installieren -> ausschließlich die genannten Bildbereiche live prüfen.**
