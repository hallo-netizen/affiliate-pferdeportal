# Affiliate Router 6.72.185 – Version Separation + Stale-Edge Red/Green Full E2E

Datum: 2026-10-05
Branch: affiliate-672185-version-separation

## Anlass

Der korrigierte Banner-Migrationsstand darf nicht erneut als 6.72.184 ausgeliefert werden, weil auf dem realen WordPress bereits eine andere 6.72.184 installiert wurde und deren einmaliger Migrationsstatus bereits `done` sein kann.

## Änderung

- Pluginversion: 6.72.185.
- Eigene 6.72.185-Migrations-State-, Cursor-, Hook- und Result-Schlüssel.
- Dadurch kann ein alter `ppar_banner_library_migration_state_v672184=done` die neue Re-Evaluation nicht unterdrücken.
- Keine Änderung an Frontend-Ranking, Renderern oder Performance-Hotpaths.
- Der zuvor bewiesene stale-edge-Fix bleibt unverändert: während der einmaligen Banner-Migration werden nur abgeleitete automatische Zielkanten verworfen und anschließend aus der echten/decodierten Ziel-URL zentral neu gespeichert.

## Negativ-/Upgrade-Beweis

Ausgangsbasis ist ausdrücklich der fehlerhafte erste 6.72.184-Installer:
SHA-256 `bc101bd7dc06aa3ecbf085165914440e28e0b7aaefe6786d1e7db33fc7f8fe06`.

Source-Run: `37277975992` = SUCCESS.

Bewiesen:
- fehlerhafte 6.72.184 aktiv;
- alte automatische Legacy-Quelle bereits blockiert;
- falsche gespeicherte Library-Kante erzeugt und auf Schabracken sichtbar;
- alter 6.72.184-Migrationsstatus bereits `done`;
- Upgrade auf 6.72.185;
- 6.72.185 verwendet einen eigenen Migrationsstatus;
- alter 6.72.184-`done`-Status unterdrückt 6.72.185 nicht;
- falsche SanoVet-Kante verschwindet auf Schabracken;
- dieselbe Creative-Library-Zeile wird anhand der echten Ziel-URL auf Fütterung neu gespeichert;
- FIXED bleibt erhalten;
- eBay und Idealo unverändert;
- 0 Remoteaufrufe.

Upgrade-Gate: **23/23 PASS**.

## Finales ZIP

ZIP-Run: `37277994704` = SUCCESS.

Installer:
`release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.185.zip`

SHA-256:
`a0e4c28fa28d91455e288a45d6d932c49869ab0ad80353fd606fcce8e2a14f2a`

Bytes:
`793173`

Source-Manifest:
`1ae468e75c28d3e98f5e0ee2b28ce7371558f9108b91c58d2161fce9b1b9a1f7`

Weitere Gates:
- 23/23 Upgrade 6.72.184 -> 6.72.185 PASS;
- frischer kompletter Bannerpfad 21/21 PASS;
- Ziel-URL-Sammelstelle 26/26 PASS;
- ZIP/Source 27/27 byteidentisch;
- PHP lint 21/21 PASS;
- Performance-Hardlock PASS;
- keine neuen Frontend-DB-/HTTP-Aufrufe.

## Status

`release_allowed=false`

Offen ist nur der reale Produktionsnachweis:
6.72.185 auf dem echten WordPress über 6.72.184 installieren, Migration laufen lassen, zuerst Schabracken prüfen, danach repräsentativ Seite/Kategorie/Beitrag/Glossar/Rasse.
