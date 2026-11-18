# Pferdeatelier – Texterstellung 0.4.33: Gespeicherten MINI-Auftrag explizit erneut herunterladen

**Stand:** 18.11.2026. Vollständiges ZIP unter `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/Texterstellung-0.4.33-KISS-GESPEICHERTEN-MINI-AUFTRAG-LADEN.zip`; **Live-Installation noch nicht nachgewiesen**.

## Problembeleg
Auf der vom Nutzer verwendeten 0.4.32 gab es in Texterstellung → MINI-Export nur die Schaltfläche `MINI-Gesamtauftrag herunterladen`. Der Code `TXE_Workshop::seoExport()` war zwar für eine automatische Wiederaufnahme anhand `active_seo_batch` angelegt, aber ein eigener sichtbarer Download-Knopf für einen schon gespeicherten Batch **fehlte**. Der Nutzer meldete ausdrücklich, er könne den gespeicherten Auftrag nicht erneut herunterladen. Ein zusätzlicher echter HTTP-Fehler ist nicht nachgewiesen.

## Minimale KISS-Korrektur
- **Genau zwei Dateien von 0.4.32 geändert:** `texterstellung/texterstellung.php` (Version 0.4.33) und `texterstellung/README-TESTINSTALLATION.txt`. **87/89 Dateien byte-identisch**, keine zusätzliche PHP-Datei, kein neues Auftragsregal, keine neue Fachprüfung.
- Im vorhandenen MINI-Export-Menü wird bei gespeicherten unvollständigen MINI-Chargen sichtbar **`Gespeicherten MINI-Auftrag erneut herunterladen`** angezeigt. Die gespeicherte Charge ist auswählbar.
- Die WordPress-POST-Aktion `txe_seo_redownload` verwendet **nur einen Lesezugriff** auf das bestehende `texterstellung_orders_v1` und dessen `seo_batches`, `mini_worker_checkpoints`, `mini_progress`. Der Download verändert keine Redaktions- oder K0-Aufträge, löst keine Recherche und keinen neuen MINI-Lauf aus. Nur das vorhandene Diagnoseereignis zum Download wird aufgezeichnet.
- Auch wenn `active_seo_batch` nicht mehr gesetzt ist, kann der vorhandene nicht abgeschlossene Batch über seine gespeicherte ID gelesen werden. Unbekannte Batches brechen ab, ohne neue Chargen zu erzeugen.
- Solange ein offener Batch vorhanden ist, wird kein missverständlicher `Neuer MINI-Gesamtauftrag`-Knopf angeboten.

## Vor ZIP-Ausgabe geprüft
- 13/13 neue gespeicherter-MINI-Wiederdownload-Tests (Nachweis insbesondere: nach EDITORIAL → `next=TITLE`, Download vor und nach Migration von 61 Testaufträgen, verlorene Aktiv-Markierung, kein Schreibzugriff ins Auftragsregal).
- 16/16 MINI-Regressionen, 48/48 MINI→K0-E2E, 34/34 Live-MINI-Migration, 34/34 61er-Migration, 38/38 WordPress-Importregressionen; 79/79 PHP-Syntaxprüfung.
- ZIP-CRC OK, 89/89 alte Archivnamen vorhanden, 87/89 Inhalt byte-identisch.
- ZIP SHA256 `514781f2156ce436b1dda25a6daf484be8ece2010d57704aea2bb761cdcba295`.
- Prüfbericht `PFERDEATELIER-TEXTERSTELLUNG-0433-MINI-WIEDERDOWNLOAD-PRUEFBERICHT-20261118.md` und Testlogs im selben Pluginbüro.

## Nächste Schritte auf LIVE
1. WordPress → Plugins → Plugin hinzufügen → ZIP 0.4.33 hochladen → **bestehende Texterstellung ersetzen, niemals löschen**.
2. Texterstellung → MINI-Export → **Gespeicherten MINI-Auftrag erneut herunterladen**. Falls mehrere vorhanden sind, die gerade bearbeitete Charge auswählen. **NICHT neu recherchieren**.
3. Download-JSON im **bisherigen MINI-Chat** beim ausgewiesenen `next`-Arbeitsschritt fortsetzen. Nach gespeicherter EDITORIAL-FREI-Entscheidung ist dies `TITLE`; CATEGORY/EDITORIAL bleiben eingefroren.
4. Ergebnis unter Texterstellung → MINI-Import hochladen; letzter Worker erzeugt den fertigen WordPress-Auftrag. Erst danach K0-Export mit 1–3 Themen.

**Nicht behaupten:** Der Benutzer konnte den Download auf Live bereits durchführen; dazu ist nach Installation 0.4.33 die echte Bedienbestätigung notwendig. Ebenfalls keine Live-WordPress-Verbindung, die das Plugin installieren oder gespeicherte Datensätze direkt auslesen könnte.
