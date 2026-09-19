# Concept Agent

Status: ISOLATED PROTOTYPE — STARTED

Dieses Büro ist vollständig getrennt von allen bisherigen Konzepten.

Aktueller Aufbau:
- `AGENTS.md`: harte Isolation
- `ZIELVERTRAG.md`: Ziel und Grenzen
- `contracts.py`: eigene Übergabeformate
- `pipeline.py`: eigene, noch providerfreie Agenten-Kette
- `tests/test_isolation.py`: erster Isolationsnachweis

Nächster Entwicklungsschritt:
Die vier Rollen als getrennte, prüfbare Zustände aufbauen und danach mit einem kopierten realen WordPress-Auftrag testen.

Wichtig:
Kein Code außerhalb `concept_agent/**` wird verändert oder aufgerufen.
