# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR BREADCRUMB LIVE PASS / GLOSSAR HERO LIVE PASS / JOURNAL 1.50.497 LIVE FAIL / DESIGN 1.50.498 HART LOKAL POSITIV+NEGATIV RENDER-PASS / AUTOMATION CORE 1.3.0 SANDBOX LIVE PASS

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Glossar-Breadcrumb Inhalt + Position/Abstand: **LIVE PASS**. Nicht mehr anfassen.
- Glossar-Hero nach Design `1.50.494`: **LIVE PASS**. Breites Bild + weicher Übergang bestätigt.
- Automation Core `1.3.0` Sandbox unter `Glossar -> Automation -> Sandbox hart testen`: **LIVE PASS 2026-09-14**.
- Sandbox-Readback: `ok:true`; alle Tests `true`; `batch_upper_guard_100:true`; `production_write_performed:false`; Modus `SANDBOX`; Auto-Publish AUS; Produktion scharf AUS.

## Journal – Nutzerreadback nach 1.50.497

**LIVE FAIL.** Der Hero klebt sichtbar direkt unter dem Breadcrumb. Damit ist der behauptete lokale Sicht-PASS von 1.50.497 widerlegt.

Ursache der fehlerhaften Prüfung: 1.50.497 prüfte den beabsichtigten CSS-Abstand, aber nicht die tatsächlich gerenderte Bounding-Box-Distanz `hero.top - breadcrumb.bottom`. Zusätzlich existiert eine spezifischere Altregel:

`body.pftk-journal-root-image-gap-v150422.pftk-has-leading-page-image-v150385 ... .ast-container { padding-top:20px!important; }`

Sie konnte die weniger spezifische Reparaturregel überstimmen. Margin-basierter Abstand am Breadcrumb war dadurch nicht belastbar.

## Design-Kandidat 1.50.498

Paket: `PFERDE_ATELIER_DESIGN_V1.50.498_JOURNAL_GAP_RENDERFIX_INSTALLIEREN.zip`

SHA-256: `798d4fbd0d6c5452c1ff6b402cdb9f356365cdca7b31549d1bc9132921758293`

Umsetzung:
- Journal-Claim bleibt exakt `Mehr wissen – besser verstehen` ohne Punkt.
- Ockerfarbene Zeile bleibt exakt `WISSEN & INSPIRATION`.
- nur `PFERDE ATELIER –` bleibt entfernt.
- Breadcrumb selbst bekommt **keinen** Journal-Sondermargin mehr.
- die spezifische alte 20px-`ast-container`-Regel wird im Journal-Root mit mindestens gleicher Spezifität auf `padding-top:0` überschrieben.
- der sichtbare Abstand wird direkt am Journal-Wrapper erzwungen: Desktop `padding-top:34px`, mobil `24px`.
- Padding statt Margin: kein Margin-Collapse möglich.
- Glossar-Breadcrumb/Hero bleiben unverändert.

## Harte lokale Positiv-/Negativprüfung 1.50.498

Gemessen in Headless Chromium wird **nicht der CSS-Wert**, sondern die reale sichtbare Distanz:

`gap = hero.getBoundingClientRect().top - breadcrumb.getBoundingClientRect().bottom`

Positiv:
- Desktop 1200px: Journal `34px`, Glossar `34px` -> **PASS**.
- Mobil 500px: Journal `24px`, Glossar `24px` -> **PASS**.

Negativ:
- spezifische Override-Regel absichtlich entfernt -> Journal Desktop `54px`, mobil `44px` -> **Fehler erkannt / PASS**.
- Journal-Padding absichtlich auf `0` gesetzt -> Desktop `0px`, mobil `0px` -> **angeklebter Hero erkannt / PASS**.
- absichtlich falscher Abstand `40/30px` -> unterscheidet sich von Glossar `34/24px` -> **Fehler erkannt / PASS**.

Regression/Verpackung:
- PHP-Lint aller 5 PHP-Dateien -> **PASS**.
- gleicher 500-Dateien-Bestand wie 1.50.497; nur `pferde-template-kit.php` geändert -> **PASS**.
- Claim/Kicker-Vertrag -> **PASS**.
- ZIP-Stamm `affiliate-portal-template-kit/` -> **PASS**.
- ZIP-Lesetest -> **PASS**.
- Version `1.50.498` -> **PASS**.

Marker: `JOURNAL_150498_RENDER_BOUNDING_BOX_POS_NEG_PASS`.

## Harte Grenze

**Keine LIVE-Abnahme ohne Nutzerreadback.** 1.50.498 ist hart lokal positiv/negativ geprüft, aber bleibt bis Installation + realem Screenshot **LIVE OFFEN**.

## Core 1.3.0 – Automation

Sandbox LIVE PASS. Nächster realer Schritt ist `Pool jetzt aktualisieren`. Produktion scharf und Auto-Publish bleiben AUS. Danach Pool-Inhalt und Kandidatenstatus prüfen; `Automatiklauf jetzt starten` erst nach diesem Readback.
