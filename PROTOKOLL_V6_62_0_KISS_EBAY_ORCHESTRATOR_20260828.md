# Affiliate-Zentrale V6.62.0 – KISS eBay-Orchestrator

Status: **LOCAL_HARD_PASS_AWAITING_LIVE**

## Ausgangsfehler V6.61.16
Der öffentliche Heartbeat-Endpunkt konnte trotz nicht ausgeführtem Arbeitspaket `status=running` zurückgeben. Lokal reproduziert:
- Lease bereits belegt -> V6.61.16 antwortet `running`.
- Lease während des Pakets verloren -> V6.61.16 antwortet `running`.
Damit konnte GitHub einen grünen Lauf melden, obwohl der kanonische Run keinen echten Fortschritt machte.

## KISS-Vertrag V6.62.0
- Genau ein Taktgeber für Facharbeit: externer Heartbeat.
- Genau ein kanonischer persistenter Run bleibt die fachliche Autorität.
- Jeder Tick liefert eines von: `advanced`, `busy`, `retryable_error`, `completed`, `failed`.
- `progress_seq` steigt nur bei nachgewiesenem Workflow-Fortschritt.
- Lease-Verlust wird sofort terminal als `canonical_worker_lease_lost` sichtbar.
- Drei echte Ticks ohne Fortschritt werden terminal `canonical_worker_no_progress`.
- Der zusätzliche interne Work-Block-Pausentakt wurde aus dem Workerpfad entfernt.
- Endpoint sendet `server_time`, `contract=external_tick_v2` und No-Cache-Header.
- GitHub verwendet Cache-Buster + `Cache-Control: no-store` und verwirft wiederholte/stale `server_time`-Antworten.
- Einzelne fachliche Produktfehler bleiben in der bestehenden Fachlogik überspringbar.

## Nicht verändert
Ausgehend vom installierbaren V6.61.16-Paket sind nur drei Plugin-Dateien geändert:
1. `includes/trait-ppar-ebay-run.php`
2. `pferdeportal-affiliate-router.php` (nur Pluginversion 6.62.0)
3. `readme.txt`

Alle übrigen Plugin-Dateien sind byteidentisch, insbesondere eBay-Fachlogik (`trait-ppar-ebay.php`), idealo, Provider-/Feed-/Rankinglogik, Frontend-CSS/JS, Portalabdeckung und Produktkartenlayout.

`EBAY_RUNTIME_BUILD` bleibt absichtlich unverändert, damit der aktuell persistierte kanonische Run nicht durch historische Build-Migrationspfade umgebaut oder zurückgesetzt wird.

## Lokale harte Prüfung
- V6.61.16 NEGATIV: busy/lease-lost werden fälschlich als `running` gemeldet.
- V6.62.0 POSITIV: `advanced`, `busy`, `failed` maschinenlesbar korrekt.
- Selection-Prepare: Fortschritt PASS; Lease-Verlust FAIL-CLOSED; 3× Nullfortschritt FAIL-CLOSED.
- Completion explizit `completed`.
- Fresh-Unpack PASS.
- PHP-Lint aller Plugin-PHP-Dateien PASS.
- Geänderte Plugin-Dateien exakt 3.

## GitHub-Taktgeber
Workflow-Commit für explizite Tick-Ergebnisse: `df58c018b03ac2af12662c2abf6705f002931a6f`
Workflow-Commit für Cache-Buster/Stale-Response-Guard: `e3daec9bfe8dc0ff7483734ec2d4e52d350ca9f0`

Der Plugin-Quellbaum auf `main` ist historisch/alt und wird deshalb **nicht** mit V6.62.0 überschrieben. Installationsbasis ist ausschließlich das verifizierte V6.61.16-Installerpaket aus dem laufenden Chat.
