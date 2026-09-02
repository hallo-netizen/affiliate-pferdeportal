# AFFILIATE-ZENTRALE — CURRENT-SCOPE-AMENDMENT ZUM FEHLERREGISTER

Stand: 2026-09-02
Branch: `affiliate-release-current`
Status: `MANDATORY_CURRENT_SCOPE_PRECEDENCE`

## AFF-ERR-017 — Spätere ausdrückliche Nutzerentscheidung wurde durch ältere Discovery-Regeln überschrieben

**Symptom:** Nach der ausdrücklichen Nutzerentscheidung für einen manuellen Digistore24-Bulkimport über genau ein Uploadfeld wurde wiederholt zur automatischen Discovery zurückgesprungen. Dadurch wurden erneut Partnerliste/CSV, Browser-Network-Evidence und die frühere 6.71-Quelle als Voraussetzung angefordert.

**Root Cause:** Ältere Einträge AFF-ERR-008, AFF-ERR-012, AFF-ERR-015 und AFF-ERR-016 wurden als aktuelle Navigation interpretiert, obwohl der Nutzer den aktuellen Betriebsweg später ausdrücklich geändert hatte. Ziel-/Fehlerhistorie wurde dadurch fälschlich über die spätere Nutzerentscheidung gestellt.

**Verbindlicher aktueller Vorrang:** `control/release-governance/CURRENT_RELEASE.json -> user_scope_lock` und `protocol/AFFILIATE_RELEASE_CURRENT_USER_SCOPE_LOCK_20260902.md` sind für den aktuellen Auftrag maßgeblich.

**Nicht wiederholen:** Bis zu einer neuen ausdrücklichen Nutzerentscheidung niemals erneut Partnerliste, dieselbe DS24-CSV, Browser-/Network-Screenshots, automatische DS24-Discovery oder die historische 6.71-ZIP als Voraussetzung für den aktuellen manuellen Bulkimport anfordern.

**Aktueller Betriebsweg:** `MANUELLER EIN-FELD-BULKIMPORT -> AUTO-PROVIDERERKENNUNG -> DS24-RUNTIME-SYNC -> VORHANDENER DOWNSTREAM -> POSITIV/NEGATIV/GESAMTWORKFLOW -> LIVE-READBACK`.

**Auswirkung auf ältere Fehler-IDs für den aktuellen Scope:**
- AFF-ERR-008: automatische Bulk-Discovery bleibt historische/langfristige Anforderung, blockiert den ausdrücklich autorisierten manuellen Bulkimport aber nicht.
- AFF-ERR-012: Discovery-API-Problem bleibt historisch belegt, ist für den aktuellen Auftrag OUT OF SCOPE / NON-BLOCKING.
- AFF-ERR-015: die frühere Aussage „CSV nur Testoracle“ ist durch die spätere ausdrückliche Nutzerentscheidung für diesen Auftrag superseded.
- AFF-ERR-016: die historische 6.71-Diskrepanz darf den direkt committed canonical source nicht als Arbeitsautorität verdrängen und darf keine erneute ZIP-Anforderung auslösen.

**POSITIV:** genau ein Uploadfeld; DS24/idealo/Awin/ADCELL werden eindeutig erkannt; aktueller DS24-Bestand wird manuell synchronisiert; bekannte Sollstruktur 18 genehmigte Produktpartnerschaften / 10 Vendoren wird im lokalen Contract-Fixture erreicht.

**NEGATIV:** unbekannte/widersprüchliche Dateien, doppelte Produkt-ID, Werbemittel-ID/Vendor-Konflikt, falsche DS24-Identität und GZIP-Overflow fail-closed; eBay-Datei wird erkannt, aber nicht in einen falschen Importpfad gezwungen.

**Evidence:** `release/affiliate-zentrale/evidence/manual_single_upload_multi_provider_import_20260902.txt`, gebunden an Source-Manifest SHA-256 `af8cf12ee63e8627f33d90046da916f9275079b39e94870f6c93be5ab2c065f5`.

**Status:** FIXED_LOCAL / WordPress-Live-Readback offen.

## Vorrangregel

Bei Widerspruch zwischen älteren Einträgen des Haupt-Fehlerregisters und diesem Amendment gilt für den aktuellen Auftrag dieses Amendment zusammen mit dem aktiven `user_scope_lock`. Nur eine neue ausdrückliche Nutzerentscheidung kann diesen Vorrang ändern.
