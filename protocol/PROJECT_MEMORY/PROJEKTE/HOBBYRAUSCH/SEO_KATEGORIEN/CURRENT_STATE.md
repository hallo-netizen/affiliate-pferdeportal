# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: BUCHBINDEN RESEARCH COMPLETE / LIVE-ROOT-CAUSE BEWIESEN / V1.9.4 EXAKTER PRODUKTIONSPFAD POS+NEG HARD PASS / LIVE-RETEST NÄCHSTES

## Harte Abnahmeregel

**Keine Datei, kein Pluginstand und kein Produktionsschritt gilt als abnahmefähig ohne dokumentierte lokale Positiv- UND Negativsimulation.**

## Live-Root-Cause

V1.9.3 hat den realen Fehler feldgenau offengelegt:

`node:hdc-21557545f2e7cc51`
`Feld: name`

Knoten:
`Techniken & Praxis`

WordPress-Core speichert den Termnamen intern escaped:
`Techniken &amp; Praxis`.

Der bisherige Readback verglich diesen rohen DB-Wert gegen den Klartextnamen und produzierte dadurch einen falschen Mismatch.

## Exakte Altcode-Reproduktion

Mit dem echten Buchbinden-Kandidaten, 7 CREATE und WordPress-Core-Term-Escaping reproduziert V1.9.3 wortgleich:

`DEPLOY_READBACK_MISMATCH @ node:hdc-21557545f2e7cc51 | Felder: name | Automatischer Rollback: PASS`

## Fix V1.9.4

Installer SHA:
`85990b87f0ef35530b616df7716547cb20974d1c77ca21aa7b3e0edec723f249`

Taxonomie-Namen werden beim Readback ausschließlich von WordPress-Core-Escaping zurück in Klartext normalisiert.

Keine fachliche Strukturänderung.

## Positivsimulation

Echter Produktionspfad:
- 7 CREATE;
- Core-Escaping aktiv;
- `Techniken & Praxis` intern `Techniken &amp; Praxis`;
- Deploy + Readback PASS.

## Negativsimulation

Weiterhin korrekt BLOCKED:
- echter falscher Name;
- doppelt kodierter/falscher Name;
- falscher Slug;
- falscher Parent;
- falsche concept_id;
- falscher logical parent.

Rollback jeweils PASS.

Regression:
- Source 251/251 PASS;
- Fresh Installer 251/251 PASS;
- PHP Source 25/25 PASS;
- PHP Installer 17/17 PASS;
- Runtime-Parität 22/22 PASS.

## NEXT ACTION

V1.9.4 installieren.

Dann den bereits vorhandenen 7-CREATE-Dry-Run genau einmal über
`Geprüften Plan anwenden`
ausführen.

Kein neuer Research-Lauf.
Keine neue Datei.
Kein neuer Dry-Run.

Erwartung:
`Deployment abgeschlossen` und `Schreiben und Readback erfolgreich.`
