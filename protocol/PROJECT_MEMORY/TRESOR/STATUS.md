# NOTFALL-TRESOR – STATUS

STAND: 2026-09-05

ERGEBNIS:
`TRESOR_FAIL:RECOVERY_DEPENDENCIES_UNVERIFIED`

## Git-/Repository-Sicherung – PASS

Externer PREPASS-Speicher:
`/Campus-Tresor/2026-09-05_132542_PREPASS/`

Aktueller V2-Tresor:
`CAMPUS_TRESOR_GIT_MIRROR_20260905_V2.zip`

GitHub-Actions-Artefakt:
- Artifact ID: `9970336506`
- Artifact-Digest: `sha256:2e4ba85da266105b82fb57e75e1d35699305b2e38adb0d2bb105ba8f4f603c14`

Git-Bundle SHA-256:
`0809fb0a170224fdde70f37c2f1433d04107a89d783a6c277a6eb57b78a455f5`

## Gebundene Stände

- main: `c8a96e7a2f598de69134d90b143257c3559bc98a`
- Campus: `04130dfde2f2682f87fb887730f31ad5c650153d`
- Paul TEXT/SEO: `515550994b97505a463a0bf1a8f212e8bc0a346e`

## Vollständigkeitsbeleg V2

- Branches: 261
- Tags: 1
- Issues: 136
- Pull Requests: 127
- Releases: 1
- Rulesets: 1
- Workflows: 59

Zusätzlich extern gesichert:
`RULESET_21788951_FULL.json`

Der aktive Main-Ruleset enthält u. a.:
- Löschschutz;
- Non-Fast-Forward-Schutz;
- Pull-Request-Regel;
- Pflichtchecks `hardlock` und `hardlock-base`.

## Wiederherstellungstest

Git-Bundle wurde im isolierten Workflow:
- verifiziert;
- geklont;
- mit `git fsck --full` geprüft.

Ergebnis:
`GIT_BUNDLE_RESTORE_PASS`

## Erster verbleibender Blocker

Noch NICHT hart verifiziert:
alle nicht automatisch exportierbaren Wiederherstellungsabhängigkeiten, insbesondere Secrets/Schlüssel/externe Autorisierungen.

Der Inhaltsvertrag verlangt für jede solche Abhängigkeit entweder:
1. sichere wiederherstellbare Quelle oder
2. eindeutige Wiederherstellungsprozedur.

Bis diese Prüfung abgeschlossen ist:

**KEIN TRESOR_PASS.**

## Harte Regel

Ein Git-/Metadaten-PASS allein ist noch kein vollständiger Katastrophen-PASS.

Der nächste gültige Endstatus ist erst nach Prüfung der Recovery-Abhängigkeiten und vollständiger Tresor-Abnahme zulässig.
