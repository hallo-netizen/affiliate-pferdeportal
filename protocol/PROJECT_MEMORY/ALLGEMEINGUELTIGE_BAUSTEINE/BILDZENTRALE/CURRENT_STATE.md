# BILDZENTRALE – CURRENT STATE

STAND: 2026-09-16
STATUS: **2.7.1 LOCAL HARD PASS / WORDPRESS-LIVE RETEST OFFEN**

## Aktueller technischer Release-Kandidat

Plugin:
`ALLGEMEINE_BILDZENTRALE_2.7.1_POST_TYPE_HERO_TAB_FIX_INSTALLIEREN.zip`

Version:
**2.7.1**

SHA-256:
`4453a39dfda7adc7a849428eca41c8ee0d2410a705011c7c254616a789ad0d21`

Ausgang:
2.7.0 / SHA-256 `8403bf1ad06be7c6102c37c53648826663fdcbebbe73d27e011364fab51dc5e4`

## Realer Fehler 2.7.0

WordPress-LIVE-Test zeigte: `Post-Type-Hero` war sichtbar, aber per Klick nicht aktivierbar.

Root Cause:
- Button `data-pabz-target="cpt"` vorhanden;
- CPT-Panel vorhanden;
- `cpt` fehlte im JavaScript-Register `pabzTabPanels`;
- dadurch brach `activatePabzTab('cpt')` fail-closed sofort ab.

2.7.0 ist deshalb kein aktiver Release-Kandidat mehr.

## Änderung 2.7.1

Minimalfix:
- `cpt: document.getElementById('pabz-panel-cpt')` im Tab-Register ergänzt;
- Versionsmarker auf 2.7.1 erhöht;
- sonst keine Backend-/Profil-/Prompt-/Import-/Readback-/Rollback-Änderung.

Der generische `post_type_hero`-Weg selbst bleibt unverändert:
- öffentliche Custom Post Types mit Thumbnail-Support;
- Ziel-Post-Type konfigurierbar, kein `pa_breed`-Hardcoding im allgemeinen Kern;
- 3:1 / 1200×400 / WebP;
- lokaler Medienimport;
- Featured-Image-Zuordnung;
- Readback und Dateiformatprüfung;
- Rollback auf vorheriges Featured Image bei fehlgeschlagenem Readback/Formatcheck.

## Harte lokale Prüfung

- PHP-Lint Arbeitskopie: PASS;
- exakter Delta-/Whitelist-Test: PASS;
- 21/21 Struktur-/Regressionstests: PASS;
- 12/12 Tab-Runtime Positiv/Negativ: PASS;
- Negativkontrolle reproduziert den 2.7.0-Klickfehler: PASS;
- 2.7.1 `cpt`-Klick aktiviert exakt Button + Panel: PASS;
- alle fünf Haupttabs klickbar: PASS;
- Query-/Hash-Direktaufruf für `cpt`: PASS;
- unbekannter Tab / fehlendes Panel: fail-closed PASS;
- ZIP-Lesetest / Re-Extract / PHP-Lint aus Re-Extract / Version: PASS;
- persistente allgemeine `BILDZENTRALE/CURRENT.zip`: Readback byte-identisch / SHA PASS;
- persistente PPA-003-Ausgabekopie: Readback byte-identisch / SHA PASS.

Der dokumentierte 2.7.0-Testharness belegt 28/28 Backend-/Workflowtests. Sein ausführbarer Runner ist in den aktuell auffindbaren Quellen nicht persistent vorhanden und wurde nicht erfunden oder als erneut ausgeführt behauptet. Der 2.7.1-Backendcode ist gegenüber dem getesteten 2.7.0-Release außerhalb der Versionsmarker byte-identisch; die einzige funktionale Änderung ist das Admin-Tab-Mapping.

## LIVE-Grenze

Kein WordPress-LIVE-PASS aus lokalen Tests.

Pferde-Atelier-LIVE-Abnahme liegt im Projektbüro:
`../../../PROJEKTE/PFERDE_ATELIER/BILD/CURRENT_STATE.md`

Erster Retest-Punkt: 2.7.1 installieren und `Post-Type-Hero` real anklicken.

## Wasserzeichen

Nicht Bestandteil 2.7.1. Das Konzept bleibt separater Pferde-BILD-Backlog und wird erst mit eigener Ziel-/Rollback-/Idempotenzprüfung umgesetzt.

## Historie / Altbelege

2.7.0 bleibt als Fehler-/Vorversionsbeleg erhalten, ist aber kein aktueller Kandidat. Weitere Historie siehe `MASTERDATEIEN_INVENTAR.md` und Projekt-BILD-Masterinventar.
