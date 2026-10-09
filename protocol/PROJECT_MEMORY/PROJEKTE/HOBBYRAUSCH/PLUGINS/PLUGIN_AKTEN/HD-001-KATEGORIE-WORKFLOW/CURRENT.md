# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-09
STATUS: 1.14.8 CODEBASIS / RULE 2.7 FAIL-CLOSED PROFIL LOKAL PASS / LIVE-DRY-RUN PENDING

## Plugin

ID:
`HD-001-KATEGORIE-WORKFLOW`

Name:
`Affiliate-Portal Kategorie-Workflow`

Art:
Eigenentwicklung / allgemeingültiger Kategorie-Workflow mit Hobby-Depot-Profil.

Fachbüro:
`SEO_KATEGORIEN`

## Aktuelle technische Wahrheit

Freigegebene Codebasis:
`1.14.8`.

V1.14.9 und V1.14.10 sind verworfen und dürfen nicht weiterverwendet werden.

Aktueller lokal freigegebener Profilkandidat:
`HD001_V1.14.8_RULE27_FAILCLOSED_COMPLETE_ONE_SYNC_HARDPASS.zip`

SHA-256:
`0ae09fa5d75656416a0e4e7c1bb4fab74e01e776c2e36b13b8b6734a9efc5c0c`

Revision:
`HD-TARGET-3P-RULE27-FAILCLOSED-COMPLETE-20261009+bacb614f00854923`

Gegenüber dem zuvor live vorgeprüften 2148er Kandidaten wurde ausschließlich
`profiles/hobby-depot-v1.json`
geändert.

Grund:
46 nur generisch erzeugte, nicht per Hobby mit >=3 eigenständigen Intents belegte `Ausrüstung & Kosten`-Leafs wurden fail-closed entfernt.

PHP-Code, DataForSEO-Client, Dry-Run-Engine, Sync-Engine, Writer und Deployment-Writer wurden dabei nicht verändert.

## Lokale Abnahme des aktuellen Kandidaten

Frisch wiederholt:
- ZIP-Integrität PASS;
- PHP 33/33 PASS;
- Dry-Run gegen realen 1.14.8-Live-Baseline-Stand PASS;
- 373 CREATE / 0 ADOPT / 1729 UPDATE / 6 ARCHIVE;
- Full Sync COMPLETE;
- 2102/2102 Readback;
- Frontend PASS;
- 279/279 HOBBY_HUBs PASS;
- Header PASS;
- zweiter Dry-Run 2102 UNCHANGED / 0 Delta.

Evidence:
`../../../SEO_KATEGORIEN/HD001_RULE27_FAILCLOSED_FINAL_LOCAL_ACCEPTANCE_20261009.md`

## Live

Der im WordPress-Backend aktuell sichtbare 2148er Dry-Run gehört zum verworfenen Vorgängerprofil und darf NICHT synchronisiert werden.

Der fail-closed 2102er Kandidat ist noch nicht live installiert/geprüft.

## ERSTER OFFENER BLOCKER

`HD001_RULE27_FAILCLOSED_LIVE_DRYRUN_PENDING`

## EXAKT EINE NEXT ACTION

Operativ ausschließlich der Fach-Current folgen:
`../../../SEO_KATEGORIEN/CURRENT_STATE.md`.

Kein Sync des 2148er Plans.

## Rollback / Sicherheitsgrenzen

- 1.14.8 bleibt Codebasis;
- Dry-Run vor Writes;
- Live-Fingerprint-Recheck vor Apply;
- Drift = BLOCKED;
- bounded Sync + Readback;
- Rollback bei Readbackfehler;
- kein Hard-Delete als Normalweg;
- DataForSEO erzeugt/verschiebt keine Struktur.

## Artefaktstatus

Die lokale ZIP-Datei ist bytegenau geprüft und dem Nutzer als Chat-Artefakt verfügbar.

`ISOLIERTE_PLUGINS/.../CURRENT.zip` ist weiterhin NICHT im GitHub-Campus synchronisiert, weil der verfügbare GitHub-Connector keinen lokalen Binärdatei-Upload übernimmt. Kein Binary wird erfunden oder als synchronisiert behauptet.

Das zugehörige Manifest wird auf diesen Stand nachgezogen.
