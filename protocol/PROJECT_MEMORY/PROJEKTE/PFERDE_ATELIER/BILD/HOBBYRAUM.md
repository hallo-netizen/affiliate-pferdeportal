# BILD – HOBBYRAUM

STAND: 2026-09-16
STATUS: AKTIV

## GEBUNDENER AUFTRAG

Bildzentrale 2.7.0 – **Pferderassen-Hero über generischen Custom-Post-Type-Hero-Weg** bis zum echten WordPress-LIVE-PASS führen.

## AKTUELLER ARBEITSSTAND

- 2.7.0 gebaut.
- LOCAL HARD PASS: 28/28 Positiv-/Negativ-/Regressionstests.
- finale ZIP/Version/SHA-256/PHP-Lint frisch PASS.
- allgemeines Bildzentrale-Artefakt und isolierte PPA-003-Ausgabekopie auf 2.7.0 synchronisiert und frisch gelesen.
- Pferde-Design 1.50.536 benötigt nach statischem Codeabgleich derzeit **keinen Patch**: Featured Image hat Vorrang, Standardbild ist Fallback.
- Wasserzeichen bleibt separater Backlog in `TODO.md` und wird nicht in diesen Release gemischt.

## NEXT ACTION

1. Bildzentrale 2.7.0 in WordPress installieren.
2. im Post-Type-Hero-Profil `pa_breed` speichern.
3. eine reale Pferderasse auswählen und Hero erzeugen/zuordnen.
4. WordPress-Featured-Image-Readback prüfen.
5. Frontend positiv prüfen: spezifisches Bild sichtbar, Standardbild weg.
6. Frontend negativ prüfen: Rasse ohne spezifisches Bild zeigt weiterhin Standard-Fallback.
7. erst nach diesem echten LIVE-PASS `CURRENT_STATE.md` auf LIVE 2.7.0 setzen.

## VERBINDLICHER ARBEITSWEG

Technische Hauptquelle:
`ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`

Release:
`ALLGEMEINE_BILDZENTRALE_2.7.0_CUSTOM_POST_TYPE_HERO_INSTALLIEREN.zip`

SHA-256:
`8403bf1ad06be7c6102c37c53648826663fdcbebbe73d27e011364fab51dc5e4`

Zielvertrag:
`ZIELVERTRAG_BILDZENTRALE_PFERDERASSEN_HERO_20260916.md`

Rückgabeweg:
LIVE-Prüfung → BILD-CURRENT nachziehen → Pluginmanifest bleibt hashgebundene Ausgabekopie; keine zweite Fachwahrheit.

## NICHT ANFASSEN

- Wasserzeichenlogik in diesem Release;
- bestehende Artikel-/Kategorie-/HivePress-Bildwege außerhalb notwendiger Regression;
- Pferde-Design, solange der reale LIVE-Test die vorhandene Fallback-Logik nicht widerlegt;
- Archiv/Tresor/Backup als Werkbank.
