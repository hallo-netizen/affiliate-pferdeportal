# HD-006 – Bildzentrale 2.8.10 – verbindliche Bedien- und Prüfregeln

**Datum:** 08.11.2026
**Status:** ZIP vollständig erstellt, lokale WordPress-/Provider-Simulation PASS, Live-Prüfung offen.
**Plugin-ZIP**: `HOBBY_DEPOT_BILDZENTRALE_2.8.10_EINFACHE_BEDIENUNG.zip` – 83.745 Bytes, SHA256 `09c5fbfd113c1e0fa0d6552c473b5ef5d1b0f1150adddce10090291ce097227f`.
**Dauerhafte echte Voll-ZIP liegt in der persönlichen Library:** `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_BILDZENTRALE_2.8.10_EINFACHE_BEDIENUNG.zip`.
Auch Prüfprotokoll und Testnachweise dort. Eine separate GitHub-ZIP-Ablage ist nicht behauptet.

## Menüvertrag – Benutzeranweisung hat Vorrang vor älteren 2.8.8/2.8.9-Akten
- **Bildzentrale** = **HD-006, das eigentliche Bilderzeugungs-Plugin**; URL: `/wp-admin/admin.php?page=hdbz-bilder-erstellen`. Der bisherige interne Admin-Slug bleibt bewusst bestehen, um interne Links nicht zu brechen.
- **Bilder zuordnen** = anderes, unabhängiges WordPress-Plugin; URL: `/wp-admin/admin.php?page=hobby-depot-bildzentrale`. NUR dessen sichtbaren Menütext angleichen, niemals Slug, Callback, Berechtigungen, Position, Daten oder Funktion umleiten.
- Beide Einträge müssen **unterschiedliche Namen, verschiedene URLs und korrekte Klickziele** haben, egal in welcher Reihenfolge WordPress die Menüs registriert.
- Einträge anderer Plugins nicht anfassen. REST und Webhook unter `hobby-depot-bildzentrale/v1` nicht umbenennen.
- **VERBOTEN:** Die alte vertauschte Namensregel aus 2.8.8/2.8.9 wieder einführen.

## Hobbyregister – nur 1 unmittelbarer Erstellungsweg
1. Hobby suchen und öffnen. Das momentan sichtbare Bild zeigen.
2. Genau eine redaktionelle Bewertung (Auswahl): **Noch nicht geprüft**, **Bild passt**, **Bild passt nicht**. Jeder vorhandene Master bleibt jederzeit bearbeitbar. Die technische Aussage „Bild vorhanden“ ist KEINE Bewertung.
3. Optionalen Motivwunsch eingeben, **Bild erstellen** klicken. Nach Kostenbestätigung muss derselbe Klick **sofort den echten Anbieterauftrag** starten. Kein Wartelisten-Vormerken und kein zweiter Startbutton.
4. Auftrag automatisch prüfen. Fertiges Foto vor Freigabe als **noch nicht aktiv zugeordnetes WordPress-Mediathekbild** laden, damit die Vorschau lokal angezeigt werden kann. Ein gesperrtes oder defektes Providerbild NICHT als übernehmbar anzeigen.
5. **Bild übernehmen** als separate Zustimmung. Nur dann den aktuellen Hobbyregister-Master wechseln. Bei einem Fehler das bisherige Original erhalten und sichtbare Fehlermeldung ausgeben.
6. Rücknahme stellt vorherigen Master wieder her. Verwerfen entfernt nur vorläufige Entwurfsmedien, NIE das aktuelle Masterbild.
7. Bereits fertige Entwürfe dürfen eine erneute Erstellung nicht blockieren; laufende Aufträge dürfen aber nicht mehrfach kostenpflichtig ausgelöst werden. Bei fehlgeschlagenem Download kann ein vorhandener bezahlter Entwurf erneut abgeholt werden.

## Prüfbeweise und harte Freigabesperre
- 65/65 Backendprüfungen am realen HD-006-Modul, einschließlich Originalbildschutz, erneuter Mastererstellung, abgebrochenem Download, lokalem Entwurf, Wiederabholung und Rücknahme.
- 27/27 WordPress-Menüprüfungen der beiden Registrierungsreihenfolgen, der Menütexte, Slugs, Callbacks, REST-Pfade und fremden Menüs.
- 21/21 Chromium-Klicktests an der real aus PHP gerenderten 862-Hobby-Oberfläche: Der Knopf startet direkt, kein zweiter Startknopf, Ergebnisse sichtbar, ausdrückliche Übernahme, Fehler sichtbar.
- Zwei PHP-Dateien mit PHP-Syntax PASS; Voll-ZIP mit zwei vollständigen PHP-Dateien, ZIP-Integrität PASS.

**Wichtig:** Lokale WP/Provider-Mocks, kein echter Live-API-Pass und keine behauptete echte Live-WordPress-Abnahme.

**Vor jedem Update** unbedingt Menüs + direkte Bild-Erstellung + Bildvorschau + 3 Bewertungen + Bearbeitbarkeit aller Master + Schutz der alten Bilder und Wiederholung aller Regressionen prüfen. Falls ein Test scheitert: kein Installer!

**Nicht Bestandteil:** Design-/Kacheldarstellung „Drachen & Leinen“. Die Bearbeitung am Design-Plugin wurde vom Nutzer ausdrücklich gestoppt.
