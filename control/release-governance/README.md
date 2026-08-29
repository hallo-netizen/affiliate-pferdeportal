# Affiliate-Zentrale Release Governance

Dieser Ordner verhindert Versions-/Quellen-Drift technisch und fail-closed.

- `CURRENT_RELEASE.json` ist der einzige Release-State.
- `release/affiliate-zentrale/current/CURRENT_WORKING_SOURCE.b64/` (Base64-Chunks der exakten ZIP-Bytes) ist die einzige Arbeitsquelle.
- V6.62.0 und der gebundene V6.63.4-Negativfall liegen als exakte, hashgebundene Bytes im Repository und werden nie rekonstruiert.
- Release-Arbeit ist nur auf `affiliate-release-current` zulässig.
- Jeder Release-Gate-PASS braucht eine SHA-gebundene Evidence-Datei.
- Solange ein Gate offen ist, verweigert `release-check` die Freigabe.
- Historische Branches, CI_V*/STAGING_V*, Chat-Dateien und der alte Root-Pluginbaum besitzen keine Release-Autorität.

Start jeder Affiliate-Arbeit:

`python3 control/release-governance/release_guard.py start --branch "$(git branch --show-current)"`

Release:

`python3 control/release-governance/release_guard.py release-check`
