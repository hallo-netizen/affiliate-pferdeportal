# Artikelwerkstatt – KISS: Testinstaller und Chatübergabe

**Stand:** 13.11.2026, testfähiger isolierter Installer `Artikelwerkstatt_KISS_0.2.0_TEST_INSTALLIEREN.zip`. **Freigegeben ausschließlich zur Installation auf einer separaten WordPress-Testumgebung.** Keine Änderungen auf Live oder an alten Plugins. **Keine produktive Endabnahme.**

## Was tatsächlich installiert wird

WordPress-Plugin **Artikelwerkstatt – KISS (Test)**, Version `0.2.0-test`, eigener Plugin-Ordner `artikelwerkstatt-kiss`, eigener WordPress-Auftragsbestand `awk_kiss_orders_v1` und eigener DataForSEO-Cache `awk_api_*`. Es wird **kein** anderer Pluginordner, kein Original-WordPress-Optionswert, keine ursprüngliche PSTE-/PSERC-/PPM-Tabelle verändert. Alte PSTE-/PSERC-/PPM-/Editorial-Guard-Plugins werden vom neuen Plugin **nicht automatisch deaktiviert**.

**Arbeitsweg:** DataForSEO-Keywordvorschläge (Originalanbieter-Klasse portiert, vorhandene Credentials lesend) → einmalige manuelle redaktionelle Freigabe und Kategoriezuordnung → vorhandener externer Titeldatei-Vertrag `PSTE_RAW_KEYWORD_MINI_BATCH_V1` (nur Titel editierbar) → ein WordPress-Regal von freigegebenen Aufträgen (einschließlich Sofortartikel und lesend importierter Altfreigaben) → chargenweiser Original-K0-Handoff `PSERC_TEXTMACHINE_METADATA_BATCH_V2` (fünf unveränderte Felder, stabiler Hash) → externer unveränderter K0 → Rücklauf `PFERDE_ATELIER_WORDPRESS_IMPORT_V1` oder unterstützte bestehende System4-Formate → WordPress-Entwurf; Dubletten-/Publikationssperre.

**Bitte nicht mit dem bisherigen Vollumfang verwechseln:** Die komplexe automatisierte PSTE-Relevanz-/Suchintention-/Kannibalisierungsentscheidung ist noch **nicht** nachweislich durch das neue System ersetzt. Neue Vorschläge werden derzeit **einmalig durch den Administrator freigegeben**, nicht automatisch qualifiziert. K0 selbst ist nicht im Plugin. Alle neuen Auftragsdaten gehören nur zur isolierten Testinstallation.

## Gegenprüfungen

| Testdatei | Lokal bestanden |
| --- | ---: |
| `qa_original_35_migrated.php` | 35 |
| `qa_new_features.php` (DataForSEO, ursprüngliches Titelformat, 61 Altfreigaben, zweite Portalstruktur) | 28 zusätzliche |
| `qa_20_batch_and_admin.php` (WordPress-Menü, Chargenexport, 13+7 Teillieferungen, kein Doppelimport) | 15 zusätzliche |
| `qa_bad_item_isolation.php` (falsche Zeile stoppt nur Einzelauftrag, falscher Gesamthash sperrt vor Schreiben) | 5 zusätzliche |
| **Gesamt einmalig** | **83** |

Ergänzend: fünf PHP-Dateien fehlerfrei geparst, ZIP-CRC aller sieben Einträge bestanden, Plugin-Header und eigenes Verzeichnis vorhanden. Original-ZIPs nach Aufbau unverändert SHA-256:

- PSTE QA `.50`: `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`.
- PSERC QA `.71`: `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`.

**Wichtig:** Alle Funktionsprüfungen liefen lokal unter PHP 8.4 mit simulierten WordPress-Funktionen und simuliertem DataForSEO-Anbieter. Sie beweisen nicht, dass WordPress auf der tatsächlichen Testinstallation dieselben Ergebnisse liefert. Kein Test mit echtem K0-Rücklauf oder echtem Datenbank-Commit erfolgt.

## Installationsregel

1. **Nur** auf einer isolierten Testkopie mit eigener Datenbank und Sicherung installieren. Die Testkopie sollte eine `test.`-/`staging.`-/`.test`-Domain besitzen oder WordPress als `staging`, `local`, `development` kennzeichnen. Andernfalls verweigert das Plugin absichtlich seine Aktivierung.
2. Unter *WordPress → Plugins → Installieren → Hochladen* die ZIP laden und aktivieren; sie erscheint unter **Artikelwerkstatt – KISS (Test)**. Bedienelemente unter *Werkzeuge → Artikelwerkstatt – KISS*.
3. Erst auf der **Testumgebung** alte Themenengine/Redaktionsplan/PPM ggf. Guard **manuell deaktivieren**, wenn ausdrücklich nur der neue Ablauf getestet werden soll. Live unverändert.
4. Zuerst alte FREI-Freigaben nur lesend übernehmen oder **einen** Sofortartikel mit vorhandenem Keyword, Kategorie, Artikelart und Suchabsicht anlegen. Eine eventuell fehlende Fachangabe wird nicht erfunden.
5. Danach externe Titeldatei ausgeben, nur Titel eintragen/übernehmen, K0-Datei exportieren, K0 **unverändert** nutzen und später Rücklauf importieren. Prüfung in WordPress, ob ein Entwurf entstand und welche ursprüngliche Auftrags-ID benutzt wurde.
6. Fehler (besonders K0-/Planplatz- oder DataForSEO-Probleme) zusammen mit angezeigtem Status für weitere Reparatur dokumentieren. Kein manueller Import in Live und keine Veröffentlichung.

## Noch offener Zielvertrag – nicht als erledigt markieren

- Nachweis vollständiger automatischer SEO-/Relevanz-/Suchintention-/Kannibalisierungsprüfung wie im PSTE-Original (jetzt redaktionelle Freigabe in der Testoberfläche statt automatische semantische Beurteilung).
- Echte DataForSEO-Anfrage (kostenpflichtig, vom Benutzer ausgelöst) und echte ursprüngliche Zugangsdaten entschlüsselbar auf Test-WP.
- Tatsächlicher externer Titelworker mit dem eingefrorenen alten Originalformat und K0 mit Original-5-Felder-Datei.
- Echte WP-Draft-Speicherung und Wiederanlauf nach serverseitigem Fehler; keine parallelen Worker des Altbestands.
- Unterschied zwischen technischem `plan_slot` der neuen Aufträge und altseitig von PPM gebuchten Plätzen im wirklichen K0-Workflow nachweisen. **PPM NICHT auf Live deinstallieren.**
- Portalneutralität zusätzlich mit echten Kategorien und Freigaben aus Hobby Depot und Hab & Bewahr abnehmen.

**Nächster neuer Chat:** Datei in GitHub-PR #768, WordPress-Testbeobachtungen, fertige Test-ZIP aus Library lesen. Nicht neue Grundsatzarchitektur bauen; nur vorhandene Strecke gezielt gegen echte WP/K0-Daten beweisen und konkrete Abweichungen reparieren.