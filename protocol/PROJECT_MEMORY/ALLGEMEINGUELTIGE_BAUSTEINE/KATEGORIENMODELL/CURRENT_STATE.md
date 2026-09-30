# KATEGORIENMODELL – CURRENT STATE

STAND: 2026-09-30

## Status

MODULKLASSE:
**ALLGEMEINGÜLTIG**

Stabiler belegter Master:
**MASTER 016 – R10/R9 Runtime Deployment / V1.8.0**

Neuester allgemeingültiger Entwicklungsstand:
**V1.9.1 – Editorial Intent Ownership Handoff / lokal HARD PASS / Live-Abnahme offen**

## Technischer Zweck

WordPress-Plugin:
`Affiliate-Portal Kategorie-Workflow`

Allgemeingültiger SEO-/Affiliate-Kategorie-Workflow für:
- Content;
- HivePress/Marketplace;
- Journal auf explizit gebundener realer Taxonomie;
- verlustfreien Research-/Editorial-Handoff.

## Harte Architektur

- gleiche Pluginlinie; kein Companion-Plugin;
- 14-stufiger Kategorien-/Research-Kern bleibt read-only;
- `APKW_CONTENT_WRITE_CAPABILITY=false`;
- Post-FINAL-Writer bleibt getrennte Transaktionsschicht derselben Pluginlinie;
- keine automatische Taxonomieerzeugung;
- keine stillen Remaps;
- kein Auto-Delete;
- keine autonome Masteränderung.

## V1.9.1 – allgemeine Ergänzung

Der Kategorie-Workflow erzeugt keine Beiträge und keine Beitragstitel.

Er liefert für nachgelagerte Redaktionssysteme:
- stabile `concept_id`;
- Kategoriepfad und Block;
- Primärkeyword;
- Search Intent / `intent_key`;
- Research-Cluster;
- verlustfreien Residual-Research;
- explizite `ARTICLE_ONLY`-Entscheidungen;
- eindeutigen `owner_concept_id`, soweit fachlich gebunden.

Regel:
**Ein expliziter Artikel-Intent darf genau einem Kategorie-Owner gehören.**

Fehlende Artikel-Owner blockieren nur den Editorial-Handoff, nicht rückwirkend die Kategorienstruktur.

Semantische Dubletten-/Kannibalisierungsprüfung konkreter Artikel und finale Titel bleiben Downstream-Aufgabe.

## Prüfstand V1.9.1

- 248/248 PASS;
- Fresh-Unpack 248/248 PASS;
- Source PHP-Lint 18/18;
- Installer PHP-Lint 17/17;
- Source↔Installer Runtime 22/22 byteidentisch;
- Source-/Installer-Checksummen PASS.

## Release-Identitäten V1.9.1

Installer SHA-256:
`92c8b4ee6e1c53ce677b7a059766796c02afc9d39cdcd5f86511bf51b8808b1f`

Source SHA-256:
`7ccb6f45f2728466392b4a56e6fcda44e71265b7138cdb55be9921b4d576cc32`

## Beleggrenze

V1.9.1 ist noch nicht als vollständiger WordPress-Live-PASS belegt.

Der bisherige stabile Master V1.8.0 bleibt historische Masterbasis; V1.9.1 ist der aktuelle allgemeingültige Entwicklungskandidat derselben Linie.
