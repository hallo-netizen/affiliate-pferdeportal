# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED / isolated prototype / test only.** Kein Merge, kein Produktions-Publish, kein neuer Codex-Produktionslauf.

Diese Datei ist die **eine aktuelle System-4-Statuswahrheit** innerhalb des isolierten Prototyps. Der offizielle Projekt-/Campus-Stand bleibt davon getrennt in `control/startmaster0107/CURRENT_STATE.json` und wird durch System 4 nicht überschrieben.

## Verbindlicher Zielvertrag
Aktueller System-4-Zielvertrag:

`isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`

Kurzform:

`Thema/Metadaten -> Codex recherchiert -> Codex bildet Fakten/Fact-Pack -> Codex schreibt -> unveränderte echte Prüfer -> gezielte Same-Article-Reparatur -> Batch-/Wiederholungsprüfung -> exakter Chat-/WordPress-Handoff`

Codex bleibt der eine fachliche Worker. System 4 übernimmt **nicht** die alte Legacy-Orchestrierung.

## Unverhandelbare Grenzen
### Textmaschine
Die bestehende Textmaschine und ihre Regeln sind READ-ONLY. System 4 darf sie weder direkt noch indirekt ändern, erweitern, abschwächen, neu interpretieren, normalisieren, ersetzen oder durch eigene Schreibregeln überschatten.

### Design
PPM 6.7.9, bestehender Artikel-/Tabellenvertrag, WordPress-Plugin, Theme/CSS und vorhandene Designselektoren sind READ-ONLY. System 4 darf weder direkt noch indirekt CSS, Inline-Styles, Klassen, Überschriftenhierarchie, Tabellenformatierung oder Theme-/Plugin-Dateien verändern. Nach dem geprüften Artikel ist keinerlei HTML-/Designtransformation erlaubt.

`design_guard.py` ist ausschließlich ein PASS/BLOCK-Guard und verändert keine Bytes. Wenn ein Fix eine Textmaschinen- oder Designänderung voraussetzen würde, lautet der Status `BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE`.

## Aktuell umgesetzte System-4-Schutzkette
Der frühere Stand „nur Handoff-Reparatur, Produktionskern unverändert“ ist überholt.

Im isolierten System-4-Prototyp wurden nach der Ursachenanalyse zusätzliche **äußere Kontrollgrenzen** eingebaut, ohne die bestehende Textmaschine oder das Design zu verändern:

1. `content_guard.py`
   - strukturierte Research-Evidence;
   - reale Quelle/URL/Evidence/Hash;
   - Fact-Evidence muss tatsächlich im gespeicherten Quellenausschnitt vorkommen;
   - Fact-Pack muss zu akzeptierter Recherche/Faktenbasis passen;
   - Artikel-Fact-IDs müssen im gebundenen Pack existieren;
   - Repair-Kontinuität;
   - artikelübergreifende Distinctness.
2. `controller.py`
   - feste Stufen `research -> facts -> context -> draft -> fullcheck -> repair`;
   - keine nächste Stufe bei ungültiger Evidence;
   - Same-Article-Repair, keine breite Neufassung im Repair-Pfad;
   - Design-/Content-Guard vor FULL-Produktion.
3. `design_guard.py`
   - validiert ausschließlich den bereits bestehenden Produktions-/Designvertrag;
   - keine Mutation/kein Restyling.
4. `batch_repetition_guard.py`
   - erkennt lange identische Satzschablonen über mehrere Artikel;
   - nur Batch-/Release-Integrität, keine neue Autorenregel.
5. `batch_gate.py`
   - übernimmt nur bereits FULL-geprüfte Artikel;
   - prüft Fact-/Designbindung und artikelübergreifende Wiederholung erneut;
   - schreibt die Artikelbytes unverändert.
6. `handoff_transport.py`
   - letzte fail-closed Wiederholungsprüfung von Fact-Pack, Design, Batch-Distinctness/Repetition, Hashes und WordPress-Handoff;
   - kanonischer Inline-Transport zum Elternchat;
   - direkter Importvertrag derzeit `Portal SEO Editorial Plan Compiler 0.28.23`.
7. Tests
   - Positiv-/Negativtests für Research/Facts, Design, Batch, Repair, Handoff und lokalen End-to-End-Weg sind im Repository angelegt/aktualisiert.
   - alte 0.28.22-Testbindungen wurden auf die aktuelle Handoff-Autorität 0.28.23 nachgeführt.

## Unveränderte Fach-/Toolautoritäten
System 4 ersetzt diese Autoritäten nicht:
- PPM 6.7.9;
- LanguageTool 6.8 / Bestand 43;
- bestehende Textmaschine-/Artikeltyp-/Tabellen-/Link-/SEO-/PSERC-/PSTE-/Metadatenregeln;
- `publish_allowed=false`.

Der vorhandene erfolgreiche erste FULL-RULE-System-4-Einzelartikel bleibt historischer Beleg dafür, dass Codex im Einzelweg gute Texte unter diesen Regeln erzeugen kann. Er ist **kein Freigabenachweis** für den jetzt veränderten aktuellen Head.

## Aktuelle Fehler / Blocker
### S4-BLOCK-01 — frischer kompletter System-4-Testlauf fehlt
Nach den aktuellen Änderungen wurde in diesem Chat **kein kompletter lokaler**

`python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v`

gegen den exakt aktuellen Branch-Head ausgeführt. Der Container konnte das GitHub-Repository wegen fehlender Netzauflösung nicht klonen. Der erfolgreiche GitHub-`hardlock-base`-Workflow prüft die allgemeine unveränderliche Basis, aber **nicht** den `isolated_system4`-Unittestbestand.

Folge: **System-4-Gesamt-PASS ist OFFEN.** Kein Codex-Produktionslauf erlaubt.

### S4-BLOCK-02 — echter End-to-End-Produktionsweg noch nicht neu bewiesen
Der lokale E2E-Test ist vorhanden, aber nach den aktuellen Guards/Bindungsänderungen noch nicht frisch ausgeführt. Insbesondere ist noch nicht neu bewiesen, dass der aktuelle Code auf einem vollständigen lokalen Checkout vom Codex-Einstieg bis zur bytegleichen rekonstruierten Elternchat-/WordPress-JSON positiv durchläuft und die relevanten Negativfälle blockiert.

Folge: **Produktionsfreigabe bleibt BLOCKED.**

## WordPress-/Handoff-Grenze
Der aktuelle direkte Importvertrag ist:
- JSON / `application/json`;
- `WORDPRESS_DIRECT_IMPORT`;
- `Portal SEO Editorial Plan Compiler 0.28.23`;
- PPM 6.7.9;
- `direct_wordpress_upload_ready=true` nur nach allen System-4-PASS-Prüfungen;
- `publish_allowed=false`.

Die bestehende Signaturprüfung ist für diesen aktuellen Pfad ausgeschaltet. Deshalb kein Signing/ENDSTEMPEL in System 4. System 4 verändert weder Plugin noch Signaturschalter.

## HOBBYRAUM / NEXT ACTION
System-4-Arbeitsraum: **BLOCKED bis frischer Testnachweis**.

Exakter nächster Arbeitsschritt im neuen Chat:
1. PR #238 / Branch `hobbyroom/system4-true-single-room-v1` frisch lesen und aktuellen Head ermitteln.
2. **Kein Codex.** Zuerst den vollständigen aktuellen Branch lokal verfügbar machen.
3. Auf exakt diesem Head ausführen:
   - kompletten `isolated_system4`-Unittestbestand;
   - NO-LEGACY-Proof;
   - `test_local_end_to_end_chat_handoff.py` positiv und negativ;
   - relevante Guards separat nur zur Fehlerlokalisierung, falls der Gesamtlauf fehlschlägt.
4. Jeden tatsächlichen FAIL auf seine erste Ursache zurückführen und nur im isolierten System-4-Code reparieren. Keine Textmaschinenregel und kein Design verändern.
5. Nach jeder Änderung den **gesamten** System-4-Testbestand erneut auf dem neuen Head ausführen.
6. Erst wenn alles auf demselben Head PASS ist, Tests/Status/Protokoll aktualisieren.
7. Danach stoppen und Nutzerfreigabe für **einen** echten Codex-7/7-Produktionslauf einholen. Ohne diese ausdrückliche Freigabe keinen Codex-Lauf starten.

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
