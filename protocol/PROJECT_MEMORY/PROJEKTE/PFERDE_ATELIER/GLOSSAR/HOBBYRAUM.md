# GLOSSAR – HOBBYRAUM

STAND: 2026-09-14
STATUS: BLOCKED BIS LIVE-READBACK

## LIVE PASS – NICHT ANFASSEN
- Einzelbegriffe öffnen.
- 0 Links im Glossar-Fließtext.
- dünne Ockerlinie rechts.

## BREADCRUMB – ECHTE URSACHE

Der Single-Breadcrumb lief nicht über denselben DOM-Pfad wie normale Seiten: Glossar-Single renderte einen eigenen Breadcrumb innerhalb des Content-Containers; normale Seiten nutzen den universellen Breadcrumb direkt unter `.site-content`. Deshalb waren die vorherigen Abstandswerte keine belastbare Lösung.

### Design 1.50.493
`PFERDE_ATELIER_DESIGN_V1.50.493_BREADCRUMB_SAME_PATH_INSTALLIEREN.zip`
SHA-256: `067e11f7d7f54ce22206955297566fbb78fdc9abd464075ebee4b82e7aed2a5d`

- Single benutzt nun exakt den universellen Seiten-Breadcrumb-Pfad.
- eigener verschachtelter Single-Breadcrumb entfernt.
- lokale positive/negative Prüfung PASS.
- Marker `DESIGN_150493_BREADCRUMB_SAME_PATH_POS_NEG_PASS`.

## AUTOMATION-SANDBOX – CORE 1.3.0
`UNIVERSAL_GLOSSARY_ENGINE_1.3.0_AUTOMATION_SANDBOX_INSTALLIEREN.zip`
SHA-256: `b408756c63ab719fcf82131a6dd297c261e36817d957c69ceb9644d7ed8fd2a4`

WordPress: `Glossar -> Automation`.

Dort dauerhaft erreichbar:
- `Pool jetzt aktualisieren`
- `Sandbox hart testen`
- `Automatiklauf jetzt starten`
- Intervall stündlich / 2× täglich / täglich
- Batch 1..100, Standard 25
- Produktionsschalter `ARMED`
- Auto-Publish-Schalter

Standard nach Installation: **SANDBOX + Auto-Publish AUS**.

Automatisiert implementiert:
`PSTE-Pool lesen -> Kandidaten -> Dublette/Synonym -> Kannibalisierung -> Quellen-Evidence -> Research-Paket-Gate -> Relationen/Rückrelationen -> WP-Write -> Readback -> Publish oder Quarantäne/Rollback`.

## HARTE TESTS
PASS:
- PHP-Lint Core/Design.
- 16 Start-/Bestandsbegriffe 150–200 Wörter, 0 Bodylinks.
- normaler WP-Post Negativtest unverändert.
- Dubletten-/Synonym-/Kannibalisierungs-Negativfälle.
- fehlende Quelle/Bodylink blockiert.
- Write-Fehler -> Quarantäne.
- Readback-Fehler -> Quarantäne + Rollback.
- Sandbox ohne Produktionswrite.
- Cron-Anlage.
- **50/50 Glossarbeiträge in einem simulierten WP-Publish-Lauf PASS**.

Marker:
- `CORE_130_PACK16_POS_NEG_PASS`
- `AUTOMATION_130_STATIC_POS_NEG_PASS`
- `AUTOMATION_130_POS_NEG_PASS`
- `AUTOMATION_130_BATCH50_PASS`

## HARTE GRENZE

Nicht vortäuschen: Die aktuelle Textmaschine/System-4/Codex-Laufzeit wurde noch nicht als direkt aus WordPress aufrufbarer Worker nachgewiesen. Core 1.3.0 hat deshalb einen fail-closed Übergabepunkt per Filter/REST. Ohne gültiges Research-/Textpaket wird **nicht** veröffentlicht.

## NEXT ACTION EXAKT
1. Core 1.3.0 installieren.
2. Design 1.50.493 installieren.
3. `Bandmaß` LIVE prüfen – Breadcrumb-Abstand gegen normale Seite.
4. `Glossar -> Automation` öffnen.
5. `Sandbox hart testen`; `production_write_performed=false` prüfen.
6. Pool aktualisieren; keine Produktion scharf schalten.
7. erst nach LIVE-Abnahme den externen Text-/Research-Worker an den vorbereiteten Intake binden und erneut Ende-zu-Ende testen.

## NICHT ANFASSEN
- funktionierendes Routing;
- normale Posts/Seiten;
- 0-Link-Regel;
- dünne Ockerlinie;
- Produktionsschalter vor Abnahme.
