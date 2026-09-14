# DESIGN – HOBBYRAUM

STAND: 2026-09-14
STATUS: **AKTIV**

## AKTUELLER AUFTRAG

Pferderassen-Einzelansicht auf die reale breite Portal-Body-Achse bringen und den generischen Kurztext im Rassenhero entfernen.

## EXAKTE ARBEITSBASIS

Letzter installierter/getesteter Kandidat:
`PFERDE_ATELIER_DESIGN_V1.50.507_AJAX_PAGINATION_BODYWIDTH_INSTALLIEREN.zip`

SHA-256:
`b27898d26b32e9fe9910a2312b6bfbcec12c738f76290ed89304eca931353ec9`

Branch für Campus-/Fachdokumentation:
`hobbyroom/glossar-livefail-red-green-20260913`

## LIVE-BEFUND

Bereits real bestätigt und **nicht regressieren**:
- Hauptsuche / Suchwelt Pferderassen: PASS;
- Pferderassen-Hero Übersicht: PASS;
- lokale Pferderassen-AJAX-Suche: PASS;
- `Alle Rassen` Pagination: PASS.

Aktiver Fehler:
- Einzelrasse weiterhin zu schmal → LIVE FAIL.

## VERIFIZIERTE HISTORISCHE URSACHE / ARBEITSWEG

Die ältere funktionierende Portalbreiten-Lösung erweitert nicht nur einen inneren Wrapper. Sie setzt am tatsächlichen Body-/Astra-/Kubio-Containerpfad an und hebt dort die schmale Themeachse auf.

Der 1.50.507-Test bewies nur die vorhandenen CSS-Regeln, nicht dass der Live-DOM denselben Containerpfad tatsächlich vollständig verlässt.

Daher gilt:
**kein weiterer isolierter `max-width`-Versuch.**

## NEXT ACTION

1. Exakten `single-pa_breed`-Body-/Astra-/Kubio-Containerpfad aus dem aktuellen Plugin gegen den historischen bewährten Portalbreitenweg prüfen.
2. Nur für `single-pa_breed` denselben breiten Containermechanismus binden; keine fremden Seiten-/Hubdesigns übernehmen.
3. Generischen Hero-Kurztext vollständig entfernen, z. B. `Burguete stammt aus Spanien. Der Datensatz dokumentiert ...`.
4. Linke Icon-Spalte, Mitteltext, rechte Wissensspalte, Breadcrumb, Hero-Bild, AJAX und Pagination unverändert erhalten.
5. Hart positiv + negativ + Regression testen.
6. Fertige ZIP erneut exakt entpacken/testen.
7. Danach echter Nutzer-Browser-Readback der Breite.

## PASS-GRENZE

Kein Gesamt-PASS, solange die Einzelrasse live nicht sichtbar die normale breite Portal-Body-Achse nutzt.

## SCRIPT-ONLY-STANDARD

Der historische `MINIMAL_PATCH_RUNNER.py` bleibt für reine Zwei-Block-Miniänderungen verbindlich. Der aktuelle Pferderassen-Layoutauftrag ist **kein** bloßer Zwei-Block-Tausch und darf deshalb nicht fälschlich durch diesen Runner gezwungen werden.

## NICHT ANFASSEN

- normale WordPress-Beiträge;
- bestätigte Glossar-Breadcrumb-/Hero-Geometrie;
- Hauptsuche außer Regressionstest;
- Pferderassen-AJAX-Transport;
- 24er Pagination;
- Startseitenlimit 8;
- akzeptierte Grundstruktur links | Mitte | rechts.

## VERWEISE

- Stand: `CURRENT_STATE.md`
- Regeln: `PFERDERASSEN_DESIGN_RULES.md`
- Fehler: `FEHLERQUELLEN.md`
- Ausführungsprotokoll: `PROTOKOLL_20260914_PFERDERASSEN_DESIGN_CLOSEOUT.md`
