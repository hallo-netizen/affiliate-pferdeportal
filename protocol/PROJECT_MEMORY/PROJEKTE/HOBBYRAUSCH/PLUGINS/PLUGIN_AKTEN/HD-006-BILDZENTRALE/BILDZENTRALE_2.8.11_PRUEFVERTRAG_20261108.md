# HD-006 – verbindliche 2.8.11-Abnahme und Wiederholungssperre (08.11.2026)

## Maßgeblicher Stand
- ZIP: `Bildzentrale-2.8.11.zip`, 84.425 B, SHA256 `e13f79ee28d8996458f452de55973f0f75c05f2b09153b935caa3cee1af1f952`.
- Vollständiges Plugin mit zwei PHP-Dateien, PHP-Lint 2/2 und ZIP-Integrität bestanden.
- Echte Programmkonstruktionen lokal simuliert mit positiven **und** negativen Fällen: **86/86** Backend, **27/27** WordPress-Menü und **31/31** Chromium-Browser-Klicktests, gerenderte 862-Hobby-Liste.
- ZIP, Prüfbericht, Quelltests und Protokolle liegen dauerhaft in persönlicher Library `/Hobby Depot/Plugin-Büro/`; vollständige GitHub-Binärdatei ist nicht behauptet.
- **Keine bestätigte Live-WordPress-Installation, keine echte Magnific-Bildgeneration.** Lokale Tests dürfen niemals als Live-PASS bezeichnet werden.

## Ursachen und Lösungen
**Motivwunsch vs. Altbild:** Das alte Hobbyregister-Fotobriefing durfte den eigenen Motivwunsch überlagern. 2.8.11 erzeugt die Anbieter-Anfrage mit dem **eigenen Motivwunsch an erster Stelle**, ohne altes Bildbriefing bei eigenem Wunsch. Alle expliziten Ausschlüsse sind verbindlich. Für „Freunde beim 3D Bogenschiessen. kein tier!“ wird explizit ausgeschlossen: lebende Tiere, Wildschwein, Tierattrappen, tierförmige 3D-Ziele, Jäger/Jagdszenen. Die Anfrage wird serverseitig mit neuer Prompt-Zeichenfolge gesendet und das gelesene Motiv vom Backend quittiert. Andere Motive müssen andere Prompts im Provider-POST ergeben. **Der externe Anbieter kann trotzdem unbeabsichtigt ein unpassendes Bild erzeugen: Live-Ergebnis auswerten, nicht Erfüllung versprechen.**

**Bestandsbilder:** HD-007 1.2.21 ist die autoritative, echte Datenquelle für die Hobbyregister-Vorschaubilder. `hobby:airbrush-modellbau` ist dort ein explizites `FINAL_MASTER_VERIFIED`-Masterbild; genau dieses aktuelle Bild wird von 2.8.11 als „Bild passt“ erkannt, solange keine speziellere Nutzerentscheidung zum Bild existiert. Andere zugewiesene ältere Bilder gelten nicht automatisch als positiv bewertet, sondern „Noch nicht geprüft“, es sei denn dieses exakte Bild wurde ausdrücklich bestätigt. Bewertung bei Bildwechsel nicht vererben.

**Batik-Quellenkonflikt:** HD-007 1.2.21 benutzt für `hobby:batik` aktuell den generischen Registerbestand `hobby-depot-v150617/subcategories/gestalten/textilgestaltung-v150616.webp`. Der separate Batik-Kategorie-Hero in HD-003 besitzt einen anderen Bildpfad. Das Backend der Hobbyregister-Bearbeitung darf kein anderes als das tatsächliche HD-007-Hobbyregister-Bild ausgeben und nicht behaupten, es sei das separate Kategorie-Hero. 2.8.11 weist auf diese Abgrenzung hin, führt **keine** pauschale, gefährliche Gleichsetzung und keine heimliche Änderung von HD-003 aus. Eine automatische inhaltliche Beurteilung aller alten Fotos ist nicht getestet und wird nicht behauptet.

## Dauerhafte UI-Regeln
- Eigenes HD-006-Menü heißt **„Bildzentrale“**, anderer unabhängiger Menüpunkt **„Bilder zuordnen“**, **verschiedene Klick-URLs**.
- Drei redaktionelle Bewertungen: „Noch nicht geprüft“, „Bild passt“, „Bild passt nicht“. Technische Master-/Produktionsstatus separat.
- Jedes Hobby, auch Masterbilder, jederzeit neu bearbeitbar. Eigener Motivwunsch muss nach bestätigter Kosteninformation direkt in **„Bild erstellen“** einfließen. Keine zweite versteckte Starttaste.
- Neue Bilder als getrennte, vorläufige Vorschau im WordPress-Medienbestand; erst nach ausdrücklicher Übernahme aktivieren. Vorheriges Bild und Bildzuordnung nicht heimlich überschreiben. Fehldownload und Fehlerantwort sichtbar; ein bereits bezahlter Entwurf muss ohne neue Anbieterbezahlung erneut abgeholt werden können.
- Das Designplugin **HD-003 darf nicht bearbeitet** werden, bis Nutzer den Stopp aufhebt. Die bekannte Kachelformatabweichung bleibt separate Aufgabe.

## Pflichtprüfung bei jeder weiteren Version
Exakte ZIP-Quellversion, Dateisumme, 862 Zeilen, richtige Live-/Registerbildquelle pro Hobby, positiv bestätigter Originalmaster, negativ und nicht geprüft, Motivwunsch eindeutig im echten simulierten Provider-POST, neuer Wunsch/alter Job, kein Tier-Wildschwein-Ausweichmotiv im Prompt, Safe-Apply/Undo, Schutz der alten Bilder, Fehlerfälle, beide Menüs, echte Browser-Klicktests und PHP-Lint prüfen. Ausfall = keine Pluginfreigabe.
