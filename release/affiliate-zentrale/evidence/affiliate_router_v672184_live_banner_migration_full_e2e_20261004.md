# Affiliate Router 6.72.184 – Banner-Library-Migration – Live-Fail Red/Green Full E2E

Datum: 2026-10-04
Workstream: AFFILIATE_ZENTRALE
Version: 6.72.184
Branch: affiliate-release-current
Release: NICHT freigegeben; realer WordPress-Readback des korrigierten Installers offen.

## Ziel

Eine einzige automatische Bannerwahrheit über die Creative-Library:
echte/decodierte Ziel-URL einmal auswerten -> Zielkante zentral speichern -> Frontend nur aus gespeicherter Zuordnung verteilen.
Reihenfolge: exakt -> weiterer Themenkreis -> allgemein -> irgendein technisch gültiger aktiver Banner.
Manuelle FIXED-Zuweisungen bleiben separat vorrangig.
Keine Provider-Sonderlogik, keine zweite Frontend-Analyse, keine neuen Frontend-DB-/HTTP-Aufrufe.

## Reale Live-Negativevidence

Der erste 6.72.184-Liveversuch zeigte auf der echten Schabracken-Seite weiterhin den SanoVet-Fütterungsbanner.
Damit war der frühere 6.72.184-Installer mit SHA
`bc101bd7dc06aa3ecbf085165914440e28e0b7aaefe6786d1e7db33fc7f8fe06`
NICHT abnahmefähig und ist superseded.

## Fehlender Gegenfall der alten Simulation

Der alte Test belegte:
- Legacy-Automatik außerhalb der Creative-Library wird gesperrt.
- Ein noch nicht materialisierter korrekter Library-Banner wird migriert.

Er belegte jedoch nicht:
- echte Ziel-URL = Fütterung,
- gleichzeitig bereits gespeicherte falsche Creative-Library-Kante = Schabracken,
- anschließend Upgrade/Migration.

Genau dieser fehlende Zustand wurde nach dem Live-Fail ergänzt.

## Root Cause

`output_banner_destination_classification()` verwendet eine vorhandene gespeicherte Library-Kante als autoritative Eingabe.
Der Banner-only-Migrationsworker von 6.72.184 rief denselben Planner auf, ohne die alte automatische Kante für die ausdrücklich angeordnete Re-Evaluation vorher zu verwerfen.

Folge:
Eine alte falsche Kante konnte sich bei der Migration selbst bestätigen, obwohl die in derselben Library-Zeile gespeicherte echte Ziel-URL auf ein anderes Thema zeigte.

## Roter Beweis vor Fix

Source Upgrade Run: `37227361318`
ZIP Upgrade Run: `37227361328`

WordPress 7.1.2 + MariaDB.

Fixture:
- Creative: SanoVet/Fütterung.
- echte Ziel-URL: `https://example.com/fuetterung-upgrade-e2e/`
- absichtlich alter gespeicherter Target: `Ausrüstung Upgrade E2E > Schabracken Upgrade E2E`.

Ergebnis:
- falscher gespeicherter Zustand vor Migration reproduziert: PASS.
- Migration läuft: PASS.
- Performance-Hardlock: PASS.
- entscheidende Assertion `POST_UPGRADE_stale_edge_recomputed_from_real_destination`: FAIL.
- gespeicherter Target blieb Schabracken.

Damit ist der reale Fehler als fehlender Gegenfall reproduziert.

## KISS-Fix

Nur im bestehenden einmaligen Banner-only-Migrationsworker:
- für den gerade bearbeiteten aktiven Banner werden die abgeleiteten automatischen Felder `topic_targets`, `topic_score` und `classified_at` zurückgesetzt;
- danach läuft unverändert der bestehende zentrale Planner;
- der bestehende Ziel-URL-Klassifizierer wertet die echte/decodierte Ziel-URL neu aus;
- die neue Kante wird wieder zentral in der Creative-Library gespeichert.

Nicht geändert:
- Frontend-Ranking,
- Renderer,
- Request-Caches,
- Performance-Hotpaths,
- eBay,
- Idealo,
- Produktpfade,
- Providerarchitektur,
- manuelle FIXED-/Control-Entscheidungen.

## Grüner Beweis nach Fix

Source Upgrade Run: `37227561289`
Ergebnis: SUCCESS.

Exakt derselbe vorher rote Gegenfall:
- `PRE_MIGRATION_stale_library_edge_reproduces_live_failure`: PASS.
- `POST_UPGRADE_stale_library_sanovet_absent`: PASS.
- `POST_UPGRADE_stale_edge_recomputed_from_real_destination`: PASS.
- gespeicherte neue Kante: `Fütterung Upgrade E2E`.
- Quelle der neuen Kante: `banner_destination_url`.
- Ziel-URL bleibt `https://example.com/fuetterung-upgrade-e2e/`.
- Upgrade-Gate: 20/20 PASS.
- manuelle FIXED-Ausnahme: PASS.
- eBay-Produktkampagne unverändert: PASS.
- Idealo-Produktkampagne unverändert: PASS.
- Remoteaufrufe: 0.
- Performance-KISS-Hardlock: PASS.

## Finales getestetes ZIP

ZIP Full E2E Run: `37227561276`
Ergebnis: SUCCESS.

Artifact:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.184.zip`

SHA-256:
`46bcc02b2284fbbb0830b9f254d178f15ad0be072cbb3b40ee7fd658d4e1e437`

Bytes:
`793009`

Git blob:
`4cc3f5fc9b3444320fbb943b633612a7cb2ade9b`

Source-Manifest:
`63218434f3d853fd3a9035cd600caae8a7ba36be5525a9096b4a7dcc9a41ea5d`
27 Dateien.

ZIP-Nachweise:
- Upgrade mit exakt dem vorher roten stale-edge-Gegenfall: 20/20 PASS.
- frischer kompletter Library-Bannerpfad: 21/21 PASS.
- frische Ziel-URL-Sammelstelle: 26/26 PASS.
- ZIP Source-Byteidentität: 27/27 PASS.
- PHP lint: 21/21 PASS.
- Performance-KISS-Hardlock: PASS.
- keine neuen Frontend-DB-/HTTP-Aufrufe.
- keine Frontend-URL-Neuklassifikation.
- eBay/Idealo unverändert.

## Status

Lokaler/CI-Nachweis inklusive NEGATIV -> FIX -> POSITIV ist vollständig.

`release_allowed=false`

Offen ist ausschließlich der reale Produktionsnachweis des korrigierten Installers:
exakt diesen neuen 6.72.184-Installer auf dem echten WordPress installieren, Banner-only-Migration laufen lassen und zuerst Schabracken readback-prüfen. Danach repräsentativ Seite, Kategorie, Beitrag, Glossar und Rasse.

Kein weiterer Umbau vor einem real belegten Fehler dieses korrigierten Installers.
