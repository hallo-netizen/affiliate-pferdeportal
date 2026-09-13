# SYSTEM 4 — TRUE SINGLE ROOM

Status: **LOCAL PREFLIGHT PASS / isolated prototype / test only / USER APPROVAL REQUIRED BEFORE CODEX.** Kein Merge, kein Produktions-Publish. Ein echter Codex-Produktionslauf wurde noch nicht gestartet.

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit** innerhalb des isolierten Prototyps. Der offizielle Projekt-/Campus-Stand bleibt davon getrennt in `control/startmaster0107/CURRENT_STATE.json` und wird durch System 4 nicht überschrieben.

## Verbindlicher Zielvertrag
`isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`

Kurzform:
`gebundene Metadaten -> Codex recherchiert -> Codex bildet Fakten/Fact-Pack -> Codex schreibt -> unveränderte echte Prüfer -> gezielte Same-Article-Reparatur -> Batch-/Wiederholungsprüfung -> exakter Chat-/WordPress-Handoff`

Codex bleibt der eine fachliche Worker. System 4 übernimmt **nicht** die alte Legacy-Orchestrierung.

## Universelle Produktionsgrenze
Verbindlich gilt:
- Produktionsmenge = exakt die nichtleere Item-Menge des gebundenen Snapshots;
- **1..N ohne künstliche System-4-Obergrenze**;
- 1 / 7 / 25 / 1000 sind ausschließlich Regressionstestgrößen;
- `article_type` kommt aus den gebundenen Metadaten;
- **keine System-4-Beitragsart-Whitelist**;
- neue Beitragsarten laufen ohne Änderung an Controller, Batch-Gate oder Handoff durch denselben generischen Weg;
- typspezifische fachliche/designseitige Zulässigkeit bleibt Sache der unveränderten autoritativen Textmaschine-/PPM-/Designregeln.

## Unverhandelbare Grenzen
### Textmaschine
Die bestehende Textmaschine und ihre Regeln sind READ-ONLY. System 4 darf sie weder direkt noch indirekt ändern, erweitern, abschwächen, neu interpretieren, normalisieren, ersetzen oder durch eigene Schreibregeln überschatten.

### Design
PPM 6.7.9, bestehender Artikel-/Tabellenvertrag, WordPress-Plugin, Theme/CSS und vorhandene Designselektoren sind READ-ONLY. System 4 darf weder direkt noch indirekt CSS, Inline-Styles, Klassen, Überschriftenhierarchie, Tabellenformatierung oder Theme-/Plugin-Dateien verändern. Nach dem geprüften Artikel ist keinerlei HTML-/Designtransformation erlaubt.

`design_guard.py` ist ausschließlich PASS/BLOCK und verändert keine Bytes. Die `ppm-type-*`-Bindung wird aus dem gebundenen `article_type` generisch abgeleitet. Bekannte typspezifische Regeln bleiben nur für ihren Typ aktiv und sind keine Zulassungsliste.

## System-4-Schutzkette
1. `content_guard.py`: Research-/Fact-Bindung, Fact-Traces, Repair-Kontinuität, skalierte Batch-Distinctness; Einzelbatch ist gültig.
2. `controller.py`: feste Stufen `research -> facts -> context -> draft -> fullcheck -> repair`; Same-Article-Repair.
3. `design_guard.py`: generischer Beitragsart-Design-Hardlock ohne Beitragsart-Whitelist; keine Mutation.
4. `batch_repetition_guard.py`: Wiederholungsschutz für Multi-Artikel-Batches; Einzelbatch PASS ohne künstlichen Vergleich.
5. `batch_gate.py`: akzeptiert exakt die gebundene Snapshot-Menge; keine feste Zahl, keine Beitragsartbindung; übernimmt nur FULL-geprüfte Bytes.
6. `handoff_transport.py`: `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`; count `1..N`; keine Beitragsart-Whitelist; mehrteiliger V2-Inline-Transport statt festem Gesamt-60k-Umschlag.
7. Regressionstests: 1, mehrere, 25, 1000 sowie gemischte Beitragsarten und 0-Artikel-Negativfall.

## Unveränderte Fach-/Toolautoritäten
System 4 ersetzt diese Autoritäten nicht:
- PPM 6.7.9;
- LanguageTool 6.8 / Bestand 43;
- bestehende Textmaschine-/Artikeltyp-/Tabellen-/Link-/SEO-/PSERC-/PSTE-/Metadatenregeln;
- `publish_allowed=false`.

## Frischer finaler lokaler Preflight 2026-09-13
Belegdatei, ausdrücklich **keine zweite CURRENT_STATE**:
`isolated_system4/TESTNACHWEIS_20260913_UNIVERSAL_PREFLIGHT.md`

Die zuvor lokal fehlende PPM-6.7.9-ZIP wurde **nicht nachgebaut und nicht verändert**. Die historischen Original-Zwischendateien `ppm.00.b64` bis `ppm.06.b64` wurden aus der vorhandenen Dateibibliothek materialisiert, decodiert und gegen die historischen Git-Blob-SHAs der sieben Repo-Chunks geprüft. Alle sieben Chunk-Blob-SHAs stimmen exakt.

Das zusammengesetzte Paket ist exakt:
- Datei: `control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip`
- Größe: `1614485` Bytes;
- Git-Blob: `151e9d6f908453dfc5b4acb497c4927a3f03c940`;
- SHA256: `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`;
- ZIP-Integrität: PASS.

Danach frisch ausgeführt:
- kompletter aktueller Unittestbestand: **87/87 PASS**;
- lokaler E2E `test_local_end_to_end_chat_handoff.py`: **5/5 PASS**;
- NO-LEGACY über `production_checks.no_legacy_runtime_dependencies(...)`: **PASS**, `legacy_import_count=0`;
- Universalität 1 / 3 / 7 / 25 / 1000, gemischte/neue Beitragsarten und 0-Artikel-Negativfall bleiben PASS.

Der frühere lokale PPM-Materialisierungsblocker ist damit **geschlossen**. Es besteht aktuell **kein bekannter offener System-4-Code-/Preflight-Blocker**.

Beweisgrenze: Dies ist ein vollständiger **lokaler Preflight-PASS**, aber noch **kein echter Codex-Produktionsnachweis**. Ein realer Codex-Lauf darf erst nach ausdrücklicher Nutzerfreigabe gestartet werden.

## Reale Infrastrukturgrenze
System 4 enthält keine künstliche Artikelzahl-Obergrenze. Reale Laufzeit-, Speicher- und Chat-Ausgabelimits bleiben physische Infrastrukturgrenzen. Der V2-Handoff teilt große Daten in geordnete Transportteile. Bei einem realen Ressourcenblock muss der Lauf fail-closed mit dem konkreten Infrastrukturblocker stoppen; die gebundene Artikelmenge darf nicht willkürlich gekürzt werden.

## WordPress-/Handoff-Grenze
Der aktuelle direkte Importvertrag ist:
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- JSON / `application/json`;
- `WORDPRESS_DIRECT_IMPORT`;
- `Portal SEO Editorial Plan Compiler 0.28.23`;
- PPM 6.7.9;
- `direct_wordpress_upload_ready=true` nur nach allen System-4-PASS-Prüfungen;
- `publish_allowed=false`.

Die bestehende Signaturprüfung ist für diesen aktuellen Pfad ausgeschaltet. Deshalb kein Signing/ENDSTEMPEL in System 4. System 4 verändert weder Plugin noch Signaturschalter.

## HOBBYRAUM / NEXT ACTION
System-4-Arbeitsraum: **LOCAL PREFLIGHT PASS / wartet auf Nutzerfreigabe.**

Exakter nächster Arbeitsschritt:
1. **kein weiterer Umbau und kein Codex ohne Nutzerfreigabe**;
2. Nutzerfreigabe für **einen echten Codex-Lauf des konkret gebundenen Input-Batches** einholen;
3. Anzahl und Beitragsarten ausschließlich aus diesem gebundenen Input übernehmen;
4. Lauf fail-closed durch dieselbe System-4-Kette bis zum V2-Elternchat-/WordPress-Handoff führen;
5. weiterhin kein Merge und kein Publish ohne gesonderte Freigabe.

## Nicht anfassen
- `control/startmaster0107/**` und offizieller CURRENT_STATE;
- Textmaschine-/Content-Regelquellen;
- PPM-6.7.9-Paket und dessen Fachregeln;
- PSERC/PSTE-Fachregeln;
- WordPress-Plugin/Signaturschalter;
- Theme/CSS/Designplugin/Designselektoren;
- historische Konzepte 1–3 als Laufzeitabhängigkeit;
- Main/Merge/Publish.

## Historie
Historische Protokolle bleiben Historie und sind keine CURRENT-Quelle:
- `PROTOKOLL_CLOSEOUT_20260912.md`
- `PROTOKOLL_CLOSEOUT_20260912_HANDOFF_NACHTRAG.md`

Aktueller Nachhol-/Übergabestand dieses Arbeitsabschnitts:
- `PROTOKOLL_HANDOVER_20260913_CODEX_STRICT_PIPELINE.md`
