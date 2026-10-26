# HD-009 – GATE 4 – POSITIV/NEGATIV/REGRESSION – 2026-10-26

ROLLE: Evidence / Nachweis, keine Current-Autorität.

## Bindung

Arbeitsbranch:
`hobbyrausch/hd009-affiliate-port-20261026`

Geprüfter Quellstand:
`a1b482e4e1b70163ec48b32dc2bd5780eb5f72ec`

GitHub-Actions-Lauf:
`40319481655`

Job:
`121560434781`

Ergebnis:
**PASS**

## Ausgeführte Prüfungen

- PHP-Lint: **23/23 PASS**
- Positiv: gültiger HD-004-Snapshot mit 8 CORE-Welten, 320 strukturellen Hobbyseiten und 320 direkten Artikelkategorien → HD-009-Katalog → eBay + idealo: **PASS**
- Negativ: HD-004-Registry nicht bereit → fail-closed: **PASS**
- Negativ: leerer/ungültiger Snapshot → fail-closed: **PASS**
- Negativ: Weltzahl != 8 → fail-closed: **PASS**
- Negativ: < 300 strukturell belegte Hobbyseiten → fail-closed: **PASS**
- eBay propagiert Registry-Fehler fail-closed: **PASS**
- idealo propagiert Registry-Fehler fail-closed: **PASS**
- Regression: entfernte Pferdeatelier-Dateiquellen bleiben abwesend; verbleibende PHP/JS/CSS ohne geprüfte Fremdprojektmarker: **PASS**
- Amazon: Providerstatus bleibt `prepared`; kein aktiver HDAR-Amazon-Adapter im Bootstrap und kein erfundener Amazon-Adapter: **PASS**

## Fehlerkette innerhalb Gate 4

Erster Lauf `40319097524`:
- FAIL im PHP-Lint.
- Ursache: nach Entfernung des historischen Pferde-Recovery-Lookups blieben zwei verwaiste Zeilen `return $lookup; }` in der Hauptdatei.
- Fix-Commit: `a5fca469dda22d459dd65f040bb8cd872c697982`.

Zweiter Lauf `40319345523`:
- PHP-Lint 23/23 PASS.
- Positiv- und Negativpfade bis Fremdprojekt-Regression PASS.
- Regressionstest schlug auf `fohlen` innerhalb des neutralen Wortes `empfohlen` an.
- Ursache: Testregex zu breit, kein Quell-/Fachfehler.
- Testfix-Commit: `a1b482e4e1b70163ec48b32dc2bd5780eb5f72ec`.

Dritter Lauf `40319481655`:
- kompletter Gate-4-Lauf: **PASS**.

## Grenze

Dies ist ein lokaler/CI-Ausführungsnachweis der bereinigten Arbeitsquelle.
Es ist **kein WordPress-Live-PASS** und noch **kein Installations-/Release-PASS**.
Gate 5 (Paketierung, Fresh-Unpack, Versions-/Struktur-/SHA-Prüfung und isolierter CURRENT.zip-Sync) wurde noch nicht ausgeführt.
