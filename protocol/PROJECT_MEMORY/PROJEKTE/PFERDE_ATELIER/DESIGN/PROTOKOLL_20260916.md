# DESIGN – PROTOKOLL 2026-09-16

## Ausgeführte Änderungen

### Pferderassen-Hero
- 1.50.537: Hero-Bilddarstellung testweise auf vollständigeres Motiv / `contain` geändert und Ocker-Linien für H2 ergänzt; lokal geprüft, vom Nutzer visuell nicht übernommen.
- 1.50.538: Hero-Bilddarstellung wieder auf `cover` zurückgeführt, Ocker-Linien beibehalten; Regression lokal geprüft.
- 1.50.539: Desktop-Langtitel der Pferderassen gegen unsauberen Umbruch abgesichert; Auto-Fit auf alle Viewports erweitert, kurze Titel bleiben unverändert; Nutzerbestätigung `pass`.

### Journal-Startseite – ausschließlich `/journal/`
- 1.50.540: Überschriften der Haupt-Themenkarten fett; Bilddarstellung weniger stark beschnitten/weiter herausgezoomt; Motiv nach rechts verankert; linker Verlauf unverändert.
- Nutzer-LIVE: Bildwirkung und übriger Scope PASS; `Glossar` und `Pferderassen` im separaten Referenzraster waren noch nicht fett.
- 1.50.541: ausschließlich die beiden Referenzkachel-Titel `Glossar` und `Pferderassen` auf fett gesetzt.
- Nutzer-LIVE: `ok pass`.
- Keine Ausweitung auf Journal-Kategorien, Einzelartikel, Pferderassen- oder Glossarseiten.

## Prüfungen

1.50.539:
- alter Desktop-Umbruch reproduziert: PASS;
- neuer langer Titel einzeilig: PASS;
- kurzer Titel unverändert: PASS;
- sehr langer Titel + Mobile: PASS;
- PHP/ZIP/Regression: PASS.

1.50.540:
- Scope-Test ausschließlich Journal-Startseiten-Kartenmodul: PASS;
- Hauptkartentitel fett: PASS;
- Bildzoom/Bildfokus angepasst, linker Verlauf erhalten: PASS;
- WordPress-LIVE: Teil-PASS; nur Referenztitel noch offen.

1.50.541:
- Delta ausschließlich Version + Fettregel für Journal-Referenzkacheln: PASS;
- PHP-Lint: PASS;
- ZIP-Lesetest/Re-Extract/Version: PASS;
- WordPress-LIVE: PASS, Nutzerbestätigung 2026-09-16.

## Aktuelles Artefakt

Plugin-ID: `PPA-002`
Version: `1.50.541`
SHA-256: `f93870321df4a989e8ceeb71d6a9b4a0780831184f3b9a36f1e6e29b5e8a6ee6`
Isolierter Stand: `/Campus-Plugins/PFERDE_ATELIER/PPA-002/CURRENT.zip`

## Korrektur der Plugin-ID

Eine zwischenzeitlich im physischen Plugin-Schrank angelegte Design-ID `PPA-013` war eine zweite/falsche Identität für dasselbe Plugin. Kanonische ID laut Pluginregister ist `PPA-002`. Die aktive zweite Kopie wurde deshalb aus dem aktiven Schrank entfernt und in `/Campus-Plugins/PFERDE_ATELIER/ARCHIV/PPA-013` verschoben. Sie ist nicht CURRENT.

## Warum

- Journal-Anpassungen bleiben absichtlich root-spezifisch, weil der Nutzer ausdrücklich **nur die Journal-Startseite** ändern wollte.
- Bildfokus liegt rechts, weil der linke Verlauf den sichtbaren Hauptinhalt sonst abschneidet.
- Keine globalen Stilregeln aus dieser lokalen Änderung ableiten.
- Eine Pluginidentität pro reales Plugin; keine zweite CURRENT-Wahrheit.
