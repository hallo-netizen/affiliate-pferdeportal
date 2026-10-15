# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-15
STATUS: **SEITE ERREICHBAR / TEMPLATE-KIT 1.50.650 EINGEFROREN / HERO-HELPER 1.50.663 LIVE VISUAL FAIL + VERWORFEN / KEIN NEUES ZIP FREIGEGEBEN**

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
Textinhalt und Grundaufteilung aus 1.50.650 bleiben eingefroren.

## Nicht verwenden
- 1.50.651;
- Repair Installer 1.50.657;
- Recovery 1.50.658;
- Hero Images ONLY 1.50.659;
- Hero Replace 1.50.660;
- Hero Replace 1.50.661;
- Hero Replace 1.50.662;
- Hero Replace 1.50.663.

## LIVE VISUAL FAIL 1.50.663
1.50.663 ist technisch nicht der Maßstab. Die Live-Sichtprüfung hat den Bildsatz verworfen.

Belegte Grundfehler:
- derselbe kleine Bestand an Ausgangsszenen wurde mehrfach für verschiedene Kategorien benutzt;
- teilweise nur andere Ausschnitte/Crops derselben Grundszene;
- sichtbare Bild-in-Bild-/Collage-Konstruktionen;
- semantisch falsche Motive;
- Doppel-/Mehrfachverwendung;
- damit Verstoß gegen die bereits verbindliche Regel: **ein eigenes, fachlich passendes, weit gefasstes Motiv pro Kategorie**.

## Nutzer-Hard-Reject 2026-10-15 – besonders fehlerhafte 18
1. Papierkunst – BILD IN BILD
2. Schrift & Lettering – BILD IN BILD
3. Holz – falsches Motiv
4. Leder – falsches Motiv / bereits live sichtbar unpassende Szene
5. Keramik & Glas – BILD IN BILD
6. Mechanik & Uhren – falsches Motiv + BILD IN BILD
7. Astronomie – falsches Motiv + BILD IN BILD
8. Messen & Analysieren – falsches Motiv
9. Mikroskopie – falsches Motiv + BILD IN BILD
10. Wetter & Umwelt – falsches Motiv + BILD IN BILD
11. Gärtnern – doppelt
12. Moos & Miniaturgärten – falsches Motiv + doppelt
13. Pilze & Kulturen – falsches Motiv
14. Ameisen & Insekten – falsches Motiv
15. Wirbellose – falsches Motiv + dreifach
16. Naturfunde – verworfen
17. Spielzeug & Spiele – falsches Motiv
18. Technik & Medien – falsches Motiv + BILD IN BILD

## Übergeordneter Hard-Reject
Zusätzlich bleiben die bereits vom Nutzer verworfenen insgesamt 30 Heroes vollständig offen:
Miniaturen & Szenen; Papierkunst; Textilgestaltung; Malen & Zeichnen; Schrift & Lettering; Guss & Formen; Holz; Leder; Heimwerken; Keramik & Glas; Mechanik & Uhren; Robotik & Automation; Astronomie; Messen & Analysieren; Mikroskopie; Wetter & Umwelt; Gärtnern; Essbare Pflanzen; Moos & Miniaturgärten; Pilze & Kulturen; Ameisen & Insekten; Wirbellose; Wind & Drachen; Klettern & Seil; Wasser; Alltagsobjekte; Naturfunde; Spielzeug & Spiele; Münzen & Geld; Technik & Medien.

## Verbindliche Bildregel
- **keine Wiederverwendung derselben Ausgangsszene** in mehreren Kategorien;
- **kein anderer Crop derselben Szene** als angeblich neues Motiv;
- **kein Bild in Bild / keine Collage / kein zusammengesetztes Ersatzmotiv**;
- breiter Szenenausschnitt, kein Makro/Detailzoom;
- Hauptmotiv vollständig und sofort erkennbar;
- sichtbare Umgebung;
- scharf, kein sichtbares Upscaling;
- semantisch eindeutiges Motiv exakt zur Kategorie;
- keine Doppel-/Dreifachverwendung;
- technische Maße/Hashes/Pfade sind kein visueller PASS.

## Aktuelle Arbeit
Kein neues Plugin wird ausgegeben, bevor die 18 besonders beanstandeten Motive und anschließend der gesamte 30er-Hard-Reject-Satz **einzeln visuell** gegen Thema → Motiv → Abstand/Zoom → Schärfe → kein Bild-in-Bild → keine Ausgangsszenen-Wiederholung geprüft sind.

## EXAKT EINE NEXT ACTION
**Bildquellen für die verworfenen Kategorien neu auswählen; alte 1.50.663-Ausgangsszenen und deren Crops vollständig sperren. Erst nach vollständiger Einzelprüfung darf ein reiner Bilddatei-Ersatzkandidat entstehen.**


## Interne Rückfallprüfung – alte lokale Bildvarianten ebenfalls nicht pauschal verwenden
Nach dem Verwerfen von 1.50.663 wurden die vorhandenen älteren lokalen Varianten für die 18 besonders beanstandeten Kategorien erneut als mögliche Quellen gegengeprüft.

Ergebnis:
- **kein pauschaler Rückgriff auf v150616/v150623/v150627/v150629/v150631/v150634**;
- mehrere alte Motive sind zwar semantisch näher, verletzen aber weiterhin die neue harte Distanzregel (zu dicht/Detail);
- besonders auffällig: Papierkunst, Schrift & Lettering, Mechanik & Uhren, Astronomie, Mikroskopie, Wetter & Umwelt sowie Ameisen & Insekten;
- für Messen & Analysieren, Pilze & Kulturen und Wirbellose ist im vorhandenen lokalen Altbestand aktuell **keine belastbar passende Quelle** festgestellt.

Konsequenz:
Alte Varianten sind nur Einzelquellenkandidaten, niemals automatischer Fallback. Kein alter Crop wird allein wegen besserer Semantik übernommen.
