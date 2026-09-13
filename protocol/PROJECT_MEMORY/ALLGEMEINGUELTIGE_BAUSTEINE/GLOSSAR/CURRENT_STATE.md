# UNIVERSAL GLOSSAR ENGINE – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.8 TECHNISCHER KANDIDAT HARDTEST PASS / PFERDE-LIVE-READBACK OFFEN

## Belastbarer Stand

- Modul: `MOD-008 – Universal Glossar Engine`.
- Neutraler wiederverwendbarer WordPress-Core; Pferde Atelier ist erste Projektanwendung.
- Eigener Glossar-Inhaltstyp und eigene hierarchische Oberbereiche.
- Vorhandene Seite kann als Glossar-Hauptseite gebunden werden.
- Eigene Zieladresse je veröffentlichtem Begriff.
- Suche, A–Z, Oberbereiche, Karten/Aufklapper, SEO-Felder und JSON-Import/Export vorhanden.
- Kein Bildzwang, kein Auto-Publish; Import bleibt Entwurf.

## Korrektur des früheren 0.2.7-PASS

0.2.7 wurde durch realen Pferde-Readback widerlegt und bleibt **LIVE FAIL / BLOCKED / NICHT VERWENDEN**.

Die frühere Testkette hatte relevante Lücken: Design-Stub statt echtem Designplugin, CSS-Grep statt Browsergeometrie, AJAX-JSON statt sichtbarer UI und fehlender realer Upgradepfad 0.2.6 → 0.2.7.

0.2.6 bleibt historische Zwischenversion / nicht verwenden.

## Aktueller technischer Kandidat

Version:
`0.2.8`

Rewrite-Schema:
`6`

Branch:
`hobbyroom/glossar-livefail-red-green-20260913`

Getesteter Commit:
`d14f6bff7f660cc6461208e8153fbdf237f0d609`

Autoritativer finaler Run:
`34755984363`

Jobs – alle PASS:
- Browser final `103720316319`
- Fresh final `103720316220`
- Update 0.2.6 → 0.2.8 `103720316226`
- Update 0.2.7 → 0.2.8 `103720316230`
- echter Design-1.50.469-Runtime `103720316084`
- gated package `103720510869`

Inneres Plugin-ZIP:
`universal-glossary-engine-0.2.8.zip`

SHA-256:
`9bdda56baccfb4f7af5ff512fe37cb23d6117eb9cc56bb3e5f059b168b4f1db1`

Actions-Artefakt-ID:
`10318015702`

Äußerer Actions-Artefakt-Hash:
`d404bd537f53bffb5a4a894c5ad4758ac5723524323638a6dd1e1b5fbb061b68`

Details:
`TESTPROTOKOLL_0.2.8_20260913.md`

## Echter Designnachweis

Der aktuelle Integrations-PASS verwendet den echten Pferde-Design-Hauptcode 1.50.469, nicht den früheren Stub.

SHA-256 des ausgeführten Hauptcodes:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`

Die Runtime rekonstruiert diesen Code deterministisch und bricht bei abweichendem SHA ab.

## Hart bewiesen

- Fresh WordPress + MySQL + Astra;
- Version 0.2.8 / Schema 6;
- reale Browsermessungen 1200 / 900 / 720 / 500 px;
- Hero proportional responsiv;
- AJAX reale Treffer + sichtbare korrekte Position;
- echte Kategorieseite und negativer Ausschluss der Home-Marker;
- echte Einzelbegriffseite mit Artikelmarkup/H1/Inhalt;
- unbekannter Begriff 404;
- Draft nicht öffentlich;
- A–Z, Preview, Duplicate Guard und bestehende Regressionen;
- Kategorie/gleichnamiger Begriff getrennt;
- normale WordPress-Beiträge unverändert;
- echte WordPress-Updates aus 0.2.6 und 0.2.7;
- beide Updatepfade zusätzlich aus gezielt beschädigtem Schema-5-Rewritezustand;
- Schema 6 baut den Zustand neu auf;
- echter Design-1.50.469-Runtime-Lauf;
- gated package erst nach allen grünen Gates;
- exakt heruntergeladenes ZIP lokal erneut Hash-/Struktur-/Version-/Schema-/PHP-Lint-geprüft.

## Modulklasse

Formal weiterhin:
`UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Für formale Hochstufung fehlt weiterhin ein separates zweites reales Portal.

## Noch offen

- Pferde-Atelier-Installation/Readback des exakt hashgebundenen 0.2.8-Kandidaten;
- erst danach reale Schließung der in Pferde beobachteten Frontendfehler;
- aktueller Astra+Yoast-Kombinationstest, soweit für endgültigen Release erforderlich;
- realer Campus-Wissensdatenbankimport;
- größerer Bestands-/Performance-Test;
- separates zweites reales Portal.

## Dauerregeln

**Unterschiedliche Paketbytes = unterschiedliche Pluginversion.**

Jede materielle Produktänderung nach dem geprüften 0.2.8-Stand benötigt mindestens Version 0.2.9 und die vollständige Hardtest-Kette erneut.

**Technischer Kandidaten-PASS ist kein Pferde-Atelier-LIVE-PASS.**
