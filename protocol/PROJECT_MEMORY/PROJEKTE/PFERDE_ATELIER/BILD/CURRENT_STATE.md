# BILD – CURRENT STATE

STAND: 2026-09-16
STATUS: **BILDZENTRALE 2.7.0 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## AUTORITÄT

Diese Datei ist die **einzige aktuelle Campus-Standzusammenfassung des BILD-Büros**.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- verbindliches Ziel → `ZIELVERTRAG_BILDZENTRALE_PFERDERASSEN_HERO_20260916.md`
- Wasserzeichen-Backlog → `TODO.md`
- technische allgemeine Hauptquelle → `ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/`
- Fehlerindex → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Historie/Altbelege → `MASTERDATEIEN_INVENTAR.md` und Archiv

## LETZTER SICHERER LIVE-STAND

WordPress LIVE bestätigt: **Bildzentrale 2.6.9**.

## AKTUELLER BELASTBARER RELEASE-KANDIDAT

**Bildzentrale 2.7.0 – Custom-Post-Type-Hero**

Release:
`ALLGEMEINE_BILDZENTRALE_2.7.0_CUSTOM_POST_TYPE_HERO_INSTALLIEREN.zip`

SHA-256:
`8403bf1ad06be7c6102c37c53648826663fdcbebbe73d27e011364fab51dc5e4`

Zweck:
- generischer Hero-Weg für öffentliche Custom Post Types mit Thumbnail-Support;
- Pferde Atelier nutzt ihn für `pa_breed`;
- Hero wird als Featured Image gesetzt;
- Ausgabe 3:1 / 1200×400 / WebP;
- Readback-/Formatfehler führen zum Rollback der vorherigen Featured-Image-Zuordnung.

## FRISCHECHECK 2026-09-16

- finale 2.7.0-ZIP frisch gelesen: SHA-256 PASS;
- Version 2.7.0 aus finaler ZIP: PASS;
- PHP-Lint aus finaler ZIP: PASS;
- gebundener Testreport: **28/28 Positiv-/Negativ-/Regressionstests PASS**;
- PPA-003 `CURRENT.zip` nach Synchronisierung frisch gelesen: Version 2.7.0 / SHA-256 PASS;
- allgemeine `BILDZENTRALE/CURRENT.zip` nach Synchronisierung frisch gelesen: Version 2.7.0 / SHA-256 PASS;
- Design 1.50.536: statischer Fallback-Abgleich PASS – vorhandenes Featured Image hat Vorrang vor dem Standard-Rassenbild; daher derzeit kein Designupdate erforderlich.

Dokumentationskorrektur:
Eine zwischenzeitliche Behauptung, die bisherige PPA-003-Ausgabekopie 2.6.9 sei inkonsistent bzw. ein fremdes Plugin gewesen, war falsch. Frischer Readback bestätigte vor der 2.7.0-Synchronisierung korrekt Version 2.6.9 und den damaligen SHA-256. Die falsche Behauptung ist verworfen und im korrigierten Testreport/Pluginprotokoll berichtigt.

## ERSTER OFFENER ACCEPTANCE-PUNKT

**WORDPRESS-LIVE-READBACK 2.7.0 ist offen.**

Noch erforderlich:
- 2.7.0 in WordPress installieren;
- `pa_breed` als Post-Type-Hero-Ziel speichern;
- mindestens eine reale Pferderasse bebildern;
- Featured-Image-Readback prüfen;
- Frontend positiv prüfen: spezifisches Hero ersetzt Standardbild;
- Frontend negativ prüfen: Rasse ohne spezifisches Bild behält Standard-Fallback.

## WASSERZEICHEN

Das allgemeine Wasserzeichen-/Mediathek-Konzept ist als separater Backlog in `TODO.md` erfasst und **nicht Teil von 2.7.0**.

## BESTEHENDER OFFENER ALTPUNKT

`BILD-OPEN-RATIO-001` bleibt unverändert ungeklärt: historischer Kategorie-Profil-Widerspruch 16:9 vs. gespeicherte 3:1-Ausgabe. Er ist nicht der Blocker des aktuellen Pferderassen-Hero-Releases.
