# MASTER016-R11 – Exact Live Input Artifact Rootfix

## Live-Fehler
WordPress 4A reproduziert `SOURCE_INVALID` am Pfad `source`: `source muss ein Objekt sein.`

## Root Cause
Der aktive V1.8.0-Validator und `schema-category-v1.4.json` sind korrekt fail-closed. Das tatsächlich ausgelieferte R10-Stage-13-Paket wurde nach den erfolgreichen Workflowtests noch metadaten-seitig verändert: Das zuvor schema-konforme `source`-Provenienzobjekt wurde durch den String `MASTER016-R10 R9_RUNTIME_PREPARED_FROM_APPROVED_VISIBLE_TREE_NO_LIVE_RECEIPT` ersetzt.

Damit prüften die R10-Gesamtworkflowtests nicht bytegenau das letzte, tatsächlich an den Nutzer ausgelieferte Live-Eingabeartefakt. Der R10-Prepack-Audit enthielt außerdem nebeneinander den Real-Workflow-Technical-Scope `5a3a145504855ce1fc7f7726bff0f6e11448ae36c33a6d172557a03baae70279` und den Prepared-Artifact-Scope `18c58234aec850988ac0957b4853a7bc82436ab2919fb50eb5110cb5f18e1dc2`, ohne diese Differenz fail-closed zum Releaseblocker zu machen.

## Korrektur
Produktionscode V1.8.0 bleibt unverändert. Im Live-Eingabeartefakt wird ausschließlich `source` wieder als Provenienzobjekt geführt; Nodes, Project, Research-Bindung, SEO-/Affiliate-Metadaten und Targets bleiben unverändert.

Neue allgemeingültige Regel R-181: Ein Release-PASS gilt ausschließlich für das exakte, nach der letzten Serialisierung tatsächlich auszuliefernde Live-Eingabeartefakt. Exakte Datei-SHA, aktives Schema/Runtime, Research-Bindung sowie Visible-/Technical-Scope müssen im Release-Audit übereinstimmen. Jede spätere Mutation hebt den PASS auf.

## Regression / Exact Artifact
- R10 Negativartefakt SHA-256: `3bb0bfeb1b125b965a40301670d50616afe1a32475edbaabc4e03bd86d1784bd`
- R10 Negativ: Validator `SOURCE_INVALID`, Evidence `BLOCKED_SCHEMA`, Comparator `BLOCKED_SCHEMA`
- R11 korrigiertes Artefakt SHA-256: `e77f0d0c5f56952cffa932a696139ea160df92576f38f8a7856135fe7b0d5152`
- JSON Schema: 0 Fehler
- Semantischer Diff R10 -> R11: ausschließlich Top-Level-Feld `source`
- Active Source V1.8.0: 216/216 PASS; Validator PASS; Research-Bindung PASS; Evidence PASS; R9 151/151 SEO + 151/151 Affiliate; Comparator PASS_READ_ONLY_PREVIEW
- Fresh Installer V1.8.0: 216/216 PASS; gleiche Exact-Artifact-Ergebnisse
- Lossless Coverage: 8.127/8.127; unassigned=0; silent_drop=0; parent_cascade_drop=0
- Visible Scope unverändert: `a1a2f530e43df4f54e0f723e3cd4c8719b4673876ae864156538f2a1395ab07a`
- Technical Scope unverändert gegenüber dem vorbereiteten R10-Livepaket: `18c58234aec850988ac0957b4853a7bc82436ab2919fb50eb5110cb5f18e1dc2`
- Source <-> Installer: 57/57 Dateien, 0 Diff
- PHP lint: 15/15 Source + 15/15 Fresh Installer
- Keine neuen DataForSEO-Calls

## MASTER016-R11
- aktive Regeln: 181/181
- aktive normative Dateien: 18/18
- Workflow: exakt 14 Stufen
- Plugin: V1.8.0 unverändert
- Master Fresh-Unpack Manifest: 819/819 PASS
- Master ZIP SHA-256: `e8b187416300c26c783cdc0cd5d6288701f101deaca6965490252b91f1e63578`

## Live-Grenze
LIVE WordPress 4A mit dem korrigierten exakten R11-Artefakt ist noch nicht ausgeführt und darf nicht als PASS behauptet werden. Danach gelten weiterhin serverseitige Visible-Review-Signatur, Live-Dry-Run, explizites Apply und Readback/Baseline.