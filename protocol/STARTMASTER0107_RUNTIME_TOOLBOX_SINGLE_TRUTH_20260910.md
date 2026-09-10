# STARTMASTER0107 – Runtime Toolbox Single Truth

Stand: 2026-09-10

## Zweck

Dauerhafte WAS/WARUM-/Test-Dokumentation des Runtime-Ursachenfixes. Dieses Dokument ist Protokoll und Entscheidungsnachweis, **keine CURRENT_STATE-Quelle** und **kein zweiter Zielvertrag**.

## Ausgangsfehler

Realer Produktionsblocker: `LANGUAGETOOL_6_8_BESTAND_43_EXECUTOR_OR_DEPENDENCY_NOT_AVAILABLE`.

Im weiteren Ursachenlauf traten Codex-Host-Abbrüche auf, wenn die Vorstartphase unnötig schwere bzw. doppelte Runtime-Arbeit ausführte. Das Problem war damit nicht nur LanguageTool selbst, sondern die fehlende einheitliche technische Werkzeugbereitstellung vor der netzlosen Agentphase.

## Dauerhafte Entscheidung – WAS

Es gibt eine einzige technische Werkzeugwahrheit:

`control/startmaster0107/codex-production-runtime/RUNTIME_TOOLBOX_MANIFEST.json`

Sie enthält ausschließlich technische Runtime-Identitäten für Java, PHP, Cryptography/Ed25519, LanguageTool sowie die repositorygebundenen PPM-/PSERC-Pakete.

Setup und bestehender `codex_environment_preflight.py` lesen dieselbe Manifest-Wahrheit.

LanguageTool wird persistent gecacht. Fehlender/falscher Cache darf ausschließlich manifestgebunden wiederhergestellt werden. Das fertig entpackte Runtime-Artefakt wird hashgebunden wiederverwendet, statt bei jedem Start den kompletten Bestand unnötig neu aufzubauen.

Java und PHP werden nicht kopiert, sondern gegen die manifestgebundene Version/Feature-Linie real ausgeführt und geprüft.

PPM/PSERC bleiben im Repository; keine zweite Kopie wird zur Autorität.

Cryptography/Ed25519 bleibt exakt versions-/symbolgebunden.

## Dauerhafte Entscheidung – WARUM

KISS: Ein Werkzeugkasten, eine Wahrheit, eine technische Prüfung vor Artikel 1.

Verhindert:
- Tool-/Versionsdrift zwischen Setup und Preflight;
- Werkzeugwahl durch Worker oder Chat;
- Fallback auf andere Versionen;
- Download/Installation mitten in der Agentphase;
- doppelte schwere Vorstartprüfungen;
- zweite Schattenkopie der Fach-/Projektlogik.

## Zwangsjacke / Autoritätsgrenzen

Unverändert verbindlich:
- Chat-Ausführungsautorität: NONE;
- Chat-Werkzeugwahl: NONE;
- Worker-Werkzeugwahl: NONE;
- Workflow-Navigation durch Worker/Chat: NONE;
- Reparaturwahl durch Worker/Chat: NONE;
- Content-/Semantik-/Qualitäts-/Design-/SEO-Autorität der Runtime-Schicht: NONE;
- Publish: false;
- Agentphase: netzlos, keine Tool-Installation, kein Tool-Update, keine Tool-Auswahl.

Der technische Wächter bewertet keine Inhalte. Er prüft nur feste Identitäten/Hashes/Versionen und reale technische Ausführbarkeit und liefert PASS/BLOCKED.

## Nicht verändert

Nicht verändert wurden Fachregeln, Textmaschine, PPM-/PSERC-/PSTE-Fachlogik, Artikelthemen, Titel-/Keywordregeln, SEO, Design, Handoff-Semantik, Endstempel-/Publish-Sicherheit oder WordPress-Schnittstellen.

Der Zielvertrag `control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json` bleibt unverändert.

Die einzige produktive Standwahrheit bleibt `control/startmaster0107/CURRENT_STATE.json`. Dieses Protokoll darf niemals als CURRENT verwendet werden.

## Aktiver Hobbyraum

Branch: `hobbyroom/runtime-toolbox-single-truth-20260910`

PR: #214 `Hobbyraum: eine Werkzeugwahrheit vor Codex`

Vor der Dokumentationsnachholung geprüfter Head: `84c5aa7361cee2e1a75715ef3100173b3b7a7707`.

Nachweise auf diesem Head:
- `hardlock` PASS;
- `hardlock-base` PASS;
- Codex Cloud Entrance PASS;
- vollständiger vorhandener `HOBBYRAUM_M01_M33_REGRESSION.py` => `M01_M36_FULL_PASS`, inklusive `LAST_REGRESSION PASS` und `GESAMT PASS`;
- kein Publish.

## Nachholprüfung 2026-09-10

Fehlermatrix M10 wurde erweitert, sodass die reale Werkzeug-/Vorstart-Ursachenklasse dauerhaft Teil derselben bestehenden M01–M36-Matrix bleibt. Kein M37-/Parallelrunner wurde erzeugt.

Dieses Protokoll dokumentiert die im Chat erfolgten Runtime-Entscheidungen und Tests nachträglich dauerhaft.

Da diese Dokumentationsänderungen den Branch-Head verändern, gilt der frühere PASS **nicht automatisch** für den neuen Head. Vor Merge muss auf dem dann aktuellen Head erneut gelten:

1. `hardlock` PASS;
2. `hardlock-base` PASS;
3. `python3 control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py` => M01–M36 FULL PASS;
4. letzter Regressionstest PASS.

## NEXT ACTION

Auf dem aktuellen PR-#214-Head ausschließlich dieselben bestehenden Tests erneut ausführen. Keine Reparatur während des Testlaufs.

Nur bei Gesamt-PASS darf PR #214 Merge-Kandidat werden. Danach: kompletter frischer 7/7-E2E auf current `main`, Stop beim ersten echten Blocker, kein Auto-Publish.

## Architekturfolge

Die erkannte allgemeine Regel lautet:

**Feste externe Runtime-Werkzeuge werden über genau eine technische Manifest-Wahrheit bereitgestellt und vor der Agentphase fail-closed geprüft. Projekt-/Fachlogik wird nicht in die Runtime-Grundumgebung dupliziert.**

Diese Regel ist als allgemeines Neubauprinzip geeignet. Eine repositoryweite Neubauvorlage/Globalstandard-Datei wurde in diesem Chat jedoch noch nicht geändert; das ist eine offene Campus-Architekturfolge und darf nicht fälschlich als erledigt gelten.
