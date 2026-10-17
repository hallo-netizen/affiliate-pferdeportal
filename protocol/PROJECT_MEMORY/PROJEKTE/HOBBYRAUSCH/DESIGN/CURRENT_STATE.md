# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.50.672 FRONTEND/FOTOS PASS / 1.50.673 AUDIO-&-HIFI-HERO+TEXT-PILOT LOCAL HARD PASS / LIVE-PILOTPRÜFUNG OFFEN**

## Live-Stand 1.50.672

Vom Nutzer im echten Frontend bestätigt:
- kritischer 1.50.671-Fatal behoben;
- Audio-&-HiFi-Seite lädt normal;
- die zuletzt korrigierten Bilder werden als passend akzeptiert.

Damit ist 1.50.672 der aktuelle funktionierende Live-Stand.

## Verbindliche Textregeln

Quelle:
`TEXTREGELN_PFERDEATELIER_KOPIE_20261012.md`
SHA: `721e3f77d021b3e07e29ed98c9f921d3e0669fa9`

Für Hub2-Kategorietexte:
- ca. 150–200 Wörter;
- natürliches normales Deutsch;
- themenspezifische Substanz;
- keine Generator-/Padding-/Füllsprache;
- keine generische Schlussformel;
- konkrete Orientierung;
- Anfänger und Fortgeschrittene berücksichtigen;
- nur reale Unterthemen nennen;
- direkte du-Ansprache, wenn natürlich;
- sichtbarer Lead -> `Mehr zu <Kategorie> erfahren` -> Rest im Aufklapper.

## 1.50.673 – nur Audio & HiFi als Pilot

**Keine andere Kategorie textlich oder im Hero-Layout verändert.**
**Alle 901 Bildassets gegenüber 1.50.672 byte-identisch.**

### Hero-Layout Audio & HiFi

Desktop >1100 px:
- links 34 %: Claim + H1 + exakt ein kurzer individueller Einstieg;
- rechts 66 %: vorhandenes scharfes Hero-Masterbild;
- Hero-Höhe bleibt 320 px;
- vorhandener Weißübergang bleibt, aber ohne zusätzliche Blur-Wirkung;
- langer Kategorietext bleibt vollständig unter dem Hero.

<=1100 px:
- unverändert gestapelt: Text oben, Bild darunter, Langtext danach.

### Hero-Kurztext

`Du willst Klang selbst gestalten und Technik wirklich verstehen – von Lautsprechern und Verstärkern bis zu Plattenspielern, Synthesizern und Eurorack.`

Keine Schablone `Bei Audio & HiFi geht es um ...`.

### Langer Audio-&-HiFi-Kategorietext

- 161 Wörter;
- reale Unterthemen: Lautsprecherbau, HiFi-Selbstbau, Plattenspieler restaurieren, Röhrenverstärker bauen, Synthesizer bauen, Eurorack, Effektpedale bauen;
- Einsteiger + Fortgeschrittene;
- relevante Sicherheit bei Röhren-/Netzspannung;
- keine künstlichen Unterthemen;
- kein generischer Abschluss.

Render:
- Hero-Satz: 20 Wörter;
- sichtbarer Text darunter: 68 Wörter;
- Aufklapper: 73 Wörter.

### Audio-&-HiFi-Unterkategorien – individuelle Kurzzeilen

Nur auf dieser Pilotseite:
- Effektpedale bauen -> Eigene Sounds löten, testen und verfeinern.
- Eurorack -> Module kombinieren und ein eigenes Klangsystem aufbauen.
- HiFi-Selbstbau -> Komponenten auswählen und dein Setup selbst entwickeln.
- Lautsprecherbau -> Gehäuse, Chassis und Weichen sinnvoll abstimmen.
- Plattenspieler restaurieren -> Mechanik pflegen, justieren und wieder sauber spielen lassen.
- Röhrenverstärker bauen -> Schaltung, Bauteile und Sicherheit im Blick behalten.
- Synthesizer bauen -> Klangerzeugung verstehen und eigene Schaltungen ausprobieren.

## Mega-Menü

Zielvertrag 4.5 nachgezogen:
- bis 10 direkte Zwischenbereiche / zwei Reihen sofort sichtbar;
- `Mehr Kategorien` erst ab 11 / nötiger dritter Reihe;
- aktueller V7.1-Stand 7/10/9/8/9/7/8/9 damit vollständig direkt sichtbar.

## Local QA 1.50.673

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.673_HOBBY_DEPOT_AUDIO_HIFI_HERO_TEXT_PILOT_HARDPASS.zip`

SHA-256:
`802d16fd6df5ccdd133bb390ff7d1eb7992640eee9f43627b4e58aa0c15846ef`

PASS:
- Audio-Textvertrag 161 Wörter;
- 7/7 individuelle Audio-Unterzeilen;
- keine doppelte Audio-Unterzeile;
- Audio-Prototypklasse real gerendert;
- 901/901 Assets zu 1.50.672 byte-identisch;
- AF-026 Release-Kette 7/7 PASS;
- Fronttemplate ausgeführt PASS;
- Contenttemplate ausgeführt PASS;
- Dirty-Overlay 1.50.672 -> 1.50.673 PASS;
- PHP 66/66;
- ZIP-Test PASS;
- Roundtrip 1034/1034 identisch.

## EXAKT EINE NEXT ACTION

**1.50.673 über 1.50.672 installieren und ausschließlich Audio & HiFi prüfen: Hero-Breite/Weißraum, kurzer Hero-Satz, Langtext und die sieben Karten-Unterzeilen.**
