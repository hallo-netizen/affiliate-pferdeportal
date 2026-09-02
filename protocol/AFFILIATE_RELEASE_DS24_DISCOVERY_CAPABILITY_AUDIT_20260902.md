# DIGISTORE24 — DISCOVERY CAPABILITY AUDIT / ROOT-CAUSE GATE

Stand: 2026-09-02
Projekt: Pferde Atelier / Affiliate-Zentrale
Scope: ausschließlich automatische Ermittlung der bereits genehmigten Affiliate-Partnerschaften. Kein Pluginbuild.

## ERROR-REGISTER PRECHECK

Relevante Hardlocks: AFF-ERR-001, 002, 003, 004, 006, 008, 009, 010, 011, 012.
Zusätzlich neu erkannt: die Discovery-Routen `listMarketplaceEntries` und `getAffiliateCommission(product_ids=all)` wurden in früheren lokalen Builds erneut als autoritativ angenommen, obwohl reale Live-Evidence diese Annahmen bereits widerlegt hatte.

## AFF-ERR-012 — DS24 Affiliate-Partnerschaftsinventur mit falscher API-Autorität

**Symptom:** wiederholte lokale PASS-Stände, live aber 0/0 bzw. 1/1 statt der realen 18 genehmigten Partnerschaften.

**Belegte Root Cause:** `listMarketplaceEntries` ist keine verlässliche Inventur der eigenen Affiliate-Partnerschaften; `getAffiliateCommission(product_ids=all)` wurde trotz dokumentierter Parameterfähigkeit fälschlich als Affiliate-seitige Fremdvendor-Inventur interpretiert, obwohl der reale 53213-Fall dafür bereits gescheitert war. `validateAffiliate` benötigt bekannte Produkt-IDs und kann daher nicht entdecken.

**Nicht wiederholen:** Keiner dieser drei Wege darf ohne neuen realen Gegenbeweis als autoritative Partnerschafts-Discovery implementiert werden. Ein lokales Fixture darf die gewünschte Remote-Antwort nicht erfinden.

**POSITIV:** ein unterstützter read-only Remote-Kanal liefert ohne CSV-/ID-Vorfütterung alle 18 Kontroll-IDs.

**NEGATIV:** 17/18, 53213-only, Marketplace-only, Transaktions-only, fremde Identität oder synthetische Fixture-Antwort bleiben FAIL.

**GESAMTWORKFLOW:** erst nach Discovery-PASS `validateAffiliate -> Werbemittel -> Bild/Tracking -> Ziel/Slot -> Draft -> Revalidation -> Persistenz -> LKG -> Readback -> Reassignment`; Providerregression eBay/idealo/Awin.

**Status:** OPEN / Produktcode-Fix gesperrt bis Discovery-Capability real nachgewiesen.

## Reale Bindung

Kontrolloracle: 18 genehmigte Partnerschaften / 10 Vendoren. Die 18 Produkt-IDs dienen ausschließlich als Sollvergleich, nicht als Runtime-Discovery-Quelle.
Alte lokale Quelle 53213 darf nicht als Erfolg der Remote-Discovery gezählt werden.

Reale UI-Evidence vom 02.09.2026:
- `Affiliate-Ansicht -> Verkäufe & Partner -> Partnerschaften mit Vendoren` zeigt 18 Ergebnisse und einen sichtbaren `CSV-Export`.
- `Affiliate-Ansicht -> Verkäufe & Partner -> Contentlinks` zeigt im realen Konto auf der Übersichtsseite keine Produktliste. Die vorherige Annahme, diese Übersicht liefere unmittelbar eine vollständige Produkt-/Partnerschaftsauswahl, ist damit für diesen realen Ablauf widerlegt und darf nicht als Discovery-Evidence verwendet werden.

## Capability-Ergebnis

### 1. listMarketplaceEntries — FAIL als autoritative Discovery
Historische Live-Evidence: API lieferte `data.entries=[]`, obwohl in der Affiliate-Oberfläche tausende Marketplace-Produkte sichtbar waren. Zusätzlich ist Marketplace-Inventar fachlich nicht identisch mit der Liste eigener genehmigter Vendor-Partnerschaften.

### 2. getAffiliateCommission(product_ids=all) — FAIL als autoritative Discovery
Die öffentliche Signatur erlaubt zwar `product_ids=all`. Das beweist jedoch nur den Parametervertrag. Historische reale Live-Evidence am bekannten fremden Vendor-Produkt 53213 ergab keine verwertbare `data.commissions`-Zeile für den angenommenen Affiliate-seitigen Zweck. Der spätere lokale 6.70-Test simulierte dagegen genau die gewünschte Antwortstruktur und konnte deshalb den realen Capability-Mismatch nicht widerlegen.

Der abschließende Dokumentationsabgleich erklärt diesen Mismatch zusätzlich fachlich: Das verwandte offizielle `updateAffiliateCommission(affiliate_id, product_ids, data)` ändert Provisionen eines Affiliates für Produkte des API-Key-Kontos und kann für konkret genannte Produkte sogar neue Affiliations anlegen; dafür ist Full Access erforderlich. `getAffiliateCommission` ist die lesende Schwesterfunktion derselben Provisionsverwaltung. `product_ids=all` bedeutet deshalb nicht automatisch „alle Fremdvendor-Produkte, mit denen dieses Konto als Affiliate verbunden ist“. Die frühere 6.70-Annahme war eine Perspektivverwechslung zwischen Vendor-Provisionsverwaltung und Affiliate-seitiger Partnerschaftsinventur.

### 3. validateAffiliate — KEINE Discovery
Der Endpoint verlangt `affiliate_name` plus eine oder mehrere bereits bekannte `product_ids`. Seine Antwort beschreibt die Affiliate-Identität/Validität, nicht eine inventarisierte Produktliste. Er kann bekannte Produktbezüge prüfen, aber unbekannte Partnerschafts-Produkt-IDs nicht selbst liefern.

### 4. listCommissions — KEINE vollständige Partnerschaftsinventur
Transaktions-/Provisionsdaten können nur tatsächlich entstandene Provisionen abbilden. Genehmigte Partnerschaften ohne Verkauf würden fehlen.

### 5. IPN/Zapier New Affiliate Approved — falsche Richtung
Das offizielle `on_affiliation`-Ereignis wird ausgelöst, wenn ein Affiliate ein Produkt des empfangenden Vendors bewerben möchte und die Affiliation akzeptiert wird. Es ist damit ein Vendor-seitiges Ereignis und liefert nicht die vollständige Affiliate-seitige Liste fremder Vendor-Partnerschaften dieses Kontos.

### 6. Affiliate-UI `Verkäufe & Partner → Partnerschaften mit Vendoren` — fachlich vollständig, aber keine nachgewiesene öffentliche Read-only API
Digistore24 beschreibt genau diese ungefilterte Liste als statusübergreifende Anzeige aller Affiliate-Partnerschaften. Sie zeigt Vendor, Produkt/Produktsprache, Status, Affiliate-Provision und Werbemittelseite; im Bearbeiten-Dialog zusätzlich den Promolink. Die reale Seite zeigt außerdem einen CSV-Export. In der aktuell veröffentlichten API-Referenz ist jedoch kein äquivalenter List-/Inventory-Endpunkt für diese Affiliate-seitige Partnerschaftstabelle vorhanden.

### 7. Contentlinks — kein nachgewiesener Runtime-Enumerator
Die Dokumentation bindet die Produktauswahl an bereits bestehende Affiliations. Das ist für die UI plausibel, liefert aber keinen dokumentierten serverseitigen List-Endpunkt für WordPress. Die reale Übersichtsseite des Kontos zeigte zudem keine Produkte. Deshalb ist Contentlinks kein freigegebener Discovery-Transport.

### 8. listProducts / Marketplace / Statistik — keine Ersatzinventur
`listProducts` wird von Digistore24 für die eigenen Produkte des API-Key-Kontos verwendet. Marketplace enthält bewerbbare Angebote und ist nicht identisch mit bestehenden Partnerschaften. Statistik-/Provisionsberichte sind transaktionsabhängig. Keiner dieser Wege kann deshalb die ungefilterte Affiliate-Partnerschaftsliste vollständig ersetzen.

## Lokale Tests

1. Real-Inventory-Acceptance-Gate: 12/12 PASS.
   - exakte 18 approved+active -> PASS
   - 1 fehlt -> FAIL
   - 53213 allein -> FAIL
   - pending/rejected/inactive ausgeschlossen
   - fremde Affiliate-ID -> FAIL
   - malformed/duplicate/schema mismatch -> FAIL closed

2. Discovery-Capability-/Gesamtworkflow-Vertrag: 24/24 PASS.
   - alle aktuell untersuchten ungeeigneten Discovery-Quellen werden als autoritative Discovery abgelehnt
   - nur ein supported + affiliate-side + real-complete + machine-readable + read-only Enumerator erfüllt den Vertrag
   - bei Discovery-FAIL: 0 Downstream-Aufrufe, LKG bleibt erhalten
   - bei hypothetischem 18/18-Discovery-PASS: alle 18 gehen an validateAffiliate und durch die vorhandene Kette
   - einzelner Validate-/Support-URL-/Creative-/Slot-/Persistenzfehler stoppt nicht die übrigen Partner
   - Persistenzfehler lässt LKG stehen
   - eBay/idealo/Awin bleiben außerhalb des Änderungsscopes; Baseline-Blobs wurden festgehalten

3. Public-API-Exhaustionscheck: 15/15 PASS.
   - aktuelle Swagger-Affiliate-Operationen vollständig inventarisiert
   - alle read-only Kandidaten gegen den benötigten Affiliate-seitigen Inventurvertrag geprüft
   - `validateAffiliate` wegen benötigter Produkt-IDs als Discovery ausgeschlossen
   - `getAffiliateCommission` nicht als Affiliate-seitige Vendor-Partnerschaftsliste autorisiert
   - `updateAffiliateCommission` als mutierender Vendor-Provisionsverwaltungsweg ausgeschlossen
   - `listProducts` als eigenes Produkt-/Vendorinventar, nicht als fremde genehmigte Affiliate-Partnerschaften klassifiziert
   - `listCommissions` als transaktionsabhängig und damit prinzipiell unvollständig klassifiziert
   - private/undokumentierte UI-Routen bleiben als Release-Authority gesperrt

## Aktueller Public-API-Exhaustionscheck 02.09.2026

Die aktuell veröffentlichte Digistore24-Swagger-Referenz wurde erneut gegen den benötigten Affiliate-seitigen Inventurvertrag geprüft. Im Bereich `Affiliates` sind acht Operationen veröffentlicht: `getAffiliateCommission`, `getCustomerToAffiliateBuyerDetails`, `getReferringAffiliate`, `getAffiliateForEmail`, `setAffiliateForEmail`, `setReferringAffiliate`, `updateAffiliateCommission`, `validateAffiliate`. Keine davon ist als List-/Inventory-Endpunkt für `Affiliate view -> Sales & partners -> Vendor partnerships` dokumentiert.

Zusätzlich geprüft:
- `getAffiliateCommission`: kann Produkt-IDs bzw. `all` entgegennehmen, ist aber nach realer Evidence und der Semantik der Schwesterfunktion keine belegte Affiliate-seitige Fremdvendor-Inventur.
- `updateAffiliateCommission`: Vendor-Provisionsverwaltung; kann Affiliations für Produkte des API-Key-Kontos erzeugen/ändern und benötigt Full Access.
- `validateAffiliate`: benötigt bekannte Produkt-IDs; kein Enumerator.
- `listProducts`: eigene Produkte des API-Key-Kontos; keine fremden Affiliate-Partnerschaftsprodukte.
- `listCommissions`: transaktions-/provisionsbasiert und deshalb prinzipiell unvollständig für genehmigte Partnerschaften ohne Verkauf.
- `statsAffiliateToplist`: Vendor-seitige Rangliste von Affiliates nach Umsatz und keine Affiliate-seitige Vendor-/Partnerschaftsinventur.
- `IPN on_affiliation`: Vendor-seitiges Ereignis für einen neu akzeptierten Affiliate zu einem Produkt des Vendors; falsche Richtung.
- Affiliate-UI `Sales & partners -> Vendor partnerships`: fachlich vollständige Partnerschaftsliste und realer CSV-Export, aber kein veröffentlichter API-Endpunkt/Export-Token für serverseitigen Abruf.
- Affiliate-UI `Sales & partners -> Content links`: kein dokumentierter List-Endpunkt und daher keine Runtime-Authority.

Der Dokumentations-/Capability-Test beweist nicht, dass Digistore24 intern keinen privaten UI-Endpunkt besitzt. Er beweist aber den für den Release entscheidenden Punkt: Unter den aktuell öffentlich unterstützten API-Verträgen ist kein serverseitiger read-only Enumerator nachgewiesen, der die reale Affiliate-seitige Vendor-Partnerschaftsliste vollständig liefert.

## Abschließendes technisches Ergebnis

Der aktuelle Fehler ist vollständig eingegrenzt. Er liegt nicht im Bannerparser, nicht im Target-/Slot-System, nicht in LKG/Persistenz und nicht bei eBay/idealo/Awin. Er liegt ausschließlich an der fehlenden zulässigen Discovery-Quelle für die Affiliate-seitige DS24-Partnerschaftsinventur.

Unter dem derzeit verbindlichen Zielvertrag ist daher **kein weiterer Code-/Pluginfix technisch zulässig**, solange Digistore24 keinen offiziell unterstützten read-only API- oder authentifizierbaren Exportkanal für genau diese Liste bereitstellt. Ein weiterer ZIP-Build würde entweder denselben bekannten falschen API-Weg wiederholen oder den Zielvertrag unbemerkt auf CSV-/Browser-Scraping ändern.

Darum gilt fail-closed:
- kein weiterer Pluginbuild auf Basis von Marketplace, `getAffiliateCommission(all)`, `validateAffiliate`, Provisionen oder Statistik
- keine 18er-Kontroll-CSV als Runtime-Importquelle
- kein Bruteforce über Produkt-IDs
- kein undokumentiertes Session-/Browser-Scraping als stiller Ersatz für eine API
- kein synthetisches lokales 18/18 als Remote-Beweis
- bestehender Banner-/Target-/Slot-/LKG-Pfad bleibt unangetastet
- eBay/idealo/Awin bleiben unverändert, solange kein Regressionstest scheitert

Der reale CSV-Export der Affiliate-Oberfläche beweist lediglich, dass Digistore24 die vollständigen Daten intern maschinenlesbar besitzt. Ohne dokumentierte API-/Export-Authentisierung ist dieser UI-Export noch keine stabile serverseitige Runtime-Schnittstelle für das WordPress-System.

Damit verbleiben genau zwei fachlich ehrliche Endzustände:

1. Digistore24 bestätigt/bereitstellt einen offiziell unterstützten read-only API-/Exportkanal für `Verkäufe & Partner -> Partnerschaften mit Vendoren`. Dann wird genau dieser eine Kanal gegen 18/18 real geprüft und erst danach in den bereits funktionierenden Downstream eingespeist.
2. Digistore24 bietet keinen solchen Kanal. Dann ist die bisher geforderte vollautomatische Affiliate-seitige DS24-Discovery mit der unterstützten öffentlichen Schnittstelle nicht implementierbar. Eine CSV-/Browser-/sonstige Transportlösung wäre eine bewusste Änderung des Zielvertrags und darf nicht als bloßer Pluginfix ausgegeben werden.

### Exakter Provider-Nachweis

Die einzige verbleibende fachliche Frage an Digistore24 lautet:

> Gibt es für ein Affiliate-Konto einen offiziell unterstützten read-only API-Endpunkt oder einen anderen stabilen authentifizierbaren maschinenlesbaren Export-Endpunkt, der dieselben Datensätze wie `Affiliate view -> Sales & partners -> Vendor partnerships` liefert, insbesondere Produkt-ID, Vendor, Partnership Status, Affiliate Commission, Affiliate-Support/Werbemittelseite und Promolink, und zwar vollständig auch für genehmigte Partnerschaften ohne bisherigen Verkauf? Wir benötigen ausschließlich lesenden Zugriff. `getAffiliateCommission`, `validateAffiliate`, Marketplace- und transaktionsbasierte Wege liefern für diesen Affiliate-seitigen Inventurfall keine nachgewiesene vollständige Liste.

Nur eine konkrete, von Digistore24 bestätigte Schnittstelle darf danach als neue Discovery-Authority geprüft werden.

## ERROR-REGISTER POSTCHECK

Neue Fehlerklasse erkannt: NEIN — AFF-ERR-012 deckt die Root Cause vollständig ab.
Bekannten Fehlerweg wiederholt: historisch JA (6.70/6.71), in diesem Schritt NEIN.
Falsche Contentlinks-Annahme korrigiert: JA.
Public-API-Perspektive von `getAffiliateCommission(all)` gegen Vendor-Provisionsverwaltung gegengeprüft: JA.
Produktcode geändert: NEIN.
Plugin gebaut: NEIN.
Release/Governance geändert: NEIN.
Gate: PROVIDER-CAPABILITY BLOCKED / PRODUKTCODE-ÄNDERUNG GESPERRT / KEIN RELEASE.

## Lokale Evidence-Hashes

- Discovery-Capability-Test: `30399de0e454c45b3b372a181c270438dbe3353b1468e560750c39447d1363dc`
- Discovery-Capability-Report: `14883868a2d7a2f9470025e16cde54644899c1e708a64f14fda0b872528f9a2e`
- Real-Inventory-Acceptance-Gate: `fac561010a86d5a4f415c018e1862e51c1d7fbe0baea9e433cf5202466563ad0`
- Acceptance-Gate-Test: `986299af18226f2fc71540a25e90fe5f03b9461e5b4ee5645545db6e8809eb0b`
- Acceptance-Gate-Report: `2e18cf11253bf70bdf44a583f34237d2f0363f599aba4210a79083fb565a6967`
- Public-API-Exhaustion-Test: `03b6c7384f9b29e1276fd03aebb6a41137c5915da82da3ccd2460f3cc832a728`
- Public-API-Exhaustion-Report: `513f4c4d27e5ab507b9c984b698e4ac08b9bf027e0a9470522aadadb71d87e07`
