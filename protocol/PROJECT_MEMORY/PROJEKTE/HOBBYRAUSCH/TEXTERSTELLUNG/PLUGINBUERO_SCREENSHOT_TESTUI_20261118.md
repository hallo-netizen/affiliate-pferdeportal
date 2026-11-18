# Hobbydepot Texterstellung – Screenshot und Pluginbüro-Stand 18.11.2026

## Aktuelles Originalartefakt / Ablage überprüft
- Die bereits ausgelieferte, **nicht neu gebaute** ZIP `Texterstellung_Hobbydepot_0.4.24.1_ERSETZEN.zip` existiert in `/Hobby Depot/Plugin-Büro/` und `/hobbydepot/TEXTERSTELLUNG/INSTALLATIONSKANDIDATEN/`.
- Im aktuellen Lauf ZIP lokal noch einmal geöffnet: SHA256 `55eeeb3beabeac2c316617cdb67e3934d51ae75b6d3568e0e3fb0a1147426b36`, 503435 Bytes, 87 Einträge, ZIP-CRC PASS, Hauptdatei `texterstellung-hobbydepot/texterstellung.php` mit Pluginheader `0.4.24.1`. **Kein neuer Code/keine neue ZIP, keine Architekturänderung.**
- **Eigenes Current im echten zentralen Pluginbüro erstellt:** `/Hobby Depot/Plugin-Büro/Texterstellung-CURRENT.md`. Zusätzliche Kopie im Fachbüro `/hobbydepot/TEXTERSTELLUNG/PRUEFBERICHTE/Texterstellung-CURRENT-20261118.md`. Die bestehende `/Hobby Depot/Plugin-Büro/CURRENT.md` betrifft **Bildzentrale 2.8.14** und wurde absichtlich nicht überschrieben.

## Screenshot des Betreibers
- WordPress `https://www.hobby-depot.de/wp-admin/admin.php?page=texterstellung` zeigt **Texterstellung → Übersicht** mit 6 vorhandenen Menüs (Übersicht, Recherche, Redaktionsplan, K0-Export, Rückimport, Diagnose).
- Sichtbar ist weiterhin alte Displayüberschrift `0.4.20 KISS – TEST` sowie ein Formular `Diese Testinstallation einmalig bestätigen`, Checkbox `Diese WordPress-Installation ist ausschließlich zum Testen bestimmt` und Button `Testmodus für diese Website freischalten`.
- Kein Nachweis der tatsächlich installierten Pluginheader-Version durch den Screenshot allein: Alt-Überschrift ist in der 0.4.24.1-ZIP noch literal enthalten. Eine installierte 0.4.24.1-Version darf nicht aus dieser Beschriftung allein erschlossen werden.

## Verbindliche Nutzerweisung
**Beim nächsten Update die alberne Test-Beschriftung und Test-Bestätigungsmaske aus der Oberfläche entfernen.** Nur vorhandenen Code bereinigen, KEIN Umbau/Neubau/Neuentwicklung. Die Testfreigabe ist nicht auf der produktiven Hobbydepot-Domain zu betätigen. Vor Eingriff die bestehenden Guards prüfen und `K0_PORTAL_ADAPTER_PENDING` sowie sämtliche K0-/DataForSEO-/Import- und Publikations-Sperren **nicht** stillschweigend öffnen. Keine zweite Entscheidungsstelle.

## Status und nächster Schritt
Stand 18.11.2026: Aktuelles, lokal geprüfte Paket **0.4.24.1** im Pluginbüro gesichert, Nutzeroberfläche ist auf hobby-depot.de sichtbar, echte Live-Endabnahme und K0-Produktionsfähigkeit **nicht** nachgewiesen. **Nächste Aufgabe**: in einem einzigen begrenzten Update die vorhandenen Test-UI-Texte und -Maske fachlich korrekt entfernen, dabei die restlichen Sicherheitsgrenzen beibehalten; Version erhöhen, Wurzelordneridentität und Tests prüfen, als neue ZIP im selben Pluginbüro protokollieren. Bis dahin keine neue Pluginversion behaupten.
