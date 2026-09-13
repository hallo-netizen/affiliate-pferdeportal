# GLOSSAR – HOBBYRAUM

STAND: 2026-09-13
STATUS: TECHNISCH PASS / LIVE-READBACK 0.2.8 OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**DU DARFST …**  
den exakt getesteten 0.2.8-Kandidaten für den realen Pferde-Readback verwenden und danach ausschließlich nach tatsächlichem Live-Ergebnis weiterarbeiten.

**DU DARFST NICHT …**  
`main` verändern, 0.2.6 oder 0.2.7 erneut ausgeben, ein materiell anderes Paket erneut 0.2.8 nennen, aus technischem CI-PASS einen Pferde-LIVE-PASS ableiten oder einen Live-Fehler ohne realen Nutzer-Readback schließen.

**ALS NÄCHSTES …**  
exakt das gated getestete 0.2.8-ZIP über den normalen WordPress-Update/Überschreiben-Weg installieren und die reale Frontend-Checkliste abarbeiten.

## ARBEITSORT

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

`main` bleibt unangetastet.

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

Autoritativer aktueller Stand:
`CURRENT_STATE.md`

Testprotokoll:
`../../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.8_20260913.md`

## HISTORIE

0.2.6: historische Zwischenversion / nicht verwenden.

0.2.7: **LIVE FAIL / BLOCKED / nicht verwenden.**

Die durch 0.2.7 sichtbar gewordenen Testlücken sind nicht mehr Teil der aktuellen Abnahme:
- echter Designcode statt Stub;
- echte Browsergeometrie statt CSS-Grep;
- sichtbare AJAX-Position statt nur JSON;
- Kategorie- und Einzelrenderer statt nur HTTP-Status;
- Updatepfade 0.2.6 und 0.2.7;
- gezielt zerstörter Rewritezustand als Negativfall.

## 0.2.8 TECHNISCHER KANDIDAT

Finaler Hardtest:
- Run `34755984363`
- Head `d14f6bff7f660cc6461208e8153fbdf237f0d609`
- Browser final `103720316319` SUCCESS
- Fresh final `103720316220` SUCCESS
- Update 0.2.6 → 0.2.8 `103720316226` SUCCESS
- Update 0.2.7 → 0.2.8 `103720316230` SUCCESS
- Real Design 1.50.469 `103720316084` SUCCESS
- Gated Package `103720510869` SUCCESS

Echter Design-Hauptcode:
SHA-256 `580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`.

## EXAKTE ÜBERGABE

Nur dieses Paket verwenden:
`universal-glossary-engine-0.2.8.zip`

SHA-256:
`9bdda56baccfb4f7af5ff512fe37cb23d6117eb9cc56bb3e5f059b168b4f1db1`

Actions-Artefakt:
ID `10318015702`

Outer artifact digest:
`sha256:d404bd537f53bffb5a4a894c5ad4758ac5723524323638a6dd1e1b5fbb061b68`

Regel:
Wenn sich Pluginbytes nochmals materiell ändern, ist **0.2.8 verbraucht**. Nächste Produktversion dann mindestens 0.2.9 und vollständige Hardtest-Kette erneut.

## REALER LIVE-READBACK

Nach Installation zwingend prüfen:

### Positiv
1. Abstand oberhalb Hero bleibt korrekt.
2. Hero/Bild reagiert auf Desktop/Tablet/Mobil real proportional.
3. AJAX-Suche liefert reale Treffer und Trefferbox sitzt direkt unter dem Suchfeld.
4. `/glossar/gesundheit/` ist echte Kategorieansicht mit Kategorie-Kopf/Begriffen und keine Startseitenkopie.
5. Alle getesteten Einzelbegriffe zeigen echte Glossarseite mit Titel und Inhalt.
6. Breadcrumb genau einmal und korrekt positioniert.

### Negativ
1. unbekannter Begriff → 404;
2. Draft nicht öffentlich;
3. normale WordPress-Beiträge unverändert;
4. gleichnamige Kategorie und gleichnamiger Begriff bleiben getrennt;
5. Kategorie enthält keinen Home-Hero und keine Home-Tools;
6. kein globaler Layoutshift außerhalb Glossar.

## ABSCHLUSSLOGIK

Bei realem PASS:
- betroffene Live-Fehler in `FEHLERQUELLEN.md` auf LIVE PASS/CLOSED setzen;
- `CURRENT_STATE.md` auf LIVE PASS aktualisieren;
- erst dann nächste Glossar-Integration starten.

Bei realem FAIL:
- exakten ersten Fehler in `FEHLERQUELLEN.md` dokumentieren;
- 0.2.8 live BLOCKED lassen;
- minimalen Fix bauen;
- **neue Version 0.2.9+**;
- RED→GREEN, Fresh, beide Updatepfade, echter Designruntime, Positiv/Negativ und gated package vollständig erneut.
