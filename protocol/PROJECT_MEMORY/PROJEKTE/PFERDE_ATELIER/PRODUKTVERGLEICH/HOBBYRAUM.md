# PRODUKTVERGLEICH – HOBBYRAUM

STAND: 2026-09-09
STATUS: AKTIV / 0.8.0 WORDPRESS-LIVERETEST

## AKTUELLER AUFTRAG

Einmaliger Realtest des vollständig nachgeprüften 0.8.0-Gesamtworkflows.

## GEBUNDENER WORKFLOW

`SEO ↔ Produktwissen → Vergleichbarkeit → direkte Paar-Nachfrage ODER Nachfrage A+B → aktuelle Planning-/Kannibalisierungsprüfung → Dossier → Audit`

## TESTKANDIDAT

`Universal Product Comparison 0.8.0-prototype`

ZIP SHA-256:
`c9eec5b4c7faafa23af6bd5c554d85c2c4d1763e4c618fbd49c3e04dd45abb66`

## ARBEITSORT / BRANCH

Campus-/Statusautorität:
`hobbyroom/project-memory-campus-v1-20260905`

Älterer Technikbranch:
`hobbyroom/productvergleich-workflow-v070-20260908`
Head frisch geprüft:
`5d6863a9fe9b9082c1111debc22cde96191a34eb`

HARD RULE:
Dieser Technikbranch enthält **nicht** den vollständigen 0.8.0-Quellstand und ist deshalb aktuell **keine 0.8-Source-/Runner-Autorität**. Nicht mergen, nicht als aktuellen Source-PASS ausgeben.

Aktueller 0.8-Prüfgegenstand ist ausschließlich die oben hashgebundene ZIP plus die in `PROTOKOLL.md` dokumentierten real gebundenen UPK-/PSTE-Abhängigkeiten.

## VOR DEM RETEST TATSÄCHLICH AUSGEFÜHRT

- PHP-Lint 39/39 PASS;
- gesamte Hard-PHP-Suite PASS;
- statischer Gesamtworkflow-Gate PASS;
- direkte A-gegen-B-Nachfrage positiv;
- A+B-Einzelnachfrage positiv;
- nur A/B negativ;
- keine Nachfrage negativ;
- generische Gruppenanfrage negativ;
- Same-Brand negativ;
- Vergleichbarkeit negativ;
- Provider-PARTIAL negativ;
- 0.7.x-Signale stale;
- Expiry stale;
- aktuelle Readiness/Kannibalisierung revalidiert;
- Inventory/Structure-Drift gebunden;
- idempotenter Wiederholungslauf;
- PSTE-Kostenrechnung geprüft;
- reale PSTE-Topic-Map False-Pair-Guard PASS;
- Mutation Guards PASS;
- Report-Hashes 49/49 PASS.

Wichtig:
Die vollständige Suite wurde erst nach Bindung der realen externen Fixtures/Abhängigkeiten als PASS gewertet. Der vorherige Lauf ohne diese Bindung war FAIL und ist im Protokoll dokumentiert.

## NEXT ACTION

**Nur:**

1. WordPress → vorhandenes `Universal Product Comparison` durch 0.8.0 ersetzen.
2. Produktvergleich → Vergleichsplanung → Regendecken.
3. Vor dem Lauf prüfen:
   - alte 0.7.x-Signale werden stale/offen behandelt;
   - maximale Providerkosten können bei 8 Paaren / 5 Produkten bis **$0.4056** betragen.
4. **Gesamtworkflow starten**.
5. Screenshot/Ergebnis hier zurückgeben.

## RÜCKGABEWEG

Bei PASS:
- PV-LIVE-002/003 in `FEHLERQUELLEN.md` schließen;
- CURRENT_STATE auf realen Live-PASS aktualisieren;
- erst danach den exakten 0.8-Source-/Release-Stand sauber auf einem aktuellen Technikbranch binden, bevor weiterentwickelt wird.

Bei FAIL:
- kein neues Plugin;
- ersten realen Fehler gegen den gesamten Workflow + `PROTOKOLL.md` + autoritative Fehlerquelle prüfen;
- kleinster KISS-Fix im Hobbyraum;
- Positiv/Negativ + Regression + Fresh-ZIP erneut.

## NICHT ANFASSEN

- main;
- STARTMASTER/TEXT-Reparaturweg;
- ACM-Parallelbranch;
- Affiliate-Fachlogik;
- Writer/Draft/Publish;
- Auto-Publish.

Kein weiterer Pluginstand vor dem 0.8.0-Liveretest.
