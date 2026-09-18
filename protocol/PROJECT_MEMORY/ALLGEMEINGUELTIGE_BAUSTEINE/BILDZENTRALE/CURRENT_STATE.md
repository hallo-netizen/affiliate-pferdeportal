# BILDZENTRALE – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

> **Einzige aktuelle Zustandsautorität dieses Scopes.** Status, erster offener Blocker und NEXT ACTION werden nur hier gepflegt. Eine Hobbyraumdatei ist nur Ausführungsfläche.


STAND: 2026-09-16
STATUS: **2.7.6 LOCAL HARD PASS / PFERDE-ANWENDUNG LIVE-FUNKTION PASS**

## Aktueller technischer Stand

Plugin:
`ALLGEMEINE_BILDZENTRALE_2.7.6_RASSEN_BATCH_AUTOMATIK_INSTALLIEREN.zip`

Version:
**2.7.6**

SHA-256:
`12edc4405560ac3b149cf76a0b6e65694337b1533c0ea5e3a777d3b6c98ccbf0`

Persistente allgemeine Ausgabekopie:
`/Campus-Plugins/ALLGEMEINGUELTIGE_BAUSTEINE/BILDZENTRALE/CURRENT.zip`

Pferde-Ausgabekopie:
`/Campus-Plugins/PFERDE_ATELIER/PPA-003/CURRENT.zip`

## Entwicklung seit 2.7.1

- 2.7.2: Rassen-Hero-Profil/Migration weitergeführt.
- 2.7.3: real blockierenden Magnific-GET-Preflight entfernt; gebundener POST-Weg bleibt maßgeblich.
- 2.7.4: Framing für vollständigere Pferdemotive angepasst.
- 2.7.5: `post_type_hero` für diesen Weg nativ 21:9 / 1260×540; kein nachgelagerter 3:1-Recrop.
- 2.7.6: optionaler serieller `pa_breed`-Batchhelfer für die nächsten 10 offenen Rassen, ohne Überschreiben bestehender Featured Images.

## Harte Prüfung

Aktueller 2.7.6-Stand:
- PHP-Lint: PASS;
- ZIP/Re-Extract/Version: PASS;
- `pa_breed`-Batchscope: PASS;
- serielle Verarbeitung: PASS;
- No-Overwrite: PASS;
- bestehende übrige Profile/Wege geschützt: PASS;
- relevante Positiv-/Negativ-/Regressionstests laut Testreport: PASS.

## Live-Grenze

Pferde-Atelier-LIVE:
- Batchfunktion vom Nutzer am 2026-09-16 mit `klappt` bestätigt;
- sichtbarer 10er-Batch lief seriell ohne angezeigten Fehler.

Dies ist ein Funktions-PASS des Batchwegs, **kein** Beleg einer vollständigen Bebilderung des gesamten Bestands.

Projektbezogene LIVE-Wahrheit bleibt ausschließlich in:
`../../../PROJEKTE/PFERDE_ATELIER/BILD/CURRENT_STATE.md`

## Architekturgrenze

Der allgemeine Bildkern bleibt wiederverwendbar. Der `pa_breed`-Batchhelfer ist eine optionale Pferde-Anwendungsfunktion; daraus wird keine allgemeine Pflicht für andere Projekte abgeleitet.

## Wasserzeichen

Nicht Bestandteil dieses Releasezugs; separater Pferde-BILD-Backlog.

## NEXT ACTION

**NONE – kein offener allgemeiner Bildzentrale-Reparaturauftrag gebunden.**

Projektbezogene weitere Rassenbebilderung wird ausschließlich in der Pferde-Atelier-BILD-Current-Autorität gesteuert. Eine neue allgemeine Kernänderung benötigt einen eigenen ausdrücklichen Auftrag.
