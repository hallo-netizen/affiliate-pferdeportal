# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LIVE 1.50.677 / AUDIO-&-HIFI-HERO NUTZERSEITIG ABGENOMMEN / PORTALWEITER HUB2-ROLLOUT 1.50.679 VORBEREITET / FINALPAKET OFFEN / KEIN LIVE-UPLOAD**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 4.7 / 2026-10-18**

## AKTUELLER BELASTBARER STAND

Die an Audio & HiFi entwickelte Hero-Regel ist vom Nutzer als Zielbild abgenommen und wird auf alle aktuell **69 Hub2-Seiten derselben Ebene** ausgeweitet:
- Hero-Bild Fullbleed;
- dynamischer Beige-/Textschutz statt starrem Bild/Text-Verhältnis;
- Desktop ca. 35–48 %, bei 901–1180 px ca. 42–58 % Textschutz;
- H1, Claim und kurzer Satz auf Desktop einzeilig;
- <=900 px gestapelt;
- CSS-only, keine zusätzliche Frontend-/DB-Abfrage.

Die bisherigen Hub2-Kategorietexte sind in großen Teilen schematisch erzeugt und werden nicht übernommen.

## TEXTROLLOUT

Verbindlich:
- 150–200 Wörter je Hub2 nach den kopierten Pferdeatelier-Textregeln;
- eigenständig redigiert und themenspezifisch, keine feste Generator-/Satzschablone;
- sichtbarer Lead ungefähr ein Drittel des Texts, niemals mehr als die Hälfte;
- Rest aufklappbar;
- kein sichtbarer Satz `Mehr zu <Kategorie> erfahren`;
- kleiner Chevron/Pfeil direkt unter dem Lead, geöffnet nach oben;
- Screenreader-Beschriftung bleibt erhalten;
- kein zusätzlicher redaktioneller Seitenendtext.

Für die 69 aktuellen Hub2-Slugs ist ein vollständiger individueller Textkorpus vorbereitet:
- 69/69 Kategorien;
- Gesamttexte 150–174 Wörter;
- sichtbare Leads 45–64 Wörter;
- Audio & HiFi bleibt inhaltlich auf dem bereits individuell überarbeiteten Stand und wird nur kompakter auf ungefähr ein Drittel sichtbaren Text aufgeteilt.

## TECHNISCHER STAND

1.50.678 bleibt der letzte vollständig gebaute Kandidat aus dem Audio-Pilot.
Der neue 1.50.679-Rollout ist logisch und synthetisch auf der zugänglichen 1.50.668-Quellbasis geprüft:
- 69/69 Hub2 gerendert;
- alte `Bei <Kategorie> geht es um …`-Schablone im Kandidatenpfad entfernt;
- individueller Hero-Kurztext und individueller Langtext je Hub2;
- Chevron-Aufklapper ohne sichtbares `Mehr zu …`;
- Release-Kette auf 1.50.679 im Testaufbau konsistent;
- PHP-Lint ohne Fehler.

**Das ist ausdrücklich noch kein Release-PASS.** Die exakten 1.50.678-Paketbytes sind im aktuellen Arbeitsweg nicht materialisierbar; deshalb wurde kein älterer Paketstand als vermeintliche 1.50.679 freigegeben.

## ERSTER OFFENER BLOCKER

Der vorbereitete 1.50.679-Rollout muss auf der **exakten 1.50.678-Quellbasis** gebaut werden, damit die späteren Hero-Master-, Release- und Responsive-Korrekturen garantiert erhalten bleiben.

## EXAKT EINE NEXT ACTION

**Den vorbereiteten 1.50.679-Rollout auf die exakte 1.50.678-Quelle anwenden und danach lokal positiv, negativ und regressiv prüfen; erst danach ein WordPress-Uploadkandidat.**

## NICHT ANFASSEN

- Mega-Menü nicht erneut umbauen;
- Kategoriebaum nicht ändern;
- keine alten Bildstände zurückholen;
- kein zusätzlicher Hub2-Seitenendtext;
- keine neue Architektur.
