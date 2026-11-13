# Hobby Depot – Fehlerprotokoll und aktueller Stand (13.11.2026)

## Ausgangslage und Fehler der bisherigen Arbeit
1. Auf der Seite `/gestalten/malen-zeichnen/airbrush/` wurden zuerst fachlich unpassende Idealo-Produkte (Damenmantel, Pullover „Malene“, Cotton-Batik) angezeigt. Die zuvor implementierte grobe Wortzuordnung und Elternkategorie-Vererbung war falsch.
2. Die nachfolgenden HD009-Versionen 0.1.35–0.1.37 sperrten diese falschen Artikel. Die echte passende Ausrüstungs- und Feed-Abdeckung wurde zuvor nicht ausreichend abgesichert. **Ergebnis: keine passenden Airbrush-Produkte im gezeigten Block.**
3. HD003 1.50.811–1.50.813 machte die Karten größer und passte Buttons an, **ohne die Admin-Leerplatzhalter im vorhandenen Template zu berücksichtigen**. Dadurch erschienen nach der Produktsperre drei sehr große leere Karten („Nur eingeloggt sichtbar / Affiliate-Produkt / Platz aktuell nicht belegt“).
4. Frühere synthetische HTML-/CSS-Tests überprüften eine künstlich gefüllte Produktliste, **nicht den echten Leerfall im WordPress-Hobbydepot-Template**. Die damaligen „Erfolg“-Aussagen waren fachlich unberechtigt.
5. Mehrere Plugin-Updates wurden zu früh empfohlen. Bei den letzten Tests war weder der reale WordPress-Import noch die tatsächliche Ausgabe mit passender Airbrush-Ausrüstung nachgewiesen.

## Bewiesene Ursache des aktuellen Fehlers
- Aus tatsächlichem Quellarchiv **HD003 1.50.813** (SHA256 `5fb7053f31d705b9c2001fbcdfecf518c05d8c1fe52283f058943ca48f6eba73`) vollständig geprüft.
- `affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php`, **Zeile 3219**: Wenn ein `category_product_1..3`-Slot leer ist, erzeugt das Design-Template für angemeldete Nutzer absichtlich eine **scheinbare Affiliate-Produktkarte**.
- **Zeile 1827** enthält den wortgleichen Platzhaltertext des Screenshots.
- **Zeilen 3654–3661** geben diese Platzhalter in `Empfehlungen` als drei reguläre Karten aus.
- Das war eine **Vorlagenursache**, nicht ein CSS-Farbproblem. Die leeren Produktkarten müssen **vor dem HTML-Aufbau**, nicht durch nachträgliches Ausblenden im Browser, entfallen.

## Umsetzung: HD003 1.50.814
- In **einer einzigen vorhandenen Design-Profildatei** wird die falsche Erzeugung von Produktplatzhaltern deaktiviert, für Kategorie- und frühere Startseiten-Produktplätze.
- 0 echte Produkte → **kein** Produktblock und **keine** leeren Platzhalter.
- 1 echtes Produkt → genau 1 vollwertige Karte; 3 echte Produkte → genau 3 Karten.
- Die realen Affiliate-Shortcodes und deren Produkt-HTML bleiben **unverändert**, ebenso die bereits abgenommenen Farben, das Format und Mehranbieter-Ausgabe.
- Banner- und Beitragsvorschauen werden **nicht** verändert.
- Kein Core, kein HD009, kein neuer Feed/Job/Frontend-Aufruf, kein neues System.

## Harte Prüfungen – Stand 03 (abgeschlossen)
- Originale PHP-Methoden aus dem vollständigen Plugin extrahiert und ausgeführt, nicht nur frei nachgebaute Markup-Fragmente.
- **36 Funktionstests bestanden**: eingeloggt und ausgeloggt, 0/1/3 Produkte in Kategorie, Leaf und Homepage, keine Platzhalter bei 0, erhaltene echte Produkte bei 1/3.
- Alle **1.291 ZIP-Dateien** CRC-geprüft und alle PHP-Dateien auf Syntax geprüft.
- Außer der Versionskennung im Plugin-Einstieg wurden **ausschließlich drei Zeilen im vorhandenen Produkt-Template geändert**; 1.289 der ZIP-Dateien sind byte-identisch.
- Nachweis: https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43411117782
- Neues geprüften ZIP SHA256: `263284e057b9c2a3cc57cc4807301ab2e74c1daeae8dfeb0a16191c49a9dc18f`.

## Ungeklärt – nicht als Erfolg darstellen
- **Echte Produkte für Airbrush:** Durch den Platzhalter-Fix werden keine passenden Produkte erzeugt. Bestehender Feed 2747 („Fashion/Sport/Outdoor“) hatte 52 versorgte Ziele von 381 Hobbys. Die tatsächliche zusätzliche Abdeckung des Standardfeeds 2901 wurde im authentifizierten WordPress noch nicht vergleichend ausgewertet.
- **Amazon/eBay-Mehrfachangebote:** Das Original-Rendering bleibt erhalten, aber die Anwesenheit konkreter passender Partnerangebote auf Airbrush ist damit nicht bewiesen.
- **Liveinstallation:** Diese ZIP-Datei wurde nicht durch die GitHub-Prüfung auf WordPress installiert. Ein eingeloggter Live-Screenshot nach Installation steht aus.
- **Nächste Ursache zur Bearbeitung:** Reale passende Produkte über schon vorhandene Idealo-API/Feeds/Original-Zuordnung liefern; erst echte Daten vergleichen. Nie generische Produktwerbung oder erfundene Produkte anzeigen.

## Änderungsstand
- Stand 01: Fehler-Screenshot dokumentiert, keine Änderung.
- Stand 02: Zeile 3219 als Ursache und Zeile 1827 als wortgleicher Platzhalter bewiesen.
- Stand 03: HD003 1.50.814 vollständig gebaut und 36 PHP-Lauftests bestanden. Noch nicht veröffentlicht oder installiert.


## Stand 04 – vollständiges Plugin nach harten Tests im Büro archiviert
- Datei \`HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip\` und versionsfeste Datei \`HOBBY_DEPOT_DESIGN_HD003_1.50.814.zip\` sind vollständig, byte-identisch und auf SHA256 \`263284e057b9c2a3cc57cc4807301ab2e74c1daeae8dfeb0a16191c49a9dc18f\` verifiziert.
- Vorversion \`HOBBY_DEPOT_DESIGN_HD003_1.50.813.zip\` ist unverändert vorhanden.
- Keine WordPress-Liveinstallation durch das Büro; keine echte Airbrush-Produktversorgung nachgewiesen.
- Download nach Freigabe: https://github.com/hallo-netizen/affiliate-pferdeportal/releases/download/hobby-hd003-1.50.814-no-empty-product-cards-20261113/HOBBY_DEPOT_DESIGN_HD003_1.50.814_OHNE_LEERKARTEN.zip

## Stand 05 – Veröffentlichung kontrolliert
- GitHub-Build/Archiv/Release: **vollständig erfolgreich**. [Prüf- und Veröffentlichungs-Lauf](https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/43411671049).
- Exakt herunterladbares vollständiges ZIP `HOBBY_DEPOT_DESIGN_HD003_1.50.814_OHNE_LEERKARTEN.zip`, **65.765.018 Byte**, SHA256 `263284e057b9c2a3cc57cc4807301ab2e74c1daeae8dfeb0a16191c49a9dc18f`.
- Neues `CURRENT.zip` und die versionsfeste `1.50.814.zip` im Design-Pluginbüro nachweislich vorhanden und identisch. `1.50.813.zip` bleibt separat erhalten.
- **Keine Liveinstallation und keine echte Airbrush-Produktversorgung nachgewiesen**. Leere Karten sind quellenbasiert behoben, aber relevante Produkte fehlen weiterhin, bis bestehende Idealo-Feed-Daten und Zielabgleich tatsächlich genügend passende Angebote liefern.
