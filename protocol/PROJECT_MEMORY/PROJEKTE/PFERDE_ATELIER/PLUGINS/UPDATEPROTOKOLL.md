# PFERDE-ATELIER – PLUGINS – UPDATEPROTOKOLL

STAND: 2026-09-14
ROLLE: ZENTRALES PLUGIN-ÄNDERUNGSPROTOKOLL DES PFERDE-ATELIERS

## Grenze

Genau ein Vorgang je tatsächlicher Pluginentwicklung/-aktualisierung. Keine zweite Fach-, Release- oder LIVE-Wahrheit. Keine Secrets.

## PU-20260913-001 – Universal Glossary Engine

- **Plugin-ID / Name:** `MOD-008` / `Universal Glossary Engine`
- **ART:** ENTWICKLUNG
- **Herkunft:** EIGENENTWICKLUNG
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/`
- **VON_VERSION:** `0.2.9`
- **AUF_VERSION:** `0.2.10-rc7`
- **Quelle / Branch:** `hobbyroom/glossar-livefail-red-green-20260913`
- **exakt getesteter Quell-Commit:** `1e74b7454e84f97182dbb185614371a48157bc21`
- **WARUM:** damalige technische Reparatur und Härtung der Glossar-Einzelansicht / Clusterproduktion.
- **Positiv-/Negativ-/Regressionstest:** Run `34762048546` und Closeout `34764046870` → PASS.
- **isoliertes Artefakt:** `ISOLIERTE_PLUGINS/MOD-008/CURRENT.zip` + `MANIFEST.md`.
- **CURRENT.zip SHA-256:** `3611229aa33ca50a00ec88be87e6ef92592e87d313c152f05d0c7a31ab281152`.
- **ERGEBNIS:** damaliger technischer Artefakt-PASS; nicht mit heutigem Glossarstand verwechseln.

## PU-20260914-001 – Glossar Core / Universal Glossary Engine – Bestandsartikel + Linktrennung

- **Plugin-ID / exakter Name:** `MOD-008` / aktuell lokal paketiert als `Universal Glossary Engine 1.2.1`.
- **ART:** ENTWICKLUNG
- **Herkunft:** EIGENENTWICKLUNG
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/`
- **VON_VERSION:** mehrere Chat-/Arbeitsstände nach rc11, zuletzt Bestandsupdate `1.2.0`.
- **AUF_VERSION:** lokaler Kandidat `1.2.1`.
- **Quelle / Branch / Releasequelle:** **BLOCKED** – finaler 1.2.1-Quellstand liegt in dieser Nachholprüfung nur im lokalen Arbeitscontainer vor und ist noch nicht als autoritativer GitHub-Quell-Commit/Release gebunden.
- **lokales Paket:** `UNIVERSAL_GLOSSARY_ENGINE_1.2.1_GLOSSAR_ARTIKEL_UPDATE_INSTALLIEREN.zip`.
- **SHA-256:** `f6788524f50413541ea40e33bc7005a4e936e2915e4465cf2e7a08e221c900e0`.
- **WARUM:** vorhandene Glossarbegriffe ohne Löschen nach neuen Text-/Linkregeln überschreiben; verwandte Begriffe aus dem Fließtext entfernen und separat für die rechte Linkbox binden; doppelte Zielverlinkung verhindern; Kurzdefinitionen erhalten.
- **Abhängigkeiten / Schnittstellen:** WordPress `uge_term`; Related-Slugs/Relation; primäre Portal-Kategorie; Design-Einzelansicht 1.50.489.
- **relevante Fehlerquelle:** `../GLOSSAR/FEHLERQUELLEN.md` → `GLOSSAR-SINGLE-011`.
- **Rollback:** vorhandene Bestands-IDs bleiben beim Update erhalten; Löschen des Bestands ist ausdrücklich nicht vorgesehen.
- **Positivprüfung tatsächlich ausgeführt 2026-09-14:** 14 Begriffe, 150–200 Wörter; genau 1 Fließtext-Link; Related separat; IDs beim Überschreiben erhalten → PASS.
- **Negativprüfung tatsächlich ausgeführt:** Fremd-Slug-Konflikt fail-closed; normaler WordPress-Post unverändert → PASS.
- **Marker:** `CORE_121_POS_NEG_PASS`, `CORE_121_EXISTING_IDS_OVERWRITE_POS_NEG_PASS`, `CORE_121_FOREIGN_FAILCLOSED_AND_NORMAL_POST_NEG_PASS`.
- **ZIP/Version:** ZIP-Lesetest PASS; Version `1.2.1` PASS.
- **isoliertes Artefakt:** **NICHT ERSETZT**. Bestehendes `MOD-008/CURRENT.zip` bleibt unangetastet, weil der neue Quell-/Releasebeleg fehlt.
- **ERGEBNIS:** `BLOCKED` für Plugin-Artefaktsynchronisierung/Release; lokaler technischer Teststand PASS, kein LIVE-PASS.

## PU-20260914-002 – Pferde Atelier Design / affiliate-portal-template-kit – Glossar-Einzelansicht

- **Plugin-ID / exakter Name:** Pluginordner `affiliate-portal-template-kit`, Hauptdatei `pferde-template-kit.php`; **keine eindeutige Plugin-ID im aktuell gelesenen PLUGINS-REGISTER vorhanden**.
- **ART:** ENTWICKLUNG
- **Herkunft:** EIGENENTWICKLUNG
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/` fachlich; Designintegration über `PROJEKTE/PFERDE_ATELIER/DESIGN/`.
- **VON_VERSION:** Arbeitsfolge bis `1.50.488`.
- **AUF_VERSION:** lokaler Kandidat `1.50.489`.
- **Quelle / Branch / Releasequelle:** **BLOCKED** – finaler 1.50.489-Quellstand liegt in dieser Nachholprüfung nur im lokalen Arbeitscontainer vor und ist noch nicht als autoritativer GitHub-Quell-Commit/Release gebunden.
- **lokales Paket:** `PFERDE_ATELIER_DESIGN_V1.50.489_GLOSSAR_EINZELANSICHT_FIX_INSTALLIEREN.zip`.
- **SHA-256:** `fc6bc67a827f314e37c597e4fbb764f616c86d97bfc6d621c238c813a64ab600`.
- **WARUM:** Glossar-Einzelansicht an Pferde-Atelier-Design anpassen; Autor/User entfernen; korrekten Glossar-Breadcrumb ausgeben; Kurzdefinition, Icons, rechte Boxen `Verwandte Begriffe`/`Mehr zum Thema`; harte Begrenzung auf `uge_term`.
- **Abhängigkeiten / Schnittstellen:** WordPress/Kubio; `uge_term`; `uge_group`; Related-Meta des Glossar-Core; primäre Portal-Kategorie.
- **relevante Fehlerquelle:** `../GLOSSAR/FEHLERQUELLEN.md` → `GLOSSAR-SINGLE-011`.
- **Positivprüfung tatsächlich ausgeführt 2026-09-14:** Browser 1200/900/720/500; Breadcrumb korrekt; 2 Sideboxen; mindestens 3 Icons; Desktop-Oberkante bündig; kein Overflow → PASS.
- **Negativ-/Regressionstest tatsächlich ausgeführt:** globaler/falscher Breadcrumb auf Glossar-Single verborgen; Designcode hart auf `uge_term` begrenzt; normale Beiträge sollen nicht betroffen sein → technischer PASS im lokalen Testfixture.
- **Marker:** `DESIGN_150489_POS_NEG_PASS`.
- **ZIP/Version:** ZIP-Lesetest PASS; PHP-Lint PASS; Version `1.50.489` PASS.
- **isoliertes Artefakt:** **NICHT ANGELEGT/ERSETZT**, weil Plugin-ID und autoritativer Quell-/Releasebeleg fehlen.
- **ERGEBNIS:** `BLOCKED` für Plugin-Artefaktsynchronisierung/Release; lokaler technischer Teststand PASS, kein LIVE-PASS.

## Aktuelle Fach-/Release-/LIVE-Autorität

Ausschließlich:
- `../GLOSSAR/CURRENT_STATE.md`
- `../GLOSSAR/HOBBYRAUM.md`
- `../GLOSSAR/FEHLERQUELLEN.md`

Dieses Protokoll bleibt Kontrollpult und erzeugt keine zweite Fachwahrheit.
