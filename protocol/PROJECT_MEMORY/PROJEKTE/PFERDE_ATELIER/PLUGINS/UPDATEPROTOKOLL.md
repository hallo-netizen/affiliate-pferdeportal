# PFERDE-ATELIER – PLUGINS – UPDATEPROTOKOLL

STAND: 2026-09-14
ROLLE: ZENTRALES PLUGIN-ÄNDERUNGSPROTOKOLL DES PFERDE-ATELIERS

## Grenze

Genau ein Vorgang je tatsächlicher Pluginentwicklung/-aktualisierung. Keine zweite Fach-, Release- oder LIVE-Wahrheit. Keine Secrets.

## PU-20260913-001 – Universal Glossary Engine – historischer RC

- Plugin-ID / Name: `MOD-008` / `Universal Glossary Engine`.
- damaliger Stand: `0.2.10-rc7`.
- technischer Artefakt-PASS historisch; nicht mit heutigem Glossarstand verwechseln.

## PU-20260914-001 – Glossar Core – aktueller lokaler Kandidat 1.3.0

- **Plugin-ID / exakter Name:** `MOD-008` / Pferde Atelier Glossar Core.
- **ART:** ENTWICKLUNG.
- **zuständiges Fachbüro:** `PROJEKTE/PFERDE_ATELIER/GLOSSAR/`.
- **VON_VERSION:** 1.2.3.
- **AUF_VERSION:** lokaler Kandidat `1.3.0`.
- **Paket:** `UNIVERSAL_GLOSSARY_ENGINE_1.3.0_AUTOMATION_SANDBOX_INSTALLIEREN.zip`.
- **SHA-256:** `b408756c63ab719fcf82131a6dd297c261e36817d957c69ceb9644d7ed8fd2a4`.
- **WARUM:** dynamischer Kandidatenpool, dauerhafte Sandbox, Automatiktrigger, Dubletten-/Kannibalisierungsprüfung, Research-Gate, Rückrelationen, sichere WordPress-Erstellung/-Aktualisierung und vorbereitete automatische Veröffentlichung.
- **PSTE-Abhängigkeit:** vorhandener Portal SEO Topic Engine-Pool wird lesend genutzt; kein zweiter DataForSEO-Pfad.
- **URF-Abhängigkeit:** vorhandene `URF_Core::sources()` können Quellen-Evidence liefern.
- **Sicherheitsmodus:** Standard `SANDBOX`, Auto-Publish AUS; Produktion nur bei `ARMED + auto_publish=true`.
- **Rollback:** Snapshot vor Bestandsupdate; Write-/Readback-/Publishfehler -> Quarantäne; Bestandsrollback.
- **Positiv/Negativ tatsächlich lokal ausgeführt:** PHP-Lint PASS; 16 Start-/Bestandsbegriffe PASS; 0 Bodylinks PASS; Dubletten/Synonyme/Kannibalisierung PASS; fehlende Quelle/Bodylink blockiert; Write-Failure Quarantäne; Readback-Failure Quarantäne + Rollback; Sandbox ohne Produktionswrite; Cron-Anlage PASS.
- **Batch:** 50 gültige Glossarbeiträge in EINEM simulierten WordPress-Publish-Lauf `50/50 PASS`.
- **Marker:** `CORE_130_PACK16_POS_NEG_PASS`, `AUTOMATION_130_STATIC_POS_NEG_PASS`, `AUTOMATION_130_POS_NEG_PASS`, `AUTOMATION_130_BATCH50_PASS`.
- **ZIP/Version:** ZIP-Lesetest PASS; Version 1.3.0 aus ZIP PASS.
- **Quelle / Releasequelle:** **BLOCKED** – lokaler Pluginquellstand ist noch nicht als autoritative Plugin-Source/Release gebunden; bestehendes `MOD-008/CURRENT.zip` deshalb nicht ersetzen.
- **LIVE:** OFFEN. Keine automatische Veröffentlichung vor realer Sandbox-/WordPress-Abnahme.
- **externe Textworker-Grenze:** direkte WordPress-Aufrufbarkeit der aktuellen Textmaschine/System-4/Codex-Laufzeit ist nicht nachgewiesen. Intake per Hook/REST ist vorbereitet; ohne gültiges Research-/Textpaket fail-closed.

## PU-20260914-002 – Pferde Atelier Design – aktueller lokaler Kandidat 1.50.493

- **Pluginordner:** `affiliate-portal-template-kit`; Hauptdatei `pferde-template-kit.php`.
- **ART:** ENTWICKLUNG.
- **zuständiges Fachbüro:** Glossar fachlich, Designintegration über Designbüro.
- **VON_VERSION:** 1.50.492.
- **AUF_VERSION:** lokaler Kandidat `1.50.493`.
- **Paket:** `PFERDE_ATELIER_DESIGN_V1.50.493_BREADCRUMB_SAME_PATH_INSTALLIEREN.zip`.
- **SHA-256:** `067e11f7d7f54ce22206955297566fbb78fdc9abd464075ebee4b82e7aed2a5d`.
- **WARUM:** Nutzerreadback: Breadcrumb-Abstand am Glossar-Single weiterhin falsch, obwohl andere Seiten korrekt sind.
- **nachgewiesene Ursache:** Glossar-Single benutzte einen eigenen verschachtelten Breadcrumb im Content-Container; normale Seiten verwenden den universellen Breadcrumb direkt unter `.site-content`.
- **Fix:** `uge_term` nutzt denselben universellen Breadcrumb-Ausgabepfad wie normale Seiten/Kategorien; eigener verschachtelter Single-Breadcrumb entfällt; keine neue Pixel-Sonderregel.
- **Positivprüfung:** gleicher `.site-content`-/Container-/Mounted-Reset-Pfad, korrekte Kette → PASS.
- **Negativprüfung:** alten `uge_term`-Guard absichtlich wieder eingebaut → Test rot; verschachtelten Single-Breadcrumb absichtlich wieder eingebaut → Test rot.
- **Marker:** `DESIGN_150493_BREADCRUMB_SAME_PATH_POS_NEG_PASS`.
- **ZIP/Version:** PHP-Lint PASS; ZIP-Lesetest PASS; Version 1.50.493 aus ZIP PASS.
- **Quelle / Releasequelle:** **BLOCKED** – lokaler Pluginquellstand noch nicht als autoritative Plugin-Source/Release gebunden.
- **LIVE:** OFFEN bis Installation/Readback.

## PU-20260914-003 – Pferde Atelier – Pferderassen Manager 0.1.0

- **Plugin-ID:** noch nicht zentral vergeben.
- **exakter Name:** `Pferde Atelier – Pferderassen Manager`.
- **ART:** NEUENTWICKLUNG.
- **Zweck:** Pferderassen-Beiträge im WordPress-Backend von normalen Beiträgen trennen und einen einfachen kontrollierten JSON→Draft-Produktionsweg bereitstellen.
- **Post Type:** `pa_breed`; normale WordPress-Beiträge bleiben getrennt.
- **Kategorien:** vorhandene WordPress-Kategoriehierarchie unter Pferderassen-Hauptkategorie ID `1482` wird weiterverwendet; keine zweite Frontend-Kategorielogik, keine automatische Kategorienanlage.
- **Produktionsregister:** gebündelter WDB-Katalog mit exakt `108` stabilen `breed-*`-IDs; technischer Quellen-Tree SHA `679b8a438f74954d39311c53b23aa526675593ac`.
- **Batchvertrag:** `PA_BREED_BATCH_V1`; maximal 25 Artikel pro Datei.
- **Pflichtfelder je Artikel:** `source_id`, `rassename`, `slug`, `rassengruppe_slug`, `titel`, `artikeltext`, `kurztext`, `meta_title`, `meta_description`.
- **Sicherheit:** unbekannte WDB-ID, Dublette, bestehender Slug, fehlende Rassengruppe, unsicheres HTML oder technischer Minimalinhalt → BLOCKED.
- **Write:** ausschließlich `post_status=draft`; kein Auto-Publish-Pfad.
- **Readback:** Titel, Slug, Inhalt, Kurztext, Metaangaben, WDB-ID und Kategorie werden nach dem WordPress-Write real zurückgelesen; Mismatch → kompletter neu angelegter Batch Rollback.
- **Produktionsstand:** `OFFEN / JSON_GEPRUEFT / DRAFT / DRAFT_READBACK_PASS / VEROEFFENTLICHT` wird aus Katalog + realem WordPress-Bestand abgeleitet.
- **lokaler Test:** 30/30 Positiv-/Negativtests PASS; 5er-Draftbatch PASS; normale Posts unverändert; Reimport blockiert; Readback-Fehler rollt vollständig zurück.
- **Mutationstest:** 7/7 absichtlich gebrochene Schutzvarianten wurden erkannt und liefen ROT (Publish statt Draft, WDB-Gate, Batch-Dublette, Gruppen-Gate, Readback-Gate, Batchlimit, HTML-Gate).
- **fertige ZIP:** komplette 30/30 Tests erneut gegen aus der ZIP extrahierte Bytes PASS; PHP-Lint PASS; ZIP-Stamm PASS.
- **Paket:** `PFERDE_ATELIER_PFERDERASSEN_MANAGER_0.1.0_INSTALLIEREN.zip`.
- **SHA-256:** `9d17bc68b56cd99f2a55764721fce46e54884b9d1edf9119e7d5d3ffac70ae5b`.
- **LIVE:** OFFEN. Installation, reale Gruppenauflösung und erster echter 5er-JSON-Batch müssen auf WordPress noch bewiesen werden.
- **Releasebindung:** noch nicht als autoritative CURRENT-Pluginquelle gebunden.

## Aktuelle Fach-/Release-/LIVE-Autorität

Ausschließlich:
- `../GLOSSAR/CURRENT_STATE.md`
- `../GLOSSAR/HOBBYRAUM.md`
- `../GLOSSAR/FEHLERQUELLEN.md`
- Pferderassen-Fachwahrheit: `../WISSENSDATENBANK/AKTENSCHRAENKE/PFERDERASSEN/`

Dieses Protokoll bleibt Kontrollpult und erzeugt keine zweite Fachwahrheit.
