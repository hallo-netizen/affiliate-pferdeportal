# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.683 METALL LIVE ABGENOMMEN / 1.50.684 PORTALWEITER HUB2-ROLLOUT GEBAUT / LOKAL POSITIV+NEGATIV+RESPONSIVE PASS / WORDPRESS-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 4.9 / 2026-10-18**

## NUTZERENTSCHEIDUNG

Der Metall-Pilot 1.50.683 ist für Bild und Text abgenommen.

Damit gilt für alle aktuell **69 Hub2-Seiten derselben Ebene**:
- bisheriges Hero-Prinzip mit Claim + H1 + kurzem Satz links bleibt;
- rechts wird die **ursprüngliche/bestmögliche Master-Szenerie** verwendet;
- kein Hineinzoomen in einen kleineren Ausschnitt;
- Desktop darf für das flachere Hero ausschließlich **oben und unten** beschneiden;
- horizontal bleibt die Szene erhalten;
- niemals über die native Bildauflösung hochskalieren;
- Mobil verwendet dieselbe Szene und keinen anderen Ausschnitt.

Zusätzlich sind die schablonenhaften Untertitel der Unterkategoriekarten verworfen. Die Karten sollen kurz und konkret sagen, worum es im jeweiligen Thema geht.

## KANDIDAT 1.50.684

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.684_HOBBY_DEPOT_ALL_HUB2_SCENE_MASTER_CARDTEXT.zip`

SHA-256:
`2756075151e1996ceaa72e9057e85f1af42c181f6356867accae0ffbd43a8920`

### Hero-Rollout

69/69 aktive Hub2 besitzen jetzt einen gebundenen Szenenmaster:
- **45** aus wiedergefundenen größeren Original-/Masterquellen derselben vorhandenen Szene;
- **19** aus bereits vorhandenen 1600×853-Heroquellen;
- **5** Themen besitzen im vorhandenen Bestand nur eine belastbare 600-px-Quelle: `saatgut-zucht`, `rollen-balance`, `wurf-ziel`, `team-wettkampf`, `geschick-tricks`.

Für diese fünf wird **nicht** hochskaliert:
- Desktop maximal 600 px Bildbreite;
- Hero-Höhe auf native Szenenhöhe begrenzt;
- Mobil ebenfalls niemals über 600 px.

Alle Szenenmaster haben ein flaches Verhältnis um ca. 2,72:1. Bei Desktop 901–1440 px ist der Bildcontainer rechnerisch und im Browser immer mindestens so breit im Verhältnis wie die Quelle. Dadurch kann `object-fit:cover` **nur oben/unten beschneiden, niemals links/rechts**.

### Kartenuntertitel

Für alle aktuell vorhandenen **328 direkten Unterkategoriekarten** ist eine individuelle, themenspezifische Kurzzeile gebunden.

Beispiele:
- Airbrush → `Farbe fein zerstäuben und kontrolliert schichten.`
- CNC-Fräsen → `Werkstücke computergesteuert präzise ausfräsen.`
- Bonsai → `Bäume klein halten, formen und langfristig entwickeln.`
- Formicarienbau → `Nestkammern, Arena und Klima für Ameisen konstruieren.`
- Discgolf → `Scheiben mit unterschiedlichen Flugbahnen Richtung Korb werfen.`
- Numismatik → `Münzen wissenschaftlich bestimmen, ordnen und bewerten.`

Die bisherigen generischen Welt-Fallbacks mit Formulierungen wie `loslegen`, `ausprobieren`, `praktische Einstiege` oder pauschalem `verstehen` sind aus dem Hub2-Kartenpfad entfernt.

Für eine spätere neue, noch nicht redigierte Unterkategorie gilt:
**vorhandene echte redaktionelle Kurzzeile verwenden; sonst leer statt generischem Fülltext.**

## QA 1.50.684

Release / Paket:
- aus exakter 1.50.683-Basis gebaut;
- Pluginwurzel korrekt;
- PHP **96/96 PASS**;
- aktive Main-/Klassen-/Routenkette vollständig V150684;
- reale Front-Route → V150684 PASS;
- reale Content-Route → V150684 PASS;
- Fronttemplate mit V150684 ausgeführt PASS;
- Contenttemplate mit V150684 ausgeführt PASS;
- Negativtest mit ausschließlich V150683: beide V150684-Templates scheitern erwartungsgemäß;
- Dirty-Overlay 1.50.683 → 1.50.684: aktive Route und beide Templates PASS;
- ZIP-Test PASS;
- Roundtrip **1136/1136 byte-identisch**.

Regression:
- gegenüber 1.50.683 exakt **1 bestehende Datei geändert**: `pferde-template-kit.php`;
- **72 Dateien neu**: Profilklasse + 2 Templates + 69 Szenenmaster;
- **0 Dateien entfernt**;
- **894/894 bestehende Bildassets byte-identisch**.

Inhalt:
- 69/69 Hub2-Render mit neuem Szenenmaster PASS;
- 328/328 Kartenuntertitel vorhanden und exakt gebunden;
- 328 Kurzzeilen sind eindeutig;
- 0 generische Hub2-Welt-Fallbacks im aktiven Kartenpfad.

Responsive / Bild:
- alle 69 Masterdimensionen gegen 1440 / 1180 / 1024 / 901 px rechnerisch geprüft: **0 Upscaling, 0 Risiko für seitlichen Crop**;
- Browserprüfung mit realen Assets bei 1440 / 1180 / 1024 / 901 / 900 / 760 / 390 px;
- geprüft wurden 2070-, 1600-, 1354-, 1245-, 900- und 600-px-Quellen;
- **42/42 Browserfälle PASS**;
- kein horizontaler Overflow;
- mobile Szene bleibt im Master-Seitenverhältnis;
- 600-px-Sonderfall wird auch bei 900/760 px nicht vergrößert.

## EXAKT EINE NEXT ACTION

**1.50.684 installieren und mehrere Hub2 aus unterschiedlichen Welten real prüfen. Bei Frontend-PASS ist der Metall-Hero-/Kartenuntertitel-Standard portalweit übernommen.**

## NICHT ANFASSEN

- Kategoriebaum nicht ändern;
- Mega-Menü nicht ändern;
- Kategorietexte nicht neu schreiben;
- keine generische Karten-Schablone wieder einführen;
- keine Heroquelle künstlich hochskalieren;
- keine neue Architektur.
