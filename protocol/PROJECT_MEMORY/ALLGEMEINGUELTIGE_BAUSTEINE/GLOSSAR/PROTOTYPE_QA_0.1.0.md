# MOD-008 – PROTOTYP QA 0.1.0

STAND: 2026-09-12
STATUS: LOCAL PROTOTYPE PASS / KEIN WORDPRESS-LIVE-PASS

## Geprüft

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

Geprüft wurden zwei Konfigurationen mit demselben Core:
1. Pferde-Atelier-Profil mit Designwerten des bestehenden Designplugins;
2. fachfremdes Testportal `Lexikon` mit anderer URL-Basis, anderem SEO-Schema, anderer Farbe/Rundung und zusätzlichem Feld `Quellenhinweis`.

Ergebnis:
zweite Portalnutzung ohne Coreänderung im lokalen Vertrags-/Stubtest PASS.

Zusätzliche Konfliktprüfung:
- kein doppeltes Canonical durch eigene Ausgabe;
- Robots über WordPress-/Yoast-Schnittstellen statt zweitem Meta-Tag;
- keine doppelte Glossarausgabe bei bewusst gesetztem Shortcode;
- Import niemals Auto-Publish.

ZIP-Struktur:
- Single-Root PASS;
- Pflichtdateien PASS;
- Pluginheader PASS.

Aktueller Prototyp-ZIP SHA-256:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

## Noch NICHT bewiesen

- echter WordPress-Install/Upgrade;
- echte Permalink-Auflösung `/glossar/<begriff>/` neben vorhandener Seite `/glossar/`;
- echtes Backend mit Yoast in der Zielinstallation;
- echte Frontenddarstellung mit Astra/Pferde-Live-Theme;
- realer Import aus Campus-Wissensdatenbank;
- Performance mit realem größeren Begriffsbestand;
- zweites echtes WordPress-Portal statt Stub-Konfiguration.

Daher keine Release-/LIVE-Freigabe und Modulklasse bleibt formal UNGEKLÄRT / Ziel ALLGEMEINGÜLTIG.
