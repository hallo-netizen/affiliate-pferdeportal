# SYSTEM 4 — REALER 1-ARTIKEL-CODEX-LAUF — MANIFEST-BINDING-BLOCKER — 2026-09-13

Status dieses Dokuments: **Beleg-/Fehlerprotokoll, keine zweite CURRENT_STATE.** Aktuelle System-4-Statuswahrheit bleibt `isolated_system4/README.md`.

## Nutzerfreigabe

Der Nutzer gab ausdrücklich genau **einen realen Codex-Testlauf mit einem Artikel** frei und verlangte eine gründliche Protokollierung.

Verbindliche Grenzen:

- exakt 1 Artikel;
- kein automatischer zweiter Codex-Versuch;
- kein Merge;
- kein Publish;
- keine Repository-Ausgabe als Artikel-Handoff;
- kein Signing / ENDSTEMPEL;
- keine Änderungen an Textmaschine, PPM, WordPress oder Design.

## PR-/Code-Ausgangsstand

PR: `#238` — `System 4 — true single-room article production`

Head bei Start und bei terminalem Abschluss:

`6e35f359e3bb654396e9791dffd5942c1c1ad176`

Der Head blieb während des Codex-Laufs unverändert.

Aktuelle Root-Identitätslösung:

- kein symbolischer Branchname mehr als Identitätsbedingung;
- stattdessen `system4_root_manifest_sha256`;
- aktueller gebundener Manifestwert:

`3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

## Erneuter Preflight unmittelbar vor Codex

Ohne Codex erneut ausgeführt auf den bytegleichen aktuellen System-4-Ausführungsdateien:

### Unittests

`python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v`

Ergebnis:

- `Ran 101 tests in 28.595s`
- `OK`
- **101/101 PASS**

### Kompletter Root→Datei-Acceptance-Lauf

`python3 isolated_system4/full_local_acceptance.py`

Ergebnis:

- Contract: `SYSTEM4_FULL_LOCAL_ROOT_TO_FILE_ACCEPTANCE_V2`
- Status: `PASS`
- Testanzahl: **10/10 PASS**
- `POS_ROOT_STDIN_TO_FILE`: PASS
- `NEG_ROOT_BAD_STDIN`: PASS
- `NEG_ROOT_MANIFEST_MISSING`: PASS
- `NEG_ROOT_MANIFEST_MISMATCH`: PASS
- `NEG_PUBLISH_AUTHORITY`: PASS
- `NEG_FAKE_FACT`: PASS
- `NEG_DESIGN_DRIFT`: PASS
- `NEG_HANDOFF_TAMPER`: PASS
- `NEG_BATCH_STATE_TAMPER`: PASS
- `NEG_NO_LEGACY_RUNTIME`: PASS
- `mocks_used=false`
- `codex_used=false`
- `merge_or_publish=false`

Echte Prüfer:

- LanguageTool 6.8 SHA256: `2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8`
- PPM 6.7.9 SHA256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`

Lokale Acceptance-Enddatei:

- 1 Artikel
- Revision 2
- 66753 Bytes
- SHA256 `4f3c3585d1b42f3ca53f1f65bb4bca728a6426527c7eec75c45e2622dd7220ae`

Wichtig für den späteren Real-Blocker: Die positiven Root-Tests und der positive Acceptance-Lauf erzeugen den Snapshot mit dem Pflichtfeld `system4_root_manifest_sha256`. Der Negativtest `NEG_ROOT_MANIFEST_MISSING` entfernt genau dieses Feld und erwartet fail-closed `ROOT_ENTRY_MANIFEST_BINDING_MISSING`.

## Gebundener Real-Testartikel

- `article_type`: `Beratung`
- `category`: `putzbox-beratung`
- `plan_slot`: `88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5`
- `target_keyword`: `Putzbox für Pferde`
- Titel: `Putzbox für Pferde richtig auswählen`
- `batch_sha256`: `7b471ee2acef71531b067d2a8324a72580f4d9c8bc8d67412d021c1facf2e6e3`
- Snapshot-Contract: `SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1`
- Metadata-Batch-Contract: `PSERC_TEXTMACHINE_METADATA_BATCH_V2`
- `item_count=1`
- `publish_allowed=false`

## Codex-Auftrag

GitHub-Task-Kommentar:

`issuecomment-5652822158`

Erstellt:

`2026-09-13T10:53:31Z`

Der Auftrag verlangte ausdrücklich:

1. ersten ausführbaren System-4-Befehl über `root_entry.py start-stdin`;
2. Fresh Research;
3. Facts/Fact-Pack/Context;
4. neuen Artikel;
5. einzigen Prüforchestrator `controller.py fullcheck`;
6. Same-Article-Repair bei `REPAIR_REQUIRED`;
7. FULL PASS bis `OUTPUT_GATE_REQUIRED`;
8. Batch-Gate;
9. V2-Handoff;
10. vollständiges V2-Inline-Relay.

Keine Wiederholung bei Fehler.

## Fehler im von mir erzeugten Live-Auftrag

Der im Codex-Auftrag übergebene JSON-Snapshot enthielt **nicht** das seit der Checkout-Identity-Reparatur zwingende Top-Level-Feld:

`system4_root_manifest_sha256`

Erforderlicher Wert für diesen Stand:

`3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

Der tatsächlich übergebene Live-Snapshot begann nur mit:

- `contract`
- `next_textmachine_metadata_batch`

Das Pflichtfeld fehlte.

Das war ein Fehler in der Live-Auftragskonstruktion durch den aufrufenden Chat. Es war **kein** unbekannter Codex-Checkout-Effekt und **kein** Versagen der neuen Root-Prüfung.

## Reale Codex-Ausführung

Codex nahm genau diesen einen Auftrag an.

Terminale Codex-Antwort:

`issuecomment-5652827317`

Erstellt:

`2026-09-13T10:54:40Z`

Zeit zwischen Auftragskommentar und terminaler Antwort:

**69 Sekunden**.

Tatsächlich ausgeführte System-4-Tür:

`python3 isolated_system4/root_entry.py start-stdin /tmp/system4-one-article-production`

Terminaler Befund:

`SYSTEM4_HARD_BLOCKER:ROOT_ENTRY_MANIFEST_BINDING_MISSING`

Codex meldete:

- stage=`SYSTEM4_ROOT_ENTRY`
- status=`SYSTEM4_ROOT_ENTRY_FAIL`
- error=`ROOT_ENTRY_MANIFEST_BINDING_MISSING`

## Abgleich mit dem realen Code

`root_entry.py` verlangt in `_verify_snapshot_binding(...)`:

- Top-Level-Feld `system4_root_manifest_sha256` vorhanden;
- String;
- exakt 64 hexadezimale Zeichen;
- Wert exakt gleich dem aktuell berechneten Manifest der kritischen System-4-Dateien.

Fehlt das Feld, ist die definierte fail-closed-Reaktion:

`ROOT_ENTRY_MANIFEST_BINDING_MISSING`

Damit entspricht der reale Codex-Ausgang exakt dem bereits vorhandenen Negativtest.

## Was real erreicht wurde

Bewiesen durch diesen Lauf:

- Codex folgt weiterhin der System-4-Root-Tür;
- der frühere Fehler `ROOT_ENTRY_BRANCH_NOT_SYSTEM4` trat **nicht** erneut auf;
- die Root-Prüfung ist im echten Codex-Lauf aktiv;
- fehlende Manifest-Bindung blockiert real fail-closed;
- kein Legacy-Fallback wurde gewählt;
- kein zweiter Lauf wurde gestartet.

## Was NICHT ausgeführt wurde

Nach dem Root-Blocker wurden ausdrücklich nicht gestartet:

- Web-Recherche;
- `SYSTEM4_RESEARCH_EVIDENCE_V1`;
- `SYSTEM4_FACTS_EVIDENCE_V1`;
- Fact-Pack;
- Production Context;
- Draft;
- LanguageTool im Codex-Lauf;
- PPM im Codex-Lauf;
- Repair;
- Batch-Gate;
- V2-Handoff;
- Inline-Relay;
- Parent-Chat-Rekonstruktion;
- WordPress-Datei.

Daher gibt es aus diesem Real-Lauf:

- **keinen Artikel**;
- **keinen LT-/PPM-Real-PASS innerhalb des Codex-Laufs**;
- **keinen Batch-PASS**;
- **keinen Handoff-PASS**;
- **keine WordPress-Datei**;
- **keinen SYSTEM4_BOUND_BATCH_PASS**.

## Repository-/Sicherheitsstatus

Codex meldete:

- keine Repository-Datei geändert;
- kein Commit;
- kein neuer Pull Request;
- kein Merge;
- kein Publish.

Der bestehende PR blieb auf dem gleichen Head während des Laufs.

## Bewertung

Dieser Lauf ist insgesamt:

**FAIL / BLOCKED**

Der konkrete aktuelle Blocker lautet:

`S4-BLOCK-REAL-LIVE-SNAPSHOT-MANIFEST-MISSING`

Kritische Einordnung:

- Die neue Root-Implementierung hat sich in diesem Fall wie spezifiziert verhalten.
- Der lokale Negativtest hat genau diesen Fall bereits korrekt abgedeckt.
- Der Fehler lag darin, dass der aufrufende Chat beim Erzeugen des realen Live-Snapshots das neue Pflichtfeld nicht mitgegeben hat.
- Deshalb darf dieser Lauf **nicht** als Beleg gegen die Checkout-Identity-Reparatur gewertet werden.
- Ebenso darf aus ihm **kein** Real-PASS für die restliche Produktionskette abgeleitet werden, weil diese Kette nicht begonnen hat.

## Next Action

Kein weiterer Codex-Lauf ohne neue ausdrückliche Nutzerfreigabe.

Vor einem möglichen weiteren Real-Lauf muss der gebundene Produktionssnapshot bereits vor dem Codex-Aufruf vollständig und bytegenau einschließlich

`system4_root_manifest_sha256 = 3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c`

feststehen und genau dieser vollständige Snapshot an `root_entry.py start-stdin` übergeben werden.

Kein Architekturumbau. Keine Änderung an Textmaschine, LT, PPM, Batch-Gate, Handoff, WordPress oder Design aufgrund dieses Fehlers.

Kein Merge. Kein Publish.
