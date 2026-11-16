# K0 – erweiterbares Beitragsarten-Regal, Abnahme 16.11.2026

## Verbindlicher Stand
- **Eingebaut** in den bestehenden K0-Arbeitszweig `konzept0-portal-neutral-20261002`, Zusammenführung aus PR #812, Commit `6e74ba9ec8310ae2b1fc6ae2917075217822b12f`.
- **Kein neuer Worker, kein neuer Arbeitsschritt, kein neuer technischer Prüfpunkt.** Bereits vorhandene Schreib-, Regel-, Qualitäts- und WordPress-Übergabeschritte bleiben.
- **Keine Live-WordPress-Änderung oder Veröffentlichung.** `publish_allowed=false` bleibt zwingend.
- **Bisherige Regeldatei `RULE_VALUES.json` unverändert** mit Beratung, FAQ, Pflege und Vergleich.
- **Neues Regelfach `ARTIKELTYPEN/Anleitung.json`** für vorbereiten, aufbauen, installieren, montieren, reparieren, umbauen, abbauen; mit Vorbereitung, Schritten, Risiken, häufigen Fehlern, Ergebnisprüfung.
- Tabellen nur bei Mehrwert oder definierter Ausnahme; bei linearen Schrittfolgen erlaubt die existierende Ausnahme `LINEAR_SEQUENCE`.
- Fachliche **Einmalentscheidung vor K0**. K0 darf Beitragsart, Titel, Keyword oder Kategorie nicht erneut bestimmen. Ein Kategorie-Suffix wie `-installation` ist **keine** Beitragsart.
- Neue Beitragsarten: Ein eigenes Regelpaket im selben Ordner, vollständig mit Absicht, Abgrenzung, Struktur, Pflichtlisten, Quellen-/Sicherheitsregeln und Tabellenregel; erst dann `READY`. Fehlende, unfertige oder falsche Typen werden mit konkretem Fehlergrund abgewiesen, niemals still umgedeutet.
- Regeln werden nur für den **angeforderten Typ** geladen, damit ein neues Regelfach alte Auftragskennungen nicht verändert.

## Abgrenzung (einmalig upstream, nicht in K0 erneut)
- Beratung: passende Lösung auswählen.
- Vergleich: Alternativen gegeneinander prüfen.
- FAQ: einzelne konkrete Frage beantworten.
- Pflege: wiederkehrend reinigen, pflegen oder warten.
- Anleitung: konkrete einmalige Arbeit schrittweise durchführen.
- Ist keine eindeutige Beitragsart möglich oder fehlt ein fertiges Regelfach: Auftrag vor K0 zurückstellen, ohne Ersatztyp zu erfinden.

## Belegte Tests
- 22/22 isolierte Typregaltests: positiv/negativ, unvollständige Regeln, unbekannte/unfertige Typen, Titel-/Typbindung, Regelkennungen und Abgrenzung.
- 176/176 Gesamttests inkl. vollständigem **synthetischem** Anleitungstext, bestehenden Qualitätsprüfungen, simuliertem LanguageTool-PASS, unverändertem Writer-Seal und WordPress-Exportvertrag.
- Isolierter Test: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43863746145
- Nach Einbau: K0-Selbsttest mit Portalzuordnung, PPM-6.7.9-Parität, K0-Sperren und gesamter Regression erfolgreich.
- Live-Quelle: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43864164747
- Alle neuen Tests nutzen für das neue Regalfach frisch erzeugte Daten und keinen alten K0-Lauf.

## Offene Punkte – keine falschen Fertigmeldungen
1. Alte MINI-Charge sendet `Installation` als Beitragsart. Diesen **vorgelagerten Fehler** ohne neue SEO-/Titelentscheidung und ohne K0-Umbau korrigieren. Die Kategorie `wassertroege-fuer-weiden-installation` bleibt eine Kategorie.
2. Echte LanguageTool-6.8-Ausführung auf einem frischen `Anleitung`-Produktionsauftrag sowie echter WordPress-Import sind **noch nicht erfolgt**. Die Tests dafür sind bislang nur lokal/synthetisch.
3. Keine automatische Umbenennung historischer Aufträge. Die Besitzerentscheidung für `article_type` muss einmalig vor K0 erfolgen.

## KISS-Vertrag
**Ein Regalfach = ein vollständiges Regelpaket. Ein Worker. Die bestehenden Stationen und Prüfungen. Eine Artikeltypentscheidung ausschließlich upstream. Keine zweite Auswahl, kein Ersatztyp, keine neue Station und keine automatische Veröffentlichung.**
