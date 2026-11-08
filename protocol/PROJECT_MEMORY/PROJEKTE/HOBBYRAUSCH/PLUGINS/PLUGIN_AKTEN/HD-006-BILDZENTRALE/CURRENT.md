# HD-006 – HOBBY DEPOT BILDZENTRALE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-08
STATUS: **2.8.13 IST DER AKTUELLE VOLLSTÄNDIGE LOKALE INSTALLATIONSKANDIDAT. LOKALE POSITIV-/NEGATIVTESTS PASS; 2.8.13-WORDPRESS-LIVE UND ECHTER HERO-PROMPT OFFEN.**

## Aktuell: Bildzentrale 2.8.13

- Vollständige WordPress-Plugin-ZIP **`Bildzentrale-2.8.13.zip`**, **86.359 Byte**, SHA256 `96979106181f8d488e3cc124c9c46d9834494be08f18828c266331db2ed4045a`.
- Die **Voll-ZIP, das Zwischenprotokoll und das reproduzierbare Testpaket** sind in der dauerhaften persönlichen Library **`/Hobby Depot/Plugin-Büro/`** gespeichert. Sie liegen **nicht als Binärdatei auf GitHub**.
- **Systematisches Read-only-Audit aller 862 HD007-Einträge** direkt gegen die HD007- und HD003-CURRENT-Originalarchive: 862 vorhandene und lesbare Bilder, 0 fehlende oder beschädigte Dateien, 265 verschiedene WebP-Dateien, 733 Hobbys teilen sich 136 Fotodateien. Von den bisherigen Zuordnungen sind 24 explizite HD007-Finals und 62 eigene HD003-Master; 776 weitere Fotozuordnungen benötigen weiterhin eine separate Motivprüfung. **Bonsai-Landschaften** ist von diesen als einziges jetzt zusätzlich durch den vorgelegten Screenshot und seinen exakt verifizierten Originalpfad als passend bestätigt; 775 verbleiben im **geschützten** Altbestand, ohne pauschale Freigabe oder Ersetzung.
- **Neue Hobbyregister-Hero-Komposition:** Kamera weiter weg; Hobby, Hände und Werkzeuge zusammen erkennbar; wichtige Elemente in mittlerer Bildhöhe (35–65 %) und rechts der Mitte (55–80 %) wegen flachem Hero-Zuschnitt und links überlagertem Titel; kein Makro/kein unlesbar kleines Motiv. Gilt sowohl mit als auch ohne eigenen Motivwunsch.
- Vorhandene passende Bilder **bleiben**. Jede Bewertung hängt an exakter Bildidentität, frühere Ablehnungen des Nutzers haben Vorrang, neue Bildaufträge bleiben bewusst und kostenpflichtig, nur ausdrückliche Übernahme ersetzt das aktuelle Foto. Keine Änderung an HD003/HD007, Bilddateien, Pferdeatelier/K0.
- **Lokal positiv und negativ geprüft:** **123/123 PHP-Backendtests**, **27/27 WordPress-Menütests**, **39/39 Chromium-Klicktests**, komplett erneut aus frischem Testpaket. 2/2 PHP-Syntax; ZIP-Integrität PASS. Es wurden lokale WordPress-/Bildanbieter-Mocks genutzt, **kein echter WordPress-Livetest von 2.8.13**.
- Bildübernahme unter 2.8.12 wurde vom Nutzer am Arduino-Hobby live bestätigt; **neue Hero-Prompt-Wirkung in 2.8.13 noch nicht live beurteilt**.
- [Verbindliches 2.8.13-Auditprotokoll](./BILDZENTRALE_2.8.13_BESTANDSAUDIT_UND_HERO_PROMPT_20261108.md). Ältere 2.8.8–2.8.12 bleiben Archiv.

---

## Historischer Stand (nicht mehr Current)

## Aktueller Pluginstand: Bildzentrale 2.8.12
- **Voll-ZIP**: `Bildzentrale-2.8.12.zip`, 85.492 Byte, SHA-256 `75b9b54b5956be86ca8c672c51da2231bba6956bf63eac2d55eb811a348ca73c`. Zwei vollständige PHP-Dateien; PHP-Lint und ZIP-Integrität PASS.
- **Dauerhafte Dateien:** vollständige ZIP, lokales Prüfprotokoll und wiederholbares Testpaket in der ChatGPT-Library `/Hobby Depot/Plugin-Büro/`. Die binäre ZIP ist **nicht im GitHub-Repository** gespeichert.
- **Ursache 1:** HD007 1.2.21 hat für Airbrush, Aeroponik und Batik alte allgemeine Platzhalter. Im unveränderten HD003 1.50.803/804 liegen bereits ausdrückliche Original-Master/Zuordnungen. HD006 2.8.12 fragt die bestehende HD003-Bildzentrale **nur lesend** für denselben exakten Hobby-Slug ab, akzeptiert nur belegte Bildquellen (`bildzentrale`, `hobby-master`, `hd007-master`, `batik-master`) und führt sie über den auf das HD007-Hobbyregister begrenzten Filter in dieselbe Bildausgabe. Bereits verifizierte HD007-Master bleiben unverändert. Keine Vermutungen aus ähnlich benannten Bildern.
- **Ursache 2:** In 2.8.11 testete die Übernahme nur einen simulierten Frontend-Aufruf ohne echten Bildfilter. Neu 2.8.12: Nach der ausdrücklichen Zustimmung muss die **aktive PHP-Bildauflösung von HD007** genau die neue Master-URL zurückgeben. Nur dann wird der Auftrag als angewendet markiert. Bei absichtlich unterbrochenem Bildfilter ist die Übernahme ein sichtbarer FEHLER, der ursprüngliche Master und der bezahlte Entwurf bleiben erhalten; erneute Übernahme möglich. Auch Undo geprüft.
- **Bestehende Regeln bleiben:** Bilderzeugungsplugin heißt **Bildzentrale**, separates Plugin **Bilder zuordnen** mit unterschiedlichen URLs. Motivwunsch beim Bildanbieter vorrangig. Drei Bewertungen; alle Master bearbeitbar; altes Bild bis zur bestätigten Übernahme unverändert; keine zweite Starttaste.
- **Prüfungen:** **103/103** Backendtests; **27/27** WordPress-Menütests; **35/35** echte Chromium-Klicktests. Die Testnachweise wurden zusätzlich frisch in einen **zweiten sauberen Ordner** entpackt und alle drei Testläufe wiederholt – PASS. Backend benutzt die echte 2.8.12-PHP-Datei, aber eine WP-/HD003-/HD007-/Provider-Simulation. Originale HD003-/HD007-Bildzuordnungen separat aus deren aktuellen GitHub-Artefakten hart geprüft.
- **Freigabegrenze:** **kein WordPress-Live-PASS, kein echter kostenpflichtiger Magnific-Bildtest, kein Nachweis für Browser-/Seiten-Cache auf der Live-Webseite**. Keine Live-Wirkung behaupten. **HD003 Design-Plugin, HD007 Originalplugin und alle Bestandsdateien sind UNVERÄNDERT.**

[**Verbindliche 2.8.12-Prüfakte**](./BILDZENTRALE_2.8.12_PRUEFVERTRAG_20261108.md). Frühere 2.8.8–2.8.11 sind historisch, nicht Current.

---

## Historische frühere Fassung (nicht als aktuelle Installationsanweisung verwenden)

## Aktuelle vollständige Installationsdatei – 2.8.11

`Bildzentrale-2.8.11.zip` – **84.425 Bytes**, SHA-256 `e13f79ee28d8996458f452de55973f0f75c05f2b09153b935caa3cee1af1f952`. Zwei vollständige PHP-Dateien, ZIP/PHP-Syntax PASS. **ZIP und Prüfbelege dauerhaft in der persönlichen Library** unter `/Hobby Depot/Plugin-Büro/` gespeichert. Keine Behauptung, dass die binäre ZIP bereits im GitHub-Repository liegt.

**Pflichtvertrag:** [BILDZENTRALE_2.8.11_PRUEFVERTRAG_20261108.md](./BILDZENTRALE_2.8.11_PRUEFVERTRAG_20261108.md)

- Erstellungsplugin = **Bildzentrale**; separates Zuordnungsplugin = **Bilder zuordnen**. Unterschiedliche URLs und Click-Callbacks.
- Manuell formulierter Motivwunsch hat **Vorrang vor Alttexten/Fotomotiven**; „Freunde beim 3D Bogenschiessen. kein tier!“ wurde mit hartem Tier-/Wildschwein-/Jagd-Ausschluss an den simulierten Magnific-POST geprüft. Jede geänderte Eingabe ergibt eine andere vollständige Prompt-Anfrage.
- Echte freigegebene `FINAL_MASTER_VERIFIED`/DONE-Originale des **HD-007 1.2.21** werden nur bei identischer Bildquelle als **„Bild passt“** erkannt. Beispiel **Airbrush-Modellbau**. Andere vorhandene Fotos werden NICHT pauschal freigegeben; sie bleiben **„Noch nicht geprüft“**, bis beurteilt.
- **Batik:** Die eigene Batik-Kategorieseite verwendet einen anderen Hero-Bildpfad als das Hobbyregister. Bildzentrale zeigt das tatsächlich im Hobbyregister verwendete Foto; sie darf die beiden Quellen nicht ohne Bestätigung gleichsetzen. Abgleich mit dem Live-Hero ist noch offen. Designplugin ausdrücklich unverändert.
- Ausdrückliche Bildübernahme, Erhalt vorhandener Bilder, Foto-für-Foto-Bewertungen und Bearbeitung bereits freigegebener Master weiterhin bindend.
- **Frisch wiederholt:** 86/86 Backend, 27/27 Menüs, 31/31 Chromium-Klicktests PASS. Die Tests verwenden simulierte WordPress-/Magnific-Aufrufe, **keinen echten kostenpflichtigen Serverlauf**.
- `2.8.10` sowie ältere Installationshinweise sind **historisch**, nicht mehr Current.

**Exakt nächster Schritt:** 2.8.11 in WordPress installieren, ohne HD003/HD007 zu ersetzen, und EINEN Hobbyregister-Bildauftrag mit abweichendem Motivwunsch einschließlich Ergebnisübernahme auf der echten Site kontrollieren. Erst danach Live-PASS.

---

## Älterer Stand 2.8.10 – nur Archiv / kein aktueller Installer

## AKTUELLER LOKALER INSTALLATIONSKANDIDAT: 2.8.10

**Installation:** `HOBBY_DEPOT_BILDZENTRALE_2.8.10_EINFACHE_BEDIENUNG.zip`
**Größe:** 83.745 Bytes
**SHA-256:** `09c5fbfd113c1e0fa0d6552c473b5ef5d1b0f1150adddce10090291ce097227f`

- Vollständiges Bildzentrale-Plugin, 2 PHP-Dateien; ZIP/PHP-Syntax PASS.
- **Die Bilderzeugung heißt „Bildzentrale“** und bleibt unter `admin.php?page=hdbz-bilder-erstellen`.
- Die getrennte, ältere Bildzuordnungsoberfläche heißt **„Bilder zuordnen“** und bleibt unter `admin.php?page=hobby-depot-bildzentrale`. Beide URLs sind verschieden, unabhängig von der Registrierungsreihenfolge.
- Für ein Hobby: Bild ansehen, **genau eine** redaktionelle Bewertung (Noch nicht geprüft / Bild passt / Bild passt nicht), optionaler Motivwunsch, **Bild erstellen**.
- **Ein Klick auf „Bild erstellen“ startet den tatsächlichen Bildauftrag nach ausdrücklicher Kostenbestätigung; keine unsichtbare Warteschlange und kein zweiter Auslöser.**
- Jeder vorhandene Master bleibt bearbeitbar. Vorhandene Fotos bleiben erhalten, bis ein neuer Entwurf mit **Bild übernehmen** ausdrücklich aktiviert wird.
- Entwürfe werden als eigene, noch nicht zugeordnete Mediathekdateien für die Vorschau geprüft; Fehler und fehlgeschlagene Downloads sichtbar, kein heimlicher Ersatz. Rücknahme/Verwerfen betrifft ausschließlich nicht übernommene Entwürfe.
- **Lokale Regression:** 65/65 Backend, 27/27 Menü und 21/21 echte Chromium-Klicktests, gerenderte Oberfläche mit 862 Hobbys.
- **Grenze:** Test gegen lokale WordPress- und Provider-Simulation; kein echter Live-WordPress-/kostenpflichtiger Provider-PASS. Vollständige ZIP liegt im aktuellen Chat bereit, aber eine byteidentische Kopie im Campus-Pluginbüro ist **noch offen**.
- **Ausgenommen:** Design-Plugin HD003 und Kacheldarstellung „Drachen & Leinen“ sind ausdrücklich angehalten und unverändert; ebenso HD007-Bestandsdaten, Pferdeatelier und K0.

**Pflicht vor allen künftigen HD-006-Updates:** [Verbindlicher Menüvertrag 2.8.10](./MENUE_VERTRAG_20261108.md) und [Prüfvertrag 2.8.10](./BILDZENTRALE_2.8.10_PRUEFVERTRAG_20261108.md) lesen; Titel, beide URLs, direkter Klick zur Bilderzeugung, drei Bildbewertungen, Schutz der Bestandsbilder und echte Klicktests positiv und negativ wiederholen.

---

## HISTORISCHE STÄNDE – NICHT ALS CURRENT VERWENDEN

## Historische Pflichtregel 2.8.8 (08.11.2026) – durch 2.8.10 im Menü-NAMEN ersetzt

**Vor jedem HD-006-Update zwingend lesen:** [MENUE_VERTRAG_20261108.md](./MENUE_VERTRAG_20261108.md) und die dort abgelegte reproduzierbare [Patch-Datei](./REPRODUKTION_2.8.8_MENU_FIX.py) sowie [Regressionstests](./MENU_REGRESSION_2.8.8.php).

**Fehlerursache:** Zwei verschiedene WordPress-Bildverwaltungen haben dieselbe Admin-Menüadresse verwendet. Eine reine Titelkorrektur ist verboten.

- **Bilder erstellen** (HD-006) → `/wp-admin/admin.php?page=hdbz-bilder-erstellen`.
- **Bilder zuordnen** (bestehende Zuordnung) → `/wp-admin/admin.php?page=hobby-depot-bildzentrale`.
- Beide Klickpfade müssen real verschieden sein; bestehende Zuordnung und API/Webhooks bleiben unverändert.

**Neu erstellter Installationskandidat:** `HOBBY_DEPOT_BILDZENTRALE_2.8.8_GETRENNTE_MENUES_UND_KLICKPFADE.zip` (SHA-256 `dd076c7772c820adcceabea85897a6bcfe79a47dd66430475b988d413541787a`). Lokal 27/27 Menüszenarien bestanden; Hobbyregister-Datei unverändert. ZIP aus Chatlieferung, kein eigener Download im GitHub-Pluginbüro bestätigt; ein WordPress-Livetest ist offen. **Nicht** zu alten 2.7.x-Installationskandidaten zurückkehren.

## Verifizierte Quelle

WPvivid-Pluginbackup:
`pferde-atelier.de_wpvivid-6e9ec6d805997_2026-09-24-11-08_backup_plugin.part001.zip`

Originaldatei:
`plugins/pferde-atelier-bildzentrale/pferde-atelier-bildzentrale.php`

Beweis:
- Version 2.7.6;
- 383603 Bytes;
- SHA-256 `984a8d4da6594ffa93e6d4024b57cc6c22c7d1fbfec398177a19b0490c20d89b`;
- exakte Übereinstimmung mit dokumentiertem Pferdeatelier-Source-Scan.

## Historischer Kandidat vom 20.10.2026 (nicht zur Neuinstallation)

`HOBBY_DEPOT_BILDZENTRALE_2.7.8_VERBINDLICHER_BILDPROMPT_INSTALLIEREN.zip`

ZIP SHA-256:
`d9d8caad4c2f4057fee30f9d21607376fa110d82defed8c0f759e5c202b83342`

Hauptdatei:
- 320401 Bytes;
- SHA-256 `edda98383add25fc2d02bf35bfff433b2c5ded332cc21a0fc43a82577e6004ec`.

## Korrektur

Der frühere Kandidat 1.0.0 war **nicht** aus dem echten Pluginquellstand abgeleitet und ist verworfen. Seine Library-Kopien im Bildbüro und Plugin-Büro wurden entfernt.

## Delta

Entfernt:
- pa_breed;
- kompletter Rassen-Batch;
- Rassen-Hero-Sonderprompt;
- Pferde-Motivcluster und Pferde-Such-/Alttext-/Fallbackregeln;
- feste ID 9120;
- Pferdeatelier-Admin-/REST-Slugs.

Angepasst:
- Hobby-Depot-Name/Slug;
- HDBZ-Namespace;
- neutraler Hobby-Prompt;
- acht Hobbywelten;
- Hobby-Depot-WordPress-/HivePress-Bildbindung.

Beibehalten:
- allgemeiner Originalkern; nach Namespace-Normalisierung 134 Funktionen unverändert.

## Bildprompt 2.7.8

- verbindlicher Hobby-Depot-Grundprompt;
- ruhige, nicht überladene Motive;
- Tätigkeit bevorzugt;
- Hände/Arme/handelnde Personen zur Verdeutlichung;
- Menschen nicht dekorativ;
- automatische Beitragsableitung aus Titel + Kurztext + bis zu 120 Wörtern Inhalt;
- Grundregel auch für Kategorie-, Hero- und HivePress-Prompts.

## QA

- PHP PASS;
- ZIP PASS;
- WordPress-Paketstruktur PASS;
- 0 fehlende Callbacks;
- 0 fehlende self-calls;
- 0 Pferde-/Rassen-/Horse-/Breed-/pa_breed-Literale;
- allgemeine Kernwege gegen Original unverändert PASS;
- lokaler Prompt-Positivtest 2874/3000 Zeichen PASS;
- 2.7.7 → 2.7.8 Funktionsdelta nur Prompt-/Themenableitung + Versionswert.

## Bildertrommel

Im verifizierten Original ist kein eindeutiger Code-/UI-Block dieses Namens belegbar. Daher wurde kein allgemeiner Weg auf Verdacht gelöscht.

## WordPress-Inventarabgleich 01.11.2026

Die vom Betreiber gelieferte vollständige WordPress-Pluginliste zeigt **Version 2.7.8 als aktiv**. Der zuvor dokumentierte Entwicklungs-/Teststand 2.7.8 ist versionsgleich, aber nicht dadurch funktional live-geprüft. Ein unabhängiger Server-Quellcode-/ZIP-Readback und ein Live-Funktionstest wurden in diesem Abgleich nicht ausgeführt. Keine Plugininstallation oder Campus-CURRENT.zip-Synchronisierung. Beleg: `../../EVIDENCE_WP_PLUGINLISTE_20261101.md`; operative WordPress-Current: `../../../WORDPRESS_TECHNIK/CURRENT_STATE.md`.

## EXAKT EINE NEXT ACTION (08.11.2026)

**Bei installiertem 2.8.8 im WordPress-Backend die getrennten Menüs „Bilder erstellen“ und „Bilder zuordnen“ mit ihren zwei verschiedenen URLs kontrollieren. Danach das geprüfte 2.8.8-Plugin-ZIP dauerhaft im Pluginbüro hinterlegen.**
