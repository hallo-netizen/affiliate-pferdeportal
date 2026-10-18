# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.50.674 VISUELL/RESPONSIVE FAIL / 1.50.675 CODE PASS / ERSTE ZIP FALSCH GEPACKT / KORREKT REPACKAGED / LIVE OFFEN**

## Reales Live-Ergebnis 1.50.674

Vom Nutzer im Frontend belegt:
- Text/Claim lagen optisch zu dicht am linken Hero-Rand;
- der Fullbleed-Hero funktionierte nur bei breiten Desktop-Auflösungen;
- bei kleineren Desktop-/Tabletbreiten fiel die Seite auf die alte begrenzte Bildbreite zurück und ließ rechts Leerraum;
- unter der H1 stand weiterhin der alte lange Satz statt der freigegebenen Kurzzeile;
- auch der Claim blieb optisch im alten Layout statt im neuen Hero sauber positioniert.

Ursache:
1.50.674 hatte den Fullbleed-Fix nur für `min-width:1101px` ergänzt und ließ darunter die alte Hub2-Responsive-Regel weiterlaufen. Zusätzlich wurde der Hero-Einstieg weiterhin automatisch aus dem ersten Satz des langen Kategorietextes gezogen.

## 1.50.675 – zentrale Lösung, aktuell nur an Audio & HiFi gebunden

Kein neuer Bildsatz, keine andere Kategorie.

### Hero-Logik

Neue wiederverwendbare Klasse:
`hd-hub2-hero-fullbleed`

Aktuell bekommt **nur Audio & HiFi** diese Klasse.

Performance:
- ein vorhandenes Hero-Bild;
- kein zweiter Bildrequest;
- kein JavaScript;
- kein Blur/Backdrop-Blur;
- kein Masking;
- nur CSS-Verlauf;
- Header-Beige exakt `#f5f1e9`.

### Responsive

>=901 px:
- Fullbleed-Hero;
- Bild füllt 100 % der Hero-Breite;
- Text bekommt echten Innenabstand über `clamp()`;
- Claim/H1/Kurzzeile liegen auf einer beige auslaufenden Fläche;
- Bild läuft weich darunter weiter.

<=900 px:
- stabiler Stapel;
- Textblock oben;
- Bild darunter **100 % breit**, ohne 600-px-Maximalbreite und ohne rechten Leerraum.

Getestet:
1440 / 1180 / 1024 / 901 / 900 / 800 / 760 / 600 / 390 px.
Ergebnis:
- horizontaler Overflow 0 bei allen neun Breiten;
- Bildbreite = Hero-Breite in allen neun Fällen;
- kein leerer rechter Bereich.

### Text/Claim

Claim bleibt inhaltlich wie freigegeben:
`Klang, der begeistert.`

Aber Darstellung im Audio-Hero ist jetzt eigenständig angepasst:
- größer;
- mit echtem Innenabstand;
- Pinselunterstreichung bleibt;
- nicht mehr direkt am linken Außenrand.

H1:
`Audio & HiFi` bleibt echte H1.

Kurzzeile im Hero jetzt fest und unabhängig vom Langtext:
`Klang verstehen, Technik entdecken und selbst bauen.`

Der alte Hero-Satz `Du willst Klang selbst gestalten ...` kann im Hero nicht mehr erscheinen.

Der lange Text darunter wurde als eigener 161-Wörter-Text geführt und bleibt vollständig unter dem Hero:
- Pferdeatelier-Regeln eingehalten;
- reale Audio-Unterthemen;
- kein Generator-Schema.

## Scope-Schutz

Unverändert zu 1.50.674:
- 901/901 Assets byte-identisch;
- alle anderen Kategorien;
- Mega-Menü;
- Kategoriebaum;
- Audio-Unterkategorie-Kurzzeilen.

## QA

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.675_HOBBY_DEPOT_AUDIO_HIFI_RESPONSIVE_FULLBLEED_FIX_REPACKED_HARDPASS.zip`

SHA-256:
`356a8e9861f0c018e42620d311eb9985f48279b3a5d1ed26be321c63ddfa24bd`

PASS:
- erste 1.50.675-ZIP als INSTALLER VERWORFEN: äußerer Pluginordner fehlte;
- korrigierte ZIP enthält exakt `affiliate-portal-template-kit/` und `affiliate-portal-template-kit/pferde-template-kit.php` wie 1.50.674;
- 1041/1041 Innendateien byte-identisch zur technisch geprüften 1.50.675;
- PHP 73/73;
- aktiver Release-Chain-Scan ohne 1.50.674-Stale-Referenz;
- Render-Harness: Fullbleed-Klasse PASS;
- Claim PASS;
- H1 PASS;
- neue Kurzzeile PASS;
- alter Hero-Satz im Hero ABSENT;
- neuer Langtext PASS;
- 161 Wörter;
- 901/901 Assets identisch;
- Browser-Simulation 9 Breiten: 0 Overflow / Bild jeweils volle Hero-Breite;
- ZIP-Test PASS.

## EXAKT EINE NEXT ACTION

**1.50.675 über 1.50.674 installieren und nur Audio & HiFi bei breitem Fenster sowie einem halbbreiten Fenster prüfen.**
