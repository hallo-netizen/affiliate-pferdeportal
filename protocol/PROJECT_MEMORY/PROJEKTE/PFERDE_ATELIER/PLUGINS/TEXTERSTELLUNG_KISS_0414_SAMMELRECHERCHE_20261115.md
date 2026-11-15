# Texterstellung KISS 0.4.14 – Kategorie-Sammelrecherche (TEST)

Stand: 2026-11-15. Nur isolierte WordPress-Testseite oliver-beil.de, kein Live-Release.

## Verbindliche Bedienung
- Bestehende PSTE-Sammelrecherche statt neuer/zweiter Recherchetechnik.
- Standard: `Nächste offene Kategorien recherchieren` mit 5 als Vorschlag und 1–40 pro Auftrag.
- Alternative: `Bestimmte offene Kategorien auswählen`; nur noch nicht bearbeitete Themenfamilien auswählbar, max. 40.
- Vor jeder kostenpflichtigen Recherche ausdrückliche DataForSEO-Kostenbestätigung.
- Originalqueue `PSTE_Breadth_Research_Queue` und Original-Driver; keine zweiten Keyword- oder Artikelentscheidungssysteme.
- Bereits `ANALYZED` oder `ANALYZED_NO_ELIGIBLE_CANDIDATE` bearbeitete Familien sind keine Startkandidaten.
- Historische `RUNNING`/abgebrochene Forschungsruns werden NICHT mehr fälschlich als `ANALYZED` gezählt.
- `BLOCKED` getrennt sichtbar, nicht automatisch kostenpflichtig erneut recherchieren.
- Aktiver/gesperrter Lauf blockiert konkurrierenden Start; gespeicherte Queue und Wiederaufnahme bleiben bestehen.
- Ergebnisse/Status pro Kategorie, Anzahl Keywords, nutzbare Keywords sowie letzter Einzellauf sichtbar.
- Individuelle Ausgangsbegriff-Recherche bleibt optional als vorhandener Originalweg.
- Kategorie-Worker im MINI bleibt alleiniger Entscheider für finale Beitragskategorie.
- Original-K0 (81 Regeln, Writer, LanguageTool 6.8, Rückgabe) unberührt.

## Vollständige installierbare Test-ZIP
`Texterstellung_KISS_0.4.14_TEST_Sammelrecherche_Offene_Kategorien.zip`
Lokale SHA256 nach finalem Packen: `b831d75239beacb1ccc11912a6fdcdd1ee149fd6081b5c883a7e0d673a18d308`.
86 Dateien, davon 77 PHP, PHP-Lint 77/77 PASS, ZIP-CRC PASS.
Ausgehend von installierbarer 0.4.13, nur 4 Dateien geändert: Hauptdatei, vorhandene Original-PSTE-Sammelqueue, bestehende Original-PSTE-Recherche-Statuszählung, README. Keine Datei gelöscht.

## Ausgeführte Tests
- Bestehende Kategorieauswahl, gezielte Auswahlreihenfolge: PASS.
- Doppel-/ungültige/bereits bearbeitete/stale Kategorieauswahl: 4 Negativfälle PASS.
- Endstatus ANALYZED, ANALYZED_NO_ELIGIBLE_CANDIDATE; RUNNING, ABORTED, BLOCKED und unberührt: PASS.
- Kategorienzählung und Übergang nach erfolgreichem letzten Run: PASS.
- Form-Aktion → alte Queue → bestehenden Research Driver, Quellen- und Schnittstellenprüfung: PASS.
- **Nicht ausgeführt:** echter WordPress-/MySQL-/DataForSEO-Durchlauf auf oliver-beil.de.
- Kein Anspruch auf Live-Freigabe vor WordPress-End-to-End-Test.
