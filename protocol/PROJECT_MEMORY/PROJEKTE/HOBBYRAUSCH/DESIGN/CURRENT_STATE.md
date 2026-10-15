# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-15
STATUS: **SEITE WIEDER ERREICHBAR / RUNTIME+ARCHITEKTUR EINGEFROREN / 1.50.660 VISUELL FÜR 30 HEROES VERWORFEN / 1.50.661 30-BILD-ONLY LOKAL E2E PASS / LIVE-VISUALPRÜFUNG OFFEN**

## Harte Sperre
Keine Änderungen an:
- Template-Kit-PHP;
- Routing;
- Templates;
- CSS;
- Mapping;
- Karten;
- Seitenstruktur;
- Architektur/System.

## Aktiver Grundstand
Affiliate Portal Template Kit **1.50.650** bleibt unangetastet.

## Verworfen
- 1.50.651;
- Repair Installer 1.50.657;
- Recovery 1.50.658;
- Hero Images ONLY 1.50.659;
- Hero Replace ONLY 1.50.660 für die unten genannten 30 Heroes wegen Live-Sichtbefund: unscharf/zu eng/teilweise falsches Motiv/teilweise Doppelungen.

## Nutzer-Hard-Reject – 30 Heroes
Miniaturen & Szenen; Papierkunst; Textilgestaltung; Malen & Zeichnen; Schrift & Lettering; Guss & Formen; Holz; Leder; Heimwerken; Keramik & Glas; Mechanik & Uhren; Robotik & Automation; Astronomie; Messen & Analysieren; Mikroskopie; Wetter & Umwelt; Gärtnern; Essbare Pflanzen; Moos & Miniaturgärten; Pilze & Kulturen; Ameisen & Insekten; Wirbellose; Wind & Drachen; Klettern & Seil; Wasser; Alltagsobjekte; Naturfunde; Spielzeug & Spiele; Münzen & Geld; Technik & Medien.

## Verbindliche Bildregel
- breite Szene statt Makro/Detailcrop;
- Thema sofort erkennbar;
- Hauptmotiv vollständig mit sichtbarer Umgebung;
- scharf, kein sichtbares Upscaling;
- kein falsches Ersatzmotiv;
- keine offensichtliche Bildwiederholung;
- Technik-PASS ist kein Live-Visual-PASS.

## Aktueller Kandidat
`HOBBY_DEPOT_HERO_REPLACE_30_ONLY_1.50.661.zip`

SHA-256:
`befb9a73f67e3827b7ad5c7c03d940976a5362a2a732f779654499685f0f0b3e`

## Was 1.50.661 exakt macht
- Payload: exakt 30 WebP-Heroes, jeweils 600×220;
- ersetzt nur die 30 vom Nutzer verworfenen Heroes;
- liest deren **bereits aktive** Zielpfade aus dem vorhandenen 65er-Mapping;
- schreibt das Mapping niemals;
- lässt die übrigen 35 aktuell gemappten Heroes byte-identisch;
- 0 Änderungen am Template-Kit-PHP;
- 0 Änderungen an Templates/Routing/CSS/Karten/Architektur.

## Lokaler Nachweis
Payload:
- 30/30 = 600×220;
- 30/30 SHA-eindeutig;
- niedrigster lokaler Schärfewert (Laplacian variance) > 1684;
- nächstes perzeptuelles Paar im 30er-Satz: Hamming-Distanz 19.

E2E-Aktivierung mit dem echten Plugin-PHP:
1. pristine 1.50.650: PASS;
2. simuliertes reales Nach-1.50.659+1.50.660-Szenario: PASS.

In beiden Szenarien:
- exakt 30 Datei-Diffs;
- exakt die 30 aktuell gemappten Zielbilder;
- Mapping byte-identisch;
- übrige 35 Hero-Zieldateien unverändert;
- 0 PHP-Diffs;
- 30/30 Zielbilder SHA-identisch zum Payload;
- keine .tmp/.bak-Reste.

## EXAKT EINE NEXT ACTION
**1.50.661 installieren/aktivieren und die 30 betroffenen Hub2-Seiten live visuell prüfen. Keine andere Plugin-, Mapping- oder Architekturänderung.**
