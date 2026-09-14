# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: LIVE TEILPASS / BREADCRUMB SINGLE LIVE FAIL / DESIGN 1.50.493 LOKAL HART PASS / AUTOMATION CORE 1.3.0 LOKAL HART PASS, SANDBOX

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Breadcrumb-Inhalt bei `Bandmaß`: korrekt `Startseite > Glossar > Pferd & Biologie > Bandmaß`; nur Position/Abstand ist LIVE noch falsch.

## Breadcrumb – tatsächliche Ursache

Die bisherigen 18-px-/Variable-Fixes griffen am falschen Punkt. Der Glossar-Single erzeugte seinen Breadcrumb **innerhalb des eigenen Content-/`.ast-container`-Pfads**, während normale Seiten den universellen Breadcrumb direkt unter `.site-content` mounten. Deshalb konnte der Single trotz gleicher CSS-Variable sichtbar einen anderen Abstand haben.

### Design-Kandidat 1.50.493

Paket: `PFERDE_ATELIER_DESIGN_V1.50.493_BREADCRUMB_SAME_PATH_INSTALLIEREN.zip`

SHA-256: `067e11f7d7f54ce22206955297566fbb78fdc9abd464075ebee4b82e7aed2a5d`

Fix:
- `uge_term` wird nicht mehr vom universellen Breadcrumb-Payload ausgeschlossen;
- `uge_term` benutzt denselben universellen Breadcrumb-DOM-/CSS-Pfad wie normale Seiten/Kategorien;
- eigener verschachtelter Single-Breadcrumb wird nicht mehr ausgegeben;
- keine neue Glossar-Pixel-Sonderregel als Ersatz.

Hart lokal:
- PHP-Lint PASS;
- gleicher `.site-content`-/Container-/Mounted-Reset-Pfad PASS;
- Kette `Glossar > Oberbereich > Begriff` PASS;
- NEGATIV: alten `uge_term`-Guard wieder eingebaut → Test rot PASS;
- NEGATIV: verschachtelten Single-Breadcrumb wieder eingebaut → Test rot PASS;
- Marker `DESIGN_150493_BREADCRUMB_SAME_PATH_POS_NEG_PASS`;
- ZIP/Version PASS.

## Core 1.3.0 – dynamischer Glossarpool + dauerhafte Sandbox

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.3.0_AUTOMATION_SANDBOX_INSTALLIEREN.zip`

SHA-256: `b408756c63ab719fcf82131a6dd297c261e36817d957c69ceb9644d7ed8fd2a4`

Enthalten:
- persistenter Kandidatenpool;
- bestehender PSTE-Retained-/Planning-Pool wird **lesend** und begrenzt eingelesen; keine zweite DataForSEO-Pipeline;
- zusätzliche Artikel-Kandidaten über `_uge_glossary_candidates`;
- Dubletten-/Synonymprüfung;
- Kannibalisierungs-Quarantäne;
- Quellen-Evidence über vorhandene `URF_Core::sources()` sofern konfiguriert;
- Research-/Textpaket-Gate fail-closed;
- neue und rückwirkende Relationen;
- bestehende Glossarbeiträge werden per gleicher ID aktualisiert, nicht dupliziert;
- Snapshot → Write → Readback → bei Fehler Quarantäne/Rollback;
- dauerhafte WordPress-Sandbox unter `Glossar -> Automation`;
- manuelle Aktionen: Pool aktualisieren / Sandbox testen / Automatiklauf;
- WP-Cron: stündlich, 2× täglich oder täglich;
- Standardbatch 25, technisch 1..100 pro Lauf;
- automatische Veröffentlichung nur wenn **ARMED + Auto-Publish AN**; Standard ist SANDBOX/AUS;
- REST-Status und Research-Package-Intake für einen externen Text-/Research-Worker.

Hart lokal:
- Core PHP-Lint PASS;
- 16 gebundene Start-/Bestandsbegriffe: 150–200 Wörter, 0 Bodylinks, Relationsvertrag PASS;
- bestehende Glossar-ID erhalten; normaler WP-Post im Negativtest unverändert;
- Dublette, Synonym, Kannibalisierung, fehlende Quelle, Bodylink → korrekt blockiert;
- Write-Failure → Quarantäne;
- Readback-Korruption → Quarantäne + Rollback;
- Sandbox schreibt nicht in Produktion;
- Cron-Anlage PASS;
- **50 gültige Glossarbeiträge in EINEM simulierten WordPress-Publish-Lauf: 50/50 PASS**.

Marker:
- `CORE_130_PACK16_POS_NEG_PASS`
- `AUTOMATION_130_STATIC_POS_NEG_PASS`
- `AUTOMATION_130_POS_NEG_PASS`
- `AUTOMATION_130_BATCH50_PASS`

## Automationsgrenze – nicht raten

Kandidatenfindung, Pool, Gates, Relationen, WordPress-Write/Readback/Rollback und automatische Veröffentlichung sind implementiert und lokal testbar.

Für **vollautomatische fachliche Recherche + Textformulierung** fehlt noch eine nachgewiesene direkt aufrufbare Verbindung vom WordPress-Glossar zur aktuellen externen Textmaschine/System-4/Codex-Laufzeit. Deshalb erfindet Core 1.3.0 hier keinen Worker: ohne gültiges Research-/Textpaket bleibt ein Kandidat fail-closed in Recherche/Wartezustand. Der Übergabepunkt ist vorbereitet (`uge_automation_research_package` bzw. REST `/wp-json/uge/v1/automation/package`).

## Harte Grenze

**Kein LIVE-PASS für 1.3.0 oder 1.50.493 vor Installation und realem Readback.** Sandbox bleibt bis zur Abnahme unscharf; automatische Veröffentlichung nicht aktivieren.

## Nächster realer Readback

1. Core `1.3.0` installieren.
2. Design `1.50.493` installieren.
3. `Bandmaß` öffnen: Breadcrumb muss jetzt über denselben Seitenpfad wie normale Seiten stehen.
4. `Glossar -> Automation` öffnen: Sandbox muss jederzeit erreichbar sein.
5. `Sandbox hart testen` ausführen; `production_write_performed=false` muss bleiben.
6. `Pool jetzt aktualisieren`: PSTE-/Artikel-Kandidaten sichtbar, keine Veröffentlichung.
7. Erst nach realem PASS Produktionsmodus separat freigeben.
