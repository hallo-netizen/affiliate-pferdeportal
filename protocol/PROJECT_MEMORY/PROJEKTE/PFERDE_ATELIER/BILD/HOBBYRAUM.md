# BILD – HOBBYRAUM

STAND: 2026-09-16
STATUS: AKTIV

## GEBUNDENER AUFTRAG

Bildzentrale **2.7.1** – Pferderassen-Hero über den generischen Custom-Post-Type-Hero-Weg bis zum echten WordPress-LIVE-PASS führen.

## AKTUELLER ARBEITSSTAND

- letzter sicherer WordPress-LIVE-Stand: 2.6.9;
- 2.7.0 wurde real in WordPress geprüft und ist **LIVE FAIL / verworfen**: `Post-Type-Hero` sichtbar, aber nicht anklickbar;
- Root Cause: fehlendes `cpt`-Mapping im JavaScript-Register `pabzTabPanels`;
- 2.7.1 behebt ausschließlich dieses Mapping und die Versionsmarker;
- harte lokale Prüfung 2.7.1: 21/21 Struktur-/Regression + 12/12 Tab-Runtime Positiv/Negativ PASS;
- Negativkontrolle reproduziert den 2.7.0-Klickfehler;
- ZIP/Re-Extract/PHP-Lint/Version/SHA PASS;
- allgemeines `BILDZENTRALE/CURRENT.zip` und PPA-003 `CURRENT.zip` persistent auf 2.7.1 synchronisiert und byte-identisch zum Release gelesen;
- Pferde-Design 1.50.536 bleibt unverändert: Featured Image hat Vorrang, Standardbild ist Fallback;
- Wasserzeichen bleibt separater Backlog in `TODO.md`.

## NEXT ACTION

1. Bildzentrale 2.7.1 über 2.7.0 in WordPress installieren.
2. `Post-Type-Hero` real anklicken – Tab muss öffnen.
3. `pa_breed` speichern.
4. eine reale Pferderasse auswählen und Hero erzeugen/zuordnen.
5. WordPress-Featured-Image-Readback prüfen.
6. Frontend positiv prüfen: spezifisches Bild sichtbar, Standardbild weg.
7. Frontend negativ prüfen: Rasse ohne spezifisches Bild zeigt weiterhin Standard-Fallback.
8. erst nach diesem echten LIVE-PASS `CURRENT_STATE.md` auf LIVE 2.7.1 setzen.

## VERBINDLICHER ARBEITSWEG

Technische Hauptquelle:
`ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`

Release:
`ALLGEMEINE_BILDZENTRALE_2.7.1_POST_TYPE_HERO_TAB_FIX_INSTALLIEREN.zip`

SHA-256:
`4453a39dfda7adc7a849428eca41c8ee0d2410a705011c7c254616a789ad0d21`

Zielvertrag:
`ZIELVERTRAG_BILDZENTRALE_PFERDERASSEN_HERO_20260916.md`

Rückgabeweg:
LIVE-Prüfung → BILD-CURRENT nachziehen → Pluginmanifest bleibt hashgebundene Ausgabekopie; keine zweite Fachwahrheit.

## NICHT ANFASSEN

- 2.7.0 nicht erneut als Kandidat verwenden;
- Wasserzeichenlogik in diesem Release;
- bestehende Artikel-/Kategorie-/HivePress-Bildwege außerhalb notwendiger Regression;
- Pferde-Design, solange der reale LIVE-Test die vorhandene Fallback-Logik nicht widerlegt;
- Archiv/Tresor/Backup als Werkbank.
