# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-13
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13

NUTZER-READBACK:
Abstand nach oben ist mit 0.2.7 korrekt.

Keine weitere Änderung an diesem Punkt ohne neue Regression.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: LIVE FAIL / BLOCKER

NUTZER-READBACK:
0.2.7 ist real nicht responsiv.

HART REPRODUZIERT:
Der ausgelieferte Code hält oberhalb 720px den Hero auf `min-height:360px` und das Bild absolut auf `height:100%`. Erst unter 720px greift `height:auto`.

Der frühere Acceptance-Test war unzureichend: Er prüfte nur CSS-Zeichenfolgen und keine realen Browsermaße.

DIAGNOSE:
Run `34749713877`, Job `103703878642` → Marker `UGE_RESPONSIVE_GAP_REPRODUCED`.

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung kaputt
STATUS: LIVE FAIL / ROOTCAUSE TECHNISCH REPRODUZIERT / BLOCKER

NUTZER-READBACK:
AJAX-Trefferliste liegt falsch über dem Hero statt direkt am Suchfeld.

ROOTCAUSE:
`render_search_tools()` gibt `.uge-search-suggestions` außerhalb des positionierten `.uge-search-form` aus. Gleichzeitig ist `.uge-search-suggestions` absolut positioniert, ohne einen passenden positionierten Container. Die JSON-Antwort kann korrekt sein, obwohl die sichtbare Suche kaputt ist.

Der frühere AJAX-Test prüfte nur `admin-ajax.php`-JSON und nicht die sichtbare Browserposition.

DIAGNOSE:
Run `34749713877`, Job `103703878642` → Marker `UGE_AJAX_OVERLAY_BUG_REPRODUCED`.

## GLOSSAR-ROUTE-004 – Einzelbegriffe liefern keine echte Glossarseite
STATUS: LIVE FAIL / UPDATE-PFAD-FEHLER REPRODUZIERT / BLOCKER

NUTZER-READBACK:
Links auf Einzelartikel funktionieren nicht.

HART REPRODUZIERT:
Der bisherige Hardtest prüfte 0.2.5 → 0.2.7. Der reale, durch unsere Übergaben mögliche Pfad 0.2.6 → 0.2.7 wurde nicht geprüft.

0.2.6 und 0.2.7 verwenden beide Rewrite-Schema `5`. Ist der Rewrite-Zustand unter 0.2.6 bereits falsch, erkennt 0.2.7 keinen Schemawechsel und führt keinen erzwungenen Rewrite-Neuaufbau aus.

Im Diagnose-Run wurde unter 0.2.6 bei gespeichertem Schema 5 der Glossar-Rewritezustand gezielt beschädigt und danach über den echten WordPress-Updater auf 0.2.7 aktualisiert. Ergebnis: Schema bleibt 5 und heilt nicht. Der Einzelbegriff liefert danach zwar HTTP 200, aber **kein** `<article class="uge-single-wrap">` – damit ist der frühere reine HTTP-Status als falscher Sicherheitsbeleg widerlegt.

DIAGNOSE:
Run `34749713877`, Job `103703878642` → `UGE_027_AFTER_026_TERM_HTTP=200` + `UGE_026_TO_027_UNCHANGED_SCHEMA_BUG_REPRODUCED`.

## GLOSSAR-ROUTE-005 – Kategorieseiten erreichen nicht den echten Kategorie-Renderer
STATUS: LIVE FAIL / UPDATE-PFAD-FEHLER REPRODUZIERT / BLOCKER

NUTZER-READBACK:
Kategorieseiten erscheinen identisch zur Startseite.

HARTER GEGENBELEG:
Im sauberen Runtimezustand ist die Kategorieausgabe eindeutig verschieden von der Startseite: Kategorie enthält `.uge-category-head` und enthält weder `.uge-hero` noch `.uge-tools`.

Wenn live die Startseite erscheint, erreicht der Request den Kategorie-Renderer nicht korrekt.

Im reproduzierten 0.2.6-Schema-5-Fehlerzustand und anschließendem Update auf 0.2.7 heilt der Rewritezustand nicht; `/glossar/gesundheit/` liefert im Diagnosefall HTTP 301 statt der Kategorieausgabe.

DIAGNOSE:
Run `34749713877`, Job `103703878642` → Marker `UGE_CLEAN_CATEGORY_DISTINCT_PASS`, danach `UGE_027_AFTER_026_CAT_HTTP=301` und `UGE_026_TO_027_UNCHANGED_SCHEMA_BUG_REPRODUCED`.

## GLOSSAR-FE-006 – Frühere Testumgebung war kein echter Design-Integrationstest
STATUS: TESTLÜCKE BESTÄTIGT / MUSS VOR NÄCHSTER ABNAHME GESCHLOSSEN WERDEN

BEFUND:
`exact-0.2.6-test/02_boot.sh` installierte real WordPress, MySQL und Astra, ersetzte das Pferde-Designplugin aber durch einen kleinen selbstgebauten `Pferde_Template_Kit`-Stub.

Folge:
Ein PASS dieses Runners darf nicht mehr als echter Pferde-Design-Integrations-PASS bezeichnet werden.

Pflicht vor nächster Plugin-Ausgabe:
- tatsächliches Pferde-Designplugin in den Integrationslauf;
- sichtbare Browserprüfung der AJAX-Position;
- echte Browserbreiten für Hero-Responsivität;
- Kategorie muss echten Kategorie-Renderer liefern und Startseitenmarker negativ ausschließen;
- Einzelbegriff muss echtes Glossar-Artikelmarkup/Inhalt liefern;
- Updatepfade von allen tatsächlich ausgegebenen Vorgängern, insbesondere 0.2.6 und 0.2.7, müssen geprüft werden.

## ÜBERGREIFENDER STATUS

0.2.7: **BLOCKED / NICHT VERWENDEN / KEINE ABNAHME**.

0.2.6: historische Zwischenversion, ebenfalls nicht verwenden.

Aktiver Diagnosebranch:
`hobbyroom/glossar-027-release-hardtest-20260913`.

Autoritativer Live-Fail-Diagnoselauf:
Run `34749713877`, Job `103703878642`.

Kein neues Plugin ausgeben, bevor die vier realen FAILs im neuen Acceptance-System zuerst ROT reproduziert und anschließend mit minimalem Fix GRÜN bewiesen sind.
