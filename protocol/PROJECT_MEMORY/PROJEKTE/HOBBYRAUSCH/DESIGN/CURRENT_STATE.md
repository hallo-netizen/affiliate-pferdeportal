# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.684 LIVE-READBACK HERO VISUELL FAIL / 1.50.685 HERO-SZENERIE-KORREKTUR GEBAUT / KERAMIK-&-GLAS PFLICHTTEST PASS / LOKAL POSITIV+NEGATIV+RESPONSIVE PASS / WORDPRESS-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.0 / 2026-10-18**

## REALER FEHLER 1.50.684

Keramik & Glas zeigte im echten WordPress-Readback, dass die technisch korrekte Masterdatei visuell trotzdem wie ein vergrößerter Ausschnitt wirkte.

Ursache:
- Master/Original war korrekt und enthielt die volle horizontale Szene;
- die Bildfläche lag rechts bei 70 %;
- der Textblock plus ca. 130–170 px breiter Verlauf verdeckte jedoch einen großen Teil der linken Bildfläche;
- dadurch blieb sichtbar nur ein enger Teil der Szene und der Hero wirkte erneut hineingezoomt.

## 1.50.685 – KORREKTUR

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.685_HERO_SCENE_VISIBILITY_FIX.zip`

SHA-256:
`a72b7baa257b09d3fc2f4112bdcb25e03bdbe8d6d120ae0d60764ee53f6c7b1e`

Änderung ausschließlich am Hub2-Hero:
- bestehende Original-/Masterbilder unverändert;
- Bildfeld jetzt ca. 72 % des Hero, begrenzt durch native Breite;
- kein Upscaling;
- horizontaler Bildinhalt bleibt vollständig;
- nur oben/unten darf beschnitten werden;
- Übergang stark verkürzt: Desktop ca. 64 px, 901–1180 px ca. 56 px;
- dadurch wird die Szene nicht mehr großflächig vom Beigebereich verdeckt;
- Mobil zeigt weiterhin dieselbe vollständige Szene im Masterverhältnis.

Texte, Kartenuntertitel, Kategoriebaum und Mega-Menü unverändert.

## PFLICHTTEST KERAMIK & GLAS

Quelle:
- Original `keramik-glas-source.png`: 1672×941;
- Szenenmaster `keramik-glas.webp`: 1672×614;
- Master entstand ausschließlich durch oberen/unteren Beschnitt; horizontale Szene blieb vollständig.

Browser:
- 1440 px: 979×300 Bildfeld, nur vertikaler Crop;
- 1180 px: 821×260, nur vertikaler Crop;
- 1024 px: 709×225, nur vertikaler Crop;
- 901 px: 620×220, nur vertikaler Crop;
- 900/760/390 px: vollständiges Masterverhältnis, kein anderer Ausschnitt;
- kein Upscaling;
- kein horizontaler Overflow.

## QA

- PHP 99/99 PASS;
- reale Front-Route → V150685 PASS;
- reale Content-Route → V150685 PASS;
- Front-/Contenttemplate positiv V150685 PASS;
- Negativtest mit ausschließlich V150684 scheitert erwartungsgemäß;
- 69/69 Hub2-Render PASS;
- 69 Master × 4 Desktopbreiten = 276 Geometrieprüfungen: 0 Upscaling, 0 seitlicher Crop;
- Browser-Repräsentativtest 49/49 PASS;
- ZIP PASS;
- Roundtrip 1139/1139 byte-identisch;
- Delta zu 1.50.684: 1 bestehende Datei geändert + 3 neue Dateien + 0 entfernt.

## EXAKT EINE NEXT ACTION

**1.50.685 installieren und Keramik & Glas zuerst real prüfen. Wenn die Szene jetzt wie bei Metall sichtbar bleibt, denselben Stand stichprobenartig auf weitere Hub2 lesen.**
