# Pferdeatelier – Performance-Ursachenaudit 2026-11-19

Status: **ANALYSE / KEINE PLUGINÄNDERUNG**

## Ergebnis in einem Satz
Die jüngsten Änderungen 6.72.357 -> 6.72.358 -> 6.72.359 sowie Template 1.50.615 -> 1.50.616 haben nach der erneuten lokalen Quell- und Semantikprüfung **keine Funktion entfernt**. 6.72.359 ist durch den aktuellen Lauf **nicht als Ursache der Verschlechterung bewiesen**; die von 6.72.359 adressierten Options-Einzelreads sind sogar gesunken. Das grundsätzliche Performanceproblem ist auf GitHub bereits seit 21.09.2026 dokumentiert.

## Aktueller Messvergleich
Vorheriger belegter Stand 6.72.358 + 1.50.616:
- Frontend Ø 3.856,22 ms
- Median 3.799,36 ms
- CPU Ø 2.139,51 ms
- Queries Ø 312,24
- DB Ø 758,52 ms
- Options-Einzelreads Ø 130,47 pro Frontend
- Browser-TTFB Ø 4.207 ms
- LCP Ø 4.619 ms
- p95 4.906 ms

Aktueller Stand 6.72.359 + 1.50.616:
- Frontend Ø 5.405,77 ms
- Median 4.115,58 ms
- CPU Ø 2.344,11 ms
- Queries Ø 298,53
- DB Ø 964,87 ms
- Options-Einzelreads Ø 116,07 pro Frontend
- Browser-TTFB Ø 5.605,12 ms
- LCP Ø 5.910,22 ms
- p95 10.919 ms

Bewertung:
- Queries insgesamt niedriger.
- Zielgruppe der Options-Einzelreads niedriger.
- Wall-Time und DB-Zeit trotzdem höher.
- Deshalb keine zulässige Kausalaussage "6.72.359 macht die Seite langsamer".
- Der aktuelle Lauf begann 49 Sekunden nach dem letzten im Diagnosebericht gespeicherten OPcache-Restart. Zusätzlich gab es Parallelrequests. Das macht ihn als reine A/B-Zeitmessung ungeeignet.

## Eigene lokale Funktions- und Semantikprüfung

### Affiliate 6.72.357 -> 6.72.358
- 66 -> 66 Dateien
- 1.551 -> 1.551 benannte PHP-Funktionen
- entfernt: 0
- hinzugefügt: 0
- Signaturänderungen: 0
- genau ein Funktionskörper geändert: output_finalize_digistore24_object()
- eBay/Idealo/Amazon/Automation/Output/Control geschützt unverändert
- 23/23 PHP-Dateien Lint PASS

64-Fall-Zustandssimulation:
- normale Erfolgs-/Fehlerpfade erhalten
- einzige Abweichung: bei bereits aktiver Digistore-Kampagne entfällt der redundante erneute Campaign-Schreibversuch. Wenn genau dieser unnötige Schreibversuch früher fehlschlug, kann der neue Pfad weiter bis zur eigentlichen Output-Persistenz laufen.
- Das ist kein Funktionsabbau, aber deshalb wird ausdrücklich **nicht** behauptet, der interne Ablauf sei in jedem künstlichen Fehlerfall bit-/verhaltensidentisch.

### Affiliate 6.72.358 -> 6.72.359
- 66 -> 66 Dateien
- 1.551 -> 1.552 Funktionen
- entfernt: 0
- hinzugefügt: 1, prime_init_guard_options_v672359()
- Signaturänderungen: 0
- 1.550 vorhandene Funktionskörper unverändert
- bestehend geändert nur Konstruktor zur Registrierung des neuen init-Hooks
- eBay-Funktionen 471 -> 471; 0 entfernt, 0 hinzugefügt, 0 Funktionskörper geändert
- 23/23 PHP-Lint PASS

Lokale Options-Simulation:
- Werte vor/nach Prime identisch
- normale WordPress-Invalidierung nach update_option liefert danach den frischen Wert
- keine bestehende get_option-Entscheidung wurde ersetzt oder abgeschaltet

### Template 1.50.615 -> 1.50.616
- 504 -> 504 Dateien
- 721 -> 721 Funktionen
- entfernt: 0
- hinzugefügt: 0
- Signaturänderungen: 0
- genau ein Funktionskörper geändert: direct_published_page_children()
- Hooks 165 -> 165
- 7/7 PHP-Lint PASS

Erneute lokale Semantik-Simulation:
- 500 Zufallsbestände mit je 424 Seiten
- 50.000 Elternabfragen alt gegen neu
- Abweichungen: 0
- 250 Mutationsschritte, 5.000 Zusatzprüfungen
- Abweichungen: 0

## Historie
GitHub-Evidence vom 21.09.2026 dokumentiert bereits bei 6.72.142:
- 13.671 DB-Queries auf einer Problemseite
- ca. 10,323 Sekunden Serverzeit
- 11.297 wiederholte Control-Lookups
- 1.484 eBay-BUSINESS-Lookups
- 305 Creative-Library-Lookups

Am 01.10.2026 ist bereits dasselbe Seitenmuster dokumentiert:
- /ausruestung/ ca. 1,65 s
- tiefere Kategorie-/Produktseiten ca. 8,62 bis 9,09 s
- damaliger Hotspot: wiederholter PHP-Ranking-/Gate-/Providerpfad der drei category_product-Slots

Aktueller Lauf:
- Home Ø ca. 4,70 s
- Top-Hubs Ø ca. 3,23 s
- fünf Kategorie-/Produktseiten Ø ca. 8,31 s

Damit ist das historische Kategorieprodukt-Muster wieder sichtbar.

## Nächster belegter Kandidat – noch NICHT als Ursache freigegeben
Vergleich 6.72.211 -> 6.72.359:
Fünf geschützte Ranking-/Request-Cache-Funktionen sind textinhaltlich unverändert.
Verändert haben sich unter anderem:
- select_category_product_campaign_fast_v672171()
- ranked_campaigns_for_slot()
- category_product_provider_mix_v672133()

Der heutige Pfad sammelt mehr Kandidaten über Relevanzbänder und kann bei weniger als drei Treffern zusätzlich product_fill_verified_portal_fallback_v672226() durchlaufen. Das passt zum aktuellen und historischen Tiefenkategorie-Muster. PASSIV misst aber nicht die Laufzeit genau dieser privaten Methoden. Deshalb ist das ein **starker Prüf-Kandidat, keine bewiesene alleinige Ursache**.

## Hard Rule
Keine Funktion abschalten, keine Auswahlregel entfernen, keinen Provider-/Veto-/Fallback-/Slot-Pfad kürzen, solange nicht vorher/nachher dieselben Kampagnen und dieselbe Ausgabe nachgewiesen sind.

## Nächster Schritt
Ohne Codeänderung kontrollierter warmer PASSIV-Readback auf einer festen URL-Gruppe und ohne parallele Admin-/Kubio-/eBay-Aufrufe. Erst wenn das Kategorieprodukt-Muster reproduzierbar bleibt, gezielte reine Zeitmessung um den Kategorie-Auswahlpfad. Danach erst darf über eine Optimierung entschieden werden.
