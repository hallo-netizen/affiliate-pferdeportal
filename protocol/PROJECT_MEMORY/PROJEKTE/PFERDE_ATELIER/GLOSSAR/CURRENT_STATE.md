# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: LIVE TEILPASS / BREADCRUMB SINGLE LIVE PASS / DESIGN 1.50.493 LIVE PASS BREADCRUMB / AUTOMATION CORE 1.3.0 LOKAL HART PASS, LIVE-SANDBOXPRUEFUNG OFFEN

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Breadcrumb-Inhalt bei `Bandmaß`: korrekt `Startseite > Glossar > Pferd & Biologie > Bandmaß`.
- Breadcrumb-Position/Abstand nach Design `1.50.493`: **LIVE PASS 2026-09-14**. Nicht mehr anfassen.

## Breadcrumb – geschlossene Ursache

Die bisherigen 18-px-/Variable-Fixes griffen am falschen Punkt. Der Glossar-Single erzeugte seinen Breadcrumb **innerhalb des eigenen Content-/`.ast-container`-Pfads**, während normale Seiten den universellen Breadcrumb direkt unter `.site-content` mounten. Design `1.50.493` hat den Glossar-Single auf denselben universellen Breadcrumb-DOM-/CSS-Pfad umgestellt. Nutzerreadback 2026-09-14: **PASS**.

## Core 1.3.0 – dynamischer Glossarpool + dauerhafte Sandbox

Korrekt paketierter Installer: `UNIVERSAL_GLOSSARY_ENGINE_1.3.0_AUTOMATION_SANDBOX_INSTALLIEREN_KORREKT.zip`.

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

Breadcrumb ist LIVE PASS. **Automation 1.3.0 bleibt bis zur realen WordPress-Sandboxprüfung nicht LIVE freigegeben.** Automatische Veröffentlichung nicht aktivieren.

## Nächster realer Schritt

1. `Glossar -> Automation` öffnen.
2. `Sandbox hart testen` ausführen. Erwartung: Test PASS und **kein Produktionswrite**.
3. Danach `Pool jetzt aktualisieren` ausführen. Erwartung: Kandidaten sichtbar, keine Veröffentlichung.
4. Danach genau einen echten Kandidaten End-to-End mit Produktionsmodus AUS durchlaufen lassen.
5. Erst nach diesem Live-PASS Zeittrigger und Auto-Publish separat scharf schalten.
