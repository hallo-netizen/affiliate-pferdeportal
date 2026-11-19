# Performance Diagnose Safe 6.0.0 – All-in-One

Stand: 2026-11-19  
Status: **INSTALLATIONSREIF / QA PASS / KEINE PRODUKTIONSFUNKTION GEÄNDERT**

## Paket
- Datei: `PERFORMANCE_DIAGNOSE_SAFE_6.0.0_ALL_IN_ONE.zip`
- SHA-256: `5c20fd10acb16f35d807bfe79354f7086455d9d6c5189ba65d5951a0e0729536`
- PHP-Source SHA-256: `043770f2b97d6d562014369f361196429370d86f6d7162c83df9750c5db034df`
- ZIP-Integrität: PASS
- PHP-Lint: PASS
- Pferdeatelier-Büro: `/pferdeatelier/PLUGINS/PERFORMANCE/`

## Funktionsschutz
- Diagnosefunktionen 5.0 -> 6.0: **113 -> 136**
- entfernt: **0**
- neue Diagnosefunktionen: 23
- Affiliate-Zentrale: **nicht geändert**
- Template-Kit: **nicht geändert**
- keine Post-/Term-/Meta-Schreibfunktionen
- keine Cron-Änderung
- kein Cache-Flush
- kein direkter DB-Write
- WordPress-Schreiben nur eigene Sessionoption; Dateien nur im eigenen Diagnose-Tempbereich

## Vier dauerhafte Messmodi
1. PASSIV: kein SAVEQUERIES, keine Hook-Spans, keine Tiefenobserver.
2. URSACHENPROFIL: SQL-Einzelzeiten + ausgewählte Hook-/Slot-Walltime, Filterwerte unverändert.
3. FRONTEND-TIEFEN: bestehende hochauflösende Frontend-Attribution.
4. KOMPLETT-TIEFEN: bestehende hochauflösende Attribution für alle Requestarten.

Lokale Modussimulation:
- PASSIV: SAVEQUERIES aus; 0 Span-Callbacks; 0 sensitive Observer.
- URSACHENPROFIL: SAVEQUERIES an; 42 Span-Callbacks; 0 sensitive Observer.
- FRONTEND-/KOMPLETT-TIEFEN: 42 Span-Callbacks + 6 sensitive Observer.
- Filter-Pass-through: Array identisch; Objektidentität identisch.

## Methodische Korrekturen gegenüber 5.0
- PASSIV schaltet SAVEQUERIES nicht mehr ein.
- schwere Template-/Affiliate-Proof-Inspektion wird in PASSIV nicht pro Request ausgeführt.
- automatischer Loopback läuft erst am Sessionende.
- Diagnose-Loopback wird nicht als normale Seite gezählt.

## Neu dauerhaft abgedeckt
- Hook-/Slot-Zeitprofil
- SQL nach Art und Tabelle
- Request-Phasenaggregation
- Start-/End-Snapshot und DB-/OPcache-/Cron-/Options-Deltas
- DB-Indexübersicht
- Dateisystemprobe
- detaillierte Cron-/Action-Scheduler-Rückstände
- Browser DNS/Connect/TLS/Download/Protokoll/Cache-/Third-Party-Anteile
- HTTP-Zeit nach Host
- Diagnose-Eigenaufwand
- PHP-Fehlerkomponente

## Harte technische Grenze
Exakte CPU-Zeit jedes beliebigen fremden PHP-Callbacks und PHP-FPM-Worker-Sättigung sind ohne Server-Profiler/Serverzugriff nicht sicher direkt messbar. Dafür wird kein weiteres WordPress-Diagnoseplugin als Scheinlösung benötigt.
