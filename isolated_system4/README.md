# SYSTEM 4 — TRUE SINGLE ROOM

Status: **REALER CODEX-LAUF ERREICHT SYSTEM-4-ROOT / FAIL-CLOSED AN FEHLENDER LIVE-SNAPSHOT-MANIFESTBINDUNG / isolated prototype / test only.** Kein Merge, kein Publish.

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit**. Der offizielle Campus-/Projektstand in `control/startmaster0107/CURRENT_STATE.json` bleibt getrennt und unverändert.

## Verbindliches Ziel

`gebundene Metadaten -> System-4-Root-Einstieg -> Codex recherchiert -> Research Evidence -> Facts/Fact-Pack -> Context -> Draft -> unveränderte echte Prüfer -> gezielte Same-Article-Reparatur -> Batch-Gate -> V2-Handoff -> Parent-Chat-Rekonstruktion -> exakte WordPress-JSON`

Codex bleibt der eine fachliche Worker. System 4 übernimmt keine alte Legacy-Orchestrierung.

## Aktueller Root-Einstieg

Der frühere reale Ein-Artikel-Lauf stoppte mit:

`ROOT_ENTRY_BRANCH_NOT_SYSTEM4`

Dieser Branchnamensfehler wurde beseitigt. Die Root-Prüfung bindet jetzt **nicht mehr den symbolischen Branchnamen**, sondern den tatsächlich geladenen kritischen System-4-Inhalt über das Pflichtfeld:

`system4_root_manifest_sha256`

Aktueller gebundener Manifestwert:

`3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

Die Prüfung ist fail-closed: fehlende/abweichende Bindung, manipulierte kritische Dateien, fehlende getrackte Dateien, falscher Git-Root oder dirty kritische Dateien blockieren.

## Lokaler Testnachweis vor dem aktuellen Real-Lauf

Autoritativer Beleg für die Checkout-Identity-Korrektur:

`TESTNACHWEIS_20260913_CHECKOUT_IDENTITY_MANIFEST.md`

Unmittelbar vor dem aktuellen Codex-Lauf erneut ohne Codex ausgeführt:

- Gesamt-Unittests: **101/101 PASS**;
- kompletter Root-bis-Datei-Acceptance-Lauf: **10/10 PASS**;
- echter LanguageTool-6.8-Pfad;
- echter PPM-6.7.9-Pfad;
- Same-Article-Repair;
- Batch-Gate;
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- Inline-Pack / Inline-Unpack;
- bytegenaue WordPress-Datei;
- `mocks_used=false`;
- `codex_used=false` im Preflight;
- `merge_or_publish=false`.

Lokale Acceptance-Enddatei:

- 1 Artikel;
- Revision 2;
- 66753 Bytes;
- SHA256 `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`.

Echte Prüfer:

- LanguageTool 6.8 SHA256 `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`
- PPM 6.7.9 SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

## Aktueller realer Codex-Lauf — 1 Artikel

Gründliches Laufprotokoll:

`PROTOKOLL_REALRUN_20260913_ONE_ARTICLE_MANIFEST_BINDING_BLOCKER.md`

Getesteter Head bei Start und terminalem Abschluss:

`6e35f359e3bb654396e9791dffd5942c1c1ad176`

Gebundener Artikel:

- `Beratung`;
- Kategorie `putzbox-beratung`;
- Titel `Putzbox für Pferde richtig auswählen`;
- Keyword `Putzbox für Pferde`;
- Plan-Slot `88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5`;
- Batch `7b471ee2acef71531b067d2a8324a72580f4d9c8bc8d67412d021c1facf2e6e3`;
- exakt 1 Item;
- `publish_allowed=false`.

Codex-Auftrag:

`issuecomment-5652822158` — `2026-09-13T10:53:31Z`

Terminale Codex-Antwort:

`issuecomment-5652827317` — `2026-09-13T10:54:40Z`

Laufdauer zwischen Auftrag und terminaler Antwort:

**69 Sekunden**.

Tatsächlich ausgeführte erste System-4-Tür:

`python3 isolated_system4/root_entry.py start-stdin /tmp/system4-one-article-production`

Terminaler Befund:

`SYSTEM4_HARD_BLOCKER:ROOT_ENTRY_MANIFEST_BINDING_MISSING`

- stage=`SYSTEM4_ROOT_ENTRY`
- status=`SYSTEM4_ROOT_ENTRY_FAIL`
- error=`ROOT_ENTRY_MANIFEST_BINDING_MISSING`

## Konkrete Ursache des aktuellen Real-Blockers

Der von Chat für den realen Codex-Aufruf erzeugte gebundene JSON-Snapshot enthielt **nicht** das neue Pflichtfeld:

`system4_root_manifest_sha256`

Der erforderliche Wert wäre gewesen:

`3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

Das ist **kein unbekannter neuer Root-/Codex-Fehler**. Der vorhandene Negativtest `NEG_ROOT_MANIFEST_MISSING` prüft genau diesen Fall und erwartet genau diesen fail-closed Blocker.

Damit gilt für diesen Lauf:

- die neue Root-Prüfung hat sich wie spezifiziert verhalten;
- der frühere Branchnamensfehler trat nicht erneut auf;
- der Live-Auftrag war unvollständig konstruiert;
- Fehlerursache liegt beim aufrufenden Chat/Payload, nicht bei LT, PPM, Textmaschine, Batch-Gate, Handoff, WordPress oder Design.

## Nicht ausgeführte Produktionsstufen

Nach dem Root-Blocker wurden nicht gestartet:

- Recherche;
- Research Evidence;
- Facts;
- Fact-Pack/Context;
- Draft;
- LanguageTool im Codex-Lauf;
- PPM im Codex-Lauf;
- Repair;
- Batch-Gate;
- V2-Handoff;
- Inline-Relay;
- Parent-Chat-Rekonstruktion;
- WordPress-Datei.

Deshalb gibt es aus diesem Lauf ausdrücklich **keinen REAL-CODEX-PASS** und keinen Artikeloutput.

## Beweisgrenze

**Bewiesen:**

- Codex erreicht real die System-4-Root-Tür;
- der frühere symbolische Branchname ist nicht mehr der Blocker;
- die Manifest-Prüfung ist im echten Codex-Lauf aktiv;
- fehlende Manifestbindung wird real fail-closed blockiert;
- kein Legacy-Fallback wurde genommen;
- kein zweiter Lauf wurde gestartet.

**Nicht bewiesen:**

`Root PASS -> Research -> Facts -> Context -> Draft -> real LT/PPM -> Repair falls nötig -> Batch -> V2-Handoff -> WordPress-Datei`

Diese Strecke wurde im aktuellen Real-Lauf wegen des fehlenden Pflichtfelds nicht begonnen.

## Universelle Produktionsgrenze

- exakt die nichtleere gebundene Item-Menge;
- `1..N`, keine künstliche System-4-Obergrenze;
- `article_type` kommt aus Metadaten, keine System-4-Typ-Whitelist;
- `publish_allowed=false`;
- Signing/ENDSTEMPEL aus;
- kein Merge, kein Publish.

## Unverhandelbare Grenzen

- Textmaschine/content rules READ-ONLY;
- PPM 6.7.9 READ-ONLY;
- LanguageTool 6.8 unverändert;
- PSERC/PSTE-Fachregeln READ-ONLY;
- WordPress-Plugin, Theme/CSS, Designregeln READ-ONLY;
- Same-Article-Repair nur über Controller;
- `controller.py fullcheck` bleibt einziger Produktions-Prüforchestrator;
- keine Legacy-/STARTMASTER-/H7-/H8-/ACM-/System-3-Laufzeitabhängigkeit;
- finale geprüfte Artikelbytes werden nach dem Fullcheck nicht mehr transformiert.

## HOBBYRAUM / NEXT ACTION

Status: **BLOCKED — REALER LIVE-SNAPSHOT OHNE PFLICHT-MANIFESTBINDUNG.**

Kein weiterer Codex-Lauf ohne erneute ausdrückliche Nutzerfreigabe.

Vor einem möglichen weiteren Real-Lauf muss der vollständige gebundene Snapshot bereits **vor** Codex inklusive

`system4_root_manifest_sha256 = 3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

feststehen und exakt so per stdin an die System-4-Root-Tür übergeben werden.

Aus diesem Fehler folgt **kein Architekturumbau** und keine Änderung an Textmaschine, LT, PPM, Batch-Gate, Handoff, WordPress oder Design.

Kein Merge. Kein Publish.
