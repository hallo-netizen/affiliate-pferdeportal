# Pferdeatelier / Affiliate-Zentrale – physische Original-ZIP im Gespräch geprüft (08.11.2026)

## ERGÄNZUNG 08.11.2026 – PERSISTENTE ORIGINAL-ZIP ERFOLGREICH ABGELEGT UND RÜCKGEPRÜFT

**Die Original-ZIP ist jetzt tatsächlich und dauerhaft in der persönlichen ChatGPT-Dateibibliothek gespeichert. Dies ersetzt die frühere Angabe „Library-Kopie gescheitert“.**

- Ablageort: `/pferdeatelier/PLUGINS/AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`
- Datei über `files__manage_library` hochgeladen, über `files__list` mit Größe **5.345.251 Bytes** bestätigt und über `files__materialize` aus der Bibliothek neu ausgelesen.
- **Harte Nachprüfung:** SHA-256 Upload = SHA-256 Library-Readback = `b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0`; Binärvergleich **BYTE_EQUAL TRUE**.
- Die Original-ZIP wurde nicht rekonstruiert, bearbeitet, überschrieben oder als installierbar freigegeben.
- **Für Folge-Chats:** Zuerst unter diesem exakten Library-Pfad per Files suchen/listen und die vorhandene Original-ZIP zur Prüfung materialisieren. NICHT die Nutzerdatei erneut anfordern. NICHT die alte GitHub-Referenz 6.72.211 als 6.72.308 ausgeben.
- **GitHub-Abgrenzung:** Dieses GitHub-Dokument ist ein bestätigter Fundortverweis. Die ZIP selbst liegt in der persistenten Library, **nicht** als Binärdatei im GitHub-Tree. Der GitHub-Release-Branch und sein Current bleiben unangetastet.

## Verifizierter tatsächlicher Upload
- **Exakter hochgeladener Dateiname:** `AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`
- **SHA-256 der physisch geöffneten Datei:** `b4d8547fd2aa134f7f82f568db3a81df54bb7d2131fd0752e76e3f0ca2251fe0`
- **Git-Blob-SHA1 des exakt hochgeladenen ZIP-Inhalts:** `28e30ac000b4497b944026e246ea3e6ddfb3697a`
- **Dateigröße:** 5.345.251 Bytes
- **66 ZIP-Dateien; 23 PHP-Dateien; 3 JSON-Dateien; ZIP-CRC PASS**
- **PHP-Plugin-Header:** `Version: 6.72.308`
- **Originaldatei-Herkunft:** Nutzer-Upload in ChatGPT vom 08.11.2026, lokal als echte ZIP-Datei gelesen; **nicht rekonstruiert**.
- Die SHA256 stimmt **bytegenau** mit dem vom 06.11.2026 hinterlegten Prüfbericht zur tatsächlichen 6.72.308-Original-ZIP überein.

### Wichtige Grenze – KEINE ZIP-ABLAGE VORTÄUSCHEN!
Die **Binärdatei ist NICHT in diesem GitHub-Repository gespeichert**. Es wurde ausdrücklich versucht, sie via GitHub-Git-Blob-SHA zu finden; GitHub meldete **404 (Blob nicht vorhanden)**. Die verfügbaren GitHub-Dateischreibaktionen ermöglichen ausschließlich UTF-8-Text bzw. Base64 aus einem als Zeichenfolge verfügbaren Inhalt; der physische 5,3-MB-Upload ist in dieser Sitzung darüber nicht als Datei übertragbar. Die frühere persönliche Library-Kopie war zunächst am Speicherlimit gescheitert; **die neue Library-Ablage ist inzwischen erfolgreich und bytegenau nachgeprüft** (Ergänzung oben). 
Dieser Beleg ist **kein Platzhalter-Installer, keine als Datei getarnte Pointerdatei und keine freigegebene ZIP**. Nicht behaupten, `CURRENT.zip` oder das vollständige Plugin seien auf GitHub. Nicht den alten 6.72.211-Quellstand oder den 6.72.308-Text-Patch als die vollständige ZIP ausgeben.

### Bestehender Stand
- Original-ZIP-Datei im aktuellen Gespräch hochgeladen, vorhanden, byteidentisch mit dem bekannten 6.72.308-Teststand; kann hier lokal zur weiteren Quellprüfung verwendet werden.
- Offizieller Release-Kandidat in `control/release-governance/CURRENT_RELEASE.json`: 6.72.211, releasegesperrt; keinesfalls automatisch ersetzen.
- Die aktuell auf WordPress installierte Version ist dadurch nicht bewiesen; die Diagnose lief mit interner Buildkennung 6.63.8, die **keine** Pluginversion darstellt.
- **Nächstes Arbeitsziel:** Den bestehenden 6.72.311-Gesamtpatch direkt gegen die **persistierte Original-308-ZIP aus der Library** prüfen; originale ZIP unverändert lassen. GitHub-Current nicht überschreiben; die ZIP nicht fälschlich als im GitHub-Tree gespeichert ausgeben.

## Live-Fehlerdiagnose (08.11.)
Ein zum archivierten fehlgeschlagenen Gesamtlauf passender gespeicherter Discovery-Report belegt: genau ein `request_error` / `http_request_failed` mit `cURL error 28: SSL connection timeout`. Der `partial`-Zustand führt über `gapfill_partial_unresumable` zum globalen Abbruch. **Kein Fix freigegeben; die 6.72.308-Quelle muss vor jedem Patch vollständig direkt geprüft werden, Tests gegen den Gesamtworkflow.**
