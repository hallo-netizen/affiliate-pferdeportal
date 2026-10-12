# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.649 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.649_HOBBY_DEPOT_ALL_HUB2_BP_LAYOUT_PFERDE_TEXT_RULES_UNIQUE_PHOTOS_LOCALPASS.zip`

SHA-256:
`a374a3003e5842f2517095e74e178765a31fdf42ae2c5a721027acd79d80975c`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.649_HOBBY_DEPOT_ALL_HUB2_BP_LAYOUT_PFERDE_TEXT_RULES_UNIQUE_PHOTOS_LOCALPASS.zip`

## Ausgang
**1.50.648 ist verworfen.**

Live-Befund:
- Pferdeatelier-Darstellung wurde fälschlich mitkopiert, obwohl nur die Textregeln übernommen werden sollten;
- dadurch stand ein zusätzlicher `Was du hier findest`-Block unter dem Aufklapper;
- Unterkategoriekarten wiederholten teilweise dasselbe Elternmotiv;
- kleine Untertitel der Karten fehlten bzw. waren nicht wie beim akzeptierten Buch-&-Papier-Stand gebunden.

## 1.50.649
Basis ist wieder **1.50.645**. Der akzeptierte Buch-&-Papier-Aufbau bleibt die visuelle Vorlage.

### Text
Die **redaktionellen Textregeln** aus Pferdeatelier wurden separat und dauerhaft gebunden:
`DESIGN/TEXTREGELN_PFERDEATELIER_KOPIE_20261012.md`

Übernommen wird ausschließlich:
- ca. 150–200 Wörter;
- natürliches Deutsch;
- themenspezifische Substanz;
- keine Generator-/Padding-Sprache;
- keine generische Schlussformel;
- fachliche Orientierung statt Meta-Sätze.

Die Darstellung bleibt Hobby Depot / Buch & Papier:
**sichtbarer Lead → `Mehr zu <Kategorie> erfahren` → restlicher Text im Aufklapper.**
Kein zusätzlicher zweiter Erklärungstext darunter.

### Bilder / Karten
- alle vorhandenen Unterkategorien auf Hub2 erhalten Fotokarten;
- Buch & Papier behält exakt seine fünf akzeptierten Motive;
- pro anderer Hub2-Seite werden unterschiedliche Fotos verwendet;
- echtes Featured Image hat Vorrang;
- danach kontrollierte vorhandene Assets derselben Hobbywelt;
- kein wiederholtes Elternmotiv als Universalbild;
- jede Fotokarte erhält einen kleinen Untertitel;
- Bilder bleiben exakt im Kartenrahmen, Foto-Radius 0.

### Performance / Struktur
- **0 neue Bildassets**;
- 859/859 Assets byteidentisch zu 1.50.645;
- keine neue Taxonomie/Architektur;
- Header, Navigation und Ebene 1 unverändert;
- Kartenbilder lazy;
- Hero verwendet vorhandenes Kategorieasset.

## Vollprüfung
- reale Zielhierarchie: **65 Hub2-Seiten / 328 vorhandene direkte Kindseiten**;
- 65/65 Heroassets gefunden;
- 65/65 Claims vorhanden;
- generierte Kategorietexte: **157–176 Wörter**;
- 328/328 vorhandene Kindseiten erhalten Fotokarte;
- innerhalb jeder Hub2-Seite: **keine doppelte Foto-URL**;
- 328/328 Fotokarten mit Untertitel;
- PHP **52/52 PASS**;
- ZIP PASS;
- Release-Kette vollständig V150649, aktive alte Klassenreferenzen 0;
- Browser 1440 / 1024 / 900 / 760: Overflow 0;
- Bild/Slot-Abweichung 0;
- Hero-Bild bleibt beim Aufklappen dimensionsstabil.

## EXAKT EINE NEXT ACTION
**1.50.649 installieren und live Buch & Papier, Guss & Formen sowie mindestens eine Hub2-Seite aus einer anderen Hauptwelt prüfen.**
