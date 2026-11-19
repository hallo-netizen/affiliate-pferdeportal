# MINI-KISS-Ausgabesperre und Reparaturschleife – Prüfbericht 19.11.2026

## Auftrag
- Ausgangsproblem: Zwischenstand CATEGORY konnte bislang im Chat als hinreichende Rückgabedatei erscheinen, obwohl Redaktion/Titel für neue Themen noch fehlen.
- Nur EINE neue technische Ausgabeprüfung, bei Fehler keine Sackgasse, sondern **REPARATUR** an denselben zuständigen Worker.
- **Keine** fachliche Nachprüfung, kein Plugin-Umbau, keine Änderung an K0.

## Umsetzung
- Neuer separater Helfer `mini_release_gate.py` in `control/mini-output-gate/` im Büro, nicht im WordPress-Plugin.
- Erster Lauf bindet die gesamte unveränderte Originaldatei über SHA256.
- Alle Stufen werden im selben Arbeitsraum aus identischem Original erstellt.
- Einmaliger Gate-Lauf prüft Ausgabe-Vollständigkeit und Unverändertheit. Fehlende/redaktionell nicht entschiedene/falsche Datensätze gehen ausschließlich an `REPARATUR.json` zurück; die Quelle und bestandene Worker-Entscheidungen bleiben unangetastet. Dieselbe Gate-Funktion wird nach Korrektur erneut aufgerufen (keine konkurrierende zweite Prüfung).
- Nur bei PASS erscheinen Dateien in `FREIGABE/`, mit `NACHWEIS.json` (Batch, Dateien, SHA256, kein behaupteter WordPress-Erfolg).

## Tatsächlich geprüfte Testfälle
1. Echter zehnteiliger MINI-Export ohne Worker-Ergebnisse → REPARATUR, keine Freigabe.
2. Echter zehnteiliger MINI-Export, nur echte CATEGORY-Datei → REPARATUR bei Redaktion, keine Freigabe.
3. Künstliche EDITORIAL-Testentscheidungen, noch kein TITLE → REPARATUR nur Titel.
4. Nach Ergänzung aller fehlenden künstlichen Titel → Freigabe 3 Dateien in der Reihenfolge CATEGORY, EDITORIAL, TITLE.
5. Ein einzelner fehlender Testtitel → nur dessen Thema in REPARATUR, übrige Entscheidungen nicht zurückgesetzt; nach Korrektur PASS.
6. Manipuliertes Keyword / vertauschte Quelle → REPARATUR, keine Datei.
7. Falsche Batchkennung nach früherem PASS → alte Freigabe sofort entfernt.
8. Veränderung des gebundenen Originalexports → hart zurückgewiesen.
9. LEGACY_CATEGORY_ONLY mit gesperrten Titeln und Freigaben → nur CATEGORY nötig, kein zweites SEO- oder Titelurteil.

## Grenzen / Ehrlichkeit
- Der bestandene technische Test **beweist nicht**, dass die zehn aktuellen fachlichen Redaktionsentscheidungen/Titel bereits erstellt wurden: **NEIN**.
- Der bestandene technische Test **beweist nicht** einen WordPress-Live-Import: **NEIN**.
- Eine echte 100-prozentige globale Unterbindung falscher Datei-Links benötigt, dass die Dateiausgabe über diesen Freigabepfad erzwungen wird. Der Code stellt keine interne ChatGPT-Ausgabe-Sperre dar; er kann nur die von ihm freigegebenen Artefakte garantieren.