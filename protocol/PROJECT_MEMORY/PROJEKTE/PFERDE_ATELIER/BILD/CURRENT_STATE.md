# BILD – CURRENT STATE

STAND: 2026-09-16
STATUS: **BILDZENTRALE 2.7.1 LOCAL HARD PASS / WORDPRESS-LIVE RETEST OFFEN**

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

## REALER LIVE-BEFUND 2.7.0

**2.7.0 ist als LIVE-Kandidat verworfen / FAIL.**

Realer WordPress-Test 2026-09-16:
- Tab `Post-Type-Hero` ist sichtbar;
- Klick aktiviert den Tab nicht;
- dadurch kann `pa_breed` im vorgesehenen Bedienweg nicht ausgewählt/gespeichert werden;
- die nachfolgenden Rassen-Hero-Schritte können nicht belastbar beginnen.

Root Cause frisch am echten 2.7.0-Release nachgewiesen:
- Button `data-pabz-target="cpt"` vorhanden;
- CPT-Panel vorhanden;
- im JavaScript-Register `pabzTabPanels` fehlte `cpt: document.getElementById('pabz-panel-cpt')`;
- `activatePabzTab('cpt')` brach deshalb fail-closed sofort ab.

Fehler-ID: `BILD-LIVE-20260916-001`.

## AKTUELLER BELASTBARER RELEASE-KANDIDAT

**Bildzentrale 2.7.1 – Post-Type-Hero-Tab-Fix**

Release:
`ALLGEMEINE_BILDZENTRALE_2.7.1_POST_TYPE_HERO_TAB_FIX_INSTALLIEREN.zip`

SHA-256:
`4453a39dfda7adc7a849428eca41c8ee0d2410a705011c7c254616a789ad0d21`

Minimalfix gegenüber 2.7.0:
- fehlendes `cpt`-Mapping im Tab-Register ergänzt;
- Versionsmarker 2.7.0 → 2.7.1;
- keine weitere Backend-/Profil-/Prompt-/Import-/Readback-/Rollback-Änderung.

## HARTE LOKALE PRÜFUNG 2.7.1

- PHP-Lint Arbeitskopie: PASS;
- exakter Delta-/Whitelist-Test: PASS – außerhalb Versionsmarker + `cpt`-Tab-Mapping byte-identisch zu 2.7.0;
- Struktur-/Regressionstests: **21/21 PASS**;
- Tab-Runtime Positiv/Negativ: **12/12 PASS**;
- Negativkontrolle mit originalem 2.7.0 reproduziert exakt den Klickfehler: PASS;
- `Post-Type-Hero`-Klick in 2.7.1 aktiviert exakt CPT-Button + CPT-Panel: PASS;
- alle fünf Haupttabs posts/wp/cpt/hp/admin klickbar: PASS;
- Query `?pabz_tab=cpt` und Hash `#pabz-cpt`: PASS;
- unbekannter Tab und fehlendes CPT-Panel bleiben fail-closed: PASS;
- ZIP-Lesetest / Re-Extract / PHP-Lint aus Re-Extract / Version 2.7.1: PASS;
- allgemeines `BILDZENTRALE/CURRENT.zip`, PPA-003 `CURRENT.zip` und Release nach persistentem Readback byte-identisch: PASS;
- persistenter SHA-256 überall: `4453a39dfda7adc7a849428eca41c8ee0d2410a705011c7c254616a789ad0d21`.

Der ursprüngliche 2.7.0-Testreport belegt 28/28 Backend-/Workflowtests. Der dazugehörige ausführbare Runner ist in den aktuell auffindbaren Quellen nicht persistent vorhanden; deshalb wird **kein erneuter 28/28-Lauf behauptet**. Stattdessen ist hart nachgewiesen, dass der Backend-Code von 2.7.1 gegenüber genau diesem getesteten 2.7.0-Release byte-identisch geblieben ist; die einzige funktionale Änderung liegt im Admin-Tab-Mapping.

## ERSTER OFFENER ACCEPTANCE-PUNKT

**WORDPRESS-LIVE-RETEST 2.7.1 ist offen.**

Noch erforderlich:
1. 2.7.1 über 2.7.0 in WordPress installieren;
2. `Post-Type-Hero` anklicken – der Tab muss real öffnen;
3. `pa_breed` als Post-Type-Hero-Ziel speichern;
4. mindestens eine reale Pferderasse bebildern;
5. Featured-Image-Readback prüfen;
6. Frontend positiv prüfen: spezifisches Hero ersetzt Standardbild;
7. Frontend negativ prüfen: Rasse ohne spezifisches Bild behält Standard-Fallback.

## WASSERZEICHEN

Das allgemeine Wasserzeichen-/Mediathek-Konzept ist als separater Backlog in `TODO.md` erfasst und **nicht Teil von 2.7.1**.

## BESTEHENDER OFFENER ALTPUNKT

`BILD-OPEN-RATIO-001` bleibt unverändert ungeklärt: historischer Kategorie-Profil-Widerspruch 16:9 vs. gespeicherte 3:1-Ausgabe. Er ist nicht der Blocker des aktuellen Pferderassen-Hero-Releases.
