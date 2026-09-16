# BILD – PROTOKOLL 2026-09-16

## Tatsächlich ausgeführte Arbeit

- Wasserzeichenkonzept als separaten Backlog `TODO-BILD-WASSERZEICHEN-001` im BILD-Büro abgelegt.
- Verbindlichen Zielvertrag für Pferderassen-Hero angelegt.
- Bildzentrale 2.6.9 auf 2.7.0 erweitert: generischer Custom-Post-Type-Hero-Weg, kein `pa_breed`-Hardcoding im allgemeinen Kern.
- Pferde-Atelier-Zielnutzung: `pa_breed`.
- neues Hero-Profil: 3:1 / 1200×400 / WebP.
- Featured-Image-Readback + Dateiformatprüfung + Rollback auf vorheriges Featured Image eingebaut.
- bestehende Artikel-/Kategorie-/HivePress-Wege als Regression geprüft.
- Pferde-Design 1.50.536 statisch geprüft: Featured Image wird vor dem Standard-Rassenbild gelesen; daher aktuell kein Designpatch erforderlich.
- 2.7.0-Release persistent in der allgemeinen Bildzentrale abgelegt und PPA-003 als isolierte Ausgabekopie synchronisiert.

## Prüfungen 2.7.0

- finaler ZIP-Lesetest: PASS.
- Version 2.7.0 aus finaler ZIP: PASS.
- SHA-256 final: `8403bf1ad06be7c6102c37c53648826663fdcbebbe73d27e011364fab51dc5e4`.
- PHP-Lint aus finaler ZIP: PASS.
- damaliger Positiv-/Negativ-/Regressionstest: 28/28 PASS.
- persistenter Readback `ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/CURRENT.zip`: Version/Hash PASS.
- persistenter Readback `PPA-003/CURRENT.zip`: Version/Hash PASS.

Wichtig: Dieser 28er-Test deckte den realen Admin-Klickweg des neu hinzugefügten `Post-Type-Hero`-Tabs nicht ab. Das wurde erst durch den WordPress-LIVE-Test sichtbar.

## Fehler / Korrektur

### BILD-DOC-20260916-001 – CLOSED

Eine zwischenzeitliche Dokumentationsbehauptung lautete, die bisherige PPA-003-Ausgabekopie sei inkonsistent bzw. enthalte ein fremdes Plugin. Das war falsch.

Frischer Readback vor der 2.7.0-Synchronisierung ergab:
- Version 2.6.9;
- SHA-256 `748f77602bc3d4f64bd24a2f163c53829f0c1e8dc2102a82a642ceb4778e160e`;
- damit Übereinstimmung mit dem damaligen Manifest.

Die falsche Behauptung wurde verworfen. Sie ist keine aktuelle Wahrheit.

### BILD-LIVE-20260916-001 – 2.7.0 LIVE FAIL / 2.7.1 LOCAL FIX PASS

Realer WordPress-Befund des Nutzers:
- `Post-Type-Hero` sichtbar;
- per Klick nicht aktivierbar.

Frische Prüfung des exakten 2.7.0-Release-ZIPs bestätigte den Fehler im Quellcode:
- Button `data-pabz-target="cpt"` vorhanden;
- CPT-Panel wird gerendert;
- im JavaScript-Objekt `pabzTabPanels` waren nur `posts`, `wp`, `hp`, `admin` eingetragen;
- `cpt` fehlte;
- `activatePabzTab('cpt')` kehrte dadurch sofort über `if (!pabzTabPanels[key]) return;` zurück.

Minimalfix 2.7.1:
- `cpt: document.getElementById('pabz-panel-cpt')` ergänzt;
- Pluginheader und Einstellungs-Export auf 2.7.1 erhöht;
- keine weitere Funktionsänderung.

## Harte lokale Prüfung 2.7.1

Release:
`ALLGEMEINE_BILDZENTRALE_2.7.1_POST_TYPE_HERO_TAB_FIX_INSTALLIEREN.zip`

SHA-256:
`4453a39dfda7adc7a849428eca41c8ee0d2410a705011c7c254616a789ad0d21`

Ausgeführt:
- PHP-Lint Arbeitskopie: PASS;
- exakter Delta-/Whitelist-Test: PASS;
- außerhalb Versionsmarker + `cpt`-Mapping byte-identisch zu 2.7.0: PASS;
- Struktur-/Regressionstests: **21/21 PASS**;
- JavaScript-Tab-Runtime Positiv/Negativ: **12/12 PASS**;
- Negativkontrolle am originalen 2.7.0-Code reproduziert den realen CPT-Klickfehler: PASS;
- 2.7.1 CPT-Klick aktiviert exakt CPT-Button und CPT-Panel: PASS;
- alle fünf Haupttabs posts/wp/cpt/hp/admin klickbar: PASS;
- Query `?pabz_tab=cpt`: PASS;
- Hash `#pabz-cpt`: PASS;
- unbekannter Tab: fail-closed PASS;
- fehlendes CPT-Panel: fail-closed PASS;
- ZIP-Lesetest: PASS;
- Re-Extract: PASS;
- PHP-Lint aus Re-Extract: PASS;
- Version 2.7.1 im Re-Extract: PASS;
- Plugin-Stamm unverändert: PASS.

Der ursprüngliche ausführbare 28er-Runner ist in den aktuell auffindbaren Quellen nicht persistent vorhanden. Deshalb wurde **kein erneuter 28/28-Lauf behauptet**. Der zuvor 28/28 getestete Backend-/Workflowcode bleibt in 2.7.1 hart per exaktem Delta-Nachweis unverändert; die einzige funktionale Änderung ist das Admin-Tab-Mapping.

## Persistente Synchronisierung 2.7.1

- neues 2.7.1-Release in der allgemeinen Bildzentrale abgelegt;
- allgemeines `BILDZENTRALE/CURRENT.zip` auf 2.7.1 synchronisiert;
- PPA-003 `CURRENT.zip` auf 2.7.1 synchronisiert;
- beide CURRENT-ZIPs nach Persistierung erneut materialisiert;
- beide sind byte-identisch zum Release;
- SHA-256 bei allen drei Dateien: `4453a39dfda7adc7a849428eca41c8ee0d2410a705011c7c254616a789ad0d21`.

## WARUM / Entscheidungen

- Der neue Weg bleibt generisch statt `pa_breed`-spezifisch, damit MOD-002 allgemeingültig bleibt.
- Der 2.7.1-Fix ist absichtlich minimal: nur die fehlende UI-Bindung wird ergänzt. So bleiben die bereits geprüften Backend-Wege unverändert.
- Ab jetzt gehört der echte Tab-Klick einschließlich Positiv-/Negativkontrolle zur Regression des `post_type_hero`-Wegs; reine Backend-Konfigurationsprüfungen reichen für einen neuen Admin-Bereich nicht aus.
- Das Design wird nicht vorsorglich geändert, weil die vorhandene Featured-Image/Fallback-Logik den Bedarf bereits abdeckt; erst ein realer Gegenbeleg rechtfertigt einen Designpatch.
- Wasserzeichen werden nicht in den Hero-Release gemischt.

## LIVE-Grenze / nächste Abnahme

2.7.0 ist als LIVE-Kandidat verworfen.

2.7.1 ist erst LIVE PASS nach:
1. Installation über 2.7.0;
2. realem Öffnen des Tabs `Post-Type-Hero`;
3. Speicherung von `pa_breed`;
4. realer Hero-Erzeugung für mindestens eine Pferderasse;
5. Featured-Image-Readback;
6. Frontend-Positivprüfung;
7. Frontend-Negativprüfung des Standard-Fallbacks.
