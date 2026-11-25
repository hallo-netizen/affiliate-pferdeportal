# Aktuelles Performance-Plugin

Stand: 25.11.2026

LIVE:
- Affiliate-Zentrale 6.72.379.
- Source-Fingerprint Hauptdatei live: 0501805a4aaaa03e7c48cd930de0c27b92a21ab343cb8b3a9f5af7bd54da99a8
- dieser Fingerprint entspricht exakt dem freigegebenen 6.72.379-ZIP.
- Paket-SHA-256: 264b872aae3238027b38304282ddc6fcca868cb8a0b46629ad85f67b813ecc67

Neuer PASSIV-Lauf:
- Messung: pferdeatelier-performance-gesamtanalyse-20261125-091933.json
- Pferdesättel 6.72.379: 2.435,59 ms Wall / 1.127,46 ms CPU / 89.460 Cache-Hits / 316 Queries.
- vorher 6.72.378: 2.222,09 ms Wall / 1.092,40 ms CPU / 89.461 Cache-Hits / 310 Queries.
- Differenz: Wall +9,61 %, CPU +3,21 %, Cache praktisch identisch, Queries +6.
- loop_start -> wp_footer: 1.492,57 -> 1.601,48 ms (+7,30 %).

Bewertung:
- 6.72.379 zeigt in diesem einzelnen Live-Gesamtlauf KEINEN messbaren Gesamt-Speedup.
- Ein kausaler Rückschritt durch H+I ist daraus ebenfalls nicht bewiesen.
- Kontrollrouten ohne Pferdesättel-Hotpath: CPU-Median ca. -0,06 %, also praktisch unveränderte Server-CPU-Basis.
- Serverlast im 6.72.379-Lauf war nicht höher; OPcache-Neustartnähe ähnlich.
- Gleichzeitig haben sich andere Plugins/Bestände verändert: Relevanssi 4.28.9->4.28.10, Texterstellung 0.4.51->0.4.55, WPForms Lite 2.0.5.1->2.0.5.2; Pferdesättel hat +6 Queries.
- der lokal isolierte H+I-Kausalbeweis bleibt bestehen: direkte Teilabschnitte -75,30 % / -71,66 %, finaler Realpfad im Re-Extract-ZIP -7,31 %, Fachausgabe identisch.
- Live-Gesamtbeweis für H+I ist wegen der kleinen erwarteten Einsparung (~15 ms im lokalen ~200-ms-Pfad) gegenüber der Gesamtrauschbreite dieses Einzelrequests nicht erbracht.

Funktionsschutz 6.72.379:
- 2.721/2.721 Kampagnennormalisierungen Alt=Neu.
- 25/25 reale Seiten-/Providerkombinationen Alt=Neu.
- 75/75 gerenderte Produktkarten inkl. HTML Alt=Neu.
- dynamische Filter-/Object-Cache-Fälle und echte Mutationen Alt=Neu.
- 0 Funktionen entfernt/neu; geändert nur zwei bestehende Funktionen im bewiesenen Zielzuordnungspfad.

Nächster Arbeitsstand:
- kein neues Plugin nur wegen dieses PASSIV-Laufs.
- 6.72.379 bleibt aktuell installiert; kein bewiesener Anlass für Rückbau.
- weitere Performancearbeit ausschließlich an neu isolierten Restblöcken; erst mehrere einzeln kausal belegte Maßnahmen gemeinsam in einen nächsten Kandidaten.


VERBINDLICHE KORREKTUR DES FREIGABESTANDARDS:
- Der bisherige Standard war zu schwach: Teilpfad-/isolierter Realpfad-Speedup allein reicht NICHT mehr.
- 6.72.379 hätte nach dem neuen Standard nicht ausgegeben werden dürfen, weil der komplette lokale Seitenpfad nicht als klarer Gesamt-Speedup vor Release nachgewiesen war.
- Ab jetzt gilt: kein neues Plugin ohne vollständige lokale Alt/Neu-Seitensimulation, wiederholte Gesamtpfadmessung UND inhaltlichen 1:1-Funktionsbeweis.
- Live dient nur noch zur Bestätigung eines vorher vollständig lokal bewiesenen Gewinns.
- Verbindliche Regel: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PERFORMANCE_FREIGABEREGEL.md
