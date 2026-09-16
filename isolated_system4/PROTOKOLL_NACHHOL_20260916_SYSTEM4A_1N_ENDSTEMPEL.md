# PROTOKOLL-NACHTRAG — SYSTEM 4A 1..N / ENDSTEMPEL — 2026-09-16

Status dieses Dokuments: **historische Ausführungs- und Entscheidungs-Evidence**.

Dieses Dokument ist **keine CURRENT_STATE**, keine Bürotür, kein Fehlerregister und keine eigene NEXT-ACTION-Wahrheit. Operativer Stand muss immer frisch aus Bürotür → zuständiger CURRENT_STATE → aktuellem Branch/Head → echten Workflow-Läufen bestimmt werden.

## Anlass

Nach der WordPress-Fail-Closed-Korrektur wurde die bestehende Produktions-/ENDSTEMPEL-Strecke auf feste 7-Artikel-Annahmen geprüft. Dabei waren noch aktive Mengenbindungen in der 107008-Transport-/Finalstrecke vorhanden. Außerdem waren in `GITHUB_FINAL_RELEASE.py` bereits früher reparierte Import-Envelope-Konstanten wieder verloren gegangen.

## Dauerhafte Reparaturen — WAS / WARUM

1. `control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json`
   - feste 7er-Aussage entfernt;
   - zulässig ist `article_count>=1` exakt entsprechend dem gebundenen Release-Receipt.
   - WARUM: Mengenautorität muss aus dem real gebundenen Batch stammen, nicht aus historischer Namensgebung.

2. `control/startmaster0107/chat_delivery_payload.py`
   - Artikelmenge wird aus den tatsächlich hashgeprüften Release-Outputs ermittelt;
   - mindestens ein Artikel, keine feste Obergrenze 7;
   - historischer Dateiname mit `7` bleibt nur als Kompatibilitätsname und ist ausdrücklich kein Mengenvertrag.
   - WARUM: kein unnötiger Rename/Architekturumbau; nur die echte Mengenlogik wird dynamisch.

3. `control/startmaster0107/GITHUB_FINAL_RELEASE.py`
   - `item_count >= 1` ist die gebundene Mengenautorität;
   - Source-Items, Artikeldateien, Import-Envelope und finaler Manifest-Count müssen exakt zusammenpassen;
   - `IMPORT_ENVELOPE_NAME` und `IMPORT_ENVELOPE_KEYS` wurden wiederhergestellt;
   - historischer 7er-Dateiname bleibt reine Kompatibilität.
   - WARUM: Regression einer bereits vorhandenen Import-Envelope-Bindung beseitigen, ohne Signatur-, Hash- oder WordPress-Grenzen zu lockern.

4. `isolated_system4/downstream_1n_contract_probe.py`
   - Positiv: 1 / 3 / 25 Artikel;
   - Negativ: Source-Count-Mismatch blockiert;
   - Negativ: `item_count=0` blockiert;
   - Source-Guard blockiert erneut auftauchende feste 7er-Verträge und fehlende Import-Envelope-Konstanten.
   - Der Probe läuft im bereits vorhandenen WordPress-Importer-Prüfschritt; kein zweiter Acceptance-Workflow wurde angelegt.

## Echte Prüfungen auf funktionalem Head

Funktionaler Prüfhead: `637f800c3c0dfffda1e31e25519a6872e2a475bd`.

Auf exakt diesem Head wurden am 16.09.2026 drei bestehende Workflow-Läufe ausgeführt und erfolgreich beendet:

- `35096890497` — **System 4A Repair Owner Contract** — SUCCESS.
- `35096890762` — **System 4A Exact Head Bundle** — SUCCESS.
- `35096890660` — **System 4A Real LT68 PPM679 Acceptance** — SUCCESS.

Der Real-Acceptance-Job `104796358244` lief auf exakt `637f800c...`; die Schritte 1–35 wurden tatsächlich ausgeführt. Insbesondere:

- Schritt 7 `Inspect real WordPress importer contract` — SUCCESS;
- Schritt 29 `Textmaschine matrix — batch handoff one-to-N` — SUCCESS;
- Schritt 31 kompletter 1-Artikel-Weg — SUCCESS;
- Schritt 33 kompletter 3-Artikel-Weg mit Repair-Isolation — SUCCESS;
- Schritt 34 Fresh-Route-Evidence — SUCCESS;
- Schritt 35 Candidate-Artifact-Upload — SUCCESS.

Der in Schritt 7 direkt aufgerufene Downstream-Probe enthält und durchläuft 1 / 3 / 25 positiv sowie Count-Mismatch und Null-Batch negativ. Der reale WordPress-Probe bindet weiterhin den vorhandenen Importer-Build `0.28.18-endstempel-import-envelope-binding-ppm679`, verlangt `PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1` und blockiert einen rohen `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` als direkten WordPress-Import.

## Zielvertrag-Nachholung

Beim Abschlusscheck wurde ein Scope-Widerspruch festgestellt:

- der bisherige Zielvertrag endete formal beim V2-Handoff / bytegleichen Parent-Chat-Transport;
- das bereits verbindliche Testprotokoll verlangt als Abschlussstrecke zusätzlich reale WordPress-Importformatprüfung und Ausgabe derselben finalen Importdatei im Parent-Chat.

Der **bestehende eine** Zielvertrag `ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_CODEX_WRITER_20260914.md` wurde deshalb minimal auf die bereits verbindliche Abschlussstrecke erweitert. Es wurde kein zweiter Zielvertrag angelegt. Raw-V2-Direct-Import bleibt ausdrücklich verboten; PSERC-/ENDSTEMPEL-Grenze, Signaturbindung und `publish_allowed=false` bleiben erhalten.

Zielvertrags-Nachholcommit: `6d695226b0a30b3b435925a2c8098b448a6c7d9d`.

## Campus / CURRENT_STATE

Der campusweite Pflichtweg auf `main` ist strukturell eindeutig:

`control/CURRENT_STARTMASTER.json`
→ `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
→ `control/startmaster0107/CURRENT_STATE.json`.

Die zuständige CURRENT_STATE ist jedoch fachlich veraltet: sie bindet weiterhin den alten 107007-/M38-/PPM-Plan-Version-Stand und einen anderen Hobbyraum, während der aktuelle System-4A-Arbeitsbranch am 16.09.2026 deutlich weiter ist.

Die CURRENT_STATE setzt selbst `state_write_authority = ENTRANCE_GATE_ONLY` und `free_chat_direct_execution_valid=false`. Deshalb wurde sie **nicht** aus diesem Chat/Branch überschrieben und es wurde **keine zweite CURRENT_STATE** angelegt. Die Campus-Synchronisation ist bis zu einem autorisierten Entrance-Gate-/State-Owner-Weg BLOCKED.

## Parallelwege frisch geprüft

- aktiver System-4A-Arbeitsbranch: `hobbyroom/system4a-startgate-test-20260914`;
- alter Schritt-33-Diagnosebranch: `hobbyroom/system4a-step33-diag-35085131467`, Head `654524250166c13e1aea4bf30c0974c5041eb2c7` — nicht überschrieben;
- älterer Capsule-Branch: `hobbyroom/system4a-capsule-v1-20260913`, Head `6f1e8acd2c92ca23ccbf96b734d1d7770e3414a2` — nicht überschrieben.

## Nicht verändert

- kein Plugin entwickelt oder aktualisiert;
- `PSERC-FIX.zip` nur geprüft, nicht verändert;
- keine Textmaschinen-, LT-6.8-, PPM-6.7.9- oder Designschwelle gelockert;
- kein lokaler Signierer eingeführt;
- kein neuer WordPress-Importer gebaut;
- kein Auto-Publish aktiviert;
- kein zweiter Workflow als Acceptance-Wahrheit angelegt;
- keine zweite CURRENT_STATE angelegt;
- keine Bürotür mit dynamischer Fachwahrheit angereichert.

## Abschlussgrenze

Die System-4A-Route und die 1..N-Nachholung sind remote maschinell belegt. Das ist **kein Gesamt-PASS**.

Gemäß `PROTOKOLL_TESTSTRECKE_V2_20260914.md` fehlt bis zum Gesamtabschluss weiterhin die reale nachgelagerte Abschlussstrecke bis zur formatgeprüften finalen WordPress-Importdatei und deren tatsächlicher byte-/SHA-identischer Ausgabe im Parent-Chat. Vorher bleiben Produktionsfreigabe und Publish gesperrt.
