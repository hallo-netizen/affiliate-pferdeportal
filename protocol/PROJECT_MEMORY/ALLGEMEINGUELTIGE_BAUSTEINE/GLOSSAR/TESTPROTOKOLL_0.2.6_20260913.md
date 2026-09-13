# MOD-008 – TESTPROTOKOLL 0.2.6

STAND: 2026-09-13
STATUS: TECHNISCHER KANDIDAT HARDTEST PASS / KEIN LIVE-PASS

## GEBUNDENER STAND

Branch:
`hobbyroom/glossar-026-upgrade-hardtest-20260913`

Workflow:
`Glossar 0.2.6 Fresh + Upgrade Hardtest`

Autoritativer Run:
`34748541630`

Commit des geprüften Runs:
`e5f8c8ce1839a69f3e6fb712bd4a3d4a3e8ad059`

## KANDIDATENBAU

0.2.6 wird deterministisch aus dem bereits geprüften 0.2.5-Stand gebaut.

Erlaubtes Delta exakt:
- `universal-glossary-engine.php`: Versionsnummer 0.2.5 → 0.2.6;
- `includes/class-uge-core.php`: Rewrite-Schema 4 → 5.

Alle übrigen Dateien müssen bytegleich zum getesteten 0.2.5-Kandidaten bleiben.

Marker:
`UGE026_DELTA_GUARD_PASS ['includes/class-uge-core.php', 'universal-glossary-engine.php']`

PHP-Lint aller Plugin-PHP-Dateien: PASS.

## FRESH-INSTALL – POSITIV / NEGATIV

Job:
`103700782149`

PASS:
- WordPress + MySQL + Astra Boot;
- Pluginversion 0.2.6;
- Rewrite-Schema nach Aktivierung 5;
- Policy-/Seed-Matrix;
- Startseite / 10 Themenicons;
- alle gerenderten Kartenlinks;
- AJAX Term-only positiv und ungültiger Nonce negativ;
- Breadcrumb-/Routing-Kollision;
- primäre Portal-Kategorie-Verlinkung;
- A–Z;
- Draft nicht öffentlich;
- Preview;
- Duplikatsperre;
- normaler WordPress-Beitrag unverändert;
- echter Einzelbegriff muss Artikelmarkup + H1 enthalten, nicht nur HTTP 200;
- Hero-Abstand-Regel;
- responsive Hero-Regel;
- Breadcrumb-Achse.

Endmarker:
`UGE026_FRESH_VERSION=0.2.6`
`UGE026_FRESH_SCHEMA=5`
`UGE026_FRESH_INSTALL_POSITIVE_NEGATIVE_PASS`

## ECHTES IN-PLACE-UPDATE 0.2.5 → 0.2.6

Job:
`103700782306`

### Negativer Vorzustand

Unter aktivem 0.2.5 wurde die Einzelbegriff-Rewrite-Regel gezielt aus der gespeicherten Rewrite-Tabelle entfernt.

Bewiesen:
- vorher bekannter Einzelbegriff funktioniert;
- danach `/glossar/begriff/hufbein/` = 404;
- gespeichertes Rewrite-Schema bleibt 4.

Marker:
`UGE025_SCHEMA_BEFORE=4`
`UGE025_SCHEMA_AFTER_POISON=4`
`UGE025_POISONED_REWRITE_NEGATIVE_PASS`

### Echter WordPress-Updater

0.2.6 wurde über den WordPress-Plugin-Updater mit Überschreiben installiert, nicht durch Rohkopie in einen laufenden PHP-Prozess.

Bewiesen:
- installierter Header = 0.2.6;
- installierter Core = Rewrite-Schema 5;
- gespeicherte DB vor erstem neuen Request = 4;
- erster normaler Webrequest migriert 4 → 5;
- Rewrite-Regel `glossar/begriff` wieder vorhanden;
- Hufbein anschließend 200 + echtes Glossar-Artikelmarkup + Inhalt.

Marker:
`UGE026_SCHEMA_PRE_UPDATE=4`
`UGE026_SCHEMA_PRE_FIRST_NEW_REQUEST=4`
`UGE026_SCHEMA_POST_REQUEST=5`
`UGE026_WORDPRESS_UPDATE_REWRITE_MIGRATION_PASS`

### Positiv-/Negativmatrix nach Upgrade

PASS:
- alle Kartenlinks → echte Glossar-Artikelseite;
- unbekannter Begriff → 404;
- Entwurf → 404;
- Legacy-URL → 301;
- Kategorie und gleichnamiger Glossarbegriff bleiben getrennt;
- ungültiger AJAX-Nonce nicht 200;
- normaler WordPress-Beitrag bleibt normal;
- Datenmenge und Konfiguration unverändert;
- Frontend-Abnahme Hero/Breadcrumb PASS;
- Deaktivieren/Reaktivieren erhält Schema 5 und Route;
- komplette alte Frontend-/Regression-/Acceptance-Matrix nach Upgrade erneut PASS.

Endmarker:
`UGE026_UPGRADED_FULL_MATRIX_PASS`

## GATED PACKAGE

Job:
`103700913568`

Der Paketjob durfte erst nach PASS von Fresh-Install UND In-place-Upgrade starten.

Inneres Plugin-ZIP:
`universal-glossary-engine-0.2.6.zip`

SHA-256:
`e0717db3aa247edc30b0fe84a261aa59037050d593e3432a6fb460f6d96f3b09`

Actions-Artefakt-ID:
`10314822840`

Actions-Artefakt-Container SHA-256:
`9b64ea297238d646a113ad7a8b4c9624da3d3359563a5130624134bbf5372d35`

## LOKALE KONTROLLE DES EXAKTEN ACTIONS-ARTEFAKTS

Das tatsächlich erzeugte Actions-Artefakt wurde heruntergeladen und lokal erneut geprüft.

PASS:
- äußerer Actions-Artefakt-Hash stimmt;
- innerer Plugin-ZIP-Hash stimmt mit `SHA256.txt` und Workflowlog überein;
- ZIP-Struktur gültig, genau ein Plugin-Top-Level;
- keine absoluten Pfade, kein `..`, keine Symlinks;
- lokaler 0.2.5↔0.2.6-Dateivergleich: exakt nur die zwei erlaubten Dateien geändert;
- Version 0.2.6 vorhanden;
- Schema 5 vorhanden;
- alte Version 0.2.5 im Pluginheader nicht vorhanden;
- Schema 4 im Core nicht vorhanden;
- fixe Mobile-Höhe `240px` nicht vorhanden;
- frühere globale Astra-/Entry-Content-Hacks nicht vorhanden;
- PHP-Lint aller 10 PHP-Dateien PASS.

Lokale Marker:
`LOCAL_ZIP_STRUCTURE_POSITIVE_NEGATIVE_PASS`
`LOCAL_EXACT_DELTA_POSITIVE_NEGATIVE_PASS`
`LOCAL_SOURCE_POSITIVE_NEGATIVE_PASS`
`LOCAL_PHP_LINT_PASS`

## GRENZE

Dieser Nachweis erlaubt eine technisch gebundene Testinstallation des exakt hashgebundenen 0.2.6-Kandidaten.

Er ist KEIN Pferde-Atelier-LIVE-PASS und keine Behauptung, dass die vom Nutzer beobachtete weiße Live-Seite exakt durch die reproduzierte Rewrite-Störung verursacht wurde. Der reale Pferde-Atelier-Readback/Sichttest bleibt erforderlich.
