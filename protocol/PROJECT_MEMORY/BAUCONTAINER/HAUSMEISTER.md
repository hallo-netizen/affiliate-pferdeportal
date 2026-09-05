# CAMPUS-HAUSMEISTER

STAND: 2026-09-05
STATUS: WARTUNGSPROZESS

## Rolle

Der Hausmeister ist KEIN neuer Super-Agent, kein Fachbüro und kein Entscheider über fachliche Wahrheit.

Er ist ein wiederholbarer Wartungsprozess mit einem Ziel:

**Produktive Räume so schlank wie möglich halten, ohne Wissen zu verlieren.**

## Was er regelmäßig prüft

- erledigte Hobbyraumakten;
- alte Übergaben;
- abgelöste Zielverträge;
- historische Protokolle;
- alte Plugin-/Code-Stände;
- Dubletten;
- veraltete Verweise;
- aufgeblähte CURRENT_STATE-Dateien;
- Material, das eindeutig nur noch historisch ist;
- Archivkandidaten aus Masterdatei-Inventaren.

## Was er tun darf

1. HISTORISCH klar belegtes Material dem Archiv zuordnen;
2. Verweise auf den neuen Archivort aktualisieren;
3. Dubletten per Hash kennzeichnen;
4. produktive CURRENT_STATE-/START_HERE-Dateien auf aktuelle Wahrheit + notwendige Verweise reduzieren;
5. erledigte Hobbyräume nach vollständiger Übernahme wieder auf FREI setzen;
6. Aufräumvorgänge im `ARCHIV/HAUSMEISTER_PROTOKOLL.md` dokumentieren;
7. Architekturballast als BAU-Fehler melden.

## Was er NICHT tun darf

- AKTIV verschieben;
- UNGEKLÄRT verschieben;
- autoritative Fehlerquellen/Testquellen archivieren, solange sie aktiv referenziert werden;
- offene Zielverträge verschieben;
- Fachregeln ändern;
- technische Maschinenwege umbauen;
- Dateien löschen, nur weil sie alt aussehen;
- Branches/PRs schließen oder löschen ohne separate belegte Prüfung;
- Rohdateien mit Secrets in ein öffentliches Archiv kopieren.

## Vor jeder Verschiebung

Pflicht:
1. Status eindeutig HISTORISCH/ABGELÖST;
2. aktuelle Referenzen prüfen;
3. Hash/Identität festhalten;
4. Ziel im Archiv festlegen;
5. alle aktiven Verweise aktualisieren;
6. Hausmeister-Protokoll ergänzen.

Wenn eine Bedingung fehlt:
**NICHT VERSCHIEBEN → UNGEKLÄRT/ARCHIVKANDIDAT.**

## Regelmäßigkeit

KISS statt Dauer-Automatik:

### Kleiner Hausmeister-Check
bei Abschluss eines Hobbyraums oder einer größeren Masterdatei-Aufnahme:
- ist etwas eindeutig historisch geworden?
- kann CURRENT_STATE schlanker werden?
- sind alle Verweise aktuell?

### Großer Hausmeister-Check
periodisch oder vor einem neuen Tresor-/Backup-Gesamtstand:
- projektübergreifender Ballastcheck;
- Archivkandidaten;
- Dubletten;
- veraltete Verweise;
- offene Architekturballast-Fehler.

Eine feste Zeitautomatik ist optional und wird erst eingerichtet, wenn der gewünschte Rhythmus feststeht.

## Grundsatz

**Aufräumen = verschieben und verweisen, nicht Wissen vernichten.**
