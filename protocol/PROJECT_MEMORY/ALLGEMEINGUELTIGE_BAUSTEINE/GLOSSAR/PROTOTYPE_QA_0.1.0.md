# MOD-008 – PROTOTYP QA 0.1.0

STAND: 2026-09-12
STATUS: LOCAL PASS + ECHTER WORDPRESS/MYSQL-SMOKE-TEST PASS / KEIN PFERDE-LIVE-PASS

## Lokale Prüfung

PHP-Lint:
- 8/8 PHP-Dateien PASS.

Statische Positiv-/Negativprüfung:
- 15/15 PASS.
- keine Pferde-Fachbegriffe im Core;
- kein Auto-Publish;
- eigener Inhaltstyp;
- eigene Glossar-Gruppen;
- Feldschema erweiterbar;
- Konfiguration filterbar;
- Designtokens filterbar;
- Yoast nur optional;
- keine direkten Yoast-Metafeld-Writes;
- Hauptseite konfigurierbar;
- URL-Basis konfigurierbar;
- SEO-Schemata konfigurierbar;
- kein Beitragsbild-Support;
- strukturierter JSON-Import/Export vorhanden;
- Import übernimmt nur erlaubte Felder und legt Begriffe ausschließlich als Entwurf an.

Runtime-Stub-Vertragstest:
PASS.

Lokal geprüft wurden zwei Konfigurationen mit demselben Core:
1. Pferde-Atelier-Profil;
2. fachfremdes Testportal `Lexikon` mit anderer URL-Basis, Bezeichnungen, Designwerten und zusätzlichem Feld.

ZIP-Struktur des lokalen Vorläuferpakets:
- Single-Root PASS;
- Pflichtdateien PASS;
- Pluginheader PASS.

Prototyp-ZIP SHA-256 des lokalen Vorläuferpakets:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

## Echter WordPress/MySQL-Realtest

Workflow:
`.github/workflows/glossar-v1-wordpress-smoke.yml`

Erster Lauf:
Run `34699017775` → FAIL ausschließlich wegen falscher Testannahme „genau zwei veröffentlichte Seiten“. WordPress erzeugt bei Neuinstallation bereits eine Sample Page. Plugin-Stufen davor waren PASS. Plugin-Code wurde für die Korrektur nicht verändert.

Korrigierter vollständiger Lauf:
Run `34699122729` → GESAMT PASS.

Matrix 1:
- Job `103567632899`;
- WordPress 6.9;
- PHP 8.1.34;
- MySQL 8.0;
- Endmarker `UGE_WORDPRESS_MYSQL_REAL_SMOKE_PASS`.

Matrix 2:
- Job `103567633008`;
- WordPress 7.1;
- PHP 8.3.33;
- MySQL 8.0;
- Endmarker `UGE_WORDPRESS_MYSQL_REAL_SMOKE_PASS`.

## Real positiv/negativ bestätigt

- echte WordPress-Installation + Pluginaktivierung PASS;
- `/glossar/` als reale WordPress-Seite PASS;
- `/glossar/kolik/` als eigene Begriffszieladresse parallel dazu PASS;
- Suchfeld/Oberbereich/veröffentlichter Begriff im realen HTML PASS;
- Entwurf im Frontend NICHT sichtbar PASS;
- SEO-Titel PASS;
- Meta-Description ohne Yoast PASS;
- eigener Canonical PASS;
- Noindex PASS;
- JSON-Import PASS;
- Eingang mit `status=publish` wird trotzdem als `draft` gespeichert PASS;
- unbekanntes Importfeld wird nicht gespeichert PASS;
- JSON-Export PASS;
- zusätzliches Feld über `uge_field_schema` ohne Coreänderung PASS;
- zweite reale Konfiguration `Lexikon` mit `/lexikon/` + `/lexikon/testwort/` ohne Coreänderung PASS;
- Deaktivieren/Reaktivieren erhält Daten und Konfiguration PASS;
- Anzahl normaler Seiten bleibt durch Deaktivieren/Reaktivieren unverändert PASS;
- importierter Glossarbegriff bleibt `uge_term` und erzeugt keine normale WordPress-Seite PASS.

## Zusätzliche Konfliktprüfung

- kein eigenes zweites Canonical-Tag im Fallbackweg;
- Robots über WordPress-/Yoast-Schnittstellen statt blindem zweiten Robots-Meta;
- keine doppelte Glossarausgabe bei bewusst gesetztem Shortcode;
- Import niemals Auto-Publish.

## Noch NICHT bewiesen

- Astra + Yoast gemeinsam im echten Testsystem;
- realer Import der vorhandenen Campus-Glossardatensätze;
- Performance mit realem größeren Begriffsbestand;
- finaler Release-ZIP Install-/Update-/Reinstall-Test;
- separates zweites reales WordPress-Portal;
- Pferde-Atelier-LIVE-Installation.

Daher noch keine Release-/LIVE-Freigabe. Modulklasse bleibt formal `UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.
