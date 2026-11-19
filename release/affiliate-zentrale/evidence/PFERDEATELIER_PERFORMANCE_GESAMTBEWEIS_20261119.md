# Pferdeatelier – Performance-Gesamtbeweis 19.11.2026

## Auftrag
Keine Ursache raten. Jede Aussage auf Source, Paket, Messbericht oder Historienbeleg stützen. Keine Produktionsfunktion stillschweigend entfernen. Änderungen und Grenzen offen benennen.

## Kernbeweise
- Diagnose 5.0 -> 6.0, erneute PHP-Tokenizer-Prüfung: 111 -> 134 benannte Funktionen/Methoden; entfernt 0; neu 23; 91 bestehende vollständig unverändert; 20 bestehende Diagnosefunktionen bewusst geändert. Eine Signatur erweitert: write_snapshot(...,$stage='latest') mit Defaultwert.
- Statische bestehende Hook-Registrierungen Diagnose 5.0 -> 6.0: 30 -> 30; entfernt 0. PASSIV registriert keine neuen 42 Profil-Messcallbacks.
- Diagnose 6.0 schreibt keine Posts/Terms/Meta/Cron/Cache-/direkten DB-Daten. WordPress-Write nur eigene Sessionoption; Dateien nur eigener Tempbereich.
- Affiliate 6.72.357 -> 6.72.358: 1551 -> 1551 benannte Funktionen; entfernt 0; 1550 vollständig unverändert; genau output_finalize_digistore24_object geändert. Bewusster Sonder-Fehlerpfad: bereits aktive Kampagne überspringt redundanten Aktivierungs-Write.
- Affiliate 6.72.358 -> 6.72.359: 1551 -> 1552; entfernt 0; neu prime_init_guard_options_v672359; 1550 bestehende vollständig unverändert; eBay-Kerndateien unverändert.
- Template 1.50.614 -> 1.50.615: 720 -> 721; entfernt 0; neu eine Schutzfunktion; zwei bestehende Bodies geändert.
- Template 1.50.615 -> 1.50.616: 721 -> 721; entfernt 0; 720 vollständig unverändert; genau direct_published_page_children geändert. Neue unabhängige Semantiksimulation: 50.000 Alt/Neu-Elternabfragen + 5.000 Mutationschecks, 0 Abweichungen.
- Reale 1.50.616-Wirkung: 813 identische Child-Page-Queries / 2102,67 ms -> 0; Frontend-Ø 6177,84 -> 3856,22 ms; DB-Ø 1447,44 -> 758,52 ms.

## Historie
- 21.09.2026 / 6.72.142: 13.671 DB-Queries und ca. 10,323 s Serverzeit dokumentiert. Das Problem ist damit älter als die Novemberänderungen.
- 01.10.2026 / 6.72.171: Top-Kategorie ca. 1,65 s, tiefe Kategorieproduktseiten ca. 8,62–9,09 s. Exakt derselbe Hierarchie-/Produktkarten-Typ wie heute.
- 6.72.171 Shared-Ranking: Snapshot-A/B 1248,595 -> 249,597 ms (-80,01 %), mit identischen ausgewählten Kampagnen, HTML-Hashes, Reihenfolgen und Kandidatenzahlen.
- 6.72.176 Preservation-Recheck bestätigte den 6.72.171-Performancepfad; 6.72.208 KISS änderte Ranking/Banner-/Produktausgabe nicht.

## Aktueller Stand 6.72.359 + 1.50.616
- 15 Frontendrequests: Ø 5405,774 ms, Median 4115,58 ms, CPU Ø 2344,111 ms, Queries Ø 298,53, DB Ø 964,87 ms.
- tiefe Kategorien: Sattel 14.072,27 ms; Pferdesättel 11.011,15 ms; Futtertechnik 7349,87 ms.
- 6.72.359-Zielwert Options-Einzelreads verbesserte sich 130,47 -> 116,07 pro Request (-11 %). Daher keine Kausalität für die schlechtere Gesamtzeit bewiesen.
- Wall-Time-A/B ist konfundiert: Session nur 49 s nach OPcache-Restart, 87,04 % Hitrate, 4077 Misses, 28 manuelle Restarts, max. 4 parallele Requests.

## Wichtigster belegter späterer Veränderungspunkt
Vergleich formaler 6.72.211-Hauptrouter gegen lokalen 6.72.359:
- fünf geschützte Ranking-/Request-Cache-Funktionen bleiben textinhaltlich gleich.
- select_category_product_campaign_fast_v672171 enthält später zusätzliche Multi-Provider-/Mehrband-/Fallback-Arbeit.
- category_product_provider_mix_v672133 wurde ebenfalls erweitert.
Diese Änderungen sind konkrete Performance-Kandidaten, aber noch kein Kausalbeweis. Wegen Funktionsschutz dürfen sie nicht blind entfernt werden.

## Harte Schlussfolgerung
1. In den heute erneut geprüften Original-ZIPs 357->359 und 614->616 wurde keine bestehende benannte Produktionsfunktion entfernt.
2. Pauschal „nichts verändert“ wäre falsch; einzelne Funktionen wurden gezielt verändert und ihre Wirkung wurde separat geprüft.
3. Diagnose 6.0 verändert keine Produktionsdateien, aber bewusst ihre eigene Messlogik.
4. 1.50.616 nicht zurückbauen: echter positiver Messbeweis.
5. 6.72.359 nicht als Ursache zurückbauen: Zielwert verbessert, Kausalität der Wall-Time nicht bewiesen.
6. Das Performanceproblem ist historisch älter.
7. Nicht aus Archiv beweisbar: ein einzelner Live-Stand mit sämtlicher heutiger Funktionalität und gleichzeitig überall schneller Laufzeit.
8. Diagnose 6.0 kann den vollständigen aktuellen Kategorieprodukt-Filterpfad pftk_leaf_category_affiliate_slot_html messen; kein weiteres Diagnoseplugin nötig.

## Nächster Schritt
Keine Produktionsänderung. Einen URSACHENPROFIL-Lauf mit Diagnose 6.0 auf einer nachweislich langsamen tiefen Kategorie erzeugen. Erst wenn der Kategorieproduktpfad den Zeitblock trägt, weiter innerhalb dieses Pfads eingrenzen. Jede spätere Optimierung muss identische Kampagnen, Reihenfolge, Provider-/Fallbackregeln, Veto, Tracking und HTML-Ausgabe beweisen.
