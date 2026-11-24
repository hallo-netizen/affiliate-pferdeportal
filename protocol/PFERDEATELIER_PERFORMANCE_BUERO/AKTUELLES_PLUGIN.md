# Aktuelles Performance-Plugin

Stand: 24.11.2026

Live installiert:
- Affiliate-Zentrale 6.72.376
- letzter Livewert Pferdesättel: 5.332,37 ms Wall / 1.493,98 ms CPU / 121.246 Cache-Hits / 310 Queries
- Cache-Reduktion gegenüber 6.72.375 ursächlich bestätigt; Gesamt-Speedup wegen Serverlast nicht bewiesen.

Aktueller freigegebener Testkandidat:
- Affiliate-Zentrale 6.72.377
- Paket: PFERDEATELIER_AFFILIATE_6.72.377_GEBUENDELT_EXACT_READ_ROOTFIX.zip
- SHA-256: df04630d846b0417dd0ddb1341cd2321a308ca189e0ade4c7e6adb11b2fce844
- Büro-Ablage: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.377_GEBUENDELT_EXACT_READ_ROOTFIX.zip
- Prüfnachweis: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_6.72.377_PRUEFNACHWEIS.md
- GitHub-Nachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.377.md

Status:
- ein gebündelter Kandidat mit mehreren direkt gemessenen Ursachen, kein Einzel-Fix-Paket.
- Realbestand: Meta-Hotpath 8.080 -> 1.010; Control-Optionen 9.316 -> 11; Portal/Home 3.030 -> 3; Incident 648 -> 8; eBay-Checkpoint 393 -> 1; Shared Pool identisch.
- relevante dynamische Zustände fallen auf historischen Einzelpfad zurück.
- 0 bestehende Funktionen entfernt; Kernlogik und Schreibwege unverändert.
- PHP 23/23 und ZIP 66/66 vollständig geprüft.
- noch nicht live gemessen.
- nächster Schritt: 6.72.377 installieren, genau einen PASSIV-Gesamtlauf ausführen.
