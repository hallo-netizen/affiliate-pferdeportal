# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: FRONTEND TEILWEISE LIVE BESTÄTIGT / ALTER AUTOMATIONSPFAD ABGELÖST / NEUER JSON-IMPORTER-Umbau OFFEN

## AUTORITÄT

Diese Datei ist die einzige aktuelle Standzusammenfassung des Glossar-Büros.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `FEHLERQUELLEN.md`
- verbindliche Produktionsregeln → `PRODUKTIONSREGELN.md`
- lokale WAS/WARUM-Entscheidungen → `ENTSCHEIDUNGEN_20260914.md`
- Fachwahrheit → `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
- Zielvertrag → `ZIELVERTRAG_GLOSSAR_ABDECKUNG_V1.md`

## LIVE bestätigt – nicht regressieren

- Glossar-Einzelbegriffe öffnen: PASS.
- Fließtext: 0 Links – PASS.
- rechte Ocker-Oberkante dünn – PASS.
- Glossar-Breadcrumb-Abstand – LIVE PASS.
- Glossar-Hero – LIVE PASS.
- Hauptsuche enthält eigene Welt `Glossar` – LIVE PASS.
- Produktion/Auto-Publish bleiben AUS.

## Fachbasis

Der zentrale Glossar-Aktenschrank existiert bereits unter:
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`

Dort liegen die quellengebundenen Begriffsdaten. Diese WDB bleibt alleinige Fachwahrheit. WordPress/JSON erzeugen keine zweite Fachdatenbank.

## Architekturentscheidung 2026-09-14

Der bisherige autonome Produktionsweg mit PSTE-Discovery, Retained/Planning, Research-Paket, Cron/Loopback-Worker und Auto-Publish ist **abgelöst**.

Grund:
Die technische Automationskette wurde immer komplexer, obwohl die eigentliche Textproduktion nicht als einfache geschlossene Strecke eingebunden war. Der Nutzer hat deshalb verbindlich entschieden, das Glossar analog zum Pferderassen-Manager zu produzieren.

Neuer Zielweg:

`WDB-Aktenschrank -> Chat erstellt fertige Glossarbeiträge -> JSON-Batch -> Glossar-Importer validiert -> WordPress-Draft -> Readback -> gesonderte Freigabe`

Kein Auto-Publish als Normalweg.

## Historischer Core 1.3.5–1.3.8

- 1.3.5 LIVE FAIL: künstliches 400er-Limit.
- 1.3.6 LIVE FAIL: Planning konnte verdrängt werden.
- 1.3.7 LIVE FAIL: Phase PLANNING, aber Worker hing an WP-Cron.
- 1.3.8 lokal hart positiv/negativ/mutation PASS; LIVE nie abgenommen.

1.3.8 ist **nicht mehr NEXT ACTION**. Diese Kette bleibt nur technische Historie.

## Neuer Plugin-Umbau – OPEN

Das bestehende Glossar-Plugin muss importerorientiert neu aufgebaut werden, konzeptionell analog `Pferde Atelier – Pferderassen Manager 0.2.0`:
- fester JSON-Batchvertrag;
- stabile `term-*`-WDB-IDs;
- Draft-only Write;
- Bestandsupdate statt Löschen;
- definierter WordPress-Readback;
- Rollback/BLOCK bei Mismatch;
- Relations-/Portalzielprüfung;
- normale Posts/Pages unverändert;
- keine Pferderassen im Glossar.

## Testgrenze

Für diesen neuen Importer wurden in diesem Chat **noch keine Pluginbytes gebaut oder getestet**.

Daher:
- kein PASS für den neuen Glossar-Produktionsweg;
- kein neues Glossar-Core-`CURRENT.zip`;
- alter MOD-008-`CURRENT.zip` nicht als neuen Fachstand interpretieren.

## NEXT ACTION

Siehe ausschließlich `HOBBYRAUM.md`.