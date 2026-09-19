# CONCEPT AGENT — KOMPLETTE TESTSTRECKE

## Phase 1 — Isolation
PASS-Kriterium:
- alle Änderungen nur unter concept_agent/**
- kein Import fremder Konzepte
- kein WordPress-Write
- kein Publish

## Phase 2 — Eingang
Reale WordPress-Auftragskopie.
Pflicht: Titel, Keyword, Artikeltyp, Kategorie, exakt drei gebundene interne Links.
Fehlende Links: BLOCK vor Research.

## Phase 3 — Research Agent
Nur gebundener Quellenpool.
Ungültige URL / leere Quelle / doppelte source_id: BLOCK.

## Phase 4 — Facts Agent
Jeder Fakt muss auf akzeptierte source_id zeigen.
Unbekannte source_id: BLOCK.

## Phase 5 — Writer
Austauschbarer Writer-Port.
Aktuell:
- interner Testwriter
- manueller Chat-Writer
- Claude-Port vorbereitet, nicht verbunden

## Phase 6 — Artikelprüfung
- Identität
- Keyword
- drei interne Links
- kein externer Link
- Tabelle
- Mindeststruktur

## Phase 7 — Repair
Nur derselbe Artikel.
Danach vollständige Wiederprüfung.

## Phase 8 — Artikel-Preimport
Genau ein internes Artikelpayload je Artikel.
SHA256-Bindung.
WICHTIG: Dieses Payload ist niemals die WordPress-Uploaddatei.

## Phase 9 — 1..N
Getestete Größen:
- 1 Artikel
- 3 Artikel
- 7 Artikel
Kein Drop, keine Umordnung.
Fehler eines Artikels stoppt fail-closed.

## Phase 10 — reale Qualitätsprüfer
Verbindlich vor Downstream:
- LanguageTool 6.8
- PPM 6.7.9
Nach jeder Reparatur vollständiger Recheck.
Kein Artikel darf in Phase 11 gelangen, bevor beide real PASS sind.

## Phase 11 — PSERC-Import-Envelope
Für alle finalen Artikel muss ein echtes `PSERC_APPROVED_PRODUCTION_PACKAGE_V1` aufgebaut sein mit exakt:
- contract
- package_id
- package_payload_sha256
- source
- fact_pack_bundle
- fact_pack_bundle_sha256
- production_plan
- production_plan_sha256
- workflow_release
- workflow_release_sha256

Pflicht:
- `workflow_release.contract = WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED`
- `workflow_release.status = PASS`
- `wordpress_write_performed = false`
- alle Komponentenhashes kanonisch korrekt
- Artikelbytes im Production Plan exakt identisch zu den final geprüften Artikelbytes

## Phase 12 — ENDSTEMPEL
WordPress-Datei darf erst nach echtem GitHub-ENDSTEMPEL entstehen.

Pflichtvertrag:
- `contract = PSERC_APPROVED_PRODUCTION_PACKAGE_V1`
- `endstamp_contract = PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1`
- `status = ENDSTEMPEL_PASS`
- `signature_algorithm = ED25519`
- gebundene Produktions-Key-ID und Public-Key-SHA
- echte gültige ED25519-Signatur
- `publish_allowed = false`
- `content_mutation_performed = false`

Artikelmanifest:
- `contract = PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1`
- korrekter Batch
- runtime_generation
- source_manifest_ref + SHA
- article_count = tatsächliche Artikelzahl
- pro Artikel exakt: name, plan_slot, sha256, byte_length, content_utf8
- Name exakt `ARTICLE_<64hex-plan_slot>.md`
- Manifest- und Import-Envelope-Hashes müssen exakt stimmen

## Phase 13 — WordPress-Ausgabegate
Einzig erlaubte Chat-/WordPress-Enddatei:
`GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json`
(Der historische Dateiname ist keine Mengenautorität.)

Vor Dateiausgabe MUSS `concept_agent/wordpress_output_contract.py` PASS liefern, einschließlich echter Signaturprüfung.

VERBOTEN als WordPress-Datei:
- `CONCEPT_AGENT_FINAL_ARTICLE_V1`
- `CONCEPT_AGENT_7_ARTICLE_CHAT_HANDOFF_V1`
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`
- jedes unsigned/preimport Paket

Fail-closed:
Ohne echtes ENDSTEMPEL-PASS gibt es keine als WordPress-ready bezeichnete Datei.

## Phase 14 — Positiv-/Negativtest der WordPress-Grenze
Positiv:
- bekanntes echtes signiertes ENDSTEMPEL-Paket muss den Contract-/Hash-/Signaturcheck bestehen.

Negativ:
- falscher Top-Level-Contract -> BLOCK
- fehlende/ungültige Signatur -> BLOCK
- Artikelbyte geändert -> BLOCK
- SHA/byte_length drift -> BLOCK
- Import-Envelope-Hash drift -> BLOCK
- publish_allowed != false -> BLOCK
- article_count mismatch -> BLOCK

## Phase 15 — Chat-Ausgabe
Erst nach Phase 14 PASS:
- genau eine WordPress-Uploaddatei hier im Chat
- keine interne Handoff-Datei als Ersatz
- Dateiausgabe ist Bestandteil des Tests und kein optionaler Nachschritt

## Produktionsgrenze
Kein Publish.
Kein WordPress-Write.
Andere Konzepte unverändert.
