# Aktuelles Performance-Plugin

Stand: 24.11.2026

LIVE:
- Affiliate-Zentrale 6.72.378 – korrigierter A+C-Kandidat
- Live-Fingerprint passt exakt zum freigegebenen Paket (Hauptdatei, eBay-Trait, eBay-Run).

Neuer PASSIV-Lauf:
- Messung: pferdeatelier-performance-gesamtanalyse-20261124-173614.json
- Pferdesättel: 2.222,09 ms Wall / 1.092,40 ms CPU / 89.461 Cache-Hits / 310 Queries
- 6.72.377 vorher: 4.859,09 ms Wall / 1.601,79 ms CPU / 89.392 Cache-Hits / 310 Queries
- Wall: -54,27 %
- CPU: -31,80 %
- Haupt-Inhaltsblock loop_start -> wp_footer: 3.628,90 -> 1.492,57 ms = -58,87 %
- Cache/Queries praktisch unverändert: +69 Cache-Hits, Queries 310 -> 310.

Kausalitätsbewertung:
- Der Gesamtserver war im neuen Lauf ebenfalls schneller; deshalb wird nicht der gesamte Wall-Gewinn 6.72.378 zugerechnet.
- Vergleichsrouten ohne den vollen Pferdesättel-1010er-Hotpath verbessern sich CPU-seitig im Median um ca. -15,22 %.
- Pferdesättel verbessert sich CPU-seitig um -31,80 %; zusätzlicher Effekt gegenüber dem Kontrollmedian ca. 16,6 Prozentpunkte.
- Dieser zusätzliche Effekt liegt nahe am vorher lokal isoliert gemessenen A+C-Gewinn von -14,82 %.
- Zusammen mit den direkten Einzeltests A (-20,9 %) und C (-90,2 % in der betroffenen Schlüsselarbeit) ist der Live-Performanceeffekt von A+C damit konsistent belegt; die exakte Gesamt-Wall-Zahl bleibt hostabhängig.

Funktionsschutz:
- weiterhin 2.721/2.721 Normalisierungen, 25/25 reale Seiten-/Providerfälle, 75/75 gerenderte Produktkarten und dynamische Sonderfälle Alt=Neu aus dem Freigabenachweis.
- Live-PASSIV zeigt keine neue Query- oder HTTP-Last im Pferdesättel-Request.

Aktueller Prüfpfad:
- kein neues Plugin ausgegeben.
- verbleibender 1.010er-Pfad wird weiter zerlegt.
- aktuell gemessene Restblöcke lokal: gemeinsamer Kandidatenaufbau ~81 ms / 2.721 Kampagnendaten-Lesungen; Produkt-1-Postprocessing ~100 ms, davon 393 eBay-Metalesungen und 310 Bild/Home-Prüfungen.
- nur weitere Maßnahmen mit eigenem Zeitbeweis und vollständigem Alt/Neu-Ausgabebeweis werden gebündelt.
