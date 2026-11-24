# Pferdeatelier Affiliate-Zentrale 6.72.376 – gebündelter Context-Read-Rootfix

Stand: 24.11.2026
Basis: live 6.72.375
Paket: PFERDEATELIER_AFFILIATE_6.72.376_GEBUENDELT_CONTEXT_READ_ROOTFIX.zip
SHA-256: ec15beafe4944eddcffc8401081c31f7d330546497fab9dd3e3f4661e0245b45

## Live-Ausgangspunkt
- 6.72.375 Pferdesättel: 2.583,26 ms Wall / 1.214,68 ms CPU / 135.828 Cache-Hits / 310 Queries.
- Gegen 6.72.374 blieben Cache-Hits und Queries exakt unverändert; der große 6.72.375-Liveeffekt ist daher nicht bewiesen.
- 6.72.376 übernimmt deshalb nur neue Änderungen mit direktem Ursachenbeweis.

## Gebündelte direkte Ursachen
1. Portal/Home-Kontext:
- Ausrüstung 3.024 -> 3 home_url-Aufrufe.
- Sattel 513 -> 3.
- Pferdesättel 3.030 -> 3.
- jeweilige finale drei Produkte Alt=Neu.

2. Idealo-Rohoption:
- ppar_network_idealo_v1 auf Ausrüstung/Sattel/Pferdesättel jeweils 11 -> 3 Aufrufe.
- Amazon-Option bleibt 3 -> 3.
- finale Produktwahl Alt=Neu.

Keine Kandidaten-, Ranking-, Control-, Health-, Bild-, Provider-, Mehranbieter- oder Fallbackprüfung wird entfernt.

## Semantik-/Funktionsbeweis
- 2.721/2.721 Kampagnennormalisierungen identisch; SHA Alt=Neu c9e6d78082e8ca9ba805f3906522842a14e4bd75a6c0b6f430d1cb9c0204b7c9.
- Pferdesättel Shared Pool 1.010/1.010 identisch; SHA Alt=Neu 8a08f74d448428600a8d017cde8d2185333d9cd43639fa4ad1f582cf9ff17132.
- 30/30 Provider-Modus × Linkstrategie × Amazon: kompletter Postprocessing-Output identisch.
- 10/10 finale Drei-Slot-Auswahlen identisch.
- 10.000 Meta-Sonderfälle weiterhin 0 Abweichungen; Meta-Logik selbst unverändert.
- Dynamischer Metadata-Fall A->B Alt=Neu.
- Home A->B und Idealo Hybrid->Produkte während desselben Slots werden nach echter Option-Invalidierung sofort gesehen.
- externer Objektcache, home_url-Filter, Idealo-Optionsfilter und globales pre_option erzwingen für die jeweils betroffene neue Optimierung den historischen Einzelweg; Ausgabe Alt=Neu.

## Vollständiger Bestandsschutz
- Dateien 66 -> 66; entfernt 0; hinzugefügt 0.
- geändert nur Hauptdatei, trait-ppar-idealo.php und readme.txt.
- PHP-Dateien 23 -> 23.
- benannte Funktionen/Methoden 1.581 -> 1.585; entfernt 0.
- 1.576 bestehende Funktionen token-inhaltlich unverändert.
- geändert genau 5 bestehende Funktionen; neu 4 interne Hilfsfunktionen.
- kritische Auswahl-/Ranking-/Provider-/Fallback-/Health-/Bild-/Tracking-/Renderfunktionen token-identisch.
- Filter 30 -> 30; Shortcodes 6 -> 6.
- Actions 176 -> 179; die 3 neuen Actions sind nur added_option/updated_option/deleted_option zur Invalidierung der zwei neuen Lesesnapshots.
- sämtliche Produktions-Schreibprimitive unverändert.

## Paketprüfung
- ZIP 66/66, fehlend 0, zusätzlich 0, Hashabweichungen 0.
- PHP-Lint Arbeitsstand 23/23 PASS.
- PHP-Lint nach Re-Extract 23/23 PASS.
- Header/Klassenkonstante/Stable Tag 6.72.376.
- ZIP enthält ausschließlich affiliate-portal-router/.

## Grenze
Bewiesen ist reduzierte Wiederholungsarbeit bei identischer fachlicher Ausgabe. Ein Live-Speedup wird erst nach genau einem PASSIV-Lauf nach Installation behauptet.
