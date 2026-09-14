# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR BREADCRUMB LIVE PASS / GLOSSAR HERO LIVE PASS / JOURNAL-HERO 1.50.495 LOKAL HART POSITIV+NEGATIV PASS / AUTOMATION CORE 1.3.0 LIVE-SANDBOXPRUEFUNG OFFEN

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Breadcrumb-Inhalt und Breadcrumb-Position/Abstand nach Design `1.50.493`: **LIVE PASS 2026-09-14**. Nicht mehr anfassen.
- Glossar-Hero nach Design `1.50.494`: **LIVE PASS 2026-09-14**. Breites Bild + weicher Übergang bestätigt. Nicht mehr anfassen.

## Journal-Hero – Design-Kandidat 1.50.495

Nutzerauftrag 2026-09-14: dasselbe bewährte Hero-Konzept auf `/journal/` anwenden; Button entfernen; kurzer frecher Claim; passendes Foto; weicher Übergang.

Paket: `PFERDE_ATELIER_DESIGN_V1.50.495_JOURNAL_HERO_GLOSSAR_PRINZIP_INSTALLIEREN.zip`

SHA-256: `9f267e8495e159a818661a7813238234029ebbca59fbad9082ba4e53a2e46455`

Umsetzung:
- bestehendes thematisch passendes Journal-Pferdefoto bleibt als Asset erhalten;
- Hero folgt nun demselben Grundprinzip wie der abgenommene Glossar-Hero: rechte Bildfläche ab `35%`, `cover`, Creme→Bild-Verlauf direkt über dem sichtbaren Bild;
- Button `Themen entdecken` im Journal-Hero vollständig entfernt;
- H1 `Pferde Journal` bleibt erhalten;
- kurzer Claim: `Pferdewissen ohne Blabla.`;
- mobil eigener engerer Verlauf und breiter Bildbereich;
- restliche Journal-Seite unverändert.

Hart lokal:
- PHP-Lint aller PHP-Dateien: PASS;
- CTA-freier Hero: PASS;
- Claim: PASS;
- breites Bild / `cover`: PASS;
- weicher Verlauf: PASS;
- NEGATIV CTA wieder eingesetzt → Test rot: PASS;
- NEGATIV Verlauf entfernt → Test rot: PASS;
- NEGATIV `contain` eingesetzt → Test rot: PASS;
- NEGATIV Bild wieder schmal gesetzt → Test rot: PASS;
- NEGATIV Claim entfernt → Test rot: PASS;
- harte Regression: außerhalb Version + Journal-Hero-CSS + Journal-Hero-Markup **byteidentisch zu 1.50.494**: PASS;
- ZIP-Stamm `affiliate-portal-template-kit/`: PASS;
- vollständiger 509-Einträge-Dateibestand exakt wie 1.50.494: PASS;
- ZIP-Lesetest: PASS;
- Version `1.50.495`: PASS.

Marker: `JOURNAL_HERO_150495_POS_NEG_PASS`.

## Core 1.3.0 – Automation

Core 1.3.0 bleibt unverändert. Die reale WordPress-Sandboxprüfung unter `Glossar -> Automation -> Sandbox hart testen` ist weiterhin offen. Auto-Publish bleibt AUS.

## Harte Grenze

**Journal-Hero 1.50.495 ist lokal hart geprüft, aber noch kein LIVE PASS.** Erst Installation + Nutzerreadback schließen ihn.

## Nächster realer Schritt

1. Design `1.50.495` über 1.50.494 installieren.
2. `/journal/` prüfen: Button weg, Claim korrekt, Bild rechts breit, weicher Übergang sichtbar.
3. Glossar-Hero und Breadcrumb nur als Regression gegenprüfen; nicht verändern.
4. Danach `Glossar -> Automation -> Sandbox hart testen`.
