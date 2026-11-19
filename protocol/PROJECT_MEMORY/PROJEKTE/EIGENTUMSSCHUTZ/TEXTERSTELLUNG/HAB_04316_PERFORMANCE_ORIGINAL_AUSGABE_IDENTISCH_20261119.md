# 19.11.2026 – Hab Texterstellung 0.4.31.6 – Performance-Korrektur ohne Funktionsabbau

**Nach Nutzerauftrag selbst ausgeführt:** Kein Chrome-Screenshot und keine weitere Diagnose durch den Nutzer verlangt. Nachbar-Pferdeatelier nur als Inspiration, 0 Code übernommen. Hab 0.4.31.5 als unveränderte Quelle gesichert.

## Tatsächlich nachgewiesene unnötige Arbeit
- Die Recherche-Seite berechnete `PSTE_Category_Context::familyAnchors` zweimal und las denselben Kategorie-Laufstatus via identischer Datenbankabfrage zweimal.
- Zusätzlich baute `PSTE_Category_Context::familyAnchors` je Familie in `selectedCategory` die identische `PSTE_Article_Type_Registry` mehrfach auf. Jetzt wird die Registry **einmal** aufgebaut und an den existierenden Kategorienleser weitergegeben.
- Ausschließlich bestehende Programmeinstiegspunkte mit OPTIONALEN Argumenten erweitert, die alten Aufrufarten funktionieren unverändert; keine neue Klasse, Datenbanktabelle, Fach-/Artikelartentscheidung, Cache-Schicht oder zusätzliche Prüfung.

## Paket
- Technisch installierbare WordPress-ZIP `Texterstellung_HAB_UND_BEWAHR_0.4.31.6_RECHERCHE_PERFORMANCE_GEPRUEFT.zip`.
- SHA256 `29769acb82fc6aef9bee68de87248ed70d2af51fe454d1218af887f5b501a7eb`, **517035 Bytes**.
- Gegenüber 0.4.31.5 **83/87 Dateien bytegleich**, vier existierende Dateien geändert: Hauptdatei (Version + einmalige Weitergabe), `original/pste/includes/class-pste-category-context.php`, `original/pste/includes/class-pste-breadth-research-queue.php` und README. **0 hinzugefügt, 0 gelöscht.**

## Tatsächlich ausgeführte Tests
- **78/78 PHP-Lint, 8/8 JSON, 87/87 ZIP-CRC bestanden.**
- Sämtliche **7/7 Backendansichten** (Übersicht, Recherche, MINI-Export, MINI-Import, K0-Export, Rückimport, Diagnose) gegen die unveränderte 0.4.31.5 getestet: **vollständiges HTML bytegenau gleich** nach rein kosmetischer Normierung der sichtbaren Versionsnummer. Gleiche Status-/Formularausgabe.
- **16/16 Statusmuster** mit 20/93/285/570 simulierten Kategorien streng gleich; **zusätzlich 16/16 vollständige Original-vs.-Korrektur-Vergleiche** der Kategorienfamilien- und Einzelkategorie-Prüfwerte. Keine verlorene Familie/Statusänderung.
- Originale Einrichtungs-/Migrations-Fortsetzung, WordPress-AJAX-Serverablauf und der tatsächlich ausgegebene Browser-Button erneut erfolgreich gegen die unveränderten Originalfunktionen geprüft; keine Auswirkung auf K0.
- **Fünf Cold-PHP-Durchläufe je Variante** mit 285 synthetischen Hab-Fachkategorien/93 R3-Seiten: Median **622,25 ms** Original vs. **57,69 ms** Korrektur; ≈10,8-fach schneller **im lokalen Simulationsfall**. Wiederholte Run-SQL-Abfrage entfällt; Rechercheansicht 4→3 emulierte SQL-Leseoperationen.

## Wahrheits- und Freigabegrenze
- Dies ist eine lokal geprüfte, voll gepackte WordPress-Ersatzversion, **kein Beweis für den tatsächlichen WordPress-Server-Timing-Fix**. Der dortige minutenlange Hänger wurde mangels angemeldetem Remotezugriff nicht direkt gemessen, und kann zusätzliche SQL/Cache/Server-Ursachen haben.
- Keine echte DataForSEO-Abrechnung, produktive MINI/K0-Verarbeitung oder WordPress-Live-Migration ausgeführt. Ein voller E2E-Produktionslauf wird NICHT als bestanden behauptet.
- Nach Nutzerwunsch trotzdem alle verfügbaren lokalen Quell-, Ausgabe-, Regressions- und Leistungstests ohne weitere Nutzerhandgriffe durchgeführt. Kein separates Diagnose-Plugin, keine zusätzliche Screenshot-Aufforderung.

## Dauerhafte Ablage – erfolgreich bestätigt
- `/hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEN/04316/` (Library): **komplette installierbare ZIP**, darin die vollständigen Plugin-Quellen, RELEASE_STAND_04316.md, QA_04316.json, exakter Diff, reproduzierbarer Build, vollständige alte/neue Backend-Ausgaben- und Kategorienvergleichs-Tests samt JSON-Belegen.
- 0.4.31.5 bleibt separat unter `PLUGIN_FREIGABEN/04315/` als Rollback-/Quellstand bestehen.
- Pferdeatelier, Universal-Blanko (Robotik, Wassertechnik), MINI, K0, K0-Multi und sämtliche Live-Daten unverändert.

## Einziger nächster Nutzerweg
**Nur das Hab-WordPress-Plugin von 0.4.31.5 auf 0.4.31.6 überinstallieren, ohne Löschen**, danach Texterstellung → Recherche öffnen. Keine Chrome-Netzwerkanalyse, keine neue Installation eines Diagnose-Tools. Echte Wirkung auf dem Server erst nach realem Aufruf beurteilbar.