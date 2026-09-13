# GLOSSAR – HOBBYRAUM

STAND: 2026-09-13
STATUS: 0.2.8 LIVE FAIL / 0.2.9 TECHNISCH PASS / LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**DU DARFST …**  
den exakt getesteten 0.2.9-Kandidaten für den realen Pferde-Readback verwenden und danach nur anhand des tatsächlichen Live-Ergebnisses weiterarbeiten.

**DU DARFST NICHT …**  
`main` verändern, 0.2.6/0.2.7/0.2.8 erneut ausgeben, unterschiedliche Paketbytes unter derselben Versionsnummer erzeugen, die alte falsche Kategorie-Acceptance wiederverwenden oder aus CI einen Pferde-LIVE-PASS ableiten.

**ALS NÄCHSTES …**  
exakt das gated getestete 0.2.9-ZIP über WordPress installieren und real prüfen.

## ARBEITSORT

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

Autoritativer Stand:
`CURRENT_STATE.md`

## HISTORIE / VERBRAUCHTE VERSIONEN

- 0.2.6: historische Zwischenversion / nicht verwenden.
- 0.2.7: LIVE FAIL / nicht verwenden.
- 0.2.8: **LIVE FAIL / nicht verwenden.**

Realer 0.2.8-Readback:
1. Bild höher, aber nicht responsive;
2. Kategorien nicht dem Startseiten-Design angepasst;
3. Einzelartikel laufen ins Leere.

## VERBINDLICHE KORREKTUR

Der alte Kategorietest war falsch. Er verlangte `kein Hero / keine Tools` und prüfte damit das Gegenteil der Nutzeranforderung.

Ab 0.2.9 gilt hart:
- Kategorie hat echten Kategorieinhalt;
- **plus denselben vollständigen visuellen Glossar-Rahmen wie die Startseite**;
- Hero + Suche/A–Z + Icon-Navigation sind Pflicht;
- Hero-Kicker `WISSEN`;
- ein gerenderter Begriff-Link muss im Browser tatsächlich geklickt werden und auf die echte Einzelbegriffseite führen.

## 0.2.9 TECHNISCHER KANDIDAT

Finaler Run:
`34757795593`

Head:
`f2fa6f0c248acfa6978b5faec5daf42a40d0ba3b`

SUCCESS:
- Build `103725094481`
- Fresh + Regression + Null-Rewrite `103725094537`
- Update 0.2.8 → 0.2.9 + erneuter Null-Rewrite `103725094620`
- Real Design 1.50.469 + Browser + Null-Rewrite `103725094378`
- Gated Package `103725295224`

Real-Design Browser beweist:
- AJAX sichtbar und korrekt positioniert;
- echtes Bild responsive bei 1200/900/720/500;
- Kategorie-Vollrahmen vorhanden;
- tatsächlicher gerenderter Hufbein-Link wird angeklickt und liefert echtes `uge-single-wrap` + Inhalt;
- Negativfälle PASS.

## ROUTING-HARDLOCK GEGEN TOTE EINZELLINKS

0.2.9 verwendet Rewrite-Schema 7 und zusätzlich einen direkten Request-Binder für Glossar-Begriff und Glossar-Gruppe.

Der Test löscht **alle** gespeicherten Glossar-Rewrite-Regeln, obwohl Schema 7 bereits aktuell ist. Danach müssen die URLs weiter funktionieren. Dadurch hängt die Einzelroute nicht mehr allein davon ab, ob WordPress/Cache die gespeicherte Rewrite-Tabelle korrekt aktualisiert hat.

Native authentifizierte Draft-Preview bleibt ausdrücklich ausgenommen und ist Regression-PASS.

## EXAKTE ÜBERGABE

Nur dieses Paket:
`universal-glossary-engine-0.2.9.zip`

SHA-256:
`864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`

Actions-Artefakt-ID:
`10317444708`

Outer artifact digest:
`sha256:98513772d72fc65dc4d01520086b4c7e56e165cceeea1e31147a9d6cf830c6ff`

## REALER LIVE-READBACK

Positiv zwingend:
1. Hero-Bild wird beim Verkleinern real kleiner;
2. Kategorie `Gesundheit` hat Hero, Suche/A–Z, Icon-Navigation und eigenen Kategorieinhalt;
3. Begriffskarte anklicken → echte Einzelbegriffseite mit Titel/Inhalt;
4. AJAX funktioniert;
5. oberer Abstand bleibt korrekt.

Negativ zwingend:
1. unbekannter Begriff 404;
2. Draft nicht öffentlich;
3. normale Beiträge unverändert;
4. kein globaler Layoutshift;
5. Draft-Preview für eingeloggten Bearbeiter funktioniert.

Bei jedem realen FAIL: keine Schönrechnung, Fehlerquelle aktualisieren, Version 0.2.9 verbraucht; materielle Änderung benötigt 0.2.10+.
