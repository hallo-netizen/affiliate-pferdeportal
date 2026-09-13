# UNIVERSAL GLOSSAR ENGINE – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.6 TECHNISCHER KANDIDAT / FRESH + IN-PLACE HARDTEST PASS / LIVE-RELEASE OFFEN

## Belastbarer Stand

- Modulname: `MOD-008 – Universal Glossar Engine`.
- Ziel: ein einziger projektunabhängiger WordPress-Core für mehrere Portale.
- Erste Projektanwendung: Pferde Atelier.
- Pferde-spezifische Begriffe, Oberbereiche, Texte, URL-Basis und SEO-Schemata sind nicht im Core hart verdrahtet.
- Eigener WordPress-Backendbereich `Glossar`.
- Glossarbegriffe sind eigener Inhaltstyp, getrennt von normalen Beiträgen/Seiten.
- Oberbereiche sind eigene hierarchische Taxonomie, getrennt von normalen WordPress-Kategorien.
- Vorhandene WordPress-Seite kann als Glossar-Hauptseite gebunden werden.
- Eigene Zieladresse je veröffentlichtem Begriff.
- Eigene SEO-Titel-/Meta-Description-Werte; Core funktioniert ohne direkte Yoast-Datenbankwrites.
- Suche, A–Z, Oberbereiche, Karten/Aufklapper, JSON-Import/Export vorhanden.
- Kein Bildzwang; kein Auto-Publish; Import bleibt Entwurf.

## Aktueller technischer Kandidat

Version:
`0.2.6`

Rewrite-Schema:
`5`

Arbeitsbranch:
`hobbyroom/glossar-026-upgrade-hardtest-20260913`

0.2.6 wird deterministisch aus dem bereits getesteten 0.2.5-Kandidaten erzeugt.

Erlaubtes Delta exakt:
- `universal-glossary-engine.php`: Version 0.2.5 → 0.2.6;
- `includes/class-uge-core.php`: Rewrite-Schema 4 → 5.

Alle übrigen Plugin-Dateien bleiben bytegleich zum getesteten 0.2.5-Kandidaten.

## Autoritativer Hardtest

GitHub Actions Run:
`34748541630`

Commit des Runs:
`e5f8c8ce1839a69f3e6fb712bd4a3d4a3e8ad059`

Fresh-Install Job:
`103700782149` → PASS.

Bewiesen:
- WordPress + MySQL + Astra;
- Version 0.2.6;
- Rewrite-Schema 5 direkt nach Aktivierung;
- Policy-/Seed-Positiv-/Negativmatrix;
- alle gerenderten Kartenlinks;
- AJAX positiv und ungültiger Nonce negativ;
- A–Z, Preview, Draft-Sperre, Duplikatsperre;
- Kategorie-/Begriffskollisionen;
- normale WordPress-Beiträge unverändert;
- Einzelbegriffe benötigen echten Glossar-Artikelmarkup + H1, nicht nur HTTP 200;
- Hero-Abstand, responsive Hero-Darstellung und Breadcrumb-Achse.

In-place-Upgrade Job:
`103700782306` → PASS.

Negativer Vorzustand wurde real erzeugt:
- aktives 0.2.5;
- bekannte Einzelbegriffroute zunächst funktionsfähig;
- Einzelbegriff-Rewrite-Regel gezielt entfernt;
- danach bekannte URL = 404;
- gespeichertes Schema bleibt 4.

Echter WordPress-Updater:
- 0.2.5 wird über WordPress mit 0.2.6 überschrieben;
- installierte Dateien zeigen Version 0.2.6 und Schema 5;
- DB vor erstem neuen Request bleibt Schema 4;
- erster normaler Request migriert 4 → 5;
- Rewrite-Regel wird neu aufgebaut;
- Einzelbegriff danach 200 + echtes Artikelmarkup + erwarteter Inhalt.

Danach erneut PASS:
- alle Kartenlinks echte Glossarseiten;
- unbekannter Begriff 404;
- Entwurf 404;
- Legacy-URL 301;
- gleichnamige Kategorie/Begriff getrennt;
- ungültiger AJAX-Nonce negativ;
- normaler WordPress-Beitrag unverändert;
- Daten und Konfiguration erhalten;
- Deaktivieren/Reaktivieren ohne Routingverlust;
- komplette alte Frontend-/Regression-/Acceptance-Matrix erneut PASS.

## Gated Package

Der Paketjob durfte erst nach PASS von Fresh-Install UND In-place-Upgrade starten.

Job:
`103700913568` → PASS.

Inneres Plugin-ZIP:
`universal-glossary-engine-0.2.6.zip`

SHA-256:
`e0717db3aa247edc30b0fe84a261aa59037050d593e3432a6fb460f6d96f3b09`

Actions-Artefakt-ID:
`10314822840`

## Lokale Kontrolle des exakten erzeugten Artefakts

Das tatsächlich von Actions erzeugte Artefakt wurde heruntergeladen und lokal erneut positiv und negativ geprüft.

PASS:
- äußerer Artefakt-Hash stimmt;
- innerer Plugin-ZIP-Hash stimmt mit Workflow und `SHA256.txt`;
- ZIP-Struktur gültig, keine absoluten Pfade, kein `..`, keine Symlinks;
- lokaler 0.2.5↔0.2.6-Vergleich: exakt nur die zwei erlaubten Dateien geändert;
- 0.2.6 und Schema 5 vorhanden;
- alte deklarierte 0.2.5 / Schema 4 nicht vorhanden;
- feste Mobile-Höhe 240px nicht vorhanden;
- frühere globale Astra-/Entry-Content-Hacks nicht vorhanden;
- PHP-Lint aller 10 PHP-Dateien PASS.

Details:
`TESTPROTOKOLL_0.2.6_20260913.md`

## Dauerhafte Update-Regel

Keine materiell unterschiedlichen Pakete mehr unter derselben Pluginversion.

Rewrite-relevante Änderung → neue Pluginversion + neue Rewrite-Schema-Version + Fresh-/In-place-Hardtest + exakte ZIP-Hashbindung.

Quelle:
`ENTSCHEIDUNG_20260912.md`

## Modulklasse

Formal weiterhin:
`UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Der neutrale Core und eine fachfremde Zweitkonfiguration sind technisch belegt. Für formale Hochstufung bleibt ein separates zweites reales Portal offen.

## Noch offen

- Pferde-Atelier-Installation/Readback des exakt hashgebundenen 0.2.6-Kandidaten;
- reale Sicht-/Funktionsabnahme der vier aktuell gemeldeten Pferde-Frontendfehler;
- exakter Live-Rootcause-Nachweis der zuvor weißen Einzelbegriffseite ist nicht erbracht;
- echter Astra+Yoast-Kombinationstest für den aktuellen Kandidaten, soweit für Release erforderlich;
- realer Import aus der Campus-Wissensdatenbank;
- größerer Bestands-/Performance-Test;
- separates zweites reales Portal.

Kein Pferde-Atelier-LIVE-PASS und kein endgültiger allgemeiner Release-PASS vor den noch gebundenen Prüfungen.
