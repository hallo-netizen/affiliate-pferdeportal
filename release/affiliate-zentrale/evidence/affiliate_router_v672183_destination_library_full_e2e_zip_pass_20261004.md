# Affiliate Router 6.72.183 – zentrale Banner-Ziel-URL-Sammelstelle – Full E2E ZIP PASS

Datum: 2026-10-04
Workstream: AFFILIATE_ZENTRALE
Version: 6.72.183

## KISS-Ziel

Die vorhandene Creative-Library ist die einzige Zuordnungsquelle fuer automatisch erzeugte Banner.

Ablauf:
1. Banner importieren.
2. Echte/decodierte Ziel-URL einmal auswerten, inklusive Domain.
3. Eindeutiges Portalziel speichern.
4. Technisch kompatible Banner-Slots einmal bei der Planung speichern.
5. Frontend nutzt nur die gespeicherte Zielkante.
6. Kein Zieltreffer -> allgemeiner technisch gueltiger Fallback.
7. Ziel-URL geaendert -> alte Zielkante wird geloescht und neu berechnet.

Keine zweite Datenbank, keine Provider-Sonderlogik, keine Frontend-Neuklassifikation.

## Root Causes

- Die Creative-Library besass destination_url und topic_targets bereits, war aber nicht die alleinige Zuordnungsautoritaet.
- Asset-Verifikation setzte topic_targets wieder auf [] und konnte damit eine Zuordnung entfernen.
- Ziel-URL-Semantik beruecksichtigte Host/Domain nicht.
- Reine Tracking-Fallback-URLs konnten wie echte Zielseiten in spaetere Semantik gelangen.
- Automatisch materialisierte Banner wurden im Frontend erneut aus URL/Text/Partnerdaten interpretiert.

## Fix

Geaendert wurden nur:
- includes/trait-ppar-creative-library.php
- includes/trait-ppar-output-objects.php
- pferdeportal-affiliate-router.php
- readme.txt

Creative-Library:
- speichert destination_source = provider_explicit | decoded_tracking | tracking_fallback | unknown;
- echte Ziel-URL inkl. Domain wird einmal klassifiziert;
- topic_targets speichert pro Portal state=mapped|general, Zielkante, Level, kompatible Slots und Ziel-URL-Provenienz;
- unveraenderte Quelle behaelt die gespeicherte Kante;
- geaenderte Ziel-URL leert die alte Kante und erzwingt Neuplanung;
- Asset-Verifikation loescht topic_targets nicht mehr.

Materialisierung:
- eindeutige Ziel-URL -> gespeicherte Portal-Zielkante;
- kein/mehrdeutiges Ziel -> allgemeiner Fallback ohne Fake-Thema;
- technisch kompatible Banner-Slots werden einmal gespeichert;
- falsche Geometrie bleibt ausgeschlossen.

Frontend:
- output_object_v4-Banner werden nicht mehr aus Ziel-URL/Titel/Partnertext neu klassifiziert;
- gespeicherte Zielkante -> exakt / Themenkreis;
- allgemeiner Library-Fallback -> allgemeine Stufe;
- sonst letzter technisch gueltiger Fallback;
- Rassenlogik bleibt themenneutral.

## Source Full E2E

Run: 37219933282
Result: SUCCESS

- Source manifest 27/27 byte identity: PASS
- PHP lint: PASS
- Performance hardlock: PASS
- bestehender kompletter Bannerpfad: 21/21 PASS
- Ziel-URL-Sammelstelle Import -> Library -> Materialisierung -> Renderer -> HTML: 26/26 PASS
- bestehender Banner -> gespeicherte Schabracken-Kante: PASS
- zukuenftiger Banner -> automatische Reithelme-Kante: PASS
- tracking-only -> allgemeiner Fallback: PASS
- kein Fake-Thema beim Fallback: PASS
- falsche Geometrie blockiert: PASS
- Ziel-URL-Wechsel loescht alte Kante und berechnet neue: PASS
- Frontend 1000 Ranking-Aufrufe: 0 zusaetzliche DB-Queries, 0 HTTP: PASS
- irrefuehrende destination_url nach Materialisierung wird im Frontend ignoriert: PASS

Der vorherige Source-Run 37219856503 war ausschliesslich wegen einer ungueltigen .test-Testadresse rot; das Plugin blockierte diese korrekt. Testdaten wurden auf gueltige URLs korrigiert, danach kompletter PASS.

## Installiertes ZIP Full E2E

Run: 37220236448
Result: SUCCESS

- ZIP 27/27 manifest byte identity: PASS
- Performance hardlock: PASS
- ZIP PHP lint 21/21: PASS
- frische WordPress 7.1.2 + MariaDB 10.11 Installation: PASS
- ZIP plugin active 6.72.183: PASS
- alter kompletter Bannerpfad: 21/21 PASS
- neue Ziel-URL-Sammelstelle: 26/26 PASS
- ZIP_FULL_DESTINATION_LIBRARY_WORDPRESS_MARIADB_E2E_PASS

## Performance

- geschuetzte 6.72.182/6.72.171 Fastpaths unveraendert;
- campaign_match_rank() enthaelt keine neue DB-Abfrage, kein get_post_meta(), keinen Remote-Aufruf;
- neue Zuordnungsarbeit liegt ausschliesslich in Import/Planung;
- output_object_v4-Banner ueberspringen spaetere URL-/Text-Neuklassifikation im Frontend;
- gemessener neuer Rankingpfad: 1000 Aufrufe -> 0 DB, 0 HTTP.

## Installer

Path:
release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.183.zip

SHA-256:
3f689f076efc4318ed1188b86e51e66410f193d5256de7ddc54a91dc4aab6895

Bytes:
791323

Git blob:
b3fc195c684c6eb11d567ab63637acf0481308d6

Artifact commit/head after publish:
f71f9e235d3916979497b46a3b4b51202667be93

## Status

SOURCE_FULL_E2E_PASS
ZIP_FULL_E2E_PASS
PERFORMANCE_HARDLOCK_PASS
INSTALLER_BUILT_AND_COMMITTED
LIVE_PRODUCTION_INSTALL_NOT_RUN
