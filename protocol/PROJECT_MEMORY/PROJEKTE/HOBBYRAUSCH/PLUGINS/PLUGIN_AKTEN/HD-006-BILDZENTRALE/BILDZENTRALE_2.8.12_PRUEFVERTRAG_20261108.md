# Bildzentrale HD006 2.8.12 – verbindliche Fehlerursachen und lokale Abnahme, 08.11.2026

## Maßgebliche Vollversion
`Bildzentrale-2.8.12.zip`, 85.492 Bytes, SHA256 `75b9b54b5956be86ca8c672c51da2231bba6956bf63eac2d55eb811a348ca73c`. Zwei vollständige PHP-Dateien. ZIP, Prüfprotokoll, eigenständige Testnachweise in ChatGPT Library `/Hobby Depot/Plugin-Büro/`, NICHT als Binärdatei in GitHub.

## Ursachen – nicht Symptome
1. HD007 1.2.21 Original-Hobbyregister-Bildliste enthält für Airbrush, Aeroponik und Batik generische alte Bildverweise. HD003-Quellstand enthält freigegebene, eigene Master: Airbrush (hobby-depot-v150758/hobby-masters/airbrush.webp), Aeroponik (hobby-depot-v150759/hobby-masters/aeroponik.webp), Batik (hobby-depot-v150753/batik-hero.webp). Maßgebliche HD003-Methode `Hobby_Depot_Profile_V150709::hobby_image_center_v150769` priorisiert ausdrücklich in WordPress ausgewählte Originalbilder, dann eigene Hobby-Master, dann HD007-Master und Batik-Master. Keine blinde Gleichsetzung unterschiedlicher Kategorie-/Registerquellen.
2. HD006 2.8.11 testete die „Übernahme“ mit einer vereinfachten Frontend-Nachbildung, ohne die aktive Bildauflösung nach dem Schreiben zu prüfen. Ein defekter Fotoanschluss konnte deshalb einen scheinbaren Erfolg melden. Ein Negativtest an der neuen Version entdeckte zudem, dass `APPLIED` vor Bestätigung des neuen Frontend-Bildes gesetzt wurde.

## Verbindliche Lösung
- HD006 2.8.12 fragt die unveränderte HD003-Methode nur **lesend**, nur für die exakte Hobby-ID ab. Ausschließlich Quellen `bildzentrale`, `hobby-master`, `hd007-master`, `batik-master` werden akzeptiert. Bereits freigegebene HD007-Finalmaster gehen vor. Generische Platzhalter gelten nicht als passend.
- Auf den **tatsächlichen** HD007-Bildaufruf (`HD_Hobbyregister_Frontend_Stable127::record_image`) begrenzte Filterung, nicht global auf andere Plugins. Rekursion wird verhindert, Datensätze für denselben Aufruf werden nur einmal gelesen. Vorschau und die PHP-Hobbyregister-Bildausgabe benutzen dieselbe Quelle.
- „Bild übernehmen“ erfordert ausdrückliche Freigabe, Medienprüfung und **den erfolgreichen erneuten Aufruf des HD007-PHP-Bildresolvers**, der exakt die übernommene Bild-URL ergeben muss. Nur dann: Status `APPLIED`, Bewertungen neu setzen und vorhandene Bearbeitungsfreigabe abschließen.
- Bei absichtlich fehlendem Frontend-Filter wird der alte Master wiederhergestellt, der bereits bezahlte Entwurf bleibt `COMPLETED` und wird **nicht** gelöscht, die Oberfläche meldet ausdrücklich Fehler (HTTP409). Der Entwurf kann nach Behebung ohne kostenpflichtige Neugeneration übernommen werden. Undo zum vorherigen freigegebenen Original geprüft.
- **Keine Code-/Options-/Dateiänderung** an HD003, HD007, Pferdeatelier oder K0. Das gesondert gestoppte Design-/Kachelprojekt bleibt unangetastet.

## Reproduzierbare Positiv-/Negativnachweise
- 103/103 Backendprüfungen auf der **tatsächlichen 2.8.12-PHP-Datei** mit eigener nachgebildeter WordPress-/HD003-/HD007-/Magnific-Umgebung. Negativfall: Bildfilter absichtlich entfernt, alte URL muss bleiben, Entwurf muss weiter freigegeben werden können, keine falsche Übernahme.
- 27/27 WordPress-Menüprüfungen (Bildzentrale/Bilder zuordnen, getrennte Ziele, fremde Menüeinträge geschützt).
- 35/35 Chromium-Klicktests für 862 Hobbys, freigegebene Airbrush-/Aeroponik-/Batikbilder, drei Bewertungen, Motiveingabe, Start/Übernahme/Fehlerzustände.
- 2/2 PHP-Syntax und vollständiges ZIP (keine Minipatches). Alle Prüfungen zusätzlich aus einem frischen entpackten Beweispaket an einem zweiten Ordner **erneut** ausgeführt und bestanden.
- Vollständige Beweisdaten: `Bildzentrale-2.8.12-Testnachweise.zip` im Library-Pluginbüro; PHP-Simulator, HTML, Browserklicktests, Testbild, Protokolle, PHP-Quellen.

## Abnahmegrenze, keine falschen PASS-Angaben
Alle Tests sind **lokale Simulationen** mit echten HD006-Quellen, nicht gegen echte WordPress-/Magnific-Server. HD003-/HD007-Quellverweise wurden separat aus den neuesten GitHub-ZIP-Dateien direkt geprüft. Der echte Live-Ausgabeweg, Magnific-Ergebnis, Bilder-Cache und der Browser des Nutzers bleiben offen. Eine sachliche Zustimmung im Backend ist keine automatische visuelle Bildbewertung durch ein KI-Modell.

**Zwingend für künftige Updates:** Quellenabgleich über vorhandenes freigegebenes HD003/HD007-Bildkonzept; echte Frontend-Übernahme mit positivem UND negativem Test; nie nur ein gespeicherter Datenbankwert als Bestätigung; keine zusätzliche zweite Fotodatenbank oder Erweiterung des Designplugins.
