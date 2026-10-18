# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.680 FRONTEND-WIEDERHERSTELLUNG BESTÄTIGT / 1.50.681 NO-ZOOM + KOMPAKTER TEXT GEBAUT / LOKAL POSITIV+NEGATIV+VISUELL PASS / WORDPRESS-READBACK OFFEN**

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.681_HOBBY_DEPOT_NOZOOM_COMPACT_TEXT.zip`

SHA-256:
`37ac20a8f6d00e6b3ab8501b186c3087867b0c397d4d33d0d14df1ae84b85e9d`

## Scope

Nur Hub2-Darstellung:
- Hero-Bild nicht mehr gezoomt/cropped;
- festes 600:320-Verhältnis auf allen Breakpoints;
- 600px-Bilder nie über 600px dargestellt;
- größere Master nur verkleinert;
- weicher Beigeübergang erhalten;
- sichtbarer Kategorietext ein Absatz ohne Leerzeile;
- Abstände und Chevron kompakter.

Keine Änderung:
- 901 Bildassets;
- Textwortlaut;
- 69 Hub2-Zuordnungen;
- Mega-Menü;
- Kategoriebaum.

## QA

- PHP 90/90 PASS;
- ZIP PASS;
- Route Front V150681 PASS;
- Route Content V150681 PASS;
- beide Templates positiv PASS;
- beide Templates negativ gegen V150680 erwartungsgemäß FAIL;
- 69/69 Hub2-Render PASS;
- Paketdelta: 1 geändert / 3 neu / 0 entfernt;
- 901/901 Assets identisch;
- visueller Inline-Chromium-Test 1440/1024/901/900/760/390 PASS;
- echte 600px-Quelle: gerendert maximal 600px;
- echter 1600px-Master: gerendert maximal 600px;
- gleiches 600:320-Bildformat Desktop/Mobil.

## EXAKT EINE NEXT ACTION

**1.50.681 installieren und WordPress-Readback von Schärfe, identischem Bildausschnitt und kompakter Textdarstellung durchführen.**
