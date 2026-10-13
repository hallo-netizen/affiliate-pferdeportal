# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **1.50.650 LOCAL HARD PASS / WORDPRESS-LIVE BILDER OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HUB2_IMAGE_CURATED_WIDER_CLEARER_NOFRAME_LOCALPASS.zip`

SHA-256:
`b3bf267ccfef1ae5efbdc4efa1df40f586d5a9ae78ee7c865906b04f113ac2d6`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_HOBBY_DEPOT_HUB2_IMAGE_CURATED_WIDER_CLEARER_NOFRAME_LOCALPASS.zip`

## Live-Befund 1.50.649
Vom Nutzer bestätigt:
- **Text PASS**;
- **Aufteilung PASS**.

Offen waren ausschließlich die Bilder:
- Hero-Szenen teilweise zu eng / nur Details;
- Unterkategoriebilder teilweise zu voll und unklar;
- teilweise sichtbare Rahmen-/Vignettenwirkung;
- teilweise inhaltlich unpassende Fallback-Bilder.

## 1.50.650 – nur Bildauswahl
Text, Claim, Fold, Untertitel, Raster, Banner, Produkte, Beiträge, Werbeplatz, Header, Navigation und Ebene 1 sind gegenüber 1.50.649 unverändert.

Bilddelta:
- 65/65 Hub2-Hero-Bilder auf eine feste kuratierte Asset-Map umgestellt;
- bevorzugt weiter gefasste vorhandene Szenen; Format/Layout unverändert;
- 328/328 vorhandene direkte Kindseiten erhalten eine deterministische Fotobindung;
- kein zufälliger Welt-Pool-Fallback mehr, solange die geprüfte Map greift;
- Bildzuordnung wird thematisch über Elternbereich + konkrete Unterkategorie gebunden;
- innerhalb derselben Hub2-Seite keine doppelte Bilddatei;
- sämtliche v150631-Motive mit sichtbarer Vignetten-/Rahmenwirkung aus der aktiven Hub2-Map ausgeschlossen;
- Buch & Papier behält seine fünf akzeptierten, bereinigten v150645-Kartenbilder;
- **keine neuen Bilddateien erzeugt**: vorhandene Assets werden performance-schonend wiederverwendet.

## Lokal geprüft
- PHP **55/55 PASS**;
- ZIP PASS;
- Release-Kette vollständig V150650; aktive V150649-Bindung 0;
- 65 Hero-Mappings / 328 Karten-Mappings;
- fehlende gemappte Assets: 0;
- v150631 aktiv: 0;
- doppelte Karten-Bilddateien innerhalb einer Hub2-Seite: 0;
- 191 unterschiedliche vorhandene Bildassets aktiv;
- alle aktiven gemappten Bilder 600×320;
- automatischer Außenkantencheck: 0 weiße eingebrannte Frame-Verdachtsfälle;
- `Papier & Dokumente` und `Guss & Formen` zusätzlich mit echten 200×107-Kartenausschnitten visuell geprüft;
- Code-Diff gegen 1.50.649 bestätigt: Text- und Layoutlogik nicht verändert.

## EXAKT EINE NEXT ACTION
**1.50.650 installieren und live die Bilder auf Papier & Dokumente, Guss & Formen sowie stichprobenartig weiteren Hub2-Seiten prüfen.**
