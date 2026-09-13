# UNIVERSAL GLOSSAR ENGINE – HOBBYRAUM

STAND: 2026-09-13
STATUS: 0.2.8 TECHNISCH PASS / PFERDE-LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der isolierte Arbeitsraum für den allgemeinen Glossar-Core.

**DU DARFST …**  
den neutralen Core und seine gebundenen Positiv-/Negativtests pflegen sowie den exakt geprüften 0.2.8-Kandidaten für den Pferde-Live-Readback verwenden.

**DU DARFST NICHT …**  
Pferde-Fachlogik in den Core schreiben, `main` verändern, unterschiedliche Paketbytes unter derselben Versionsnummer erzeugen, 0.2.6/0.2.7 erneut ausgeben oder vor realem Nachweis einen Pferde-LIVE-PASS behaupten.

**ALS NÄCHSTES …**  
exakt 0.2.8 auf Pferde Atelier über den normalen WordPress-Updateweg installieren und real zurücklesen.

## GEBUNDENER TECHNISCHER KANDIDAT

Version: `0.2.8`

Rewrite-Schema: `6`

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Getesteter Commit:
`d14f6bff7f660cc6461208e8153fbdf237f0d609`

Run:
`34755984363`

Jobs:
- Browser final `103720316319` PASS
- Fresh final `103720316220` PASS
- Update 0.2.6 → 0.2.8 `103720316226` PASS
- Update 0.2.7 → 0.2.8 `103720316230` PASS
- Real Design 1.50.469 `103720316084` PASS
- Gated Package `103720510869` PASS

Innerer ZIP-SHA-256:
`9bdda56baccfb4f7af5ff512fe37cb23d6117eb9cc56bb3e5f059b168b4f1db1`

Actions-Artefakt-ID:
`10318015702`

Testdetails:
`TESTPROTOKOLL_0.2.8_20260913.md`

## ECHTER DESIGN-RUNTIME-NACHWEIS

Der alte Stub ist kein Realnachweis mehr.

Der finale Integrationslauf rekonstruiert und aktiviert den exakten Pferde-Design-Hauptcode 1.50.469.

SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`

Danach laufen reale Browser-, Routing-, Positiv- und Negativprüfungen.

## VERSIONIERUNGSREGEL

0.2.6: historische Zwischenversion / nicht verwenden.

0.2.7: realer Pferde-LIVE-FAIL / nicht verwenden.

Aktueller Übergabekandidat ausschließlich 0.2.8.

Dauerhaft:
**Unterschiedliche Paketbytes = unterschiedliche Pluginversion.**

Jede materielle Änderung nach 0.2.8 benötigt Version 0.2.9 oder höher und erneut:
RED→GREEN + Fresh + beide realen Upgradepfade + echter Designruntime + Positiv/Negativ + gated package + lokaler exakter Artefaktcheck.

## TESTSTAND 0.2.8

PASS:
- Fresh WordPress/MySQL/Astra;
- Version 0.2.8 / Schema 6;
- Browser AJAX inkl. realer Treffer und Position;
- Browser Hero responsive 1200 / 900 / 720 / 500;
- echte Kategorieseite statt Home-Renderer;
- echte Einzelbegriffseite statt blankem/fremdem HTTP 200;
- unbekannter Begriff 404;
- Draft 404;
- Kategorie-/Begriffskollision getrennt;
- normale Beiträge unverändert;
- Update 0.2.6 → 0.2.8;
- Update 0.2.7 → 0.2.8;
- beide Updatepfade aus absichtlich zerstörtem Rewritezustand;
- Schema 6 repariert Rewritezustand;
- echtes Pferde-Design 1.50.469;
- gated Paketjob;
- exaktes heruntergeladenes ZIP lokal nochmals geprüft.

## NEXT ACTION

1. Keine weitere Codeänderung am 0.2.8-Kandidaten.
2. Exakt `universal-glossary-engine-0.2.8.zip` verwenden.
3. SHA-256 vor Übergabe/Installation bindend:
   `9bdda56baccfb4f7af5ff512fe37cb23d6117eb9cc56bb3e5f059b168b4f1db1`.
4. Pferde Atelier über normalen WordPress-Pluginupdateweg aktualisieren.
5. Real positiv prüfen: Topgap, Hero responsive, AJAX, Kategorie, Einzelbegriffe, Breadcrumb.
6. Real negativ prüfen: unbekannter Begriff, Draft, normale Beiträge, gleichnamige Kategorie/Begriff, kein Home-Renderer auf Kategorie, kein globaler Layoutshift.
7. Erst nach realem PASS Projektstatus und Fehlerquelle auf LIVE PASS setzen.
8. Bei FAIL: exakter erster Livefehler dokumentieren; nächste Produktversion mindestens 0.2.9.

## HARTE REGEL

**Technischer Kandidaten-PASS ist kein Pferde-Atelier-LIVE-PASS.**

`main` und bestehendes Designplugin bleiben unangetastet.
