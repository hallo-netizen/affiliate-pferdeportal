# Affiliate Release External Controller – Arbeitsprotokoll

Stand: 2026-08-29 19:43 Europe/Berlin

## Ziel

Externe Kontrollinstanz fuer die Affiliate-Zentrale so fertigstellen, dass der Arbeitsfluss nicht mehr chat-zentriert, sondern durch einen gebundenen GitHub-State kontrolliert wird.

## Verbindliche Leitplanken

- eine kanonische direkte Source unter `release/affiliate-zentrale/current/affiliate-portal-router/`
- `CURRENT_RELEASE.json` ist maschinenlesbare State-Wahrheit
- Arbeitsbranch: `affiliate-release-current`
- keine neue Release-/Staging-/Versionsbranch-Navigation
- keine Rekonstruktion alter Git-Staende als laufende Source-Autoritaet
- keine Wiederholung hashidentisch bestandener PASS-Stufen
- maximal ein aktiver Arbeitsstrom
- nur der im State gebundene naechste Schritt ist zulaessig
- Release bleibt fail-closed bis alle gebundenen Gates PASS sind

## 2026-08-29 – Source-Autoritaet

- Hochgeladene MASTER gefunden und lokal materialisiert.
- MASTER-SHA256 bestaetigt: `ffe1fa964da7eda60a83542c20594a578ba14593f2af2914e6676d039ce8bf29`.
- Direkter V6.63.8-Quellbaum in der MASTER gefunden.
- Exakte Source: 21 Dateien.
- 21/21 Datei-SHA256 gegen `CURRENT_SOURCE_SHA256.txt`: PASS.
- Source-Manifest-SHA256: `40972031c4e6ca2937bc3571de1b537950b8311e607c86d304b25c74ad3047d1`.
- Alte historische V6.63.5/V6.63.8-Delta-Kette als nicht verlaessliche Materialisierungsautoritaet verworfen.
- V6.62.0 und V6.63.4 bleiben historische Referenz-/Negativbeweise, nicht aktuelle Source.

## Aktueller gebundener Schritt

`COMMIT_EXACT_V6638_21_FILE_SOURCE_TO_CANONICAL_ROOT`

Erfolgskriterium: `DIRECT_SOURCE_21_OF_21_HASH_PASS`.

Danach ausschliesslich vorgebundener Uebergang zu `RUNNING_BOUND_RELEASE_GATES` / `RUN_BOUND_RELEASE_GATES`.
