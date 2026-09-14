# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR BREADCRUMB LIVE PASS / GLOSSAR HERO LIVE PASS / JOURNAL 1.50.496 LIVE FAIL / DESIGN 1.50.497 LOKAL HART POSITIV+NEGATIV BROWSER-PASS / AUTOMATION CORE 1.3.0 LIVE-SANDBOXPRUEFUNG OFFEN

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Glossar-Breadcrumb Inhalt + Position/Abstand: **LIVE PASS**. Nicht mehr anfassen.
- Glossar-Hero nach Design `1.50.494`: **LIVE PASS**. Breites Bild + weicher Übergang bestätigt.

## Journal – Nutzerreadback nach 1.50.496

**LIVE FAIL.** Zwei konkrete Fehler:

1. Abstand Breadcrumb → Journal-Hero weiterhin sichtbar größer als beim Glossar.
2. Ockerfarbene Zeile wurde zu weit entfernt. Verbindlich soll nur `PFERDE ATELIER –` entfallen; `WISSEN & INSPIRATION` muss bleiben.

### Tatsächliche Ursache Abstand

1.50.496 verglich nur Einzelwerte und neutralisierte nur den direkten `.ast-container`-Topabstand. Auf der realen Journalseite liegen zwischen Breadcrumb und Hero zusätzlich die Astra/WordPress-Wrapper:

`Breadcrumb -> ast-container -> content-area -> site-main -> article.page -> entry-content -> Journal -> Hero`

Diese komplette vertikale Kette wurde in 1.50.496 nicht als Einheit geprüft. Deshalb war der lokale PASS unzureichend und darf nicht als belastbarer Sicht-PASS gelten.

## Design-Kandidat 1.50.497

Paket: `PFERDE_ATELIER_DESIGN_V1.50.497_JOURNAL_GAP_KICKER_HARDFIX_INSTALLIEREN.zip`

SHA-256: `47ffd7a4ba19ceabd882e108c854cdeae1de28e06729f01db16b22a557b10e0e`

Umsetzung:
- Journal-Claim bleibt exakt `Mehr wissen – besser verstehen` ohne Punkt.
- Ockerfarbene Zeile ist wieder vorhanden und lautet exakt `WISSEN & INSPIRATION`.
- nur `PFERDE ATELIER –` wurde entfernt.
- vollständige Journal-Wrapperkette zwischen Breadcrumb und Hero wird auf `margin-top:0` / `padding-top:0` neutralisiert.
- einzig verbleibender Abstand ist derselbe freigegebene Breadcrumb-Abstand wie beim Glossar: Desktop `34px`, mobil `24px`.
- die Regel ist auf den Journal-Root-Scope begrenzt; Glossar-Breadcrumb/Hero werden nicht verändert.
- breites Journalbild + weicher Creme→Bild-Verlauf bleiben unverändert.

## Harte lokale Prüfung 1.50.497

Nicht nur String-/CSS-Wert-Test, sondern Headless-Chromium-Render mit real nachgebildeter Journal-Wrapperstruktur und absichtlich vorhandenen Theme-Zusatzabständen:

- Desktop Glossar sichtbarer Gap: `34px`.
- Desktop Journal 1.50.497 sichtbarer Gap: `34px` -> PASS.
- Mobil Glossar sichtbarer Gap: `24px`.
- Mobil Journal 1.50.497 sichtbarer Gap: `24px` -> PASS.
- NEGATIV mit altem 1.50.496-Mechanismus: Desktop Journal `80px`, mobil `70px` -> Fehler zuverlässig reproduziert.
- `WISSEN & INSPIRATION` vorhanden -> PASS.
- `PFERDE ATELIER – WISSEN & INSPIRATION` nicht vorhanden -> PASS.
- Claim exakt und ohne Punkt -> PASS.
- Glossar-Claim ohne Punkt Regression -> PASS.
- PHP-Lint aller PHP-Dateien -> PASS.
- exakt gleicher 500-Dateien-Bestand wie 1.50.496; nur `pferde-template-kit.php` geändert -> PASS.
- ZIP-Stamm `affiliate-portal-template-kit/` -> PASS.
- ZIP-Lesetest -> PASS.
- Version `1.50.497` -> PASS.

Marker: `JOURNAL_150497_FULL_WRAPPER_GAP_BROWSER_POS_NEG_PASS`.

## Core 1.3.0 – Automation

Core 1.3.0 bleibt unverändert. Die reale WordPress-Sandboxprüfung unter `Glossar -> Automation -> Sandbox hart testen` ist weiterhin offen.

## Harte Grenze

**1.50.497 ist lokal mit Browser-Geometrie geprüft, aber noch kein LIVE PASS.** Erst Installation + Nutzerreadback schließen den Journal-Abstand und die Kickerzeile.

## Nächster realer Schritt

1. Design `1.50.497` über 1.50.496 installieren.
2. `/journal/` prüfen: sichtbarer Breadcrumb→Hero-Abstand muss dem Glossar entsprechen; Kicker `WISSEN & INSPIRATION`; Claim `Mehr wissen – besser verstehen`.
3. Glossar nur als Regression ansehen; dort nichts verändern.
4. Danach `Glossar -> Automation -> Sandbox hart testen`.
