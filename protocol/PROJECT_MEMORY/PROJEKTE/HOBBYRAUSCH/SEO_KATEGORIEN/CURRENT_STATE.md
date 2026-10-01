# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-01
STATUS: BUCHBINDEN RESEARCH COMPLETE / LIVE-ROOT-CAUSE BEWIESEN / V1.9.4 EXAKTER PRODUKTIONSPFAD POS+NEG HARD PASS / LETZTER TESTLAUF VOLLSTÄNDIG ZURÜCKGEROLLT / LIVE-RETEST NÄCHSTES

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

## Aktueller Live-Zustand

Der Diagnose-Testlauf wurde vollständig zurückgerollt.

Sichtbarer WordPress-Stand:
- `Testlauf vollständig zurückgerollt.`
- `Rollback abgeschlossen. Der technische Testbestand ist zurückgesetzt.`

Deshalb:
- kein aktiver Deployment-Run;
- kein aktiver Dry-Run;
- kein direktes `Geprüften Plan anwenden` möglich.

## Produktionsdatei

Weiterhin derselbe fachlich geprüfte:
`HOBBY_DEPOT_BUCHBINDEN_READ_ONLY_PREVIEW_V1.json`

Kein neuer Research-Lauf erforderlich.

## NEXT ACTION

1. V1.9.4 installieren.
2. den bestehenden fachlich geprüften READ_ONLY_PREVIEW erneut über `Neue Datei übernehmen` laden.
3. `Finale Struktur freigeben`.
4. `WordPress-Vorschau erstellen`.
5. neuen Plan anwenden.

Erwartung:
`Deployment abgeschlossen` und `Schreiben und Readback erfolgreich.`

Bei Fehler:
keine Abnahme; exakte Fehlermeldung auswerten.
