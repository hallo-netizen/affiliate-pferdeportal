# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.682 METALL-ALTERNATIVE VERWORFEN / 1.50.683 METALL-SZENENMASTER + INDIVIDUELLE KARTENUNTERTITEL GEBAUT / LOKAL POSITIV+NEGATIV+VISUELL PASS / WORDPRESS-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 4.8 / 2026-10-18**

## METALL 1.50.683

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.683_METALL_SCENE_MASTER_CARDTEXT_PILOT.zip`

SHA-256:
`96315f620599527093fc8d9a6c380159b33bcf0b33dbbfc42dbc214c8580ec0a`

Umsetzung:
- aktuelles Hero-Prinzip mit Claim/H1/Kurzsatz auf gleicher Höhe bleibt;
- Metall nutzt den echten hochauflösenden Szenenmaster 2070×760;
- dieser Master ist die Quelle derselben Metall-Szenerie, aus der das bisherige 600×320-Kategoriebild abgeleitet wurde;
- Desktop: Bild rechts breit, vollständige horizontale Szene bleibt erhalten; Zuschnitt nur oben/unten;
- kein Hochskalieren: gerenderte Bildbreite bleibt deutlich unter 2070 px;
- Mobil: dieselbe vollständige Szene im nativen Seitenverhältnis, kein anderer Ausschnitt;
- bisheriger weißer Rahmen-Pilot 1.50.682 entfällt.

Kartenuntertitel auf Metall individuell:
- Kettenhemdflechten → `Ringe, Muster und bewegliche Geflechte.`
- Kunstschmieden → `Zierformen, Ornamente und geschmiedete Details.`
- Metallgießen → `Formen vorbereiten und Metall kontrolliert gießen.`
- Sandguss → `Formkasten, Sand und saubere Gussformen.`
- Schmieden → `Hitze, Hammerführung und Formgebung am Amboss.`

Keine generischen `loslegen / ausprobieren / praktische Einstiege / verstehen`-Zeilen auf diesen fünf Metall-Karten.

## QA

- PHP 93/93 PASS;
- ZIP PASS;
- Route Front V150683 PASS;
- Route Content V150683 PASS;
- Front-/Contenttemplate positiv V150683 PASS;
- Negativtest gegen V150682 erwartungsgemäß FAIL;
- 893/893 bestehende Bildassets byte-identisch;
- neu ausschließlich Metall-Master 2070×760;
- Vergleich Master → bisherige Metall-Quelle bestätigt dieselbe Szene;
- Browser 1440/1180/1024/901/900/760/390 PASS;
- Desktop-Bildcontainer-Verhältnis bei 901–1440 immer breiter als der Master: dadurch kein seitlicher Crop, nur oberer/unterer Zuschnitt;
- Mobil Master-Verhältnis vollständig erhalten;
- kein horizontaler Overflow.

## EXAKT EINE NEXT ACTION

**1.50.683 installieren und ausschließlich Metall prüfen. Bei visueller Abnahme dieselbe Master-/Szenenlogik und die individuellen Kartenuntertitel zentral auf die übrigen Hub2 ausrollen.**
