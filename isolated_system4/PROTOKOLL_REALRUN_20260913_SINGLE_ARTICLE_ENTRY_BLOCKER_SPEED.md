# SYSTEM 4 — REALRUN 1 ARTIKEL — ENTRY-BLOCKER + SPEED — 2026-09-13

Status dieses Dokuments: **Beleg-/Optimierungsprotokoll, keine zweite CURRENT_STATE**. Die aktuelle System-4-Statuswahrheit bleibt ausschließlich `isolated_system4/README.md`.

## Gebundener Realtest

Ausgangs-Head: `7e96ab85fa878b33642a110e7af67d1f0aeedf17`.

Gebundener Batch: exakt 1 Artikel.
- article_type: `Beratung`
- category: `putzbox-beratung`
- target_keyword: `Putzbox für Pferde`
- title: `Putzbox für Pferde richtig auswählen`
- plan_slot: `88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5`
- batch_sha256: `7b471ee2acef71531b067d2a8324a72580f4d9c8bc8d67412d021c1facf2e6e3`
- publish_allowed: `false`

Vor der Codex-Freigabe waren auf diesem System-4-Code lokal vollständig PASS:
- 87/87 Unittests;
- E2E 5/5;
- NO-LEGACY mit `legacy_import_count=0`;
- exakte PPM-6.7.9-Paketbindung;
- Universalität 1 / 3 / 7 / 25 / 1000 und gemischte/neue Beitragsarten.

Der Nutzer gab den ersten echten 1-Artikel-Codex-Produktionslauf ausdrücklich frei. Der Auftrag verlangte die vollständige System-4-Kette vom indexed ingress bis zum exakten V2-Elternchat-/WordPress-Handoff und verbot Legacy-Orchestrierung, direkte LT/PPM-Aufrufe, Repository-Handoff, Merge und Publish.

## Tatsächlicher Realrun-Befund

Codex-Auftrag erstellt: `2026-09-13T09:02:04Z`, PR-Kommentar `5652346738`.

Terminale Codex-Antwort: `2026-09-13T09:06:45Z`, PR-Kommentar `5652363154`.

Ergebnis:
- `SYSTEM4_HARD_BLOCKER:CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING`
- stage: `OFFICIAL_RUNTIME_ENTRY`
- source: `python3 control/output-quarantine/runtime_entry_gate.py`
- Codex bestätigt ausdrücklich: **keine Artikelrecherche und kein Draft gestartet**;
- keine Repository-Datei aus dem Produktionsauftrag verändert;
- deshalb kein System-4-ingress, kein Research, kein Fact-Pack, kein Draft, kein LT/PPM-Fullcheck, kein Batch-Gate und kein V2-Handoff;
- folglich **keine WordPress-Ausgabedatei** und **kein End-to-End-PASS**.

Gemessene Zeit bis zum Hard-Blocker: **281 Sekunden = 4:41 Minuten**. Diese Zeit erzeugte keinerlei Inhalts-/Qualitätsnachweis, weil der fachliche System-4-Lauf noch nicht begonnen hatte.

## Nachgewiesene Ursache

Repository-Root `AGENTS.md` gilt repositoryweit für Codex Cloud und verlangt vor jeder Suche/Analyse/Dateiöffnung zwingend die offizielle Cloud-Eingangstür.

Diese offizielle Strecke führt in `control/output-quarantine/runtime_entry_gate.py` / `worker_freshness_guard.py`. Der Freshness-Guard verlangt die lokale Datei `.pferde-environment/CODEX_PRODUCTION_PREFLIGHT.json`.

Der zugehörige Producer `control/startmaster0107/codex-production-runtime/codex_environment_preflight.py` verlangt wiederum, dass der lokale `HEAD` exakt dem autoritativen aktuellen `main` entspricht. Ein isolierter System-4-PR-Head kann diese Bedingung definitionsgemäß nicht zugleich erfüllen.

Damit besteht eine strukturelle Kollision:
- System 4 soll auf seinem isolierten, hashgebundenen PR-Head laufen und keinerlei Legacy-Orchestrierung als Laufzeitabhängigkeit besitzen;
- Codex Cloud liest aber repositoryweit zuerst die Root-Anweisung und wird dadurch an die offizielle STARTMASTER-/Runtime-Eingangsstrecke gebunden.

Der aktuelle Hard-Blocker liegt daher **vor System 4** und ist kein Artikel-, Textmaschine-, LT-, PPM-, Batch- oder Handoff-Fehler.

## Konsequenz für die Architektur

Dieser Befund ist für das Ziel „eine Tür / ein Wächter / keine Außenfreiheit“ kritisch: Die System-4-Tür ist innerhalb des aktuellen Repository-Roots nicht die erste Tür, die Codex sieht. Eine ältere repositoryweite Tür kann den Worker vor System 4 abfangen. Damit ist die gewünschte Isolation im echten Codex-Betrieb noch nicht bewiesen.

Nicht zulässige Scheinlösungen:
- den fehlenden Environment-Proof fälschen;
- den Freshness-Guard umgehen;
- den offiziellen STARTMASTER für System 4 passend machen;
- System 4 wieder an den alten STARTMASTER koppeln;
- Textmaschine/PPM/PSERC/PSTE/WordPress-Regeln lockern;
- den Codex-Hard-Blocker als PASS behandeln.

## Geschwindigkeitsprotokoll ohne Qualitätsverlust

### Beobachtet / gemessen

1. **281 Sekunden reine Eintrittszeit bis zum falschen Hard-Blocker.**
   - Qualitätsgewinn: keiner, da Research/Draft nicht gestartet wurden.
   - Priorität: sehr hoch.
   - Schluss: Der System-4-Produktionsworker darf nicht erst durch eine fremde Legacy-/offizielle Produktionsstrecke laufen müssen.

2. **Parent-seitiger Preflight war bereits vollständig grün.**
   - 87/87, E2E, NO-LEGACY und PPM-Bindung waren vor Codex ausgeführt.
   - Ein erneutes fachfremdes Produktions-Environment-Gating innerhalb Codex dupliziert Arbeit, ohne System-4-Qualität zu erhöhen.

### Potenzielle Optimierungen — nur wenn die Qualitätskette unverändert bleibt

A. **System 4 braucht einen echten eigenen Codex-Root/Einstieg.**
   Bevorzugte Richtung: eine technisch isolierte Codex-Ausführungswurzel, in der `isolated_system4/AGENTS.md` tatsächlich die oberste Worker-Anweisung ist und nur die explizit erlaubten, hashgebundenen Fach-/Toolinputs verfügbar sind. Die alte offizielle Root-Orchestrierung darf dort keine Laufzeitabhängigkeit sein. Das alte Produktionssystem bleibt unangetastet.

B. **Immutable Toolpakete vor dem Codex-Lauf hashgebunden bereitstellen und wiederverwenden.**
   PPM/LT dürfen gecacht werden, wenn und nur wenn Pfad/Version/SHA exakt gebunden bleiben. Dadurch entfällt Materialisierungs-/Startaufwand; Regeln und echte Ausführung bleiben unverändert.

C. **Keine erneute 87er-Preflight-Suite innerhalb eines unveränderten Codex-Heads.**
   Der Caller beweist den Head vorher. Codex produziert danach nur den gebundenen Artikelbatch. Bei Head-Änderung muss der Caller wieder frisch prüfen.

D. **Persistent LT-Worker innerhalb des einen `production_checks.run_all` beibehalten.**
   Er reduziert JVM-Startkosten, ohne LT-Regeln oder den Fullcheck zu umgehen. Direkte Vor-/Nachprüfungen bleiben verboten.

E. **Reparaturen weiterhin nur erster konkreter Defekt / gleicher Artikel.**
   Das vermeidet komplette Neuschreibungen. Qualitätsregel, Fact-Bindung und kompletter Fullcheck nach der Reparatur bleiben erhalten.

F. **Bei Multi-Artikel-Batches nur unabhängige Recherche/Artikel begrenzt parallelisieren.**
   Niemals abhängige Stufen, Prüfer oder den finalen Batch-Gate parallel überspringen. Für einen Einzelartikel bringt dies keinen Vorteil.

G. **Handoff genau einmal kanonisieren und packen.**
   Keine zusätzliche Transformation nach dem geprüften Artikel. Parent Chat entpackt und validiert nur; dadurch bleibt die WordPress-Datei bytegenau.

## Unveränderliche Qualitätsgrenze der Optimierung

Keine Geschwindigkeitsoptimierung darf entfallen, verkürzen oder lockern:
- frische echte Recherche;
- Research-Evidence;
- Fact-Evidence / Fact-Pack;
- Produktionskontext;
- Textmaschine-/Designregeln;
- LanguageTool 6.8;
- PPM 6.7.9;
- Same-Article-Repair-Bindung;
- Batch-Gate;
- V2-Handoff-Validierung;
- Parent-Chat-Rekonstruktion und erneute Validierung;
- `publish_allowed=false`.

## Aktueller Abschluss

Realrun 1 Artikel: **BLOCKED BEFORE SYSTEM-4 INGRESS**.

Kein Merge. Kein Publish. Keine WordPress-Datei erzeugt. Kein zweiter Codex-Produktionslauf gestartet.

Nächster technischer Klärpunkt ist ausschließlich die echte Codex-Eintrittsisolation. Erst nach deren belastbarer Lösung und neuem vollständigem parent-seitigem Preflight darf ein weiterer Codex-Produktionslauf nach den geltenden Freigaberegeln erfolgen.
