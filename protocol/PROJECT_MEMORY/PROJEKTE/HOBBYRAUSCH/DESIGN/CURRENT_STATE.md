# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.50.668 / V7.1 FRONTEND SICHTBAR / 1.50.670 TARGETED DESIGN FIX LOCAL HARD PASS / LIVE-PRÜFUNG OFFEN**

## Live-Wahrheit

WordPress bestätigt weiterhin:
`Affiliate Portal Template Kit 1.50.668` aktiv.

Der aktuelle Frontend-Nachweis zeigt inzwischen die neue V7.1-Struktur:
- terminale Content-Ebene bei Ameisenhaltung sichtbar;
- Forschen enthält zusätzlich Spotting & Verkehr, Citizen Science und Natur bestimmen, aktuell aber erst nach `Mehr Kategorien`.

Damit ist der frühere reine 330er-Anzeigezustand nicht mehr der aktuelle Frontend-Befund.

## 1.50.670 – exakt begrenzter Arbeitsumfang

Basis:
1.50.668 plus der bereits geprüfte 1.50.669-WIP-Renderergrundsatz:
- echte Zwischenbereiche = Mega-Spalten;
- direkte Hobbyseiten wie Heimwerken/Gärtnern = keine künstlichen Mega-Spalten;
- Registry bleibt einzige Strukturquelle.

### Mega-Menü

Neue Darstellungsregel:
- 5 Spalten;
- bis zu 10 echte Zwischenbereiche sofort sichtbar = maximal zwei Reihen;
- `Mehr Kategorien` erst ab dem 11. Bereich / einer nötigen dritten Reihe;
- Unterkategorie-Schrift leicht vergrößert.

V7.1 ergibt damit direkt sichtbar:
Gestalten 7 · Fertigen 10 · Technik 9 · Forschen 8 · Pflanzen 9 · Tiere 7 · Bewegen 8 · Sammeln 9.

Bekannte direkte Hobbyseiten bleiben korrekt ausgeschlossen:
- Heimwerken bei Fertigen;
- Gärtnern bei Pflanzen.

## Bild-Scope – HARD RULE

**Keine anderen Kategorien anfassen.**

Geändert wurden ausschließlich die vom Nutzer genannten 17 Bereiche:

Fertigen:
- Modellbau.

Technik:
- Computer & Retro;
- Audio & HiFi.

Forschen:
- Spotting & Verkehr;
- Citizen Science;
- Natur bestimmen.

Pflanzen:
- Bonsai & Miniatur;
- Orchideen & Exoten;
- Zimmerpflanzen;
- Hydroponik & Indoor.

Tiere:
- Aquaristik;
- Terraristik.

Sammeln:
- Münzen & Geld;
- Papier & Dokumente;
- Werkzeuge & Geräte;
- Werbung & Design;
- Suchen & Finden.

Für jeden dieser 17 Bereiche:
- eigenes Hero 600×320;
- daraus abgeleitete Vorschau 200×107;
- keine exakten Bildduplikate unter den 17 neuen Heroes;
- keine Nahduplikate im lokalen Bildvergleich.

**Holz & Natur wurde trotz früherem offenen Bildbrief ausdrücklich NICHT verändert**, weil es in der aktuellen Nutzerfreigabe nicht enthalten war.

## Prüfung auf Bild-Rückfall durch 1.50.668

Explizit geprüft:
1.50.668 gegen 1.50.650 für die bisher problematischen vorhandenen Bilddateien und die zentrale Bildmap.

Ergebnis:
- 13/13 geprüfte Dateien byte-identisch;
- 1.50.668 hat die falschen Bilder nicht neu zurückgespielt;
- die problematischen Motive waren bereits vorher vorhanden und wurden lediglich unverändert mitgeführt.

## Local QA 1.50.670

PASS:
- PHP 61/61;
- echter PHP-Registry-Harness mit V7.1: 7/10/9/8/9/7/8/9;
- sichtbares Limit = 10;
- Heimwerken/Gärtnern korrekt nicht als Mega-Spalten;
- vorhandene Browser-QA beweist, dass der bereits geprüfte 10er-expanded-Zustand bei 1920, 1440, 1180, 1024, 901, 900, 768 und 761 px ohne horizontalen Überlauf passt;
- 17/17 Hero-Größen 600×320;
- 17/17 Preview-Größen 200×107;
- 17/17 Hero-Mappings exakt;
- 0 exakte Bildduplikate;
- 0 Nahduplikat-Paare im benannten Set;
- Bildmap außerhalb dieser 17 Hero-Schlüssel unverändert;
- Cards-Bildmap vollständig unverändert;
- Paket-Roundtrip 1009/1009 Dateien byte-identisch;
- ZIP-Test ohne Fehler.

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.670_HOBBY_DEPOT_MEGA2ROWS_TARGETED_IMAGES_HARDPASS.zip`

SHA-256:
`9e21fd6c402fbb1a3358a58807db8b28a322a499d8478fbffb375fadbecc0408`

## PASS-GRENZE

Noch kein Live-PASS für 1.50.670.

## EXAKT EINE NEXT ACTION

**1.50.670 über 1.50.668 installieren und im Frontend gezielt Forschen-Mega-Menü plus die ausdrücklich genannten Bildbereiche prüfen. Keine weiteren Kategorien ändern.**
