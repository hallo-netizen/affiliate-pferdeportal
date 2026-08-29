# Affiliate Release Governance – Rootcause und Bindung

Ursache der wiederholten Schleifen war nicht ein einzelner eBay-Fix, sondern fehlende technische Eindeutigkeit der Releasequelle: Live-ZIP, Chat-Artefakt, historische GitHub-Bäume, Staging-Patches und Nebenbranches konnten verwechselt werden. Tests wurden außerdem teilweise als Releasebeleg behandelt, obwohl reale WordPress/MariaDB-Gates noch offen waren.

## Verbindlicher Fix

1. Exakte V6.62.0-Basisbytes werden im Repository archiviert und gehasht.
2. Exakte V6.63.4-Fehlerreferenz wird im Repository archiviert und gehasht.
3. Eine einzige aktuelle Arbeitsquelle existiert: `CURRENT_WORKING_SOURCE.b64/` (direkte Base64-Abbildung der exakten ZIP-Bytes).
4. Keine Rekonstruktion aus Historie/Patches ist zulässig.
5. Genau ein dauerhafter Arbeitsbranch: `affiliate-release-current`.
6. Release nur bei vollständiger, hashgebundener PASS-Kette.
7. Bestehende GitHub-Main-Regeln bleiben fail-closed; kein Direktwrite, kein Bypass.

Damit kann ein neuer Chat nicht mehr eigenmächtig eine andere Baseline auswählen oder eine fehlende Datei erfinden: Fehlt/abweicht ein gebundenes Byte, blockiert der Guard.
