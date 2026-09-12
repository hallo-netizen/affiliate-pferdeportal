# System 4 – Abschluss-/Nachholprotokoll 2026-09-12

Historisches WAS/WARUM-/Testprotokoll. Keine CURRENT_STATE-Autorität, kein Produktions-PASS, kein Publish.

## Tatsächlich ausgeführte Änderungen/Befunde dieses Chats
- System-4-Batch-Gate und indexierter Ingress waren bereits vorhanden; Ziel blieb ein realer 7/7-Artikelbatch mit FULL_PRODUCTION/PASS je Artikel.
- Nach einem Codex-7/7-PASS, dessen behauptete Proof-Dateien nicht dauerhaft auf dem PR-Branch vorhanden waren, wurde ein `proof_persistence_guard.py` plus Negativtests ergänzt. Dieser Guard ist nur Test-/Handoff-Härtung und keine Pflicht der Ziel-Produktionsarchitektur.
- Der Persistenz-Guard-Test war später veraltet und erwartete noch Artikel-Proof-Dateien. Ursache: Produktionsziel hatte die dauerhafte GitHub-Ablage der Artikeltexte inzwischen verworfen. Der Test wurde ohne Codex auf die aktuelle Proof-Semantik korrigiert; lokaler Guard-Test: 4/4 PASS.
- Eine isolierte `signature_bridge.py` samt Test wurde als schmale ENDSTEMPEL-/Signaturvorbereitung ergänzt. Lokaler Brückentest: gültig PASS; manipulierte Artikel/Import-Envelope/falsche Signatur BLOCK. Das ist kein WordPress-Livebeweis und keine Produktionsfreigabe.
- Ein zusätzlich angelegter GitHub-Signaturworkflow außerhalb `isolated_system4/**` wurde bei dieser Abschlussprüfung als Verstoß gegen die System-4-Isolation erkannt und wieder entfernt. Signierung/WordPress-Endstrecke sind ausdrücklich zurückgestellt.
- Ohne Codex wurde der zweite reale Beratung-Artikel `Eine richtige Reitplatzbeleuchtung ohne Mast finden` lokal durch denselben System-4-FULL-Prüfweg geführt: frische Recherche/Faktenbindung; Research-Gate Positiv/Negativ 4/4 PASS; echtes LanguageTool 6.8 zuerst 8 Findings, nach Reparatur desselben Drafts 0 Findings; echter PPM 6.7.9 TECHNICAL PASS + CONTENT QUALITY PASS + Aggregate PASS. Finaler beobachteter Draft-SHA256: `16b76a1d301e783cd151073ae39717cabe663aa0e34c93f0abdd48656444e0b5`. Dieser lokale Befund ist nicht als dauerhafter Branch-Produktionsproof materialisiert und wird deshalb nicht als Repository-PASS hochgestuft.
- Beim dritten Artikel wurde lokal LanguageTool 6.8 auf 0 Findings gebracht; ein finaler PPM-FULL-PASS wurde vor dem Wechsel zurück zu Codex nicht abgeschlossen. Artikel 3 ist daher NICHT PASS.
- Ein späterer echter Codex-7/7-Auftrag wurde erst nach lokalem Preflight angestoßen. Der Auftrag verlangte 7 frische Artikel, echtes LT 6.8, echten PPM 6.7.9, Same-Draft-Reparatur und Batch-Gate; Signatur/WordPress waren ausgeschlossen. Terminaler Rücklauf: `Codex couldn't complete this request. Try again later.` Es wurde weder ein System-4-Checkerblocker noch ein 7/7-Batchresultat geliefert. Der Lauf ist daher kein Beweis und wird nicht automatisch wiederholt.

## Verbindliche Entscheidungen / Warum
1. Primärziel ist Artikelproduktion. Signatur, ENDSTEMPEL und WordPress-Livetest werden zurückgestellt, bis ein echter 7/7-Artikelbatch vorliegt.
2. Fertige Artikeltexte müssen nicht dauerhaft in GitHub gespeichert werden. GitHub-Persistenz darf nicht zu einer zweiten Produktionspflicht werden.
3. Codex-Kontingent ist knapp und wird nicht mehr für Diagnose-, Architektur-, Read-only- oder Test-only-Läufe verbraucht. Solche Arbeiten werden soweit möglich ohne Codex erledigt.
4. Ein neuer Codex-Aufruf ist nur für einen echten Produktionslauf zulässig und nur, wenn vor dem Start der Einstieg lokal sauber geprüft ist UND der Lauf am Ende einen real abrufbaren Datei-Handoff liefern kann. Ein riesiger PR-Kommentar mit sieben Volltexten ist kein zulässiges Ziel mehr.
5. Kein neuer Codex-Lauf, solange diese reale Dateiübergabe nicht vorab geklärt ist. Der fehlgeschlagene letzte Auftrag wird weder als Artikel-PASS noch als System-4-Checker-BLOCK gewertet.
6. Main/STARTMASTER0107 bleibt von System 4 getrennt. Keine System-4-Erkenntnis überschreibt `control/startmaster0107/CURRENT_STATE.json` oder den gebundenen M38-Hobbyraum.

## Tests – tatsächlich ausgeführt
- Erster realer System-4-Beratung-Artikel: vorhandener FULL-PASS-Beweis mit realem PPM 6.7.9 und LanguageTool sowie Tabellen-/Link-Positiv/Negativprüfung.
- Batch-Gate: vorhandene positive/negative Sammlungstests PASS.
- Proof-Persistence-Guard: lokal 4/4 PASS nach Korrektur des veralteten Tests.
- Signature-Bridge: lokal 4/4 PASS (1 positiv, 3 negativ); KEIN WordPress-Livetest.
- Artikel 2 lokal: Research-Gate 4/4 PASS; LT 6.8 final 0 Findings; PPM 6.7.9 Technical/Content/Aggregate PASS.
- Artikel 3 lokal: LT 6.8 final 0 Findings; finaler PPM-PASS NICHT ausgeführt/nicht belegt.
- Letzter Codex-7/7-Auftrag: extern fehlgeschlagen; keine Artikel-/Batchprüfung daraus belegbar.
- Neuer Dokumentations-Head: kein GitHub-CI-Status vorhanden; daraus wurde ausdrücklich kein PASS abgeleitet.

## Offene Punkte
- Reale 7/7-Serie unter aktuellem System-4-Stand ist noch nicht als aktueller kompletter Batch belegt.
- Ein sparsamer realer Datei-Handoff für Codex muss VOR dem nächsten Codex-Produktionslauf feststehen.
- Signatur/ENDSTEMPEL/WordPress-Import bleiben bewusst zurückgestellt und sind nicht als aktueller System-4-PASS zu behandeln.
- Kein Publish; `publish_allowed=false`.

## Nachtrag – Geschwindigkeitsprüfung / Root Cause / KISS-Fix
- Der langsame Codex-Lauf zeigte beim dritten Artikel einen normalen LanguageTool-Fund (`Befüllweg`), der von einem ad-hoc erzeugten `/tmp/system4_run.py` fälschlich als `RuntimeError('LT_FINDINGS_PRE_CONTEXT')` behandelt wurde. Das war kein Fehler des System-4-Controllers und kein PPM-/Redaktionsplan-Fehler.
- Harte Gegenprüfung gegen den früheren schnellen 7/7-Lauf: `controller.py`, `production_checks.py`, `batch_gate.py` und `live_fixture/wordpress_snapshot.json` sind byte-identisch zum Head des früheren 7/7-PASS-Laufs. Der Geschwindigkeitsverlust liegt damit nicht im bewährten Kernpfad, sondern in zusätzlicher Codex-Orchestrierung außerhalb dieses Pfads.
- `AGENTS.md` und `FULL_RULE_BATCH_TASK.md` wurden deshalb KISS-hart gebunden: `controller.py fullcheck` ist der einzige Checker-Orchestrator; direkte LT-/PPM-Prechecks und Custom-Wrapper sind verboten; repairable Findings führen ausschließlich zu `REPAIR_REQUIRED` und Same-Draft-Reparatur; bereits bestandene Artikel werden nicht neu gestartet; unveränderte Head-Preflights werden nicht innerhalb Codex wiederholt.
- Sicherheits-/Qualitätsregeln wurden nicht reduziert: echtes LanguageTool 6.8, echter PPM 6.7.9, NO-LEGACY, External-Link-Verbot, SEO/PSERC/PSTE-Bindung, Tabellen-/Interne-Link-Regeln, immutable metadata, exakte Slots/Batchbindung und `publish_allowed=false` bleiben Pflicht.
- Neue lokale Regressionen: `test_repair_continuity.py` prüft positiv Same-Draft-Reparatur und 7er-Kontinuität sowie negativ echten Tool-Hardblock; `test_codex_economy_contract.py` sperrt die bekannte falsche Wrapper-/Preflight-Route. Lokal getesteter 7er-Kontinuitätslauf: Check-Aufrufe `1/1/2/1/1/1/1` = 8 gesamt; echter LT-Laufzeitfehler BLOCK; Immutable-Tamper BLOCK; Economy-Vertragschecks 3/3 PASS.
- Die lokal getesteten AGENTS-/Batch-Task-Bytes wurden gegen ihre Git-Blob-SHAs geprüft und stimmen exakt mit dem Branch überein.
- Nicht behauptet: Die komplette aktuelle `unittest discover`-Suite konnte in diesem Chat nicht direkt aus einem lokal geklonten Repository ausgeführt werden, weil der Container keinen GitHub-Netzzugriff hat; auf Head `9133bbee...` existiert aktuell auch kein GitHub-CI-Status. Daher kein daraus erfundener Gesamt-PASS.
- Konsequenz: Kein weiterer Codex-Aufruf, bevor aktuelle Head-Preflight/NO-LEGACY und der Datei-Handoff ohne Codex belastbar bestätigt sind.