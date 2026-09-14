# PFERDERASSEN – DESIGNREGELN

STAND: 2026-09-14
STATUS: VERBINDLICH

## Uebersicht

- Pferderassen-Startseite zeigt maximal **8 Rassenvorschauen**.
- `Alle Rassen` ist eine eigene Vollansicht; sie darf nicht wieder nur die 8 Startkarten zeigen.
- Aus A–Z-Ansichten, Suchansichten, Rassengruppen und der Vollansicht muss ein sichtbarer Rueckweg zur **Pferderassen-Startseite** vorhanden sein.
- Rassengruppen und Rassenkarten bleiben echte Links mit Pointer-/Hoververhalten.
- Karten-Hover: **Ueberschrift + `zur Rasse` ocker**; Schreibweise `zur Rasse` mit kleinem z.

## Hero

Verbindlicher Stand:

- Kicker: `PFERDE IM PORTRAET`
- H1: `Pferderassen`
- Claim: `Charakter, Herkunft & Besonderheiten`

Hero-Geometrie, weicher Uebergang und Breadcrumb-Abstand werden aus dem bestaetigten Glossar-Prinzip uebernommen und nicht separat neu erfunden.

## Einzelrasse

- eigener Scope `pa_breed`; normale WordPress-Beitraege bleiben unveraendert.
- Breadcrumb muss sichtbar sein:
  `Startseite > Pferde Journal > Pferderassen > Rassengruppe > Rassename`
- `Pferderassen` im Breadcrumb verlinkt auf die Pferderassen-Startseite.
- Rassengruppe verlinkt in die gefilterte Pferderassen-Uebersicht, nicht auf ein separates nicht-oeffentliches Taxonomiearchiv.
- letzter Breadcrumb verwendet den kurzen Rassennamen, nicht den langen SEO-Artikeltitel.
- Autor wird ausgeblendet; Datum darf dezent sichtbar bleiben.
- sichtbarer Rueckweg unter dem Titel: `Pferderassen-Startseite` und, wenn vorhanden, Rassengruppe.
- Lesedesign ruhig/lexikalisch: grosser Serifentitel, schmale Lesespalte, klare H2, keine Veraenderung normaler Artikel.

## Suche

- Hauptsuche AJAX und Suchergebnisseite enthalten getrennte Suchwelten:
  `Seiten | Beitraege | Glossar | Pferderassen | Anzeigen`.
- Pferderassen-Suche ist an den echten Post-Type `pa_breed` gebunden.

## Aktueller Kandidat

Design 1.50.505: lokal hart positiv/negativ geprueft; LIVE-Abnahme offen.
