# Pferdeatelier eBay QA9 – Ablehnungen tatsächlich im PHP-Code reproduziert

**Stand: 10.11.2026. Quellen: vom Nutzer hochgeladener CSV-Export `Pferdeatelier_eBay_fehlende_Produktfamilien_3e9e9207-d82.csv` (138 Familien), vollständiger unmodifizierter Plugin-Stand `6.72.321 QA9` und direkter Aufruf des vorhandenen Klassifikators. Keine Änderungen an laufendem WordPress, Produktdaten, gespeicherten Angeboten oder Plugin-ZIP.**

## 1. Alle Ablehnungen im vorhandenen CSV konkret gezählt

- **138** offene Familien in diesem CSV-Snapshot; **94** davon haben im Suchausschnitt Angebote, die nicht angenommen wurden; **43** haben keinen Treffer im untersuchten Suchausschnitt; **eine** Familie (Verladetraining-Zubehör) hat `http_request_failed` und ist daher technisch ungeklärt.
- **258** Suchanfragen, **1.329** empfangene Treffer, **0** angenommene Treffer **für diese aktuell fehlenden CSV-Familien**. `blockiert`-Summe **764**. Die Summe der einzelnen Ablehnungsereignisse ist größer, weil die Zählfelder unterschiedliche Phasen/Ereignisse umfassen; sie sind **keine disjunkt zu addierenden 1.329 Produkt-Identitäten**.
- Ablehnungsereignisse: `ebay_marketplace_mismatch` **610**, `ebay_portal_topic_negative` **234**, `ebay_business_concept_missing` **179**, `ebay_portal_topic_missing` **96**, `ebay_toy_item_blocked` **80**, weitere 33/21/15/3/1/1.
- Unter den **94 Familien mit gefundenen Angeboten** dominiert als protokollierter Ablehnungsgrund bei **59** der Marktplatz, bei **13** die Negativprüfung und bei **9** die fehlende eindeutige Produktzuordnung. Bei **39 Familien** ist **ausschließlich** `ebay_marketplace_mismatch` als Ablehnungsart erfasst. Diese Häufigkeiten beziehen sich auf **Produktfamilien**, nicht auf einzelne Produktidentitäten.

## 2. Tatsächlich nachgewiesene Fehlentscheidungen im bestehenden Klassifikator

Im unmodifizierten `trait-ppar-ebay.php` / `ebay_business_classify_portal_item_strict()` via PHP 8.4 und dem **Originalkatalog** `assets/ebay-portal-catalog-v2.json` mit bewusst nachgestellten Produktbeispielen ausgeführt (reproduzierbar mit `EBAY_QA9_FULL_CLASSIFIER_REPRO_20261110.php`):

- **Pferdesättel**: Der Katalog sucht selbst ausdrücklich **`Dressursattel Pferd`** (Feld `ebay_search_term`), doch `Dressursattel Pferd` wird als **`ebay_business_concept_missing`** abgewiesen. Ebenso `Reitsattel Leder Pferd` und `Western Sattel Leder Pferd`. Das eigene Katalogwort `Pferdesattel Leder` wird dagegen akzeptiert. Der vorhandene allgemeine Nomen-Fallback liefert für Reitsattel lediglich einen Sattel-**Hub**, der bei der konkret geforderten Familie nicht als Treffer gilt. **Widerspruch zwischen eigener Suchanfrage und exakter Produktentscheidung belegt.** In der CSV dieser Familie: **60** Treffer, **12** mal `ebay_business_concept_missing`; ob unter diesen zwölf genau solche Titel sind, ist mangels Originalangebotstiteln im CSV **nicht bewiesen**.
- **Anhängerbeleuchtung**: `LED Rückleuchte Pferdeanhänger` wird durch den **bereits vorhandenen** Nomen-/Synonym-Fallback **korrekt** als `concept-anhangerbeleuchtung` erkannt – dieser Weg ist **NICHT neu zu bauen**. Fügt derselbe Musterartikel aber im reinen Beschreibungstext den Satz `Universelle Verwendung, auch für Motorrad` hinzu, wird er durch die globale Negativmarker-Prüfung `ebay_portal_topic_negative` verworfen, **obwohl Titel und Kategorie unverändert passend bleiben**. Eine Beschreibung mit `Für Anhänger und Pferdeanhänger` wird dagegen angenommen. In dieser CSV: **60** Treffer, **59** Negativereignisse; **welche genauen Marker die tatsächlichen 59 Artikel auslösten, enthält die CSV nicht**. Das Beispiel reproduziert die strukturelle Überblockierung für Mehrzweckware, ist keine Behauptung über den Wortlaut der 59 Originale.
- **Reitplatzschleppe**: Ein plausibler alternativer Produktname `Reitplatzplaner Pferd` wird für das exakt erwartete Konzept `concept-reitplatzschleppe` als `ebay_business_concept_missing` abgewiesen; `Reitplatzschleppe Pferd` wird angenommen. In der CSV 30 Treffer, davon 27 `ebay_business_concept_missing`. **Ob die 27 realen Artikel Reitplatzplaner sind, ist nicht aus dem CSV ableitbar.**

Diese Tests **führen die tatsächliche bestehende private Produktklassifikation aus**, nicht eine neu geschriebene Nachbildung. Die Rohartikel werden nur **für die reproduzierbaren Testfälle konstruiert**, nicht als tatsächliche eBay-API-Antworten ausgegeben. Die unveränderten Referenzfälle sind im ausführbaren Test mit enthalten.

## 3. Was kein belegter Plugin-Fehler ist

**610 Marktplatz-Ablehnungsereignisse:** `ebay_accept_item()` prüft das originale Feld `listingMarketplaceId` strikt auf `EBAY_DE`. Der Request fragt zwar mit `X-EBAY-C-MARKETPLACE-ID: EBAY_DE` an, aber `deliveryCountry:DE` bedeutet **Lieferbarkeit nach Deutschland**, nicht sichere deutsche Herkunft jedes zurückgegebenen Angebots. Der deutsche Marktplatz ist ein **bereits am 07.11. dokumentierter bewusster Filter**. Ohne Änderung dieses Geschäftsvertrags werden diese Treffer weiterhin ausgeschlossen. **Nicht** einfach den Nachweis überschreiben oder aus dem Lieferland ableiten.

`ebay_toy_item_blocked` und schlechte Verkäuferbewertungen sind als eigene bestehende Schutzregeln erfasst; weder diese Regeln noch Datenhistorien werden für höhere Abdeckung pauschal entfernt.

**43 Nulltreffer** beweisen bei einer begrenzten 1-Seiten-Suche nicht, dass eBay die Waren nicht anbietet. **1** technischer Abruffehler beweist ebenfalls keinen fehlenden Bestand.

## 4. Warum das vorher dauernd im Kreis ging / nachgewiesener nächster gezielter Eingriff

Die früher wiederholt vorgeschlagenen Aufgaben sind bereits im Code: gespeicherten Bestand wiederverwenden, zweiten Suchbegriff versuchen, eine Klassifikationsinstanz, mehrere Familien pro Produkt, Checkpoint und frühe QA9-Freigabe. **Sie sind nicht der neue nächste Fix.**

**Sinnvoller kleiner Ursachenfix im vorhandenen Klassifikator, erst nach Abgleich der Sicherheitsfälle:** (1) explizite, fachlich belastbare Aliasnamen für dieselbe verkaufte Produktart ergänzen, so dass der **bereits eigene** Suchbegriff `Dressursattel` auf die bestehende Pferdesättel-Familie abgebildet werden kann; (2) mehrzweckfähige Reitsport-Hardware nicht ausschließlich deshalb blockieren, weil im Beschreibungstext zusätzlich eine andere Nutzungsmöglichkeit erwähnt wird, **wenn ein unabhängig belegter exakter Produkttyp und Pferdekontext vorliegen**; echte Spielzeuge/anderes Tierzubehör weiterhin sperren. (3) Such-/Auswahl-/Freigabefunktionen nicht erneut bauen und den `EBAY_DE`-Filter nicht ungefragt öffnen.

**Freigabegrenze:** Der direkte PHP-Test beweist **Regelfehler für die angegebenen Beispielangebote**, nicht die genaue Zahl real zu Unrecht abgelehnter Artikel und noch keine reale Live-Abdeckung. Für die Zuordnung jedes echten Ablehnungsfalls bräuchte man die bisher nicht im CSV enthaltenen Originaltitel und den tatsächlichen Marker. Keine neue ZIP oder Live-Änderung aus diesem Bericht.