# Aktuelles Performance-Plugin

Stand: 25.11.2026

LIVE:
- Affiliate-Zentrale 6.72.380.
- Live-Source-Fingerprints entsprechen exakt dem freigegebenen Paket:
  Hauptdatei 3dddbb387cac24dbe4492fb507cee5c8c109db3de9b59b20ecf05616d1c7fc91
  eBay-Trait a2e621a9680b2a33bc2fa5364d20862c7282805158bc4c29c1e7c5d736d6b660

PASSIV-LAUF 2026-11-25 10:24:
- Pferdesättel 6.72.380: 3.102,79 ms Wall / 1.135,25 ms CPU / 89.460 Cache-Hits / 310 Queries.
- 6.72.379 davor: 2.435,59 ms Wall / 1.127,46 ms CPU / 89.460 Cache-Hits / 316 Queries.
- CPU: +0,69 % = kein messbarer Speedup.
- Vergleichsrouten ohne Pferdesättel: CPU-Median ca. -3,36 %.
- Damit zeigt der Affiliate-Hotpath relativ zu den Kontrollen keinen Live-Gewinn.
- Wall ist wegen stark anderer Serverlast nicht kausal vergleichbar; aktueller Load 45/72/132 gegenüber vorher 44/48/52.

WICHTIGE KORREKTUR ZUR LOKALEN SIMULATION:
- der bisher als Vollpfad bezeichnete Test war der vollständige Affiliate-Drei-Slot-Ausgabepfad, NICHT ein vollständiger WordPress-Seitenrequest.
- Testdaten: echte WXR-Kampagnen/Page-Daten, aber NICHT die reale 8.114-Zeilen-Tabelle slfo_ppar_ebay_items.
- Für diesen Teil wurden deterministische Ersatz-Source-Zeilen erzeugt.
- deshalb darf der dort gemessene -46,61-%-Wert NICHT als Beweis für einen vollständigen WordPress-Seiten-Speedup verwendet werden.
- dieser Harness bleibt für Fachregressionen und interne Hotpath-Messung brauchbar, ist aber für Release-Geschwindigkeitsfreigaben ab jetzt gesperrt.

FUNKTIONSSCHUTZ:
- die inhaltlichen Regressionen von 6.72.380 bleiben gültig für die geprüften Fachpfade: 2.721/2.721 Kampagnen, 25/25 Konfigurationen, 75/75 gerenderte Karten, 2.955/2.955 Policyfälle sowie dynamische Sicherheitsfälle Alt=Neu.
- dies beweist Funktionsgleichheit der geprüften Fachlogik, nicht die Vollständigkeit einer realen WordPress-Kopie.

NÄCHSTER ARBEITSSTANDARD:
- kein neues Affiliate-Plugin.
- kein Release mehr aus WXR+Stub-Performanceharness.
- neuer Kandidat erst, wenn entweder eine echte lokale WordPress-Kopie mit vollständiger DB/Plugins/Themes inklusive slfo_ppar_ebay_items verfügbar ist oder ein realer Ursachenprofil-Lauf die betroffene Live-Ausführungsstrecke kausal isoliert.
- Live 6.72.380 bleibt vorerst installiert; kein kausaler Rückschritt im CPU-Wert bewiesen und Rückbau würde eine unnötige weitere Installation erzeugen.
