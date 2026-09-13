# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-13
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13

NUTZER-READBACK:
Der obere Abstand wurde real als korrekt bestätigt. Spätere technische Kandidaten dürfen diesen Punkt nicht regressieren.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: 0.2.8 LIVE FAIL / TECHNISCHE KORREKTUR AB 0.2.9 PASS / PFERDE-LIVE-READBACK NEUER STAND OFFEN

NUTZER-READBACK 0.2.8:
„Bild höher geworden aber kein responsive.“

TECHNISCHE ABSICHERUNG:
Das Bild selbst ist Größenanker (`width:100%`, `height:auto`), ohne künstliche feste Bildhöhe. Der Browser unter Design 1.50.469 prüft responsive Geometrie.

**Live nicht geschlossen.**

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung
STATUS: 0.2.7 LIVE FAIL / SPÄTERE TECHNISCHE REGRESSION PASS / LIVE-NEUBEWERTUNG OFFEN

AJAX-Eingabe, Treffer und Position wurden technisch grün gehalten. Kein neuer realer Nutzer-Fail hierzu dokumentiert.

## GLOSSAR-ROUTE-004 – Einzelbegriffe / Einzelartikel öffnen leer
STATUS: LIVE FAIL BESTÄTIGT / 0.2.10-rc11-native-single KUBIO-INTEGRATION PASS / PFERDE-LIVE-READBACK RC11 OFFEN

### Echter Live-Befund nach rc7

Der Nutzer lieferte den echten HTML-Anfang einer leeren Einzelansicht. Darin begann innerhalb des bereits geöffneten Kubio-`<head>` eine zweite komplette Dokumenthülle:

- erstes `<!DOCTYPE html>` / `<html id="kubio">` / `<head>`;
- danach erneut `<!DOCTYPE html>` / `<html id="kubio">` / `<head>`.

Damit war der frühere rc7-Klickbarkeitsbeweis für den echten Pferde-Livefall widerlegt.

### Root Cause

UGE ersetzte Singular-Requests über `template_include` durch `templates/single-uge-term.php`. Dieses klassische PHP-Template erzeugte mit `get_header()` / `get_footer()` eine eigene Dokumenthülle. Unter Kubio/FSE existiert die äußere Seitenhülle bereits. Der alte rc7-Test prüfte Artikelinhalt und Klickbarkeit unter rekonstruiertem Design + Loop-Poison, aber nicht die Dokumenthülle auf exakt einmal `DOCTYPE/html/head`.

### Korrektur rc11

`0.2.10-rc11-native-single` entfernt ausschließlich die UGE-Single-Template-Übernahme. Öffentliche `uge_term`-Singles werden nativ durch WordPress/Kubio gerendert. Taxonomie-/Kategorie-Template, Routing und übrige rc7-Logik bleiben erhalten.

Hardtest Run `34766187415` → SUCCESS.

Job `103747455702`:
- echtes WordPress-Docker;
- Kubio-Theme aktiv;
- Kubio-Plugin aktiv;
- Pferde-Designplugin 1.50.469 rekonstruiert und aktiv;
- veröffentlichter Hufbein-Testbegriff → HTTP 200 + Inhalt sichtbar;
- exakt 1× DOCTYPE, 1× html, 1× head;
- Draft → 404 und Inhalt nicht sichtbar;
- unbekannter Begriff → 404;
- normaler WordPress-Beitrag unverändert 200;
- Glossar-Taxonomie unverändert 200.

Marker:
- `UGE0210RC11_KUBIO_PUBLISHED_SINGLE_VISIBLE_PASS`
- `UGE0210RC11_KUBIO_SINGLE_DOCUMENT_SHELL_EXACTLY_ONCE_PASS`
- `UGE0210RC11_DRAFT_AND_MISSING_NEGATIVE_PASS`
- `UGE0210RC11_UNRELATED_POST_REGRESSION_PASS`
- `UGE0210RC11_TAXONOMY_UNCHANGED_PASS`

**Livefehler bleibt offen, bis genau rc11 real im Pferde Atelier installiert und angeklickt wurde.**

## GLOSSAR-ROUTE-005 – Kategorien nicht dem Glossar-Design angepasst
STATUS: 0.2.8 LIVE FAIL / KORRIGIERTE ACCEPTANCE TECHNISCH PASS / PFERDE-LIVE OFFEN

Verbindlich ist: eigener Kategorieinhalt plus vollständiger Glossar-Rahmen mit Hero, Suche/A–Z und Icon-Navigation. Während der aktuellen Single-Reparatur wird dieser Punkt nicht verändert.

## GLOSSAR-FE-006 – Echter Design-Integrationstest
STATUS: RC7-TESTLÜCKE FÜR FSE-SINGLE ERKANNT / RC11 UM KUBIO/FSE-INTEGRATION ERWEITERT

Design-Hauptcode 1.50.469 SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`.

rc11 prüft zusätzlich echtes Kubio-Theme + Kubio-Plugin und die Dokumenthülle auf exakt einmal `DOCTYPE/html/head`.

## GLOSSAR-REG-007 – Direktrouting zerstörte Draft-Preview
STATUS: 0.2.9 RC1 ROT / REPARIERT / REGRESSION PASS

Native Preview-Query-Parameter bleiben ausgenommen. rc11 ändert diesen Routingteil nicht.

## GLOSSAR-PROD-008 – Cluster konnte nicht vollständig veröffentlichen
STATUS: 0.2.10-rc6 FAIL / 0.2.10-rc7 REPARIERT / TECHNISCH PASS

Die `primary_category_id`-Bindung vor Veröffentlichung bleibt in rc11 unverändert erhalten.

## GLOSSAR-LAYOUT-009 – Breadcrumb-Achse im echten Design
STATUS: RC7 TECHNISCH PASS / RC11 NICHT MATERIELL GEÄNDERT

Die rc11-Reparatur betrifft ausschließlich die Single-Template-Übernahme.

## GLOSSAR-PKG-010 – Gated Übergabepaket
STATUS: RC11 TECHNISCH PASS / LIVE OFFEN

Run `34766187415`, Package Job `103747644208` → SUCCESS.

Installierbares Paket:
`universal-glossary-engine-0.2.10-rc11-native-single.zip`

Innerer Plugin-ZIP SHA-256:
`45c8f4d2a01883b6bb548c8db2db8bf9b19f5ddc80cb346b647d992fca7f748f`

Actions-Artefakt-ID:
`10320871739`

Outer artifact SHA-256:
`8ced9d219a6a38d81ab9be50fe146dc8a5acfa6a8e58a0154f5e84410d450434`

Nach Download wurde der innere ZIP erneut auf identischen SHA, ZIP-Lesbarkeit, Version und die beabsichtigte Single-/Taxonomie-Grenze geprüft → PASS.

## ÜBERGREIFENDER STATUS

- 0.2.6 / 0.2.7 / 0.2.8: historisch bzw. LIVE FAIL; nicht verwenden.
- 0.2.9: früherer technischer Kandidat; nicht CURRENT.
- 0.2.10-rc1 bis rc6: Entwicklungs-/Diagnosestufen; nicht ausgeben.
- 0.2.10-rc7: technisch grün, aber realer Single-Livefehler danach weiter vorhanden; als aktueller Kandidat abgelöst.
- rc8 / rc10 aus dem Chat: keine autoritativen Übergabestände; nicht verwenden.
- 0.2.10-rc11-native-single: **KUBIO/WORDPRESS POSITIV-/NEGATIV-/REGRESSION + PAKET PASS / PFERDE-LIVE OFFEN.**

Die realen Nutzerfehler FE-002, ROUTE-004 und ROUTE-005 werden ausschließlich durch realen Nutzer-Readback geschlossen. Aktuell wird nur ROUTE-004 bearbeitet.
