# Bildzentrale HD006 2.8.14 – verbindlicher weiter Hero-Prompt (08.11.2026)

**Aktueller Kandidat:** vollständige `Bildzentrale-2.8.14.zip`, **86.568 Bytes**, SHA256 `06ffeac81f37d5d20a424e1d93dd74c597b0bf1cb7d472da391337d5c49c529e`; gespeichert in persönlicher Library `/Hobby Depot/Plugin-Büro/`, dort nach Download erneut byteidentisch bestätigt. **Kein Binär-ZIP-Commit auf GitHub.**

## Ursache und KISS-Fix
Der allgemeine, noch von 2.8.13 übernommene Stil empfahl ausdrücklich natürliche Nahaufnahmen von Armen/Händen/Oberkörpern. Der Hobbyregister-Hero ist dagegen ein flacher, breit beschnittener Banner mit Titel links. Schon „medium-wide shot“ genügte in den Live-Beispielen Arduino und 3D-Scanning nicht. Die Kamera-Vorgaben waren widersprüchlich.

**Nur in der HD006-Hobbyregister-Prompterzeugung** wird der allgemeine widersprüchliche Stil durch einen knappen natürlichen Foto-Stil ersetzt. Die Kamera wird verbindlich **wesentlich weiter zurückgesetzt (2- bis 3-facher Abstand)**. Vorgeschrieben sind Handlung, relevantes Gerät, Objekt und Umgebung zusammen in einer einzigen verständlichen Weitaufnahme. Native 3:2 Bildquelle; schmaler 4:1 bis 5:1 Hero-Crop muss verständlich bleiben. Wichtige Gegenstände/Hände in Bildhöhe 35–65 % und Bildbreite 55–80 %; links 35 % ruhige Fläche für Titel. Keine Makroaufnahme, keine Halbporträts, keine gigantischen Vordergrundgeräte. Falls individuell ein Motiv eingegeben wird, bleibt dieses samt Verboten erhalten; **auch volle 400 Zeichen + Tier-Ausschluss** passen mit abschließendem Prioritätscheck in die 3000-Zeichen-Schnittstelle.

## Vollständiger Testnachweis
- **149/149** echte HD006-PHP-Backendregressionen mit positivem/negativem WordPress-/Magnific-Mock, insbesondere überlange Motivwünsche und kein Abschneiden der Schlussregeln.
- **27/27** Admin-Menüregressionen, Bildzentrale und Bilder zuordnen weiterhin getrennt.
- **39/39** echte Chromium-Klicktests gegen vom PHP generierte Hobbyregister-862-Oberfläche.
- Alle drei Prüfungen **aus frisch entpacktem, eigenständigem Testarchiv** unabhängig wiederholt: PASS; beide PHP-Dateien Syntax PASS, Installationsarchiv intakt.
- Genaue Quelländerung: Hauptdatei nur 2.8.13→2.8.14; Hobbyregister-Komponente genau zwei PHP-Zeilen geändert (Stil + Prompt); keine sonstigen Funktionen.

**Unverändert:** bestehende Fotos, Bildstatus, Bildzuordnung, bestehende Master, Bildübernahme/Undo und andere Bildzentrale-Workflows, HD003-Designplugin, HD007, Pferdeatelier/K0. Kein Bild automatisch ersetzt oder erzeugt. Manuelle Bildzuordnung des Nutzers bleibt bestehen.

**OFFEN:** echter WordPress-Livetest mit neu erzeugtem 2.8.14-Herobild; Magnific kann trotz prompttechnischer Vorgaben nicht garantiert folgen. Ein neuer bezahlter Auftrag erfolgt nur nach absichtlicher Nutzerentscheidung. 

**Dauerhafte Artefakte:** `Bildzentrale-2.8.14.zip`, `Bildzentrale-2.8.14-Testnachweise.zip`, `Bildzentrale-2.8.14-Zwischenprotokoll.md`, `CURRENT.md` im Library-Pluginbüro.
