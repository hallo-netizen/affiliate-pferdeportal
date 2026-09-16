# STARTMASTER0107 — System 4 Acceptance Hardening Closeout — 2026-09-16

## Status dieser Datei

Diese Datei ist **Protokoll / WAS-WARUM-Nachweis**. Sie ist **keine CURRENT-Wahrheit**, kein zweiter Zielvertrag und keine zweite Fehlerliste.

Die einzige autoritative aktuelle Zustandsquelle bleibt:

`control/startmaster0107/CURRENT_STATE.json`

Der zentrale Startmaster-Zeiger bleibt nur Navigation:

`control/CURRENT_STARTMASTER.json`

## Arbeitsbereich

- System: Campus → Pferde Atelier → Texterstellung → System 4
- Acceptance-Branch: `hobbyroom/system4-chat-output-acceptance-v1`
- frisch geprüfter Referenz-Head vor Abschlussnachholung: `392c07b1c9ad209c7efa2447366ba2b658d798c4`
- letzter vollständig abgeschlossener Acceptance-Run auf diesem Stand: `34990776210`
- Job: `104454536915`
- Ergebnis: **FAIL**
- Produktions-Parallelbranch frisch geprüft und nicht verändert: `hobbyroom/system4-parent-start-token-clean-v1` @ `a9cb5e3a7500cf4ba5e4551591ffd79cae57e36e`

## Verbindlicher erlaubter Testweg

Ausschließlich:

`Parent/Chat → Point-0 → Root → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → vollständige Textmaschine → Repair → Batch → Handoff → Datei`

Für die Acceptance gilt zusätzlich:

- nur `start-point0` als Einstieg;
- direkter Controller-Einstieg ohne Point-0/Root/Supervisor ist BLOCKED;
- `root_entry start` und `start-stdin` sind BLOCKED;
- im Test **kein Codex**; nur der gebundene Testworker;
- kein vorbereiteter Artikeltext, kein Recovery-/Fixture-Artikel als End-to-End-Artikel;
- Controller bestimmt den nächsten Schritt;
- kein Checker darf ersetzt oder übersprungen werden;
- reparierbare Fehler müssen an den zuständigen Owner zurückgegeben und dort weitergeführt werden;
- Integritäts-/Sicherheits-/technische nicht reparierbare Fehler dürfen terminal blockieren;
- GitHub-Artefakt, interner Temp-Pfad oder Hash allein sind kein terminaler Gesamt-PASS; die exakte Enddatei muss im Parent-Chat tatsächlich verfügbar sein.

## In diesem Arbeitschat tatsächlich umgesetzte Härtungen

### 1. SAME_ARTICLE_BODY-Repair für PPM-Sprachblocker

Der bestehende Repair-Pfad wurde so ergänzt, dass ein vom PPM als reparierbar klassifizierter Sprachbefund nicht terminal endet, sondern im selben kanonischen Artikel in `SAME_ARTICLE_BODY_REPAIR` weitergeführt werden kann.

**WARUM:** Frühere Läufe stoppten nach korrekt erkanntem reparierbaren Fehler mangels deterministischem Rückweg.

### 2. LanguageTool-Reparatur unbekannter deutscher Komposita

Keine fachwortspezifische Ausnahme und kein PASS trotz LT-Fund. Der Repair darf nur orthografische Bindestrichvarianten desselben Begriffs ausprobieren. Übernommen wird ausschließlich eine Variante, die vom echten LanguageTool 6.8 nachweislich akzeptiert bzw. verbessert wird. Mehrteilige Bindestrichvarianten wurden in denselben Repair-Pfad aufgenommen.

**WARUM:** Der reale Befund `Starrdeichselanhänger` hatte keinen LT-Vorschlag. Eine source-bound Ausnahme wäre mit PPM 6.7.9 unvereinbar gewesen, weil dessen Sprachbeleg rohe LT-Funde nicht als automatischen PASS akzeptiert.

### 3. Handoff-Dateiname korrigiert

Der Acceptance-Workflow suchte nach erfolgreicher Erstellung noch den veralteten Namen `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json`, obwohl die reale Übergabe `SYSTEM4_WORDPRESS_HANDOFF_V1.json` erzeugt.

Der aktuelle Vertrag/Dateiname ist:

`SYSTEM4_WORDPRESS_HANDOFF_V1`

**WARUM:** Der alte Name erzeugte `CHAT_ARTIFACT_MISSING`, obwohl der Artikelweg selbst bereits erfolgreich war.

### 4. Frühere grüne Strecke als unzureichend erkannt

Run `34980172949` war in den damaligen Workflow-Schritten grün und lud das GitHub-Artefakt hoch. Er gilt trotzdem **nicht** als endgültiger System-4-Gesamt-PASS, weil die exakte Datei nicht als Parent-Chat-Datei übergeben war und die später verlangte Vollständigkeit der Textmaschinen-Detailregeln noch nicht hart bewiesen war.

**WARUM:** `intern vorhanden / GitHub-Artefakt vorhanden` ist nicht gleich `im Parent-Chat angekommen`.

### 5. Testworker an Point-0/Root/Supervisor/Worker-Dispatch gebunden

Der Testworker darf vor gültigem Dispatch weder den Arbeitszustand als Artikelarbeit konsumieren noch einen Draft erzeugen. Der Dispatch muss aus dem erlaubten Point-0→Root→Supervisor-Weg stammen.

**WARUM:** Frühere Tests konnten hinter der eigentlichen Eingangskette starten und dadurch reale Übergabefehler verdecken.

### 6. Codex aus dem Acceptance-Testweg entfernt

Die Teststrecke enthält keinen `codex_entry`-Aufruf als Ersatz-Gate. Ein Negativnachweis prüft dies. Der Testworker nutzt die gebundene Worker-Dispatch-Prüfung direkt.

**WARUM:** Für den Acceptance-Test ist Codex ausdrücklich verboten; der Testworker darf nur am bereits gebundenen Worker-Interface stehen.

### 7. Neuer Artikel pro End-to-End-Lauf maschinell erzwungen

Der E2E-Test bekommt einen aktuellen Run-Beleg und erzeugt den Artikeltext erst im laufenden Test. Bekannte alte/Recovery-/Fixture-Bodies sowie doppelte Body-Verwendung im selben Run werden blockiert. Die Draft-Erzeugung ist an den aktuellen Lauf gebunden.

**WARUM:** Statische „frische“ Testthemen werden nach einem Lauf selbst zur Altlast. Frühere Tests konnten alte Artikel wiederverwenden und dadurch Fehler mitschleppen.

### 8. Verbindlicher Repair-Continuation-Beleg

Für reparierbare Fehler ist ein maschinell prüfbarer Rückgabe-/Continuation-Beleg erforderlich. Er bindet mindestens Owner/Ziel, Fehleridentität bzw. Fehlerhash, Reparaturzyklus sowie `terminal=false` und `continuation_required=true`. Fehlender oder manipulierter Beleg ist Test-FAIL. Negative Prüfungen decken Body, Metadaten, Links/Context sowie Research/Facts ab.

**WARUM:** Ein wiederkehrender historischer Fehler war `Fehler erkannt → BLOCK`, obwohl der Fehler reparierbar und ein Owner vorhanden war.

### 9. Vollständige Textmaschine nicht mehr aus Sammel-PASS abgeleitet

Die exakt gebundene PPM 6.7.9 ist die Regelquelle. Ihre Hard-Rule-Registry weist **557 Regeln** aus; die Coverage-Matrix weist **557 Zuordnungen** aus. Die Abnahme darf nicht aus der Anzahl beliebiger Testdateien oder einem Wrapper-PASS abgeleitet werden.

Verbindliches Ziel der Acceptance-Prüfung:

`jede registrierte Regel → eigener positiver Originaltest PASS + eigener negativer Originaltest PASS`

`UNKNOWN / UNMAPPED / UNTESTED` ist FAIL.

### 10. Alle originalen PPM-6.7.9-Testdateien als Pflichtgate

Der Workflow führt die originalen `test-*.php` aus dem exakt SHA-gebundenen PPM-Paket aus. Kein Test darf still übersprungen oder durch einen System-4-Ersatzvalidator ersetzt werden.

Gebundenes Paket:

`control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`

SHA-256:

`acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

### 11. PPM-Originaltests voneinander isoliert

Jeder Originaltest wird in einer eigenen frischen bytegleichen Entpackung derselben signierten PPM 6.7.9 ausgeführt.

**WARUM:** Ein Negativtest darf keine absichtlich manipulierte Datei/Signatur/Baseline an einen späteren Test vererben. Damit ist Altlast zwischen Originaltests ausgeschlossen.

## Letzter tatsächlich ausgeführter Teststatus

Run `34990776210`, Job `104454536915`:

- Setup: PASS
- Checkout: PASS
- Syntax-/Chat-only-/Fixed-point-Negativpfade: PASS
- Unit-/Negativsuite inklusive Mandatory Dispatch und No-Codex: PASS
- explizite Repair-Return-Regression: PASS
- Audit der exakten PPM 6.7.9, internen Originaltests und Hard-Rule-Registry: PASS
- **alle originalen PPM-Tests in frischen Einzelkopien + Hard-Rule-Coverage-Mapping: FAIL**
- echter LanguageTool-6.8-/PPM-Produktionskorridor: wegen vorherigem FAIL nicht ausgeführt
- 1-/3-Artikel-Korridor: nicht ausgeführt
- finaler Chat→WordPress-Datei-E2E ohne Codex: nicht ausgeführt
- Chat-Dateiprüfung: nicht ausgeführt
- Upload: nicht ausgeführt

Damit gilt: **Tests OFFEN. Kein Gesamt-PASS.**

## Aktueller erster Blocker

In der vollständigen Original-PPM-Prüfung bleiben **13 originale PPM-6.7.9-Tests rot**, obwohl jeder Test bereits in einer frischen Paketkopie läuft.

Die Tests/Regeln dürfen **nicht** geändert, ausgeschlossen, abgeschwächt oder durch Ersatztests ersetzt werden.

Der erste erlaubte nächste Schritt ist ausschließlich:

1. den von diesen 13 Originaltests vorgesehenen originalen Runner-/Bootstrap-/Baseline-/Signatur-Kontext aus dem unveränderten PPM-Paket bestimmen;
2. nur diesen korrekten Original-Aufrufkontext im Acceptance-Runner herstellen;
3. dieselbe vollständige PPM-Prüfung erneut ausführen;
4. erst bei PASS dieses Gates die bereits vorhandenen nachfolgenden Stationen unverändert weiterlaufen lassen;
5. 557/557 Regeln müssen ihre positive und negative Originaltestbindung tatsächlich nachweisen;
6. terminaler Gesamt-PASS erst nach realer Übergabe der exakten Enddatei in den Parent-Chat.

## Nicht anfassen

- keine neue Architektur;
- keine neue Teststrecke;
- keine Alternativroute;
- keine Änderung/Lockerung der Textmaschine oder ihrer PPM-Regeln;
- keinen der 13 roten Originaltests entfernen/überspringen;
- keinen vorbereiteten Artikeltext verwenden;
- keinen Codex-Testlauf starten;
- Produktions-Parallelbranch `hobbyroom/system4-parent-start-token-clean-v1` nicht mit Acceptance-Status überschreiben;
- `publish_allowed=false` beibehalten.

## Plugin-Status

In diesem Arbeitschat wurde **kein Plugin entwickelt und kein Plugin aktualisiert**. PSERC 0.28.23 wurde nur unverändert als bestehender Importer/Prüfgegenstand verwendet.

Daher: `Plugins: NICHT BETROFFEN`.
