# ZIELVERTRAG — SYSTEM 4 / MASCHINEN-PUNKT-0 + GEBUNDENER WORKER-DISPATCH

Status: **VERBINDLICHER AKTUELLER ZIELVERTRAG DES ISOLIERTEN SYSTEM-4-PROTOTYPS**

Er ersetzt für System 4 den Zielvertrag `ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md` ausschließlich dort, wo sich der verbindliche Acceptance-/Handoff-Stand inzwischen konkretisiert hat. Die Produktionsarchitektur wird nicht neu erfunden.

STARTMASTER0107, Textmaschine, PPM 6.7.9, LanguageTool 6.8, Design, WordPress-Plugin und Theme bleiben unverändert/read-only.

## Verbindliche Zielkette

`Parent/Chat → Point-0 → Root → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → vollständige Textmaschine → Repair → Batch → Handoff → Datei`

Der Controller bestimmt den jeweils nächsten erlaubten Schritt. Kein Aufrufer, Worker oder Test darf frei wählen, überspringen, vorziehen oder einen späteren Zustand synthetisch herstellen.

## Einstieg

- Nur `start-point0` ist zulässiger vollständiger Acceptance-Einstieg.
- `root_entry start` und `start-stdin` sind für die vollständige Acceptance BLOCKED.
- Direkter Controller-/Worker-Einstieg ohne gültigen Point-0→Root→Supervisor→Worker-Dispatch ist BLOCKED.

## Produktionsworker und Acceptance-Testworker

Produktion und Acceptance benutzen **dieselbe gebundene Worker-Schnittstelle**, aber nicht denselben ausführenden Worker:

- Produktion darf Codex nur nach der separat geltenden Produktionsfreigabe als fachlichen Worker verwenden.
- Der Acceptance-Test verwendet ausschließlich den gebundenen deterministischen Testworker.
- Im Acceptance-Test darf `codex_entry.py` nicht aufgerufen und kein Codex-Modell gestartet werden.
- Der Testworker darf erst nach gültigem Point-0-, Root-, Supervisor- und Worker-Dispatch-Beleg arbeiten.

Damit entsteht **keine zweite Route**. Nur der Worker am bereits gebundenen Worker-Interface wird für den Test ersetzt; alle Maschinenstationen davor und danach bleiben identisch.

## Research → Facts → Context → Draft

- Quellenbeschaffung, Quellenintegrität, Snapshot, Root-/Head-/Manifest-Bindung, Supervisor-State und Worker-Dispatch gehören der Maschine.
- Der gebundene Worker darf ausschließlich den gebundenen Research-Pool verwenden.
- Facts müssen auf akzeptierte Source-/Evidence-Hashes zurückführen.
- Context und Authoring Contract müssen vor Draft gebunden sein.
- Kein Worker darf Quellen, Metadaten, Links, Kategorie, Slot oder Prüfer frei ersetzen.

## Frischer Artikel pro End-to-End-Lauf

Jeder vollständige Acceptance-E2E-Lauf muss einen während genau dieses Laufs neu erzeugten Artikel verwenden.

BLOCKED sind insbesondere:
- vorbereitete Artikeltexte;
- Recovery-/Fixture-/Frozen-Candidate-Bodies;
- bekannte historische Body-Hashes;
- Wiederverwendung desselben Bodys im selben Run;
- ein angeblich „frischer“ Artikel ohne aktuellen Run-/Research-/Facts-/Context-/Authoring-Contract-Beleg.

Frische ist eine maschinelle Eigenschaft des aktuellen Runs, keine Bezeichnung im Dateinamen.

## Vollständige Textmaschine

Unverändert verpflichtend sind die echten autoritativen Prüfer und Regeln, insbesondere LanguageTool 6.8 und PPM 6.7.9 sowie die bestehenden Textmaschinen-/SEO-/Link-/Metadaten-/Design-/WordPress-Grenzen.

Für die PPM-Detailabnahme gilt fail-closed:
- exakt das SHA-gebundene PPM-6.7.9-Paket ist Regel-/Testautorität;
- Registry und Coverage-Matrix müssen exakt übereinstimmen;
- aktuell: 557 registrierte Regeln / 557 Coverage-Zuordnungen;
- jede registrierte Regel muss ihren vorgesehenen positiven **und** negativen Originaltest binden und beide müssen tatsächlich PASS sein;
- `UNKNOWN`, `UNMAPPED`, `UNTESTED`, fehlender, übersprungener oder roter Originaltest = FAIL;
- jeder Originaltest läuft in einer frischen bytegleichen Paketkopie;
- erforderlicher Original-Runner-/Bootstrap-/Baseline-/Signatur-Kontext wird reproduziert, niemals die Regel oder der Test passend gemacht.

Ein Sammel-PASS oder die bloße Anzahl grüner Testdateien ersetzt diesen Einzelnachweis nicht.

## Repair / verpflichtende Rückgabe

Ein reparierbarer Befund ist kein terminaler Prozessfehler.

Jeder reparierbare Fehler muss:
1. zum autoritativen Owner zurückgegeben werden;
2. denselben gebundenen Artikel/dasselbe Work-Item behalten;
3. einen maschinell prüfbaren Continuation-Beleg tragen, mindestens Fehleridentität/-hash, Owner/Ziel, Reparaturzyklus, `terminal=false`, `continuation_required=true`;
4. nach der Reparatur wieder dem Controller übergeben werden, der den nächsten Schritt bestimmt.

Fehlender, stale, falscher oder manipulierter Rückgabe-Beleg = FAIL.

Terminal blockieren dürfen nur echte nicht reparierbare technische, Integritäts-, Sicherheits-, Identitäts-, Binding-/Hash- oder verbotene Publish-Fehler.

## Batch

System 4 verarbeitet exakt den gebundenen nichtleeren Input-Batch `1..N` ohne künstliche System-4-Obergrenze. Größen wie 1, 3, 7, 25 oder 1000 sind Regressionen, kein Produktionslimit.

`article_type` ist gebundene Eingabemetadaten und keine System-4-Whitelist.

## Handoff / Datei

Der aktuelle finale WordPress-Handoff-Vertrag lautet:

`SYSTEM4_WORDPRESS_HANDOFF_V1`

Der finale Dateiname lautet:

`SYSTEM4_WORDPRESS_HANDOFF_V1.json`

`SYSTEM4_PARENT_CHAT_INLINE_V2` darf ausschließlich als Transport-/Relay-Vertrag für Inline-Pack/Unpack verwendet werden; er ist **nicht** der finale WordPress-Dateivertrag.

Die exakten geprüften Bytes müssen nach Rekonstruktion unverändert bleiben. `publish_allowed=false` ist verpflichtend.

GitHub-Artefakt, Repository-Datei, interner Temp-Pfad oder Hash allein erfüllen die terminale Übergabe nicht.

## Terminaler Gesamt-PASS

Gesamt-PASS ist erst erlaubt, wenn im selben vollständigen Acceptance-Lauf tatsächlich erfolgreich durchlaufen wurden:

`Parent/Chat → Point-0 → Root → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → vollständige Textmaschine → erforderliche Same-Article-Repairs → Batch → Handoff → exakte Datei im Parent-Chat`

und dabei:
- ein neuer Artikel dieses Runs verwendet wurde;
- kein Codex im Acceptance-Test lief;
- alle verpflichtenden positiven und negativen Prüfungen bestanden wurden;
- kein Pflichtprüfer/Originaltest übersprungen wurde;
- die exakte `SYSTEM4_WORDPRESS_HANDOFF_V1.json` tatsächlich im Parent-Chat verfügbar ist.

Ein interner oder GitHub-seitiger PASS ohne diese letzte Dateiübergabe ist kein terminaler Gesamt-PASS.

## Nicht erlaubt

- neue Architektur oder Alternativroute;
- Ersatzprüfer für autoritative Prüfer;
- Lockerung/Änderung der Textmaschine im Rahmen System 4;
- vorbereiteter E2E-Artikel;
- Codex im Acceptance-Test;
- terminaler BLOCK nur deshalb, weil ein reparierbarer Fehler erkannt wurde;
- automatisches Publish;
- PASS aus Codeansicht, Erinnerung oder unvollständigem Teiltest.
