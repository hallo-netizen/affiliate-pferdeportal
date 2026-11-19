# Pferdeatelier – MINI-Texterstellung: Stand 19.11.2026, Fortsetzung

## Status, verifiziert
- Zuletzt sichtbare WordPress-Version: **Texterstellung 0.4.33 KISS** (Screenshot ca. 15:33 Uhr Europe/Berlin). Eine ältere Diagnose vom selben Tag zeigte 0.4.34; Versionen nicht vermischen.
- Aktiver gespeicherter MINI-Batch: `mini-20261119124823-5320a0031aff`.
- Aktuellster Nutzer-Wiederdownload: `texterstellung-mini-gespeicherter-auftrag(1).json`, 20 Originalthemen.
- **13 DONE (Indizes 0–12), 7 offen mit next=EDITORIAL (Indizes 13–19).** Davor waren 7 DONE, 13 offen.
- WordPress-Auftragsregal laut Screenshot: 67 Aufträge (37 IMPORTIERT, 25 METADATEN_OFFEN, 5 FREI). Zwei Pferdeanhängerartikel sind erfolgreich über K0 importiert, aber falsch kategorisiert.

## Nachweis der Unterbrechung / Ursache
- Diagnose `texterstellung-diagnose-20261119-143340.json`, `last_events`:
  - **14:28:56 UTC**: `txe_seo_import` EDITORIAL gestartet, Importdatei SHA256 `aed0e72dd9a3d74d738a364802157c35c0fb9991b421d862269c2d083cd6e581`.
  - Mehrere `STATE_COMMITTED`, aber vor dem nächsten Import **kein `ACTION_COMPLETED` für EDITORIAL**.
  - **14:29:27 UTC**: Zweiter Import TITLE gestartet, während für EDITORIAL noch keine Abschlussbestätigung protokolliert war.
  - **14:30:35 UTC**: TITLE abgeschlossen, 15 Einzel-HELD: bereits abgeschlossene Indizes 0–6 und 8 `MINI_FINAL_DECISION_ALREADY_COMPLETED`; offene 13–19 `MINI_WORKER_EDITORIAL_NOT_CHECKPOINTED`.
- Original-Code 0.4.33 `texterstellung/texterstellung.php` bei `miniWorkerCheckpoint` (ca. Zeilen 1403–1573): 20 Zeilen werden einzeln dauerhaft verarbeitet; TITLE erfordert zuvor gespeichertes EDITORIAL. Wiederholung desselben Checkpoints ist für noch offene Zeilen zulässig. Abgeschlossene Zeilen werden nicht überschrieben.
- **Sicher nachgewiesen:** EDITORIAL wurde nur teilweise gespeichert, Titelimport kam vor dessen belegtem Abschluss. **Nicht nachgewiesen:** ob Ursache des fehlenden Abschlusses Browserabbruch, Serverlimit oder etwas anderes war. Nicht raten.
- 0.4.33 blendet bei aktivem unvollständigem MINI-Batch neuen MINI-Export aus und bietet den Wiederdownload.

## KISS-Fortsetzung – keine neuen Plugins oder Recherchen
Die zwei bereits vorhandenen Rückgabedateien stimmen bezüglich ursprünglicher 20 Items, Reihenfolge und Source-Hash mit dem aktuellsten Nutzer-Wiederdownload überein; alte Daten werden nicht neu entschieden:
1. `MINI_EDITORIAL_KORREKTUR_2026-11-19.json`, SHA256 `aed0e72dd9a3d74d738a364802157c35c0fb9991b421d862269c2d083cd6e581`
2. `MINI_TITLE_KORREKTUR_2026-11-19.json`, SHA256 `8beb2338c9d0d0a44fd5a1bd083acc8ba064b31e78849dfe32a391b9f32adc62`

**Genauer Nutzer-Klickpfad:**
1. WordPress → Texterstellung → **MINI-Import** → Datei 1 **erneut importieren**. **Nicht zu Datei 2 wechseln, bevor WordPress die Abschlussmeldung „MINI-Arbeitsschritt EDITORIAL gesichert“ zeigt.** Bei nicht erscheinender Bestätigung oder Fehler: keine weiteren Importe, Bildschirm/Diagnose vorlegen.
2. Erst danach unter MINI-Import Datei 2 erneut importieren und deren Abschlussmeldung „MINI-Arbeitsschritt TITLE gesichert“ prüfen.
3. MINI-Export prüfen: neuer normaler Export sollte wieder verfügbar sein, wenn der alte Batch komplett DONE ist; sonst aktuellsten Wiederdownload ohne erneuten Eingriff hochladen.

**Besonderheit:** Die Importdateien müssen alle 20 ursprünglichen Zeilen enthalten. Das Originalplugin meldet bei Wiederimport bereits fertige Zeilen irreführend als Einzel-HELD/`MINI_FINAL_DECISION_ALREADY_COMPLETED`. Das ändert abgeschlossene Entscheidungen nicht. Relevant ist, dass Indizes **13–19** korrekt weiterlaufen. Die früher durchgeführte lokale Simulation mit Original 0.4.33 zeigte 20/20 DONE beim vollständigen Ablauf, ist aber keine Bestätigung auf Live.

## Sieben offene Themen und bereits vorbereitete Entscheidungen
13 „Soll man Pferde jeden Tag reiten?“ → FREI + Titel.
14 „Häufige Fehler bei der Fütterung“ → FREI + Titel.
15 „Ist Gurke gut für Pferde?“ → FREI + Titel.
16 „Leckstein für Pferde selbst machen“ (zweites ähnliches Thema) → KLAERUNG/Überschneidung mit Thema 10, kein neuer Titel.
17 „salzleckstein mineralleckstein pferd“ → BELEGT, bestehende Referenz WORDPRESS:973183, kein neuer Titel.
18 „mineralleckstein pferd krämer“ → FREI + Titel.
19 „Sind Minerallecksteine sinnvoll?“ → FREI + Titel.

Erwartetes Ergebnis bei komplettem Ablauf: 5 neue FREI-Aufträge, ein BELEGT, ein KLAERUNG; alle sieben im MINI abgeschlossen (KLAERUNG erzeugt bewusst keinen Artikel).

## Separater Fehler: Pferdeanhänger-Kategorien
- „Leergewicht und Zuladung beim Pferdeanhänger verstehen“, Beitrag 974848.
- „Was sollte ich beachten, wenn ich einen Pferdeanhänger miete?“, Beitrag 974849.
- Beide durch frühere Chat-Kategoriewahl in `recht-finanzen-organisation` eingeordnet; diese Entscheidung ist fachlich zu korrigieren. **Nichts in den Papierkorb verschieben oder rein manuell die Kategorie ändern**, weil WordPress-Beitrag, K0-Auftrag und gespeicherte Metadaten auseinanderlaufen können. Gesondert sicher prüfen, keine Doppelproduktion.

**Verbindliche Grenzen:** Kein Pluginwechsel, keine neuen Plugins, K0 nicht verändern, keine neue SEO-Recherche, aktiven Batch nicht löschen/zurücksetzen. Erfolg nur nach echten WordPress-Abschlussmeldungen/neuester Diagnose behaupten.


## Nutzer-Fortsetzung (19.11.2026, nach MINI-Import)
- Nutzer bestätigt: **beide empfohlenen Dateien erneut importiert („erledigt“) **.
- **Wichtig:** Es liegt noch **kein** neuer WordPress-Nachweis über vollständige Annahme oder 0 offene Themen vor; daher Status „20/20 DONE“ **nicht** behaupten.
- Angeordneter nächster Schritt: WordPress → Texterstellung → MINI-Export; prüfen, ob „MINI-Gesamtauftrag herunterladen“ wieder sichtbar ist. Falls weiterhin nur Wiederdownload: aktuellen gespeicherten MINI-Auftrag herunterladen und als JSON hier vorlegen.
- Kein erneuter Import oder Pluginwechsel bis zur Prüfung. Pferdeanhänger-Kategorien bleiben separat offen.


## Nutzer-Screenshot 19.11.2026 15:54 Europe/Berlin – MINI Sperre aufgehoben (visuell bestätigt)
- WordPress Texterstellung **0.4.33 KISS**.
- Unter `Texterstellung → MINI-Export` ist wieder der Button **„MINI-Gesamtauftrag herunterladen“** sichtbar; keine Auswahl für gesicherten MINI-Auftrag mehr. Damit nach zwei wiederholten Imports vorheriger MINI-Batch nach UI abgeschlossen, neue Exportfunktion verfügbar.
- Auftragsregal 72: **IMPORTIERT 37, METADATEN_OFFEN 25, FREI 10**. Davor 67: importiert 37, metadata offen25, frei5. **+5 FREI** durch erfolgreich vervollständigten MINI-Auftrag.
- KEINE zusätzliche Plugin-Installation für diese Korrektur. Alte Importdateien nicht erneut importieren.
- Noch offen: Zwei bereits importierte Pferdeanhängerbeiträge 974848 und 974849 fachlich richtige Kategorie (aktuell `recht-finanzen-organisation`) mit Redaktionsplan und Meta synchron abgleichen. NICHT in den Papierkorb verschieben, K0 nicht ändern, kein ungetesteter Eingriff.


## WICHTIGER Vertrags-/Implementierungswiderspruch (erneute Prüfung 19.11.2026)
- Tatsächliche Originalquelle: `ARBEITSBERICHT_C_VERTRAG_20261113.md` aus Pferdeatelier-Büro. **Dort steht:** PSTE/Redaktion trifft Portalrelevanz, Suchabsicht, FREI/BELEGT/KLÄRUNG, Kategorie und Artikelart vor MINI; MINI erhält fertig entschiedenen Auftrag und formuliert genau einen Titel; danach K0-Fünffelder-Auftrag.
- Späterer Prüf-/Änderungsstand: `MINI_KISS_WORKER_CHECKPOINTS_QA_STAND_20261114.md` führte eine Aufspaltung des einen MINI-Gesamtauftrags in **drei separat im WordPress-MINI-Import zu quittierende Stufen** CATEGORY, EDITORIAL, TITLE ein. `PFERDEATELIER-TEXTERSTELLUNG-0431-GESAMTPRUEFUNG-20261118.md` beschreibt ebenfalls getrennte Worker-Checkpoints.
- **Echter Quellcode Texterstellung 0.4.33 nachweisbar:** `TXE_Workshop::seoExport` (ca. Zeile 1138) setzt `worker_checkpoints_required=true` und `checkpoint_stages=['CATEGORY','EDITORIAL','TITLE']`. `miniWorkerCheckpoint` (ca. Zeile 1403–1573) verlangt Reihenfolge und speichert getrennt. `seoImport` (ca. Zeilen 1619–1641) weist einen vollständigen One-shot-Import ohne gespeicherte Einzelquittungen mit `MINI_WORKER_*_CHECKPOINT_MISSING` zurück.
- Aktueller Original-Export `texterstellung-mini-gesamtauftrag(3).json`, Batch `mini-20261119145601-8805d0573b96`: **10 Themen, alle next=CATEGORY;** nur `decision=JA` als vorgegebene Portalrelevanz, keine vorher gespeicherten FREI-/Titelentscheidungen.
- Schluss: **Das Anwenderziel „ein MINI-Export → eine komplett entschiedene Rückgabedatei → ein MINI-Import → K0-Export“ ist mit dieser Implementierung nicht erfüllt.** Unrichtig, den tatsächlich vorhandenen dreistufigen Ablauf als denselben ursprünglichen Zielvertrag auszugeben. 3 Imports sind Code-Verhalten, nicht Bestätigung des Zielvertrags. Für echtes One-shot wäre eine geprüfte Anpassung der bestehenden Implementierung nötig; kein erfundenes Importpaket ausgeben. Kein Live-Eingriff vorgenommen.
- Bestehender Nutzer-Auftrag: 10 Themen-Export vom 19.11.2026. Eine CATEGORY-Datei wurde im Chat erstellt; **kein vollständiger MINI-Durchlauf oder WordPress-Import dieser neuen Charge nachgewiesen**. Nicht als „fertig“ ausgeben.


## KISS-Verfahrensfix OHNE Plugin-Änderung (19.11.2026, lokal am Original-0.4.33-PHP getestet)
- Falsche frühere Idee „vor Ausgabe WordPress-Fertigmeldung verlangen“ ausdrücklich VERWORFEN; WordPress kann vor dem Nutzerimport selbstverständlich nichts bestätigen.
- **Neuer, praktisch nutzbarer Chat-Ablauf:** Nach EINEM MINI-Export alle vorgesehenen Entscheidungen für die gesamte Charge (CATEGORY, EDITORIAL, TITLE für FREI) vollständig in EINER Chat-Bearbeitung vorbereiten, die drei WordPress-Importdateien VOR Übergabe konsistent aus dem identischen eingefrorenen Export erstellen und gegen den unveränderten Original-PHP-Importer in der Reihenfolge simulieren. Erst danach alle Dateien gleichzeitig im Chat ausgeben, mit Reihenfolge 1/2/3 und nur bereits offene Worker bearbeiten. Kein Chat-Back-and-forth zwischen den Imports mehr. Die WordPress-Sperre bei neuen Aufträgen bleibt bestehen und ist nicht veränderbar durch einen Chatprompt; Nutzer muss die drei Importdateien nacheinander hochladen und jeweils Abschluss abwarten. Bei LEGACY_CATEGORY_ONLY ist nur CATEGORY nötig.
- Lokaler Originalcode-Test mit 10 wirklichen exportierten Zeilen und **QA-TESTentscheidungen**, nicht mit produktiv freigegebenen Titeln: Titel vor EDITORIAL wird für alle 10 abgewiesen; CATEGORY 10/10 gespeichert, EDITORIAL 10/10 gespeichert, TITLE 10/10 gespeichert, FINAL 10/10 DONE, 10 Test-K0-Aufträge, aktiver MINI-Batch leer. Zweiter Mischtest 1 FREI + 9 KLAERUNG: FINAL 10/10 DONE, 1 neuer Testauftrag; Titelcheckpoint zeigt irreführende HELD-Meldungen für bereits fertige neun Nicht-FREI-Positionen (bekanntes Originalverhalten), das keine neuen Entscheidungen erzwingt.
- Der Test war **isoliert** mit echtem TXE_Workshop PHP aus Original ZIP 0.4.33 sowie simuliertem WordPress-Optionstore; keine echte Live-WP-Importbestätigung und **kein** Beleg für fertig bearbeitete echte 10 Themen.
- Prüfbericht in Modell-Arbeitsbereich: `/mnt/data/MINI_KISS_1_CHAT_3_DATEIEN_PRUEFNACHWEIS_2026-11-19.txt`. Kein Plugin- oder K0-Eingriff.
- **VOR AUSGABE**: all-item completeness guard; unveränderte Originalfelder/Reihenfolge/Hashes; ausschließlich bestehende echte Kategorien, gültige K0-Artikeltypen; Übernahme von gesperrten Entscheidungen; keine neue Recherche; alle späteren Dateistufen in einer Nachricht, nicht nur Kategorie-Datei.


## 19.11.2026 16:49 Europe/Berlin – neuer Auftrag: MINI-KISS-Hartschranke + REWORK (vor Umsetzung protokolliert)
- Nutzer verlangt ausdrücklich **eine einzige technische Vollständigkeitsprüfung** vor Dateiausgabe, **kein Plugin-Umbau**, **keine zusätzlichen Fach- oder Doppelprüfungen**, und **keinen Abbruch bei nicht bestandener Prüfung**: nur fehlerhafte Teile an bestehenden Worker zur Korrektur, identische Entscheidungen gesperrt erhalten, dann an derselben Prüfstation erneut antreten.
- K0-Vorbild gelesen: `control/startmaster0106/TEXTPRODUKTION_NO_STOP_CONTINUITY_HARDLOCK_V1.json`: `backtrack_policy=DENY_UNLESS_CURRENT_GATE_EXPLICITLY_RETURNS_REWORK_TO_BOUND_PREDECESSOR`, `resume_policy` ohne PASS-Wiederholung; `control/deterministic-entrance-gate/README.md`: fachblinde technische Schicht. Für MINI keine zweite SEO-/Titelprüfung.
- Zuletzt hochgeladener MINI-Gesamtauftrag `texterstellung-mini-gesamtauftrag(3).json`, Batch `mini-20261119145601-8805d0573b96`, 10 Themen, `next=CATEGORY` bei allen; Kategorie-Datei bereits ausgegeben; EDITORIAL/TITLE für diese Charge noch nicht vollständig nachgewiesen. Keine Erfolgsmeldung, keinen Live-Import annehmen.
- Zielimplementierung: **einziger vor-export Release-Gate** in separater CLI/Workflow-Schicht. Originaldatei + drei vorhandene Worker-Quittungen werden nur auf Vollständigkeit und unveränderte Batch-Identität geprüft, nicht fachlich erneut beurteilt. Bei Fehler `REPAIR_REQUIRED` mit präziser Item/Stufe und Wiederaufnahme derselben Charge. Ausgabedateien nur im freigegebenen Release-Verzeichnis nach PASS. WordPress-/K0-Plugins bleiben unverändert.
- Nach Bau Testbelege und exakte GitHub-Quelle hier ergänzen, keine ungetestete 100%-Garantie behaupten.


## 19.11.2026 16:49+ – KISS-Einzel-Ausgabegate und Reparaturschleife tatsächlich implementiert und geprüft
- **Ablage in GitHub Zweig `affiliate-release-current`**: `control/mini-output-gate/mini_release_gate.py`; daneben `README.md`, `test_mini_gate.py`, `fixtures/MINI_TEST_ORIGINAL.json`, `fixtures/MINI_TEST_CATEGORY.json`, `PRUEFBERICHT_2026-11-19.md`, `TESTLAUF_ECHTE_10_THEMEN_2026-11-19.log`.
- **Ablage auch im Pferdeatelier-Büro** `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` als MINI_KISS_RELEASE_GATE_V1.py und begleitende Tests/Protokolle. Das ist **kein WordPress-Plugin**, nichts installiert oder verändert.
- **Genau eine technische Prüfung vor der Dateiausgabe**, kein zweiter Kategorie-/SEO-/Titel-Checker. Die fachlichen Entscheidungen bleiben allein bei den bestehenden MINI-Workern/WordPress.
- Ursprungsdatei in einem lokalen Arbeitsraum SHA256-gebunden; Worker-Dateien müssen Batch-ID/Quellfingerabdruck, vollständige unveränderte Item-Reihenfolge und je nach Zustand vorhandene Pflichtentscheidungen enthalten; alte gesperrte Entscheidungen nicht neu festlegen.
- Bei fehlenden Feldern, falscher Quelle, fehlender Stufe: **`REPARATUR.json` mit exaktem Keyword, Item und zuständigem Worker**, Status `REPARATUR`. Keine Dateiausgabe. Bestehende Worker-Dateien und Original bleiben erhalten. Nach gezielter Worker-Korrektur **dieselbe** Gate-Funktion aufrufen, keine Doppelprüfung, kein Workflowreset.
- Bei PASS: aus dem einzigen technischen Gate `FREIGABE/CATEGORY.json`, `FREIGABE/EDITORIAL.json`, `FREIGABE/TITLE.json` (nur für benötigte Stufen), `FREIGABE/NACHWEIS.json` mit SHA256, Batch/Item-Zahl, erkennbar **vor** WordPress-Import.
- **7/7 lokale Python-Regressionstests bestanden, zweimal**, einmal mit portablem gekürztem 10-Themen-Testfixture und einmal mit dem tatsächlich hochgeladenen vollständigen MINI-Export plus CATEGORY-Datei. Enthalten: nur CATEGORY => REPARATUR; TITLE fehlt => REPARATUR; Korrektur derselben Position => PASS ohne Reset; manipulierte Quelle => REPARATUR; falsche Batchkennung entfernt alte Freigabe; Ursprung unveränderlich; LEGACY_CATEGORY_ONLY => nur CATEGORY.
- Tatsächlicher aktueller MINI-Batch `mini-20261119145601-8805d0573b96`: **10 Items, CATEGORY vorhanden, EDITORIAL und TITLE fehlen**. Die neue technische Sperre hat an echten Eingangsdateien **REPARATUR (EDITORIAL) und keinen Freigabeordner** geliefert. Für diesen Batch wurde **keine neue Redaktion/Titel-Produktionsdatei erfunden oder veröffentlicht**. Noch keine Live-WordPress-Freigabe.
- **Grenze:** Die Sperre kann die von ihr ausgegebenen Freigabedateien schützen, aber nicht systemweit verhindern, dass ein Chatbot sie absichtlich umgeht und andere Dateien verlinkt. Verbindlich ist daher nur der Freigabepfad des Gate-Skripts, nicht eine unbeweisbare 100%-Plattformgarantie.


## Endabgleich MINI-KISS-Gate – 19.11.2026, nachgezogener Doppelentscheidungs-Schutz
- Endversion `control/mini-output-gate/mini_release_gate.py` nachgeschärft: Hat der gespeicherte MINI-Auftrag für ein Thema bereits Kategorie, Redaktion, Titel oder DONE, dann darf ein neues Ergebnis diese bereits gespeicherte Entscheidung **nicht noch einmal in der Rückgabedatei einreichen**; andernfalls `REPARATUR` statt Upload-Freigabe.
- **9/9 Tests bestanden** mit gekürztem 10-Themen-Fixture **und 9/9 mit vollständigem echten 10-Themen-Original samt bestehender CATEGORY-Rückgabe**. Zusätzlich nachgewiesen: bereits gesicherte Kategorie und DONE-Zeilen können nicht erneut entschieden werden.
- Für die tatsächlich aktuelle Charge liegt nur eine CATEGORY-Datei vor. End-Gate hat auf unverändert gebundenem Original `status=REPARATUR`, `next_worker=EDITORIAL`, `pending=10`, `release_available=false` ausgegeben. Es gibt ausdrücklich **keine** freigegebenen produktiven MINI-Rückgabedateien und keine behauptete fertig geschriebene Redaktion/Titel.
- **Keine Plugin- oder K0-Datei verändert.** Alle Dateien, Tests und Belege unter `control/mini-output-gate/` in GitHub sowie im Pferdeatelier-Büro gesichert. Fortsetzung für nächsten Chat: offene EDITORIAL und TITLE fachlich nach bestehendem MINI-Workflow erstellen, dieselbe eine Ausgabeprüfung/REWORK laufen lassen, nur bei PASS aus `FREIGABE/` liefern.


## 19.11.2026 – laufenden 10-Themen-MINI-Auftrag vollständig vorbereitet und am Original-PHP simuliert
- Original-Freeze: `texterstellung-mini-gesamtauftrag(3).json`, Batch `mini-20261119145601-8805d0573b96`, 10 Items und identischer `source_sha256`. Vorhandene `MINI_KATEGORIE_2026-11-19_BATCH_8805d0573b96.json` unverändert weiterverwendet; alle Kategorien existieren im eingefrorenen Katalog.
- Der **bestehende eine EDITORIAL-Worker** hat anhand des vollständig enthaltenen WordPress- und Auftragsbestands einmalig entschieden: 3 BELEGT mit echten eingefrorenen WP-Referenzen: `WORDPRESS:973183` (Mineral- oder Salzleckstein Vergleich), `WORDPRESS:973172` (Salzleckstein gut/schlecht), `WORDPRESS:973175` (Minerallecksteine Produktauswahl). 7 FREI mit unterschiedlichen Suchintentionen und 7 im bestehenden TITLE-Worker genehmigten FAQ-Titeln. Keine neuen Recherchen und keine doppelte Fachentscheidung.
- Release-Gate `control/mini-output-gate/mini_release_gate.py`: Status **FREIGEGEBEN_FUER_WP_IMPORTE**, 3 vorbereitete Dateien. Einzelreparatur zusätzlich mit realen Daten getestet: fehlender Titel bei Item 5 => **REPARATUR** ohne Freigabe; nach Titelkorrektur **PASS** für dieselbe Charge, keine Neurecherche.
- **Exakter Original-Plugin-Test** mit unverändertem `TXE_Workshop::seoImport` aus Texterstellung **0.4.33** und isoliertem WordPress-Speicher: CATEGORY 10 saved 0 held; EDITORIAL 10 saved 0 held, 3 DONE; TITLE 7 saved, 3 HELD mit `MINI_FINAL_DECISION_ALREADY_COMPLETED` für die **bereits durch BELEGT erledigten Positionen**. Gesamtergebnis **10/10 DONE**, **7 neue K0-Testaufträge inklusive gültiger Plan-Slots**, leerer aktiver MINI-Batch. Test `EARLY_TITLE` vor Kategorie/Redaktion: 10/10 korrekt abgewiesen. **Kein echter Live-WP-Import behauptet**. Regressionen 9/9 mit vollem Original bestanden.
- Fertiges Chat-Reimportpaket lokal **`/mnt/data/MINI_PFERDEATELIER_10_THEMEN_REIMPORT_2026-11-19.zip`**, SHA256 `8dbe6627e42a78ac38eb68f4cc0797664abb0ba97796d28136d27761e9a5aebe`. Inhalt `01_KATEGORIE.json`, `02_REDAKTION.json`, `03_TITEL.json`, `PRUEFNACHWEIS.json`, `ANLEITUNG.txt`. Bereits erfolgreich importierte Kategorie nicht erneut importieren. Redaktion und Titel in genau dieser Reihenfolge importieren, jeweils Abschluss abwarten. Anschließend WordPress-K0-Export mit 7 neuen freigegebenen Aufträgen prüfen.
- Echte Plugin-Freigabe, Produktionsdatenbank, WordPress-Import und K0-Export **noch nicht live nachgewiesen**; Testlauf ist lokal. Ein späterer Chat sollte für diese Batch-ID keine neue Kategorie-/Redaktions-/Titelentscheidung erzeugen, sondern den zuletzt bestätigten WordPress-Status prüfen und ggf. die bestehende REWORK-Schleife fortsetzen.
