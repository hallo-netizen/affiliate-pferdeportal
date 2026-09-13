# PFERDE-ATELIER – PLUGINS – UPDATEPROTOKOLL

STAND: 2026-09-13
ROLLE: ZENTRALES PLUGIN-ÄNDERUNGSPROTOKOLL DES PFERDE-ATELIERS

## Grenze

Genau ein Vorgang je tatsächlicher Pluginentwicklung/-aktualisierung. Keine zweite Fach-, Release- oder LIVE-Wahrheit. Keine Secrets.

## PU-20260913-001 – Universal Glossary Engine

- **Plugin-ID / Name:** `MOD-008` / `Universal Glossary Engine`
- **ART:** ENTWICKLUNG
- **Herkunft:** EIGENENTWICKLUNG
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/`
- **VON_VERSION:** `0.2.9` – letzter vorhandener gated technischer Kandidat; kein bestätigter Pferde-LIVE-PASS
- **AUF_VERSION:** `0.2.10-rc7` – aktueller technisch geprüfter Entwicklungsstand, noch kein Übergabepaket
- **Quelle / Branch:** `hobbyroom/glossar-livefail-red-green-20260913`
- **getesteter Quell-Head:** `1e74b7454e84f97182dbb185614371a48157bc21`
- **WARUM:** reale Klickbarkeit von Glossarbegriffen härter beweisen; Einzelansichten auch gegen leeren normalen Main-Loop absichern; reale Design-Breadcrumb-Achse verwenden; verwandte Glossarbegriffe als geschlossenen, vollständig verlinkten Cluster erzeugen; tote `Verwandte Begriffe`-Textlisten verhindern; Publikationspolicy mit echter primärer Portal-Kategorie einhalten.
- **Abhängigkeiten / Schnittstellen:** WordPress; Astra-Testumgebung; realer ausführbarer Hauptcode des Pferde-Designplugins 1.50.469 als Integrationsnachweis; `uge_term`; `uge_group`; bestehende UGE-Publikationspolicy; primäre Portal-Kategorie `Gesundheit`.
- **relevante Fehlerquellen:** ausschließlich `../GLOSSAR/FEHLERQUELLEN.md`, insbesondere ROUTE-004, ROUTE-005, PROD-008, LAYOUT-009, PKG-010.
- **Backup-/Rollback-Referenz:** 0.2.9 bleibt letzter vorhandener gated technischer Paketstand; er ist nicht als aktueller Entwicklungsstand oder bestätigter Pferde-LIVE-PASS zu behandeln. Git-Historie bindet die 0.2.10-RC-Stufen.
- **Positivprüfung tatsächlich ausgeführt:** echter Browser klickt vorhandenen `Hufbein`-Link auf Einzelansicht; neuer Cluster `Hufrehe → Strahlfäule → Hufabszess`; Kategorienlink zurück zu `Gesundheit`; reale Design-Breadcrumb-Achse; Clusterpublikation; vorhandene alte positive Regression. Run `34762048546`, Jobs `103736483608` und `103736483696` SUCCESS.
- **Negativprüfung tatsächlich ausgeführt:** Draft öffentlich 404; authentifizierte Draft-Preview bleibt funktionsfähig; unbekannte/Regressionfälle; Duplicate Guard; normale Posts unverändert; Pferderassen-Leak ausgeschlossen; Einzelansicht zusätzlich bei absichtlich geleertem WordPress-Main-Loop getestet. Run `34762048546` SUCCESS.
- **Fach-/Regressionstest:** Fresh `103736483608` SUCCESS; Real Design/Browser/Loop-Poison `103736483696` SUCCESS; `UGE0210_EXISTING_SINGLE_CLICK_PASS`, `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`, `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`, `UGE0210_PFERDE_BREADCRUMB_AXIS_PASS`.
- **Paket-/Artefaktprüfung:** **NICHT AUSGEFÜHRT FÜR rc7.** Der Workflow endet absichtlich mit `UGE0210RC7_HARD_GATES_PASS_NO_PACKAGE`; deshalb kein rc7-Installations-ZIP, kein rc7-Paket-SHA und keine zulässige `CURRENT.zip`.
- **isoliertes Artefakt:** noch nicht vorhanden; `ISOLIERTE_PLUGINS/MOD-008/CURRENT.zip` darf erst nach einem gated Paketlauf auf exakt gebundenen Bytes angelegt werden.
- **ERGEBNIS:** `BLOCKED` für Paket/Übergabe/PLUGINS-Artefaktsynchronisierung. Technische rc7-Positiv-/Negativ-/Regressionstests PASS; Pferde-LIVE-Readback ebenfalls offen.
- **Fach-/Release-/LIVE-Autorität:** `../GLOSSAR/CURRENT_STATE.md`, `../GLOSSAR/HOBBYRAUM.md`, `../GLOSSAR/FEHLERQUELLEN.md`; dieses Protokoll ist nur Kontrollpult.
