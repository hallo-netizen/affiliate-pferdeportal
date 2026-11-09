# Pferdeatelier eBay: nachgeprüfte 298-Sollfamilien (09.11.2026)

**Quelle und Reproduzierbarkeit:** tatsächlich geöffnete lokale Originalbasis-Test-ZIP `Pferdeatelier_Affiliate_6.72.314_KISS_Gesamtworkflow_TEST.zip`, SHA-256 `2a4dc2954bf76b560583667d81c91c827fb6835754bcd58439bce1fda5f95f18`. Es wurde die komplette `assets/ebay-portal-catalog-v2.json` sowie die Quellmethode `ebay_business_required_product_concept_ids()` in `includes/trait-ppar-ebay.php` geprüft. **Keine Quelländerung, kein Release, kein WP-Eingriff.**

## Harte Erklärung der 298

- 329 `business_concepts` im statischen Katalog.
- 5 allgemeine Grundlagen-Konzepte **nicht** in dem Pflichtvertrag.
- `business_supply_contract.required_count` = **324**, Liste mit **324 tatsächlich unterschiedlichen IDs**.
- `ebay_non_goods_concept_ids` = **26** IDs; **sämtliche 26** sind im Pflichtvertrag enthalten und werden von der echten PHP-Funktion ausdrücklich entfernt.
- **324 - 26 = 298** Pflichtkonzepte. Die angezeigte Zahl ist daher **technisch richtig**.
- Ausgeschlossen sind ausdrücklich `Pferde-OP-Versicherung`, `Pferdekrankenversicherung`, `Pferdehaftpflicht` sowie Rechts-, Beratungs-, Vorlagen- und Checklistenbereiche. **Keine Versicherung in den 298**.
- **Aber:** Es wurde **noch keine fachliche Güteprüfung** des 298er-Katalogs für konkrete, aktuell kaufbare eBay-BUSINESS-Ware nachgewiesen. Die bloße Erfassung eines Themas in einer Site-Struktur rechtfertigt keine eBay-Produktpflicht.

## 28 Themen im 298er-Katalog, die als kaufbare Warenfamilie vor einer Pflichtforderung konkretisiert werden müssen

1. Bahnplaner
2. Bande & Spiegel
3. Beregnung & Bewässerung
4. Dachrinnen am Unterstand
5. Erdung beim Weidezaun
6. Festzäune für Pferde
7. Hallenklima & Belüftung
8. Heulagerung
9. Hofabsperrungen
10. Liegeflächen im Offenstall
11. Mineralbar im Stall
12. Mistlagerung
13. Offenstall-Bodenbefestigung
14. Offenstallbau
15. Paddockbau
16. Reithallenbau
17. Reithallenboden
18. Reitplatzbau
19. Reitplatzbewässerung
20. Reitplatzboden
21. Reitplatzdrainage
22. Reitplatzplaner
23. Satteltransport
24. Unterstand-Boden
25. Waschplatz für Pferde
26. Wasserleitungen im Stall
27. Weidepflegegeräte
28. Windschutz für Pferde

**Keine pauschale Streichung:** Bei einigen Begriffen existieren selbstverständlich käufliche Waren, aber der aktuelle Sammelbegriff ist zu weit. Für jedes dieser Ziele zuerst die konkrete Warengruppe fachlich festlegen; danach erst entscheiden, ob die Pflichtzahl kleiner wird oder einzelne Ziele umformuliert werden. Die übrigen 270 Ziele sind ebenfalls nicht automatisch bestätigt, sondern zunächst strukturell plausiblere Warenbezeichnungen.

## Tatsächliche Nutzerrückmeldung (09.11.2026, 14:01 Uhr)

Laufstatus `business_materialize / business_prune`, Paket 366, aktiv 271, Katalog-Zwischenstand **110/298** (188 offen). Dies ist nicht als öffentliche eBay-Produktabdeckung bestätigt; `ebay_business_selection_coverage()` misst ausgewählte aktive Konzepte, nicht alle Live-Karten/Links. Kein Beleg für Endabnahme.

## Datenwiederverwendung / wirtschaftliche Ursache

`ebay_upsert_item()` der originalbasierten ZIP führt anhand `portal_key + item_id` ein Update existierender Datensätze aus, kein blindes immerwährendes vollständiges Löschen. Ein Datenfeld `fresh_until` ist fest `source_checked_at + 6 Stunden`; ältere Ergebnisse dürfen nicht als aktuell öffentlich ausgegeben werden. **Trotz dieser Speicherung ist ein erneut gestarteter kompletter Discovery-Lauf keine fachliche Abdeckungsverbesserung.** Die Laufsteuerung und das Wiederverwenden bestehender, noch gültiger Datensätze müssen gesamthaft bei der nächsten Codeänderung vor eine teure neue Vollsuche gestellt werden, ohne Frische- oder Sicherheitssperren zu umgehen.

## Nachtrag 09.11.2026 – Historienabgleich und SCHLÜSSELFEHLER DER BEHAUPTETEN MARKTABDECKUNG

**Wahrheitsgrenze:** Zum Snapshot 14:01 (110/298) liegen uns **nur Summen**, kein aus der WordPress-Datenbank exportierter `missing_concepts`-Datensatz mit exakt 188 IDs vor. Das Plugin berechnet und persistiert ihn bereits: `ebay_business_selection_coverage()` gibt `missing_concepts` als konkrete IDs aus; `ebay_business_recovery_missing_concept_ids()` liest sie gezielt. Die Admin-Ansicht zeigt nur `missing` als Anzahl. Die 28 zuvor als unklare Baubereiche markierten Katalogthemen sind **NICHT** als Mitglied der tatsächlich 188 Fehlstellen nachgewiesen und **keine eBay-Angebotsabfrage**. Es wäre falsch, diese 28 als neu „aus eBay ausgeschlossen“ oder „nicht bei eBay erhältlich“ zu behaupten.

**Harter Quelltest auf vollständiger 314-Test-ZIP:** In der von WordPress installierbaren ZIP gespeicherter Katalog enthält **298 Pflichtkonzepte**, aber nur **4** davon haben einen individuell hinterlegten `ebay_search_term`. Für **294** wird der allgemeine Seitentitel als Suchbegriff verwendet (und abhängig vom Kontext `Pferd` angefügt). Die exakten Suchprofile `ebay_business_catalog_profiles()` begrenzen jede einzelne Pflichtkatalog-Abfrage auf **eine Seite** (`page_limit=1`) und **max. 30 angebotene Ergebnisse** (`request_limit=30`). Das wurde im vorhandenen **Quellcode** nachgewiesen, nicht als Grund für 188 Live-Lücken bewiesen. Ein fehlendes oder abgelehntes Ergebnis daraus beweist NICHT, dass eBay das entsprechende Produkt nicht anbietet. Die historischen Tests haben oft Verfügbarkeit, Güteprüfung, Portal-Routing und öffentliche Kampagnen vermischt.

**Existierende Datenquellen (ohne neuen Lauf):** `ebay_sync_summary_new()` persistiert je Suchprofil `profile_stats` mit `expected_business_concept_id`, `query`, `requests`, `received`, `accepted`, `review_pending`, `hard_blocked`, `technical_blocked`, `complete`, `stopped_reason`. Die Provider-Seite kann unter **„Technische Details zum eBay-Abruf“** das vorhandene `last_sync`-JSON rein lesend anzeigen. Der interne `missing_concepts`-Array steckt in `ebay_selection_state_load().plan_stats.business.missing_concepts`, wird aber **noch nicht als einzelne Liste** angezeigt. Die vorhandene Portalabdeckungsseite (`admin.php?page=affiliate-portal-coverage`) hat einen rein lesenden Knopf **„Vollständigen JSON-Prüfbericht herunterladen“** mit realen Zielseiten und eBay-/idealo-Kampagnen; dies ist ein Frontend-Kampagnenbericht, **kein eBay-Marktplatz-Negativbeweis**.

**Erforderlicher echter 188er-Beleg:** Aus **demselben** WordPress-Lauf einen READ-ONLY-Export der **188 exact fehlenden IDs** und der zugeordneten eBay-Suchprofil-Befunde erzeugen. Für jede ID drei strikt getrennte Tatsachen: (1) eBay-BUSINESS-API hat aktuell qualifizierbare echte Artikel mit konkreter Artikel-ID/URL zurückgegeben; (2) zwar Ergebnisse, aber systemseitig abgelehnt, mit echtem Grund; (3) Suche technisch nicht vollständig oder keine qualifizierten Treffer in den abgefragten Seiten. **Gruppe 3 ist niemals die Aussage „nicht auf eBay verfügbar“**. Fehlende WordPress-Laufdaten dürfen nicht durch synthetische Offline-Simulation, einen alten 324er-Snapshot oder reine Suchmaschinen-Treffer ersetzt werden.

**Status:** Kein Einzelbeleg der 188, keine reale eBay-API-Verifikation, **keine Endabnahme und kein neues Plugin**. Der Nutzer fordert zurecht die tatsächliche Klassifizierung statt wiederholter Katalog-Zählungen. Die 298er-Fachkatalogprüfung darf NICHT als nächste Neubau-Aufgabe umetikettiert werden; historische 6.72.303-Nichtwarenbereinigung und 6.72.307-Reitplatzplanerentscheidung sind bereits erledigt.

## Akzeptanzkriterien für eine weitere Plugin-Version

1. **Kaufbaren eBay-Sollkatalog fachlich prüfen und freigeben** (Versicherungen ausgeschlossen, 28 Prüfbedarfe prioritär). Keine erfundenen Angebotstreffer und keine unbewiesene Vollständigkeit.
2. Für jedes freigegebene Ziel tatsächliche BUSINESS-Produkte oder einen **präzise belegten Fehlgrund** speichern; bereits gültige Datensätze wiederverwenden, stale Daten nur gezielt prüfen. Kein separater Worker, keine zusätzliche Datenbanktabelle, keine K0-Änderung.
3. Ein vollständiger realer WordPress/eBay-Lauf muss ohne Neustart (Timeout-/Cursor-/Sperrtest) enden; technische Fehlliste auswerten.
4. Reale Ausgabe am Produktziel, Artikel, Kategorie und Handy prüfen, einschließlich Sechs-Stunden-Frische.
5. **Lokale Simulation allein ist keine Produktivfreigabe.** Kein weiterer Versionssprung ohne messbaren, echten Mehrwert.

**Separat nachprüfbare lokale Dateien aus demselben Audit:** `Pferdeatelier_eBay_298_Familien_Audit_2026-11-09.md` sowie eine CSV mit allen **324 Pflichtvertragspositionen** mit Markierung AUSGESCHLOSSEN / FACHLICH_PRUEFEN / IM_SOLLKATALOG. Die CSV ist eine Prüfhilfe, nicht die Freigabeliste.
