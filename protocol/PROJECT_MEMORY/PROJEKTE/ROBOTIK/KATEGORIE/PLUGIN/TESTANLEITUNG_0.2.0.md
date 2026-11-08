# Erster WordPress-Test – Robotik Kategorie 0.2.0
Stand: 08.11.2026 · **Nur neue WordPress-Testinstallation**

## Geprüfter Kandidat
`PLUGIN/INSTALLATIONSKANDIDAT_0.2.0.zip` im Robotik-Kategoriebüro.
- Identität: `robotik-kategorie-workflow`; kein Companion-Plugin.
- PHP >= 8.1; WordPress >= 6.4.
- Vorabtest: 16/16 Strukturprüfungen, 3/3 Admin-Ansicht/Speichervorgänge mit WordPress-Stubs, PHP-Lint, ZIP-CRC.
- Kein Plugin-Aufruf erzeugt WordPress-Seiten, WordPress-Terms oder HivePress-Kategorien.
- **Noch kein Test auf echter WordPress-Seite**, keine Live-Freigabe für den Import.

## Einmaliger Ablauf (noch nicht ausgeführt)
1. Ausschließlich auf einer neuen, leeren WordPress-Testinstallation arbeiten. Bestehende Kategorienplugins nicht parallel aktivieren.
2. **Plugins → Plugin hinzufügen → Plugin hochladen**: `INSTALLATIONSKANDIDAT_0.2.0.zip` hochladen und aktivieren. Soll: genau `Robotik Kategorie-Workflow (Neutralstart)` Version `0.2.0`.
3. WordPress-Menü **Robotik Kategorie** öffnen. Die JSON-Vorlage muss `project=robotik, nodes=[]` enthalten; keine andere Domain, keine Altportalbegriffe.
4. Auf **Nur prüfen** klicken: gültiger leerer Entwurf, keine neuen Seiten/Kategorien.
5. Den ausschließlich zu Demonstrationszwecken erstellten JSON-Testbaum `TESTDATEN/robotik-testbaum-3-piloten.json` in das Eingabefeld einsetzen, auf **Nur prüfen** klicken. Erwartet: PASS; keine WordPress-Objekte.
6. Auf **Geprüften Entwurf speichern** klicken. Danach im Backend neue Seiten, Beiträge, normalen WordPress-Kategorien und HivePress-Kategorien prüfen: **weiterhin keine zusätzlichen Objekte**.
7. Negativtest: Bei einer Test-Inhaltskategorie die `parent`-ID auf `area-log` statt `product-amr` ändern; **Nur prüfen** muss die Kategorie unter einer Sammelseite ablehnen. Nicht speichern.
8. Browser neu laden: gültig gespeicherter Entwurf ist noch da. Kein Frontend geändert.
9. Admin-Version, Frontend, PHP-Fehlerprotokoll und tatsächliches Ergebnis protokollieren. Erst nach echtem PASS Kandidat als `CURRENT.zip` in Robotik übernehmen.

**Achtung:** Das ist ein sicherer Planungs-/Validierungstest. Für die spätere eigentliche Produkt- und Keyword-Ermittlung fehlen im Robotik-Plugin noch die recherchierenden Funktionen der allgemeingültigen Kategorie-Engine. Diese Aufgabe getrennt lösen. Keine DataForSEO-Aufrufe ohne Freigabe.
