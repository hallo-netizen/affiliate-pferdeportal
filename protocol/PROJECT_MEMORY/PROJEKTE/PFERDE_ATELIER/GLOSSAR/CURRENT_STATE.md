# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-13
STATUS: 0.2.8 LIVE FAIL / 0.2.9 TECHNISCHER KANDIDAT HARDTEST PASS / LIVE-READBACK 0.2.9 OFFEN

## Belastbarer aktueller Stand

- Büro `GLOSSAR` steuert das öffentliche Pferde-Atelier-Glossar.
- Fachwahrheit bleibt in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Vorhandene WordPress-Seite `Glossar` bleibt Hauptseite.
- Das bestehende Pferde-Designplugin und `main` bleiben unangetastet.

## Reale Nutzerwahrheit 0.2.8

Der Nutzer-Readback 2026-09-13 widerlegt die technische 0.2.8-Abnahme:
- Hero/Bild: höher geworden, aber real weiterhin nicht responsive;
- Kategorien: weiterhin nicht wie die Glossar-Startseite gestaltet;
- Einzelartikel: Links laufen weiterhin ins Leere.

Damit ist **0.2.8 LIVE FAIL / BLOCKED / NICHT VERWENDEN**.
0.2.7 und 0.2.6 bleiben ebenfalls historische Fehl-/Zwischenstände und werden nicht mehr ausgegeben.

## Wesentliche Korrektur der Acceptance

Die frühere Kategorie-Acceptance war fachlich falsch: sie verlangte ausdrücklich, dass Kategorien **keinen** Hero und **keine** Tools enthalten. Das war das Gegenteil der Nutzer-Vorgabe.

Verbindlich ist jetzt:
- jede Glossar-Kategorie besitzt ihren eigenen Kategorieinhalt;
- zugleich verwendet sie den vollständigen visuellen Glossar-Rahmen der Startseite: Hero, Suche/A–Z, Icon-Navigation;
- Hero-Kicker lautet `WISSEN`;
- Begriffskarten müssen per echtem Browserklick auf eine echte Einzelbegriffseite führen.

## Technischer Kandidat 0.2.9

Version: `0.2.9`
Rewrite-Schema: `7`
Branch: `hobbyroom/glossar-livefail-red-green-20260913`

Finaler Workflow:
`.github/workflows/glossar-029-final-hardtest.yml`

Finaler Run:
`34757795593`

Getesteter Head:
`f2fa6f0c248acfa6978b5faec5daf42a40d0ba3b`

Alle Produkt-/Release-Gates SUCCESS:
- Build `103725094481`
- Fresh inkl. komplette alte Regression + zerstörter Rewritezustand `103725094537`
- Update vom real ausgegebenen 0.2.8-Stand → 0.2.9, anschließend Rewrite erneut zerstört `103725094620`
- echter Design-1.50.469-Runtime + Browser + Null-Rewrite `103725094378`
- gated Package `103725295224`

## Was jetzt härter bewiesen ist

### Hero
Der Browser misst das **echte `<img>`** bei 1200 / 900 / 720 / 500 px. Das Bild ist selbst der Größenanker: `width:100%`, `height:auto`, keine künstliche feste Bildhöhe und kein erzwungener 5:2-Container. Gemessene Bildgrößen unter echtem Design:
- 1096 × 438.39
- 796 × 318.39
- 664 × 265.59
- 444 × 177.59

Das entspricht dem echten Bildverhältnis 1400 × 560 und skaliert mit der Viewportbreite.

### Kategorien
`/glossar/gesundheit/` muss gleichzeitig enthalten:
- `.uge-category-head` + H1 `Gesundheit`;
- `.uge-hero`;
- `.uge-tools`;
- `.uge-topic-nav`;
- echten Link auf `/glossar/begriff/hufbein/`.

### Einzelbegriffe / tote Links
0.2.9 besitzt zusätzlich einen direkten Request-Binder. Selbst wenn **alle gespeicherten Glossar-Rewrite-Regeln entfernt werden und Schema 7 bereits als aktuell gespeichert ist**, müssen Kategorie- und Einzelbegriff-URLs weiter funktionieren.

Der Real-Design-Browsertest klickt den tatsächlich gerenderten Hufbein-Link auf der Kategorie und verlangt danach:
- Ziel-URL `/glossar/begriff/hufbein/`;
- genau ein `article.uge-single-wrap`;
- realen Sentinel-Inhalt.

### Regression / Negativ
- Draft öffentlich: 404;
- authentifizierte WordPress-Draft-Preview: PASS;
- unbekannter Begriff: 404;
- A–Z, Duplicate Guard, normale Beiträge: PASS;
- AJAX reale UI/Position: PASS.

## Exakter Übergabekandidat

Actions-Artefakt-ID: `10317444708`

Installierbares ZIP:
`universal-glossary-engine-0.2.9.zip`

SHA-256:
`864befa0d159577e418906e4de3052ad0127b7dbcdad80775ba7e8f734ed1173`

Outer Actions artifact digest:
`sha256:98513772d72fc65dc4d01520086b4c7e56e165cceeea1e31147a9d6cf830c6ff`

Das heruntergeladene Artefakt wurde lokal erneut auf ZIP-Integrität, Version 0.2.9, Schema 7, direkten Request-Binder, Kategorie-Vollrahmen und Abwesenheit einer RC-Kennung geprüft.

## PASS-Grenze

**0.2.9 technischer Kandidat: PASS.**

**Pferde-LIVE-PASS 0.2.9: noch NEIN.**

Nur der reale Nutzer-Readback des exakt hashgebundenen 0.2.9-ZIPs kann die drei aktuellen Live-Fehler schließen.
