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

Der Bridge bindet aus dem aktuellen Batch automatisch die bereits vorhandenen Portal-Links und die vorhandene PPM-6.7.9-Qualitätsautorität. Während der Produktion werden Regeln und Links nicht frei gesucht oder neu gewählt.

Hart verboten:
- historische Produktionswege als Ausführungsweg,
- alte oder Recovery-Artikel als Vorlage, Vergleich oder Produktionsquelle,
- `pferde-atelier.de` und Subdomains als Recherchequelle,
- freie Regelsuche während der Artikelproduktion,
- freie Auswahl anderer interner Links.

Der Produktionsfortschritt läuft ausschließlich über `concept_agent/progress_guard.py`.

### Harte Wiedereinstiegsregel

Sobald derselbe Batch `MACHINE_READY` erreicht hat und die Produktionsbindung erzeugt wurde, ist **nur noch der letzte gültige Produktionscheckpoint** Fortsetzungsautorität.

Nach jeder Unterbrechung muss zuerst `progress_guard.py resume BINDING CHECKPOINT` erfolgreich sein. Der hashgebundene Wert `allowed_action` ist die **einzige** erlaubte nächste Produktionsaktion.

Hart:
- fehlt der Checkpoint: **STOP**,
- passt Batch, Binding, Hash oder `allowed_action` nicht exakt: **STOP**,
- kein Wiederaufbau aus Chat-Erinnerung,
- kein Ableiten des nächsten Schritts aus alten Zuständen oder Recovery-Dateien,
- kein Batch-Import bereits vorhandener Artikel,
- immer nur genau **ein** vom Checkpoint freigegebener Artikel,
- nach LT-/PPM-Reparatur bleibt derselbe Artikel gebunden,
- nach `MACHINE_READY` desselben Batches darf `text-start` nicht erneut ausgelöst werden.

`control/startmaster0107/CURRENT_STATE.json` bleibt Startautorität **vor** `MACHINE_READY`. Für die Fortsetzung eines bereits gestarteten Produktionslaufs ist danach der gültige Produktionscheckpoint maßgeblich.

`text-start` bleibt ausschließlich Startknopf und wird dadurch nicht erweitert.
