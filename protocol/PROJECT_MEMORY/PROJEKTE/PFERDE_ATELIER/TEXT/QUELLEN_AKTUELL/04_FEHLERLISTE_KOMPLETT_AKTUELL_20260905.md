# STARTMASTER0107 – KOMPLETTE AKTUELLE FEHLERLISTE – 05.09.2026

## A. M01–M33 – bestehende historische Regressionen

### AKTUELLER GESAMTBELEG 06.09.2026

Auf dem aktuellen Hobbyraum-Quellstand `3ed31aa78978a2098f324eead6f2a5335a10e2d4` wurde der **bestehende** M01–M33-Runner vollständig ausgeführt:
- M01–M33: **PASS**;
- `LAST_REGRESSION PASS BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`;
- Abschlussstatus: **`GESAMT PASS`**.

Ausführung erfolgte in einer wegwerfbaren GitHub-Testhülle; deren einziger zusätzlicher Diff war die temporäre Workflow-Hülle. Der geprüfte Kontroll-/Produktionsbaum entsprach `3ed31aa…`.

**Grenze:** Dieser Regression-PASS ist ausdrücklich **kein Live-/7/7-PASS**.


| ID | Fehlerklasse | Teststatus | Live-Status / Bemerkung |
|---|---|---|---|
| M01 | State-/Bundle-Hash chain | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M02 | Unique article files / keine ARTICLE.md-Kollision | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M03 | PREPARED Persist/Restore | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M04 | Finalize CLI real aufrufbar | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M05 | Durable Release/Receipt | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M06 | No fake production contract | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M07 | Recovery not automatically final | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M08 | PPM 6.7.9 Original-ZIP vorhanden | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M09 | PSERC-FIX Original-ZIP vorhanden | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M10 | Preflight fail-closed | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M11 | Real PPM call | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M12 | Fake PPM blocked | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M13 | PPM content_hash == final article SHA | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M14 | Current Action Handoff | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M15 | 107007 Handoff instruction konsistent | **PASS 06.09. auf `3ed31aa…`** | Zusätzlich gefundener Testfehler: zwei Negativfälle hängten `\\n` als Literal statt eines echten Zeilenumbruchs an. Nur dieser Testfehler wurde KISS korrigiert; kompletter M01–M33-Lauf danach PASS. Kein eigener Live-Produktionsblocker. |
| M16 | Signer boundary außerhalb Codex | **Runner-Orakel stale / aktueller Vertrag lokal PASS** | Alte Marker `codex_worker_signer_access_allowed=False` sind nicht mehr Soll. Aktueller Vertrag: keine Signer-Kommandos/-Credentials im 107007-/Runtime-Pfad; Signer erst in `finalize_after_107008`. History-Kandidat `5ea8d5da…` prüft genau diese Grenze positiv/negativ. |
| M17 | 107008 fail-closed | **AKTUELLER PRE-MERGE-REGRESSIONBLOCKER: `M17_HOST_FINALIZATION_NOT_FAIL_CLOSED`** | History Authority PR #198 und sequenzielle Gate-Wartung PR #200 sind auf main `462a67b4d25c6d1d7bf4cc1f010116c0017f7da6` integriert. KISS-Kandidat #199 nach Rebase auf fresh main: Head `45b318673856ff45f42b292c04f56f06ddf76ab1`: genau 1 Logikdatei ergänzt die fehlende Prüfung `ok=true` + `PSERC_FINAL_PACKAGE_PASS`; 5 weitere Dateien sind ausschließlich die bereits vorhandene Hash-Refresh-Kette. Lokal: M16 PASS, M17 positiv PASS, fehlender Guard BLOCK, falsche Reihenfolge BLOCK, Hash-Kette konsistent. Serverseitig: current main reproduziert M17; M17-Kandidat passiert M01–M21 und erreicht anschließend M22. Die Zwangsjacke ist mit PR #200 KISS korrigiert: M17 muss verschwinden; exakt M22 darf danach als gebundener nächster bekannter erster FAIL erscheinen. M35 bleibt geparkt. |
| M18 | ENDSTEMPEL constants | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M19 | Merge trigger | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M20 | Delivery 7 Artikel + Envelope + Manifest | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M21 | No auto-publish | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M22 | H8 Provenance / Integrität ohne interne Signatur | **NÄCHSTER BEKANNTER REGRESSIONSTREFFER NACH M17** | Autoritative B15-Regel: interner 107007-/H8-Vorlauf hash-/batch-/herkunftsgebunden, keine interne ED25519-/Signer-Pflicht. Korrigiertes Orakel: current main FAIL `M22_INTERNAL_SIGNATURE_STILL_REQUIRED`; bewiesener B15-Stand `7990029428399e8ba01d88a6543ce068812e9218` PASS. M22 bleibt eigener späterer Fix, kein Sammelfix mit M17. |
| M23 | Preproduction/Runtime Guards | im bestehenden Runner enthalten | Altregel korrigiert: intern nur Hash-/Herkunftsbindung; externe Signierung nach abgeschlossener Produktion bleibt separat erhalten. |
| M24 | No H8 rollback | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M25 | Article prompt / Fachworkflow boundary | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M26 | Bound Fachworkflow production context | im bestehenden Runner enthalten | früher mehrfach LIVE BLOCKED; auf aktuellem main im letzten Lauf überwunden |
| M27 | Current-main / production environment identity | im bestehenden Runner enthalten | Preflight/HEAD im letzten Lauf PASS |
| M28 | Fachworkflow-Handoff request executable | Runner auf main korrigiert | **LIVE ÜBERWUNDEN 08.09.2026:** PR #161 / Merge `78bb2576…`; Realtest materialisierte den frischen `FACHWORKFLOW_HANDOFF_REQUEST.json`, startete den gebundenen Handoff und erreichte den echten PPM-6.7.9-Korridor. |
| M29 | Release metadata current-batch identity | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M30 | Final context batch identity | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M31 | Codex-native bound action / kein separater Executor | im bestehenden Runner enthalten | **Runner-Test war stale:** erwartete fälschlich überhaupt keinen `fachworkflow_handoff`. Aktueller Sollweg bindet den Handoff innerhalb derselben Current Action und verlangt ausdrücklich keinen separaten Executor/keine separate Capability. Im Hobbyraum korrigiert und positiv/negativ geprüft. |
| M32 | PPM runtime package path ohne Env-Abhängigkeit | im bestehenden Runner enthalten | **LIVE ÜBERWUNDEN 08.09.2026:** PR #158 / Merge `30e93335…`; nachfolgender Realtest erreichte den echten `fachworkflow_proof_handoff.py materialize` und stoppte erst bei M28. |
| M33 | GitHub ENDSTEMPEL ohne Codex git auth | im bestehenden Runner enthalten | historisch / nicht als eigener aktueller Live-Blocker offen |
| M34 | Reapplied legacy PPM handoff guards after B01 | **LIVE ÜBERWUNDEN 08.09.2026:** PR #190 / Merge `2325f6e1…` stellte den bewiesenen B01-Handoff als konsistente Einheit wieder her. Nachfolgender Realtest kam über `CANONICAL_SLOT_MISSING` hinaus und stoppte erst bei M35. |
| M35 | Fact-Pack source-hash binding parity | **AKTUELLER LIVE-BLOCKER:** `PPM679_REAL_EXECUTION_FAILED:SOURCE_HASH_BINDING_MISMATCH`; History Authority PR #196 ist auf main `d6de9265cddc1b2a011d707ad615c144cdd9d4ab` integriert. **Root Cause belegt:** PPM speichert nach Fact-Pack-Import einen eigenen Registry-Hash; der Handoff liest ihn bereits, vergleicht ihn aber gegen den Forschungs-/Fact-Pack-Hash in `source_hashes`. KISS-Kandidat `ef2ecebeb2992013873ba72100d79ffd7c48393c` ändert ausschließlich die interne PPM-Plan-Kopie: leerer Registry-Hash bleibt BLOCK, sonst `source_hashes=[PPM-Registry-Hash]`. Lokale Positiv-/Negativprüfung PASS; serverseitige Hardlocks und Live-7/7 noch offen. |

## B. Reale Blocker / Wiederholungsfehler außerhalb bzw. quer zur Matrix

### B01 – WordPress-Kategorie-Identität
- Bereits am 28.08. als Wiederholungsfehler dokumentiert.
- Historisch: Name/Slug/Taxonomy müssen korrekt zur gebundenen Kategorie passen.
- Historischer Live-Blocker: `BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION`; durch B01-Semantik überwunden. Der Realtest auf `2325f6e1…` passierte Kategorie-/Slot-Vorbedingungen und stoppte erst an M35.
- **Kausalbefund 05.09.:** Der aktuelle Handoff blockiert vor dem echten PPM allein auf fehlender numerischer WordPress-ID, obwohl der vorhandene Kategorievertrag Name/Slug/Taxonomy bindet.
- Exakter Guard-Positiv-/Negativtest:
  - gültige Name/Slug/Taxonomy ohne ID → alter Guard **BLOCK**, KISS-Guard **PASS**
  - gültige Kategorie mit ID → alt **PASS**, neu **PASS**
  - fehlender Name trotz ID → alt fälschlich **PASS**, neu **BLOCK**
  - falsche Taxonomy trotz ID → alt fälschlich **PASS**, neu **BLOCK**
  - fehlender Slug → alt **BLOCK**, neu **BLOCK**
- Bevorzugter kausaler Hobbyraum-Kandidat: Draft-PR #141, Branch `hobbyroom/b01-only-kiss-20260906`, Head `94917596adce04765380c60dd7ade0fb23793393`. PR #140 bleibt als breiterer B01+B15-Prüfstand separat bestehen.
- Kandidat ändert keine SEO-/Textmaschinen-/PPM-Regel; nur der bestehende Handoff verwendet die ID nicht mehr als vorgezogene Produktionsvoraussetzung.
- #141: `hardlock` + `hardlock-base` + `MONOTONIC_PREBOUND_TRANSITION_PASS` + Cloud-/Continuity-Positiv-/Negativtests: **PASS**.
- kompletter M01–M33-Lauf ist auf dem breiteren #140-Head `3ed31aa…` **GESAMT PASS**; auf exakt #141 wurde er nicht neu ausgeführt, weil kein vorhandener zulässiger Workflow dafür existiert und keine neue Testhülle gebaut wird.
- **Kein Gesamt-7/7-Live-PASS behauptet:** B01 selbst ist im aktuellen Korridor praktisch überwunden, der Gesamtworkflow bleibt an M35 BLOCKED.
- **Harte Nutzerregel:** Nicht durch Erweiterung des SEO-5-Felder-Handoffs lösen.

### B02 – `BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING`
- 04./05.09 mehrfach erster realer Blocker vor Artikel 1.
- Ursache im aktuellen Vertrag: Codex-Worker-Rolle nicht hart genug als Fachworkflow-Ausführung gebunden.
- PR #136 bindet Current Codex als Fachworkflow-Worker.
- Letzter Live-Lauf auf `c8a96e7…` kam über diesen Blocker hinaus → derzeit **live überwunden**.

### B03 – PPM-/PASS-Reihenfolge / Kreisschluss
- Nach Einführung echten PPM 6.7.9 wurde zeitweise ein bereits vollständiger Fachworkflow-PASS/Receipt vor dem realen PPM faktisch vorausgesetzt.
- PR #135 ordnet vorhandenen Handoff neu: realer Fachoutput → echter PPM → erst danach finaler PASS/Receipt.
- 4 positive + 4 negative Prinziptests PASS; vollständiger Livebeweis noch ausstehend, weil Live vorher am Kategoriepunkt stoppt.

### B04 – Fake-PPM-PASS im Handoff
- Prinziptest fand, dass ein behaupteter PPM-PASS zunächst bis zum nachgelagerten Validator gelangen konnte.
- Fail-closed im Handoff geschlossen: PPM-Stufe verlangt echte `ppm679_binding` und realen PPM-Pfad.

### B05 – `CODEX_CHECKOUT_NOT_CURRENT_MAIN` / stale Environment
- Historisch wiederholt.
- Aktueller Preflight verlangt/prüft main-Identität; letzter Live-Lauf HEAD exakt `c8a96e7…` PASS.

### B06 – Hobbyraum ist kein Produktions-/Live-Testort
- Hobbyraum kann absichtlich keinen Produktionsproof liefern, weil Preflight current `main` verlangt.
- Wiederholungsbeleg 06.09.: Versuch auf Hobbyraum-Head `3ed31aa…` wurde korrekt vor 107007 gestoppt mit `CODEX_CHECKOUT_NOT_CURRENT_MAIN:3ed31aa…:EXPECTED:c8a96e7…`.
- 107007 nicht ausgeführt; 107008 nicht erreicht; keine Artikelproduktion; keine Code-/WordPress-Schreibaktion.
- **Harte Testmethodik:** Live-/7/7-Test niemals aus Hobbyraum-/PR-Head starten. Erst nach regulärer Integration auf current `main`.
- Kein Produktionsfehler auf aktuellem main; dies ist eine bekannte Testgrenze.

### B07 – Runtime-Pakete PPM/PSERC nicht gebunden / Env-Variablen fehlen
- Historisch: `PPM679_PACKAGE_ZIP` / `PSERC_FIX_ZIP` fehlten.
- Repo-gebundene Pakete wurden später ergänzt; Original-SHAs sind dokumentiert.
- **Historischer Wiederholungsbefund 08.09.2026:** Nach Merge des B02-Semantikdeltas auf main `36d1ecb52cf80c91e2f30f5a1eb7ecc1f14782c9` erreichte der echte Codex-Lauf Cloud Entry, Production Preflight, Runtime Entry, Current Action READY und Single Door READY.
- B02 `BOUND_CURRENT_FACHWORKFLOW_EXECUTION_CONTEXT_MISSING` wurde dabei überwunden.
- Neuer erster echter STOP: `BOUND_REAL_PPM679_RUNTIME_PATH_NOT_EXPOSED_TO_SUBMISSION_COMMAND`.
- Konkreter Befund: der ausschließlich zulässige gebundene `fachworkflow_handoff.command` exponiert weder `PPM679_PACKAGE_ZIP` noch `PSERC_FIX_ZIP`; beide Variablen sind im Worker nicht gesetzt.
- 107007 nicht abgeschlossen; 107008 nicht erreicht; kein Publish; keine Codeänderung im Test.
- **Aktueller Status: LIVE ÜBERWUNDEN 08.09.2026:** B07/M32 wurde vor M28/M34/M35 real passiert.

### B08 – `BOUND_RUNTIME_PRODUCTION_CONTEXT_MISSING`
- Historischer realer Blocker nach PPM-Härtung.
- Später präzisiert: Bootstrap-Paket ist nicht Fachworkflow-Kontext.

### B09 – `ITEM_RECEIPT_FIELDS_OR_CONTRACT_INVALID` / Pass-Ref-Mismatch
- Historische Übergabe-/Receipt-Probleme während Handoff-Umstellungen.

### B10 – `RELEASE_METADATA_INVALID`
- Historischer Blocker: Release-Metadaten nicht exakt an Batch/Count gebunden.

### B11 – `FINAL_CONTEXT_BATCH_MISMATCH`
- Historischer Blocker zwischen 107007/107008/Host-Finalisierung.

### B12 – `STAGING_DESTINATION_COLLISION:ARTICLE.md`
- Reale 7/7-Produktion auf `d841ed…` erzeugte 7 Artikel und alle 12 Stages, kollidierte danach wegen gemeinsamem `ARTICLE.md`.
- Später mit artikel-/plan-slot-eindeutigen Dateinamen adressiert.

### B13 – GitHub Endstempel / fehlendes remote/auth
- Reale `de21…`-Strecke erreichte 107008 PASS; danach Endstempel/Auth-Persistenzproblem.
- Hostseitiger Signer/Endstempelweg später gehärtet.

### B14 – Test-Live-Paritätslücke
- Systemischer Fehler: Regressionstests können PASS melden, obwohl die reale Verkettung nicht bewiesen ist.
- Besonders kritisch: der sogenannte „last real regression re-check“ im Runner ist kein echter Replay des letzten 7/7-Laufs.
- Dieser Punkt erklärt die wiederkehrende Erfahrung „Tests grün, Live wieder alter Fehler“.

### B15 – Interne Signieraltlasten aus altem Raum-zu-Raum-Modell
- Historische Sollentscheidung: **innerhalb der Produktion keine kryptografische Arbeiter-/Raum-Signierung; externe Versiegelung erst nach abgeschlossener Produktion**.
- Harte Prüfung 05.09. fand trotzdem aktive interne Reste in H8-Bootstrap/Provenance, Preproduction-Handoff, Runtime-Guard, Codex-Preflight und im gebundenen Generation-1-H8-Paket.
- Hobbyraum-Säuberung auf PR #140: interne Signaturpflicht entfernt; Hash-, Batch-, Slot- und Herkunftsbindung bleiben erhalten.
- Externe Signierung **nicht entfernt**: hostseitige Finalisierung erst nach 107008 sowie GitHub-ENDSTEMPEL/WordPress-Verifikation bleiben unverändert.
- Link-/Tabellen-/LanguageTool-/PPM-/PSERC-/PSTE-/SEO-/Designregeln wurden nicht gelockert oder entfernt.
- M22/M23 sowie die stale M26/M28-Testlogik wurden an den aktuellen Sollweg angepasst.
- **SCOPE-PASS 05.09.:** aktiver Call-Graph bis 107007 enthält keine interne ED25519-/Signer-/Key-/`SIGNED`-Pflicht mehr; aktuelles gebundenes H8-Paket ist `WORKFLOW_SUPERVISOR_RELEASE_V2_HASH_BOUND` ohne Signaturfelder.
- Interne `HASH_BOUND`-Metadaten werden erst in `finalize_after_107008` in den externen `WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED`-Vertrag überführt.
- Externer Production-Release-/ENDSTEMPEL-Weg bleibt signiert; der Host-Signer wird erst im 107008-Endzustand verlangt und bleibt für den Codex-Worker verboten.
- `hardlock` + `hardlock-base` auf Head `3ed31aa78978a2098f324eead6f2a5335a10e2d4`: **PASS**.
- vorhandener M01–M33-Runner auf demselben Quellstand: **M01–M33 PASS + LAST_REGRESSION PASS + GESAMT PASS**.
- **Noch offen:** echter Live-/7/7-Beweis erst nach regulärer Integration auf current `main`; Hobbyraum ist dafür gemäß B06 kein zulässiger Testort.

## C. Letzte real bewiesene positive Referenzen

- `d841ed7590436ac100b98f15194874573e09bc03`: 7/7 frisch produziert; alle zwölf Stages; späterer Lauf erreichte 107008.
- `de21f6cd35c60849c551fd82f78e75ce57c99fab`: 7/7 + 107008 Review PASS; späterer Fehler erst im GitHub-Endstempel/Auth-Bereich.

## D. Historischer Stand vor dem Plan-A-Live-Lauf vom 07.09.2026 – ABGELÖST

Der zuvor erste belegte Live-Blocker auf main `c8a96e7…` war:
`BOUND_WORDPRESS_CATEGORY_ID_MISSING_FOR_REAL_PPM679_EXECUTION`.

Dafür wurde der isolierte B01-Kandidat #141 gebaut und später regulär integriert.

**Dieser Abschnitt ist nicht mehr die aktuelle Fehlerwahrheit.**
Die aktuelle Live-Wahrheit steht oben in der M-Tabelle bei M35. Der nachfolgende LanguageTool-Befund bleibt nur als Historie erhalten.

## HISTORISCHER LIVE-BEFUND 07.09.2026 – LANGUAGETOOL – ABGELÖST

Damals geprüfter main:
`f14ccf187b94c4beab9a86d0c69144f792ba2f64`

Plan-A-Live-Lauf nach Merge von PR #141:
- Cloud Entry: PASS
- Environment Preflight: PASS
- Runtime Entry: PASS
- Current Action: `CURRENT_BOUND_ACTION_READY`
- Single Door: READY
- erster echter STOP: `BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING`
- state_advanced=false
- 107007 nicht abgeschlossen
- 107008 nicht erreicht
- keine Code-/Artikel-/Publish-Änderung.

Harte lokale Einordnung:
- #141 hat LanguageTool nicht verändert.
- `codex_current_action.py` ist zwischen vorherigem main `c8a96e7…` und aktuellem main byte-identisch.
- verbindlicher Texterstellungs-Prompt ist zwischen letztem realen 7/7-Stand, `c8a96e7…` und aktuellem main identisch.
- `languagetool` war bereits im letzten realen 7/7-Stand Pflichtstufe.
- im gebundenen STARTMASTER-Pfad ist kein eigener LanguageTool-Ausführungsbefehl / keine eigene LanguageTool-Runtime als authorized input sichtbar.
- der Fehlerstring `BOUND_LANGUAGETOOL_EXECUTION_PATH_MISSING` ist kein im Repo implementierter Wächterfehler; er wurde vom aktuellen Codex-Lauf aus der fehlenden ausführbaren Bindung abgeleitet.
- der vorherige Live-Lauf auf `c8a96e7…` erreichte dagegen B01 bei identischer Current-Action-/Prompt-Grundlage.

Schluss:
Kein belegter LanguageTool-Abbau durch B01. Aktuell sichtbar ist eine ältere technische Lücke: Pflicht zur realen LanguageTool-Ausführung ist fachlich fest, der konkrete ausführbare Weg ist jedoch im aktuellen gebundenen Worker-Interface nicht deterministisch vorgegeben. Kein Qualitäts- oder Regel-Fix zulässig; zuerst bestehenden historischen Ausführungsweg suchen/belegen.

B01 bleibt live noch nicht als PASS bewiesen, weil der neue Lauf vor B01 stoppte.
