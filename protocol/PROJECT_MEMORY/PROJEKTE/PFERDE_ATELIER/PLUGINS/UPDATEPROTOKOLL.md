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
- **VON_VERSION:** `0.2.9` – früherer gated technischer Kandidat; kein bestätigter Pferde-LIVE-PASS
- **AUF_VERSION:** `0.2.10-rc7` – aktueller technisch geprüfter und hashgebunden paketierter Kandidat; Pferde-LIVE offen
- **Quelle / Branch:** `hobbyroom/glossar-livefail-red-green-20260913`
- **exakt getesteter Quell-Commit:** `1e74b7454e84f97182dbb185614371a48157bc21`
- **WARUM:** reale Klickbarkeit von Glossarbegriffen härter beweisen; Einzelansichten auch gegen leeren normalen Main-Loop absichern; reale Design-Breadcrumb-Achse verwenden; verwandte Glossarbegriffe als geschlossenen, vollständig verlinkten Cluster erzeugen; tote `Verwandte Begriffe`-Textlisten verhindern; Publikationspolicy mit echter primärer Portal-Kategorie einhalten.
- **Abhängigkeiten / Schnittstellen:** WordPress; Astra-Testumgebung; realer ausführbarer Hauptcode des Pferde-Designplugins 1.50.469 als Integrationsnachweis; `uge_term`; `uge_group`; bestehende UGE-Publikationspolicy; primäre Portal-Kategorie `Gesundheit`.
- **relevante Fehlerquellen:** ausschließlich `../GLOSSAR/FEHLERQUELLEN.md`, insbesondere ROUTE-004, ROUTE-005, PROD-008, LAYOUT-009, PKG-010.
- **Backup-/Rollback-Referenz:** 0.2.9 bleibt historischer früherer gated Paketstand; nicht als aktueller Entwicklungsstand oder bestätigter Pferde-LIVE-PASS behandeln. Git-Historie bindet die 0.2.10-RC-Stufen.
- **Positivprüfung tatsächlich ausgeführt:** echter Browser klickt vorhandenen `Hufbein`-Link auf Einzelansicht; neuer Cluster `Hufrehe → Strahlfäule → Hufabszess`; Kategorienlink zurück zu `Gesundheit`; reale Design-Breadcrumb-Achse; Clusterpublikation; bestehende positive Regression. Hardtest Run `34762048546`, Jobs `103736483608` und `103736483696` SUCCESS.
- **Negativprüfung tatsächlich ausgeführt:** Draft öffentlich 404; authentifizierte Draft-Preview bleibt funktionsfähig; unbekannte/Regressionfälle; Duplicate Guard; normale Posts unverändert; Pferderassen-Leak ausgeschlossen; Einzelansicht zusätzlich bei absichtlich geleertem WordPress-Main-Loop getestet. Run `34762048546` SUCCESS.
- **Fach-/Regressionstest:** Fresh `103736483608` SUCCESS; Real Design/Browser/Loop-Poison `103736483696` SUCCESS; `UGE0210_EXISTING_SINGLE_CLICK_PASS`, `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`, `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`, `UGE0210_PFERDE_BREADCRUMB_AXIS_PASS`.
- **Paket-/Artefaktprüfung:** NACHGEHOLT aus exakt getestetem Quell-Commit `1e74b7454e84f97182dbb185614371a48157bc21`; Closeout Run `34764046870`, Job `103741741909` SUCCESS; `unzip -t` PASS; Source-vs-Unpack `diff -qr` PASS; Version `0.2.10-rc7` PASS; PHP-Lint PASS; SHA-256 PASS.
- **isoliertes Artefakt:** `ISOLIERTE_PLUGINS/MOD-008/CURRENT.zip` + `MANIFEST.md`; abgeleitete hashgebundene Ausgabekopie des exakt getesteten Quellstands.
- **CURRENT.zip SHA-256:** `3611229aa33ca50a00ec88be87e6ef92592e87d313c152f05d0c7a31ab281152`
- **Actions-Artefakt:** ID `10319439428`; outer artifact SHA-256 `cbf72dc81229adf33febca085c43d70a12188880cd62c7aafd3f687cb62f2bab`.
- **ERGEBNIS:** `PASS` für Entwicklung + technische Paket-/Artefaktsynchronisierung. Pferde-LIVE-Readback bleibt offen und wird nicht aus CI abgeleitet.
- **Fach-/Release-/LIVE-Autorität:** `../GLOSSAR/CURRENT_STATE.md`, `../GLOSSAR/HOBBYRAUM.md`, `../GLOSSAR/FEHLERQUELLEN.md`; dieses Protokoll ist nur Kontrollpult.
