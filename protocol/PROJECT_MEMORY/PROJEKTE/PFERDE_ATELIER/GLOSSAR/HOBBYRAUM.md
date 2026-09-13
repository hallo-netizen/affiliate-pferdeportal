# GLOSSAR – HOBBYRAUM

STAND: 2026-09-13
STATUS: BLOCKED / LIVE FAIL / ROTER ACCEPTANCE-NEUBAU AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**DU DARFST …**  
die real beobachteten Fehler reproduzieren, die Testlücken schließen und danach ausschließlich minimal erforderliche Reparaturen prüfen.

**DU DARFST NICHT …**  
`main` verändern, ein neues ZIP ausgeben, einen PASS aus Quelltext-Greps ableiten, das Pferde-Design durch einen Stub als Realtest ausgeben oder einen Fehler ohne echten Positiv-/Negativnachweis schließen.

**ALS NÄCHSTES …**  
neue Acceptance-Kette zuerst auf dem fehlerhaften Stand ROT beweisen.

## AKTUELLER AUFTRAG

Kein Pluginbau für Übergabe.

Zuerst müssen die vier realen Fehler technisch so geprüft werden, dass der vorhandene fehlerhafte Stand zuverlässig durchfällt:
1. Hero/Bild Responsivität;
2. AJAX-Trefferposition;
3. echte Kategorieausgabe;
4. echte Einzelbegriffausgabe.

Der obere Startseitenabstand ist im realen Readback PASS und bleibt Regressionstest.

## ARBEITSORT

Branch:
`hobbyroom/glossar-027-release-hardtest-20260913`

`main` bleibt unangetastet.

Autoritative Fehlerquelle:
`FEHLERQUELLEN.md`

Aktueller Diagnosebeleg:
Run `34749713877`, Job `103703878642`.

## 0.2.7 STATUS

**BLOCKED / NICHT VERWENDEN.**

Der frühere Run `34749231699` ist als isolierter technischer Test historischer Beleg, aber keine gültige reale Abnahme mehr.

Grund:
Realer Pferde-Readback widerlegt vier behauptete Frontendpunkte und die Testkette hatte nachgewiesene Lücken.

## BEREITS HART REPRODUZIERT

- AJAX: Vorschlagsliste absolut positioniert, aber nicht am Suchfeld verankert → sichtbarer Overlayfehler.
- Responsive: Hero oberhalb 720px weiterhin feste 360px-/Absolute-Logik.
- Kategorie: sauberer Renderer ist von Startseite verschieden; live identische Startseite bedeutet falscher Routing-/Querypfad.
- Update: 0.2.6 → 0.2.7 behält Rewrite-Schema 5; beschädigter Schema-5-Zustand wird nicht neu aufgebaut.
- Einzelbegriff: nach diesem Fehlerpfad ist HTTP 200 möglich, obwohl `uge-single-wrap` fehlt.
- Kategorie: nach diesem Fehlerpfad ist HTTP 301 statt `.uge-category-head` reproduziert.

## VERBINDLICHE NEUE ACCEPTANCE-SCHRANKEN VOR JEDEM FIX

### A – echtes Design
Tatsächliches Pferde-Designplugin in den Integrationslauf. Kein selbstgebauter `Pferde_Template_Kit`-Stub als Realnachweis.

### B – Browser statt Stringsuche
Headless-Browserprüfung mindestens auf 1200 / 900 / 720 / 500 px.

Hero:
- reale Breite/Höhe aus DOM messen;
- Bild bleibt im Container;
- keine starre Desktop-/Tablet-Höhe als angebliche Responsivität durchgehen lassen.

AJAX:
- Suchbegriff real eintippen;
- Trefferliste muss unmittelbar unter Suchfeld liegen;
- horizontale Breite an Suchbereich gebunden;
- Treffer anklickbar;
- ungültiger/kein Treffer als Negativfall.

### C – Kategorie
Eine Glossar-Kategorie muss:
- `.uge-category-head` enthalten;
- eigenen Kategorienamen enthalten;
- passende Begriffskarten enthalten;
- **nicht** `.uge-hero` enthalten;
- **nicht** `.uge-tools` enthalten;
- nicht auf Startseite oder fremde Seite umleiten.

### D – Einzelbegriff
Jeder getestete Begriff muss:
- HTTP 200;
- `<article class="uge-single-wrap">`;
- genaues H1;
- erwarteten Sentinel-Inhalt;
- keine leere/weiße/fremde 200-Seite.

Negativ:
- unbekannter Begriff 404;
- Draft 404.

### E – Updatepfade
Vor Ausgabe muss der neue Kandidat real per WordPress-Updater mindestens von:
- 0.2.6 → neu;
- 0.2.7 → neu

getestet werden, jeweils auch aus einem gezielt beschädigten Rewritezustand.

Die nächste routingrelevante Reparatur benötigt ein neues Rewrite-Schema gegenüber Schema 5, damit ein alter beschädigter Zustand zwangsweise neu aufgebaut wird.

### F – Regression
- Startseitenabstand bleibt PASS;
- normale Beiträge/Seiten unverändert;
- kein globaler Layout-Hack;
- Kategorie/gleichnamiger Begriff bleiben getrennt;
- Legacy-Verhalten nur gemäß bestehendem Vertrag.

## ROT→GRÜN-REGEL

1. Neue Acceptance-Tests müssen auf 0.2.7 zuerst ROT sein.
2. Erst danach darf Produktcode geändert werden.
3. Minimaler Fix.
4. Derselbe Test muss GRÜN werden.
5. Vollständige alte Positiv-/Negativmatrix zusätzlich erneut GRÜN.
6. Erst dann neuer Versionsname und Paketjob.
7. Exaktes erzeugtes ZIP lokal nochmals prüfen.
8. Vor diesen Punkten **keine Übergabe**.
