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

### Harte Wiedereinstiegsregel – alle Phasen

Sobald derselbe Batch `MACHINE_READY` erreicht hat, gilt nach **jeder** Unterbrechung ausschließlich:

`concept_agent/universal_reentry_guard.py`

Der normale Produktionscheckpoint bestimmt weiterhin Artikel und äußeren Schritt. Der Universal-Reentry-Checkpoint bindet zusätzlich den **vollständigen echten Arbeitszustand** des aktuell laufenden Artikels.

Das gilt unabhängig davon, ob die Unterbrechung bei Recherche, Faktenprüfung, Kontext, Schreiben, Fullcheck, LT/PPM-Reparatur, Output-Gate, Signatur, Artikelabschluss, PSERC oder ENDSTEMPEL passiert.

Hart:
- fehlt der gültige Produktionscheckpoint: **STOP**,
- läuft bereits ein Artikel und fehlt seine gültige Recovery-Kapsel: **STOP**,
- falscher Batch, Artikel, Plan-Slot, Phase, Text-Hash, Prüfbefund, Revision oder Kapsel-Hash: **STOP**,
- Phasensprung oder Artikelwechsel ohne erlaubten Übergang: **STOP**,
- der Chat besitzt **keine freie Ausführungsautorität**,
- der Chat darf beim Wiedereinstieg **weder Repository noch Prüferdateien/Binaries frei suchen**,
- kein Wiederaufbau aus Chat-Erinnerung,
- kein Ableiten aus alten Zuständen, Recovery-Artikeln oder historischen Wegen,
- nur der exakt gebundene nächste Worker-/Prüfschritt ist zulässig,
- Reparatur bleibt beim selben Artikel,
- PSERC und ENDSTEMPEL liegen ebenfalls hinter derselben Wiedereinstiegssperre,
- nach ENDSTEMPEL-PASS ist ausschließlich STOP erlaubt,
- nach `MACHINE_READY` desselben Batches darf `text-start` nicht erneut ausgelöst werden.

Ein Wiedereinstieg ohne vollständigen beweisbaren Zustand darf daher **niemals** durch Suchen, Raten oder einen Ersatzweg repariert werden.

`control/startmaster0107/CURRENT_STATE.json` bleibt Startautorität **vor** `MACHINE_READY`. Danach bestimmen ausschließlich die gültig verketteten Produktions-/Reentry-Checkpoints die Fortsetzung.

`text-start` bleibt ausschließlich Startknopf und wird dadurch nicht erweitert.
