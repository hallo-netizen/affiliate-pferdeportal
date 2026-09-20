# Affiliate – Übergabe neuer Chat – 20.09.2026 10:56:39 +02:00

Diese Datei ist **nur Wegweiser**. Keine zweite CURRENT-/Status-/NEXT-ACTION-Wahrheit.

## EXAKTER EINSTIEGSPUNKT

Nachfolgechat ab **20.09.2026 10:56:39 +02:00**.

Pflichtweg:
1. Repo `hallo-netizen/affiliate-pferdeportal`
2. Branch `affiliate-release-current`
3. `release/affiliate-zentrale/AGENTS.md`
4. genau eine Current-Autorität: `control/release-governance/CURRENT_RELEASE.json`
5. erwartete Current-Generation: **75**
6. Current-Blob-SHA nach der Recovery-Nachholung: `fb24b4a0377f936e963937efb17f648304c341e1`
7. Commit, der diese Current-Generation gebunden hat: `527bf88cafe4a3ae223f51c5f54f35d5d888c43a`
8. beim Einstieg Branch-HEAD frisch lesen; wenn Generation/Blob unverändert sind, **KEINE VOLLREKONSTRUKTION**, direkt die NEXT ACTION aus CURRENT ausführen.
9. bei Änderung seit diesem Commit nur das Delta prüfen.

## ZIELVERTRAG

Aktiver Recovery-Zielvertrag:
`protocol/AFFILIATE_RELEASE_EMERGENCY_RECOVERY_672108_STATE_TARGET_20260920.md`

Langfristiger Zielvertrag bleibt unverändert:
`protocol/AFFILIATE_RELEASE_AUTOMATIC_CREATIVE_LIFECYCLE_SCOPE_20260918.md`

Recovery hat Vorrang. Keine neue Affiliate-Fachentwicklung vor Recovery-LIVE-PASS.

## AKTUELLER BELASTBARER STAND

- Kanonische Repository-Source: weiterhin **6.72.105**, 26 Dateien.
- Kanonischer Source-Manifest-SHA: `ab1f4f54a7b0743e00ccbde5e1c11aa278a790ca47e5f72348bd125be9eabf29`.
- Letzter belastbar getesteter/live verwendeter Referenzstand vor dem Incident: **6.72.108**.
- 6.72.108 ZIP SHA-256: `d8aeb69bd67a18072996da9ca8101923e6ff6765a40c5d0d6a6f74bde3be5bb3`.
- 6.72.108 Source-Manifest-SHA: `d7771d6f2d7816217b0ccd576580bf722a22a40f5d1e19b333e29b5775719b8e`.
- Aktuell installierte Live-Pluginversion nach 6.72.109–117 und Downgradeversuchen: **NICHT BELASTBAR BESTIMMT**.
- Keine physische Löschung von WordPress-Beiträgen/Produkten ist belegt.
- Belegt ist eine massive **Ausgabe-/Persistenzregression**.

## ERSTER OFFENER FEHLER / BLOCKER

`AFF-ERR-039`

Nichtkanonische 6.72.109–117 haben persistente WordPress-Zustände verändert. Ein Downgrade des PHP-Plugins stellt diesen Zustand nicht wieder her.

Autoritative Fehlerbeschreibung:
`protocol/AFFILIATE_RELEASE_ERROR_REGISTER.md#aff-err-039`

Vollständiges Nachhol-/Incidentprotokoll:
`release/affiliate-zentrale/evidence/incident_672109_118_persistent_state_regression_20260920.txt`

## WAS WURDE SCHON GEMACHT

- 6.72.109 Banner-Placement-Plan eingeführt.
- 6.72.110 Partneranalytics-v2/Bootstrap eingeführt.
- 6.72.111–113 Reithelme-/Deeplink-/Report-Fixes versucht.
- 6.72.114 Awin-Destination-Auflösung und Produkt-Schwellenänderung versucht.
- 6.72.115 Mehrprovider-Reparaturversuch; dabei idealo-Modus/Activation/Artikelplan-Revision persistent verändert.
- 6.72.116 Revisions-Recovery versucht.
- 6.72.117 Sichtbarkeits-Recovery versucht.
- zwei unterschiedliche 6.72.118-Recoverykandidaten lokal gebaut.
- vorhandene ZIPs 6.72.108–118 lokal gegeneinander byte-/codebezogen forensisch verglichen.
- Current-Autorität, Fehlerregister und Recovery-Zielvertrag auf den tatsächlichen Incidentstand nachgezogen.

## WAS HAT NICHT GEHOLFEN

- 6.72.110–113: beanstandete Livefehler nicht behoben.
- 6.72.114: Produktdarstellung nicht stabilisiert.
- 6.72.115: sichtbarer Produktausfall wurde massiv verschärft.
- 6.72.116: keinerlei sichtbare Wiederherstellung laut Nutzer.
- 6.72.117: nicht der alte Zustand; stattdessen generische Produktplatzhalter und beanstandeter Direktwerbeplatz-Platzhalter.
- ältere ZIP wie 6.72.111 erneut installieren: Fehler bleiben bestehen.
- lokale POS/NEG-Mocktests ersetzen keinen realen WordPress-Persistenztest.

## WAS IST KAPUTT

Belegt:
- Kategorie-Produkt-/Artikelausgabe entspricht nicht mehr dem letzten funktionierenden Zustand.
- zeitweise nur eine Produktkachel pro Kategorie.
- eBay verschwand aus der sichtbaren Produktmischung; idealo blieb.
- später sichtbare Artikel-/Produktausgabe weg.
- nach Recoveryversuch generische Produktplatzhalter sichtbar.
- beanstandeter Direktwerbeplatz-Platzhalter sichtbar.
- Reithelme-Bannermatching blieb falsch.
- Code-Downgrade allein stellt den Zustand nicht wieder her.

Nicht belegt / NICHT RATEN:
- keine bestätigte physische Datenlöschung;
- aktuell aktive Pluginversion;
- exakte aktuelle DB-Werte der betroffenen Optionen/Postmeta;
- exakter minimaler Recovery-Delta;
- Verfügbarkeit eines exakt passenden Vor-6.72.109-Backups.

## GENAU EINE NEXT ACTION

**KEINE PLUGININSTALLATION.**

Rein lesenden Live-Readback erstellen und exakt erfassen:
- aktive Pluginversion;
- `ppar_article_plan_revision_v1`;
- `ppar_article_plan_log_v1`;
- `ppar_article_plan_rebuild_state_v1`;
- relevante `ppar_article_delivery_plan_v1`-Postmeta;
- `ppar_network_idealo_v1` inkl. `output_mode`;
- `ppar_banner_placement_plan_v2`;
- `ppar_partner_analytics_report_cache_v2`;
- `ppar_partner_analytics_bootstrap_v672110`;
- `ppar_multiprovider_category_repair_v672115`;
- `ppar_v672115_article_revision_recovery_v1`;
- `ppar_v672117_product_visibility_recovery_v1`;
- betroffene Cron-Hooks;
- Awin-Creative-Zeilen mit `_destination_*`-Payloadzustand.

Dann **nur den belegten persistenten Delta gegen 6.72.108** bestimmen. Erst danach darf ein Recoveryweg gebaut werden.

## NICHT ANFASSEN

- keine weitere 6.72.109–6.72.118 installieren;
- **6.72.118 ausdrücklich gesperrt**: zwei verschiedene Pakete tragen dieselbe Versionsnummer;
- keine Banner-/Reithelme-/Produkt-/Analytics-Neuentwicklung;
- keine globale `campaign_revision`;
- kein pauschaler Artikelplan-Rebuild;
- keine Provider-Modusänderung;
- geschützte Journal-/Glossar-/Pferderassen-/Kategoriepfade nicht verändern;
- `AFF-ERR-035` erst nach Recovery wieder aufnehmen.

## 6.72.118 – NICHT VERWECHSELN

Zwei unterschiedliche Artefakte:
- SHA-256 `544ff072f3ec893fb3eb6244c8b22fce73ec18e540bd22fb54829ec96c66bbd4`
- SHA-256 `3923edf87d90bac2dd1eb20723e17553310664c4105666b6cbea9d765a3fc10f`

Keines hat einen Live-PASS. Keines installieren.

## TEST-/GUARD-GRENZE

- Branch/HEAD, Bürotür, Current, kanonische Source und Manifest wurden frisch über GitHub gelesen.
- Der lokale Versuch, den Repository-Guard auf einem frischen Clone auszuführen, scheiterte an fehlender DNS-/Netzwerkauflösung im Container.
- Daher **kein governance-check/start PASS** behauptet.
- Die ZIP-Forensik auf den tatsächlich vorhandenen 6.72.108–118-Artefakten wurde lokal ausgeführt.
