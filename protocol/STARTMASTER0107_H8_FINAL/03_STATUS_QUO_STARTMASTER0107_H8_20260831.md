# STARTMASTER0107 / H8 – STATUS QUO

Stand: 2026-08-31

## GitHub

Repository: `hallo-netizen/affiliate-pferdeportal`  
Aktueller `main`: `a3708a322f493578596c374736ef328d0caba504`

H8 Produktivmerge:
- PR #58
- Commit `298711faf3a17ff3faeed53de8276f812523c96d`

Dokumentationsmerge:
- PR #59
- aktueller Commit `a3708a322f493578596c374736ef328d0caba504`

CI:
- H8 PR-Checks: PASS
- H8 Post-Merge Deterministic Entrance Gate Run 104: SUCCESS
- aktueller `main` Deterministic Entrance Gate Run 106: SUCCESS

## Aktiver Einstieg

`control/CURRENT_STARTMASTER.json`:
- STARTMASTER0107
- `gate_ref = control/single-door-boundary/project_single_door_entry_v2.py`
- `free_chat_execution_authority = false`
- hard worker: CODEX_CLOUD

## Aktueller Workflow-State

- 107001–107006: abgeschlossen
- nächster autorisierter äußerer Step: 107007 `RUN_NEW_ARTICLE_BATCH_NO_STOP`
- danach gebunden: 107008 Final Review / Await User Publish
- Auto-Publish: nein

## Aktueller Runtime-State

- Status: `BATCH_READY_PACKAGE_PENDING`
- Generation: 1
- Batch SHA: `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
- Source Snapshot: `control/startmaster0107/runtime_inbox/generations/000001/SOURCE_SNAPSHOT.json`
- Runtime Snapshot SHA: `be73a986124fc80429c0c0d85fba94636a0ff5a506d23a6cff68f291e3645027`
- Produktionspaket: noch nicht gebunden
- `publish_allowed = false`

## Aktuelle sieben gebundenen Themen

1. `hindernisstangen-beratung` — **Das Wichtigste über Hindernisstangen für Pferde** — Keyword: `Hindernisstangen für Pferde` — Plan-Slot `9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56`
2. `reitplatzbeleuchtung-beratung` — **Eine richtige Reitplatzbeleuchtung ohne Mast finden** — Keyword: `Reitplatzbeleuchtung ohne Mast` — Plan-Slot `6ce9a1e47446daf84e85f08e84c33ada214f92612a654d79e68df18ea4e9fa19`
3. `mistcontainer-beratung` — **Mistcontainer mit Deckel wählen** — Keyword: `Mistcontainer mit Deckel` — Plan-Slot `7b0e8f8b0653eb3a40aee2a68f4b9909df9d8bda374db0ec8c49e7b53ecbee87`
4. `pferdehaftpflicht-beratung` — **Pferdehaftpflicht mit Fremdreiter auswählen** — Keyword: `Pferdehaftpflicht mit Fremdreiter` — Plan-Slot `5999b9b00de2a1756101c5ebfb2b547c6ff2b9360bd9bae0988696a795ff6288`
5. `huffett-beratung` — **So findest du Huffett für Pferde** — Keyword: `Huffett für Pferde` — Plan-Slot `7f7a0b4169c19676b3dfe6457ac07c6685ae6ead6c1873a9467d9b6ee32a81da`
6. `fliegenmasken-beratung` — **So wählst du geeignete Fliegenmasken für Pferde** — Keyword: `Fliegenmasken für Pferde` — Plan-Slot `8c8408cebf7f41becc33cdccf04b60387cf75644468a887730a8d18a4a1a7648`
7. `pellets-beratung` — **Wissenswertes über Pellets für Pferde** — Keyword: `Pellets für Pferde` — Plan-Slot `906ddc4ee72429a8544da018e1f78d63cb2b80c1f11488180f381e2dc16c4af5`

## H8-Sicherheitszustand

Repositoryseitig aktiv:
- neue erste Tür `R_BOOT_001`
- nur eine erzwungene Capability
- fachblind
- H8 Herkunftsbindung
- erneute Herkunftsprüfung vor `R_001`
- altes/frei erzeugtes Paket ohne H8-Bindung blockiert
- Chat hat keine Workflow-Autorität

## Aktueller offene Punkt

**Noch offen/nicht nachgewiesen:** produktive serverseitige Producer-/Signer-Capability an `R_BOOT_001`.

Bis diese Bindung verfügbar und real positiv getestet ist:
- bleibt `R_BOOT_001` fail-closed,
- keine Artikelproduktion,
- kein Chat-Fallback,
- keine Ersatzsignatur,
- keine neue Architektur aus dem Chat.

## Nächster echter Test

Sobald die Producer-/Signer-Capability gebunden ist:
`R_BOOT_001 -> Paket -> R_PRE_001 -> R_001 -> bestehender kompletter Fachworkflow`

Dann den gleichen 7er-Batch vollständig neu produzieren. Die alten Artikeltexte sind keine Produktionsquelle.
