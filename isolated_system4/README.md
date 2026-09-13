# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED / isolated prototype / test only.** Kein Merge, kein Produktions-Publish, kein neuer Codex-Produktionslauf.

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit** innerhalb des isolierten Prototyps. Der offizielle Projekt-/Campus-Stand bleibt davon getrennt in `control/startmaster0107/CURRENT_STATE.json` und wird durch System 4 nicht überschrieben.

## Verbindlicher Zielvertrag
`isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`

Kurzform:
`gebundene Metadaten -> Codex recherchiert -> Codex bildet Fakten/Fact-Pack -> Codex schreibt -> unveränderte echte Prüfer -> gezielte Same-Article-Reparatur -> Batch-/Wiederholungsprüfung -> exakter Chat-/WordPress-Handoff`

Codex bleibt der eine fachliche Worker. System 4 übernimmt **nicht** die alte Legacy-Orchestrierung.

## Neue universelle Produktionsgrenze
Der frühere aktuelle Zustand „genau sieben `Beratung`-Artikel“ ist **entfernt**.

Verbindlich gilt jetzt:
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

`design_guard.py` ist ausschließlich PASS/BLOCK und verändert keine Bytes. Die `ppm-type-*`-Bindung wird aus dem gebundenen `article_type` generisch abgeleitet. Bekannte typspezifische Regeln (z. B. Beratung-H2) bleiben nur für ihren Typ aktiv und sind keine Zulassungsliste.

## Aktuell umgesetzte System-4-Schutzkette
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

## Aktuelle Fehler / Blocker
### S4-BLOCK-01 — kompletter aktueller Testbestand auf finalem Head noch offen
Die universelle Mengen-/Beitragsartkorrektur wurde lokal in Teil- und Skalierungstests positiv geprüft. Der vollständige Branch muss nach Abschluss aller Dokument-/Testbindungen erneut bytegenau lokal rekonstruiert und mit
`python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v`
auf dem **dann finalen Head** ausgeführt werden.

Folge: **System-4-Gesamt-PASS bleibt bis dahin OFFEN. Kein Codex-Produktionslauf.**

### S4-BLOCK-02 — kompletter lokaler E2E auf finalem Head noch offen
Der End-to-End-Test muss nach Abschluss der V2-/Universalbindung auf demselben finalen Head erneut positiv und negativ laufen, inklusive Elternchat-Handoff.

### S4-BLOCK-03 — Transportressourcen sind real endlich
System 4 enthält keine künstliche Artikelzahl-Obergrenze. Reale Laufzeit-, Speicher- und Chat-Ausgabelimits bleiben physische Infrastrukturgrenzen. Der V2-Handoff teilt große Daten in geordnete Transportteile, damit keine feste einzelne 60k-Gesamtgrenze mehr die Produktionsmenge definiert. Ein tatsächlicher Produktionslauf darf deshalb nie aus einer willkürlichen System-4-Zahl heraus gekürzt werden; bei realem Ressourcenblock muss er fail-closed mit dem konkreten Infrastrukturblocker stoppen.

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
System-4-Arbeitsraum: **BLOCKED bis frischer Gesamt-Testnachweis**.

Exakter nächster Arbeitsschritt:
1. aktuellen PR-Head nach den Universaländerungen binden;
2. **kein Codex**;
3. vollständigen aktuellen `isolated_system4/**`-Stand lokal bytegenau rekonstruieren;
4. kompletten Unittestbestand + NO-LEGACY + lokalen E2E positiv/negativ auf exakt diesem Head ausführen;
5. jeden tatsächlichen FAIL nur an seiner ersten Ursache im isolierten System-4-Code reparieren;
6. nach jeder Änderung den gesamten Testbestand auf dem neuen Head wiederholen;
7. erst bei vollständigem PASS README/Protokoll auf PASS aktualisieren;
8. danach Nutzerfreigabe für **einen echten Codex-Lauf des konkret gebundenen Input-Batches** einholen. Anzahl und Beitragsarten kommen ausschließlich aus diesem Input.

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
