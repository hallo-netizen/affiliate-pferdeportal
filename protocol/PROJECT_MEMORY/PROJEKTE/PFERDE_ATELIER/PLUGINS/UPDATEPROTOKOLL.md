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

## PU-20260914-001 – Glossar Core / Universal Glossary Engine – Bestandsartikel + Null-Link-Regel

- **Plugin-ID / exakter Name:** `MOD-008` / aktuell lokal paketiert als `Universal Glossary Engine 1.2.2`.
- **ART:** ENTWICKLUNG
- **Herkunft:** EIGENENTWICKLUNG
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/`
- **VON_VERSION:** `1.2.1` Kandidat bzw. davor Bestandsupdate `1.2.0`.
- **AUF_VERSION:** lokaler Kandidat `1.2.2`.
- **Quelle / Branch / Releasequelle:** **BLOCKED** – Ausgangsbytes 1.2.1 wurden exakt aus dem gespeicherten Kandidaten geladen; der neue 1.2.2-Pluginquellstand ist noch nicht als eigene autoritative GitHub-Pluginquelle/Release gebunden.
- **lokales Paket:** `UNIVERSAL_GLOSSARY_ENGINE_1.2.2_ZERO_BODY_LINKS_BESTAND_UPDATE_INSTALLIEREN.zip`.
- **SHA-256:** `3d6ffc2cdfcc4872e49e97f4adc54de31d4ef2714b0af07e399a681f15d1f447`.
- **WARUM:** Nutzerreadback 2026-09-14 verlangt ausnahmslos 0 Links im Glossar-Fließtext und Reparatur/Überschreiben auch bereits bestehender Glossarbeiträge.
- **Abhängigkeiten / Schnittstellen:** WordPress `uge_term`; Related-Slugs/Relation; Design-Einzelansicht 1.50.490.
- **relevante Fehlerquelle:** `../GLOSSAR/FEHLERQUELLEN.md` → `GLOSSAR-SINGLE-011`.
- **Rollback/Sicherheit:** Bestandsupdate nutzt vorhandene IDs; normale WordPress-Posts sind ausgeschlossen; keine pauschale Löschung.
- **Positivprüfung tatsächlich ausgeführt 2026-09-14:** 14 Begriffe weiterhin 150–200 Wörter; 0 `<a>`-Links im Fließtext; Related separat → PASS.
- **Bestands-Positivprüfung:** vorhandener `uge_term` mit Test-ID 77 wird per Update mit derselben ID linkfrei überschrieben → PASS.
- **Negativprüfung:** normaler WordPress-Post im selben Fixture wird nicht verändert → PASS.
- **Marker:** `CORE_122_ZERO_BODY_LINKS_POS_NEG_PASS`, `CORE_122_EXISTING_ID_PRESERVE_AND_NORMAL_POST_NEG_PASS`.
- **ZIP/Version:** ZIP-Lesetest PASS; PHP-Lint PASS; Version `1.2.2` PASS.
- **isoliertes Artefakt:** **NICHT ERSETZT**. Bestehendes `MOD-008/CURRENT.zip` bleibt unangetastet, weil autoritative Plugin-Quell-/Releasebindung und LIVE-Readback fehlen.
- **ERGEBNIS:** `BLOCKED` für Artefaktsynchronisierung/Release; lokaler technischer Kandidat PASS, kein LIVE-PASS.

## PU-20260914-002 – Pferde Atelier Design / affiliate-portal-template-kit – Glossar-Einzelansicht

- **Plugin-ID / exakter Name:** Pluginordner `affiliate-portal-template-kit`, Hauptdatei `pferde-template-kit.php`; **keine eindeutige Plugin-ID im aktuell gelesenen PLUGINS-REGISTER vorhanden**.
- **ART:** ENTWICKLUNG
- **Herkunft:** EIGENENTWICKLUNG
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/` fachlich; Designintegration über `PROJEKTE/PFERDE_ATELIER/DESIGN/`.
- **VON_VERSION:** `1.50.489` Kandidat.
- **AUF_VERSION:** lokaler Kandidat `1.50.490`.
- **Quelle / Branch / Releasequelle:** **BLOCKED** – Ausgangsbytes 1.50.489 wurden exakt aus dem gespeicherten Kandidaten geladen; der neue 1.50.490-Pluginquellstand ist noch nicht als eigene autoritative GitHub-Pluginquelle/Release gebunden.
- **lokales Paket:** `PFERDE_ATELIER_DESIGN_V1.50.490_GLOSSAR_BREADCRUMB_STRIPE_FIX_INSTALLIEREN.zip`.
- **SHA-256:** `251e90a7c7115cd4ce166ddefb5f0918904f28b89d85f2a173c190201b454657`.
- **WARUM:** realer Screenshot zeigt Breadcrumb weiterhin falsch/doppelt; Nutzer verlangt außerdem 0 Fließtextlinks und dünnere Ocker-Oberkante der rechten Boxen.
- **Abhängigkeiten / Schnittstellen:** WordPress/Kubio; `uge_term`; `uge_group`; Related-Meta des Glossar-Core.
- **relevante Fehlerquelle:** `../GLOSSAR/FEHLERQUELLEN.md` → `GLOSSAR-SINGLE-011`.
- **Positivprüfung tatsächlich ausgeführt:** eigener Breadcrumb-Vertrag `Startseite > Glossar > Oberbereich > Begriff`; obere Boxkante 2 px; Fließtext-Endschranke entfernt Restlinks → PASS.
- **Negativ-/Regressionstest:** globaler Universal-Breadcrumb wird auf `uge_term` serverseitig nicht erzeugt; CSS-Failsafe zusätzlich vorhanden; Filter hart auf `uge_term`; normale Posts ausgeschlossen → PASS.
- **Marker:** `DESIGN_150490_BREADCRUMB_ZERO_LINKS_THIN_STRIPE_POS_NEG_PASS`.
- **ZIP/Version:** ZIP-Lesetest PASS; PHP-Lint PASS; Version `1.50.490` PASS.
- **isoliertes Artefakt:** **NICHT ANGELEGT/ERSETZT**, weil eindeutige Plugin-ID/autoritative Quell-/Releasebindung und LIVE-Readback fehlen.
- **ERGEBNIS:** `BLOCKED` für Artefaktsynchronisierung/Release; lokaler technischer Kandidat PASS, kein LIVE-PASS.

## Aktuelle Fach-/Release-/LIVE-Autorität

Ausschließlich:
- `../GLOSSAR/CURRENT_STATE.md`
- `../GLOSSAR/HOBBYRAUM.md`
- `../GLOSSAR/FEHLERQUELLEN.md`

Dieses Protokoll bleibt Kontrollpult und erzeugt keine zweite Fachwahrheit.
