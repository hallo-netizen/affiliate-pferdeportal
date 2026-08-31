# AFFILIATE-ZENTRALE V6.64.0 — Codex-Auftrag: exakte Digistore24-Source binden

Stand: 2026-08-31
Workstream: `AFFILIATE_ZENTRALE`
Branch: `affiliate-release-current`
Governance: `PFERDE_ATELIER_AFFILIATE_RELEASE_GOVERNANCE_V4`

## Einzige Aufgabe

Übertrage die vier **beigefügten lokalen Dateien byte-identisch** in ihre unten gebundenen Repository-Zielpfade und binde damit den bereits lokal getesteten Digistore24-Block an die kanonische Release-Quelle.

Dies ist **keine Rekonstruktion**, kein neuer Entwurf und keine neue Architektur. Die angehängten Dateien sind die Source-Autorität für genau diesen gebundenen Transfer. Ihre Bytes dürfen nicht verändert, formatiert, normalisiert oder neu erzeugt werden.

Vor jeder Änderung zuerst lesen:

`control/release-governance/CURRENT_RELEASE.json`

Nur fortfahren, wenn weiterhin gilt:

- `workstream=AFFILIATE_ZENTRALE`
- `mode=ENFORCED`
- `active_candidate.version=6.64.0`
- `execution_state.state=RUNNING_BOUND_RELEASE_GATES`
- `execution_state.authorized_next_action=RUN_BOUND_RELEASE_GATES`
- aktiver Branch `affiliate-release-current`
- die vier Zielpfade sind durch die aktuellen `authorized_change_prefixes` erlaubt.

## Vier exakte Eingabedateien

### 1. Digistore24-Trait

Beigefügter Dateiname:
`trait-ppar-digistore24-v664-auto.php`

Zielpfad:
`release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-digistore24.php`

Pflichtwerte:
- Bytes: `73596`
- SHA-256: `94115598adb6200c4d07bb43130ec31bcb0e5f5bc0a214bc54c2ec4054dcf2f3`
- Git-Blob-SHA1 (`git hash-object`): `c3ec4e1943092afb01a56fa7a46711b384a0a546`

### 2. Output-Objects-Trait

Beigefügter Dateiname:
`trait-ppar-output-objects-v664-ds24.php`

Zielpfad:
`release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php`

Pflichtwerte:
- Bytes: `136739`
- SHA-256: `6e3adf23735d7f326df96b4e66df2bc47bb3f75c390fad50416ce850676a185b`
- Git-Blob-SHA1 (`git hash-object`): `ba9f01db409bf005294ad45674d9314dcb3ef522`

### 3. Source-Manifest

Beigefügter Dateiname:
`CURRENT_SOURCE_SHA256.ds24.txt`

Zielpfad:
`release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt`

Pflichtwerte:
- SHA-256: `e5dfbaac4673f1e2c448691c6708a0173acdd8581ae1dab9aeac70eed25b227a`
- Git-Blob-SHA1: `0c65c9437b15a7244eb4fd3c1a45773b380f9166`
- Source-Dateien laut Manifest: `25`

Das Manifest unterscheidet sich vom vorherigen kanonischen Manifest ausschließlich durch die beiden gebundenen Source-Hashes der Dateien aus Punkt 1 und 2.

### 4. Governance-Bindung

Beigefügter Dateiname:
`CURRENT_RELEASE.ds24.json`

Zielpfad:
`control/release-governance/CURRENT_RELEASE.json`

Pflichtwerte:
- SHA-256: `078299143ac2bb4f8846086b27f165180d016efb5e7576cce64c88427aa7a97f`
- Git-Blob-SHA1: `a6417f14ab7371ac0a4a429ea81df1f09ff617e5`
- `source_authority.manifest_sha256=e5dfbaac4673f1e2c448691c6708a0173acdd8581ae1dab9aeac70eed25b227a`
- `active_candidate.current_source_manifest_sha256=e5dfbaac4673f1e2c448691c6708a0173acdd8581ae1dab9aeac70eed25b227a`
- Gate `explicit_scope_product_deals_partner_analytics` bleibt `PENDING`.
- `release_allowed=false` bleibt unverändert.

## Vor dem Schreiben

Prüfe lokal für **jede** beigefügte Datei:

```bash
wc -c <DATEI>
sha256sum <DATEI>
git hash-object <DATEI>
```

Bei irgendeiner Abweichung: **fail-closed**, nichts schreiben, nichts rekonstruieren, keine Ersatzdatei erzeugen.

## Schreibregel

Die vier Zielpfade müssen in **einem atomaren Commit** auf `affiliate-release-current` landen. Keine weiteren Dateien ändern.

Verboten:
- keine Zeilenendungsnormalisierung,
- kein Formatter,
- kein PHP-CS-Fix,
- kein automatisches JSON-Reformatting,
- kein Patch-Rebuild,
- keine historische Rekonstruktion,
- kein neuer Branch,
- keine neue Plugin-Version,
- keine ZIP-Erzeugung,
- keine eBay-Wiederholungsprüfung,
- keine Änderung an `.github/workflows/**`, Tests, Archive, Hardlocks oder Governance-Guard.

## Prüfung nach dem Schreiben

Unmittelbar nach dem Commit müssen die **committeten** Zielpfade erneut geprüft werden:

```bash
wc -c release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-digistore24.php
sha256sum release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-digistore24.php
git hash-object release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-digistore24.php

wc -c release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php
sha256sum release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php
git hash-object release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php

sha256sum release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt
sha256sum control/release-governance/CURRENT_RELEASE.json
php -l release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-digistore24.php
php -l release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php
```

Danach die vorhandenen Governance-Prüfungen nur in ihrem bestehenden Modus ausführen. Keine bereits hash-identisch bestandenen eBay-Gates wiederholen.

## Erwarteter Endzustand

Nur bei vollständiger Byte-Identität und Governance-PASS:

`DIGISTORE24_EXACT_SOURCE_BIND_PASS`

Ausgabe danach ausschließlich:
- Commit-SHA,
- vier bestätigte Zielpfade,
- SHA-256 der beiden PHP-Dateien,
- Manifest-SHA-256 `e5dfbaac4673f1e2c448691c6708a0173acdd8581ae1dab9aeac70eed25b227a`,
- Governance-PASS/FAIL,
- `release_allowed=false`,
- nächster gebundener Schritt: realer Digistore24-Livegate.

Bei FAIL nur exakter Fehler und Beleg; keine Alternativroute.