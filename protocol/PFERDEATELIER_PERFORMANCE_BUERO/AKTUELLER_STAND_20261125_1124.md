# Pferdeatelier – Performance-Arbeitsstand

Stand: 25.11.2026, 11:24 CET

## 1. Aktuell installierter Live-Stand
- Affiliate-Zentrale 6.72.380.
- Paket: PFERDEATELIER_AFFILIATE_6.72.380_GEBUENDELT_PERFORMANCE_ROOTFIX.zip
- Paket-SHA-256: 00da8aa7bf6ff560563433abeb643eb0352b72ef5a97c1314a6a40c365223348
- Live-Hauptdatei-SHA-256: 3dddbb387cac24dbe4492fb507cee5c8c109db3de9b59b20ecf05616d1c7fc91
- Live-eBay-Trait-SHA-256: a2e621a9680b2a33bc2fa5364d20862c7282805158bc4c29c1e7c5d736d6b660
- Live-Fingerprints entsprechen dem gespeicherten 6.72.380-Paket.
- Kein Rückbau durchgeführt.

## 2. Letzte Live-Messung
Datei: pferdeatelier-performance-gesamtanalyse-20261125-102437.json
Pferdesättel 6.72.380:
- Wall 3.102,79 ms
- CPU 1.135,25 ms
- Cache-Hits 89.460
- Queries 310

Vorher 6.72.379:
- Wall 2.435,59 ms
- CPU 1.127,46 ms
- Cache-Hits 89.460
- Queries 316

Bewertung:
- CPU +0,69 %: kein nachweisbarer Live-Speedup durch 6.72.380.
- Kontrollrouten ohne Pferdesättel lagen CPU-seitig im Median etwa 3,36 % niedriger.
- Pferdesättel wurde relativ zu den Kontrollen nicht schneller.
- Wall-Zeit ist wegen stark veränderter Serverlast nicht kausal vergleichbar.
- neuer Server-Load etwa 45 / 72 / 132; vorher etwa 44 / 48 / 52.
- OPcache-Messung erneut nahe Restart; alle Frontendrequests eingeloggt.

## 3. Korrektur des lokalen Performance-Beweises
Der vor Ausgabe von 6.72.380 als Vollpfad bezeichnete Test war NICHT ein vollständiger WordPress-Seitenrequest.

Tatsächlich enthalten:
- kompletter Affiliate-Drei-Slot-Ausgabepfad
- echte Pferdeatelier-WXR-Kampagnen/Page-Daten
- Affiliate-Ranking und Rendering

Nicht enthalten:
- kompletter WordPress-Core-Request
- alle aktiven Plugins/Themes im realen Zusammenspiel
- reale vollständige WordPress-Datenbank
- insbesondere die echte slfo_ppar_ebay_items-Tabelle mit aktuell 8.114 Zeilen

Für fehlende eBay-Source-Zeilen wurden deterministische Ersatzzeilen erzeugt.

Konsequenz:
- -46,61 % bleibt nur ein interner Affiliate-Hotpath-Benchmark.
- dieser Wert ist KEIN WordPress-Gesamtseitenbeweis.
- WXR+Stub-Harness ist für Performance-Releasefreigaben gesperrt.
- Harness darf nur noch für Fachregression und interne Hotpathvergleiche verwendet werden.

## 4. Weiterhin gültiger Funktionsschutz 6.72.380
Inhaltlich bewiesen für die geprüften Affiliate-Fachpfade:
- 2.721/2.721 reale Kampagnennormalisierungen Alt=Neu
- 25/25 Seiten-/Provider-/Strategiekonfigurationen Alt=Neu
- 75/75 tatsächlich gerenderte Produktkarten inkl. vollständigem HTML Alt=Neu
- 2.955/2.955 Inhalts-/Sperrlogikfälle Alt=Neu
- globale Notabschaltung Alt=Neu
- eBay-Pause Alt=Neu
- idealo-Pause Alt=Neu
- sanitize_key-Filter Alt=Neu
- Metadata-Filter Alt=Neu
- pre_option-Filter Alt=Neu
- externer Objektcache Alt=Neu
- Locale-Wechsel Alt=Neu
- REST-Fallback Alt=Neu
- Cron-Fallback Alt=Neu
- keine geprüfte Produktions-Schreibfunktion entfernt

Damit ist kein inhaltlicher Funktionsrückbau in den geprüften Fachpfaden nachgewiesen.
Diese Prüfung ersetzt nicht die noch fehlende reale WordPress-Echtdaten-Performanceabnahme.

## 5. Verworfene Performance-Ideen
Nicht erneut aufnehmen ohne neue Evidenz:
- kompletter Home-Host-Read-Cache: langsamer
- GTIN-Cache: langsamer
- Deferred Title/Signature: langsamer
- Seller-Key-Cache: kein stabiler Gewinn
- kompletter Postmeta-Bulk-Read: langsamer
- nur eBay-Meta seeden: betroffener Direktabschnitt langsamer
- Candidate-Array-Gesamthash statt Row-Hash: langsamer
- direkter campaign_match_rank-Reuse/J: im strengen Test minimal langsamer

## 6. Historie der relevanten Performance-Releases
6.72.378:
- A+C lokal kausal schneller.
- lokaler Realpfad ca. -14,82 %.
- Live gegenüber 6.72.377 deutlich schneller, jedoch mit Host-/OPcache-Konfundierung.

6.72.379:
- H+I intern lokal ca. -7,31 %.
- Live kein klarer Gesamtgewinn.
- Folge: Freigabestandard verschärft.

6.72.380:
- mehrere interne Reuse-Maßnahmen im eBay-Text-/Policy-/Placement-Pfad.
- interner Harness ca. -46,61 %.
- Live kein messbarer CPU-Gewinn.
- Folge: WXR+Stub-Performanceharness als Releasebeweis verworfen.

## 7. Ab jetzt verbindlicher Performance-Freigabestandard
Kein neues Performance-Plugin ohne VORHERIGEN Nachweis:
1. echte lokale WordPress-Kopie oder gleichwertiger Echtdatenaufbau mit vollständiger DB, Plugins, Theme und realer Affiliate/eBay-Datenbasis;
2. mehrere alternierende Alt/Neu-Läufe derselben realen Seite;
3. kompletter WordPress-Seitenrequest klar schneller;
4. jede Einzelmaßnahme separat kausal schneller;
5. mehrere bewiesene Maßnahmen erst danach bündeln;
6. finales ZIP erneut entpacken und exakt diesen Quellstand nochmals vollständig messen;
7. inhaltlicher Funktionsvergleich zusätzlich zwingend: Kandidaten, Reihenfolge, Ranking, Provider, Strategien, IDs, Titel, URLs, Tracking, Bilder, CTA, Preis, Währung, Verfügbarkeit, Fallbacks, Pausen, Notabschaltung, dynamische Meta-/Optionsänderungen, Filter, Objektcache und tatsächlich gerendertes HTML;
8. Byte-/Dateivergleich nur Zusatzbeweis;
9. Live dient nur zur Bestätigung eines vorher bereits real lokal bewiesenen Gesamtgewinns.

## 8. Aktueller nächster Arbeitsweg
- kein neues Plugin bauen.
- 6.72.380 bleibt live installiert; kein bewiesener Grund für einen Rückbau.
- nächster technischer Schritt: Ursachenprofiling der realen Live-Ausführungsstrecke oder echte lokale WordPress-/DB-Kopie.
- neue Optimierungen erst nach kausaler Isolation des realen Rest-Hotpaths.
- Maßnahmen sammeln; kein Plugin für einzelne kleine Fixes.
- vor jeder späteren Ausgabe kompletter inhaltlicher Funktionsbeweis.

## 9. Gesicherte Bürodateien
- /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.380_GEBUENDELT_PERFORMANCE_ROOTFIX.zip
- /pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_AFFILIATE_6.72.380_GEBUENDELT_PERFORMANCE_ROOTFIX.zip
- /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_6.72.380_PRUEFNACHWEIS.md
- /pferdeatelier/PERFORMANCE_BUERO/MESSUNGEN/pferdeatelier-performance-gesamtanalyse-20261125-102437.json
- /pferdeatelier/PERFORMANCE_BUERO/PFERDEATELIER_PERFORMANCE_STAND_2026-11-25_1124.md


## 2026-11-25 – Datenbankbereinigung gestartet
- IONOS-Sperre wegen >2 GB.
- OPTIMIZE wegen fehlendem INSERT-Recht nicht möglich.
- DELETE funktioniert.
- 107 WordPress-Transients gelöscht.
- Hauptverursacher in slfo_options nach Gruppen: PPAR ~110,4 MB, PSTE ~99,0 MB, TXE ~93,0 MB, PSERC ~60,1 MB.
- auffälligste Einzelwerte: TXE-Legacy-Backup ~83,45 MB und PSTE-Sandbox ~58,23 MB.
- fortlaufendes Detailprotokoll: DATENBANK_SPEICHER_20261125.md
- noch keine großen produktiven Daten gelöscht.
