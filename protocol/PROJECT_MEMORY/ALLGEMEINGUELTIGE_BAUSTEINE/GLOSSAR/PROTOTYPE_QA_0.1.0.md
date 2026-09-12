# MOD-008 – PROTOTYP QA 0.1.0

STAND: 2026-09-12
STATUS: LOCAL PROTOTYPE PASS / KEIN WORDPRESS-LIVE-PASS

## Geprüft

PHP-Lint:
- 7/7 PHP-Dateien PASS.

Statische Positiv-/Negativprüfung:
- 13/13 PASS.
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
- kein Beitragsbild-Support.

Runtime-Stub-Vertragstest:
PASS.

Geprüft wurden zwei Konfigurationen mit demselben Core:
1. Pferde-Atelier-Profil mit Designwerten des bestehenden Designplugins;
2. fachfremdes Testportal `Lexikon` mit anderer URL-Basis, anderem SEO-Schema, anderer Farbe/Rundung und zusätzlichem Feld `Quellenhinweis`.

Ergebnis:
zweite Portalnutzung ohne Coreänderung PASS.

Zusätzliche Konfliktprüfung nach Erstlauf:
- kein doppeltes Canonical durch eigene Ausgabe;
- Robots über WordPress-/Yoast-Schnittstellen statt zweitem Meta-Tag;
- keine doppelte Glossarausgabe bei bewusst gesetztem Shortcode.

ZIP-Struktur:
- Single-Root PASS;
- Pflichtdateien PASS;
- Pluginheader PASS.

Aktueller Prototyp-ZIP SHA-256:
`1405e0cd5b0c9a3db113e69c75ca478fc0b367e163d9eb7bd7c2f33eb7c74ab5`

## Noch NICHT bewiesen

- echter WordPress-Install/Upgrade;
- echte Permalink-Auflösung `/glossar/<begriff>/` neben vorhandener Seite `/glossar/`;
- echtes Backend mit Yoast in der Zielinstallation;
- echte Frontenddarstellung mit Astra/Pferde-Live-Theme;
- Datenimport aus Campus-Wissensdatenbank;
- Performance mit realem größeren Begriffsbestand.

Daher keine Release-/LIVE-Freigabe.
