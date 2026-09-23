# Pferde Atelier — Konzept 5 / Concept Agent

Diese Datei ist nur die Bürotür.

## Einzige Current-Autorität

`control/startmaster0107/CURRENT_STATE.json` auf dem geschützten `main`.

Ablauf:
1. `concept_agent/CONTROL_ENTRY_POINTER.json` lesen.
2. Genau die dort genannte Current-Autorität lesen.
3. Frischecheck nur auf Delta.
4. Ausschließlich die eine dort gespeicherte `next_action` ausführen.

Diese Datei enthält bewusst keine eigene Produktionsaktion und keine zweite Statuswahrheit.

Nicht als Current-/Startautorität verwenden:
- alte `control/startmaster0107/runtime_inbox/**`-Batchzustände,
- historische Concept-Agent-Runner oder Produktionsworkflows,
- alte Cross-Chat-Transportdateien oder Run-Requests,
- historische Branches oder Protokolle.

Recherche- und Artikelqualität, LanguageTool 6.8, PPM 6.7.9, PSERC und ENDSTEMPEL bleiben unverändert. Kein Publish. Keine Alternativroute.

## Aktueller Produktionsanschluss nach gebundener Recherche

Nach `CONCEPT_AGENT_RESEARCH_BOUND_V1` ausschließlich:

`concept_agent/production_bridge.py`

Der Bridge bindet aus dem aktuellen Batch automatisch die vorhandenen Portal-Links und die vorhandene PPM-6.7.9-Qualitätsautorität. Während der Produktion werden Regeln und Links nicht frei gesucht oder neu gewählt.

Hart verboten:
- historische Produktionswege als Ausführungsweg,
- alte oder Recovery-Artikel als Vorlage, Vergleich oder Produktionsquelle,
- `pferde-atelier.de` und Subdomains als Recherchequelle,
- freie Regelsuche während der Artikelproduktion,
- freie Auswahl anderer interner Links.

Der Produktionsfortschritt läuft ausschließlich über `concept_agent/progress_guard.py`.

## Harte Wiedereinstiegsregel — überall

Sobald derselbe Batch `MACHINE_READY` erreicht hat, muss **vor jeder Fortsetzung nach einer Unterbrechung** zuerst

`concept_agent/universal_reentry_guard.py`

aus dem aktuellen Produktions-Binding und dem aktuellen Fortschritts-Checkpoint eine exakte
`CONCEPT_AGENT_UNIVERSAL_REENTRY_DECISION_V2` ableiten und verifizieren.

Diese Entscheidung ist für jede weitere Produktionsaktion Pflicht. Ohne passende Entscheidung akzeptiert `progress_guard.py` weder Schreiben noch Prüfen, Reparieren, Wiederherstellen des aktuellen Textes, PSERC noch ENDSTEMPEL.

Der Wiedereinstieg beginnt logisch immer bei Stufe 0 und darf ausschließlich bereits hashgebunden nachgewiesene Stufen überspringen. Der Chat darf weder Stufe noch Artikel auswählen.

Aktuelle Textbytes werden zusammen mit SHA-256, Größe und Revision dauerhaft im Fortschritts-Checkpoint gespeichert. Bei einem Wiedereinstieg dürfen sie nur aus diesem Checkpoint bytegenau wiederhergestellt werden.

Hart:
- fehlender oder falscher Produktionscheckpoint: **STOP**,
- fehlende oder falsche Reentry-Entscheidung: **STOP**,
- falscher Batch, Binding, Artikel, Reihenfolge, Text-Hash, Revision oder Prüferzustand: **STOP**,
- freie Chat-Ausführung: **verboten**,
- freie Repository-Suche beim Wiedereinstieg: **verboten**,
- freie Suche nach Prüferdateien/Binaries: **verboten**,
- Alternativroute: **verboten**,
- fehlt die kanonische Ausführungsumgebung: **STOP statt Suchen oder Improvisieren**,
- Reparatur bleibt beim selben Artikel,
- nächster Artikel erst nach LT-6.8- und PPM-6.7.9-PASS,
- PSERC → ENDSTEMPEL → STOP bleibt gebunden,
- nach `MACHINE_READY` desselben Batches kein zweites `text-start`.

Damit kann ein neuer Chat den Arbeitsstand weder aus Erinnerung rekonstruieren noch einen anderen Weg wählen.

## Dauerhafter Maschinenzustand nach MACHINE_READY

`control/startmaster0107/CURRENT_STATE.json` bleibt die einzige Current-Autorität dafür, **welcher Batch und welcher dauerhafte Ereignisweg gelten**.

Nach `MACHINE_READY` wird der laufende Produktionsfortschritt ausschließlich aus dem append-only Maschinenprotokoll abgeleitet:

`concept_agent/durable_event_log.py`

Autoritative Fortschrittsquelle sind nur gültige `CONCEPT_AGENT_DURABLE_EVENT_V1`-Kommentare des
`chatgpt-codex-connector[bot]` im in `CURRENT_STATE.json` fest gebundenen Batch-Issue.

Der Chat darf:
- die Fortsetzung anstoßen;
- den abgeleiteten Zustand anzeigen.

Der Chat darf **nicht**:
- Stufe, Artikel, Prüfer oder Reparaturweg auswählen;
- einen Produktionsfortschritt behaupten;
- ein autoritatives Event schreiben;
- einen fehlenden Schritt aus Erinnerung rekonstruieren;
- einen anderen Speicherort oder Ersatzpfad wählen.

Die Maschine macht vor jeder Aktion immer dasselbe:

1. festen `MACHINE_READY`-Anker prüfen;
2. alle Bot-Events ab Event 1 vollständig und hashverkettet wiederholen;
3. daraus genau **eine** erlaubte nächste Aktion ableiten;
4. genau diese Aktion ausführen;
5. das Ergebnis als neues hashgebundenes Bot-Event zurückgeben;
6. erst dieses außerhalb des Workers vorhandene Bot-Event erlaubt den nächsten Schritt.

Textbytes werden im jeweiligen Draft-/Repair-Event komprimiert, Base64-kodiert und zusätzlich an SHA-256 und Bytegröße gebunden. Beim Wiedereinstieg rekonstruiert die Maschine den Produktionscheckpoint ausschließlich aus der vollständigen Eventkette und den vorhandenen unveränderten Prüfern.

Damit gilt:
- Worker-Abbruch **vor** Bot-Event → alter sicherer Zustand bleibt aktuell;
- Worker-Abbruch **nach** Bot-Event → neuer Chat kann exakt daraus fortsetzen;
- fehlendes, manipuliertes, nicht vom Bot stammendes oder mehrdeutiges Event → **STOP**;
- kein `GH_TOKEN`, kein `git push`, kein `git remote` als Voraussetzung für Produktionsfortschritt;
- kein zweites `text-start` für denselben MACHINE_READY-Batch;
- alte Drafts, Recovery-Archive und historische Produktionszweige bleiben als NEW-Quelle verboten;
- LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL und Publish-Regeln bleiben unverändert.

Für den aktuellen 16er-Batch existiert noch kein gültiges Produktions-Event. Deshalb ist die einzige abgeleitete nächste Aktion:
`RESEARCH_ITEM` für Artikelindex 0.

`text-start` bleibt ausschließlich Startknopf und wird dadurch nicht erweitert.
