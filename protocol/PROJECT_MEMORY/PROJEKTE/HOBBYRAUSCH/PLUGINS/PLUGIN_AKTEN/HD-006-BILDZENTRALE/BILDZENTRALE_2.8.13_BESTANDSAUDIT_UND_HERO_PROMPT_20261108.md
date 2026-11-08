# Bildzentrale HD006 2.8.13 – systematischer Fotobestand, Motivprüfung und neuer Hero-Prompt

**08.11.2026 – lokal geprüfter Kandidat, kein Live-WordPress-PASS.**

## Vollständiger Bestand direkt gegen aktuelle Quellen geprüft

Die HD007-1.2.21-CURRENT-ZIP enthält 862 exakt zugeordnete Hobby-Fotopfade. Beide Originalarchive HD007 und HD003 wurden durch den GitHub-Read-only-Audit-Workflow direkt geöffnet; jedes referenzierte WebP-Bild wurde tatsächlich gelesen und als Bild decodiert. Bestätigte Ergebnisse aus erfolgreichen Actions-Läufen **42499289913** (Struktur/Quellen) und **42499778815** (alle Bilddateien/Formate/Auflösungen):

- **862/862** Original-Fotozuordnungen lesbar, **0** fehlende oder beschädigte Dateien, Format **WebP** für alle.
- **265** einzigartige referenzierte Bilddateien; **136** davon werden mehrfach verwendet, und **733** Hobbys nutzen diese mehrfach verwendeten Dateien.
- Alte HD007-Einträge nach vorliegendem Beweis: **24** `FINAL_MASTER_VERIFIED` Originale; **62** weitere Hobbys besitzen eigene genehmigte Design-Hobby-Master in HD003, die HD006 bereits nutzt; **776** allgemeine/geteilte Altzuordnungen sind **nicht** automatisch fachlich überprüft.
- Bildauflösung der **originalen HD007-Altverweise**: **24** mit mindestens 1500×1000 Pixel; **475** mit >=900×300 aber unter dem Mastermaß; **363** unter 900×300. **Keiner dieser Einträge wird bei der Prüfung ersetzt.** Moderne genehmigte HD003-Master können anstelle der Altverweise im Frontend stehen.
- Alte Herstellungskennzeichnungen: 519 `SEMANTIC_MASTER_REUSE`, 319 `EXACT_CURATED_CORE_CARD`, 24 `FINAL_MASTER_VERIFIED`. **„Datei vorhanden“ und „SEMANTIC_MASTER_REUSE“ sind nicht gleich „Bild passt“.**

**Bonsai-Landschaften** ist ein ausdrücklich belegter Einzelfall der 776: Operator-Screenshot zeigt ein fachlich passendes Miniatur-Landschaftsbild; der Originalpfad `hobby-depot-v150617/hero-masters-v150684/bonsai-miniatur.webp` stimmt exakt mit HD007 und dem HD003-Archiv überein. In 2.8.13 ergibt **nur dieses konkrete Bild** jetzt `Bild passt`. Änderung von Bildpfad oder Quelle führt wieder zu „Noch nicht geprüft“; eine explizite Nutzer-Ablehnung schlägt jede Vorfreigabe. Damit bleiben **775** allgemeine Altzuordnungen für visuelle Sichtprüfung offen. Diese Zahl ist ein **Archivinventar**, nicht der aktuelle Live-Bewertungszähler mit gespeicherten WordPress-Nutzerentscheidungen.

## Keine Ersetzungen ohne Einwilligung
- Alle 862 alten zugewiesenen Dateien bleiben unverändert und werden nicht automatisch nachgeneriert.
- Originalbilder, 24 HD007-Finals, 62 HD003-Master und bereits manuell bestätigte Bilder haben Vorrang vor generischem Altmaterial.
- Neue Bilder kosten ggf. Geld und werden nur durch bewusste Nutzeraktion erstellt. Übernahme nur ausdrücklich und erst nach Abgleich mit tatsächlichem HD007-PHP-Frontend-Aufruf; bei Fehlschlag bleibt das Original erhalten und der fertige Entwurf erneut verfügbar.
- **HD003 Designplugin, HD007 Registerplugin, Kategorien-/Hero-Layouts und Pferdeatelier/K0 wurden nicht geändert.** Keine neue Tabelle oder zweite Datenbank eingeführt.

## Hero-Grundprompt (nur HD006 Hobbyregister)
Der frühere Foto-Grundprompt erzeugte bei Arduino eine enge Nahaufnahme, deren entscheidende Tätigkeit im flachen breiten Hero kaum zu erkennen ist. 2.8.13 ergänzt verbindlich:

- Umwelt/Arbeitsplatz weiter, aber nicht so weit, dass Tätigkeit und Gerät winzig werden.
- Wichtigste Tätigkeit samt Werkzeug innerhalb der **mittleren 35–65 % Bildhöhe**, da das 3:2-Foto im Hero oben/unten stark beschnitten wird.
- Motiv leicht rechts der Mitte (**55–80 % der Bildbreite**) und links **35 % ruhiger Hintergrund** für den überlagerten Titel.
- Kein extremes Makro, keine abgeschnittenen Hände/Geräte; eine zusammenhängende fotorealistische Szene; eigener deutscher Motivwunsch und explizite Ausschlüsse bleiben vorrangig.
- Provider erhält weiterhin 3:2 / 2K, native 1500×1000 WebP-Master; keine Änderung an Fremdplugins.
- **Nicht bestätigt:** Ein echtes neu erzeugtes Magnific-Bild nach 2.8.13 oder dessen Qualität im Live-Hero. Nur die Prompt-Konstruktion und die Übergabe an den simulierten Anbieter wurden geprüft.

## Beweise, Tests, Ablage
`Bildzentrale-2.8.13.zip`: **86.359 Bytes**, SHA256 **96979106181f8d488e3cc124c9c46d9834494be08f18828c266331db2ed4045a**, genau 2 PHP-Dateien. PHP-Syntax und ZIP-Integrität bestanden. 123/123 Backend-, 27/27 Menü-, 39/39 Chromium-Browsertests bestanden, **erneut aus frisch entpacktem eigenständigem Testpaket**.

**Aktueller vollständiger Plugin-ZIP-Bestand + Zwischenprotokoll + Testarchiv + CURRENT** befinden sich in der persönlichen Library **`/Hobby Depot/Plugin-Büro/`**. Diese GitHub-PR speichert ausschließlich die dokumentierte Verbindlichkeit und den getrennten, nur lesenden Audit-Workflow; **keine Binär-ZIP auf GitHub behauptet**.

**Nächster Schritt:** Nach Installation 2.8.13 zuerst „Bonsai-Landschaften“ auf die bildspezifische Bewertung prüfen; bei Bedarf einen echten Arduino-Bildauftrag bewusst starten und den sichtbaren Hero-Zuschnitt beurteilen. Die 775 übrigen Altbilder in thematisch geordneten Prüfpaketen visuell beurteilen, ohne automatische Ersetzung oder ungerechtfertigte Positivfreigabe.
