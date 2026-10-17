# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.14.12 REALER WORDPRESS-DRY-RUN BLOCKED / URSACHE ISOLIERT / 1.14.13 LOCAL HARD PASS / ECHTER V7.1-WORDPRESS-DRY-RUN OFFEN**

## Reales Ergebnis 1.14.12

Der Nutzer hat HD-001 1.14.12 installiert und den Finalen Delta-Dry-Run ausgeführt.

Ergebnis:
- BLOCKED;
- 2642 Zielobjekte;
- CREATE 279;
- ADOPT 4;
- UPDATE 2357;
- UNCHANGED 0;
- ARCHIVE 0;
- kein Apply/Sync.

Blockierende Altbindungen:
- Libellenbeobachtung;
- Nachtvogel-Beobachtung.

Die 2642 Zielobjekte gehören nicht zum eingebetteten V7.1-Zielstand mit 3487 Zielobjekten. Damit ist belegt, dass beim Final-Dry-Run noch ein alter externer Zielprofilpfad wirksam war.

## Ursache

1.14.12 enthielt zwar bytekorrekt das V7.1-Profil, aber der Final-Dry-Run durfte weiterhin einen extern gesetzten Profilpfad vor dem eingebetteten Profil verwenden.

Zusätzlich erkannte der Migrationspfad frühere `_apkw_target_node_id`-Bindungen der neu stabilisierten Proposal-Hobbyseiten nicht als zulässige Legacy-Bindung.

Dadurch wurden zwei vorhandene Hobbyseiten fälschlich als Fremdkollision behandelt.

## Einziger Kandidat

`HD001_V1.14.13_HOBBY_DEPOT_V7_1_LIVE_COLLISION_FIX_LOCALPASS.zip`

SHA-256:
`c543ac655f12d4fcb0d5cb581b3f8a3410103988655a87bb62bab9cbd9995fa3`

Eingebettetes V7.1-Profil:
SHA-256:
`23c707b38f1892703f959c5374b736c7b85fa4db56023a22e987debdc215911f`

## Fachstand

V7.1 bleibt unverändert:
- 3517 logische Knoten;
- 3487 physische Ziele;
- 862 Entities;
- 383 CORE Entities;
- 381 terminale Hobby-Hubs;
- 2995 Content-Kategorien.

Keine Fachkategorie und keine Strukturentscheidung wurde durch 1.14.13 verändert.

## Korrektur 1.14.13

- Finaler Hobby-Depot-Dry-Run bindet für diesen Weg hart das eingebettete V7.1-Profil;
- alter externer Profilpfad kann diesen Final-Dry-Run nicht mehr auf den 2642er Stand zurücksetzen;
- 51 Proposal-Hobbyseiten besitzen ihre frühere Target-Identität zusätzlich als Migrationsbindung;
- Dry-Run erkennt frühere Target-Bindungen und verwendet die vorhandene Seite weiter;
- derselbe Wiederverwendungsweg ist auch für einen später ausdrücklich bestätigten Sync vorhanden;
- fremde Slug-Bindungen blockieren weiterhin;
- doppelte Legacy-Bindungen blockieren weiterhin;
- manual-only bleibt unverändert;
- Dry-Run und Apply bleiben getrennt.

## Lokale Safety-QA

PASS:
- PHP 33/33;
- ZIP-Roundtrip PASS;
- V7.1-Zahlen unverändert;
- externer Altprofil-Override simuliert und abgewehrt;
- Libellenbeobachtung Altbindung → vorhandene Seite wiederverwendet;
- Nachtvogel-Beobachtung Altbindung → vorhandene Seite wiederverwendet;
- alle 51 Proposal-Migrationen zusammen → PASS;
- echte Fremdkollision → BLOCKED;
- doppelte Legacy-Bindung → BLOCKED;
- Provider Calls 0;
- WordPress Structure Writes 0;
- Dry-Run ruft keinen Apply auf.

## Isoliertes Artefakt

Pfad:
`../../ISOLIERTE_PLUGINS/HD-001-KATEGORIE-WORKFLOW/`

`CURRENT.zip` bleibt **noch nicht synchronisiert**.

Grund:
Der echte WordPress-Dry-Run mit 1.14.13 ist noch offen. Bis dahin ist 1.14.13 ein lokal vollständig geprüfter Reparaturkandidat, kein Live-/Release-PASS.

## EXAKT EINE NEXT ACTION

**1.14.13 über die aktuell installierte 1.14.12 installieren. Danach nur den Finalen Delta-Dry-Run starten; keinen Apply/Sync bestätigen.**

Direkte Abnahme:
- Zielobjekte = 3487;
- keine Kollision für Libellenbeobachtung;
- keine Kollision für Nachtvogel-Beobachtung;
- anschließend vollständiges reales Dry-Run-Ergebnis prüfen.
