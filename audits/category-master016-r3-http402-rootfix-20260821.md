# Kategorie-Workflow MASTER 016-R3 / V1.6.3 – DataForSEO HTTP402 Rootfix

Datum: 2026-08-21
Branch: `category-master016-r3-http402-rootfix-20260821`
Basis: `category-master016-r2-rootfix-20260821`
Status: `LOCAL FULL ARTIFACT HARD PASS / LIVE 402 RETRY NOT CLAIMED`

## Realer Trigger
Im Gaumen-Atelier-Blatt-Longtail-Fallback war der kostenlose Preflight korrekt: 107 Content-Blätter, 93 Evidenzlücken, erster Paid-Batch 20, keine Global-/Cluster-Wiederholung. Der anschließende DataForSEO-Aufruf endete mit `DataForSEO HTTP-Fehler 402.`

## Root Cause im Plugin
V1.6.2 prüfte bei DataForSEO zuerst den HTTP-Status und warf bei Nicht-2xx sofort. Dadurch wurden `status_code` und `status_message` aus einem vorhandenen JSON-Body verworfen. Die konkrete externe 402-Ursache war daher nicht belegbar.

## V1.6.3 Rootfix
- JSON-Body wird vor dem Nicht-2xx-Throw sicher dekodiert.
- Provider-`status_code` und `status_message` bleiben sichtbar erhalten.
- Vollständige Provider-Responses, Authorization-Header, Credentials und Secrets werden nicht ausgegeben.
- Nicht-JSON-HTTP-Fehler bleiben generisch; kein Subcode wird erfunden.
- Kein automatischer Retry eines fehlgeschlagenen Paid-Calls.
- Keine Änderung an Kategorie-, Longtail-, Paid-Call-, Content-, Titel-, Beitragsarten- oder Textmaschinenlogik.

## DataForSEO 402
Offizielle 402-Familie: 40200 Guthaben/Payment Required; 40201 Account pausiert; 40202 Rate-Limit; 40203 Kostenlimit; 40204 API-/Subscription-Zugriff. Die konkrete Ursache des realen Fehlers bleibt `UNKNOWN/BLOCKED`, bis V1.6.3 den Provider-Subcode sichtbar macht oder der DataForSEO-Account den Grund direkt zeigt.

## Prüfungen
- aktive Source: 136/136 PASS
- Fresh Source ZIP: 136/136 PASS
- Fresh Installer ZIP: 136/136 PASS
- Fresh Master-Source: 136/136 PASS
- Fresh Master-Installer: 136/136 PASS
- Source↔Installer: 0 Diff
- PHP-Lint: PASS
- JSON-Parse: PASS
- Content-Write-Scan: 0 Treffer
- aktive Regeln: 127/127 ACTIVE
- Workflow: unverändert 14/14
- Master-Manifest: 449 Einträge PASS

## Artefakte
- Installer `AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.6.3_MASTER016_R3_HTTP402_ROOTFIX.zip`
  - SHA-256 `da8a1502d79f0e10e8c61840ad1054861e8caf34ae3dd8d590451f60a9c486a8`
- Source `QUELLCODE_KATEGORIE_WORKFLOW_V1.6.3_MASTER016_R3_HTTP402_ROOTFIX.zip`
  - SHA-256 `afdab63d0c01e81eb268552444f779a276bb324f0e7306e532e1322c6721a4ea`
- Master `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R3_WORKFLOW_HARDLOCK.zip`
  - SHA-256 `e4baa66c820a0f8d4ae1a8b0e944dc840deac6241f48bd806c5ace98d8f6353a`

`main` bleibt unverändert; kein Merge. Keine API-Keys, WordPress-Datenbank, Medien oder Secrets in GitHub.