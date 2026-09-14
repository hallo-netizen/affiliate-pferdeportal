# PFERDE-ATELIER – PLUGINS – UPDATEPROTOKOLL

STAND: 2026-09-14
ROLLE: ZENTRALES PLUGIN-ÄNDERUNGSPROTOKOLL DES PFERDE-ATELIERS

## Grenze

Genau ein Vorgang je tatsächlicher Pluginentwicklung/-aktualisierung. Keine zweite Fach-, Release- oder LIVE-Wahrheit. Keine Secrets.

## PU-20260913-001 – Universal Glossary Engine – historischer RC

- Plugin-ID / Name: `MOD-008` / `Universal Glossary Engine`.
- damaliger Stand: `0.2.10-rc7`.
- technischer Artefakt-PASS historisch; nicht mit heutigem Glossarstand verwechseln.

## PU-20260914-001 – Glossar Core – lokaler Kandidat 1.3.0

- **Plugin-ID / exakter Name:** `MOD-008` / Pferde Atelier Glossar Core.
- **ART:** ENTWICKLUNG.
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/`.
- **VON_VERSION:** 1.2.3.
- **AUF_VERSION:** lokaler Kandidat `1.3.0`.
- **Paket:** `UNIVERSAL_GLOSSARY_ENGINE_1.3.0_AUTOMATION_SANDBOX_INSTALLIEREN.zip`.
- **SHA-256:** `b408756c63ab719fcf82131a6dd297c261e36817d957c69ceb9644d7ed8fd2a4`.
- **WARUM:** damaliger Aufbau von Kandidatenpool, Sandbox, Research-Gate und vorbereiteter Automatik.
- **ERGEBNIS:** historischer lokaler Kandidat; später durch 1.3.5–1.3.8 weiterentwickelt und der autonome Produktionsansatz am 14.09.2026 fachlich abgelöst.

## PU-20260914-002 – Pferde Atelier Design – Glossar Breadcrumb 1.50.493

- **Pluginordner:** `affiliate-portal-template-kit`; Hauptdatei `pferde-template-kit.php`.
- **ART:** ENTWICKLUNG.
- **zuständiges Fachbüro:** Glossar fachlich, Designintegration über Designbüro.
- **VON_VERSION:** 1.50.492.
- **AUF_VERSION:** lokaler Kandidat `1.50.493`.
- **Paket:** `PFERDE_ATELIER_DESIGN_V1.50.493_BREADCRUMB_SAME_PATH_INSTALLIEREN.zip`.
- **SHA-256:** `067e11f7d7f54ce22206955297566fbb78fdc9abd464075ebee4b82e7aed2a5d`.
- **WARUM:** damaliger Nutzerreadback: Breadcrumb-Abstand am Glossar-Single falsch.
- **ERGEBNIS:** historischer Zwischenstand; spätere Designstände folgen in eigenem Vorgang.

## PU-20260914-003 – Pferde Atelier – Pferderassen Manager 0.1.0

- **Plugin-ID:** noch nicht zentral vergeben.
- **exakter Name:** `Pferde Atelier – Pferderassen Manager`.
- **ART:** NEUENTWICKLUNG.
- **Herkunft:** EIGENENTWICKLUNG.
- **zuständiges Fachbüro:** WDB `PFERDERASSEN` + Pluginbüro.
- **VON_VERSION:** keine.
- **AUF_VERSION:** 0.1.0.
- **Zweck:** eigener `pa_breed`-Backendbereich und kontrollierter JSON→Draft-Weg.
- **damaliger Test:** 30/30 PASS; 7/7 Mutanten ROT.
- **ERGEBNIS:** historischer Erststand; durch 0.2.0 fachlich/technisch ersetzt.

## PU-20260914-004 – Universal Glossary Engine 1.3.5→1.3.8 – autonome Workerstrecke

- **Plugin-ID / Name:** `MOD-008` / Universal Glossary Engine / Glossar Core.
- **ART:** ENTWICKLUNG.
- **Herkunft:** EIGENENTWICKLUNG.
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/`.
- **VON_VERSION:** 1.3.4.
- **AUF_VERSION:** 1.3.8 letzter Kandidat dieser Architektur.
- **Quelle / Branch:** lokale Kandidaten + Fachprotokolle auf `hobbyroom/glossar-livefail-red-green-20260913`; keine autoritativ gebundene Plugin-Source/Releasequelle für die finalen Paketbytes.
- **WARUM:** damaliger Versuch, PSTE-Discovery/Planning selbstlaufend bis zur Research-/Publish-Strecke zu treiben.
- **Abhängigkeiten/Schnittstellen:** PSTE-Retained/Planning, internes REST-Loopback, WP-Cron als Recovery, Research-Paket-Gate, WordPress-Readback.
- **Fehlerbezug:** `../GLOSSAR/FEHLERQUELLEN.md` → historische `GLOSSAR-AUTO-013`-Kette.
- **Positivprüfung 1.3.8:** E2E Discovery→Research→Sandbox→Armed→Readback→Publish simuliert; 50/50 simulierte WordPress-Beiträge; 93 explizite PASS-Zeilen, 0 explizite FAIL-Zeilen; PHP-Lint/ZIP-Lesetest/exakte ZIP-Retests PASS.
- **Negativprüfung:** Provider-Verstoß, Retry/Timeout, Lock, Research-/PRE-PUBLISH-/Readback-Gates PASS.
- **Mutation:** 6/6 Driver-Mutanten ROT.
- **Paket:** `UNIVERSAL_GLOSSARY_ENGINE_1.3.8_LOOPBACK_DRIVER_HARDLOCK_INSTALLIEREN.zip`.
- **SHA-256:** `dc8850eb1b67006fefaafeb27679973932982f891f6ec84a9702bfd4532277f1`.
- **LIVE:** 1.3.5/1.3.6/1.3.7 jeweils real FAIL; 1.3.8 nie live abgenommen.
- **Rollback/Backup:** bestehender alter isolierter `MOD-008/CURRENT.zip` wurde nicht ersetzt.
- **ERGEBNIS:** **BLOCKED / PRODUKTIONSARCHITEKTUR ABGELÖST**. Nutzerentscheidung 14.09.2026: künftig WDB→Chat→JSON→Draft/Readback statt autonome Worker-/Auto-Publish-Strecke.

## PU-20260914-005 – Pferde Atelier Design – Pferderassen 1.50.500→1.50.507

- **Plugin-ID / Name:** `MOD-003` / Pferde Atelier Design (`affiliate-portal-template-kit`).
- **ART:** ENTWICKLUNG.
- **Herkunft:** EIGENENTWICKLUNG.
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/DESIGN/`.
- **VON_VERSION:** 1.50.499 als direkte Basis der Pferderassen-Strecke.
- **AUF_VERSION:** 1.50.507 aktueller Kandidat.
- **Quelle / Branch:** lokal erzeugte Paketkette; Campus-/Fachdokumentation `hobbyroom/glossar-livefail-red-green-20260913`; keine autoritativ gebundene Plugin-Source/Releasequelle der finalen Paketbytes.
- **WARUM:** Pferderassen-Übersicht und eigene `pa_breed`-Einzelansicht im Glossar-Prinzip, Suchintegration, Navigation, Factsheetdarstellung, Pagination.
- **Schnittstellen:** `pa_breed`, `pa_breed_group`, Header-AJAX mit `scope=pa_breed`, Featured Image als Hero/Vorschau.
- **relevante Fehlerquelle:** `../DESIGN/FEHLERQUELLEN.md` → `DESIGN-RASSEN-20260914`.
- **Paket 1.50.507:** `PFERDE_ATELIER_DESIGN_V1.50.507_AJAX_PAGINATION_BODYWIDTH_INSTALLIEREN.zip`.
- **SHA-256:** `b27898d26b32e9fe9910a2312b6bfbcec12c738f76290ed89304eca931353ec9`.
- **Positivprüfung exakt ZIP:** Contract 28/28 PASS; Runtime 28/28 PASS; PHP-Lint/ZIP/Struktur PASS.
- **Negativ/Mutation:** 11/11 absichtlich gebrochene Varianten ROT.
- **Regression:** normale Posts unverändert; Startseitenlimit 8; `pa_breed`-Scope; Featured-Image-Bindung; Pagination/AJAX geprüft.
- **LIVE-Readback:** lokale Rassen-AJAX-Suche PASS; `Alle Rassen` Pagination PASS; Pferderassen-Hero/Hauptsuchwelt zuvor PASS; **Einzelrassenbreite FAIL**.
- **Rollback-Referenz:** vorheriger Paketstand 1.50.506/1.50.505 als lokale Vorgänger; kein isoliertes CURRENT ersetzt.
- **ERGEBNIS:** **FAIL** für Gesamt-LIVE von 1.50.507; NEXT FIX ausschließlich reale Body-/Astra-/Kubio-Breite + generischen Hero-Kurztext entfernen.

## PU-20260914-006 – Pferde Atelier – Pferderassen Manager 0.2.0

- **Plugin-ID:** noch nicht zentral vergeben.
- **exakter Name:** `Pferde Atelier – Pferderassen Manager`.
- **ART:** UPDATE/ENTWICKLUNG.
- **Herkunft:** EIGENENTWICKLUNG.
- **zuständiges Fachbüro:** WDB `PFERDERASSEN` + Pluginbüro.
- **VON_VERSION:** 0.1.0.
- **AUF_VERSION:** 0.2.0.
- **WARUM:** Pferderassen vollständig von normalen Posts/Kategorien trennen; eigene Taxonomie `pa_breed_group`; kontrollierter WDB-ID→JSON→Draft→Readback-Weg.
- **Schnittstellen:** CPT `pa_breed`; Taxonomie `pa_breed_group`; WDB-Katalog 108 `breed-*`-IDs; JSON-Vertrag `PA_BREED_BATCH_V1`.
- **Paket:** `PFERDE_ATELIER_PFERDERASSEN_MANAGER_0.2.0_INSTALLIEREN.zip`.
- **SHA-256:** `1be279b2c90e2dfd3165c91bea876e82ee8ccf83e680b64e6157a8e4fce7fcd4`.
- **Positivprüfung exakt ZIP:** 35/35 PASS, 0 FAIL; 5er-Draftimport + Meta/Content/Slug/Taxonomie-Readback PASS; normales `post` unverändert.
- **Negativprüfung:** falscher Vertrag, unbekannte WDB-ID/Gruppe, Dubletten, unsicheres HTML, >25, Reimport, korrupter Readback/Batchrollback BLOCK/PASS.
- **Mutation:** 9/9 Schutzmutanten ROT.
- **Updateprüfung:** struktureller Install-over-0.1.0-Test PASS; PHP-Lint/ZIP-Integrität PASS.
- **LIVE:** reale `pa_breed`-Beiträge existieren; eine vollständige managerseitige LIVE-Abnahme/Releasebindung wurde in diesem Chat nicht als abgeschlossen belegt.
- **Backup/Rollback:** kein isoliertes CURRENT ersetzt; 0.1.0 bleibt historischer Vorgängerbeleg.
- **ERGEBNIS:** **BLOCKED** für isolierte CURRENT-/Releasefreigabe, weil autoritative Quell-/Releasebindung der 0.2.0-Paketbytes fehlt und vollständige LIVE-Abnahme offen ist.

## Aktuelle Fach-/Release-/LIVE-Autorität

Ausschließlich die zuständigen Fachquellen:
- Design: `../DESIGN/CURRENT_STATE.md`, `../DESIGN/HOBBYRAUM.md`, `../DESIGN/FEHLERQUELLEN.md`;
- Glossar: `../GLOSSAR/CURRENT_STATE.md`, `../GLOSSAR/HOBBYRAUM.md`, `../GLOSSAR/FEHLERQUELLEN.md`;
- Pferderassen-Fachwahrheit: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`.

Dieses Protokoll bleibt Kontrollpult und erzeugt keine zweite Fachwahrheit.