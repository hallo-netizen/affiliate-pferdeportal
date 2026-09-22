# REPOSITORY-BESEN-AUDIT – 2026-09-22

STATUS: HAUSMEISTER-AUDIT ABGESCHLOSSEN / KEINE LÖSCHUNG

## Harte Schutzregel

Bei diesem Lauf wurden **keine aktuellen Einträge, keine CURRENT-/START_HERE-/HOBBYRAUM-/Ziel-/Fehlerautoritäten und kein aktuelles Plugin gelöscht oder verschoben**.

Das aktuelle Pferde-Atelier-Pluginregister wurde vor dem Audit frisch gelesen.
Aktuelle Pluginartefakte unter `/Campus-Plugins/PFERDE_ATELIER/<PLUGIN-ID>/CURRENT.zip` sind ausdrücklich tabu.

Hausmeisterregel bleibt:
**AKTIV oder UNGEKLÄRT = nicht verschieben. Dateien nicht löschen.**

## Mengenprüfung main

Frisch vermessener `main`:
- 422 Dateien;
- ca. 86.45 MB Dateiinhalt;
- 17 ZIP-Dateien;
- ZIP-Dateien zusammen ca. 75.70 MB.

Damit liegen rund 88 % des aktuellen Datei-Inhalts in ZIP-Paketen.

## Große historische/diagnostische ARCHIVKANDIDATEN

Die folgenden Dateien liegen im Repository-Root, stammen aus einzelnen Upload-Commits im August 2026 und sind nach exakter Dateinamensuche im aktuellen Default-Branch **nicht als aktive Referenz gefunden worden**.

WICHTIG:
Das reicht für `ARCHIVKANDIDAT`, aber nicht für Löschung. Deshalb wurde nichts entfernt.

| Datei | Bytes | Git-Blob | Ursprungscommit |
|---|---:|---|---|
| `CODEX_QUELLCODE_SANDBOX_ROOTCAUSE_FINAL_20260819.zip` | 15059533 | `f73b598f7d0693f19b06dab110a3eaeb97b39d4c` | `526184bb6d64ba601c954c5daf007768d5023316` |
| `CODEX_QUELLCODE_JOURNAL_WORKFLOW_ROOTCAUSE_20260819 (1).zip` | 14847896 | `3aa62b5c8e5f778ae34caae575bd105de610664c` | `8c3179b4a2376879f4e87c6f3e2eb7c44de1c1bb` |
| `CODEX_QUELLCODE_REDPLAN_GATEWAY_TIMEOUT_AUDIT_20260819.zip` | 14522436 | `b7b85205e62478e6d49607d347059dd643f2c2d2` | `d4271852c1078abc8c0db704e6bfe852417b68f9` |
| `CODEX_JOURNAL_LIVE_ROOTCAUSE_SOURCE_AND_TASK_20260820.zip` | 8737102 | `2e78ab932a35c87288c8748cf2ff4117163c9353` | `a87994b322febb5cbcba2702e3048e17371cc109` |
| `CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820.zip` | 6636538 | `47716ac5993db7a3fc8632afba2399bcf5619f21` | `f79d264127c4879d476578cf7b429f765a1e5bce` |
| `CODEX_PSTE056_HANDOFF_MINIMAL_20260820.zip` | 4473442 | `88fe7193fd729e22733f960ae9e2ef0a066e0b03` | `f7e96f2a25ae330b9d5da70bbd6c2c4be206a91e` |
| `CODEX_QUELLTEXT_AFFILIATE_EQUAL_CARD_ROOTCAUSE_V6610_20260827.zip` | 3857992 | `7b613eed1b559791611845b8cbc2d738cf0321d4` | `3ea2d862e92dcd366a4cc3fdda390ed3e76919ca` |
| `CODEX_QUELLTEXT_V6611_LIVE_FAIL_EQUAL_CARDS_20260827.zip` | 1607475 | `1de13836ddcd022fc9e0146949df635e3bb88eab` | `334a259a0af74a8d35724064a3bedcbf85b6cfc1` |
| `CODEX_QUELLCODE_AFFILIATE_ZENTRALE_AKTUELL.zip` | 507288 | `e170a014b9f63daa3b6a87cde9017b42f2a0accc` | `63ef7a09aa81f24fb803714d3cdaa12cabe2a803` |

Gesamt dieser neun Kandidaten:
70249702 Bytes ≈ 70.25 MB.

## Einordnung

Diese neun Kandidaten machen ca. 81.3 % des aktuell vermessenen Datei-Inhalts von main aus.

Sie sind deshalb der mengenmäßig wichtigste Besen-Block.

## Noch KEIN Entfernungs-PASS

Vor einer echten Entfernung aus `main` wäre je Datei zusätzlich nötig:
1. eindeutiger HISTORISCH/ABGELÖST-Beleg;
2. aktive Referenzprüfung gegen zuständige Fach-/Current-Autoritäten;
3. unveränderte externe Archivkopie;
4. Hash-Readback der Archivkopie;
5. erst danach separater, ausdrücklich autorisierter Entfernungsweg.

Bis dahin:
**NICHT LÖSCHEN.**

## Geschützte aktive Bereiche

Insbesondere nicht anfassen:
- `protocol/PROJECT_MEMORY/**` aktive Campusakten;
- `control/**` aktive Startmaster-/Runtime-/Governancewege;
- aktuelle Fachquellen/Releasequellen;
- alle im Pferde-Atelier-Pluginregister als aktuell/synchronisiert geführten Plugins;
- `/Campus-Plugins/PFERDE_ATELIER/**/CURRENT.zip`;
- alles mit Status AKTIV, BLOCKED oder UNGEKLÄRT.
