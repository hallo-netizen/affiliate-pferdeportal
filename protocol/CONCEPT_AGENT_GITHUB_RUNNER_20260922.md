# Concept Agent GitHub Runner — 2026-09-22

## Zweck
Konzept 5 behält ChatGPT als Schreibagenten. Die freie Workflow-Steuerung wird dem Chat entzogen und in GitHub festgelegt.

## Fester Weg
Chat-Auslöser -> GitHub Action -> concept_agent/runner.py -> genau ein gebundener Artikel -> Prüfung -> gegebenenfalls Reparatur desselben Artikels -> PASS -> nächster Artikel -> CONCEPT_AGENT_CHAT_HANDOFF_V1.json.

## Unverändert
- intake_bridge.py bleibt der fachliche Eingang.
- bestehende Recherche-/Authoring-Bindungen bleiben Eingabe.
- LanguageTool 6.8 und PPM 6.7.9 bleiben die echten Produktionsprüfer.
- PSERC und ENDSTEMPEL bleiben unverändert.
- publish_allowed bleibt false.

## Simulation
- 1 Artikel positiv.
- 3 Artikel positiv; Artikel 2 benötigt genau eine Reparatur, Artikel 3 startet erst nach PASS von Artikel 2.
- negativ: vorzeitiger Sprung zum nächsten Artikel blockiert.
- negativ: falsche Artikelidentität/Plan-Slot blockiert.
- weitere Unit-Negativtests: Publish-Flag, Reihenfolge, doppelter Plan-Slot.

## Aktuelle reale Grenze
Der laufende 16er-Stand ist in GitHub nur über CONCEPT_AGENT_CURRENT_WORK_BINDING_POINTER.json referenziert. Die exakte Datei CONCEPT_AGENT_16_WORK_BINDING.json ist noch nicht im Repository persistiert. run-current muss deshalb bis zur bytegenauen Ablage dieser Datei fail-closed blockieren.
