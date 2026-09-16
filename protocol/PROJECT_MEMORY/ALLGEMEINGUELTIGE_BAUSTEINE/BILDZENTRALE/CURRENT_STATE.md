# BILDZENTRALE – CURRENT STATE

STAND: 2026-09-16
STATUS: **2.7.0 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Aktueller technischer Release-Kandidat

Plugin:
`ALLGEMEINE_BILDZENTRALE_2.7.0_CUSTOM_POST_TYPE_HERO_INSTALLIEREN.zip`

Version:
**2.7.0**

SHA-256:
`8403bf1ad06be7c6102c37c53648826663fdcbebbe73d27e011364fab51dc5e4`

Ausgang:
2.6.9 / SHA-256 `748f77602bc3d4f64bd24a2f163c53829f0c1e8dc2102a82a642ceb4778e160e`

## Änderung 2.7.0

- generischer `post_type_hero`-Weg für öffentliche Custom Post Types mit Thumbnail-Support;
- Ziel-Post-Type konfigurierbar, kein `pa_breed`-Hardcoding im allgemeinen Kern;
- 3:1 / 1200×400 / WebP;
- lokaler Medienimport;
- Featured-Image-Zuordnung;
- Readback und Dateiformatprüfung;
- Rollback auf vorheriges Featured Image bei fehlgeschlagenem Readback/Formatcheck;
- bestehende Artikel-, WordPress-Taxonomie- und HivePress-Wege bleiben im Regressionsscope.

## Frische Prüfung

- finale ZIP: lesbar PASS;
- Version 2.7.0: PASS;
- SHA-256: PASS;
- PHP-Lint: PASS;
- Testharness: 28/28 PASS;
- persistente `BILDZENTRALE/CURRENT.zip`: Readback Version/Hash PASS.

## LIVE-Grenze

Kein WordPress-LIVE-PASS aus lokalen Tests.

Pferde-Atelier-LIVE-Abnahme liegt im Projektbüro:
`../../../PROJEKTE/PFERDE_ATELIER/BILD/CURRENT_STATE.md`

## Wasserzeichen

Nicht Bestandteil 2.7.0. Das Konzept bleibt separater Pferde-BILD-Backlog und wird erst mit eigener Ziel-/Rollback-/Idempotenzprüfung umgesetzt.

## Historie / Altbelege

Siehe `MASTERDATEIEN_INVENTAR.md` und Projekt-BILD-Masterinventar. Historische Exporte mit Secrets sind keine Arbeitsquelle und werden nicht in CURRENT dupliziert.
