# Wassertechnik W9 – bestehendes WT001 um einmaligen Import erweitert (nur Testkandidat)

**Stand 14.11.2026. Kein WordPress-Schreibvorgang ausgeführt.**

## Ergebnis
- Die bisherige, belegte WT001-Version **0.1.4** bleibt unverändertes Archiv und weiterhin Ausgangsbasis der erfolgreich abgeschlossenen SEO-Fortsetzung.
- Neue ZIP **`WASSERTECHNIK_KATEGORIE_WORKFLOW_0.1.5_IMPORT_NUR_TEST.zip`**: gleiche WordPress-Pluginidentität `wassertechnik-kategorie-workflow`, dieselben bestehenden Inventur-/DataForSEO-/Recherchemodule unverändert übernommen. **Keine zweite Pluginlinie**.
- Eine neue Klasse **`includes/class-wassertechnik-import.php`** ergänzt genau den Hauptfunktionsblock für die 218 vorhandenen W6-Ziele.
- Gebündelte W6-Importliste **`assets/wassertechnik-wp-import-plan.json`**: genau **113 WP-Seiten** (8 Haupt, 19 Gruppen, 1 Industriehub, 6 Industrielandings, 79 konkrete Produktseiten) und **105 WP-Beitragskategorien**. Fachzuordnung zu konkreter Produktseite bleibt erhalten.
- Das Plugin bietet im Backend einen separaten Punkt **W4-Strukturimport** mit einer schreibfreien Vorschau. Ausschließlich die bestätigende Admin-Aktion auf `wasser.oliver-beil.de` kann danach einen einmaligen ADD-only-Import auslösen. Keine automatische Anlage bei Aktivierung.
- Sämtliche neuen Produktseiten werden **als Entwürfe** angelegt. Keine Veröffentlichung, keine 356 Artikel, kein Journal/HivePress/Designimport. Produktbezogene Kategorien erhalten eine stabile Zuordnung zur Produktseite, keine zusätzliche Seitenebene im Mega-Menü.
- Ein gemeinsamer Bestandsabgleich entscheidet vorhandene/fehlende/konfliktbehaftete Seiten und Kategorien. Kollidierende, nicht zugeordnete Objekte bleiben unberührt. Neue Seiten werden in Eltern-vor-Kind-Reihenfolge erstellt. Vorhandene Standardinhalte werden nicht gelöscht.
- Bei neu auftretendem Fehler werden **ausschließlich im laufenden Vorgang neu erzeugte** Kategorien und Seiten zurückgenommen. Bereits früher vorhandene oder importierte Objekte werden nicht gelöscht.

## Einmalige Gesamtprüfung des Kandidaten
1. ZIP-Struktur aus allen acht Dateien erzeugt und auf Einträge, Größen und gespeicherte CRC-Werte geprüft: **PASS**.
2. W6-Importliste aus unverändertem W6 exportiert: 218/218 Owner, 113/113 Seiten, 105/105 Kategorien, alle Eltern-/Produktpfade vorhanden, keine doppelte Kategorie-Slugzuordnung: **PASS**.
3. Neuer PHP-Importer lokal mit PHP-Syntaxprüfung: **PASS**.
4. Ein integrierter PHP-WordPress-Mock mit denselben 113/105 Strukturobjektanzahlen: 
   - Normaler Lauf: 113 Seiten + 105 Kategorien angelegt, Standardobjekte erhalten: **PASS**
   - Nach bereits erfolgtem Import: 0 neue Seiten/Kategorien: **PASS**
   - Fehler bei 17. Kategorie: zuvor in diesem Lauf erzeugte 113 Seiten + 16 Kategorien zurückgenommen, Standards erhalten: **PASS**
   - Falsche Zielwebsite: 0 Änderungen: **PASS**
   - Konflikt mit bestehendem Pfad: 0 Änderungen: **PASS**
   - Geänderte Importvorlage nach Vorschau: 0 Änderungen: **PASS**.
5. Der echte Live-Betrieb auf WordPress, ein aktueller WordPress-Readback und die Anzeige im wirklichen Desktop-/Mobil-Mega-Menü sind **NICHT** getestet. Es gibt weiterhin **keine Schreibfreigabe**.

## Nächster gebündelter Praxisschritt
**Erst nach ausdrücklicher Freigabe**: die neue Version im bereits bestehenden Wassertechnik-Plugin auf der gebundenen WordPress-Testseite aktualisieren, einmal die Gesamtvorschau prüfen, nach separater ausdrücklicher Importfreigabe einmal ADD-only als Entwürfe anlegen, einmal echten WP-Readback prüfen. W7-Menübild erst bei sichtbarer Freigabe mit vorhandener Designsteuerung abnehmen. Nicht noch einmal Daten recherchieren, keine zweite Plugin- oder Prüfstruktur beginnen.

**Status: `W9_TESTZIP_ERSTELLT_OFFLINE_GEPRUEFT / WP_LIVETEST_OFFEN / WP_IMPORT_NICHT_FREIGEGEBEN`.**
