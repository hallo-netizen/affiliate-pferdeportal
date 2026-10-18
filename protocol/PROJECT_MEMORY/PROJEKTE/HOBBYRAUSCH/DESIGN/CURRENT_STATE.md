# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.681 LIVE-READBACK VISUELL NICHT ABGENOMMEN / METALL-ALTERNATIVE 1.50.682 GEBAUT UND LOKAL GEPRÜFT / NUR METALL-PILOT / WORDPRESS-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 4.8 / 2026-10-18**

## REALER READBACK 1.50.681

Nutzerbefund:
- Hero auf Metall wirkt weiterhin zu nah/zu stark beschnitten;
- Ursache ist nicht ein anderes Motiv: das Metall-Kategoriebild `metall-v150634.webp` ist die 200×107-Ableitung aus `metall-v150627.webp`;
- der Hero nutzt dieselbe 600×320-Szene, aber die linke Beige-/Fade-Überlagerung verdeckt einen großen Teil der Szene und lässt das Motiv dadurch wie gezoomt wirken;
- sichtbarer Metall-Text wirkt weiterhin wie zwei Blöcke; gewünschtes Ziel ist ein einziger kompakter Fließtext ohne Leerzeile.

## ALTERNATIVE 1.50.682 – NUR METALL

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.682_METALL_ALT_WHITE_FRAME_PILOT.zip`

SHA-256:
`4f9e23ff92aaeddcacc0c1f1b051c207a7b238b15dc53f2181de855099925b72`

Pilotaufbau:
- ausschließlich Seite `Metall`;
- Hero rechts bindet ausdrücklich das Original `subcategories/fertigen/metall-v150627.webp` (600×320), aus dem das Kategoriebild abgeleitet ist;
- komplettes Motiv sichtbar;
- kein Zoom/Crop;
- keine Beige-/Weiß-Verlaufsüberlagerung über dem Bild;
- links reines Weiß;
- Text- und Bildhälfte gemeinsam in einem dünnen 1-px-Rahmen;
- Desktop nebeneinander, Mobil gestapelt;
- Textwortlaut unverändert;
- sichtbarer Lead wird vor Ausgabe whitespace-normalisiert und als genau ein `p` gerendert; keine Leerzeile/`br`.

Alle anderen 68 Hub2 bleiben auf 1.50.681-Darstellung.

## QA 1.50.682

- aus exakter 1.50.681 gebaut;
- PHP 90/90 PASS;
- ZIP PASS;
- aktive Route Front V150682 PASS;
- aktive Route Content V150682 PASS;
- beide Templates positiv mit V150682 PASS;
- Negativtest gegen nur V150681 erwartungsgemäß FAIL;
- Dirty-Overlay 1.50.681 → 1.50.682 aktive Kette PASS;
- 901/901 Bildassets byte-identisch;
- Metall-Heroquelle exakt 600×320, gerendert maximal 600×320;
- Desktop 1440/1024/901 PASS;
- Mobil 900/390 PASS;
- Copy-Hintergrund Weiß PASS;
- Fade-Pseudoelemente aus PASS;
- Außenrahmen 1 px PASS;
- Desktop kein Text/Bild-Overlap PASS;
- sichtbarer Metall-Lead: 1 Absatz, 0 `br`, Margin oben/unten 0.

## EXAKT EINE NEXT ACTION

**1.50.682 installieren und ausschließlich Metall auf Desktop und Mobil beurteilen: Ist die Alternative mit weißem Textfeld, vollständigem Originalmotiv und dünnem Rahmen die bessere zentrale Hub2-Richtung?**

## NICHT ANFASSEN

- noch keine Übertragung auf die anderen 68 Hub2;
- keine neuen Bilder;
- Textinhalte nicht ändern;
- Mega-Menü/Kategoriebaum nicht ändern.
