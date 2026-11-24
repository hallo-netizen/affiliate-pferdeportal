# Aktuelles Performance-Plugin

Stand: 24.11.2026

Live installiert:
- Affiliate-Zentrale 6.72.377
- letzter PASSIV-Livewert Pferdesättel: 4.859,09 ms Wall / 1.601,79 ms CPU / 89.392 Cache-Hits / 310 Queries
- gegenüber 6.72.376: Cache-Hits 121.246 -> 89.392 (-31.854 / -26,3 %), Queries 310 -> 310
- Gesamt-Speedup von 6.72.377 wegen abweichender Laufbedingungen nicht isoliert behauptet.

Aktueller freigegebener Testkandidat:
- Affiliate-Zentrale 6.72.378 – KORRIGIERT
- Paket: PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_CAUSAL_ROOTFIX.zip
- SHA-256: af39e106c595be83210d2c4a164c1274c723d25c2a2599b77f86488e4eda9839
- Büro-Ablage: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_CAUSAL_ROOTFIX.zip
- Prüfnachweis: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_6.72.378_KORRIGIERT_PRUEFNACHWEIS.md
- GitHub-Nachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.378.md

WICHTIG:
- Der zuerst erzeugte 6.72.378-POSTPROCESS_ROOTFIX mit SHA 9283dd3b... ist VERWORFEN und darf nicht installiert werden.
- Nach verschärfter Einzel-Kausalitätsprüfung bleiben nur zwei Maßnahmen A+C.

Kausalitätsbeweis:
- A eBay-Kohorten-Schlüsselarbeit: 78,83 -> 62,34 ms (-20,9 %) im exakt betroffenen Produktionsabschnitt; Meta 1.010 -> 393; 315 -> 315 Ergebnisse; geordneter Output-Hash identisch.
- C Kandidaten-Fingerprint Slot 2/3: 17,08 -> 1,67 ms (-90,2 %) in exakt der wiederholten Schlüsselarbeit.
- Gesamt A+C im echten 1.010er-Pool: 220,75 -> 188,04 ms (-14,82 %).

Funktionsschutz – inhaltlich, nicht Bytevergleich:
- 2.721/2.721 reale Kampagnennormalisierungen Alt=Neu.
- 25/25 reale Seiten-/Providerkombinationen Alt=Neu.
- 75/75 tatsächlich gerenderte Produktkarten einschließlich HTML Alt=Neu.
- sechs explizit aktivierte dynamische Sonderfälle: Ausgabe UND Aufrufzahlen Alt=Neu; historischer Einzelweg bleibt erhalten.
- echte Meta-/Provider-/Strategieänderungen während des Ablaufs werden Alt=Neu erkannt.
- 0 bestehende Funktionen entfernt; Produktions-Schreibwege unverändert (nur Zusatzbeweis).

Bewusst NICHT aufgenommen:
- Home-Host-Cache: kein belastbarer Zeitgewinn, Einzeltest ca. +1,3 %.
- GTIN-Cache: 17,19 -> 20,25 ms, also langsamer.
- Deferred-Titelsignatur-Reuse: 242,72 -> 259,33 ms, also langsamer.
- Seller-Key-Cache: kein stabiler Gewinn.

Paketprüfung:
- 66/66 Dateien, 23/23 PHP-Lint PASS.
- Re-Extract: fehlend 0, zusätzlich 0, Hashabweichungen 0.
- nächster Schritt: ausschließlich korrigierte 6.72.378 installieren und genau einen PASSIV-Gesamtlauf ausführen.
