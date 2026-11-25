# Hobbydepot 0.4.24.17 – EIN MINI-Export, EIN MINI-Import (20.11.2026)

## Grund
Nutzer verlangt strikt den funktionierenden technischen Pferdeatelier-Ablauf bei nur **einem** MINI-Export in den Chat und **einem** MINI-Import aus dem Chat. Die ursprüngliche Bühne verlangte sichtbare einzelne CATEGORY/EDITORIAL/TITLE-Checkpoint-Dateien. Diese sind ausschließlich ein internes Sicherheits- und Entscheidungsprotokoll, **keine zusätzlichen Nutzer-Uploads**.

## Fix an vorhandener Stelle, keine neuen Entscheidungsebenen
In exakt einer Datei `texterstellung-hobbydepot/texterstellung.php` (86 von 87 Plugin-Dateien unverändert) erfolgt der eine externe MINI-Import jetzt als Transporthülle: Der Original-Batch mit identischer unveränderbarer Inventar-/Keywordquelle wird vor jeder WordPress-Änderung geprüft. Dann werden **die vorhandenen Originalmethoden** `miniWorkerCheckpoint` für CATEGORY, EDITORIAL und TITLE in der festgelegten Reihenfolge intern ausgeführt. Jede Stufe speichert bisherige Belege; Fremddaten oder geänderte frühere Entscheidungen werden vor dem Start abgewiesen. Kein zusätzlicher Editor, keine zweite Entscheidung; alter 3-Stufen-Import bleibt für Rückwärtskompatibilität. Original DataForSEO, PSERC und K0 vollständig unverändert.

## Tatsächlich ausgeführte lokale Tests
- 20 echte MINI-Positionen aus Nutzerdatei, alter WordPress-CATEGORY-Bestand mit 20 bestätigten Receipts: **20/20 fertig, 3 K0-Aufträge, 17 Klärungen, 0 Fehlzuordnungen in einem Import**.
- Komplette Kategorie-/Redaktion-/Titelkette mit leerem MINI-Zwischenstand ebenfalls in **einem Import** abgeschlossen.
- Wiederholtes Einlesen ohne Dubletten; negative Fälle (manipulierte Originalquelle, Kategorie, K0-Typ, Titel, redaktionelle Entscheidung, anderer Batch, fehlende Stage-Felder, nicht erlaubter Titel bei KLAERUNG) blockiert.
- Separate Regression der alten Originalcheckpoint-Schnittstelle bestanden.
- PHP-Syntax 78/78; ZIP-CRC 87/87; 86/87 unveränderte Dateien.
- Upload `texterstellung-k0-export-mit-zuordnung.json` (3 Artikel) mit echtem SHA256-Metadatenbatch/WordPress-Receipt/Order-ID/Artikel-ID/Slot-Verknüpfung originalgetreu geprüft. Es ist **bereits** die K0-Eingabedatei, daher **kein MINI-Restart**.
- **Grenze:** keine Live-Installation ausgeführt, keine neuen Hobby-K0-Artikel mit LanguageTool erstellt oder verifiziert. Hier wird ein technischer MINI-Transportfix bestätigt, kein K0-Texterfolg behauptet.

## Ablage
Persönliche Library `/Hobby Depot/Plugin-Büro/`:
- `Texterstellung_Hobbydepot_0.4.24.17_EIN_MINI_EXPORT_EIN_IMPORT.zip` (518148 Bytes, SHA256 `50403c6c75444351f8880a344ba6f984d2ae0b7ab54051bc0a16fd473725ae59`)
- `Hobbydepot_0.4.24.17_MINI_EIN_DATEI_PRUEFNACHWEIS.json`
- `Texterstellung-CURRENT.md` Version 0.4.24.17.

**Nächster WordPress-Schritt nur für zukünftige MINI-Läufe:** Plugin wie gewohnt überinstallieren; in WP `Texterstellung → MINI-Export` genau einmal exportieren, komplette MINI-Entscheidungen mit gleicher Datei im Chat, anschließend `Texterstellung → MINI-Import` genau einmal importieren. Aktuelle drei K0-Aufträge bereits an K0 übergeben, keine MINI-Wiederholung.
