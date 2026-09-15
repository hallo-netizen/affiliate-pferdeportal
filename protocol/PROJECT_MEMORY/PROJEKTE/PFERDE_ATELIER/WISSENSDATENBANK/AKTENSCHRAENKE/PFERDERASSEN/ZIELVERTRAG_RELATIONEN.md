# ZIELVERTRAG – PFERDERASSEN-RELATIONEN

ID: ZV-PFERDERASSEN-REL-001
STAND: 2026-09-15
STATUS: AKTIV
FASSUNG: 1.0

## Ziel

Die beiden Frontendmodule `Zur gleichen Rassengruppe` und `Ähnliche Rassen` müssen fachlich und technisch unterschiedliche Bedeutungen haben.

## Verbindliche Semantik

`Zur gleichen Rassengruppe`
- Quelle ausschließlich `pa_breed_group`;
- zeigt andere veröffentlichte Pferderassen derselben taxonomischen Rassengruppe.

`Ähnliche Rassen`
- Quelle ausschließlich strukturierte Relations-IDs `_prm_related_source_ids`;
- Ziel muss eine veröffentlichte `pa_breed` mit stabiler `_prm_source_id` sein;
- Selbstreferenz verboten;
- maximal 3 eindeutige Ziel-IDs;
- keine zufällige Auffüllung ohne belegbares Ähnlichkeitssignal;
- **jede Zielrasse aus derselben `pa_breed_group` ist hart ausgeschlossen**;
- damit darf zwischen beiden Kartenblöcken keine gemeinsame Rassenidentität auftreten.

## Betriebsgrenze

Relations-Neuberechnung ist eine explizite Backend-Aktion. Sie darf niemals automatisch auf Frontend-`init`, Plugin-Aktivierung oder über einen `get_post_metadata`-Filter laufen.

Doppelte `_prm_source_id` im WordPress-Bestand dürfen nicht still kollabiert werden. Jeder reale Post muss im Reparaturlauf erhalten bleiben; Doppel-IDs müssen sichtbar gewarnt und separat bereinigt werden.

## PASS-Bedingung

1. lokale Positivprüfung des realen Pluginpakets;
2. lokale Negativ-/Mutationstests für Same-Group, Self, unbekannte IDs, Frontend-Backfill und Duplicate-Collapse;
3. WordPress-Einzelseite lädt nach Installation normal;
4. manueller Backend-Neuaufbau beendet sich;
5. Aegidienberger: keine Überschneidung zwischen beiden Blöcken;
6. mindestens eine weitere Einzelrasse als Gegenprobe;
7. erst danach LIVE-PASS.

## Hauptquellen

- Fachfehler: `FEHLERQUELLEN.md`
- Manager-Testbeleg: `TESTREPORT_PFERDERASSEN_MANAGER_0.2.7.md`
- Design-Schnittstelle: `_prm_related_source_ids` → `_prm_source_id` im Pferderassen-Einzelrassen-Design.
