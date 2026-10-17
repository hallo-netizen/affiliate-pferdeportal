# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **MEGA-MENÜ 1.50.670 GRUNDSATZ BLEIBT / 1.50.670 BILDTEIL VERWORFEN / 1.50.671 SHARP-MASTER-IMAGE-FIX LOCAL HARD PASS / LIVE-PRÜFUNG OFFEN**

## Ausgangspunkt

Der letzte Frontend-Test zeigte:
- Mega-Menü-Grundsatz aus 1.50.670 ist fachlich richtig: bis 10 echte Zwischenbereiche = zwei sichtbare Reihen, `Mehr Kategorien` erst oberhalb 10;
- Bildteil 1.50.670 ist dagegen verworfen.

Konkreter Fehler 1.50.670:
- die neuen Hero-Dateien waren nur 600×320;
- dadurch wurden sie auf großen/Retina-Displays sichtbar weich;
- mehrere Motive waren zu eng bzw. wie vergrößerte Vorschau-Ausschnitte;
- besonders Modellbau, Technik, Pflanzen sowie Sammeln;
- Suchen & Finden / Werbung & Design / Werkzeuge & Geräte waren in der kleinen Darstellung nicht klar genug lesbar.

## HARTE BILDREGEL AB 1.50.671

- Hero = einziges Masterbild;
- Mastergröße 1600×853;
- Vorschau wird ausschließlich aus demselben Hero nach unten auf 600×320 gerechnet;
- niemals Vorschau -> Hero hochskalieren;
- keine Collagen;
- klare vollständige Szene statt unlesbarem Makro-/Detailausschnitt.

## Exakter Scope 1.50.671

**Keine anderen Kategorien anfassen.**

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
- Zimmerpflanzen;
- Hydroponik & Indoor.

Unverändert:
- Orchideen & Exoten.

Tiere:
- Terraristik.

Unverändert:
- Aquaristik.

Sammeln – alle 9 aktuellen Zwischenbereiche:
- Münzen & Geld;
- Papier & Dokumente;
- Technik & Medien;
- Spielzeug & Spiele;
- Naturfunde;
- Werbung & Design;
- Werkzeuge & Geräte;
- Alltagsobjekte;
- Suchen & Finden.

Gestalten und alle nicht genannten Bereiche bleiben komplett unangetastet.

## Mega-Menü

Keine neue Änderung gegenüber 1.50.670:
- 5 Spalten;
- bis 10 Zwischenbereiche direkt = maximal zwei Reihen;
- `Mehr Kategorien` erst ab 11;
- Unterkategorie-Schrift leicht größer;
- Heimwerken/Gärtnern bleiben direkte Hobbyseiten und keine künstlichen Mega-Spalten.

## 1.50.671 – Local QA

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.671_HOBBY_DEPOT_SHARP_MASTER_HERO_TARGETED_HARDPASS.zip`

SHA-256:
`be1e2ed9d82ee290e3744fd23f2c882849e612f768a820868703c50a46c8a606`

PASS:
- 61/61 PHP;
- 19/19 Hero-Master 1600×853;
- 19/19 Vorschauen 600×320 aus den jeweiligen Masterbildern;
- 0 exakte Hero-Duplikate;
- 0 Collage-Dateien neu eingebaut;
- Hero-Map nur an exakt diesen 19 Schlüsseln geändert;
- Cards-Map vollständig unverändert;
- Orchideen & Exoten byte-identisch;
- Gestalten-Bildbestand byte-identisch;
- Klassenlogik gegenüber 1.50.670 unverändert, nur Versionsbindung;
- ZIP-Test PASS;
- Roundtrip 1029/1029 byte-identisch.

Interne visuelle Kontrolle:
- Modellbau weiter herausgezoomt, vollständige Werkstatt-/Modellszene;
- Computer & Retro weiter;
- Audio & HiFi weiter;
- Spotting/Citizen Science/Natur bestimmen als scharfe große Szenen;
- Bonsai & Miniatur neue eigenständige Szene;
- Zimmerpflanzen und Hydroponik nicht mehr derselbe Frau-/Gestik-/Hintergrund-Ausschnitt;
- Terraristik scharfes eigenes Terrarium;
- Sammeln komplett neue scharfe Master, inklusive deutlich weiterer Szenen für Werbung & Design, Werkzeuge & Geräte und Suchen & Finden.

## PASS-GRENZE

Noch kein Live-PASS für 1.50.671.

## EXAKT EINE NEXT ACTION

**1.50.671 installieren und im Frontend ausschließlich die genannten Bildbereiche prüfen. Mega-Menü-Grundsatz nicht erneut umbauen.**
