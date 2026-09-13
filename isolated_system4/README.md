# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED BEFORE SYSTEM-4 INGRESS / isolated prototype / test only.** Kein Merge, kein Produktions-Publish, kein weiterer Codex-Produktionslauf bis zur belastbaren Eintrittsisolation.

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

## Lokaler Preflight 2026-09-13
Belegdatei, ausdrücklich **keine zweite CURRENT_STATE**:
`isolated_system4/TESTNACHWEIS_20260913_UNIVERSAL_PREFLIGHT.md`

Vor dem echten Codex-Lauf wurden auf dem System-4-Code vollständig ausgeführt:
- kompletter aktueller Unittestbestand: **87/87 PASS**;
- lokaler E2E `test_local_end_to_end_chat_handoff.py`: **5/5 PASS**;
- NO-LEGACY: **PASS**, `legacy_import_count=0`;
- Universalität 1 / 3 / 7 / 25 / 1000, gemischte/neue Beitragsarten und 0-Artikel-Negativfall: PASS;
- PPM 6.7.9 exakt gebunden: Größe `1614485`, Git-Blob `151e9d6f908453dfc5b4acb497c4927a3f03c940`, SHA256 `acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1`, ZIP-Integrität PASS.

Damit bleibt bewiesen: Der **lokale System-4-Kern und seine komplette simulierte Eingang-bis-Handoff-Kette sind grün**. Dieser Beweis ersetzt aber keinen echten Codex-Produktionslauf.

## Erster echter 1-Artikel-Codex-Lauf — 2026-09-13
Beleg-/Optimierungsprotokoll:
`isolated_system4/PROTOKOLL_REALRUN_20260913_SINGLE_ARTICLE_ENTRY_BLOCKER_SPEED.md`

Gebundener Testartikel:
- `Beratung`;
- Titel `Putzbox für Pferde richtig auswählen`;
- Keyword `Putzbox für Pferde`;
- exakt 1 Item;
- `publish_allowed=false`.

Der Nutzer gab diesen echten Produktionsversuch ausdrücklich frei. Der Codex-Auftrag verlangte die vollständige System-4-Kette bis zum exakten V2-Elternchat-/WordPress-Handoff und verbot Legacy-Orchestrierung.

Tatsächliches Ergebnis:
- **BLOCKED BEFORE SYSTEM-4 INGRESS**;
- Codex stoppte bei `OFFICIAL_RUNTIME_ENTRY` mit `CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`;
- ausgeführte fremde Eintrittsstrecke: `control/output-quarantine/runtime_entry_gate.py`;
- Codex bestätigt: keine Artikelrecherche und kein Draft gestartet;
- deshalb kein Research-Evidence, Fact-Pack, Draft, LT/PPM-Fullcheck, Batch-Gate, V2-Handoff und keine WordPress-Datei.

Gemessene Zeit vom Codex-Auftrag bis zur terminalen Blockermeldung: **281 Sekunden / 4:41 Minuten**.

## Aktueller echte Blocker: S4-BLOCK-REAL-ENTRY
Die repositoryweite Root-`AGENTS.md` gilt für Codex Cloud **vor** der verschachtelten System-4-Anweisung und erzwingt die offizielle Cloud-/Runtime-Eingangstür.

Diese Strecke verlangt über `worker_freshness_guard.py` die Datei `.pferde-environment/CODEX_PRODUCTION_PREFLIGHT.json`. Der zugehörige Producer verlangt seinerseits, dass der lokale Checkout-HEAD exakt dem autoritativen aktuellen `main` entspricht.

Damit kollidieren zwei Bedingungen:
1. System 4 muss auf seinem isolierten, hashgebundenen PR-Head laufen und darf keine Legacy-/STARTMASTER-Orchestrierung als Laufzeitabhängigkeit übernehmen.
2. Die repositoryweite Codex-Root-Anweisung zieht den Worker vor System 4 in eine offizielle Produktionsstrecke, deren Environment-Proof auf exakt `main` gebunden ist.

Folge: **Die gewünschte echte „eine Tür / ein Wächter“-Isolation ist im realen Codex-Betrieb noch nicht erreicht**, obwohl der lokale System-4-Kern grün ist.

Nicht als Lösung zulässig:
- Environment-Proof fälschen;
- offiziellen Freshness-/Runtime-Guard umgehen oder abschwächen;
- System 4 an STARTMASTER koppeln;
- offiziellen CURRENT_STATE für System 4 ändern;
- den Blocker als PASS behandeln.

## Geschwindigkeitsbefund ohne Qualitätsverlust
Der erste reale Befund ist eindeutig: **4:41 Minuten wurden vor dem System-4-ingress verbraucht, ohne einen einzigen fachlichen Qualitätsnachweis zu erzeugen.** Die wichtigste Optimierung ist deshalb nicht ein schnellerer Text oder weniger Prüfung, sondern ein eigener echter System-4-Codex-Einstieg ohne fremde Orchestrierungsrunde.

Weitere Optimierungen bleiben nur unter unveränderter Qualitätskette zulässig:
- PPM/LT nur hashgebunden cachen/wiederverwenden;
- den bereits caller-seitig bewiesenen unveränderten Head nicht erneut komplett innerhalb Codex preflighten;
- persistenten LT-Worker innerhalb `production_checks.run_all` nutzen;
- Reparaturen nur erster konkreter Defekt / gleicher Artikel statt Komplettneuschreibung;
- bei Multi-Artikel-Batches nur voneinander unabhängige Recherche/Artikel begrenzt parallelisieren;
- Handoff einmal kanonisieren/packen und im Parent Chat nur entpacken + erneut validieren.

**Niemals** zur Beschleunigung entfallen oder gelockert werden dürfen Recherche, Fact-Bindung, Textmaschine/Design, LT 6.8, PPM 6.7.9, Same-Article-Repair, Batch-Gate, V2-Handoff oder Parent-Chat-Validierung.

## Reale Infrastrukturgrenze
System 4 enthält keine künstliche Artikelzahl-Obergrenze. Reale Laufzeit-, Speicher- und Chat-Ausgabelimits bleiben physische Infrastrukturgrenzen. Der V2-Handoff teilt große Daten in geordnete Transportteile. Bei einem realen Ressourcenblock muss der Lauf fail-closed mit dem konkreten Infrastrukturblocker stoppen; die gebundene Artikelmenge darf nicht willkürlich gekürzt werden.

## WordPress-/Handoff-Grenze
Der Zielvertrag bleibt:
- `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`;
- JSON / `application/json`;
- `WORDPRESS_DIRECT_IMPORT`;
- `Portal SEO Editorial Plan Compiler 0.28.23`;
- PPM 6.7.9;
- `direct_wordpress_upload_ready=true` nur nach allen realen System-4-PASS-Prüfungen;
- `publish_allowed=false`.

Die bestehende Signaturprüfung ist für diesen Pfad ausgeschaltet. Deshalb kein Signing/ENDSTEMPEL in System 4.

## HOBBYRAUM / NEXT ACTION
System-4-Arbeitsraum: **BLOCKED am echten Codex-Einstieg.**

Exakter nächster Arbeitsschritt:
1. keinen zweiten Codex-Produktionslauf starten;
2. die Codex-Eintrittsarchitektur so isolieren, dass der System-4-Worker tatsächlich zuerst und ausschließlich seine System-4-Tür sieht, ohne das alte Produktionssystem zu verändern oder dessen Schutzregeln abzuschwächen;
3. Lösung hart positiv/negativ lokal prüfen;
4. danach vollständigen parent-seitigen Preflight auf dem dann aktuellen Head erneut ausführen;
5. erst dann nach den geltenden Freigaberegeln einen weiteren echten Codex-Produktionslauf ausführen;
6. Ziel bleibt die komplette Kette bis zur bytegenau validierten `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json` hier im Chat.

## Nicht anfassen
- `control/startmaster0107/**` und offizieller CURRENT_STATE;
- repositoryweite alte Produktionsschutzlogik als Scheinlösung lockern;
- Textmaschine-/Content-Regelquellen;
- PPM-6.7.9-Paket und dessen Fachregeln;
- PSERC/PSTE-Fachregeln;
- WordPress-Plugin/Signaturschalter;
- Theme/CSS/Designplugin/Designselektoren;
- historische Konzepte 1–3 als System-4-Laufzeitabhängigkeit;
- Main/Merge/Publish.

## Historie
Historische Protokolle bleiben Historie und sind keine CURRENT-Quelle:
- `PROTOKOLL_CLOSEOUT_20260912.md`
- `PROTOKOLL_CLOSEOUT_20260912_HANDOFF_NACHTRAG.md`

Aktueller Nachhol-/Übergabestand dieses Arbeitsabschnitts:
- `PROTOKOLL_HANDOVER_20260913_CODEX_STRICT_PIPELINE.md`
