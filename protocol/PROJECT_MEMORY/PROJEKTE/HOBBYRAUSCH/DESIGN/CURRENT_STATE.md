# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.680 WORDPRESS-FRONTEND OHNE FATAL / VISUELLER READBACK: HERO-UPSCALING + RESPONSIVE-AUSSCHNITT FALSCH / 1.50.681 GEBAUT UND LOKAL POSITIV+NEGATIV+VISUELL GEPRÜFT / WORDPRESS-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 4.8 / 2026-10-18**

## REALER READBACK 1.50.680

Nutzer-Readback:
- Hobby-Depot-Seiten laden wieder ohne den 1.50.679-Fatal;
- Hub2-Heroes wirken unscharf, weil 600×320-Quellen durch `object-fit:cover` über den ganzen Hero hochskaliert und gecroppt wurden;
- Desktop und Mobil zeigten dadurch unterschiedliche Bildausschnitte;
- Texte inhaltlich akzeptiert;
- Textdarstellung unter dem Hero zu luftig, insbesondere durch zwei sichtbare Absätze/Leerzeile.

## 1.50.681 – KORREKTUR

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.681_HOBBY_DEPOT_NOZOOM_COMPACT_TEXT.zip`

SHA-256:
`37ac20a8f6d00e6b3ab8501b186c3087867b0c397d4d33d0d14df1ae84b85e9d`

Hero:
- einheitliches Bildformat **600:320** auf Desktop, Tablet und Mobil;
- `object-fit:contain` statt `cover`;
- keine Quelle wird über ihre native Breite hochskaliert;
- 600×320-Quellen maximal 600 px breit;
- 1600×853-Master werden nur heruntergerechnet;
- gleicher vollständiger Bildausschnitt auf allen Breakpoints;
- weicher Beige-Verlauf am linken Bildrand bleibt;
- Desktop dynamischer Textschutz bleibt 35–48 %, bei 901–1180 px 42–58 %;
- Mobil-H1 darf natürlich umbrechen statt abgeschnitten zu werden.

Kategorietext:
- Wortlaut der 69 Texte unverändert;
- sichtbarer Lead bleibt im vorhandenen Umfang ca. 45–64 Wörter;
- Lead wird als **ein zusammenhängender Absatz** gerendert, keine künstliche Leerzeile;
- vertikale Abstände verkleinert;
- kleiner Chevron näher am Text;
- kein zusätzlicher Kasten;
- kein zusätzlicher sichtbarer Text nötig.

## QA 1.50.681

- aus exakter 1.50.680 gebaut;
- ZIP PASS;
- PHP 90/90 PASS;
- aktive Release-Kette V150681 PASS;
- reale Front-Route → V150681 PASS;
- reale Content-Route → V150681 PASS;
- Front-/Contenttemplate positiv mit V150681 PASS;
- Negativtest mit nur V150680 scheitert erwartungsgemäß auf fehlender V150681-Klasse;
- Paketdelta gegen 1.50.680: **1 Datei geändert + 3 neue Dateien + 0 entfernt**;
- 901/901 Bildassets byte-identisch;
- 69/69 Hub2-Text-/Renderprüfung PASS;
- Inline-Chromium-Test mit echten 600×320- und 1600×853-Bildern bei 1440/1024/901/900/760/390 px PASS;
- dabei keine Bildbreite über 600 px, keine Quelle über Natural Width, Bildverhältnis durchgehend 600:320, kein horizontaler Overflow.

## EXAKT EINE NEXT ACTION

**1.50.681 installieren und Imkerei & Bestäuber sowie zwei weitere Hub2 auf Desktop und Mobil gegen den Nutzer-Screenshot prüfen: Bild scharf, kompletter identischer Ausschnitt, Text kompakt ohne Leerzeile.**

## NICHT ANFASSEN

- Textinhalte nicht neu schreiben;
- Bilddateien nicht hochskalieren;
- Kategoriebaum nicht ändern;
- Mega-Menü nicht ändern;
- keine neue Architektur.
