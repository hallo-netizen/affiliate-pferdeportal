# PFERDERASSEN – DESIGNREGELN

STAND: 2026-09-14
STATUS: VERBINDLICH

## Übersicht

- Pferderassen-Startseite zeigt maximal **8 Rassenvorschauen**.
- `Alle Rassen` ist eine eigene Vollansicht und wird mit **24 Rassen pro Seite** paginiert.
- Aus A–Z-Ansichten, Suchansichten, Rassengruppen und der Vollansicht muss ein sichtbarer Rückweg zur **Pferderassen-Startseite** vorhanden sein.
- Rassengruppen und Rassenkarten bleiben echte Links mit Pointer-/Hoververhalten.
- Karten-Hover: **Überschrift + `zur Rasse` ocker**; Schreibweise `zur Rasse` mit kleinem z.

## Hero Übersicht

Verbindlicher Stand:

- Kicker: `PFERDE IM PORTRÄT`
- H1: `Pferderassen`
- Claim: `Charakter, Herkunft & Besonderheiten`

Hero-Geometrie, weicher Übergang und Breadcrumb-Abstand werden aus dem bestätigten Glossar-Prinzip übernommen und nicht separat neu erfunden.

## Einzelrasse

- eigener Scope `pa_breed`; normale WordPress-Beiträge bleiben unverändert.
- Breadcrumb muss sichtbar sein:
  `Startseite > Pferde Journal > Pferderassen > Rassengruppe > Rassename`
- `Pferderassen` im Breadcrumb verlinkt auf die Pferderassen-Startseite.
- Rassengruppe verlinkt in die gefilterte Pferderassen-Übersicht, nicht auf ein separates nicht-öffentliches Taxonomiearchiv.
- letzter Breadcrumb verwendet den kurzen Rassennamen, nicht den langen SEO-Artikeltitel.
- Autor wird ausgeblendet; Datum darf dezent sichtbar bleiben.
- Hero nutzt das Beitragsbild; dasselbe Bild ist Vorschaubild in Rassenkarten/Navigation/Suche.
- Hero zeigt **keinen zusätzlichen generischen Kurztext** wie `X stammt aus ... Der Datensatz dokumentiert ...`.
- Die linke visuelle Icon-Spalte bleibt Bestandteil des Designs.
- Desktop-Grundstruktur: **linker Icon-Steckbrief | redaktioneller Factsheet-Text | rechte Wissensspalte**.
- rechte Wissensspalte: Rassengruppe, Besonderheiten, später strukturierte ähnliche Rassen.
- Mobil werden die drei Zonen kontrolliert untereinander gestapelt.

## Breitenregel Einzelrasse

Die Einzelrassenseite muss die **bewährte breite Portal-Body-Achse** verwenden. Ein bloßes lokales `max-width` am inneren Rassenwrapper reicht nicht.

Verbindlich:
- Astra/Kubio-Containerbegrenzungen müssen für `single-pa_breed` am tatsächlichen Body-/Containerpfad aufgehoben werden;
- der Fix orientiert sich am bereits bewährten Portalbreitenweg (`pftk-portal-page`/volle Content-Achse), ohne fremde Seitendesigns auf `pa_breed` zu ziehen;
- kein PASS aus CSS-Sollwerten; maßgeblich ist der reale Browser-Readback.

## Suche

- Hauptsuche AJAX und Suchergebnisseite enthalten getrennte Suchwelten:
  `Seiten | Beiträge | Glossar | Pferderassen | Anzeigen`.
- Pferderassen-Suche ist an den echten Post-Type `pa_breed` gebunden.
- lokale Pferderassen-AJAX-Suche verwendet den bereits bewährten Header-AJAX-Transport mit `scope=pa_breed`.

## Tatsächlicher Stand 1.50.507

Paket:
`PFERDE_ATELIER_DESIGN_V1.50.507_AJAX_PAGINATION_BODYWIDTH_INSTALLIEREN.zip`

SHA-256:
`b27898d26b32e9fe9910a2312b6bfbcec12c738f76290ed89304eca931353ec9`

Lokale Prüfung exakt gegen ZIP:
- Contract 28/28 PASS;
- Runtime 28/28 PASS;
- PHP-Lint PASS;
- 11/11 absichtlich gebrochene Varianten ROT;
- ZIP-/Strukturprüfung PASS.

Realer Nutzer-Readback:
- Pagination `Alle Rassen`: **LIVE PASS**;
- lokale Pferderassen-AJAX-Suche: **LIVE PASS**;
- Einzelrassenbreite: **LIVE FAIL** – Seite bleibt sichtbar zu schmal.

Damit ist 1.50.507 **kein Gesamt-LIVE-PASS**.

## NEXT FIX

Nur die reale Breitenursache am Body-/Astra-/Kubio-Containerpfad korrigieren und im selben Patch den generischen Hero-Kurztext entfernen. AJAX und Pagination nicht regressieren.