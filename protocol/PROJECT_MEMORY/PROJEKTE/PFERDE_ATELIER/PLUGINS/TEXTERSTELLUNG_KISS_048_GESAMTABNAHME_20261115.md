# Pferdeatelier – Texterstellung KISS 0.4.8: gemeinsame Bereinigung und Gesamtsimulation

**Datum:** 15.11.2026. **Status:** lokal getestetes, vollständiges WordPress-TESTplugin, keine Produktionsfreigabe. Original-K0 und Live unberührt.

## Auslöser, tatsächlich aus echter WP-Diagnose
Die echte oliver-beil.de-Diagnose vom 15.11.2026 08:54 UTC belegt `MINI_CURRENT_PARKHOUSE_INCOMPLETE` durch alten Plan (`original_reader_reason=PSERC_PLAN_NOT_PROVEN_COMPLETE`, `PSERC_ACTIVE_PLAN_INCOMPLETE_OR_STALE`), obwohl `WORDPRESS`, `PSTE_PLAN`, `EDITORIAL_PLAN` vollständig waren; 1.034 Originalbestandszeilen, 61 bestehende Aufträge (1 FREI, 60 METADATEN_OFFEN), 20 Recherchebegriffe.

## Vertragsbereinigung ohne Neubau
- **Ein einziges Regal** `texterstellung_orders_v1`, eine redaktionelle Entscheidung einmal pro Phase, keine nachgelagerte fachliche Zweitentscheidung. Bestehende 61 Titel bleiben unverändert, insbesondere bei Wiederaufnahme.
- Bestehende Original-PSTE-Lesefunktion `PSTE_Mini_Workflow::readParkhausForMini()` verwendet im bestätigten KISS-Modus nur bereits gelesene WordPress-Beiträge, bisherigen PSTE-Keywordbestand und vorhandenes WordPress-Regal; gibt den eingefrorenen Bestand vor den alten `EDITORIAL_PLAN`, `PSERC_ACTIVE_PLAN`, `PPM679_EXISTING_EDITORIAL_RUNTIME`-Planabfragen zurück. Keine alte PSERC-Redaktions- oder Planfreigabe kann MINI blockieren; keine alte Quelle wird zusätzlich abgefragt.
- Konkurrierende WordPress-/PSTE-Aktionswege für direkte Kategorien/Titel, alte separate MINI-Rückläufe und der alte tägliche Neuzuordnungs-Cron im aktiven Pfad abgeschaltet. Originalrecherche bleibt aktiv, WordPress-Testseitenbestätigung zwingend.
- Vorhandene alte PSTE-FREI-Belege werden nur bei wirklich fehlenden Einträgen nachgezogen, nie zum wiederholten Urteil über 61 eingefrorene Titel.
- Fachliche MINI-Schritte `CATEGORY -> EDITORIAL -> TITLE` werden jeweils einzeln in exakt derselben WordPress-Regal-Charge gespeichert, nach Unterbrechung nur der fehlende Schritt übernommen. `BELEGT` muss einen Verweis aus der **bereits eingefrorenen** Originalbestandsaufnahme nennen (keine zweite Leseentscheidung). Neue Schaf-/Ziegen-/Wild-Keywords ohne Pferde-JA-Beleg werden nicht automatisch freigegeben.
- Bisherige **technische** originale PSERC-/PPM-Funktionen bleiben ausschließlich für die unverfälschte signierte K0-Platzbindung und den unveränderten WordPress-Entwurfsimport bestehen. Kein neuer PSERC-Redaktionsplan, keine Fachentscheidung aus PPM. Fehlt technische signierte Kapazität, bleibt nur der betreffende Artikel offen.

## Lokal WIRKLICH ausgeführte Simulation, keine Behauptung über echte WP/PPM
- 18/18: exakte 61 historischen Titel aus Benutzerdiagnose, 1.034 künstliche WordPress-Bestandsbeiträge, künstliche originale K0-Platzdaten, erneuter Download und K0-Übergabe.
- 13/13: neue JA-Keywords plus unerwünschter Schaf/Ziege/Wild-Begriff, Kategorie/Redaktion/Titel/Schluss-Import, Fehlreferenz blockiert nur ein Thema, kein erneutes Urteil nach Wiederaufnahme.
- 10/10: mit tatsächlichem gebündelten ORIGINAL `PSERC_System4_Import` und simuliertem WordPress-Rückspeicher: defekter Einzelartikel hält andere nicht auf, späterer Einzelimport, identische Rückgabe ohne zweiten Entwurf, geänderte Daten bleiben gesperrt, nie öffentlich.
- 3/3: WP-Plugin unbestätigt ist inert, Originalquelle wird nicht gestartet.
- 11/11: WP-Plugin bestätigt, Original-Recherchetreiber aktiv, alte Entscheidungs- und Cron-Hooks entfernt.
- 16/16: Original-PSTE **READY** inkl. gefälschter gültiger Migrationsquittung, ursprüngliches Recherche-AJAX aktiv, alte Titel-/Kategorien-Aktionen tatsächlich entfernt.
- 4 weitere Reader-Läufe bei altem, fehlendem, manipuliertem und validem histor. PSERC-Plan (je 1.034 WP-Beiträge): immer vollständiger KISS-MINI-Bestand ohne PSERC-Plan-Read und ohne Schreiboperation.
- Direkter WordPress-HTTP-Aktionshandler `txe_seo_export` bis `download` mit simulierten Quellen erzeugt eine vollständig dekodierbare **532.514-Byte-JSON-Datei mit 20 Themen**. ZIP-Dateikonsistenz PASS.
- **71/71** Funktions-/Startchecks, **117/117** PHP-Syntaxprüfungen; 173 Dateien in vollständiger WordPress-ZIP. Gegenüber 0.4.7 genau **2 PHP-Dateien und 1 README geändert, 170 Dateien byteidentisch**.

## Installations-Testartefakt / private Ablage
Texterstellung_KISS_0.4.8_TEST_ZIELVERTRAG.zip; SHA256 `5d93a65a0387063404c8f4c095a063220ee4bd42ba969be8898e6d9999eaa929`.
Privates Büro: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung_KISS_0.4.8_TEST_ZIELVERTRAG.zip`. Der wieder heruntergeladene Büro-Upload wurde mit `cmp` bytegleich verglichen. Testbericht und Prüfprotokoll in gleichem Büro.
Pluginheader `0.4.8-kiss-contract-qa.1`, Root `texterstellung/texterstellung.php`, 173 Dateien, CRC und alle PHP-Dateien geprüft.

## Noch offen – klar abgegrenzt
Kein echter WordPress-/MySQL-Live-E2E auf `oliver-beil.de` durchgeführt. Kein echter signierter PPM-6.7.9-Slot und keine echte externe MINI/K0-Produktion durchlaufen. Nächster EINZIGER Test: Vollständige 0.4.8 **nur auf getrenntem WordPress-Testsystem** an Stelle 0.4.7 installieren (nicht löschen und 61 gespeicherte Aufträge nicht zurücksetzen), Menü `Texterstellung -> Redaktionsplan`, Feld `Themen pro MINI-Auftrag` 20, Button `MINI-Gesamtauftrag herunterladen`. Bei fehlendem Download genau eine neue Diagnose-JSON exportieren. Keine K0- oder Live-Veröffentlichung ohne diesen echten Nachweis.

`production_release_allowed=false`, `real_wordpress_end_to_end_passed=false`.