# UNIVERSAL GLOSSAR ENGINE – CURRENT_STATE

STAND: 2026-09-12
STATUS: V1-PROTOTYP / ECHTER WORDPRESS+MYSQL-SMOKE-TEST PASS / ASTRA+YOAST-REALTEST OFFEN

## Belastbarer Stand

- Modulname: `MOD-008 – Universal Glossar Engine`.
- Ziel: ein einziger projektunabhängiger WordPress-Core für mehrere Portale.
- Erste Projektanwendung: Pferde Atelier.
- Pferde-spezifische Begriffe, Oberbereiche, Texte, URL-Basis und SEO-Schemata sind nicht im Core hart verdrahtet.
- Projektkonfiguration liegt außerhalb des Fachkerns bzw. wird ausschließlich über Konfiguration/Filter gebunden.
- Eigener WordPress-Backendbereich `Glossar`.
- Glossarbegriffe als eigener Inhaltstyp, getrennt von normalen Beiträgen/Seiten.
- Oberbereiche getrennt von normalen WordPress-Kategorien und hierarchisch erweiterbar.
- Vorhandene WordPress-Seite als Glossar-Hauptseite auswählbar.
- Eigene Zieladresse je veröffentlichtem Begriff.
- Eigene SEO-Titel-/Meta-Description-Werte; providerneutraler Core mit optionaler Yoast-Brücke.
- Suchfeld, A–Z, Oberbereiche und Aufklapper vorhanden.
- Kein Bildzwang.
- Kein Auto-Publish.
- JSON-Import/Export vorhanden; Import ausschließlich als Entwurf und nur für erlaubte Felder.
- Feldschema erweiterbar, ohne bestehende Begriffe umzuschreiben.

## Prüfstand

Autoritativ:
`PROTOTYPE_QA_0.1.0.md`

Lokal belegt:
- PHP-Lint 8/8 PASS;
- statische Positiv-/Negativprüfung 15/15 PASS;
- Runtime-Stub-Vertragstest PASS;
- Pferde-Konfiguration PASS;
- fachfremde Zweitkonfiguration `Lexikon` PASS ohne Coreänderung;
- ZIP-Struktur PASS.

Echter WordPress/MySQL-Realtest:
- GitHub Actions Run `34699122729` → GESAMT PASS;
- Job `103567632899`: WordPress 6.9 / PHP 8.1.34 / MySQL 8.0 → PASS;
- Job `103567633008`: WordPress 7.1 / PHP 8.3.33 / MySQL 8.0 → PASS;
- Endmarker in beiden Jobs: `UGE_WORDPRESS_MYSQL_REAL_SMOKE_PASS`.

Real bestätigt:
- Plugin lässt sich aktivieren/deaktivieren/reaktivieren;
- vorhandene Glossar-Hauptseite `/glossar/` und Begriffszieladresse `/glossar/kolik/` funktionieren gleichzeitig;
- Suche, Oberbereich und veröffentlichter Begriff werden real ausgegeben;
- Entwürfe erscheinen nicht im Frontend;
- SEO-Titel, Meta-Description, Canonical und Noindex funktionieren ohne Yoast;
- JSON-Import/Export funktioniert;
- Import ignoriert unbekannte Felder;
- Import bleibt trotz `status=publish` im Eingang immer Entwurf;
- neues Feld über das erweiterbare Feldschema funktioniert ohne Coreänderung;
- reale Zweitkonfiguration `Lexikon` mit anderer URL-Basis, Bezeichnungen und Designwerten funktioniert ohne Coreänderung;
- Deaktivieren/Reaktivieren erhält Daten und Konfiguration;
- Glossarbegriffe erzeugen keine normalen WordPress-Seiten.

Prototyp-ZIP SHA-256 des lokal gebauten Vorläuferpakets:
`c8f58f0b144d286567a269d3fc26f09db36cb94446619528ff8b896d6b8682ee`

Wichtig:
Dieser Hash ist noch kein freigegebener Release-Installer. Vor Ausgabe wird ein finaler Kandidat neu paketiert und hashgebunden geprüft.

## Modulklasse

Formal weiterhin:
`UNGEKLÄRT / ZIEL ALLGEMEINGÜLTIG`.

Grund:
Der Core hat nun auch einen echten WordPress-Zweitkonfigurationstest bestanden. Für die formale Hochstufung bleibt aber ein separates zweites reales Portal sowie der vollständige Release-/Integrationsnachweis offen.

## Kritische Entscheidung

Keine parallele Pluginentwicklung.

`Core + Projektkonfiguration` ist technisch bestätigt tragfähig. Falls ein späteres reales Zweitportal eine unkonfigurierbare Projektspezifik beweist, wird nur ein kleiner Adapter ergänzt; kein vollständiger Fork.

## Noch offen

- echter Astra+Yoast-Kombinationstest;
- realer Import aus der Campus-Wissensdatenbank;
- größerer Bestands-/Performance-Test;
- finaler ZIP-Install-/Update-/Reinstall-Test des Release-Kandidaten;
- separates zweites echtes WordPress-Portal;
- Pferde-Atelier-LIVE-Installation.

Keine Release-/LIVE-Freigabe vor den für den Release-Kandidaten gebundenen Prüfungen.
