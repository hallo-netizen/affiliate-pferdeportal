# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.627 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.627_HOBBY_DEPOT_HUB_COPY_IMAGES_NAV_FINAL_LOCALPASS.zip`

SHA-256:
`bc6690acd847dac08b646243a07f133b189b5facc5abc6ba58526a79d383d158`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.627_HOBBY_DEPOT_HUB_COPY_IMAGES_NAV_FINAL_LOCALPASS.zip`

## Delta 1.50.627

### Navigation
- ab 761 px exakt eine horizontale 8er-Zeile;
- alle acht Labels besitzen identische Y-/Bottom-Koordinate;
- `Sammeln` ausdrücklich mitgemessen;
- Pfeil sitzt in eigener Gridspalte und beeinflusst die Textbaseline nicht;
- Navigation direkt an der unteren Headerkante.

### Hub-Bilder
- 65 kontrollierte direkte Welt-Unterkategorie-Motive;
- alle 600×320;
- optisch stärker herangezoomt: größere Hauptmotive, weniger Nebenmotive/Detailrauschen;
- 65/65 unterschiedliche SHA-256;
- zusätzlicher perceptual dHash: Mindestabstand 92;
- kontrollierte Assets bleiben vor WordPress Featured Images.

### Texte der acht Hauptwelten
- Hero-Seitentexte komplett neu;
- alle acht unterschiedlich;
- direkte, natürliche Ansprache;
- beschreiben konkret, was der Nutzer dort findet;
- kein generischer Auto-Text.

### Hub1-Langtext
- `Mehr über <Welt> erfahren` vollständig aus dem Hauptkategorie-Ausgabepfad entfernt;
- stattdessen am Seitenende je Hauptwelt ein eigener längerer redaktioneller Text;
- klare Zwischenüberschriften;
- direkte Ansprache;
- semantisch passende Textlinks ausschließlich zu real vorhandenen direkten Unterkategorien;
- alle Link-Slugs gegen das zentrale Kategorieprofil validiert.

## Lokal
- PHP **10/10 PASS**;
- ZIP PASS;
- Klassen-/Templatebindung V150627 PASS;
- alte V150624/V150625/V150626-Klassenreferenzen 0;
- 65/65 Bilder 600×320;
- 65/65 SHA-eindeutig;
- dHash-Minimum 92;
- 8/8 Hero-Texte eindeutig;
- 8/8 Langtexte vorhanden;
- `Mehr über … erfahren` im aktiven Codepfad 0;
- Navigation Playwright 1600/1200/1024/900/800/761: gleiche Baseline inkl. Sammeln, Overflow 0;
- 760: Mobilepfad;
- Sammeln-Flyout viewport-safe.

## EXAKT EINE NEXT ACTION
**1.50.627 installieren und Technik + Pflanzen + Sammeln live prüfen.**
