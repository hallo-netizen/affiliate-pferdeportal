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