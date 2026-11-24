# Aktuelles Performance-Plugin

Stand: 24.11.2026

Live installiert:
- Affiliate-Zentrale 6.72.377
- letzter PASSIV-Livewert Pferdesättel: 4.859,09 ms Wall / 1.601,79 ms CPU / 89.392 Cache-Hits / 310 Queries
- gegenüber 6.72.376: Cache-Hits 121.246 -> 89.392 (-31.854 / -26,3 %), Queries 310 -> 310
- Live-Speedup wegen abweichender Laufbedingungen weiterhin nicht isoliert behauptet.

Aktueller freigegebener Testkandidat:
- Affiliate-Zentrale 6.72.378
- Paket: PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_POSTPROCESS_ROOTFIX.zip
- SHA-256: 9283dd3b4237717db084708f981b2b4ef3b5b7c67568794a66f47c522f265bd7
- Büro-Ablage: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_POSTPROCESS_ROOTFIX.zip
- Prüfnachweis: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_6.72.378_PRUEFNACHWEIS.md
- GitHub-Nachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.378.md

Status:
- vier zusammenhängende Restursachen im Kategorie-Produktpfad gemeinsam gebündelt; kein Einzel-Fix.
- echter 1.010er-Pferdesättel-Pool lokal: 20 Durchläufe Median 216,71 -> 187,71 ms (-13,38 %).
- get_post_meta 3.731 -> 3.114; get_option 324 -> 15.
- 2.721/2.721 Kampagnennormalisierungen identisch.
- 25/25 reale Seiten-/Providerkombinationen mit identischen Shared-Pools und Produkt-1/2/3-Ausgaben.
- Pferdesättel Produkt-1/2/3 bis render_banner(): HTML Alt=Neu.
- dynamische Filter/externer Objektcache: historischer Einzelweg, Alt/Neu identische Ausgaben und Aufrufzahlen.
- Funktionen 1.591 -> 1.594; entfernt 0; 1.582 bestehende unverändert; Produktions-Schreibprimitive unverändert.
- PHP 23/23 PASS; ZIP 66/66; Re-Extract 0 Hashabweichungen; PHP erneut 23/23 PASS.
- nächster Schritt: 6.72.378 installieren und genau einen PASSIV-Gesamtlauf ausführen.
