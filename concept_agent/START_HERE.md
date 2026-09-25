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

Vor jeder Fortsetzung nach einer Unterbrechung muss zuerst

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

Damit kann ein neuer Chat den Arbeitsstand weder aus Erinnerung rekonstruieren noch einen anderen Weg wählen.

`text-start` trägt keinen Produktionsfortschritt. Nach dem Start bestimmen ausschließlich aktuelles Produktions-Binding, aktueller Fortschritts-Checkpoint und die daraus exakt abgeleitete Reentry-Entscheidung die Fortsetzung.

`text-start` bleibt ausschließlich Startknopf und wird dadurch nicht erweitert.
