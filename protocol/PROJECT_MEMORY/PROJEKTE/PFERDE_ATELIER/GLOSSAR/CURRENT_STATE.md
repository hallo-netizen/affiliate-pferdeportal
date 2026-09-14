# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR BREADCRUMB LIVE PASS / GLOSSAR HERO LIVE PASS / JOURNAL-HERO 1.50.496 LOKAL HART POSITIV+NEGATIV PASS / AUTOMATION CORE 1.3.0 LIVE-SANDBOXPRUEFUNG OFFEN

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Glossar-Breadcrumb Inhalt + Position/Abstand: **LIVE PASS**. Nicht mehr anfassen.
- Glossar-Hero nach Design `1.50.494`: **LIVE PASS**. Breites Bild + weicher Übergang bestätigt.

## Journal-Hero – Design-Kandidat 1.50.496

Nutzerreadback 2026-09-14 nach 1.50.495:
- Hero-Prinzip grundsätzlich übernommen;
- Claim `Pferdewissen ohne Blabla.` soll ersetzt werden;
- ockerfarbene Zeile `Pferde Atelier – Wissen & Inspiration` soll entfallen;
- Abstand Breadcrumb → Hero ist auf `/journal/` zu groß und soll exakt wie beim Glossar sein;
- Glossar-Claim soll ebenfalls keinen Punkt am Ende haben.

Paket: `PFERDE_ATELIER_DESIGN_V1.50.496_JOURNAL_CLAIM_GAP_INSTALLIEREN.zip`

SHA-256: `5fce725f3b2b38ff7f26bfaef05f75830f2ee18eda545fe9ba1038741b663ae8`

Umsetzung:
- Journal-Claim exakt: `Mehr wissen – besser verstehen`;
- kein Punkt am Ende;
- ockerfarbene Journal-Kickerzeile komplett entfernt;
- Glossar-Claim jetzt `Begriffe sattelfest erklärt` ohne Punkt;
- Journal übernimmt exakt die freigegebenen Glossar-Abstände Breadcrumb → Hero: Desktop `34px`, mobil `24px`;
- alter Journal-Zwischenweg über zusätzlichen `.ast-container`-Topabstand wird für Journal-Root auf `0` neutralisiert;
- breites Journalbild + weicher Creme→Bild-Verlauf aus 1.50.495 bleiben unverändert;
- Breadcrumb selbst wird nicht verändert.

Hart lokal:
- PHP-Lint aller PHP-Dateien: PASS;
- Journal-Claim exakt: PASS;
- alte Claim-Zeile entfernt: PASS;
- ockerfarbene Journal-Kickerzeile entfernt: PASS;
- Glossar-Claim ohne Punkt: PASS;
- Journal Desktop-Abstand exakt Glossar `34px`: PASS;
- Journal Mobil-Abstand exakt Glossar `24px`: PASS;
- zusätzlicher Journal-Containerabstand neutralisiert: PASS;
- NEGATIV alter Journal-Abstand zurück → Test rot: PASS;
- NEGATIV alter Claim zurück → Test rot: PASS;
- NEGATIV Kicker zurück → Test rot: PASS;
- NEGATIV Glossar-Punkt zurück → Test rot: PASS;
- NEGATIV alter Containerabstand zurück → Test rot: PASS;
- Hero `cover` + weicher Verlauf Regression: PASS;
- Tree gegen 1.50.495: exakt gleicher 500-Dateien-Bestand, nur `pferde-template-kit.php` geändert: PASS;
- ZIP-Stamm `affiliate-portal-template-kit/`: PASS;
- ZIP-Lesetest: PASS;
- Version `1.50.496`: PASS.

Marker: `JOURNAL_HERO_150496_CLAIM_GAP_POS_NEG_PASS`.

## Core 1.3.0 – Automation

Core 1.3.0 bleibt unverändert. Die reale WordPress-Sandboxprüfung unter `Glossar -> Automation -> Sandbox hart testen` ist weiterhin offen.

## Harte Grenze

**Journal-Hero 1.50.496 ist lokal hart geprüft, aber noch kein LIVE PASS.** Erst Installation + Nutzerreadback schließen Journal-Claim und Abstand.

## Nächster realer Schritt

1. Design `1.50.496` über 1.50.495 installieren.
2. `/journal/` prüfen: `Mehr wissen – besser verstehen`, keine ockerfarbene Kickerzeile, Breadcrumb→Hero-Abstand wie Glossar.
3. Glossar nur Regression: Claim ohne Punkt; Hero/Breadcrumb ansonsten unverändert.
4. Danach `Glossar -> Automation -> Sandbox hart testen`.
