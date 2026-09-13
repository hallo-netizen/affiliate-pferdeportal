# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.8 TECHNISCHER KANDIDAT HARDTEST PASS / PFERDE-LIVE-READBACK OFFEN

## Belastbarer aktueller Stand

- Büro `GLOSSAR` steuert das öffentliche Pferde-Atelier-Glossar.
- Fachwahrheit bleibt in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Vorhandene WordPress-Seite `Glossar` bleibt Hauptseite.
- Das bestehende Pferde-Designplugin bleibt unangetastet.
- `main` bleibt unangetastet.

## Historischer Live-Fail 0.2.7

Der reale Nutzer-Readback vom 2026-09-13 bleibt gültig:
- Abstand oberhalb Startseiten-Hero: PASS;
- Hero/Bild responsive: FAIL;
- AJAX-Suche sichtbare Darstellung: FAIL;
- Kategorieseiten: FAIL;
- Links auf Einzelbegriffe: FAIL.

0.2.7 bleibt deshalb **LIVE FAIL / BLOCKED / NICHT VERWENDEN**.
0.2.6 bleibt historische Zwischenversion / nicht verwenden.

## Neue technische Absicherung 0.2.8

Die falsche frühere Abnahme wurde ersetzt durch eine RED→GREEN-Kette, die die realen Fehler zuerst reproduziert und anschließend denselben Vertrag gegen den minimal reparierten Kandidaten prüft.

0.2.8 enthält gegenüber dem verworfenen 0.2.7 nur die notwendigen Reparaturen:
- AJAX-Treffercontainer korrekt an das Suchformular gebunden;
- Hero/Bild proportional responsiv statt fester 360px-Desktop-/Tabletlogik;
- Rewrite-Schema 5 → 6, damit beschädigte Schema-5-Zustände neu aufgebaut werden.

## Echter Design-Integrationsnachweis

Der finale Lauf verwendet den **echten Pferde-Designcode 1.50.469**, nicht den früheren Stub.

Exakter Design-Hauptcode SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`

## Finaler 0.2.8-Hardtest

Workflow:
`.github/workflows/glossar-028-final-hardtest.yml`

Run:
`34755984363`

Getesteter Head:
`d14f6bff7f660cc6461208e8153fbdf237f0d609`

Alle Jobs SUCCESS:
- Browser final `103720316319`
- Fresh final `103720316220`
- Update 0.2.6 → 0.2.8 `103720316226`
- Update 0.2.7 → 0.2.8 `103720316230`
- Real Design 1.50.469 final `103720316084`
- Gated package `103720510869`

Bewiesen sind u. a.:
- Browser-AJAX inkl. sichtbarer Position und realen Treffern;
- responsive Hero-Messung bei 1200 / 900 / 720 / 500 px;
- echte Kategorieansicht und negativer Ausschluss von Home-Hero/Home-Tools;
- echte Einzelbegriffseite mit Artikelmarkup und Inhalt;
- unbekannter Begriff 404;
- Draft 404;
- normaler WP-Beitrag unverändert;
- Kategorie/gleichnamiger Begriff getrennt;
- gezielt beschädigte Rewritezustände aus 0.2.6 und 0.2.7 werden beim echten Update auf Schema 6 repariert;
- echter Design-1.50.469-Runtime-Lauf PASS.

Vollständiges Protokoll:
`../../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.8_20260913.md`

## Exakter Übergabekandidat

Actions-Artefakt ID:
`10318015702`

Inneres installierbares ZIP:
`universal-glossary-engine-0.2.8.zip`

SHA-256:
`9bdda56baccfb4f7af5ff512fe37cb23d6117eb9cc56bb3e5f059b168b4f1db1`

Outer artifact digest:
`sha256:d404bd537f53bffb5a4a894c5ad4758ac5723524323638a6dd1e1b5fbb061b68`

Das exakt heruntergeladene Artefakt wurde lokal nochmals auf ZIP-Integrität, Hash, Version 0.2.8, Rewrite-Schema 6 und PHP-Lint geprüft.

## PASS-Grenze

**Technischer Kandidat 0.2.8: PASS.**

**Pferde-LIVE-PASS: noch NEIN.**

Erst nach Installation exakt dieses ZIPs und realem Nutzer-Readback dürfen die Live-Fehler in `FEHLERQUELLEN.md` geschlossen werden.

Die exakte historische Ursache der früheren weißen Live-Seite wird nicht rückwirkend behauptet; technisch reproduziert und abgesichert ist die Fehlerklasse inklusive der realen Vorgängerpfade 0.2.6 und 0.2.7.

## NEXT ACTION

Ausschließlich exakt `universal-glossary-engine-0.2.8.zip` mit SHA
`9bdda56baccfb4f7af5ff512fe37cb23d6117eb9cc56bb3e5f059b168b4f1db1`
über den normalen WordPress-Update/Überschreiben-Weg installieren.

Danach real prüfen:
1. oberer Startseitenabstand bleibt korrekt;
2. Hero/Bild responsive;
3. AJAX-Trefferliste sitzt direkt am Suchfeld und liefert reale Treffer;
4. Kategorieseite ist echte Kategorieansicht, nicht Startseite;
5. alle Einzelbegriff-Links zeigen echten Titel/Inhalt;
6. unbekannter Begriff 404;
7. Draft nicht öffentlich;
8. normaler WP-Beitrag unverändert;
9. Kategorie und gleichnamiger Begriff getrennt;
10. kein zweiter Breadcrumb / kein globaler Layoutshift.
