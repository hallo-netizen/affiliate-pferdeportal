# Hobby Depot – Bildzentrale HD-006 2.8.10 – Pflichtprüfvertrag

**08.11.2026: Lokaler vollständiger Installationskandidat.** Live-WordPress und echte Anbieteraufträge sind nicht validiert.

## Ausgangsfehler aus den Screenshots
1. Falsche/verkehrte Menünamen, obwohl zwei verschiedene Admin-Seiten gebraucht werden.
2. Klick auf „Neues Bild erstellen“ hat nur vorgemerkt, ohne einen Auftrag auszulösen. Zusätzlicher Startknopf war versteckt.
3. Zu viele sich überschneidende Knöpfe, technische Statusmeldung „Masterbild fertig“ mit menschlicher Bewertung verwechselt.
4. Vorhandener Entwurf blockierte neue Bearbeitung.
5. Externe Entwurfs-URL konnte im Browser ein kaputtes Vorschaubild ergeben.

## Verbindliche Regeln
- **Bildzentrale** (HD-006, originale Bilderzeugung), URL `admin.php?page=hdbz-bilder-erstellen`.
- **Bilder zuordnen** (anderes, ursprüngliches Zuordnungsplugin), URL `admin.php?page=hobby-depot-bildzentrale`.
- 862 Hobbys: jedes Foto und Masterbild bleibt grundsätzlich bearbeitbar.
- Redaktioneller Status exakt „Noch nicht geprüft“, „Bild passt“, „Bild passt nicht“. Der technische Bildbestand wird separat angezeigt; ein Master ist niemals automatisch positiv bewertet.
- Ein einziger „Bild erstellen“-Klick startet nach Kostenbestätigung **unmittelbar** den Anbieterauftrag, nicht lediglich eine Vormerkung.
- Das bestehende Foto bleibt bis „Bild übernehmen“ unverändert.
- Noch nicht übernommene Entwürfe in der WordPress-Mediathek prüfen; kaputte Bilder dürfen nicht übernommen werden.
- „Entwurf verwerfen“ darf **niemals** ein früher veröffentlichtes Bild löschen. Sichtbare Fehlermeldung bei Fehlschlag.
- Keine Änderungen an HD-003-Design-Plugin, der Kategorie-Fotokachel oder weiteren Portalen ohne gesonderten Auftrag.

## Geprüfter Artefaktstand
Vollständige ZIP `HOBBY_DEPOT_BILDZENTRALE_2.8.10_EINFACHE_BEDIENUNG.zip`.
SHA256 `09c5fbfd113c1e0fa0d6552c473b5ef5d1b0f1150adddce10090291ce097227f`, 83.745 Byte, 2 vollständige PHP-Dateien, ZIP-Integrität PASS, PHP-Syntax 2/2 PASS.

Lokale wiederholbare Prüfung mit echten Klassen und simulierter WordPress-Anbindung:
- **65 / 65** Backendtests bestanden;
- **27 / 27** Admin-Menütests bestanden (verschiedene Anmelde-/Registrierungsreihenfolgen, beide Klickpfade);
- **21 / 21** Chromium-Browser-Klicktests bestanden (echte gerenderte 862-Hobby-Liste).

**Das ist kein Live-Test** der tatsächlichen WordPress-Installation und kein echter kostenpflichtiger Anbieterauftrag.

## Freigaberegel für Zukunft
Nie ein weiteres Update freigeben, bevor Menü- und Klickwege, alle drei Bewertungen, Masterbild-Bearbeitung, ein einziger auslösender Bild-Button, Bestandsbild-Schutz, positive und negative Erstellungs-/Übernahmefälle, echte gerenderte Browser-Klicks, vollständige ZIP und PHP-Syntax kontrolliert sind.

## Noch offen
- Installation auf tatsächlichem WordPress und ein einmaliger End-to-End-Test eines Hobbyregister-Fotos.
- Vollständige installierbare ZIP als byteidentische Datei ins GitHub-Pluginbüro hochladen. Die hier dokumentierte GitHub-Änderung enthält **noch nicht** die ZIP; vollständiges ZIP liegt als Chat-Datei vor.
