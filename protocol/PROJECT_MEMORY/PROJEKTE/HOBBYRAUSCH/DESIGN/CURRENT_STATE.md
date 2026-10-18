# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LIVE 1.50.677 / 1.50.679 AUS EXAKTER 1.50.678 GEBAUT / TEXT+RENDER 69/69 PASS / BILDQUALITÄTS-READBACK OFFEN / KEIN LIVE-PASS**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 4.7 / 2026-10-18**

## AKTUELLER KANDIDAT 1.50.679

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.679_HOBBY_DEPOT_ALL_HUB2_TEXT_HERO_ROLLOUT.zip`

SHA-256:
`721a7843c862cc59b47d80e51035d589220a56ecf4a5a8caad2307e921801f4d`

1.50.679 wurde aus dem **exakten 1.50.678-Paket** gebaut. Keine Rekonstruktion auf älterem Stand.

## PORTALWEITER HUB2-ROLLOUT

Für alle aktuell **69 Hub2-Seiten**:
- die bestehende dynamische Fullbleed-Hero-Regel aus 1.50.678 wird zentral verwendet;
- Audio & HiFi ist keine Sonderbindung mehr;
- Desktop Textschutz 35–48 %, bei 901–1180 px 42–58 %;
- H1, Claim und Kurzzeile Desktop einzeilig;
- <=900 px gestapelt;
- CSS-only, keine neue Frontend-/DB-Abfrage;
- keine doppelte neue Hero-CSS über die bestehende 1.50.678-Regel gelegt.

## TEXTE

Die alte feste Hub2-Generator-Schablone ist im aktiven Kandidatenpfad entfernt.

69/69 aktuelle Hub2 haben eigenständig redigierte Texte:
- 150–174 Wörter je Gesamttext;
- sichtbare Leads 45–64 Wörter, ungefähr ein Drittel und nie mehr als die Hälfte;
- echter Informationswert bereits im sichtbaren Lead;
- Rest über kleinen Chevron/Pfeil;
- kein sichtbarer Satz `Mehr zu <Kategorie> erfahren`;
- Screenreader-Beschriftung bleibt erhalten;
- kein zusätzlicher Seitenendtext.

Audio & HiFi bleibt inhaltlich auf dem bereits individuell überarbeiteten Stand; sichtbar sind jetzt 48 von 162 Wörtern.

## QA

PASS:
- Paketwurzel korrekt;
- ZIP-Test PASS;
- PHP 84/84 PASS;
- aktive 1.50.679-Releasekette PASS;
- positiver Template-Ausführungstest PASS;
- negativer Test mit nur alter 1.50.678-Klasse scheitert erwartungsgemäß;
- 69/69 Hub2-Render PASS;
- unbekannter Hub2 erzeugt keine alte Textschablone;
- 901/901 Bildassets gegenüber 1.50.678 byte-identisch;
- 69/69 Hub2 haben ein eigenes vorhandenes Hero-Asset;
- 69/69 Hero-Pfade eindeutig;
- kein Welt-/Fallback-Hero.

## OFFENER BILDQUALITÄTS-PUNKT

Beim vollständigen Asset-Audit:
- 19 Hub2-Heroes liegen als 1600×853-Master vor;
- 50 bestehende Hub2-Heroes liegen noch in 600×320 vor.

Diese 50 Dateien stammen unverändert aus 1.50.678. Da die Fullbleed-Regel nun portalweit greift, ist für diese Bilder ein echter WordPress-Readback auf Schärfe zwingend. Sichtbares Hochskalieren darf nach Zielvertrag nicht als finaler PASS akzeptiert werden.

## ERSTER OFFENER BLOCKER

Portalweiter visueller WordPress-Readback von 1.50.679, insbesondere der 50 bestehenden 600×320-Heroes.

## EXAKT EINE NEXT ACTION

**1.50.679 als Testkandidat installieren und mehrere kurze sowie lange Hub2-Titel plus mindestens einen 600×320- und einen 1600×853-Hero auf Desktop, mittlerer Breite und Mobil prüfen. Bei sichtbarer Unschärfe der 600×320-Heroes anschließend nur diese Bildmaster ersetzen; Text- und Layoutlogik nicht erneut umbauen.**

## NICHT ANFASSEN

- Mega-Menü nicht erneut umbauen;
- Kategoriebaum nicht ändern;
- keine alte Textschablone reaktivieren;
- kein zusätzlicher Hub2-Seitenendtext;
- keine neue Architektur.
