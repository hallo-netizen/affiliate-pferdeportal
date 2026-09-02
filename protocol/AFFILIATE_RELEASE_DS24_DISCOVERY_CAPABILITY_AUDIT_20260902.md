# DIGISTORE24 — DISCOVERY CAPABILITY AUDIT / ROOT-CAUSE GATE

Stand: 2026-09-02
Projekt: Pferde Atelier / Affiliate-Zentrale
Scope: ausschließlich automatische Ermittlung der bereits genehmigten Affiliate-Partnerschaften. Kein Pluginbuild.

## ERROR-REGISTER PRECHECK

Relevante Hardlocks: AFF-ERR-001, 002, 003, 004, 006, 008, 009, 010, 011.
Zusätzlich neu erkannt: die Discovery-Routen `listMarketplaceEntries` und `getAffiliateCommission(product_ids=all)` wurden in früheren lokalen Builds erneut als autoritativ angenommen, obwohl reale Live-Evidence diese Annahmen bereits widerlegt hatte.

## Reale Bindung

Kontrolloracle: 18 genehmigte Partnerschaften / 10 Vendoren. Die 18 Produkt-IDs dienen ausschließlich als Sollvergleich, nicht als Runtime-Discovery-Quelle.
Alte lokale Quelle 53213 darf nicht als Erfolg der Remote-Discovery gezählt werden.

## Capability-Ergebnis

### 1. listMarketplaceEntries — FAIL als autoritative Discovery
Historische Live-Evidence: API lieferte `data.entries=[]`, obwohl in der Affiliate-Oberfläche tausende Marketplace-Produkte sichtbar waren. Zusätzlich ist Marketplace-Inventar fachlich nicht identisch mit der Liste eigener genehmigter Vendor-Partnerschaften.

### 2. getAffiliateCommission(product_ids=all) — FAIL als autoritative Discovery
Die öffentliche Signatur erlaubt zwar `product_ids=all`. Das beweist jedoch nur den Parametervertrag. Historische reale Live-Evidence am bekannten fremden Vendor-Produkt 53213 ergab keine verwertbare `data.commissions`-Zeile für den angenommenen Affiliate-seitigen Zweck. Der spätere lokale 6.70-Test simulierte dagegen genau die gewünschte Antwortstruktur und konnte deshalb den realen Capability-Mismatch nicht widerlegen.

### 3. validateAffiliate — KEINE Discovery
Der Endpoint benötigt Produkt-IDs als Eingabe. Er kann bekannte IDs verifizieren, aber unbekannte Partnerschafts-IDs nicht inventarisieren.

### 4. listCommissions — KEINE vollständige Partnerschaftsinventur
Transaktions-/Provisionsdaten können nur tatsächlich entstandene Provisionen abbilden. Genehmigte Partnerschaften ohne Verkauf würden fehlen.

### 5. IPN/Zapier New Affiliate Approved — falsche Richtung
Dokumentiert als Vendor-seitiges Ereignis für neue Affiliates zu eigenen Produkten. Es liefert nicht die vollständige Affiliate-seitige Liste der Vendor-Partnerschaften dieses Kontos.

### 6. Affiliate-UI `Verkäufe & Partner → Partnerschaften mit Vendoren` — fachlich vollständig, aber keine nachgewiesene öffentliche Read-only API
Die Oberfläche zeigt Vendor, Produkt, Status, Provision, Werbemittelseite und Promolink. In der aktuell veröffentlichten API-Referenz ist jedoch kein äquivalenter List-Endpunkt für diese Affiliate-seitige Partnerschaftstabelle nachgewiesen.

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
   - nur ein hypothetischer supported + affiliate-side + real-complete + machine-readable + read-only Enumerator erfüllt den Vertrag
   - bei Discovery-FAIL: 0 Downstream-Aufrufe, LKG bleibt erhalten
   - bei hypothetischem 18/18-Discovery-PASS: alle 18 gehen an validateAffiliate und durch die vorhandene Kette
   - einzelner Validate-/Support-URL-/Creative-/Slot-/Persistenzfehler stoppt nicht die übrigen Partner
   - Persistenzfehler lässt LKG stehen
   - eBay/idealo/Awin bleiben außerhalb des Änderungsscopes; Baseline-Blobs wurden festgehalten

## Ergebnis / technische Konsequenz

Der aktuelle Block ist kein weiterer Parser-/Pluginfehler, sondern ein fehlender nachgewiesener Discovery-Kanal für die Affiliate-seitige Partnerschaftsinventur.

Darum gilt fail-closed:
- kein weiterer Pluginbuild auf Basis von Marketplace oder getAffiliateCommission(all)
- keine 18er-CSV als Runtime-Importquelle
- kein synthetisches lokales 18/18 als API-Beweis
- validateAffiliate erst nach einer echten Discovery bekannter Produkt-IDs
- bestehender Banner-/Target-/Slot-/LKG-Pfad bleibt unangetastet

Nächster technisch zulässiger Schritt ist ausschließlich der Nachweis eines von Digistore24 unterstützten, read-only, maschinenlesbaren Affiliate-seitigen Partnerschaftsinventars, das die 18 Kontroll-IDs ohne lokale Vorfütterung liefert. Solange ein solcher Kanal nicht existiert/nachgewiesen ist, darf kein Plugin-PASS behauptet werden.

## ERROR-REGISTER POSTCHECK

Neue Fehlerklasse erkannt: JA — wiederholte Verwechslung von API-Parameterfähigkeit mit realer Affiliate-seitiger Discovery-Fähigkeit.
Bekannten Fehlerweg wiederholt: historisch JA (6.70/6.71), in diesem Schritt NEIN.
Produktcode geändert: NEIN.
Plugin gebaut: NEIN.
Release/Governance geändert: NEIN.
Gate: TECHNISCHE DISCOVERY-CAPABILITY OFFEN / PRODUKTCODE-ÄNDERUNG GESPERRT.

## Lokale Evidence-Hashes

- Discovery-Capability-Test: `30399de0e454c45b3b372a181c270438dbe3353b1468e560750c39447d1363dc`
- Discovery-Capability-Report: `14883868a2d7a2f9470025e16cde54644899c1e708a64f14fda0b872528f9a2e`
- Real-Inventory-Acceptance-Gate: `fac561010a86d5a4f415c018e1862e51c1d7fbe0baea9e433cf5202466563ad0`
- Acceptance-Gate-Test: `986299af18226f2fc71540a25e90fe5f03b9461e5b4ee5645545db6e8809eb0b`
- Acceptance-Gate-Report: `2e18cf11253bf70bdf44a583f34237d2f0363f599aba4210a79083fb565a6967`
