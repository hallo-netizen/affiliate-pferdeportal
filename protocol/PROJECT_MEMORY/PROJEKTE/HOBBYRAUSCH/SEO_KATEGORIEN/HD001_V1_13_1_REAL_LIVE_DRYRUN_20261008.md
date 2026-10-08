# HD-001 V1.13.1 – REALER LIVE-DRY-RUN

STAND: 2026-10-08
STATUS: FINAL TARGET DRY-RUN PASS / ALTER ROLLBACK IM EXPORT NOCH PENDING / FRISCHER POST-ROLLBACK-READBACK OFFEN

Reale Datei:
`hobby-depot-final-target-readback-20261008-082217-utc.json`

Dry-Run:
- contract = APKW_FINAL_TARGET_DRY_RUN_V1
- plugin_version = 1.13.1
- status = PASS
- valid = true
- 841 Inventar-Identitäten
- 340 CORE
- 501 Finder/Editorial
- 440 Logikknoten
- 431 physische Zielobjekte
- worlds_core_level_1 = true
- 8 Hobbywelten-View-Relations
- CREATE 12
- ADOPT 0
- UPDATE 419
- UNCHANGED 0
- ARCHIVE 1
- errors = []
- provider_calls = 0
- provider_cost_usd = 0
- wordpress_structure_writes = 0

CREATEs:
Scale-Crawling, Drohnenfotografie, BattleBots-Modellbau, Morsefunk, Drone Soccer, RC-U-Boote, RC-Segelflug, Funkpeilung, Wabikusa, RC-Segelboote, Wettersonden-Tracking, RC-Panzer.

ARCHIVE:
alte Brettspiele.

Damit entspricht das reale Live-Delta exakt dem lokal erwarteten Finaldelta.

WICHTIG:
Im selben Export steckt noch ein ALTER V1.12-Sync-State:
- status = ROLLBACK_PENDING
- Fehler = Target-Tree-Readback fehlgeschlagen: directory:events-reisen [name]
- runner_status = RUNNING / EXISTING_TARGET_TREE_RESUME

Der V1.13.1-Runner setzt diesen alten Rollback automatisch fort.
Der neue finale Sync wurde noch NICHT gestartet.

Der spätere Screenshot von 10:31 zeigt keinen sichtbaren "Sync läuft automatisch"-Hinweis mehr. Das spricht dafür, dass der alte Rollback inzwischen terminal geworden ist; dies ist aber erst mit einem neuen JSON-Export belastbar bestätigt.

NEXT:
1. KEIN Sync.
2. Auf derselben Seite erneut "Finalen Delta-Dry-Run ausführen".
3. Danach "Finalen Readback als JSON herunterladen".
4. Neuen JSON-Readback prüfen.
5. Nur wenn alter Sync-State terminal und der neue Dry-Run weiter PASS ist: exakt einen finalen Sync starten.
