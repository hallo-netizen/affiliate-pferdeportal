# Pferdeatelier eBay – QA11 / Plugin 6.72.322: Schlussprüfung, Fortsetzung, Backend-KISS

**Stand: 11.11.2026. Isolierte Test-ZIP, KEIN produktives Live-Release / kein CURRENT-Wechsel.** Grundlage ist die physisch vorhandene, bereits gesicherte 6.72.321-QA9-ZIP plus der vorliegenden QA10-Berichtsverschlankung. Kein Zugriff auf die produktive WordPress-Datenbank, keine produktiven Optionen bearbeitet, keine Recherche-/Produktdaten gelöscht. Die vorhandenen anderen Provider und Portal-Plugins unverändert.

## 1. Reales Fehlerbild (Nutzerscreenshot vom 11.11.2026, 09:44)

- Kanonischer Gesamtworkflow **Status: Fehlgeschlagen**, Fehler **`public_source_refresh_provider_failed`**.
- Öffentlicher letzter gespeicherter Nachweis **161/298**, **137 offene** Produktfamilien.
- **432 gespeicherte eBay-Freigaben** (kein Beweis von 432 sichtbar/aktuell verfügbaren Produkten).
- **548 Worker-Pakete**, letzter echter Fortschritt **05:53:43**; der Fehler trat an der letzten öffentlichen Quellenprüfung nach abgeschlossener BUSINESS-Auswahl auf.
- Angezeigt: eBay konnte einen ausgewählten Kandidaten vor der Veröffentlichung nicht bestätigen. **Der genauere Anbieter-/Artikel-Fehlercode ist auf dem Screenshot nicht zu sehen.**
- Gespeicherter öffentlicher Bestand laut Backend erhalten; keine pauschalen Löschungen.

## 2. Die nachgewiesene Ursache – am echten QA9-Code reproduziert

`includes/trait-ppar-ebay-run.php`, Methode `ebay_run_public_source_refresh_tick`:

1. Ein bereits ausgewähltes Produkt wird mittels **bestehendem** getItem-/Refresh-Pfad erneut kontrolliert.
2. Die eigentliche Refresh-Funktion schreibt bei einem individuellen HTTP-, Klassifikations- oder Qualitätsergebnis einen begründeten Einzelfehler in die vorhandene Arbeitspaket-Zusammenfassung.
3. Bei nicht temporären Fehlern löste der Schlussprüfungskoordinator **für den gesamten Run** `ebay_run_fail('public_source_refresh_provider_failed', ...)` aus, **bevor die restlichen Produktkandidaten geprüft wurden**. Die Ausnahme für vorübergehende Fehler beendete bei vorhandenem sicherem Checkpoint sogar die Schlussprüfung bereits beim ersten nicht erfolgreich erneut bestätigten Item.
4. Dieser Ablauf widersprach der bereits festgelegten KISS-Regel aus QA2/QA5 („ein Einzelfehler stoppt keine anderen Produktfamilien“). Die frühere Fehlerisolation war **in der Auswahlschleife**, aber **nicht vollständig im abschließenden öffentlichen getItem-Pfad** implementiert. Kein neuer Such- oder Synonymumbau nötig.

**Direkter Alt-vs.-Neu-Beweis** am Original-Trait: In QA9 führt Produkt 101 mit Fehler `ebay_refresh_http` dazu, dass Produkt 102 **gar nicht geprüft** wird und der ganze Run auf **failed** geht. In QA11 wird Produkt 102 trotzdem kontrolliert, und der Lauf endet mit ausdrücklich **offenen Quellenprüfungen**, nicht mit falschem Gesamt-PASS.

## 3. Minimaler KISS-Fix / Daten- und Sicherheitsgrenzen

- **Eine einzige bestehende finale Refresh-Methode angepasst:** Einzelne nicht bestätigbare eBay-Kandidaten werden **begrenzt und mit Code/Post-ID im bisherigen Laufzustand protokolliert**, nicht als verfügbare Produkte erfunden und nicht als eBay-Marktlücke klassifiziert. Die restlichen Produkte werden mit **maximal zwei echten Remote-Anfragen pro Tick** weiter geprüft.
- Bestehende Versuche für zeitweise Provider-Probleme bleiben **maximal zwei Wiederholungen pro Kandidat**. Ein tatsächlich ausgelöstes HTTP-`401`/`403` oder fehlender globaler eBay-Zugang bleibt **harter Zugangsfehler**. Fehlende DB-/Quellspeicherintegrität bleibt ebenfalls harter Fehler.
- Wenn ein Kandidat am Ende nicht bestätigt wurde, **kein neuer unvollständig geprüfter Gesamt-Checkpoint**. Der bisherige sichere öffentliche Checkpoint bleibt, soweit vorhanden, unverändert; pro Produkt greifen weiterhin die bestehende Sechs-Stunden-Frischegrenze, Ausverkauft-/Beendet-Prüfung und redaktionellen Qualitäts-/Marktplatzregeln. Noch nicht verifizierte Produkte werden **nicht** neu veröffentlicht.
- Abschluss nach isolierten Einzelfehlern wird als **`completed_with_skips` + `public_source_refresh_unverified`** und Warnung statt falsch „alles erledigt“ gespeichert. **Bereits von QA9 früh und individuell sicher freigegebene Produkte bleiben unabhängig davon sichtbar**, solange sie aktuell und fachlich gültig sind.
- **Gespeicherten fehlgeschlagenen Schlussprüfstand fortsetzen:** Bei exakt `public_source_refresh_provider_failed` aus `public_verify` kann derselbe Run via bisherigen Admin-Neustart-Formular-Endpunkt in **dieselbe letzte Phase** zurückgesetzt werden. UUID, Kandidaten, Unterphasen, Recherche-/Nachsuchverlauf, Prüf-Cursor, Quellen und sicherer Checkpoint bleiben. Der vorhandene Button heißt für diesen belegten Fall „Gespeicherte Schlussprüfung fortsetzen“. Andere Fehler benutzen weiter den bisherigen strengen Weg; keine automatische Datenmutation beim Seitenaufruf.
- **Backend read-only:** Die vorhandene 45-Sekunden-Statusabfrage darf auch bei 180 Sekunden Stillstand **keinen synchronen Worker mehr starten**. Stattdessen arbeiten die **bereits bestehenden** selbstgetriebenen Signatur-/Lease-/Heartbeat-Wege weiter. Keine zusätzliche Queue, Tabelle, Backendseite oder API.
- **QA10 übernommen:** Fehlende-Familien-CSV zeigt vier bereits gespeicherte Duplikat-/Prüf-/Kapazitäts-/Abschlussfelder zusätzlich, ohne die ursprünglichen elf Spalten zu ändern; der aufwendige Bericht wird im Backend erst auf ausdrücklichen Klick berechnet. Keine neue eBay-Suche.
- `X-EBAY-C-MARKETPLACE-ID: EBAY_DE` und der konsequente Herkunfts-/Sicherheitsfilter **unverändert**. Versicherungen / 26 Nicht-Waren und die bestehende begrenzte Suche unverändert.

## 4. Nachweis der fertigen ZIP und tatsächlichen Tests

**ZIP:** `Pferdeatelier_Affiliate_6.72.322_QA11_KISS_SCHLUSSPRUEFUNG_NUR_TEST.zip`  
**SHA256:** `c86fc0f46a0b69b1c8041453caf7a3665775ff53b92bc9fef373f65500889666`  
**Größe:** **5.361.052 Bytes**, exakt **66 Einträge**, ZIP-/CRC-Prüfung bestanden.  
**62/66 Dateien** gegenüber QA9 **byteidentisch**. Nur die beiden eBay-Trait-Dateien, Plugin-Hauptdatei und Readme geändert. WordPress-Plugin-Header, interne Version und `Stable tag` stimmen sämtlich auf **6.72.322**.

- **23/23** PHP-Dateien Syntax PASS.
- **61/61** bestehende Fachtests gegen **die QA11-Originalquellen** PASS (16 Auswahl, 13 Fehlerisolation, 11 Materialisierung, 10 Gesamtpfad, 11 dauerhafte Speicherung).
- **34** weitere PASS-Nachweise im originalen QA11-Schlussprüfungs-Trait, darunter Alt-Fehlerreproduktion auf QA9, per-item-failed + gesundes Folgeitem, 2x Timeout-Retry, echte Request-Obergrenze auch bei Fehlern, Auth 401 und fehlender Token, normaler alter Erfolgsweg, geschützter Checkpoint, kein neuer vermeintlich sicherer Bestand ohne vorherigen Nachweis, Wiederaufnahme **derselben UUID/Quell-Cursors** und bei Erstfehler ohne Cursor, falscher Fehler nicht fortsetzbar, read-only-Backend auch bei Stillstand.
- **12/12** zusätzliche Datei-Vergleichsszenarien QA9/QA11 der bestehenden Auswahl- und öffentlichen Coverage-Methoden identisch.
- **QA10-Berichte:** ursprüngliche Zahlen unverändert; 4 Zusatzfelder korrekt; 6 bedarfsabhängige Backend-Aufrufe geprüft.

Reproduzierbare Testskripte, Bericht, vollständiger QA9-vs.-QA11-Patch und Datei-Prüf-JSON sind im GitHub-QA-Zweig unter `protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/AFFILIATE/` bzw. `PLUGINS/EVIDENCE/` hinterlegt. Die physische **ZIP liegt in der persönlichen Library**, nicht als Binärdatei in GitHub.

## 5. Unveränderte Freigabegrenze und nächste reale Abnahme

**Nicht behaupten:** Dass 161/298 jetzt steigt, dass alle 432 Freigaben sichtbar sind, dass das Backend nachweislich schneller ist oder dass die einzelne Live-HTTP-/Klassifikationsursache identifiziert wäre. Die Tests verwenden den echten PHP-Quellcode, aber einen simulierten WordPress/eBay-Datenbestand. Ein echter WordPress-/MariaDB-/eBay-Gesamttest ist weiterhin nötig.

**Konkrete Testprüfung:** 6.72.322 nur auf einer **getrennten WordPress-Testinstallation mit gesichertem Run-Zustand** installieren. Backend muss gleiche Run-UUID und gespeicherte Abdeckung zeigen; für genau diesen bekannten Fehler muss statt des generischen Neustart-Knopfs „Gespeicherte Schlussprüfung fortsetzen“ angezeigt werden. **Einmal** auslösen: derselbe Lauf setzt ausschließlich die letzte Quellenprüfung fort, ohne erneute 298er-Recherche. Danach: kein Gesamtabbruch bei einem belegten Einzel-Item-Fehler, keine unkontrollierte Freigabe, eine richtige eBay-Kachel, und die normale Backend-Seite blockiert nicht wegen des Reports oder Status-Ticks. Erst nach realer Abnahme eine produktive Freigabe erwägen.

**Hobbydepot (HD-009) / Hab & Bewahr (HAB-004):** Diese Korrektur nur im zentralen Änderungsregister als fachlich nachvollziehbare Übertragungsreferenz aufführen, **keine** Fremdplugin-Installation/Übernahme ohne unabhängigen Quellvergleich, Tests und Freigabe.

## Reales Folge-Screenshot 11.11.2026 10:15

Nutzer zeigt neues WordPress-Backendbild zur **installierten 6.72.322 QA11**. Kanonischer Run mit derselben sichtbaren Kennung `ab9fd428-fac`, Status **Läuft**, Phase `public_verify`, Lease frei. Im vorigen Bild (10:09) **550 Pakete, Schritt 581**, im Folgefoto (10:15) **607 Pakete, Schritt 690**. Es wurden also **57 weitere Arbeitspakete und 109 weitere Fortschrittsschritte** angezeigt, ohne erkennbaren Rücksprung in `gapfill_discovery`. Letzter angezeigter echter Fortschritt 11.11.2026 09:13:58 (WordPress-Anzeige vermutlich abweichende Zeitzone zum Desktop; keine Stagnation daraus behaupten). **Öffentliche Gesamtabdeckung bleibt 161/298, 137 offen; 432 gespeicherte eBay-Freigaben**. Produktverfügbarkeitsstand 07:22 mit drei Prüfproblemen; im Foto kein Nachweis einer nachfolgenden Aktualisierung. **Diese Zahlen belegen Fortschritt der Schlussprüfung, nicht ihre Fertigstellung, neu verfügbare Produktkacheln oder gemessene Performanceverbesserung.** Keine Live-Daten oder Plugin-Quellen durch diesen Dokumentationsnachtrag verändert.

## NACHPRÜFUNG 11.11.2026 – Fehlerprotokoll im Backend NICHT vorhanden

**Berichtigung einer unzutreffenden früheren Zusage:** „Einzelfehler mit Code und Post-ID protokolliert“ bedeutet in Version 6.72.322 **nur interne Speicherung**, nicht ein für Betreiber sichtbares vollständiges Fehlerprotokoll. Dies wurde an der tatsächlichen fertigen QA11-ZIP, nicht nur am Patch, kontrolliert.

- In `includes/trait-ppar-ebay-run.php` schreibt `ebay_run_public_source_refresh_tick` bei Einzelproblemen in `$state['provider_error_samples']` lediglich maximal **12** Elemente mit `post_id` und `code` sowie den Zähler `provider_errors`. Der Zustand landet via `ebay_run_save` in der WP-Option **`ppar_ebay_run_state_v1`**. Darin liegt nur der **aktuelle Lauf**, keine append-only vollständige Diagnose aller früheren Läufe.
- `ebay_run_archive_terminal` archiviert in **`ppar_ebay_run_history_v1`** nur kompakte Laufmetadaten: Run-ID, status, phase, error_code, Zeit/Build, letzte allgemeine Provider-Fehlerkennung, Kurz-Zähler usw., begrenzt auf **10** Einträge. **`provider_error_samples` wird NICHT archiviert**.
- In `includes/trait-ppar-ebay.php`, `render_ebay_page`, wird bei `public_source_refresh_warning` lediglich die **Anzahl** problematischer Angebote und die unveränderte Sicherheit des alten Checkpoints angezeigt. **Keine sichtbare Liste der 12 Einzelcodes, kein Vorher/Nachher-Laufprotokoll, kein CSV-Export für diese Schlussfehler**.
- Der vorhandene Backend-Aufklapper **„Technische Details zum eBay-Abruf“** zeigt `$sync` aus dem gewöhnlichen Abruf, **NICHT** `$canonical_run['public_source_refresh']['provider_error_samples']`. „Technische Details zum Bestandsabgleich“ ist ebenfalls ein anderer gespeicherter Zustand.
- Bei einem **neu gestarteten Run** wird `ppar_ebay_run_state_v1` mit dem neuen Laufzustand ersetzt. Eine eventuell archivierte Vorgänger-Version behält nur die beschriebenen Kurzwerte. Das aktuelle Screenshot mit neuer Run-UUID und `0/298` beweist noch **keine Löschung der 432 Freigaben**.

**Fazit:** Behauptung einer fertigen Fehlerprotokollierung war falsch. Ein verantwortbarer Nachweis müsste beim Abbruch und Übergang zu einem neuen Lauf die konkreten Einzelcodes und Ablaufübergänge **auslesbar und dauerhaft** dokumentieren. Kein neues Plugin/Workflow/Loggingsystem auf Verdacht aufsetzen. Zunächst diese Lücke ehrlich im gemeinsamen KISS-Vertrag festhalten und vor einer neuen Version eine **bestehende** lesende Admin- oder Exportansicht an vorhandene Zustandsspeicherung anbinden, ohne Nachsuche, Produktdaten oder öffentliche Freigaben zu verändern. **Dieser Nachtrag dokumentiert nur, repariert die Protokollierung nicht.**
