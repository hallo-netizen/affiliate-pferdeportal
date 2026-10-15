# HOBBYRAUSCH – LIBRARY SOURCE GUARD

STAND: 2026-10-15
ROLLE: Verhindert versehentlichen Rückgriff auf alte Bildbestände.

## Geprüfter Library-Befund
Die Projekt-Library wurde nach den offenen Kategorien und passenden Dateinamen durchsucht.

Aktiv zulässig sind ausschließlich:
- die 7 neuen eigenständigen Quellen im aktuellen Arbeitsbestand;
- die 13 V2-Referenzcrops unter `/hobby rausch/_working/reference-crops-v2/` als **Richtungsreferenz**, niemals als Releasequelle.

Explizit gesperrt:
`/hobby rausch/WIP_1.50.653_WORKING/`

Dort liegen zwar noch alte Dateien mit passenden Kategorienamen, u. a.:
- `robotik-automation.png`;
- `leder.png`;
- `mechanik-uhren.png`;
- `essbare-pflanzen.png`;
- `ameisen-insekten.png`.

Diese Dateien stammen aus dem verworfenen WIP-1.50.653-Bestand und dürfen **nicht** als Ersatz, Fallback, Motivvorlage oder neue Quelle verwendet werden.

## Harte Auswahlregel
Eine namensgleiche Datei ist nicht automatisch aktuell.

Vor jeder Quellenübernahme muss gelten:
1. Pfad gehört zum neuen Nach-1.50.663-Arbeitsbestand oder zur verifizierten V2-Referenzbindung;
2. Datei ist nicht unter `WIP_1.50.653_WORKING`;
3. Current/Manifest führt sie ausdrücklich als aktive Quelle oder Referenz;
4. sonst gilt sie als **NICHT VERWENDEN**.

## Ergebnis
Der alte WIP-Bestand kann die 10 aktuell BLOCKED-Kategorien nicht scheinbar „füllen“. Fehlend bleibt fehlend, bis eine echte neue Bindung bzw. Einzelquelle existiert.


## Zusätzlich hart gesperrte Fehlgenerierungen 2026-10-15
Diese zwei fachfremden Bildgenerator-Ausgaben liegen weiterhin als Projektdateien vor, können über die verfügbare Dateiverwaltung aber nicht aus dem Project-Surface gelöscht werden. Sie sind deshalb explizit **QUARANTÄNE / NICHT VERWENDEN**:

- `file_00000000d654820aa38cee0e4660af0f` – WordPress-Plugin Release-Dashboard
- `file_00000000d49481f69adc2b2223a606a2` – WP-Bildersammler 1.50.664: Finale Fertigstellung

Sie dürfen niemals als Quelle, Referenz, Vorschau, Mapping oder Pluginbestand verwendet werden.
