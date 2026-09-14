# PROTOKOLL / ÜBERGABE — SYSTEM 4 CODEX STRICT PIPELINE — 2026-09-13

Status dieses Dokuments: **ABSCHLUSS-/NACHHOLPROTOKOLL DES AKTUELLEN CHATS**. Es ist kein zweiter CURRENT_STATE. Die eine aktuelle System-4-Statuswahrheit liegt in `isolated_system4/README.md`. Der offizielle Projekt-/Campus-CURRENT_STATE bleibt `control/startmaster0107/CURRENT_STATE.json` und wurde nicht verändert.

## A. Ausgangslage und gesicherter Befund
Der Nutzer hat die seit langem unveränderten fachlichen Textregeln ausdrücklich als funktionierend bestätigt. Historische gute Chat-Produktion und ein guter System-4-Einzeltest zeigen, dass die Regeln selbst nicht als Ursache des schlechten 7er-Laufs behandelt werden dürfen.

Die Forensik dieses Chats hat zwei getrennte Fehlerklassen des schlechten System-4-7er-Laufs herausgearbeitet:

1. **Recherche-/Faktenstufe:** Der schlechte Lauf erzeugte generische, selbstzertifizierte Fakten/Fact-Packs mit synthetischen Quellenbezeichnern. Der bisherige Controller prüfte Research/Facts strukturell zu schwach; gute Einzeltests konnten trotzdem funktionieren, weil der Worker dort gute Eingaben geliefert hatte.
2. **Artikelübergreifende Schreibstufe:** Auch korrekte Fakten garantieren keinen individuellen Text. Der 7er-Lauf wiederholte Satz- und Absatzschablonen über verschiedene Artikel. Die vorhandenen Einzelartikelprüfungen sahen jeweils nur einen Artikel und konnten diese Batch-Wiederholung nicht zuverlässig als artikelübergreifenden Fehler erkennen.

Daraus folgt ausdrücklich **nicht**, dass die bestehende Textmaschine geändert werden muss. Die Lösung liegt in der strengeren Bindung und Prüfung des Workers und des Batch-/Releasewegs.

## B. Verbindliches Konzept / Ziel
Der fachliche Arbeiter bleibt **Codex** und führt weiterhin die komplette fachliche Kette selbst aus:

`Thema/Metadaten -> Recherche -> Fakten/Fact-Pack -> Schreiben -> Prüfen -> gezielte Reparatur`

Das ist konzeptionell die Übertragung des früher funktionierenden Chat-Arbeitsprinzips auf Codex. Neu ist nur, dass die Maschine nicht darauf vertraut, dass der Worker sich freiwillig in der Spur hält.

### Unverhandelbar
- Textmaschine und bestehende fachliche Regeln bleiben READ-ONLY.
- Design, Theme/CSS, Plugin, vorhandene Klassen/Selektoren und bestehender Produktions-/Tabellenvertrag bleiben READ-ONLY.
- Kein Legacy-Orchestrator wird zurückgeholt.
- Kein zweiter Chat-Schreiber oder Faktenlieferant wird eingeführt.
- Guards dürfen nur PASS/BLOCK liefern, nicht schreiben, stylen oder Fachregeln ersetzen.
- `publish_allowed=false`.
- Kein Merge, kein Publish, kein Codex-Lauf ohne neue ausdrückliche Nutzerfreigabe.

Der verbindliche statische Zielvertrag ist jetzt:
`isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`.

## C. Umsetzung dieses Chats
### 1. Research-/Fact-Bindung
`content_guard.py` wurde eingeführt/verschärft:
- `SYSTEM4_RESEARCH_EVIDENCE_V1` verlangt echte Source-Metadaten, URL, Evidence und Hash.
- `SYSTEM4_FACTS_EVIDENCE_V1` verlangt source-gebundene Claims.
- `evidence_text` muss nach Normalisierung tatsächlich im gespeicherten Source-Evidence vorkommen.
- Fact-Pack muss akzeptierte Quellen/Evidence und Kernclaims unverändert weitertragen.
- quellenlose/self-certified Packs werden blockiert.
- Artikel-Fact-IDs müssen im gebundenen Fact-Pack existieren.

### 2. Controller-Reihenfolge
`controller.py` bindet jetzt die Stufen fail-closed:
`ingress -> research -> facts -> context -> draft -> fullcheck -> repair/fullcheck`.

Die Research-/Facts-/Context-Stufen können nicht mehr nur durch beliebigen Mindesttext passiert werden. Der Draft wird gegen den gebundenen Faktkontext geprüft. Repair bleibt derselbe Artikel; breite Neufassungen werden über Kontinuität blockiert.

### 3. Design-Hardlock ohne Designänderung
Nach ausdrücklicher Nutzerregel wurde `design_guard.py` ergänzt.

Er **ändert nichts**, sondern blockiert vor WordPress u. a.:
- fehlende bestehende Produktionsklasse `ppm-generated`;
- falsche/fehlende bestehende Artikeltypklasse;
- falsches `data-article-type`;
- driftende Tabellenklassen gegenüber `system-129-table comparison-table`;
- Inline-/globale Styles, aktive HTML-Payloads;
- für Beratung abweichende H3/H1/H4-H6-Zwischenüberschriften gegenüber dem bestehenden H2-Designpfad.

Damit wird der dokumentierte historische Designfehler nicht durch Restyling repariert, sondern fail-closed verhindert.

### 4. Artikelübergreifende Wiederholung
Zwei reine Release-/Batch-Integritätsprüfungen wurden gebunden:
- Shingle-/Ähnlichkeitsprüfung in `content_guard.py`;
- konkrete wiederholte Langsatzprüfung in `batch_repetition_guard.py`.

Beide mutieren keinen Artikel und sind ausdrücklich **keine neue Textmaschinen-/Autorenregel**. Sie sollen nur verhindern, dass sieben einzeln akzeptierte, aber untereinander offensichtlich schablonenhafte Artikel als Batch freigegeben werden.

### 5. Batch und finaler Handoff
`batch_gate.py` prüft die gebundenen Artikel/Fact-/Design-/Batchbedingungen erneut und übernimmt die Artikelbytes unverändert.

`handoff_transport.py` prüft am letzten Ausgang nochmals:
- Body-Hash;
- Fact-Pack/Fact-Traces;
- Designneutralität;
- Batch-Distinctness und Satzwiederholung;
- LT-/PPM-PASS-Belege;
- WordPress-Direktimportvertrag;
- kanonischen Inline-Transport zum Elternchat.

Die aktuell gebundene Direct-Import-Version ist `Portal SEO Editorial Plan Compiler 0.28.23`. Eine im Closeout gefundene veraltete 0.28.22-Bindung in aktuellem Produktionsauftrag/Testfixtures wurde nachgeholt: `FULL_RULE_BATCH_TASK.md`, `test_handoff_transport.py` und `test_local_end_to_end_chat_handoff.py` sind auf die zentrale aktuelle Handoff-Version ausgerichtet.

### 6. Codex-Arbeitsauftrag
`AGENTS.md`, `FULL_RULE_ARTICLE_TASK.md`, `FULL_RULE_BATCH_TASK.md` und `codex_entry.py` binden Codex auf den neuen engen Arbeitsweg.

Wichtig: Codex bleibt Researcher + Faktenbildner + Autor. Die zusätzlichen Stufen nehmen ihm nicht die fachliche Arbeit ab; sie verhindern nur, dass unbelegte oder querlaufende Zwischenprodukte in die nächste Stufe gelangen.

## D. Textmaschine-/Design-Unveränderlichkeit
Dieser Chat hat **keine bestehende Textmaschinenregel, PPM-6.7.9-Fachregel, PSERC/PSTE-Regel, Theme-/CSS-Datei oder WordPress-Plugin-Datei geändert**.

Die neuen System-4-Guards liegen ausschließlich unter `isolated_system4/**` und sollen die existierenden Autoritäten nur lesen/prüfen.

Der historische Designfehler aus dem PSERC-Live-Lauf 2026-08-02 bleibt Regressionsevidenz: externer HTML-Payload hatte damals bestehende Klassen/Heading-/Tabellenkonventionen verletzt und dadurch sichtbares Design geändert. System 4 darf diesen Fehler nicht wiederholen.

## E. Abschluss-/Nachholprüfung gegen autoritative Quellen
### 1. FEHLER
Neu/aktuell festgestellt:
- `S4-BLOCK-01`: kompletter aktueller System-4-Testbestand wurde nach den jüngsten Änderungen noch nicht auf exakt aktuellem Head ausgeführt.
- `S4-BLOCK-02`: aktueller positiver/negativer lokaler End-to-End-Weg vom Codex-Einstieg bis zur Elternchat-/WordPress-JSON ist noch nicht frisch ausgeführt.
- veraltete 0.28.22-Bindung in aktuellen Task-/Testdateien wurde im Closeout erkannt und nachgeführt.

Die beiden aktiven System-4-Blocker stehen in der aktuellen `isolated_system4/README.md`. Das zentrale Projektfehlerregister wurde nicht verändert, weil dieser isolierte Prototyp nicht in den offiziellen STARTMASTER/CURRENT_STATE übernommen wurde.

### 2. PROTOKOLL
Nachgeholt mit diesem Dokument. Es dokumentiert die tatsächlich vorgenommenen Architektur-/Guard-/Testfixture-/Dokumentationsänderungen und ausdrücklich die noch nicht ausgeführten Prüfungen.

### 3. WARUM / ENTSCHEIDUNGEN
Dauerhafte Entscheidungen dieses Chats:
- nicht Textregeln ändern, sondern Codex/stufenweise Übergänge kontrollieren;
- Codex bleibt kompletter fachlicher Worker;
- Fact-Evidence muss aus tatsächlich gespeicherter Source-Evidence stammen;
- Batch-Repetition wird separat geprüft;
- Textmaschine und Design sind immutable;
- Design-Guard ist nur Validator;
- nach FULL PASS keine HTML-/Designtransformation;
- kein Codex für Diagnose/Preflight.

Diese Entscheidungen stehen im Zielvertrag, AGENTS und diesem Protokoll.

### 4. CURRENT_STATE
Offizieller Campus-/Projekt-CURRENT_STATE wurde frisch gelesen und **nicht geändert**. Er bleibt STARTMASTER0107 und hat seinen eigenen alten Produktionsblocker. System 4 ist weiterhin isolierter PR-Prototyp und darf diese Wahrheit nicht überschreiben.

Die zuvor veraltete System-4-README wurde nachgeholt und ist jetzt die eine aktuelle System-4-Statuswahrheit.

### 5. HOBBYRAUM / NEXT ACTION
Die aktuelle System-4-README enthält jetzt den exakten System-4-Arbeitsraumstatus `BLOCKED bis frischer Testnachweis` und einen eindeutigen Einstiegspfad.

Der offizielle STARTMASTER0107-Hobbyraumstatus bleibt separat/unverändert; keine Fremdwahrheit wurde überschrieben.

### 6. ZIELVERTRAG
Das Ziel wurde in diesem Chat fachlich präzisiert: frühere funktionierende Chat-Arbeitslogik auf Codex, aber Textmaschine/Design immutable und Codex maximal kontrolliert.

Dafür wurde ein eindeutiger aktueller System-4-Zielvertrag angelegt:
`ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`.

### 7. ÄNDERUNGS-/ERKLÄRUNGSREGISTER
System 4 besitzt kein separates allgemeines Projekt-AENDERUNGSREGISTER. Um keine zweite Projektarchitektur zu erzeugen und nichts außerhalb `isolated_system4/**` zu verändern, werden die WAS/WARUM-Entscheidungen in diesem neuen System-4-Protokoll dauerhaft festgehalten. Der PR-Text bleibt nur Wegweiser.

### 8. ARCHIV
Die bisherigen Closeout-Dateien vom 12.09. bleiben historische Protokolle. Sie werden nicht als CURRENT verwendet. Nichts Aktives wurde ins Archiv verschoben.

### 9. PAUL / WORKER / PARALLELBRANCHES
Gebundener System-4-Arbeitsweg ist PR #238, Branch `hobbyroom/system4-true-single-room-v1`.

Kein Paul-Parallelauftrag und kein anderer gebundener Worker-Branch wurde in diesem Chat als aktuelle System-4-Arbeit verwendet. Codex wurde in diesem Umsetzungs-/Closeoutabschnitt **nicht** gestartet.

### 10. TESTS / PASS
Tatsächlich frisch geprüft:
- aktueller PR-/Branchstatus über GitHub;
- aktueller offizieller STARTMASTER-/CURRENT_STATE read-only;
- aktueller System-4-Regel-/Task-/Guard-/Handoff-Code durch Quellprüfung;
- GitHub `hardlock-base` auf dem vor dem Closeout geprüften Head war SUCCESS; dieser Workflow schützt die allgemeine unveränderliche Basis, ist aber **kein System-4-Unittest-PASS**.

Nicht tatsächlich ausgeführt:
- kompletter `isolated_system4`-Unittestbestand auf dem nach diesem Closeout aktuellen Head;
- echter lokaler `test_local_end_to_end_chat_handoff.py`-Lauf;
- frischer realer PPM-/LanguageTool-System-4-End-to-End-Lauf nach diesen Änderungen;
- neuer Codex-7/7-Lauf.

Grund: Der aktuelle Arbeitscontainer konnte das Repository wegen fehlender GitHub-DNS/Netzauflösung nicht klonen. Deshalb wird **kein System-4-PASS behauptet**.

### 11. EINE WAHRHEIT
- Offizieller Projekt-CURRENT_STATE: ausschließlich `control/startmaster0107/CURRENT_STATE.json`.
- System-4-Prototyp-CURRENT: ausschließlich `isolated_system4/README.md`.
- System-4-Ziel: ausschließlich `ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md`.
- PR-Text: nur Wegweiser.
- Historische Closeouts: keine CURRENT-Quelle.
- Aktiver System-4-Produktionsauftrag: `FULL_RULE_BATCH_TASK.md`, jetzt auf Direct Import 0.28.23 nachgeführt.

### 12. CAMPUS-/ARCHITEKTURFOLGEN
Die erkannten Prinzipien (stage-bound Evidence, immutable Design/Textmaschine, Batch-Integritätsprüfung) können später allgemein sinnvoll sein. Sie werden **jetzt nicht** in globale Campus-/Neubau-Standards übernommen, weil System 4 noch ein unbewiesener, blockierter isolierter Prototyp ist und seine AGENTS ausdrücklich Änderungen außerhalb `isolated_system4/**` verbieten.

Eine allgemeingültige Campus-Übernahme darf erst nach vollständigem System-4-PASS und einer ausdrücklichen Architekturentscheidung erfolgen. Vorher wäre das Verbreiten eines unbewiesenen Prototyps selbst ein Architekturfehler.

### 13. PLUGINS
**NICHT BETROFFEN.**

In diesem Chat wurde kein WordPress-Plugin entwickelt, kein Plugin-Code geändert und kein Plugin tatsächlich auf eine neue Version aktualisiert/installiert. Die Versionsbindung `Portal SEO Editorial Plan Compiler 0.28.23` wurde nur als bereits vorhandene Handoff-/Import-Schnittstelle im System-4-Test-/Taskvertrag nachgeführt.

Daher keine Änderung im PLUGINS-Büro und kein PU-Vorgang.

## F. Exakter Einstieg für den nächsten Chat
Der neue Chat soll **nicht aus Erinnerung** beginnen.

Zwingende Reihenfolge:
1. PR #238 `hallo-netizen/affiliate-pferdeportal` frisch lesen.
2. Branch `hobbyroom/system4-true-single-room-v1` und aktuellen Head-SHA frisch ermitteln.
3. `isolated_system4/README.md` vollständig lesen — einzige aktuelle System-4-Statuswahrheit.
4. `isolated_system4/ZIELVERTRAG_SYSTEM4_CODEX_STRICT_PIPELINE_20260913.md` vollständig lesen — verbindliches Ziel.
5. `isolated_system4/AGENTS.md` vollständig lesen — Hard Rules.
6. `isolated_system4/FULL_RULE_BATCH_TASK.md` lesen — späterer Produktionsauftrag, **noch nicht ausführen**.
7. Dieses Protokoll lesen — WAS/WARUM/Historie/offene Tests.
8. `control/CURRENT_STARTMASTER.json` und dessen `state_ref` nur read-only frisch lesen, damit der offizielle Campus-Stand nicht mit System 4 verwechselt wird.
9. **Kein Codex.** Zuerst auf exakt demselben aktuellen Head den vollständigen lokalen System-4-Test-/NO-LEGACY-/E2E-Preflight ausführen.
10. Bei FAIL: ersten tatsächlichen Fehler lokalisieren; nur isolierten System-4-Code reparieren; Textmaschine/Design/PPM/Plugin/Theme/CSS nicht anfassen; danach gesamten Testbestand erneut laufen lassen.
11. Nur bei vollständigem PASS den System-4-Status/Protokoll aktualisieren und dann Nutzerfreigabe für genau einen echten Codex-7/7-Lauf einholen.

## G. Kurzstatus für Übergabe
**AKTUELLER STAND:** System-4-Konzept und Schutzarchitektur sind auf den neuen Codex-streng-kontrolliert-Weg umgestellt; Textmaschine/Design sind ausdrücklich immutable; aktueller Status bleibt BLOCKED, weil der neue Head noch keinen frischen vollständigen System-4-Testnachweis besitzt.

**LETZTER SICHERER STAND:** guter System-4-FULL-RULE-Einzelartikel unter unveränderten PPM-/LT-Bindungen ist historisch belegt; allgemeiner GitHub-Hardlock war auf dem vor Closeout geprüften Head grün. Das ist kein PASS des jetzigen Gesamtstands.

**OFFENE FEHLER:** S4-BLOCK-01 vollständige Tests offen; S4-BLOCK-02 lokaler E2E nach aktuellem Umbau offen.

**NEXT ACTION:** frischer kompletter lokaler System-4-Preflight auf exakt aktuellem PR-Head, ohne Codex.

**VERBINDLICHER ARBEITSWEG:** Research -> Facts -> Context -> Draft -> real Fullcheck -> Same-Article Repair -> Batch Guards -> exact Handoff; Codex macht die Facharbeit, Maschine kontrolliert die Übergänge.

**NICHT ANFASSEN:** Textmaschine-Regeln, PPM-6.7.9-Fachregeln/Paket, PSERC/PSTE-Fachautoritäten, WordPress-Plugin/Signaturschalter, Theme/CSS/Design, STARTMASTER0107, Main/Merge/Publish, Legacy-Orchestrierung.

**PLUGIN-REFS:** keine Pluginentwicklung/-aktualisierung in diesem Chat; Import-Schnittstelle nur gebunden auf `Portal SEO Editorial Plan Compiler 0.28.23`.
