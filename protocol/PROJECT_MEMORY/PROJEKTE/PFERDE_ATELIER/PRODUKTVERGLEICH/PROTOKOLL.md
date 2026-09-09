# PRODUKTVERGLEICH – ARBEITSPROTOKOLL

ROLLE: CHRONIK / TEST- UND ÄNDERUNGSBELEGE  
**Niemals CURRENT_STATE, Fehlerautorität oder NEXT ACTION.**

## 2026-09-08 – Produktwissen / Rechercheweg

- bestehendes `Universal Product Knowledge` als ein Plugin weiterentwickelt, keine zusätzliche Pluginlinie;
- Recherchepaket-/Herstellerquellenprüfung aufgebaut;
- Produktpool statt fest vorgegebenem Vergleichspaar als Produktwissen-Ziel festgelegt;
- Produktvergleich muss SEO und Produktwissen gemeinsam konsumieren;
- feste Viererzahl pro Kategorie verworfen.

## 2026-09-08 – Produktvergleich / SEO-Kopplung

- Produktvergleich auf exakt zwei Produkte unterschiedlicher Hersteller festgelegt;
- bidirektionale Entdeckung eingeführt:
  - SEO kann konkrete Produkt-/Paar-Nachfrage entdecken;
  - Produktwissen kann technisch vergleichbare Paare zur SEO-Prüfung geben;
- A/B und B/A als dieselbe Paaridentität behandelt;
- Dossier erst nach Vergleichbarkeit + SEO-/Kannibalisierungsfreigabe;
- Affiliate bleibt nachgelagerter Exact-Match-Layer.

## 2026-09-08/09 – Release-Disziplin

Dauerhaft eingeführt:
- keine Zwischen-ZIP ohne sinnvoll testbaren Gesamtabschnitt;
- jeder geänderte Schritt gegen den Gesamtworkflow;
- Positiv/Negativ + Regression;
- autoritative Fremdverträge prüfen;
- fertige ZIP frisch entpacken und erneut testen;
- Mutationstest für neue kritische Regressionen, wenn sinnvoll.

## 2026-09-09 – PV-LIVE-001

Realer WordPress-Lauf 0.7.0:
- 8 Kandidaten;
- 16 Provider-Aufrufe;
- $0.1920;
- 0 SEO-PASS;
- 8 blockiert;
- 0 Dossiers;
- fälschlich grünes PASS.

0.7.1-Korrektur:
- `NO_ELIGIBLE_COMPARISONS` statt False-PASS;
- Warning statt Success;
- Laufkosten und Schätzung eines neuen Laufs getrennt.

Realer 0.7.1-Liveretest:
- Statuskorrektur sichtbar PASS;
- PV-LIVE-001 geschlossen.

## 2026-09-09 – PV-LIVE-002 / PV-LIVE-003

Gesamtworkflowprüfung ergab:
- direkte Paar-Nachfrage allein war zu eng;
- Nachfrage nach beiden konkreten Produkten A+B muss ebenfalls einen Vergleich ermöglichen;
- alte/abgelaufene SEO-Signale dürfen weder dauerhaft sperren noch dauerhaft freigeben;
- aktuelle Planning-/Kannibalisierungsentscheidung und Inventory-/Structure-Zustand müssen vor Dossierfreigabe erneut gebunden werden.

0.8.0-Kandidat:
- direkte A-gegen-B-Nachfrage positiv;
- A+B-Einzelnachfrage positiv;
- nur A/B negativ;
- keine Nachfrage negativ;
- generische Gruppenanfrage negativ;
- Same-Brand negativ;
- unpassende Vergleichsklasse negativ;
- Provider-PARTIAL negativ;
- Signal-Staleness/Expiry negativ;
- aktuelle Readiness-Revalidierung positiv/negativ;
- Dossier-/Strukturdrift gebunden;
- idempotenter Wiederholungslauf;
- Mutation Guards für drei kritische Altfehler.

## 2026-09-09 – ABSCHLUSSPRÜFUNG 0.8.0

Geprüfte ZIP:
`universal-product-comparison-0.8.0-prototype.zip`

SHA-256:
`c9eec5b4c7faafa23af6bd5c554d85c2c4d1763e4c618fbd49c3e04dd45abb66`

Frisch aus der ZIP entpackt und in diesem Abschlusslauf tatsächlich ausgeführt:

1. PHP-Lint: **39/39 PASS**.
2. Erster Versuch der Gesamtsuite: **korrekt FAIL**, weil der reale PSTE-Topic-Map-Fixturepfad und die externen UPK/PSTE-Wurzeln nicht gebunden waren. Dieser Lauf gilt ausdrücklich **nicht** als PASS.
3. Reale Abhängigkeiten gebunden:
   - PSTE-Topic-Map `pste-global-seo-topic-map-20260802-180439-utc.json`;
   - Universal Product Knowledge 0.5.0;
   - autoritativer PSTE-0.56.25-Installer.
4. Danach gesamte Hard-Suite aus der frisch entpackten ZIP erneut ausgeführt: **PASS**.
5. `hard_070_static_gate.py`: **PASS** gegen echte UPK-/PSTE-Wurzeln und PSTE-Installerhash.
6. Mutation Guards: **PASS**, alle drei absichtlich entfernten Sicherungen wurden erkannt.
7. Report-Dateihashes: **49/49 PASS** gegen die tatsächlich entpackten Dateien.

Wichtige Korrektur zur früheren Aussage:
Eine „komplette Fresh-ZIP-Suite“ ist nur dann bewiesen, wenn die externen realen Fixtures/Abhängigkeitswurzeln explizit gebunden sind. Ohne diese ist die Suite unvollständig.

## GITHUB-/WORKER-REALITÄT 2026-09-09

Frisch geprüft:
- Campus-Branch `hobbyroom/project-memory-campus-v1-20260905` ist die Büro-/Statusautorität.
- Produktwissen-Draft-PR #142: offen, ungemergt, Head `49363529463509b87a8ea7deb079d7d4c1b6e006`.
- Produktvergleich-Technikbranch `hobbyroom/productvergleich-workflow-v070-20260908`: Head `5d6863a9fe9b9082c1111debc22cde96191a34eb`; enthält **nicht** den kompletten 0.8.0-Quellstand und ist daher aktuell **keine 0.8-Source-Autorität**.
- 0.8.0 ist derzeit als hashgebundener getesteter ZIP-Kandidat verfügbar; kein Merge/Produktionsstatus wird aus dem älteren Technikbranch abgeleitet.

## ACM-ZWISCHENPRÜFUNG 2026-09-09 – READ ONLY

Frisch geprüft:
- Branch `alternative/seo-text-central-machine-20260908`;
- Draft-PR #195 offen/ungemergt;
- aktueller Head `3cd425f0a212b8cf79eea578c687bfbab4485046`;
- ACM bleibt strikt vom laufenden STARTMASTER-/Reparaturweg getrennt;
- bestehende Textmaschine und Fachregeln bleiben autoritativ;
- Controller ist beitragsart-unabhängig;
- zusätzliche Beitragsarten sind orchestratorisch grundsätzlich einfacher anschließbar, sofern ihr bestehender Fachworkflow einen vollständig definierten Artikeltyp-/Fact-Pack-Vertrag kennt;
- externe Signatur/WordPress-Preimport/kein Auto-Publish bleiben erhalten.

Kritischer offener Punkt für Produktvergleich:
Die exakten Produktidentitäten A/B plus quellengebundenes Produktvergleichsdossier müssten ohne neue freie Payload-/Handoff-Architektur sauber in den bestehenden Fachworkflow passen.

Daher:
**theoretisch vielversprechend, aber noch keine bindende Architekturänderung und keine technische Kopplung.**
