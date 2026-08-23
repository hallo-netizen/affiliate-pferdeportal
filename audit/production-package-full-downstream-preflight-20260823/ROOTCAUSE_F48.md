# F-48 – Produktionspaket vor Auslieferung nicht gegen realen Downstream-Endlauf geprüft

## Status
ROOT CAUSE IDENTIFIED / CORRECTED / FULL DOWNSTREAM PREFLIGHT PASS

## Betroffener Artikel
- Titel: `Boxenmatten für Pferde – worauf es bei der Auswahl ankommt`
- Kategorie: `boxenmatten-beratung`
- Beitragsart: `Beratung`
- verbindlicher Planplatz: `a574700d0b94f6e31fe6a87743497009210e04816a7d7c8236a6b40ac04b8a7f`
- kanonische Artikel-ID: `article:2d2f4c0ece3dc16e52a378c5`

## Fehlerkette
1. F-47 hatte bereits gezeigt, dass ein externer Builder die `canonical_article_id` eigenmächtig neu erzeugt hatte. Das wurde korrigiert.
2. Das danach ausgelieferte Paket wurde aber weiterhin nur gegen Hilfs-/Teilprüfungen geprüft und **nicht** gegen den realen nachfolgenden PPM-6.7.9-Endlauf.
3. Dadurch blieben zwei weitere statische Paketfehler unentdeckt:
   - `plan.items[0].source_hashes` enthielt den kompakten kanonischen Fact-Pack-Hash `f6eee7...`, während `PPM679_Storage::save_fact_pack()` den Hash des kanonisch pretty-encodierten JSON speichert: `86bb9795...`.
   - Tabellenzeilen trugen `data-fact-ids` nur am `<tr>`. PPM 6.7.9 verlangt für jede faktische sichtbare Tabellenzelle `<td>` eine eigene Faktreferenz.
4. Der Live-Server blockierte korrekt vor jedem WordPress-Write zuerst am Fact-Pack-Hash.

## Root Cause
Die eigentliche Ursache ist **nicht** PSERC oder PPM. Die Ursache war ein unvollständiges Release-Verfahren außerhalb der Fachplugins:

> Ein Produktionspaket durfte als `FINAL` bezeichnet und signiert werden, obwohl nicht exakt der reale nachgelagerte Pfad `PSERC -> Supervisor -> PPM 6.7.9 -> Draft -> Readback` mit diesem Paket durchgelaufen war.

Dadurch konnten unterschiedliche Hash-Namensräume und spätere Validatoranforderungen nacheinander erst auf dem Live-Server sichtbar werden.

## Korrektur
### 1. Fact-Pack-Hash-Namensräume werden getrennt
- Forschungs-/Inhaltsbindung: kompakter stabiler Hash des Fact-Packs (`f6eee7...`). Dieser bleibt in `canonical_article.fact_pack_hash` und den Supervisor-Evidenzbindungen.
- PPM-Registry-Bindung: SHA-256 von `PPM679_Diagnostic::encode($pack, true)` (`86bb9795...`). **Nur dieser** muss in `plan.items[].source_hashes` stehen.

### 2. Tabellen-Traceability
Bei jeder Tabellenzeile mit `data-fact-ids` wurden dieselben Fakt-IDs zusätzlich auf die zugehörigen `<td>`-Zellen übertragen.
- sichtbarer Text: unverändert
- Reihenfolge/Anzahl der HTML-Elemente: unverändert
- Tabelleninhalt: unverändert
- Design/CSS: unverändert
- nur technische Traceability-Attribute ergänzt

### 3. Verbindliches Full-Downstream-Release-Gate
Eine Datei darf künftig **nicht** als FINAL ausgeliefert werden, bevor alle folgenden Prüfungen mit exakt diesem Paket PASS sind:
1. kanonische ID/Planplatz-Bindung
2. PPM-Registry-Fact-Pack-Hash-Bindung
3. PSERC Package Envelope
4. Supervisor Ed25519-Authentizität
5. vollständiger Workflow-Supervisor
6. Fact-Pack-Import
7. PSERC-PPM-Bridge
8. echter PPM-6.7.9-Normal-Draft-Endlauf
9. Draft-Readback
10. Publish weiterhin false

Pflicht-Endstatus:
`NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH`

## Negative Pflichtproben
- alter kompakter Hash in `source_hashes` -> `BLOCKED_FACT_PACK_HASH_MISMATCH`
- fehlende Zell-Faktreferenzen -> `BLOCKED_CONTENT_FACT_REFS_MISSING`
- falsche kanonische ID -> Identity Guard BLOCKED
- manipuliertes Paket/Signatur -> Package-/Authentizitätsprüfung BLOCKED

## Nicht verändert
- Redaktionsplan
- READY-Metadaten
- Planplatz
- Kategorie
- Beitragsart
- Target Keyword
- sichtbarer Artikeltext
- Tabellenwerte
- Design
- PPM 6.7.9
- PSERC 0.28.5
- Auto-Publish bleibt verboten
