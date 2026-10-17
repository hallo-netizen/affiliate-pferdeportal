# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.50.673 TECHNISCH PASS / AUDIO-HERO GRAFISCH VERWORFEN / 1.50.674 FULLBLEED-BEIGE-HERO LOCAL HARD PASS / LIVE-PRÜFUNG OFFEN**

## Live-Stand

1.50.673 läuft technisch und die Bildqualität ist bestätigt.

Grafischer Befund Audio & HiFi:
- 34/66-Aufteilung wirkt wie zwei getrennte Blöcke;
- zu viel optische Trennung links/rechts;
- Hero soll stattdessen als eine zusammenhängende Fläche wirken.

## 1.50.674 – nur Audio & HiFi Hero

Keine andere Kategorie geändert.

Desktop >1100 px:
- Hero bleibt 320 px hoch;
- bestehendes scharfes Audio-Hero-Masterbild läuft über die volle Hero-Breite;
- links blendet das Bild weich in **exakt #f5f1e9** über, identisch zur Header-Hintergrundfarbe;
- kein Logo im Hero;
- Claim `Klang, der begeistert.` mit vorhandener Pinselunterstreichung bleibt;
- `Audio & HiFi` bleibt echte H1;
- darunter nur die kurze Zeile `Klang verstehen, Technik entdecken und selbst bauen.`;
- langer 161-Wörter-Kategorietext bleibt darunter;
- Tablet/Mobil bleiben gestapelt.

Unverändert:
- 901/901 Bildassets gegenüber 1.50.673 byte-identisch;
- Audio-Unterkategorie-Kurzzeilen;
- Mega-Menü;
- Kategorien;
- alle übrigen Hub2-Seiten.

## QA

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.674_HOBBY_DEPOT_AUDIO_HIFI_FULLBLEED_BEIGE_HERO_HARDPASS.zip`

SHA-256:
`c40e3271bc31c822aeb076f51880d8c2ef222f27ff31a05f29b4dcc0bf2f98e9`

PASS:
- PHP 69/69;
- Release-Kette ohne aktive 1.50.673-Stale-Referenz;
- aktive Profilklasse/Route/Templates 1.50.674 konsistent;
- H1 im echten Renderer erhalten;
- Claim/Pinsel erhalten;
- kein Hero-Logo;
- Beige exakt #f5f1e9 wie Header;
- Audio-Scope über `hd-audio-hifi-prototype` begrenzt;
- 901/901 Assets identisch;
- ZIP-Test PASS.

## EXAKT EINE NEXT ACTION

**1.50.674 über 1.50.673 installieren und ausschließlich Audio & HiFi im Frontend prüfen.**
