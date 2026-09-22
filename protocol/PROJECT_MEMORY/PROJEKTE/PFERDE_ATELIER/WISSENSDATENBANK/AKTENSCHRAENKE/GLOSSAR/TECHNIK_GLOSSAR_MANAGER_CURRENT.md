# TECHNIK – GLOSSAR MANAGER CURRENT

STAND: 2026-09-15
STATUS: LOKAL HART PASS / LIVE OFFEN

## AKTUELLER KANDIDAT

Core:
`UNIVERSAL_GLOSSARY_ENGINE_1.4.0_SAFE_MANAGER_RELATIONS_REVIEW_INSTALLIEREN.zip`

SHA-256:
`fb75ff8044eff4383ba44dd6389b1aa97ff16ab500445037ce2d5819f2335231`

Design:
`PFERDE_ATELIER_DESIGN_V1.50.528_GLOSSAR_RELATIONS_DESIGN_INSTALLIEREN.zip`

SHA-256:
`d1487e69bfbf54e0e58ccd83b938223ea2c0f9ebafb4b6e688372605eec56f3e`

Persistente Ausgabekopien:
- `/Campus-Plugins/PFERDE_ATELIER/GLOSSAR/`
- `/Campus-Plugins/PFERDE_ATELIER/DESIGN/`

## ARCHITEKTURENTSCHEIDUNG

Die alte autonome Glossar-Discovery-/Cron-/Loopback-Automation ist ab 1.4.0 **nicht mehr aktiver Produktionsweg**.

Historisch belegte LIVE-Probleme der Automationslinie:
- `REFRESH_LIMIT_REACHED`
- festhängender `RUNNING / RETAINED`
- `PLANNING` mit `Planning-Seiten 0`
- Abhängigkeit von erneutem WP-Cron-/Request-Antrieb

Die alte Automationsklasse bleibt nur als historischer Quellbestand im Paket und wird nicht geladen oder initialisiert. Der bisherige Content-Pack-Autopublisher wird ebenfalls nicht mehr initialisiert.

## NEUER PRODUKTIONSWEG

Vorbild: Pferde Atelier Pferderassen Manager.

`Campus → Research/Text → PA_GLOSSARY_BATCH_V2 → JSON-Staging → Validator → WordPress-Draft → Readback → PASS/ROLLBACK`

### Harte Regeln
- maximal 25 neue Begriffe je Batch
- stabile `term-*`-ID
- genau eine gültige Themenwelt (`uge_group`)
- 150–200 Wörter
- Kurzdefinition Pflicht
- verwandte Begriffe + Slugs Pflicht
- SEO-Titel + Description Pflicht
- Quellen Pflicht
- `last_verified_at` Pflicht
- Prüfintervall nur 6/12/24 Monate
- Hauptseite optional: `page` oder `category`
- Bodylinks blockiert
- unsicheres HTML blockiert
- bestehende ID/Slug blockiert bei Neuanlage
- Importstatus immer `draft`
- Staging-Hash vor Write erneut prüfen
- Feld-/Taxonomie-Readback nach Write
- Readback-Mismatch → kompletter neuer Batch-Rollback
- kein Auto-Publish

## BESTANDSMIGRATION

Die 16 bekannten Start-/Bestandsbegriffe erhalten beim ersten Adminlauf ausschließlich fehlende Beziehungs-/Prüfmetadaten:
- vorhandene primäre Themenwelt
- verwandte Begriffe + Slugs
- Prüfdatum, falls leer
- Prüfintervall, falls leer

Keine Fachtexte werden dabei geändert. Kein Beitragsstatus wird geändert.

## REGELMÄSSIGE AKTUALISIERUNG

Backend: `Glossar → Prüfbedarf`.

Fälligkeit wird dynamisch aus `last_verified_at + review_interval_months` berechnet. Die Liste ist read-only und erzeugt keine automatische Textänderung. Fällige Begriffe müssen erneut durch Recherche, Validator und kontrollierten WordPress-Weg.

## FRONTEND 1.50.528

Rechte Spalte der Glossar-Einzelseite:
1. `Themenwelt`
2. `Verwandte Begriffe`
3. optional `Mehr zum Thema`

Vorhandene verwandte Glossarbegriffe werden verlinkt. Noch nicht vorhandene Relationstermine bleiben sichtbar, aber unverlinkt; keine URL wird geraten.

## LOKALE PRÜFUNG

Core:
- Runtime-Stubs: gültiger Batch, Stage, Draft-Import, Themenwelt-/Related-Readback PASS
- Negativ: Bodylink, Related fehlt, Wortzahl, falsche Themenwelt, falscher Contract PASS/BLOCK
- absichtlich korrupter Readback → BLOCK + kompletter Rollback PASS
- autonome Automation nicht aktiv PASS
- Content-Pack-Autopublisher nicht aktiv PASS
- PHP-Lint PASS
- ZIP PASS
- Install-over-1.3.8 PASS

Design:
- Themenwelt/Related/Hauptseite-Vertrag PASS
- Mutation: Themenwelt oder Related entfernt → ROT erkannt
- PHP-Lint PASS
- 501/501 Dateien, nur `pferde-template-kit.php` geändert
- ZIP PASS
- Install-over-1.50.527 PASS

## LIVE-GRENZE

Kein LIVE-PASS vor Installation und echtem WordPress-Readback.
