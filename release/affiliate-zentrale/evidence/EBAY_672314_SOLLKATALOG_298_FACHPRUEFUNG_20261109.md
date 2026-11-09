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

## Akzeptanzkriterien für eine weitere Plugin-Version

1. **Kaufbaren eBay-Sollkatalog fachlich prüfen und freigeben** (Versicherungen ausgeschlossen, 28 Prüfbedarfe prioritär). Keine erfundenen Angebotstreffer und keine unbewiesene Vollständigkeit.
2. Für jedes freigegebene Ziel tatsächliche BUSINESS-Produkte oder einen **präzise belegten Fehlgrund** speichern; bereits gültige Datensätze wiederverwenden, stale Daten nur gezielt prüfen. Kein separater Worker, keine zusätzliche Datenbanktabelle, keine K0-Änderung.
3. Ein vollständiger realer WordPress/eBay-Lauf muss ohne Neustart (Timeout-/Cursor-/Sperrtest) enden; technische Fehlliste auswerten.
4. Reale Ausgabe am Produktziel, Artikel, Kategorie und Handy prüfen, einschließlich Sechs-Stunden-Frische.
5. **Lokale Simulation allein ist keine Produktivfreigabe.** Kein weiterer Versionssprung ohne messbaren, echten Mehrwert.

**Separat nachprüfbare lokale Dateien aus demselben Audit:** `Pferdeatelier_eBay_298_Familien_Audit_2026-11-09.md` sowie eine CSV mit allen **324 Pflichtvertragspositionen** mit Markierung AUSGESCHLOSSEN / FACHLICH_PRUEFEN / IM_SOLLKATALOG. Die CSV ist eine Prüfhilfe, nicht die Freigabeliste.
