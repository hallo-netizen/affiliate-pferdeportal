# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-14
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero
STATUS: damaliger Hero-Abstand LIVE PASS; Breadcrumb-Position separat in 011.

## GLOSSAR-FE-002 – Hero-Bild / Ausschnitt / Übergang
STATUS: letzter Nutzerreadback vor 1.50.492 LIVE FAIL; 1.50.492 lokal positiv/negativ geprüft, neuer LIVE-Readback noch offen.

Nicht mit dem Breadcrumb-Fix vermischen.

## GLOSSAR-ROUTE-004 – Einzelbegriffe öffnen
STATUS: LIVE PASS.
Nicht anfassen.

## GLOSSAR-SINGLE-011 – Breadcrumb Single
STATUS: **LIVE FAIL / Design 1.50.493 lokal hart POSITIV+NEGATIV PASS / LIVE-READBACK OFFEN**

### LIVE bereits bestätigt
- Breadcrumb-Inhalt: `Startseite > Glossar > Oberbereich > Begriff` korrekt.
- Fließtext 0 Links: PASS.
- rechte Ockerlinie dünn: PASS.

### Tatsächliche Ursache

Der sichtbare Abstand ließ sich mit der zentralen Abstandsvariable allein nicht beheben, weil Glossar-Single und normale Seiten **nicht denselben Breadcrumb-Ausgabepfad** nutzten:
- normale Seiten: universeller Breadcrumb wird direkt unter `.site-content` gemountet;
- Glossar-Single: eigener Breadcrumb wurde innerhalb des Glossar-Content-/`.ast-container`-Pfads gerendert und der universelle Breadcrumb war dort gesperrt.

Daher waren 18-px-/Variable-Korrekturen am Glossar-Single unzureichend.

### Kandidat 1.50.493
- `uge_term` darf durch den universellen Breadcrumb-Payload laufen;
- gleicher `.site-content`-/Container-/Mounted-Reset-Pfad wie normale Seiten;
- verschachtelter Single-Breadcrumb entfernt;
- keine neue Pixel-Sonderregel.

Harte lokale Prüfung:
- PHP-Lint PASS;
- gleicher Seitenpfad PASS;
- Breadcrumb-Kette PASS;
- NEGATIV alter Single-Guard -> Test rot PASS;
- NEGATIV verschachtelter Single-Breadcrumb -> Test rot PASS;
- Marker `DESIGN_150493_BREADCRUMB_SAME_PATH_POS_NEG_PASS`.

Paket: `PFERDE_ATELIER_DESIGN_V1.50.493_BREADCRUMB_SAME_PATH_INSTALLIEREN.zip`
SHA-256: `067e11f7d7f54ce22206955297566fbb78fdc9abd464075ebee4b82e7aed2a5d`

## GLOSSAR-AUTO-013 – dynamischer Kandidatenpool / Sandbox / Auto-Publish
STATUS: **Core 1.3.0 lokal hart PASS / LIVE und externe Textworker-Bindung OFFEN**

### Implementiert
- persistenter Kandidatenpool;
- PSTE-Retained-Pool lesend, bounded;
- Artikel-Kandidaten-Meta;
- Dubletten/Synonyme;
- Kannibalisierungs-Quarantäne;
- Quellen-Evidence über vorhandene URF-Quellen;
- Research-/Textpaket-Gate;
- Relationen und Rückrelationen;
- Update vorhandener Begriffe mit gleicher ID;
- Snapshot/Readback/Rollback;
- dauerhafte Sandbox `Glossar -> Automation`;
- manueller Start + WP-Cron;
- Auto-Publish nur ARMED + Schalter AN.

### Harte Tests
- 16 gebundene Begriffe 150–200 Wörter / 0 Bodylinks PASS;
- normaler WP-Post Negativtest unverändert PASS;
- Dublette/Synonym/Kannibalisierung Negativfälle PASS;
- fehlende Quelle/Bodylink blockiert PASS;
- Write-Fehler -> Quarantäne PASS;
- Readback-Korruption -> Quarantäne + Rollback PASS;
- Sandbox -> kein Produktionswrite PASS;
- **50 gültige Beiträge in einem simulierten WordPress-Lauf: 50/50 PASS**.

Marker:
- `CORE_130_PACK16_POS_NEG_PASS`
- `AUTOMATION_130_STATIC_POS_NEG_PASS`
- `AUTOMATION_130_POS_NEG_PASS`
- `AUTOMATION_130_BATCH50_PASS`

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.3.0_AUTOMATION_SANDBOX_INSTALLIEREN.zip`
SHA-256: `b408756c63ab719fcf82131a6dd297c261e36817d957c69ceb9644d7ed8fd2a4`

### Fail-closed Grenze

Die bestehende externe Textmaschine/System-4/Codex-Laufzeit ist bislang nicht als direkt von WordPress aufrufbare Research-/Text-API nachgewiesen. Das Glossar darf deshalb keine fachliche Recherche oder Formulierung vortäuschen. Ohne gültiges Paket bleibt der Kandidat wartend/blockiert. Intake vorbereitet über `uge_automation_research_package` oder REST `/wp-json/uge/v1/automation/package`.

## PASS-GRENZE

Kein LIVE PASS für 1.50.493 / 1.3.0 vor Installation und realem Readback. Auto-Publish bis dahin AUS/SANDBOX.
