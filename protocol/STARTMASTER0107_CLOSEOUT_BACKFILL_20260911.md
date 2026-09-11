# STARTMASTER0107 – Closeout-/Nachholprotokoll 2026-09-11

**STATUS DIESER DATEI:** HISTORISCHES WAS/WARUM-/TESTPROTOKOLL. **KEINE CURRENT-AUTORITÄT.** Aktueller Zustand ausschließlich in `control/startmaster0107/CURRENT_STATE.json`.

## Anlass

Nach Abschlussprüfung des Chats wurde festgestellt, dass `CURRENT_STATE.json` noch den Stand nach PR230 (`66c4224d...`) führte, obwohl danach weitere KISS-Reparaturen, reale Livetests und neue Befunde erfolgt waren. Dieses Protokoll holt ausschließlich die tatsächlich ausgeführten Änderungen und Befunde nach. Es erzeugt keine zweite Standwahrheit.

## Tatsächlich ausgeführte Änderungen seit dem bisherigen Protokoll

### PR236 – gebundene Fachworkflow-Arbeit wieder vollständig ausführen

- PR236 wurde gemergt; Merge-Commit `b705f78e26bcc62dda0adda31ad0d181438f6f19`.
- Ursache: Die Worker-/Prüfergrenze war durch PR217 so verschoben worden, dass der Worker nur noch unvollständige Rohprodukte erzeugen sollte.
- KISS-Eingriff: ausschließlich die bestehende 107007-Arbeitsanweisung wieder auf vollständige Ausführung der bereits gebundenen Textmaschinen-/Fachworkflow-Regeln verpflichtet.
- Unverändert: `stage_proofs=[]`, Worker besitzt keine PASS-Autorität; keine Textmaschinen-, PPM-, PSERC-, PSTE-, LanguageTool-, SEO-, Design- oder Publish-Regel geändert.
- GitHub-Nachweis auf PR236-Head `621ecb7a141c05e3b149d7e437781fb81ba2d758`: Deterministic Entrance Gate = SUCCESS; Immutable Base Hardlock = SUCCESS.

### PR237 – production_plan_header wieder aus dem aktuellen Fachworkflow

- PR237 wurde gemergt; Merge-Commit `c2258ead34b506d0b06f85e639e1d776ee5268cf`.
- Belegte Ursache: der bewusst fachlich leere H8-Bootstrap-Header war später fälschlich als produktiver PPM-`production_plan_header` verwendet worden. Daraus entstand `PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH`.
- KISS-Eingriff: H8 bleibt reine Herkunfts-/Türbindung; `production_plan_header` wird im aktuellen gebundenen Fachworkflow erzeugt und anschließend vom unveränderten PPM/PSERC geprüft.
- Keine Fach-, Inhalts-, PPM-, PSERC-, PSTE-, LanguageTool-, SEO-, Link-, Tabellen-, Design- oder Publish-Regel geändert.
- GitHub-Nachweis auf PR237-Head `2eed5e5d1f12371abdd1a1dd48e2876639b69d3c`: Deterministic Entrance Gate = SUCCESS; Immutable Base Hardlock = SUCCESS.

### PR243 – bestehenden PPM-Fact-Pack-Vertrag vollständig binden

- PR243 wurde gemergt; Merge-Commit und aktueller Main `bb005a5324a0a6270aacb52b5927613bde1ab4bc`.
- Belegter Liveblocker vor dem Fix: `BLOCKED_FACT_PACK_IMPORT_ITEM_INVALID`.
- KISS-Eingriff: Der bestehende 107007-Fachworkflow muss im realen `fact_pack` die bereits von PPM 6.7.9 verlangten Felder `status=SOURCE_VERIFIED_PRODUCTION_READY` und `claims` als Array erzeugen.
- H8 und Handoff ergänzen diese Fachfelder nicht. Keine PPM-/PSERC-/PSTE-/Textmaschinen-/Inhalts-/SEO-/Link-/Tabellen-/Design-/Publish-Regel geändert.
- GitHub-Nachweis auf PR243-Head `ee66c991c3e22da4c5e7d8bff19b92a6b51fea47`: Deterministic Entrance Gate = SUCCESS; Immutable Base Hardlock = SUCCESS.

## Tatsächliche Livetests und Fehlerstatus

1. Auf aktuellem Main `bb005a53...` blockierte ein erster frischer 7/7-Versuch vor der Recherche mit `REAL_RESEARCH_FACT_PACK_SOURCE_ACCESS_UNAVAILABLE`, weil die damals verwendete Web-Recherche-Schnittstelle `HTTP 401 Unauthorized` lieferte.
2. Eine Read-only-Prüfung zeigte: Der Fachworkflow verlangt reale belegbare Quellen, ist aber nicht ausdrücklich an `web.run/search_query` gebunden. Es wurde keine neue API und keine Ersatzarchitektur eingebaut.
3. Ein anschließender unveränderter Main-Livetest konnte reale Quellen recherchieren und den **ersten frischen Artikel tatsächlich erzeugen**. Damit ist der 401-Befund **nicht mehr der aktuelle Projektblocker**.
4. Derselbe erste frische Artikel erreichte den realen PPM-6.7.9-/PSERC-Handoff und blockierte dort mit `PPM679_REAL_EXECUTION_BLOCKED` / `FACHWORKFLOW_PROOF_HANDOFF_BLOCKED`.
5. Der erste verschachtelte PPM-Grund ist weiterhin **nicht bekannt**. Er darf nicht geraten werden.
6. Der unmittelbar danach gestartete Read-only-Auftrag, exakt diesen verschachtelten Grund aus denselben Task-Artefakten auszulesen, konnte nicht ausgeführt werden, weil Codex Cloud `You have reached your Codex usage limits` meldete. Das ist ein **externer Ausführungsverfügbarkeitsblocker**, kein neuer Fach-/Projektfehler.
7. 107008 wurde nicht erreicht. Kein Publish und keine WordPress-Schreibaktion.

Erster gebundener Artikel des aktuellen Batches:
- Titel: `Das Wichtigste über Hindernisstangen für Pferde`
- Target Keyword: `Hindernisstangen für Pferde`
- Der exakt im letzten Codex-Task erzeugte Artikel wurde nicht dauerhaft im Repository materialisiert und darf daher nicht aus alten Recovery-Dateien ersetzt werden.

## Neuer technischer Befund – Sichtbarkeit, noch NICHT repariert

Im aktuellen `fachworkflow_proof_handoff.py` wird ein nicht reparierbarer innerer PPM-/PSERC-Bridge-Fehler weiterhin zu dem generischen `PPM679_REAL_EXECUTION_BLOCKED` zusammengezogen. Dadurch ist der reale innere Grund im Terminal nicht sichtbar.

**Status:** erkannt, aber wegen Benutzer-Freeze und Codex-Limit **nicht geändert**.

Dafür wurde ausschließlich der leere isolierte Branch `hobbyroom/ppm-inner-reason-visibility-20260911` auf aktuellem Main angelegt. Auf diesem Branch wurde keine funktionale Datei geändert.

## Eingefrorener Arbeitsstand / NEXT ACTION

Benutzerentscheidung: Stand einfrieren, bis Codex wieder verfügbar ist.

Aktive Arbeit:
- Main: `bb005a5324a0a6270aacb52b5927613bde1ab4bc`
- PR107 permanenter Dispatcher: Head exakt auf demselben Main; nicht mergen.
- Hobbyraum: `hobbyroom/ppm-inner-reason-visibility-20260911`
- Status: BLOCKED wegen `CODEX_USAGE_LIMIT_REACHED`, nicht wegen eines neuen nachgewiesenen Projektfehlers.

Nächster zulässiger Schritt nach Freigabe von Codex:
1. Zuerst exakt den bereits gestellten **Read-only-Auftrag** auf denselben ersten Artikel/Task wiederholen und den ersten verschachtelten PPM-Grund auslesen. Keine Codeänderung, kein neuer Artikel, kein neuer 7/7-Lauf.
2. Nur falls die alten Task-Artefakte nicht mehr verfügbar sind: auf dem bestehenden Hobbyraumbranch ausschließlich die kleinste Observability-Korrektur bauen, die den vorhandenen inneren PPM-/PSERC-Code sichtbar macht, während der Handoff unverändert BLOCKED bleibt. Positive/negative Prüfung + bestehende Hashkette + beide Hardlocks vor Merge.
3. Danach nur den bewiesenen Root Cause reparieren.
4. Zuerst **einen** frischen Artikel vollständig durch real LanguageTool + real PPM bringen. Erst danach Restbatch bis 7/7 und 107008. Vor Publish stoppen.

## Tatsächlich ausgeführte Prüfungen / ausdrücklich NICHT als PASS gewertet

Ausgeführt und persistent belegt:
- PR236: Deterministic Entrance Gate SUCCESS; Immutable Base Hardlock SUCCESS.
- PR237: Deterministic Entrance Gate SUCCESS; Immutable Base Hardlock SUCCESS.
- PR243: Deterministic Entrance Gate SUCCESS; Immutable Base Hardlock SUCCESS.
- Mehrere reale 107007-Livetests über PR107 bis zu den jeweils beschriebenen echten Blockern.
- Letzter Lauf: erster frischer Artikel recherchiert/erzeugt, realen PPM erreicht, dort BLOCKED.

Nicht als aktueller Produktions-PASS ausgeführt/belegt:
- kein 7/7-PASS auf aktuellem Main;
- 107008 nicht erreicht;
- kein Publish;
- kein aktueller vollständiger M01-M33-Lauf wird für den Endstatus als Produktionsbeweis herangezogen;
- der verschachtelte aktuelle PPM-Grund wurde wegen Codex-Limit noch nicht ausgelesen.

## Ziel / Architektur / eine Wahrheit

- Zielvertrag `control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json` blieb unverändert.
- Keine neue Architektur wurde als verbindlicher Standard eingeführt.
- Die in diesem Chat diskutierte allgemeine Idee „Prüfer soll den produktiven Weg nicht neu definieren“ wurde **nicht** als neue Campus-Architektur umgesetzt. Tatsächlich gebaut wurden nur lokale minimale STARTMASTER0107-Bindungskorrekturen.
- Deshalb keine Campus-Neubauvorlage oder allgemeiner Standard geändert.
- Autoritative CURRENT-Wahrheit bleibt ausschließlich `control/startmaster0107/CURRENT_STATE.json`.
- `PFERDE_ATELIER_START_HERE.json` und `control/CURRENT_STARTMASTER.json` bleiben nur Wegweiser.
- Dieses und ältere Protokolle sind historische WAS/WARUM-/Testnachweise, keine CURRENT-Autorität.
- PR231 `System 3` bleibt strikt separater Draft-Parallelweg und wurde nicht verändert.
- Der permanente PR107 ist ausschließlich Dispatcher und besitzt keine Fach-/State-/Publish-Autorität.

## Archiv / Nebenmutationen

- Ältere Blocker `PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH` und `BLOCKED_FACT_PACK_IMPORT_ITEM_INVALID` sind durch PR237 bzw. PR243 abgelöst und nur noch Historie.
- Der frühere Recherche-401 ist durch den nachfolgenden erfolgreichen Recherche-/Erzeugungslauf als aktueller Projektblocker abgelöst; er bleibt historischer Livebefund.
- Versehentlich angelegtes GitHub-Issue #244 wurde sofort als `not_planned` geschlossen und ausdrücklich als ohne Projektaktion/-anforderung markiert. Es besitzt keine Autorität.

## NICHT ANFASSEN

Textmaschine; Inhalts-/Qualitätsregeln; PPM-6.7.9-Regeln; PSERC; PSTE; LanguageTool-Regeln; SEO/Links/Tabellen/Dubletten/Design; WordPress-Fachlogik; Endstempel-/Publish-Sicherheit; Cloud Entry; Single-Door-Navigation; H8-Fachblindheit. Kein Worker-PASS. `publish_allowed=false`.
