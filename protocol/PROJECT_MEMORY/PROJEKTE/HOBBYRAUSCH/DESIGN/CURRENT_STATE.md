# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LIVE 1.50.676 / AUDIO-HERO FEINTUNING 1.50.677 LOCAL HARD PASS / LIVE OFFEN**

## Reales Live-Ergebnis 1.50.676

Vom Nutzer bestätigt:
- Hero-Höhe jetzt okay;
- Claim sitzt vertikal grundsätzlich richtig;
- Pinselunterstrich ist jetzt zu kurz;
- Bild soll noch deutlich breiter wirken, Ziel ungefähr drei Viertel der Hero-Fläche;
- die kurze Zeile unter der H1 soll in jedem Fall einzeilig bleiben.

## 1.50.677 – nur Audio & HiFi

Keine andere Kategorie geändert.

Korrektur:
- Unterstrich auf ca. Claim-Textlänge: 98 % der realen Claim-Breite;
- bestehende Claim-Höhe/Position bleibt unverändert;
- Bildanteil optisch verbreitert:
  - >1180 px Text-/Verlaufszone 30 %;
  - 901–1180 px Text-/Verlaufszone 35 %;
  - Bild liegt weiterhin als ein einziges Fullbleed-Masterbild über 100 % des Hero;
- Bildposition leicht nach links verschoben, damit mehr Motiv sichtbar bleibt;
- Kurzzeile unter H1: white-space nowrap, kein Umbruch;
- Mobil-Schrift skaliert nur soweit, dass die Zeile ebenfalls einzeilig bleibt;
- <=900 px bleibt der stabile gestapelte Weg mit 100-%-Bildbreite.

Performance:
- kein neues Bild;
- kein zusätzlicher Request;
- kein JavaScript;
- kein Blur/Masking;
- nur zentrale CSS-Regel in der vorhandenen Fullbleed-Klasse.

Unverändert:
- Hero-Bilddatei;
- H1;
- Claimtext;
- Kurztext-Wortlaut;
- Langtext;
- Karten;
- Mega-Menü;
- alle anderen Kategorien;
- 901/901 Assets.

## QA

Artefakt:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.677_HOBBY_DEPOT_AUDIO_IMAGE_3Q_SINGLELINE_FIX_HARDPASS.zip

SHA-256:
e0b5b6819f91c7e43b2f6929a04ef97d83d51db34404d87b39506aff9f9c5f16

PASS:
- PHP 78/78;
- aktive Release-Kette vollständig 1.50.677;
- keine aktive 1.50.676-Routen-/Klassenreferenz;
- Unterstrich 98 % der Claim-Breite;
- Desktop-Copy-/Verlaufszone 30/35 %;
- Kurzzeile explizit nowrap;
- 901 Assets unverändert;
- WordPress-Pluginwurzel korrekt;
- ZIP-Test PASS;
- Roundtrip 1047/1047 byte-identisch.

## EXAKT EINE NEXT ACTION

**1.50.677 über 1.50.676 installieren und nur Audio & HiFi prüfen: Unterstrichlänge, breiteres Bild und einzeilige Kurzzeile.**
