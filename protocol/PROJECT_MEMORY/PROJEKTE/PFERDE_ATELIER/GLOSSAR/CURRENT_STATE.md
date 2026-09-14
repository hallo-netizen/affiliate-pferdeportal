# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR BREADCRUMB LIVE PASS / GLOSSAR HERO LIVE PASS / JOURNAL DESIGN 1.50.498 LOKAL HART POSITIV+NEGATIV RENDER-PASS, LIVE OFFEN / AUTOMATION SANDBOX LIVE PASS / POOL-REFRESH TECHNISCH LIVE PASS / CORE 1.3.1 POOL-INHALT FACHLICH LIVE FAIL / CORE 1.3.2 TERM-EXTRACTOR LOKAL HART POSITIV+NEGATIV PASS

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Glossar-Breadcrumb Inhalt + Position/Abstand: **LIVE PASS**. Nicht mehr anfassen.
- Glossar-Hero nach Design `1.50.494`: **LIVE PASS**. Breites Bild + weicher Übergang bestätigt.
- Automation-Sandbox: **LIVE PASS 2026-09-14**.
- Sandbox-Readback: `ok:true`; alle Positiv-/Negativtests `true`; `batch_upper_guard_100:true`; `production_write_performed:false`; Modus `SANDBOX`; Auto-Publish AUS; Produktion scharf AUS.
- `Pool jetzt aktualisieren`: **technisch LIVE PASS**. 14 Rohfundstellen wurden geladen; kein Produktionswrite.

## Pool 1.3.1 – fachlicher LIVE FAIL

Die neue Prüftabelle hat den tatsächlichen Fehler sichtbar gemacht: Core 1.3.1 übernimmt komplette PSTE-SEO-/Artikeltitel direkt als Glossar-Kandidaten. Beispiele aus dem Live-Readback:

- `Das Wichtigste über Hindernisstangen für Pferde`
- `Die geeigneten Regendecken mit Abschwitzfunktion finden`
- `Kosten für Reitplatzbeleuchtung`
- `Mistcontainer mit Deckel wählen`
- `Wie reinigt man Pferdebürsten?`

Diese Zeilen sind **keine Glossarbegriffe**. Deshalb darf `Automatiklauf jetzt starten` nicht freigegeben werden.

## Core-Kandidat 1.3.2 – PSTE Term Extractor

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.3.2_TERM_EXTRACTOR_INSTALLIEREN.zip`

SHA-256: `a48fd1c821a3516bd0385e3337a425183768cd36206b7af189fdc1bba5fa3706`

### Umsetzung

- PSTE-Rohfundstellen werden nicht mehr direkt als Kandidatenlabel gespeichert.
- deterministischer, konservativer Extractor erzeugt maximal einen fachlichen Kopfbegriff oder verwirft den Rohfund.
- keine freie Umformulierung; keine erfundenen Synonyme.
- alte ungeprüfte 1.3.0/1.3.1-PSTE-Titelkandidaten werden beim nächsten Pool-Refresh entfernt.
- geschützte Zustände `GEPRUEFT`, `READY`, `PUBLISHED`, `BESTAND` bleiben erhalten.
- gemischte Kandidaten mit zusätzlicher Nicht-PSTE-Quelle bleiben erhalten; nur die alte PSTE-Quelle wird entfernt.
- Rohfund, PSTE-Referenz und verwendete Extraktionsregel bleiben am Begriff als Provenienz gespeichert.
- Prüftabelle zeigt zusätzlich `Rohfund` und `Extraktion`.

### Harte lokale Positivprüfung – exakt gegen die 14 Live-Rohfundstellen

14/14 Rohfundstellen wurden deterministisch verarbeitet und zu 9 eindeutigen Begriffen dedupliziert:

- `Hindernisstange`
- `Regendecke`
- `Reitplatzbeleuchtung`
- `Mistcontainer`
- `Pferdehaftpflicht`
- `Huffett`
- `Fliegenmaske`
- `Pferdebürste`
- `Pellet`

Weitere PASS-Nachweise:
- kein kompletter Editorial-/Artikeltitel überlebt als Kandidatenlabel;
- vier unterschiedliche Regendecken-Rohfundstellen -> genau ein Kandidat `Regendecke`, alle vier Rohfundstellen bleiben sichtbar;
- Rohfund + Extraktionsregel in Prüfansicht sichtbar;
- Legacy-Migration entfernt alle 14 alten ungeprüften PSTE-Titelkandidaten;
- `GEPRUEFT` und Nicht-PSTE-Kandidaten bleiben erhalten;
- gemischte Quellen bleiben erhalten.

### Harte Negativprüfung

- Extraktionsregel `Die geeigneten ... mit ...` absichtlich entfernt -> Test ROT.
- Singularisierung `Regendecken -> Regendecke` absichtlich gebrochen -> Test ROT.
- Legacy-Cleanup absichtlich deaktiviert -> Test ROT.
- bewusst unklare Editorial-Sätze wie `Welche Regendecke ist die beste für mein Pferd?`, `Warum ist mein Pferd heute so müde?`, `10 Tipps für den perfekten Pferdealltag`, `Pferd kaufen – kompletter Ratgeber` -> vollständig abgelehnt, kein Kandidat.

### Sicherheits-/Regressionstest

Gegen 1.3.1 unverändert:
- `publish_verified`
- `run_cycle`
- `cron_run`
- `sandbox_test`
- `admin_settings`
- `accept_research_package`
- `validate_package`

Damit ändert 1.3.2 nur Kandidatengewinnung/Prüfbarkeit, nicht die bereits getestete Publish-/Sandbox-Sicherheitslogik.

Verpackung:
- PHP-Lint aller 3 PHP-Dateien PASS.
- Dateibestand wie 1.3.1: 3 Dateien.
- `class-uge-pferde-content-pack.php` bytegleich.
- ZIP-Stamm `universal-glossary-engine/` PASS.
- ZIP-Lesetest PASS.
- Version 1.3.2 PASS.

## Journal

Design `1.50.498` bleibt lokal hart positiv/negativ geprüft, aber bis realem Nutzerreadback **LIVE OFFEN**. Gemessen wurde in Headless Chromium die gerenderte Bounding-Box-Distanz `hero.top - breadcrumb.bottom`: Desktop Journal 34 px = Glossar 34 px; mobil 24 px = 24 px. Negativfälle 0 px, 54/44 px und 40/30 px wurden zuverlässig rot erkannt.

## Harte Grenze / NEXT ACTION

1. Core `1.3.2` über `1.3.1` installieren.
2. `Glossar -> Automation -> Pool jetzt aktualisieren` erneut klicken.
3. Prüftabelle kontrollieren: In `Begriff` dürfen keine kompletten SEO-/Artikeltitel mehr stehen; diese dürfen nur noch unter `Rohfund` erscheinen.
4. Produktion scharf und Auto-Publish bleiben AUS.
5. Erst nach diesem LIVE-Readback darf der nächste Automatikschritt geprüft werden.
